import pandera as pa

metricas_setores = pa.DataFrameSchema({
    "cod_setor": pa.Column(
        pa.Int,
        checks=[
            #pa.Check(lambda s: s.notnull(), error="Cod Setor não pode ser nulo"),
            pa.Check(lambda s: s.astype(str).str.strip().str.len().between(1, 10), error="Cod Setor não pode ser vazio e deve ter até 10 caracteres"),
            pa.Check(lambda s: s > 0, error="Cod Setor deve ser maior que zero"),
        ],
        nullable=False
    ),
    "nome_setor": pa.Column(
        pa.String,
        checks=[
            #pa.Check(lambda s: s.notnull(), error="Nome setor não pode ser nulo"),
            pa.Check(lambda s: s.apply(lambda x: isinstance(x, str)), error="Nome setor deve ser texto"),
            pa.Check(lambda s: s.str.strip().str.len().between(1, 200), error="Nome setor não pode ser vazio e deve ter até 200 caracteres"),
        ],
        nullable=False
    ),
    "cnpj_da_empresa": pa.Column(
        pa.String,
        checks=[
            #pa.Check(lambda s: s.notnull(), error="CNPJ da empresa não pode ser nulo"),
            pa.Check(lambda s: s.apply(lambda x: isinstance(x, str)), error="CNPJ deve ser texto"),
            pa.Check(lambda s: s.str.len() == 18, error="CNPJ deve ter 18 caracteres"),
            pa.Check.str_matches(r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$", error="CNPJ deve estar no formato XX.XXX.XXX/XXXX-XX"),
        ],
        nullable=False
    ),
})