import pandas as pd
import pandera as pa

metricas_setores = pa.DataFrameSchema({
    "cod_setor": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 15), error="Cod Setor não pode ser vazio e deve ter até 15 caracteres"),
            pa.Check(lambda s: s.str.match(r'^[\d\.]+$'), error="Cod Setor deve conter apenas dígitos e pontos"),
            pa.Check(lambda s: s.str.replace('.', '', regex=False).astype(int) > 0, error="Cod Setor deve ser maior que zero"),
        ],
        nullable=False,
        unique=True
    ),
    "nome_setor": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.apply(lambda x: isinstance(x, str)), error="Nome setor deve ser texto"),
            pa.Check(lambda s: s.str.strip().str.len().between(1, 200), error="Nome setor não pode ser vazio e deve ter até 200 caracteres"),
        ],
        nullable=False
    ),
    "cnpj_da_empresa": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.apply(lambda x: isinstance(x, str)), error="CNPJ deve ser texto"),
            pa.Check(lambda s: s.str.len() == 18, error="CNPJ deve ter 18 caracteres"),
            pa.Check.str_matches(r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$", error="CNPJ deve estar no formato XX.XXX.XXX/XXXX-XX"),
        ],
        nullable=False
    ),
},
    strict=True, 
    coerce=True
)

metricas_cargos = pa.DataFrameSchema({
    "cod_cargo": pa.Column(
        pa.Int,
        checks=[
            #pa.Check(lambda s: s.notnull(), error="Cod Cargo não pode ser nulo"),
            pa.Check(lambda s: s > 0, error="Cod Cargo deve ser maior que zero"),
        ],
        nullable=False,
        unique=True
    ),
    "cod_cbo": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 15), error="Cod CBO não pode ser vazio e deve ter até 15 caracteres"),
        ],
        nullable=True
    ),
    "nome_cargo": pa.Column(
        pa.String,
        checks=[
            #pa.Check(lambda s: s.notnull(), error="Nome Cargo não pode ser nulo"),
            pa.Check(lambda s: s.str.strip().str.len().between(1, 30), error="Nome Cargo não pode ser vazio e deve ter até 30 caracteres"),
        ],
        nullable=False
    ),
    "descricao_detalhada_do_cargo": pa.Column(
        pa.String,
        checks=[
            #pa.Check(lambda s: s.notnull(), error="Descrição detalhada do cargo não pode ser nula"),
            pa.Check(lambda s: s.str.strip().str.len().between(1, 1000), error="Descrição detalhada do cargo deve ter entre 1 e 1000 caracteres"),
        ],
        nullable=True
    )
},
    strict=True,
    coerce=True
)

metricas_empresas = pa.DataFrameSchema({
    "cod_empresa": pa.Column(
        pa.Int,
        checks=[
            pa.Check(lambda s: s.astype(str).str.strip().str.len().between(1, 10), error="Cod Empresa não pode ser vazio e deve ter até 10 caracteres"),
            pa.Check(lambda s: s > 0, error="Cod Empresa deve ser maior que zero"),
        ],
        nullable=True
    ),
    "nome_da_empresa": pa.Column(
        pa.String,
        checks=[
            #pa.Check(lambda s: s.notnull(), error="Nome Empresa não pode ser nulo"),
            pa.Check(lambda s: s.str.strip().str.len().between(1, 60), error="Nome Empresa não pode ser vazio e deve ter até 60 caracteres"),
        ],
        nullable=False
    ),
    "cnae_7": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.notnull(), error="CNAE 7 não pode ser nulo"),
            pa.Check(lambda s: s.str.strip().str.len().between(1, 10), error="CNAE 7 deve ter ate 10 caracteres"),
            pa.Check.str_matches((r'^\d{7}$'), error="CNAE 7 deve estar no formato XXXXXXX"),
        ],
        nullable=False
    ),
    "cnpj": pa.Column(
        pa.String,
        checks=[
            #pa.Check(lambda s: s.notnull(), error="CNPJ Empresa não pode ser nulo"),
            pa.Check(lambda s: s.str.len() == 18, error="CNPJ Empresa deve ter 18 caracteres"),
            pa.Check.str_matches(r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$", error="CNPJ Empresa deve estar no formato XX.XXX.XXX/XXXX-XX"),
        ],
        nullable=False
    ),
    "razao_social": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 200), error="Razão Social não pode ser vazia e deve ter até 60 caracteres"),
        ],
        nullable=False
    ),
    "inscricao": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 200), error="Inscrição Unidade deve ter entre 1 e 200 caracteres"),
        ],
        nullable=False
    ),
    "cnpj_da_matriz": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.len() == 18, error="CNPJ da Matriz deve ter 18 caracteres"),
            pa.Check.str_matches(r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$", error="CNPJ da Matriz deve estar no formato XX.XXX.XXX/XXXX-XX"),
        ],
        nullable=False
    ),
    "endereco": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 110), error="Endereço não pode ser vazio e deve ter até 110 caracteres"),
        ],
        nullable=False
    ),
    "numero": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.eq("S/N") | (s.astype(str).str.strip().str.len().between(1, 10)),error="numero deve ter até 10 caracteres ou 'S/N'"),
            pa.Check(lambda s: s.eq("S/N") | s.astype(str).astype(float) > 0,error="numero deve ser maior que zero ou 'S/N'"),
    ],
    nullable=False
    ),
    "bairro": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 80), error="Bairro não pode ser vazio e deve ter até 80 caracteres"),
        ],
        nullable=False
    ),
    "cidade": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 60), error="Cidade não pode ser vazia e deve ter até 60 caracteres"),
        ],
        nullable=False
    ),
    "uf": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 5), error="UF deve ter entre 1 e 5 caracteres"),
        ],
        nullable=False
    ),
    "cep": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len() == 9, error="CEP deve ter exatamente 9 caracteres"),
            pa.Check.str_matches(r"^\d{5}-\d{3}$", error="CEP deve estar no formato XXXXX-XXX"),
        ],
        nullable=False
    ),
    "telefone": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1,25), error="Telefone deve ter entre 1 e 25 caracteres"),
            pa.Check.str_matches(r"^(?:\(\d{2}\) \d{4,5}-\d{4}|\(\d{2}\) \d{8})$", error="Telefone deve estar no formato (XX) XXXXX-XXXX ou (XX)XXXXXXXX"),
        ],
        nullable=True
    )
},
    strict=True,
    coerce=True
)

