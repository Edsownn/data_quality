from datetime import date, datetime

from sqlalchemy import TEXT, Boolean, Date, String, Text, Integer, BigInteger, JSON, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime


class Base(DeclarativeBase):
    pass


class ArquivosUpload(Base):
    __tablename__ = "arquivos_upload"
    __table_args__ = {"schema": "public"}

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    nome_original: Mapped[str] = mapped_column(Text, nullable=False)
    chave_s3: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    tamanho: Mapped[int] = mapped_column(BigInteger, nullable=True)
    mime: Mapped[str] = mapped_column(String(255), nullable=True)
    usuario: Mapped[str] = mapped_column(String(255), nullable=True)
    dt_upload: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    dt_validacao: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    dt_importacao: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    stats: Mapped[dict] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ArquivosErros(Base):
    __tablename__ = "arquivos_erros"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    arquivo_id: Mapped[str] = mapped_column(String(36), ForeignKey("public.arquivos_upload.id"), nullable=False)
    codigo: Mapped[str] = mapped_column(Text, nullable=True)
    descricao_codigo: Mapped[str] = mapped_column(Text, nullable=True)
    mensagem: Mapped[str] = mapped_column(Text, nullable=True)
    planilha: Mapped[str] = mapped_column(Text, nullable=True)
    linha: Mapped[int] = mapped_column(Integer, nullable=True)
    coluna: Mapped[str] = mapped_column(Text, nullable=True)
    tipo: Mapped[str] = mapped_column(Text, nullable=True)
    severidade: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Attachments(Base):
    __tablename__ = "attachments"
    __table_args__ = {"schema": "public"}

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    ref_tipo: Mapped[str] = mapped_column(Text, nullable=False)
    ref_id: Mapped[str] = mapped_column(Text, nullable=False)
    arquivo_id: Mapped[str] = mapped_column(String(36), ForeignKey("public.arquivos_upload.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())