import pandas as pd
import janitor as jn
import pandera.pandas as pa
from janitor import clean_names
from core.schemas import metricas_setores
from core.util import tratar_caracteres

def extrai_dados(dir_arquivos: pd.DataFrame) -> pd.DataFrame:
    df = pd.read_excel(dir_arquivos, sheet_name="Setores")
    df = df.applymap(tratar_caracteres)
    df = clean_names(df, case_type="snake")


    # Validação amostral
    sample_df = df.sample(n=min(5, len(df)), random_state=42)
    try:
        metricas_setores.validate(sample_df, lazy=True)
    except pa.errors.SchemaErrors as e:
        print("Erros de validação encontrados na amostra:")
        for error in e.failure_cases.itertuples():
            print(f"- Linha: {error.index}, Coluna: {error.column}, Erro: {error.failure_case}, {error.check}")
        return 0
    
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