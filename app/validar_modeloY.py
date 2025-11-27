import pandas as pd
import numpy as np
import pandera.pandas as pa
import sys
import os

from janitor import clean_names
from core.schemas import metricas_setores, metricas_cargos, metricas_empresas, metricas_funcionarios
from core.util import tratar_caracteres, validar_sexo, normalizar_coluna_cep, verificar_integridade, settings
from core.codigos_erro import mapear_codigo_erro, mapear_codigo_erro_pandera, obter_descricao_codigo, eh_campo_opcional


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


def print_sucesso(msg):
    print(f"✓ {msg}")


def print_erro(msg):
    print(f"✗ {msg}")


def print_aviso(msg):
    print(f"⚠ {msg}")


def print_info(msg):
    print(f"ℹ {msg}")


def print_titulo(msg):
    print(f"\n{'='*50}")
    print(f"{msg}")
    print(f"{'='*50}")


schemas = {
    "Setores": metricas_setores,
    "Empresas": metricas_empresas,
    "Cargos": metricas_cargos,
    "Modelo F": metricas_funcionarios
}


CAMPOS_OPCIONAIS = [
    "cod_empresa", "telefone", "cod_cbo", "nome_social",
    "trabalho_em_altura", "dt_admissao", "pis_pasep", "rg",
    "uf_do_rg", "emissor_rg", "ctps", "serie_ctps", "uf_ctps",
    "endereco", "numero", "bairro", "cidade", "uf", "celular", "cep"
]


