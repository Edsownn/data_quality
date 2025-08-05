import pandera.pandas as pa
import pandas as pd
from pandera.typing import Series


class MetricasSetores(pa.DataFrameModel):
    CodSetor: Series[int] = pa.Field(alias="Cod Setor", nullable=False,)
    NomeSetor: Series[str] = pa.Field(alias="Nome setor", nullable=False,)
    cnpjEmpresa: Series[str] = pa.Field(alias="CNPJ da empresa", nullable=False,)

    class Config:
        coerce = True
        strict = True

    @pa.check("Cod Setor", name = "Checagem de cod de setor", error = "Cod Setor nao pode ser vazio e deve ter ate 10 caracteres")
    def cod_setor(cls, series: Series[int]) -> Series[bool]:
        return (series > 0) & (series.astype(str).str.len() <= 10)

    @pa.check("Nome setor", name = "Checagem de nome do setor", error = "Nome do setor nao pode ser vazio e maximo 200 caracteres")
    def nome_setor(cls, series: Series[str]) -> Series[bool]:
        return (series.str.len() > 0) & (series.str.len() <= 200)

    @pa.check("CNPJ da empresa", name = "Checagem de CNPJ", error = "CNPJ deve ter 18 caracteres e formato valido XX.XXX.XXX/0001-XX")
    def cnpj_empresa_valido(cls, series: Series[str]) -> Series[bool]:
        return (series.str.len() == 18) & (series.str.match(r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$"))