import json
import sqlite3
from enum import Enum
from typing import Any, Dict, List, Self, Tuple, Union
from urllib.parse import quote_plus

import pandas as pd
import psycopg
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from .dw_model import Base
from .util import logger, settings


class DatabaseType(Enum):
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"


class Operator:
    """Table helper for database operations."""

    def __init__(
        self,
        table: str = "table_default",
        db_type: DatabaseType = DatabaseType.POSTGRESQL,
        database: str = "default",
        key_field: str = "integration_code",
    ):
        """
        Table helper for database operations.

        Args:
            table (str, optional): Defaults to "table_default".
            db_type (DatabaseType, optional): Defaults to DatabaseType.POSTGRESQL.
            database (str, optional): Defaults to "default".
            key_field (str, optional): Defaults to "integration_code".


        Returns:
            None
        """
        self.key_field = key_field
        self.table = table
        self.db_type = db_type
        if db_type == DatabaseType.SQLITE and (not database or database == "default"):
            database = settings.DATABASE_LOCAL_SQLITE
        self.database = database
        self.conn = self.create_connection()

    def create_connection(self) -> Union[sqlite3.Connection, psycopg.Connection]:
        """Create a database connection based on the specified type and database name.
        Args:
            database: Name of the database configuration to use (from settings), for PostgreSQL db_name or file path for SQLite.
        Returns:
            Union[sqlite3.Connection, psycopg.Connection]: Connection object to the database.
        """
        _database = self.database
        # SQLite path fallback
        if self.db_type == DatabaseType.SQLITE:
            if not _database or _database == "default":
                # prefer explicit setting, otherwise use app data dir
                sqlite_path = settings.get("DATABASE_LOCAL_SQLITE") or (settings.get("APP_DATA_DIR") + "/local.db")
                _database = sqlite_path
            return sqlite3.connect(_database)

        # PostgreSQL: use settings.get to avoid KeyError; if any required key is missing, fall back to local sqlite
        elif self.db_type == DatabaseType.POSTGRESQL:
            user = settings.get(f"DATABASE_{_database.upper()}_USER")
            password = settings.get(f"DATABASE_{_database.upper()}_PASSWORD")
            host = settings.get(f"DATABASE_{_database.upper()}_HOST")
            port = settings.get(f"DATABASE_{_database.upper()}_PORT")
            db_name = settings.get(f"DATABASE_{_database.upper()}_DB")

            missing = [k for k, v in (
                ("user", user), ("password", password), ("host", host), ("port", port), ("db", db_name)
            ) if not v]
            if missing:
                logger.warning(f"Postgres config incomplete for '{_database}' ({missing}); falling back to local sqlite for development.")
                sqlite_path = settings.get("DATABASE_LOCAL_SQLITE") or (settings.get("APP_DATA_DIR") + "/local.db")
                return sqlite3.connect(sqlite_path)

            return psycopg.connect(
                dbname=db_name,
                user=user,
                password=password,
                host=host,
                port=port,
                application_name="dw_import",
            )

    def create_engine(self) -> Engine:
        """Create a SQLAlchemy engine for PostgreSQL or SQLite based on the database configuration.
        Returns:
            Engine: SQLAlchemy engine object.
        """
        _database = self.database
        if self.db_type == DatabaseType.SQLITE:
            return create_engine(f"sqlite:///{self.database}")
        elif self.db_type == DatabaseType.POSTGRESQL:
            return create_engine(
                f"postgresql+psycopg://{settings[f"DATABASE_{_database.upper()}_USER"]}:{quote_plus(
                    settings[f"DATABASE_{_database.upper()}_PASSWORD"]
                )}@{settings[f"DATABASE_{_database.upper()}_HOST"]}:{settings[f"DATABASE_{_database.upper()}_PORT"]}/{settings[f"DATABASE_{_database.upper()}_DB"]}",
            )

    def create_table(self, model: Base) -> Self:
        """Create a table in the database based on the SQLAlchemy model.
        Args:
            model: SQLAlchemy model class (subclass of Base)
            database: Name of the database to create the table in (default: “default”)
        """
        engine = self.create_engine()
        logger.info(f"Creating table: {model.__table__}")
        Base.metadata.create_all(engine, tables=[model.__table__], checkfirst=True)
        return self

    def generate_upsert_query(
        self,
        data: Dict[str, Any],
        updated_at_field: str = "updated_at",
        exclude_update_columns: Tuple[str, ...] = ("id", "created_at", "created_at"),
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Generate an UPSERT query with a conditional UPDATE only when any monitored fields changed.
        The updated_at_field will set to now() on an update.

        Args:
            table: Table name.
            key_field: Column used for ON CONFLICT.
            data: Dict of column:value for insert/update.
            updated_at_field: Column name to set to now() on update.
            exclude_update_columns: Columns excluded from update checks.

        Returns:
            Tuple of (query, parameters dict).
        """
        # Keys excluding key_field and excluded columns
        update_columns = [
            col
            for col in data.keys()
            if col not in exclude_update_columns and col != self.key_field
        ]

        insert_columns = list(data.keys())

        # Build SET clause (include updated_at) for update when there are columns to update
        set_parts = [f"{col} = EXCLUDED.{col}" for col in update_columns]
        set_parts.append(f"{updated_at_field} = CURRENT_TIMESTAMP")
        set_clause = ",\n    ".join(set_parts)

        # Build WHERE clause - true if any monitored column differs from EXCLUDED
        where_conditions = [
            f"{self.table}.{col} IS DISTINCT FROM EXCLUDED.{col}"
            for col in update_columns
        ]
        where_clause = (
            " OR\n       ".join(where_conditions) if where_conditions else "FALSE"
        )

        if self.db_type == DatabaseType.SQLITE:
            insert_placeholders = [f":{col}" for col in insert_columns]
            query = (
                f"INSERT INTO {self.table} ({', '.join(insert_columns)}) \n"
                f"VALUES ({', '.join(insert_placeholders)}) \n"
                f"ON CONFLICT ({self.key_field}) DO UPDATE SET \n"
                f"{set_clause} \n"
                f"WHERE {where_clause};"
            )
            return query, data
        else:
            # PostgreSQL
            insert_placeholders = [f"%({col})s" for col in insert_columns]
            query = (
                f"INSERT INTO {self.table} ({', '.join(insert_columns)}) \n"
                f"VALUES ({', '.join(insert_placeholders)}) \n"
                f"ON CONFLICT ({self.key_field}) DO UPDATE \n"
                f"SET {set_clause} \n"
                f"WHERE {where_clause} \n"
                f"RETURNING (xmax = 0) AS inserted;"
            )
            return query, data

    def generate_insert_query(
        self,
        data: Dict[str, Any],
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Generate an INSERT query for the given data.

        Args:
            data: Dict of column:value for insert.

        Returns:
            Tuple of (query, parameters dict).
        """
        columns = list(data.keys())
        

        if self.db_type == DatabaseType.SQLITE:
            placeholders = [f":{col})" for col in columns]
            query = (
                f"INSERT INTO {self.table} ({', '.join(columns)}) \n"
                f"VALUES ({', '.join(placeholders)});"
            )
            return query, data
        else: # PostgreSQL
            placeholders = [f"%({col})s" for col in columns]
            query = (
                f"INSERT INTO {self.table} ({', '.join(columns)}) \n"
                f"VALUES ({', '.join(placeholders)}) \n"
                f"RETURNING (xmax = 0) AS inserted;"
            )
            return query, data

    def delete(self, conditions: Dict[str, Any] = None) -> Self:
        """
        Delete records from the table based on conditions.
        If no conditions are provided, all records will be deleted.
        Args:
            conditions: Dict of column:value for deletion conditions.
        """
        query = f"DELETE FROM {self.table}"
        if conditions:
            where_clause = " AND ".join(
                [f"{col} = %({col})s" for col in conditions.keys()]
            )
            query += f" WHERE {where_clause};"

        with self.conn.cursor() as cur:
            cur.execute(query, conditions)
            self.conn.commit()
        logger.info(f"[DELETE] Records deleted from {self.table} where {conditions}")
        return self

    def insert(
        self,
        records: Union[List[Dict], pd.DataFrame],
    ) -> Self:
        """
        Insert records into the table.
        Args:
            records: List of dictionaries or DataFrame to insert.
        """
        if isinstance(records, pd.DataFrame):
            records = records.to_dict(orient="records")
        if not records:
            raise ValueError("No records to insert.")
        logger.info(
            f"Starting insert for {len(records)} records into table '{self.table}'"
        )

        _inserted = 0
        _rollbacks = 0
        for idx, data in enumerate(records):
            query, params = self.generate_insert_query(data)
            logger.debug(f"Inserting record {idx+1}: {params}")
            if self.db_type == DatabaseType.SQLITE:
                cur = self.conn.cursor()
                try:
                    cur.execute(query, params)
                    _inserted += 1
                except sqlite3.Error as e:
                    logger.error(f"Error inserting record {idx+1}: {e}")
                    _rollbacks += 1
                    continue
            else:  # PostgreSQL
                try:
                    with self.conn.cursor() as cur:
                        cur.execute(query, params)
                        self.conn.commit()
                        _inserted += 1
                except psycopg.Error as e:
                    logger.error(f"Error inserting record {idx+1}: {e}")
                    self.conn.rollback()
                    _rollbacks += 1
                    continue
        logger.info(
            f"[INSERT] Inserted data into table '{self.table}'\n{json.dumps({'inserted': _inserted, 'rollbacks': _rollbacks, 'total': len(records)}, indent=2,)}"
        )
        return self

    def upsert(
        self,
        records: Union[List[Dict], pd.DataFrame],
    ) -> Self:
        """
        Upsert using a generated query with conditional update.
        Logs progress and wrap execution in a transaction.
        """
        if isinstance(records, pd.DataFrame):
            records = records.to_dict(orient="records")

        logger.info(
            f"Starting upsert for {len(records)} records into table '{self.table}'"
        )
        _inserted = 0
        _updated = 0
        _rollbacks = 0
        for idx, data in enumerate(records):
            query, params = self.generate_upsert_query(data)
            logger.debug(f"Upserting record {idx+1}: {params}")
            if self.db_type == DatabaseType.SQLITE:
                cur = self.conn.cursor()
                try:
                    cur.execute(query, params)
                    _updated += 1
                except sqlite3.Error as e:
                    logger.error(f"Error upserting record {idx+1}: {e}")
                    _rollbacks += 1
                    continue
            else:  # PostgreSQL
                try:
                    with self.conn.cursor() as cur:
                        cur.execute(query, params)
                        result = cur.fetchone()
                        was_inserted = result
                        if was_inserted:
                            _inserted += 1
                        else:
                            _updated += 1
                        self.conn.commit()
                except psycopg.Error as e:
                    logger.error(f"Error upserting record {idx+1}: {e}")
                    self.conn.rollback()
                    _rollbacks += 1
                    continue
        stats = {
            "inserted": _inserted,
            "updated": _updated,
            "rollbacks": _rollbacks,
            "total": len(records),
        }
        logger.info(
            f"[STATS] Upsert executed for {len(records)} records into table '{self.table}'\n{json.dumps(stats, indent=2)}"
        )
        return self

    # Check if table exists otherwise create it
    def _table_exists(self) -> bool:
        with self.conn.cursor() as cur:
            cur.execute(
                f"""
                    SELECT EXISTS(
                        SELECT
                            TRUE
                        FROM
                            information_schema."tables" t
                        WHERE
                            t.table_schema = '{settings[f"DATABASE_{self.database.upper()}_SCHEMA"]}'
                            AND t.table_name = '{self.table}';
                    );
                """
            )
            exists = cur.fetchone()[0]

            if not exists:
                logger.info(f"Table '{self.table}' does not exist. Creating it.")
                return False

            logger.info(f"Table '{self.table}' already exists.")
            return True

    def create_table_from_df(self, df: pd.DataFrame) -> Self:
        """
        Create a table based on DataFrame schema if it does not exist.
        """
        if self._table_exists():
            return

        # Map pandas dtypes to PostgreSQL types
        dtype_mapping = {
            "object": "TEXT",
            "int64": "BIGINT",
            "float64": "NUMERIC(18,6)",
            "bool": "BOOLEAN",
            "datetime64[ns]": "TIMESTAMP",
            "category": "TEXT",
            "string": "TEXT",
            "date": "DATE",
            "timedelta[ns]": "INTERVAL",
            "int32": "BIGINT",
            "float32": "NUMERIC(18,6)",
            "int16": "BIGINT",
            "int8": "BIGINT",
            "uint8": "BIGINT",
            "uint16": "BIGINT",
            "uint32": "BIGINT",
            "uint64": "BIGINT",
            "complex64": "TEXT",
            "complex128": "TEXT",
            "bytes": "BYTEA",
        }

        columns = []
        for col, dtype in df.dtypes.items():
            pg_type = dtype_mapping.get(str(dtype), "TEXT")
            columns.append(f"{col} {pg_type}")

        create_table_query = f"""
        CREATE TABLE {self.table} (
            id BIGSERIAL PRIMARY KEY,
            {', '.join(columns)}
        );
        """

        with self.conn.cursor() as cur:
            cur.execute(create_table_query)
            self.conn.commit()
        logger.info(f"Table '{self.table}' created successfully.")
        return self
