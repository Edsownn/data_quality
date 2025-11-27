"""Serviço de importação pós-validação.

Fluxo resumido:
1. Ler arquivo normalizado do S3 (normalized/ path)
2. Carregar planilhas em DataFrames
3. Persistir em tabelas de staging (1:1 com colunas da planilha)
4. Transformar e inserir/upsert em tabelas finais (dw.*) se necessário
5. Retornar estatísticas da importação

Observação: Ajuste nomes de tabelas conforme seu DW real. Aqui usamos nomes sugestivos.
"""
from __future__ import annotations
from typing import Dict, Any
import io
import pandas as pd
from .storage_service import get_bytes
from .util import settings
from .repository import ArquivoRepository
from .models_validacao import StatusArquivo
from .util import logger
from .db import Operator


def _save_staging(df: pd.DataFrame, tabela: str):
    op = Operator(table=tabela)
    # Estratégia: criar tabela se não existir e inserir tudo
    try:
        op.create_table_from_df(df)
    except Exception as e:
        logger.debug(f"Tabela pode já existir: {e}")
    # Limpa (opcional)
    try:
        op.delete()
    except Exception as e:
        logger.warning(f"Falha ao limpar staging {tabela}: {e}")
    # Insere
    registros = df.to_dict(orient="records")
    op.insert(registros)


def _load_to_dw(df: pd.DataFrame, tabela: str, key_field: str | None = None):
    """Carrega um DataFrame na tabela final do DW.
    Estratégia: criar tabela a partir do DataFrame se não existir e executar upsert.
    key_field: coluna usada para ON CONFLICT; se None, usa o padrão do Operator.
    """
    if df is None or df.empty:
        logger.info(f"Nada a carregar para {tabela}")
        return {"loaded": False, "rows": 0}

    op = Operator(table=tabela)
    if key_field:
        op.key_field = key_field

    try:
        op.create_table_from_df(df)
    except Exception as e:
        logger.debug(f"create_table_from_df pode já existir ou falhou para {tabela}: {e}")

    try:
        op.upsert(df)
        return {"loaded": True, "rows": len(df)}
    except Exception as e:
        logger.error(f"Falha ao carregar dados em {tabela}: {e}")
        return {"loaded": False, "rows": len(df), "error": str(e)}


def importar_dados(arquivo_id: str, nome_original: str) -> Dict[str, Any]:
    repo = ArquivoRepository()
    repo.atualizar_status(arquivo_id, StatusArquivo.IMPORTANDO)

    # Use the normalized file path that matches our S3 structure
    base_path = "yavix-dev/data_integration"
    chave_norm = f"{base_path}/normalized/{nome_original}"
    logger.info(f"Iniciando import: {chave_norm}")
    conteudo = get_bytes(chave_norm)
    dfs = pd.read_excel(io.BytesIO(conteudo), sheet_name=None)

    stats_import = {}

    # Exemplo: salvar cada sheet em staging
    mapping_staging = {
        "Setores": "dw.stg_setores",
        "Empresas": "dw.stg_empresas",
        "Cargos": "dw.stg_cargos",
        "Modelo F": "dw.stg_funcionarios",
    }

    for nome_sheet, df in dfs.items():
        tabela = mapping_staging.get(nome_sheet)
        if not tabela:
            continue
        try:
            _save_staging(df, tabela)
            stats_import[nome_sheet] = {"linhas": len(df)}
        except Exception as e:
            logger.error(f"Erro staging {tabela}: {e}")
            stats_import[nome_sheet] = {"erro": str(e)}

    # Placeholder transformações → inserir em dimensões/fatos reais
    # Nenhuma métrica específica solicitada no momento; métricas podem ser adicionadas
    # conforme necessidade (ex.: linhas lidas, linhas inseridas, etc.).

    # Mapping para tabelas finais no DW (ajuste conforme seu modelo)
    mapping_final = {
        "Setores": "setores",
        "Empresas": "empresas",
        "Cargos": "cargos",
        "Modelo F": "funcionarios",
    }

    load_stats = {}
    for nome_sheet, df in dfs.items():
        tabela_final = mapping_final.get(nome_sheet)
        if not tabela_final:
            continue
        res = _load_to_dw(df, tabela_final)
        load_stats[nome_sheet] = res

    stats_import["load"] = load_stats

    repo.atualizar_status(arquivo_id, StatusArquivo.IMPORTADO, stats_import)
    return {"arquivo_id": arquivo_id, "status": StatusArquivo.IMPORTADO, "stats_import": stats_import}