metricas_funcionarios = pa.DataFrameSchema({
    "cnpj_empresa": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.len() == 18, error="CNPJ Empresa deve ter 18 caracteres"),
            pa.Check.str_matches(r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$", error="CNPJ Empresa deve estar no formato XX.XXX.XXX/XXXX-XX"),
        ],
        nullable=False
    ),
    "cod_setor":pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 15), error="Cod Setor não pode ser vazio e deve ter até 15 caracteres"),
            pa.Check(lambda s: s.str.match(r'^[\d\.]+$'), error="Cod Setor deve conter apenas dígitos e pontos"),
            pa.Check(lambda s: s.str.replace('.', '', regex=False).astype(int) > 0, error="Cod Setor deve ser maior que zero"),
        ],
        nullable=False
    ),
    "cod_cargo":pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 10), error="Cod Setor não pode ser vazio e deve ter até 10 caracteres"),
            pa.Check(lambda s: s.str.match(r'^[\d\.]+$'), error="Cod Setor deve conter apenas dígitos e pontos"),
            pa.Check(lambda s: s.str.replace('.', '', regex=False).astype(int) > 0, error="Cod Setor deve ser maior que zero"),
        ],
        nullable=False
    ),
    "cod_funcionario":pa.Column(
        pa.Int,
        checks=[
            pa.Check(lambda s: s.astype(str).str.strip().str.len().between(1, 10), error="Cod Funcionario não pode ser vazio e deve ter até 10 caracteres"),
            pa.Check(lambda s: s > 0, error="Cod Funcionario deve ser maior que zero"),
        ],
        nullable=False
    ),
    "cpf":pa.Column(
        pa.String,
        checks=[
            #pa.Check(lambda s: s.notnull(), error="CPF não pode ser nulo"),
            pa.Check(lambda s: s.str.len() == 14, error="CPF deve ter 14 caracteres"),
            pa.Check.str_matches(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", error="CPF deve estar no formato XXX.XXX.XXX-XX"),
            pa.Check.unique(error="CPF deve ser único"),
        ],
        nullable=False
    ),
    "nome_funcionario":pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 150), error="Nome Funcionario não pode ser vazio e deve ter até 150 caracteres"),
        ],
        nullable=False
    ),
    "nome_social":pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 150), error="Nome Social não pode ser vazio e deve ter até 150 caracteres"),
        ],
        nullable=True
    ),
    "dt_nascimento": pa.Column(
        pa.DateTime,
        checks=[
        pa.Check(lambda s: s.gt(pd.Timestamp("1900-01-01")), error="Data de Nascimento deve ser posterior a 01/01/1900"),
        pa.Check(lambda s: s.lt(pd.Timestamp.now()), error="Data de Nascimento deve ser anterior a data atual"),
        ],
        nullable=False
    ),
    "sexo": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 1), error="Sexo deve ter exatamente 1 caractere"),
            #pa.Check.str_matches(r"^(M|F|m|f)$", error="Sexo deve ser M, F"),
            pa.Check(lambda s: s.fillna('').astype(str).str.strip().str.lower().map(lambda v: {'feminino':'f','f':'f','masculino':'m','m':'m'}.get(v, '')).isin(['f','m']), error="Sexo deve ser Feminino/Masculino ou F/M")
        ],
        nullable=False
    ),
    "situacao": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 20), error="Situação deve ter até 20 caracteres"),
            pa.Check.str_matches(r"^(ATIVO|INATIVO|AFASTADO|FERIAS)$", error="Situação deve ser ATIVO, INATIVO, AFASTADO ou FERIAS"),
        ],
        nullable=False
    ),
    "dt_admissao": pa.Column(
        pa.DateTime,
        checks=[
        pa.Check(lambda s: s.gt(pd.Timestamp("1900-01-01")), error="Data de Admissão deve ser posterior a 01/01/1900"),
        pa.Check(lambda s: s.lt(pd.Timestamp.now()), error="Data de Admissão deve ser anterior a data atual"),
        ],
        nullable=False
    ),
    "matricula_rh": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 50), error="Matrícula RH deve ter até 50 caracteres"),
        ],
        nullable=False
    ),
    "matricula_esocial": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 30), error="Matrícula eSocial deve ter até 30 caracteres"),
        ],
        nullable=False
    ),
    "codigo_categoria_esocial": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 8), error="Código da Categoria eSocial deve ter até 8 caracteres"),
        ],
        nullable=False
    ),
    "trabalho_em_altura": pa.Column(
        pa.String,
        checks=[
            pa.Check.str_matches(r"^(SIM|NAO)$", error="Trabalho em Altura deve ser SIM ou NAO"),
        ],
        nullable=True
    ),
    "dt_demissao": pa.Column(
        pa.DateTime,
        checks=[
        pa.Check(lambda s: s.gt(pd.Timestamp("1900-01-01")), error="Data de Demissão deve ser posterior a 01/01/1900"),
        pa.Check(lambda s: s.lt(pd.Timestamp.now()), error="Data de Demissão deve ser anterior a data atual"),
        ],
        nullable=True
    ),
    "pis_pasep": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 25), error="PIS/PASEP deve ter até 14 caracteres"),
        ],
        nullable=True
    ),
    "rg": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.replace(r"\D+", "", regex=True).str.len().between(1, 15), error="RG deve ter até 15 caracteres"),
        ],
        nullable=True
    ),
    "uf_do_rg":pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 2), error="UF do RG deve ter até 2 caracteres"),
        ],
        nullable=True
    ),
    "emissor_rg": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 30), error="Emissor do RG deve ter até 30 caracteres"),
        ],
        nullable=True
    ),
    "ctps": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 60), error="CTPS deve ter até 60 caracteres"),
        ],
        nullable=True
    ),
    "serie_ctps": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 60), error="Série CTPS deve ter até 60 caracteres"),
        ],
        nullable=True
    ),
    "uf_ctps": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 60), error="UF da CTPS deve ter até 2 caracteres"),
        ],
        nullable=True
    ),
    "endereco": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(2, 60), error="Endereço deve ter entre 2 e 60 caracteres"),
        ],
        nullable=True
    ),
    "numero": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 60), error="Número deve ter até 60 caracteres"),
        ],
        nullable=True
    ),
    "bairro": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 60), error="Bairro deve ter até 60 caracteres"),
        ],
        nullable=True
    ),
    "cidade": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 60), error="Cidade deve ter até 60 caracteres"),
        ],
        nullable=True
    ),
    "uf": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 2), error="UF deve ter até 2 caracteres"),
        ],
        nullable=True
    ),
    "cep": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 10), error="CEP deve ter até 10 caracteres"),
            pa.Check.str_matches(r"^\d{2}\.\d{3}-\d{3}|\d{5}-\d{3}$", error="CEP deve estar no formato XXXXX-XXX"),
        ],
        nullable=False
    ),
    "celular": pa.Column(
        pa.String,
        checks=[
            pa.Check(lambda s: s.str.strip().str.len().between(1, 15), error="Celular deve ter até 15 caracteres"),
            pa.Check.str_matches(r"^\(\d{2}\) \d{5}-\d{4}|\(\d{2}\) \d{9}|\(\d{2}\) \d{8}$", error="Celular deve estar no formato (XX) XXXXX-XXXX ou (XX)XXXXXXXX"),
        ],
        nullable=True
    )
},
    strict=True,
    coerce=True
)