def validar_planilha(dir_arquivos: str):
    """Valida a planilha e retorna os DataFrames normalizados e lista de erros"""
    
    print_titulo("VALIDADOR DE PLANILHAS")
    print(f"\nArquivo: {dir_arquivos}\n")
    
    if not os.path.exists(dir_arquivos):
        print_erro(f"Arquivo não encontrado: {dir_arquivos}")
        return None, []
    
    abas = list(schemas.keys())
    
    try:
        df_dict = pd.read_excel(dir_arquivos, sheet_name=abas)
    except Exception as e:
        print_erro(f"Erro ao ler arquivo: {e}")
        return None, []
    
    # Normaliza nomes das colunas em todas as abas PRIMEIRO
    for aba_nome, aba_df in df_dict.items():
        aba_df = aba_df.applymap(tratar_caracteres)
        df_dict[aba_nome] = clean_names(aba_df, case_type="snake")
    
    normalized_dfs = {}
    todas_abas_validas = True
    lista = []  # Lista para coletar todos os erros

    for aba, df in df_dict.items():
        df = df.replace({np.nan: None})
        df_dict[aba] = df
        
        print_titulo(f"Aba: {aba}")

        # Verificação de integridade para Modelo F -> Setores
        if aba == "Modelo F" and "Setores" in df_dict and 'cod_setor' in df.columns:
            erros_integridade = verificar_integridade(df, df_dict["Setores"], "cod_setor", "cod_setor")
            erros_reais = [erro for erro in erros_integridade if erro.get("quantidade_registros", 0) > 0]
            
            if erros_reais:
                total_registros_com_erro = sum(erro.get("quantidade_registros", 0) for erro in erros_reais)
                print_erro(f"ERRO: {total_registros_com_erro} funcionários com códigos de setor inválidos!")
                
                for erro in erros_reais:
                    linhas_afetadas = erro.get("linhas_afetadas", [])
                    if linhas_afetadas:
                        for linha in linhas_afetadas:
                            adicionar_erro_relatorio(
                                lista, erro.get("erro", "Erro de integridade referencial"),
                                aba, linha, "cod_setor", "INTEGRIDADE_REFERENCIAL"
                            )
                    else:
                        adicionar_erro_relatorio(
                            lista, erro.get("erro", "Erro de integridade referencial"),
                            aba, "N/A", "cod_setor", "INTEGRIDADE_REFERENCIAL"
                        )
                
                print("  Detalhes dos erros de setor:")
                for erro in erros_reais:
                    codigo = erro.get("codigo_invalido", "N/A")
                    qtd = erro.get("quantidade_registros", 0)
                    print(f"    - Código `{codigo}`: {qtd} registros")
                
                todas_abas_validas = False
            else:
                erros_sistema = [erro for erro in erros_integridade if "não encontrada" in erro.get("erro", "")]
                if erros_sistema:
                    print_aviso(erros_sistema[0]['erro'])
                else:
                    print_sucesso("Integridade referencial OK")
        
        # Verificação de integridade para Cargos -> Setores
        elif aba == "Cargos" and "Setores" in df_dict and "cod_setor" in df.columns:
            erros_integridade = verificar_integridade(df, df_dict["Setores"], "cod_setor", "cod_setor")
            erros_reais = [erro for erro in erros_integridade if erro.get("quantidade_registros", 0) > 0]
            
            if erros_reais:
                total_registros_com_erro = sum(erro.get("quantidade_registros", 0) for erro in erros_reais)
                print_erro(f"ERRO: {total_registros_com_erro} cargos com códigos de setor inválidos!")
                
                for erro in erros_reais:
                    linhas_afetadas = erro.get("linhas_afetadas", [])
                    if linhas_afetadas:
                        for linha in linhas_afetadas:
                            adicionar_erro_relatorio(
                                lista, erro.get("erro", "Erro de integridade referencial"),
                                aba, linha, "cod_setor", "INTEGRIDADE_REFERENCIAL"
                            )
                    else:
                        adicionar_erro_relatorio(
                            lista, erro.get("erro", "Erro de integridade referencial"),
                            aba, "N/A", "cod_setor", "INTEGRIDADE_REFERENCIAL"
                        )
                
                print("  Detalhes dos erros de setor em cargos:")
                for erro in erros_reais:
                    codigo = erro.get("codigo_invalido", "N/A")
                    qtd = erro.get("quantidade_registros", 0)
                    print(f"    - Código `{codigo}`: {qtd} registros")
                
                todas_abas_validas = False
            else:
                erros_sistema = [erro for erro in erros_integridade if "não encontrada" in erro.get("erro", "")]
                if erros_sistema:
                    print_aviso(erros_sistema[0]['erro'])
                else:
                    print_sucesso("Integridade referencial Cargos → Setores OK")
        
        # Verificação de integridade para Modelo F -> Cargos
        if aba == "Modelo F" and "Cargos" in df_dict and 'cod_cargo' in df.columns:
            erros_integridade = verificar_integridade(df, df_dict["Cargos"], "cod_cargo", "cod_cargo")
            erros_reais = [erro for erro in erros_integridade if erro.get("quantidade_registros", 0) > 0]
            
            if erros_reais:
                total_registros_com_erro = sum(erro.get("quantidade_registros", 0) for erro in erros_reais)
                print_erro(f"ERRO: {total_registros_com_erro} funcionários com códigos de cargo inválidos!")
                
                for erro in erros_reais:
                    linhas_afetadas = erro.get("linhas_afetadas", [])
                    if linhas_afetadas:
                        for linha in linhas_afetadas:
                            adicionar_erro_relatorio(
                                lista, erro.get("erro", "Erro de integridade referencial"),
                                aba, linha, "cod_cargo", "INTEGRIDADE_REFERENCIAL"
                            )
                    else:
                        adicionar_erro_relatorio(
                            lista, erro.get("erro", "Erro de integridade referencial"),
                            aba, "N/A", "cod_cargo", "INTEGRIDADE_REFERENCIAL"
                        )
                
                print("  Detalhes dos erros de cargo:")
                for erro in erros_reais:
                    codigo = erro.get("codigo_invalido", "N/A")
                    qtd = erro.get("quantidade_registros", 0)
                    print(f"    - Código `{codigo}`: {qtd} registros")
                
                todas_abas_validas = False
            else:
                erros_sistema = [erro for erro in erros_integridade if "não encontrada" in erro.get("erro", "")]
                if erros_sistema:
                    print_aviso(erros_sistema[0]['erro'])
                else:
                    print_sucesso("Integridade referencial Modelo F → Cargos OK")

        if df is None or len(df) == 0:
            print_aviso("Aba vazia, pulando validação.")
            continue

        # Normaliza sexo e CEP no DataFrame completo
        validar_sexo(df)
        normalizar_coluna_cep(df)

        normalized_dfs[aba] = df.copy()

        sample_size = max(1, int(len(df) * 0.10))
        sample_df = df.sample(n=sample_size, random_state=42)

        print_info(f"Amostra usada para validação (10% = {len(sample_df)} linhas)")

        schema = schemas[aba]

        aba_valida = True
        
        # Validação da amostra
        try:
            schema.validate(sample_df, lazy=True)
        except pa.errors.SchemaErrors as e:
            print_erro("Erros de validação encontrados na amostra:")
            aviso_opcional = []
            erro_critico = False
            erros_criticos = []
            
            for error in e.failure_cases.itertuples():
                linha_excel = (error.index + 2) if error.index is not None else "N/A"
                mensagem_erro = f"{error.failure_case}, {error.check}"
                
                if error.column in CAMPOS_OPCIONAIS:
                    adicionar_erro_schema(lista, mensagem_erro, aba, linha_excel, error.column, "OPCIONAL")
                    aviso_opcional.append(
                        f"  - Linha: {linha_excel}, Coluna: {error.column}, Erro: {error.failure_case}, {error.check}"
                    )
                    continue
                
                adicionar_erro_schema(lista, mensagem_erro, aba, linha_excel, error.column, "OBRIGATORIO")
                erros_criticos.append(
                    f"  - Linha: {linha_excel}, Coluna: {error.column}, Erro: {error.failure_case}, {error.check}"
                )
                erro_critico = True
            
            if erros_criticos:
                print("\n  Erros críticos na amostra:")
                for erro in erros_criticos:
                    print(erro)
            
            if aviso_opcional:
                print("\n  Campos opcionais com problemas na amostra:")
                for aviso in aviso_opcional:
                    print(aviso)
            
            if erro_critico:
                aba_valida = False
                todas_abas_validas = False
                continue

        # Validação completa
        try:
            schema.validate(df, lazy=True)
            print_sucesso("Planilha válida!")
        except pa.errors.SchemaErrors as e:
            print_erro("Erros de validação encontrados no arquivo completo:")
            aviso_opcional = []
            erro_critico = False
            erros_criticos = []
            
            for error in e.failure_cases.itertuples():
                linha_excel = (error.index + 2) if error.index is not None else "N/A"
                mensagem_erro = f"{error.failure_case}, {error.check}"
                
                if error.column in CAMPOS_OPCIONAIS:
                    adicionar_erro_schema(lista, mensagem_erro, aba, linha_excel, error.column, "OPCIONAL")
                    aviso_opcional.append(
                        f"  - Linha: {linha_excel}, Coluna: {error.column}, Erro: {error.failure_case}, {error.check}"
                    )
                    continue
                
                adicionar_erro_schema(lista, mensagem_erro, aba, linha_excel, error.column, "OBRIGATORIO")
                erros_criticos.append(
                    f"  - Linha: {linha_excel}, Coluna: {error.column}, Erro: {error.failure_case}, {error.check}"
                )
                erro_critico = True
            
            if erros_criticos:
                print("\n  Erros críticos no arquivo completo:")
                for erro in erros_criticos:
                    print(erro)
            
            if aviso_opcional:
                print("\n  Campos opcionais com problemas:")
                for aviso in aviso_opcional:
                    print(aviso)
            
            if erro_critico:
                aba_valida = False
                todas_abas_validas = False
            else:
                print_sucesso("Planilha válida! (apenas campos opcionais com problemas)")
        except Exception as e:
            print_erro(f"Erro inesperado: {e}")
            aba_valida = False
            todas_abas_validas = False

    return normalized_dfs, lista, todas_abas_validas


