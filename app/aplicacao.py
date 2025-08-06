import streamlit as st
import pandas as pd
import pandera.pandas as pa
import io

from contrato import MetricasSetores


st.title("Validador de Planilhas")

uploaded_file = st.file_uploader("Faça upload da sua planilha Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Setores")
    st.write("Prévia dos dados:", df.head(20))
    try:
        MetricasSetores.validate(df, lazy=True)
        st.success("Planilha válida!")
    except pa.errors.SchemaErrors as e:
        st.write("Erros de validação encontrados:")
        for error in e.failure_cases.itertuples():
            st.write(f"- Linha: {error.index}, Coluna: {error.column}, Erro: {error.failure_case}, {error.check}")
    except Exception as e:
        st.write(f"Erro inesperado: {e}")
