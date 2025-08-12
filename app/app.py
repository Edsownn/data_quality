import pandas as pd
import pandera.pandas as pa


from janitor import clean_names
from core.schemas import metricas_setores, metricas_cargos, metricas_empresas, metricas_funcionarios
from core.util import tratar_caracteres


def extrai_dados(dir_arquivos: str):
    abas = ["Setores", "Empresas", "Cargos", "Modelo F"]
    df_dict = pd.read_excel(dir_arquivos, sheet_name=abas)

    resultados = {}

    for aba, df in df_dict.items():
        print(f"\n--- Validando aba: {aba} ---")
        df = df.applymap(tratar_caracteres)
        df = clean_names(df, case_type="snake")

        # Seleciona schema conforme a aba
        if aba == "Setores":
            schema = metricas_setores
        elif aba == "Empresas":
            schema = metricas_empresas
        elif aba == "Cargos":
            schema = metricas_cargos
        elif aba == "Modelo F":
            schema = metricas_funcionarios

    sample_df = df.sample(n=min(5, len(df)), random_state=42)
    try:
        schema.validate(sample_df, lazy=True)
    except pa.errors.SchemaErrors as e:
        print("Erros de validação encontrados na amostra:")
        for error in e.failure_cases.itertuples():
            print(f"- Linha: {error.index}, Coluna: {error.column}, Erro: {error.failure_case}, {error.check}")
        return 0
    
    try:
        df = schema.validate(df, lazy=True)
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