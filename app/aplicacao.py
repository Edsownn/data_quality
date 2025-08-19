import streamlit as st
import pandas as pd
import pandera.pandas as pa
import io
import janitor as jn

from core.schemas import metricas_setores, metricas_cargos, metricas_empresas, metricas_funcionarios
from core.util import tratar_caracteres, validar_sexo
from janitor import clean_names


schemas = {
    "Setores": metricas_setores,
    "Empresas": metricas_empresas,
    "Cargos": metricas_cargos,
    "Modelo F": metricas_funcionarios
}

st.title("Validador de Planilhas")

uploaded_file = st.file_uploader("Faça upload da sua planilha Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    abas = list(schemas.keys())  
    df_dict = pd.read_excel(uploaded_file, sheet_name=abas)

    for aba, df in df_dict.items():
        st.subheader(f"Aba: {aba}")

        df = df.applymap(tratar_caracteres)
        df = clean_names(df, case_type="snake")

        #st.write("Tipos das colunas:", df.dtypes)

        st.write("Prévia dos dados:", df.head(10))

        schema = schemas[aba]

        # Validação amostral
        sample_df = df.sample(n=min(500, len(df)), random_state=42)
        try:
            validar_sexo(sample_df)
            schema.validate(sample_df, lazy=True)
        except pa.errors.SchemaErrors as e:
            st.error("Warning, validação encontrados na amostra:")
            for error in e.failure_cases.itertuples():
                st.write(f"- Linha: {error.index}, Coluna: {error.column}, Erro: {error.failure_case}, {error.check}")
            continue

        # Se passou na amostra, valida tudo
        try:
            schema.validate(df, lazy=True)
            st.success("Planilha válida!")
        except pa.errors.SchemaErrors as e:
            st.error("Erros de validação encontrados no arquivo completo:")
            for error in e.failure_cases.itertuples():
                st.write(f"- Linha: {error.index}, Coluna: {error.column}, Erro: {error.failure_case}, {error.check}")
        except Exception as e:
            st.error(f"Erro inesperado: {e}")