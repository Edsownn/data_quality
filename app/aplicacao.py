import streamlit as st
import pandas as pd
import numpy as np
import pandera.pandas as pa
import io


from core.schemas import metricas_setores, metricas_cargos, metricas_empresas, metricas_funcionarios
from core.util import tratar_caracteres, validar_sexo, normalizar_coluna_cep, verificar_integridade
from core.codigos_erro import mapear_codigo_erro, mapear_codigo_erro_pandera, obter_descricao_codigo, eh_campo_opcional
from janitor import clean_names

def adicionar_erro_relatorio(lista, mensagem, planilha, linha, coluna, tipo):
    nullable = eh_campo_opcional(coluna)
    codigo_erro = mapear_codigo_erro(mensagem, coluna, nullable)
    descricao_codigo = obter_descricao_codigo(codigo_erro)
    
    erro = {
        "codigoERRO": codigo_erro,
        "Descrição do Código": descricao_codigo,
        "Mensagem Detalhada": mensagem,
        "planilha": planilha,
        "linha": linha,
        "coluna": coluna,
        "tipo": tipo,
        "severidade": "CRÍTICO" if not nullable else "AVISO"
    }
    lista.append(erro)

def adicionar_erro_schema(lista, mensagem, planilha, linha, coluna, tipo):
    """Função específica para erros de validação de schema (pandera)"""
    codigo_erro = mapear_codigo_erro_pandera(mensagem, coluna)
    descricao_codigo = obter_descricao_codigo(codigo_erro)
    nullable = eh_campo_opcional(coluna)
    
    erro = {
        "codigoERRO": codigo_erro,
        "Descrição do Código": descricao_codigo,
        "Mensagem Detalhada": mensagem,
        "planilha": planilha,
        "linha": linha,
        "coluna": coluna,
        "tipo": tipo,
        "severidade": "CRÍTICO" if not nullable else "AVISO"
    }
    lista.append(erro)


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
    
    # Normaliza nomes das colunas em todas as abas PRIMEIRO
    for aba_nome, aba_df in df_dict.items():
        aba_df = aba_df.applymap(tratar_caracteres)
        df_dict[aba_nome] = clean_names(aba_df, case_type="snake")
    
    normalized_dfs = {}
    todas_abas_validas = True  # Variável para controlar se todas as abas são válidas
    lista = []  # Lista para coletar todos os erros

    for aba, df in df_dict.items():
        df = df.replace({np.nan: None})
        df_dict[aba] = df
        
        st.subheader(f"Aba: {aba}")

        if aba == "Modelo F" and "Setores" in df_dict and 'cod_setor' in df.columns:
            erros_integridade = verificar_integridade(df, df_dict["Setores"], "cod_setor", "cod_setor")
            
            # Filtra apenas erros que realmente afetam registros
            erros_reais = [erro for erro in erros_integridade if erro.get("quantidade_registros", 0) > 0]
            
            if erros_reais:
                total_registros_com_erro = sum(erro.get("quantidade_registros", 0) for erro in erros_reais)
                st.error(f" ERRO: {total_registros_com_erro} funcionários com códigos de setor inválidos!")
                
                # Adiciona cada erro ao relatório - um para cada linha afetada
                for erro in erros_reais:
                    linhas_afetadas = erro.get("linhas_afetadas", [])
                    if linhas_afetadas:
                        # Adiciona um erro para cada linha específica
                        for linha in linhas_afetadas:
                            adicionar_erro_relatorio(
                                lista,
                                erro.get("erro", "Erro de integridade referencial"),
                                aba,
                                linha,  # Linha específica em vez de "Múltiplas"
                                "cod_setor", 
                                "INTEGRIDADE_REFERENCIAL"
                            )
                    else:
                        # Fallback se não houver linhas específicas
                        adicionar_erro_relatorio(
                            lista,
                            erro.get("erro", "Erro de integridade referencial"),
                            aba,
                            "N/A",
                            "cod_setor", 
                            "INTEGRIDADE_REFERENCIAL"
                        )
                
                # Mostra detalhes dos erros
                with st.expander("Ver detalhes dos erros de setor"):
                    for erro in erros_reais:
                        codigo = erro.get("codigo_invalido", "N/A")
                        qtd = erro.get("quantidade_registros", 0)
                        st.write(f"- Código `{codigo}`: {qtd} registros")
                
                todas_abas_validas = False
            else:
                # Verifica se houve erro de coluna não encontrada
                erros_sistema = [erro for erro in erros_integridade if "não encontrada" in erro.get("erro", "")]
                if erros_sistema:
                    st.warning(f"{erros_sistema[0]['erro']}")
                else:
                    st.success("Integridade referencial OK")
        
        # Verifica integridade para Cargos também
        elif aba == "Cargos" and "Setores" in df_dict and "cod_setor" in df.columns:
            erros_integridade = verificar_integridade(df, df_dict["Setores"], "cod_setor", "cod_setor")
            
            # Filtra apenas erros que realmente afetam registros
            erros_reais = [erro for erro in erros_integridade if erro.get("quantidade_registros", 0) > 0]
            
            if erros_reais:
                total_registros_com_erro = sum(erro.get("quantidade_registros", 0) for erro in erros_reais)
                st.error(f"ERRO: {total_registros_com_erro} cargos com códigos de setor inválidos!")
                
                for erro in erros_reais:
                    linhas_afetadas = erro.get("linhas_afetadas", [])
                    if linhas_afetadas:
                        # Adiciona um erro para cada linha específica
                        for linha in linhas_afetadas:
                            adicionar_erro_relatorio(
                                lista,
                                erro.get("erro", "Erro de integridade referencial"),
                                aba,
                                linha,  # Linha específica
                                "cod_setor", 
                                "INTEGRIDADE_REFERENCIAL"
                            )
                    else:
                        # Fallback se não houver linhas específicas
                        adicionar_erro_relatorio(
                            lista,
                            erro.get("erro", "Erro de integridade referencial"),
                            aba,
                            "N/A",
                            "cod_setor", 
                            "INTEGRIDADE_REFERENCIAL"
                        )
                
                with st.expander("Ver detalhes dos erros de setor em cargos"):
                    for erro in erros_reais:
                        codigo = erro.get("codigo_invalido", "N/A")
                        qtd = erro.get("quantidade_registros", 0)
                        st.write(f"- Código `{codigo}`: {qtd} registros")
                
                todas_abas_validas = False
            else:
                # Verifica se houve erro de sistema
                erros_sistema = [erro for erro in erros_integridade if "não encontrada" in erro.get("erro", "")]
                if erros_sistema:
                    st.warning(f"⚠️ {erros_sistema[0]['erro']}")
                else:
                    st.success("Integridade referencial Cargos → Setores OK")
        
        if aba == "Modelo F" and "Cargos" in df_dict and 'cod_cargo' in df.columns:
            erros_integridade = verificar_integridade(df, df_dict["Cargos"], "cod_cargo", "cod_cargo")
            
            erros_reais = [erro for erro in erros_integridade if erro.get("quantidade_registros", 0) > 0]
            
            if erros_reais:
                total_registros_com_erro = sum(erro.get("quantidade_registros", 0) for erro in erros_reais)
                st.error(f"ERRO: {total_registros_com_erro} funcionários com códigos de cargo inválidos!")
                
                for erro in erros_reais:
                    linhas_afetadas = erro.get("linhas_afetadas", [])
                    if linhas_afetadas:
                        for linha in linhas_afetadas:
                            adicionar_erro_relatorio(
                                lista,
                                erro.get("erro", "Erro de integridade referencial"),
                                aba,
                                linha, 
                                "cod_cargo", 
                                "INTEGRIDADE_REFERENCIAL"
                            )
                    else:
                        adicionar_erro_relatorio(
                            lista,
                            erro.get("erro", "Erro de integridade referencial"),
                            aba,
                            "N/A",
                            "cod_cargo", 
                            "INTEGRIDADE_REFERENCIAL"
                        )
                
                # Mostra detalhes dos erros
                with st.expander("Ver detalhes dos erros de cargo"):
                    for erro in erros_reais:
                        codigo = erro.get("codigo_invalido", "N/A")
                        qtd = erro.get("quantidade_registros", 0)
                        st.write(f"- Código `{codigo}`: {qtd} registros")
                
                todas_abas_validas = False
            else:
                # Verifica se houve erro de coluna não encontrada
                erros_sistema = [erro for erro in erros_integridade if "não encontrada" in erro.get("erro", "")]
                if erros_sistema:
                    st.warning(f"{erros_sistema[0]['erro']}")
                else:
                    st.success("Integridade referencial Modelo F → Cargos OK")

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


        aba_valida = True  # Controla se a aba atual é válida
        try:
            schema.validate(sample_df, lazy=True)
        except pa.errors.SchemaErrors as e:
            st.error("Erros de validação encontrados na amostra:")
            aviso_opcional = []
            erro_critico = False
            erros_criticos = []
            for error in e.failure_cases.itertuples():
                linha_excel = (error.index + 2) if error.index is not None else "N/A"
                mensagem_erro = f"{error.failure_case}, {error.check}"
                
                if error.column in ["cod_empresa","telefone", "cod_cbo","nome_social",
                                    "trabalho_em_altura", "dt_admissao", "pis_pasep", "rg",
                                    "uf_do_rg", "emissor_rg", "ctps", "serie_ctps", "uf_ctps",
                                    "endereco", "numero", "bairro", "cidade", "uf", "celular","cep"]:
                    # Erro opcional - adiciona ao relatório
                    adicionar_erro_schema(
                        lista, mensagem_erro, 
                        aba, linha_excel, error.column, "OPCIONAL"
                    )
                    aviso_opcional.append(
                        f"- Linha: {linha_excel}, Coluna: {error.column}, Erro: {error.failure_case}, {error.check}"
                    )
                    continue
                # Erro crítico - adiciona ao relatório
                adicionar_erro_schema(
                    lista, mensagem_erro,
                    aba, linha_excel, error.column, "OBRIGATORIO"
                )
                erros_criticos.append(f"- Linha: {linha_excel}, Coluna: {error.column}, Erro: {error.failure_case}, {error.check}")
                erro_critico = True
            
            if erros_criticos:
                with st.expander("Ver detalhes dos erros críticos na amostra"):
                    for erro in erros_criticos:
                        st.write(erro)
            
            if aviso_opcional:
                with st.expander("Ver detalhes dos campos opcionais com problemas na amostra"):
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
            erros_criticos = []
            for error in e.failure_cases.itertuples():
                linha_excel = (error.index + 2) if error.index is not None else "N/A"
                mensagem_erro = f"{error.failure_case}, {error.check}"
                
                if error.column in ["cod_empresa","telefone", "cod_cbo","nome_social",
                                    "trabalho_em_altura", "dt_admissao", "pis_pasep", "rg",
                                    "uf_do_rg", "emissor_rg", "ctps", "serie_ctps", "uf_ctps",
                                    "endereco", "numero", "bairro", "cidade", "uf", "celular","cep"]:
                    adicionar_erro_schema(
                        lista, mensagem_erro, 
                        aba, linha_excel, error.column, "OPCIONAL"
                    )
                    aviso_opcional.append(
                        f"- Linha: {linha_excel}, Coluna: {error.column}, Erro: {error.failure_case}, {error.check}"
                    )
                    continue
                # Erro crítico - adiciona ao relatório
                adicionar_erro_schema(
                    lista, mensagem_erro,
                    aba, linha_excel, error.column, "OBRIGATORIO"
                )
                erros_criticos.append(f"- Linha: {linha_excel}, Coluna: {error.column}, Erro: {error.failure_case}, {error.check}")
                erro_critico = True
            
            if erros_criticos:
                with st.expander("Ver detalhes dos erros críticos no arquivo completo"):
                    for erro in erros_criticos:
                        st.write(erro)
            
            if aviso_opcional:
                with st.expander("Ver detalhes dos campos opcionais com problemas"):
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

    # Botão para baixar relatório de erros
    if lista:
        df_relatorio = pd.DataFrame(lista)
        
        buffer_relatorio = io.BytesIO()
        df_relatorio.to_excel(buffer_relatorio, index=False, sheet_name="Relatório_Erros")
        buffer_relatorio.seek(0)
        
        st.download_button(
            label="Baixar Relatório de Erros",
            data=buffer_relatorio,
            file_name=f"relatorio_erros_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


    if normalized_dfs:
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
    elif not normalized_dfs:
        st.info("Faça upload de uma planilha para começar a validação.")