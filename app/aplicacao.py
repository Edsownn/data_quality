import streamlit as st
import pandas as pd
import pandera.pandas as pa
import io
import janitor as jn

from core.schemas import metricas_setores
from core.util import tratar_caracteres
from janitor import clean_names


st.title("Validador de Planilhas")

uploaded_file = st.file_uploader("Faça upload da sua planilha Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Setores")
    df = df.applymap(tratar_caracteres)
    df = clean_names(df, case_type="snake")

    st.write("Prévia dos dados:", df.head(20))

    # Validação amostral
    sample_df = df.sample(n=min(5, len(df)), random_state=42)
    try:
        metricas_setores.validate(sample_df, lazy=True)
    except pa.errors.SchemaErrors as e:
        st.error("Erros de validação encontrados na amostra:")
        for error in e.failure_cases.itertuples():
            st.write(f"- Linha: {error.index}, Coluna: {error.column}, Erro: {error.failure_case}, {error.check}")
        st.stop()  # Para a execução do Streamlit aqui

    # Se passou na amostra, valida tudo
    try:
        metricas_setores.validate(df, lazy=True)
        st.success("Planilha válida!")
    except pa.errors.SchemaErrors as e:
        st.error("Erros de validação encontrados no arquivo completo:")
        for error in e.failure_cases.itertuples():
            st.write(f"- Linha: {error.index}, Coluna: {error.column}, Erro: {error.failure_case}, {error.check}")
    except Exception as e:
        st.error(f"Erro inesperado: {e}")