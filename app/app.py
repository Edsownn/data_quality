import pandas as pd
import pandera.pandas as pa
from contrato import metricas_setores

def extrai_dados(dir_arquivos: pd.DataFrame) -> pd.DataFrame:
    df = pd.read_excel(dir_arquivos, sheet_name="Setores")
    
    try:
        df = metricas_setores.validate(df, lazy=True)
        return df
    except pa.errors.SchemaErrors as e:
        print("Erros de validação encontrados:")
        for error in e.failure_cases.itertuples():
            print(f"- Coluna: {error.column}, Erro: {error.failure_case}, {error.check}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    return df


if __name__ == "__main__":
    dir_arquivos = "data\\Template_ModeloF.xlsx"
    df = extrai_dados(dir_arquivos)