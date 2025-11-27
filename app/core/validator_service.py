import io
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np
import pandera.pandas as pa
from janitor import clean_names

from .schemas import metricas_setores, metricas_cargos, metricas_empresas, metricas_funcionarios
from .util import tratar_caracteres, validar_sexo, normalizar_coluna_cep, verificar_integridade, logger
from .codigos_erro import mapear_codigo_erro, mapear_codigo_erro_pandera, obter_descricao_codigo, eh_campo_opcional

SCHEMAS = {
    "Setores": metricas_setores,
    "Empresas": metricas_empresas,
    "Cargos": metricas_cargos,
    "Modelo F": metricas_funcionarios,
}

CAMPOS_OPCIONAIS = {
    "cod_empresa","telefone", "cod_cbo","nome_social",
    "trabalho_em_altura", "dt_admissao", "pis_pasep", "rg",
    "uf_do_rg", "emissor_rg", "ctps", "serie_ctps", "uf_ctps",
    "endereco", "numero", "bairro", "cidade", "uf", "celular","cep","descricao_detalhada_do_cargo","inscricao"
}


def _add_erro(lista: List[dict], codigo: str, desc: str, msg: str, planilha: str, linha, coluna: str, tipo: str):
    nullable = eh_campo_opcional(coluna)
    lista.append({
        "codigoERRO": codigo,
        "Descrição do Código": desc,
        "Mensagem Detalhada": msg,
        "planilha": planilha,
        "linha": linha,
        "coluna": coluna,
        "tipo": tipo,
        "severidade": "CRÍTICO" if not nullable else "AVISO"
    })


def _erro_regra(lista: List[dict], mensagem: str, planilha: str, linha, coluna: str, tipo: str):
    codigo = mapear_codigo_erro(mensagem, coluna, eh_campo_opcional(coluna))
    _add_erro(lista, codigo, obter_descricao_codigo(codigo), mensagem, planilha, linha, coluna, tipo)


def _integridade(aba_fato: str, aba_dim: str, col_fato: str, col_dim: str, df_dict: Dict[str, pd.DataFrame], erros: List[dict]):
    fact = df_dict.get(aba_fato)
    dim = df_dict.get(aba_dim)
    if fact is None or dim is None:
        return
    if col_fato not in fact.columns or col_dim not in dim.columns:
        return
    validos = set(dim[col_dim].dropna().unique())
    for idx, val in fact[col_fato].items():
        if val is not None and val not in validos:
            _erro_regra(erros, f"Valor {val} inexistente em {aba_dim}.{col_dim}", aba_fato, idx + 2, col_fato, "INTEGRIDADE_REFERENCIAL")


def validar_arquivo_excel(file_bytes: bytes) -> Tuple[Dict[str, pd.DataFrame], List[dict], Dict]:
    """Valida um arquivo Excel completo e retorna dfs normalizados, lista de erros e estatísticas."""
    erros: List[dict] = []
    normalized: Dict[str, pd.DataFrame] = {}
    buf = io.BytesIO(file_bytes)
    sheets = list(SCHEMAS.keys())
    df_dict = pd.read_excel(buf, sheet_name=sheets)

    # Normalização base
    for nome, df in df_dict.items():
        df = df.applymap(tratar_caracteres)
        df = clean_names(df, case_type="snake")
        df = df.replace({np.nan: None})
        validar_sexo(df)
        normalizar_coluna_cep(df)
        df_dict[nome] = df

    # Regras de integridade
    if "Setores" in df_dict:
        if "Modelo F" in df_dict and "cod_setor" in df_dict["Modelo F"].columns:
            _integridade("Modelo F", "Setores", "cod_setor", "cod_setor", df_dict, erros)
        if "Cargos" in df_dict and "cod_setor" in df_dict["Cargos"].columns:
            _integridade("Cargos", "Setores", "cod_setor", "cod_setor", df_dict, erros)
    if "Cargos" in df_dict and "Modelo F" in df_dict and "cod_cargo" in df_dict["Modelo F"].columns:
        _integridade("Modelo F", "Cargos", "cod_cargo", "cod_cargo", df_dict, erros)

    # Validação de schema completa
    for aba, df in df_dict.items():
        schema = SCHEMAS[aba]
        try:
            schema.validate(df, lazy=True)
        except pa.errors.SchemaErrors as e:
            for error in e.failure_cases.itertuples():
                linha_excel = (error.index + 2) if error.index is not None else None
                msg = f"{error.failure_case}, {error.check}"
                codigo = mapear_codigo_erro_pandera(msg, error.column)
                tipo = "OPCIONAL" if error.column in CAMPOS_OPCIONAIS else "OBRIGATORIO"
                _add_erro(erros, codigo, obter_descricao_codigo(codigo), msg, aba, linha_excel, error.column, tipo)
        normalized[aba] = df.copy()

    # Estatísticas
    if erros:
        severidade = pd.Series([e["severidade"] for e in erros]).value_counts().to_dict()
        tipos = pd.Series([e["tipo"] for e in erros]).value_counts().to_dict()
    else:
        severidade, tipos = {}, {}

    stats = {
        "total_erros": len(erros),
        "por_severidade": severidade,
        "por_tipo": tipos,
    }
    logger.info(f"Validação concluída: {stats}")
    return normalized, erros, stats