def salvar_relatorio_erros(lista, dir_saida="data"):
    """Salva o relatório de erros em Excel"""
    if not lista:
        print_info("Nenhum erro encontrado para gerar relatório.")
        return None
    
    df_relatorio = pd.DataFrame(lista)
    nome_arquivo = f"{dir_saida}/relatorio_erros_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.xlsx"
    df_relatorio.to_excel(nome_arquivo, index=False, sheet_name="Relatório_Erros")
    print_sucesso(f"Relatório de erros salvo em: {nome_arquivo}")
    return nome_arquivo


def salvar_planilha_normalizada(normalized_dfs, dir_saida="data"):
    """Salva a planilha normalizada em Excel"""
    if not normalized_dfs:
        print_info("Nenhuma planilha normalizada para salvar.")
        return None
    
    nome_arquivo = f"{dir_saida}/planilha_normalizada_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.xlsx"
    with pd.ExcelWriter(nome_arquivo, engine="openpyxl") as writer:
        for aba, ndf in normalized_dfs.items():
            sheet_name = aba[:31]
            ndf.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print_sucesso(f"Planilha normalizada salva em: {nome_arquivo}")
    return nome_arquivo


if __name__ == "__main__":

    if len(sys.argv) > 1:
        dir_arquivos = sys.argv[1]
    else:
        dir_arquivos = "data\\Modelo Y - Oficial_CALI_20250820.xlsx"
    
    normalized_dfs, lista_erros, todas_validas = validar_planilha(dir_arquivos)
    
    print_titulo("RESUMO FINAL")
    
    if todas_validas:
        print_sucesso("Todas as abas foram validadas com sucesso!")
    else:
        print_erro("Foram encontrados erros de validação.")
    
    # Salva os arquivos de saída
    if lista_erros:
        salvar_relatorio_erros(lista_erros)
    
    if normalized_dfs:
        salvar_planilha_normalizada(normalized_dfs)