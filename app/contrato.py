import pandera.pandas as pa

from pandera.typing import Series


class metricas_setores(pa.DataFrameModel):
    CodSetor: Series[int] = pa.Field(alias="cod_setor", nullable=False,)
    NomeSetor: Series[str] = pa.Field(alias="nome_setor", nullable=False,)
    cnpjEmpresa: Series[str] = pa.Field(alias="cnpj_da_empresa", nullable=False,)

    class Config:
        coerce = True
        strict = True

    @pa.check("cod_setor", name = "Checagem de cod de setor", error = "Cod Setor nao pode ser vazio e deve ter ate 10 caracteres")
    def cod_setor(cls, series: Series[int]) -> Series[bool]:
        return (series > 0) & (series.astype(str).str.len() <= 10)

    @pa.check("nome_setor", name = "Checagem de nome do setor", error = "Nome do setor nao pode ser vazio e maximo 200 caracteres")
    def nome_setor(cls, series: Series[str]) -> Series[bool]:
        return series.notnull() & (series.str.strip().str.len() > 0) & (series.str.len() <= 200)

    @pa.check("cnpj_da_empresa", name = "Checagem de CNPJ", error = "CNPJ deve ter 18 caracteres e formato valido XX.XXX.XXX/XXXX-XX")
    def cnpj_empresa_valido(cls, series: Series[str]) -> Series[bool]:
        return (series.str.len() == 18) & (series.str.match(r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$"))