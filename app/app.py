import pandas as pd
import janitor as jn
import pandera.pandas as pa
from contrato import MetricasSetores

def extrai_dados(dir_arquivos: pd.DataFrame) -> pd.DataFrame:
    df = pd.read_excel(dir_arquivos, sheet_name="Setores")
    
    try:
        df = MetricasSetores.validate(df, lazy=True)
        return df
    except pa.errors.SchemaErrors as e:
        print("Erros de validação encontrados:")
        print(e)

    return df


if __name__ == "__main__":
    dir_arquivos = "data\\Template_ModeloF.xlsx"
    df = extrai_dados(dir_arquivos)