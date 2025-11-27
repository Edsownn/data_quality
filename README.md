# data-quality

Projeto para validação de dados de setores de empresas utilizando Pandas, Pandera, PyJanitor e Streamlit.

## Estrutura do Projeto
# data-quality

Backend para validação e importação de planilhas (FastAPI + Pandas + Pandera). O fluxo principal:
- Upload para S3 (presigned or direct)
- Validação + normalização (gera planilha normalizada)
- Geração de relatório de erros (XLSX) e upload para S3
- Importação das abas normalizadas para o DW (Postgres)

## Estrutura resumida

Principais arquivos e diretórios:

- `app/` — código da aplicação (API, serviços, repositório, validação)
- `data/` — arquivos de exemplo e arquivos gerados localmente
- `sql/` — DDL (caso queira aplicar manualmente)
- `run_s3_validate.py` — baixa do S3, valida, gera relatório e normalizada no S3
- `generate_normalized.py` — gera localmente a planilha normalizada a partir de um arquivo local
- `run_import_test.py` — script de teste para executar `importar_dados` (importa para o DW)
- `apply_models.py` — cria tabelas do `app/core/dw_model.py` no banco

## Requisitos

- Python 3.11/3.12
- Dependências listadas em `pyproject.toml` (instale pelo seu gerenciador: `poetry` ou `pip`)

Recomendo criar um venv localizado em `.venv`.

## Configuração (exemplo `settings.toml`)

O projeto usa `dynaconf` (ou similar). No `settings.toml` (ou `.secrets.toml` / variáveis de ambiente) configure:

```toml
# AWS S3
AWS_BUCKET = "riskseg-aaurus"
AWS_REGION = "sa-east-1"
AWS_ACCESS_KEY_ID = "AKIA..."
AWS_SECRET_ACCESS_KEY = "..."
AWS_S3_BASE_PATH = "yavix-dev/data_integration"

# Banco DW (Postgres)
DATABASE_DW_HOST = "db.example.internal"
DATABASE_DW_PORT = 5432
DATABASE_DW_USER = "dw_user"
DATABASE_DW_PASSWORD = "secret"
DATABASE_DW_DBNAME = "dw_database"
```

Observação: Prefira colocar credenciais sensíveis em `.secrets.toml` ou variáveis de ambiente.

## Instalando dependências

Se estiver usando o venv local `.venv`:

```pwsh
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt   # ou: poetry install
```

## Rodando a API (FastAPI)

Use `uvicorn` para executar a API (endpoints para upload/validar/importar/listar erros):

```pwsh
.\.venv\Scripts\python.exe -m uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
```

Endpoints úteis (resumo):

- `POST /arquivos/iniciar` — cria registro e retorna presigned PUT
- `POST /arquivos/{id}/validar` — executa validação do arquivo no S3, cria relatório e normalizada
- `POST /arquivos/{id}/importar` — importa as abas normalizadas para o DW
- `GET /arquivos/{id}/erros/xlsx` — baixa/gera relatório de erros (XLSX)

## Scripts úteis

- Gerar planilha normalizada localmente a partir de `data/Modelo Y.xlsx`:

```pwsh
.\.venv\Scripts\python.exe generate_normalized.py
```

- Validar arquivo no S3, gerar relatório e normalizada no S3 (script de exemplo):

```pwsh
.\.venv\Scripts\python.exe run_s3_validate.py --filename "Modelo Y .xlsx"
```

- Aplicar modelos SQLAlchemy e criar tabelas DW (usa `app/core/dw_model.py`):

```pwsh
.\.venv\Scripts\python.exe apply_models.py
```

- Rodar o teste de import (cria registro, chama `importar_dados` e mostra erros):

```pwsh
.\.venv\Scripts\python.exe run_import_test.py
```

## Fluxo recomendado para testar end-to-end

1. Garanta credenciais AWS e DB configuradas em `settings.toml` ou variáveis de ambiente.
2. Rode `apply_models.py` para criar as tabelas de controle no DW.
3. Envie (ou garanta existência de) `Modelo Y - Oficial_CALI_20250820.xlsx` em `s3://<AWS_BUCKET>/<AWS_S3_BASE_PATH>/Modelo Y - Oficial_CALI_20250820.xlsx`.
4. Rode `run_s3_validate.py` para validar e gerar `normalized` + `erros` no S3.
5. Rode `run_import_test.py` (ou `POST /arquivos/{id}/importar`) para carregar as abas normalizadas no DW.

## Erros e relatório de erros

Os erros de validação são armazenados em `dw.arquivos_erros` (quando o banco estiver disponível) e também são gerados como XLSX em `s3://<bucket>/<base>/reports/...`. Use o endpoint `/arquivos/{id}/erros/xlsx` para obter o relatório via API.

## Observações operacionais

- Para produção, considere:
  - Rodar a API com um servidor ASGI (uvicorn + gunicorn/uvloop) e configurar TLS/reverse-proxy.
  - Usar roles/credentials temporárias (IAM) para S3 e restringir permissões por prefixo.
  - Implementar retries/exponential backoff nas operações S3/DB.

## Testes

```pwsh
pytest
```

## Contato

Abra uma issue ou PR no repositório para discutir alterações maiores.
