import streamlit as st
import pandas as pd
import pandera.pandas as pa
import io


from core.schemas import metricas_setores, metricas_cargos, metricas_empresas, metricas_funcionarios
from core.util import tratar_caracteres, validar_sexo, normalizar_coluna_cep
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
    normalized_dfs = {}
    todas_abas_validas = True  # Variável para controlar se todas as abas são válidas

    for aba, df in df_dict.items():
        st.subheader(f"Aba: {aba}")

        df = df.applymap(tratar_caracteres)
        df = clean_names(df, case_type="snake")

        if df is None or len(df) == 0:
            st.warning("Aba vazia, pulando validação.")
            continue

        # Normaliza sexo e CEP no DataFrame completo
        validar_sexo(df)
        normalizar_coluna_cep(df)

        normalized_dfs[aba] = df.copy()

        sample_size = max(1, int(len(df) * 0.10))
        sample_df = df.sample(n=sample_size, random_state=42)

        st.write(f"Amostra usada para validação (10% = {len(sample_df)} linhas):")
        st.dataframe(sample_df)

        schema = schemas[aba]

        # Valida amostra
        aba_valida = True  # Controla se a aba atual é válida
        try:
            schema.validate(sample_df, lazy=True)
        except pa.errors.SchemaErrors as e:
            st.error("Erros de validação encontrados na amostra:")
            aviso_opcional = []
            erro_critico = False
            for error in e.failure_cases.itertuples():
                linha_excel = (error.index + 2) if error.index is not None else "N/A"
                # Verifica se o erro é em um campo opcional
                if error.column in ["cod_empresa","telefone", "cod_cbo","nome_social",
                                    "trabalho_em_altura", "dt_admissao", "pis_pasep", "rg",
                                    "uf_do_rg", "emissor_rg", "ctps", "serie_ctps", "uf_ctps",
                                    "endereco", "numero", "bairro", "cidade", "uf", "celular"]:
                    aviso_opcional.append(
                        f"- Linha: {linha_excel}, Coluna: {error.column}, Erro: {error.failure_case}, {error.check}"
                    )
                    continue
                st.write(f"- Linha: {linha_excel}, Coluna: {error.column}, Erro: {error.failure_case}, {error.check}")
                erro_critico = True
            if aviso_opcional:
                st.warning("Campos opcionais com problemas:")
                for aviso in aviso_opcional:
                    st.write(aviso)
            if erro_critico:
                aba_valida = False
                todas_abas_validas = False
                continue
            # Se não houver erro crítico, segue para validação total normalmente

        # Valida tudo
        try:
            schema.validate(df, lazy=True)
            st.success("Planilha válida!")
        except pa.errors.SchemaErrors as e:
            st.error("Erros de validação encontrados no arquivo completo:")
            aviso_opcional = []
            erro_critico = False
            for error in e.failure_cases.itertuples():
                linha_excel = (error.index + 2) if error.index is not None else "N/A"
                # Verifica se o erro é em um campo opcional
                if error.column in ["cod_empresa","telefone", "cod_cbo","nome_social",
                                    "trabalho_em_altura", "dt_admissao", "pis_pasep", "rg",
                                    "uf_do_rg", "emissor_rg", "ctps", "serie_ctps", "uf_ctps",
                                    "endereco", "numero", "bairro", "cidade", "uf", "celular"]:
                    aviso_opcional.append(
                        f"- Linha: {linha_excel}, Coluna: {error.column}, Erro: {error.failure_case}, {error.check}"
                    )
                    continue
                st.write(f"- Linha: {linha_excel}, Coluna: {error.column}, Erro: {error.failure_case}, {error.check}")
                erro_critico = True
            if aviso_opcional:
                st.warning("Campos opcionais com problemas:")
                for aviso in aviso_opcional:
                    st.write(aviso)
            if erro_critico:
                aba_valida = False
                todas_abas_validas = False
            else:
                # Se não há erros críticos, apenas opcionais, considera válida
                st.success("Planilha válida! (apenas campos opcionais com problemas)")
        except Exception as e:
            st.error(f"Erro inesperado: {e}")
            aba_valida = False
            todas_abas_validas = False

    # Só mostra o botão de download se todas as abas forem válidas
    if normalized_dfs and todas_abas_validas:
        st.success("Todas as abas foram validadas com sucesso! Você pode baixar a planilha normalizada.")
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            for aba, ndf in normalized_dfs.items():
                sheet_name = aba[:31]
                ndf.to_excel(writer, sheet_name=sheet_name, index=False)
        buffer.seek(0)
        st.download_button(
            label="Baixar planilha normalizada",
            data=buffer,
            file_name="planilha_normalizada.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    elif normalized_dfs and not todas_abas_validas:
        st.warning("Existem erros em uma ou mais abas. Corrija os erros antes de baixar a planilha normalizada.")
    elif not normalized_dfs:
        st.info("Faça upload de uma planilha para começar a validação.")