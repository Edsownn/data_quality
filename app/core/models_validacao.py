from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any

class StatusArquivo(str, Enum):
    INICIADO = "INICIADO"
    UPLOADED = "UPLOADED"
    VALIDANDO = "VALIDANDO"
    ERROS = "ERROS"
    VALIDADO = "VALIDADO"
    IMPORTANDO = "IMPORTANDO"
    IMPORTADO = "IMPORTADO"
    FALHA_IMPORT = "FALHA_IMPORT"

@dataclass
class ArquivoRegistro:
    id: str
    nome_original: str
    chave_s3: str
    status: StatusArquivo
    tamanho: Optional[int] = None
    mime: Optional[str] = None
    usuario: Optional[str] = None
    dt_upload: datetime = field(default_factory=datetime.utcnow)
    dt_validacao: Optional[datetime] = None
    dt_importacao: Optional[datetime] = None
    stats: Optional[Dict[str, Any]] = None

@dataclass
class ErroValidacao:
    arquivo_id: str
    codigoERRO: str
    descricao_codigo: str
    mensagem: str
    planilha: str
    linha: Optional[int]
    coluna: str
    tipo: str
    severidade: str

    @staticmethod
    def from_dict(arquivo_id: str, d: Dict[str, Any]) -> "ErroValidacao":
        return ErroValidacao(
            arquivo_id=arquivo_id,
            codigoERRO=d.get("codigoERRO"),
            descricao_codigo=d.get("Descrição do Código"),
            mensagem=d.get("Mensagem Detalhada"),
            planilha=d.get("planilha"),
            linha=d.get("linha"),
            coluna=d.get("coluna"),
            tipo=d.get("tipo"),
            severidade=d.get("severidade"),
        )
