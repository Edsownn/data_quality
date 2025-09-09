from datetime import date, datetime

from sqlalchemy import TEXT, Boolean, Date, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime


class Base(DeclarativeBase):
    pass

class Exames(Base):
    __tablename__ = "soc_exames"
    __table_args__ = {"schema": "dw"}

    id: Mapped[int] = mapped_column(primary_key=True)
    cod: Mapped[str] = mapped_column(String(255), nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=True)
    ativo: Mapped[str] = mapped_column(String(255), nullable=True)
    integration_code: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class Cargos(Base):
    __tablename__ = "soc_cargos"
    __table_args__ = {"schema": "dw"}

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo_empresa: Mapped[str] = mapped_column(String(255), nullable=False)
    nome_empresa: Mapped[str] = mapped_column(String(255), nullable=True)
    codigo_cargo: Mapped[str] = mapped_column(String(255), nullable=False)
    nome_cargo: Mapped[str] = mapped_column(String(255), nullable=False)
    codigo_rh_cargo: Mapped[str] = mapped_column(String(255), nullable=True)
    cargo_ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    funcao: Mapped[str] = mapped_column(String(255), nullable=True)
    gfip: Mapped[str] = mapped_column(String(10), nullable=True)
    descricao_detalhada: Mapped[str] = mapped_column(TEXT, nullable=True)
    cbo: Mapped[str] = mapped_column(String(255), nullable=True)
    integration_code: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class Empresas(Base):
    __tablename__ = "soc_empresas"
    __table_args__ = {"schema": "dw"}

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(String(255), nullable=False)
    nome_abreviado: Mapped[str] = mapped_column(String(255), nullable=False)
    razao_social_inicial: Mapped[str] = mapped_column(String(255), nullable=True)
    razao_social: Mapped[str] = mapped_column(String(255), nullable=False)
    endereco: Mapped[str] = mapped_column(String(255), nullable=True)
    numero_endereco: Mapped[str] = mapped_column(String(255), nullable=True)
    complemento_endereco: Mapped[str] = mapped_column(String(255), nullable=True)
    bairro: Mapped[str] = mapped_column(String(255), nullable=True)
    cidade: Mapped[str] = mapped_column(String(255), nullable=True)
    uf: Mapped[str] = mapped_column(String(2), nullable=True)
    cep: Mapped[str] = mapped_column(String(10), nullable=True)
    cnpj: Mapped[str] = mapped_column(String(18), nullable=True)
    inscricao_estadual: Mapped[str] = mapped_column(String(20), nullable=True)
    inscricao_municipal: Mapped[str] = mapped_column(String(20), nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    codigo_cliente_integracao: Mapped[str] = mapped_column(String(50), nullable=True)
    codigo_cliente_int: Mapped[str] = mapped_column(String(50), nullable=True)
    integration_code: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class ExamesGeral(Base):
    __tablename__ = "soc_exames_geral"
    __table_args__ = {"schema": "dw"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    empresa: Mapped[str] = mapped_column(String(255), nullable=False)
    nome_empresa: Mapped[str] = mapped_column(String(255), nullable=True)
    data_ficha: Mapped[datetime] = mapped_column(Date, nullable=True)
    data_resultado: Mapped[datetime] = mapped_column(Date, nullable=True)
    tipo_exame: Mapped[str] = mapped_column(String(255), nullable=True)
    data_exame: Mapped[datetime] = mapped_column(Date, nullable=True)
    cod_exame: Mapped[str] = mapped_column(String(255), nullable=True)
    nome_exame: Mapped[str] = mapped_column(String(255), nullable=True)
    exame_alterado: Mapped[str] = mapped_column(String(255), nullable=True)
    cpf_medico_examinador: Mapped[str] = mapped_column(String(14), nullable=True)
    nome_medico_examinador: Mapped[str] = mapped_column(String(255), nullable=True)
    codigo_prestador: Mapped[str] = mapped_column(String(255), nullable=True)
    nome_prestador: Mapped[str] = mapped_column(String(255), nullable=True)
    uf: Mapped[str] = mapped_column(String(2), nullable=True)
    cidade_prestador: Mapped[str] = mapped_column(String(255), nullable=True)
    integration_code: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

class Funcionarios(Base):
    __tablename__ = "soc_funcionarios"
    __table_args__ = {"schema": "dw"}

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo_empresa: Mapped[str] = mapped_column(String(255), nullable=False)
    nome_empresa: Mapped[str] = mapped_column(String(255), nullable=True)
    codigo: Mapped[str] = mapped_column(String(255), nullable=False)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    codigo_unidade: Mapped[str] = mapped_column(String(255), nullable=True)
    nome_unidade: Mapped[str] = mapped_column(String(255), nullable=True)
    codigo_setor: Mapped[str] = mapped_column(String(255), nullable=True)
    nome_setor: Mapped[str] = mapped_column(String(255), nullable=True)
    codigo_cargo: Mapped[str] = mapped_column(String(255), nullable=True)
    nome_cargo: Mapped[str] = mapped_column(String(255), nullable=True)
    cbo_cargo: Mapped[str] = mapped_column(String(255), nullable=True)
    matricula_funcionario: Mapped[str] = mapped_column(String(255), nullable=True)
    cpf_funcionario: Mapped[str] = mapped_column(String(255), nullable=True)
    situacao: Mapped[str] = mapped_column(String(255), nullable=True)
    data_nascimento: Mapped[str] = mapped_column(String(255), nullable=True)
    data_admissao: Mapped[str] = mapped_column(String(255), nullable=True)
    data_demissao: Mapped[str] = mapped_column(String(255), nullable=True)
    endereco: Mapped[str] = mapped_column(String(255), nullable=True)
    numero_endereco: Mapped[str] = mapped_column(String(255), nullable=True)
    bairro: Mapped[str] = mapped_column(String(255), nullable=True)
    uf: Mapped[str] = mapped_column(String(255), nullable=True)
    email_corporativo: Mapped[str] = mapped_column(String(255), nullable=True)
    email_pessoal: Mapped[str] = mapped_column(String(255), nullable=True)
    telefone_celular: Mapped[str] = mapped_column(String(255), nullable=True)
    data_cadastro: Mapped[str] = mapped_column(String(255), nullable=True)
    
    integration_code: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

class ExamesPorEmpresa(Base):
    __tablename__ = "soc_exames_por_empresa"
    __table_args__ = {"schema": "dw"}

    id: Mapped[int] = mapped_column(primary_key=True)
    empresa: Mapped[str] = mapped_column(String(255), nullable=True)
    cod_funcionario: Mapped[str] = mapped_column(String(255), nullable=True)
    nome_funcionario: Mapped[str] = mapped_column(String(255), nullable=True)
    matricula: Mapped[str] = mapped_column(String(255), nullable=True)
    data_ficha: Mapped[datetime] = mapped_column(Date, nullable=True)
    tipo_ficha: Mapped[str] = mapped_column(String(255), nullable=True)
    data_exame: Mapped[datetime] = mapped_column(Date, nullable=True)
    cod_exame: Mapped[str] = mapped_column(String(255), nullable=True)
    nome_exame: Mapped[str] = mapped_column(String(255), nullable=True)
    exame_alterado: Mapped[str] = mapped_column(String(255), nullable=True)
    sai_aso: Mapped[str] = mapped_column(String(255), nullable=True)
    unidade: Mapped[str] = mapped_column(String(255), nullable=True)
    setor: Mapped[str] = mapped_column(String(255), nullable=True)
    cargo: Mapped[str] = mapped_column(String(255), nullable=True)
    cpf: Mapped[str] = mapped_column(String(255), nullable=True)
    codigo_sequencial_ficha: Mapped[str] = mapped_column(String(255), nullable=True)
    codigo_sequencial_resultado: Mapped[str] = mapped_column(String(255), nullable=True)
    parecer_aso: Mapped[str] = mapped_column(String(255), nullable=True)

    integration_code: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

class Setores(Base):
    __tablename__ = "soc_setores"
    __table_args__ = {"schema": "dw"}

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo_empresa: Mapped[str] = mapped_column(String(255), nullable=False)
    nome_empresa: Mapped[str] = mapped_column(String(255), nullable=True)
    codigo_setor: Mapped[str] = mapped_column(String(255), nullable=False)
    nome_setor: Mapped[str] = mapped_column(String(255), nullable=False)
    codigo_rh_setor: Mapped[str] = mapped_column(String(255), nullable=True)
    setor_ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    integration_code: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

class Ged(Base):
    __tablename__ = "soc_ged"
    __table_args__ = {"schema": "dw"}

    id: Mapped[int] = mapped_column(primary_key=True)
    cd_empresa: Mapped[str] = mapped_column(String(255), nullable=True)
    cd_unidade: Mapped[str] = mapped_column(String(255), nullable=True)
    cd_ged: Mapped[str] = mapped_column(String(255), nullable=True)
    nm_ged: Mapped[str] = mapped_column(String(255), nullable=True)
    dt_validade: Mapped[datetime] = mapped_column(Date, nullable=True)
    dt_emissao: Mapped[datetime] = mapped_column(Date, nullable=True)
    ic_criado_socnet: Mapped[str] = mapped_column(String(255), nullable=True)
    cd_funcionario: Mapped[str] = mapped_column(String(255), nullable=True)
    data_ficha: Mapped[datetime] = mapped_column(Date, nullable=True)
    tipo_ficha: Mapped[str] = mapped_column(String(255), nullable=True)
    cd_arquivo_ged: Mapped[str] = mapped_column(String(255), nullable=True)
    nm_arquivos_ged: Mapped[str] = mapped_column(String(255), nullable=True)
    assinado_digitalmente: Mapped[str] = mapped_column(String(255), nullable=True)
    cd_tipo_ged: Mapped[str] = mapped_column(String(255), nullable=True)
    sequencial_ficha: Mapped[str] = mapped_column(String(255), nullable=True)
    nome_funcionario: Mapped[str] = mapped_column(String(255), nullable=True)
    cpf_funcionario: Mapped[str] = mapped_column(String(255), nullable=True)
    matricula_funcionario: Mapped[str] = mapped_column(String(255), nullable=True)
    unidade: Mapped[str] = mapped_column(String(255), nullable=True)
    dt_upload_arquivo: Mapped[datetime] = mapped_column(Date, nullable=True)
    observacao: Mapped[str] = mapped_column(TEXT, nullable=True)
    hr_upload_arquivo: Mapped[str] = mapped_column(String(255), nullable=True)

    integration_code: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

class Prestadores(Base):
    __tablename__ = "soc_prestadores"
    __table_args__ = {"schema": "dw"}

    id: Mapped[int] = mapped_column(primary_key=True)
    socnet: Mapped[str] = mapped_column(String(255), nullable=True)
    codigo_prestador: Mapped[str] = mapped_column(String(255), nullable=True)
    situacao: Mapped[str] = mapped_column(String(255), nullable=True)
    status_contrato: Mapped[str] = mapped_column(String(255), nullable=True)
    bairro: Mapped[str] = mapped_column(String(255), nullable=True)
    cidade: Mapped[str] = mapped_column(String(255), nullable=True)
    estado: Mapped[str] = mapped_column(String(2), nullable=True)
    endereco: Mapped[str] = mapped_column(String(255), nullable=True)
    numero_endereco: Mapped[str] = mapped_column(String(255), nullable=True)
    complemento_endereco: Mapped[str] = mapped_column(String(255), nullable=True)
    cep: Mapped[str] = mapped_column(String(20), nullable=True)
    representante_legal: Mapped[str] = mapped_column(String(255), nullable=True)
    cnpj: Mapped[str] = mapped_column(String(20), nullable=True)
    cpf: Mapped[str] = mapped_column(String(14), nullable=True)
    codigo_agencia_banco: Mapped[str] = mapped_column(String(50), nullable=True)
    codigo_banco: Mapped[str] = mapped_column(String(50), nullable=True)
    nome_banco: Mapped[str] = mapped_column(String(255), nullable=True)
    numero_conta_corrente: Mapped[str] = mapped_column(String(50), nullable=True)
    nome_titular_conta: Mapped[str] = mapped_column(String(255), nullable=True)
    data_cancelamento: Mapped[str] = mapped_column(String(255), nullable=True)  # date parsed in ETL
    data_contratacao: Mapped[str] = mapped_column(String(255), nullable=True)    # date parsed in ETL
    dia_pagamento: Mapped[str] = mapped_column(String(10), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    horario_atendimento_inicial: Mapped[str] = mapped_column(String(20), nullable=True)
    horario_atendimento_final: Mapped[str] = mapped_column(String(20), nullable=True)
    motivo_cancelamento: Mapped[str] = mapped_column(String(255), nullable=True)
    nome_prestador: Mapped[str] = mapped_column(String(255), nullable=True)
    razao_social: Mapped[str] = mapped_column(String(255), nullable=True)
    telefone: Mapped[str] = mapped_column(String(50), nullable=True)
    celular: Mapped[str] = mapped_column(String(50), nullable=True)
    tipo_atendimento: Mapped[str] = mapped_column(String(255), nullable=True)
    tipo_pagamento: Mapped[str] = mapped_column(String(255), nullable=True)
    tipo_prestador: Mapped[str] = mapped_column(String(255), nullable=True)
    tipo_pessoa: Mapped[str] = mapped_column(String(255), nullable=True)
    regra_padrao_pagamento: Mapped[str] = mapped_column(String(255), nullable=True)
    codigo_rh: Mapped[str] = mapped_column(String(255), nullable=True)
    nivel_classificacao: Mapped[str] = mapped_column(String(255), nullable=True)
    responsavel: Mapped[str] = mapped_column(String(255), nullable=True)
    pagamento_antecipado: Mapped[str] = mapped_column(String(255), nullable=True)
    conselho_classe: Mapped[str] = mapped_column(String(255), nullable=True)
    uf_conselho_classe: Mapped[str] = mapped_column(String(2), nullable=True)
    especialidade_responsavel: Mapped[str] = mapped_column(String(255), nullable=True)
    especialidade_responsavel2: Mapped[str] = mapped_column(String(255), nullable=True)
    campanha: Mapped[str] = mapped_column(String(255), nullable=True)
    ambulatorio: Mapped[str] = mapped_column(String(255), nullable=True)

    integration_code: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

class Unidades(Base):
    __tablename__ = "soc_unidades"
    __table_args__ = {"schema": "dw"}

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo_empresa: Mapped[str] = mapped_column(String(255), nullable=False)
    nome_empresa: Mapped[str] = mapped_column(String(255), nullable=True)
    codigo_unidade: Mapped[str] = mapped_column(String(255), nullable=False)
    nome_unidade: Mapped[str] = mapped_column(String(255), nullable=False)
    codigo_rh_unidade: Mapped[str] = mapped_column(String(255), nullable=True)
    grau_risco_unidade: Mapped[str] = mapped_column(String(255), nullable=True)
    unidade_ativa: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    cnpj_unidade: Mapped[str] = mapped_column(String(20), nullable=True)
    inscricao_estadual_unidade: Mapped[str] = mapped_column(String(255), nullable=True)
    codigo_cliente_integracao: Mapped[str] = mapped_column(String(255), nullable=True)
    endereco: Mapped[str] = mapped_column(String(255), nullable=True)
    numero_endereco: Mapped[str] = mapped_column(String(255), nullable=True)
    complemento: Mapped[str] = mapped_column(String(255), nullable=True)
    bairro: Mapped[str] = mapped_column(String(255), nullable=True)
    cidade: Mapped[str] = mapped_column(String(255), nullable=True)
    uf: Mapped[str] = mapped_column(String(2), nullable=True)
    cep: Mapped[str] = mapped_column(String(20), nullable=True)
    cpf_unidade: Mapped[str] = mapped_column(String(14), nullable=True)
    razao_social: Mapped[str] = mapped_column(String(255), nullable=True)

    integration_code: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

class FlowControl(Base):
    __tablename__ = "flow_control"
    __table_args__ = {"schema": "dw"}
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    table_name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    control_field: Mapped[str] = mapped_column(Text, nullable=False)
    last_run: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    last_value: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )