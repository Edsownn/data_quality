import pandera as pa
from pandera.typing import Series


class MetricasSetores(pa.DataFrameModel):
    CodSetor: Series[int] = pa.Field(alias="Cod Setor")
    NomeSetor: Series[str] = pa.Field(alias="Nome Setor")
    cnpjEmpresa: Series[str] = pa.Field(alias="CNPJ da Empresa")

    class Config:
        coerce = True
        strict = True
