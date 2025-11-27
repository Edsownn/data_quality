# Data Quality - Sistema de Validação de Planilhas

Sistema de validação e importação de planilhas Excel utilizando **Streamlit** + **Pandas** + **Pandera** + **PyJanitor**.

## 📋 Visão Geral

Aplicação para validação de qualidade de dados em planilhas Excel contendo informações de:
- **Funcionários** (Modelo F)
- **Empresas** 
- **Setores**
- **Cargos**

### Funcionalidades Principais

- ✅ Validação de dados com schemas Pandera
- 🔄 Normalização automática de colunas e dados
- 🔗 Verificação de integridade referencial entre abas
- 📊 Classificação de erros (CRÍTICOS vs AVISOS)
- 📁 Geração de planilha normalizada
- 📋 Geração de relatório de erros em Excel
- 💾 Persistência em banco PostgreSQL

## 📁 Estrutura do Projeto

```
data_quality/
├── app/                          # Código da aplicação
│   ├── aplicacao.py             # Interface Streamlit (principal)
│   ├── core/                    # Módulos core
│   │   ├── schemas.py          # Schemas de validação Pandera
│   │   ├── util.py             # Funções utilitárias
│   │   ├── codigos_erro.py     # Mapeamento de códigos de erro
│   │   ├── db.py               # Conexão com banco de dados
│   │   ├── dw_model.py         # Modelos SQLAlchemy
│   │   └── validator_service.py # Serviço de validação
│   └── __pycache__/            # Cache Python
├── data/                        # Arquivos de dados
│   ├── local.db                # Banco SQLite local
│   └── *.xlsx                  # Planilhas de exemplo
├── logs/                        # Logs da aplicação
│   └── jobs.log
├── sql/                         # Scripts SQL
│   ├── schema_backend.sql      # Schema de controle
│   └── schema_public.sql       # Schema público
├── tests/                       # Testes
│   └── test_contrato.py
├── settings.toml               # Configurações
├── pyproject.toml              # Dependências do projeto
└── README.md                   # Este arquivo
```

## 🚀 Requisitos

- **Python** 3.12+
- **PostgreSQL** (para persistência de dados)
- Dependências listadas em `pyproject.toml`

## ⚙️ Configuração

### 1. Criar ambiente virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar dependências

```powershell
pip install -e .
```

## 🎯 Como Usar

### Executar a aplicação Streamlit

```powershell
streamlit run app/aplicacao.py
```

A aplicação abrirá no navegador em `http://localhost:8501`

### Fluxo de Validação

1. **Upload da planilha**: Faça upload de um arquivo `.xlsx` contendo as abas:
   - `Setores`
   - `Empresas`
   - `Cargos`
   - `Modelo F` (Funcionários)

2. **Validação automática**: O sistema irá:
   - Normalizar os dados
   - Validar integridade referencial
   - Aplicar schemas de validação
   - Classificar erros (críticos vs avisos)

3. **Downloads disponíveis**:
   - 📁 **Planilha normalizada**: Dados limpos e padronizados
   - 📋 **Relatório de erros**: Excel com detalhamento de todos os erros encontrados

## 📊 Tipos de Validação

### Campos Obrigatórios (CRÍTICOS)
Erros nesses campos impedem a aprovação da planilha:
- Códigos de identificação
- Nomes
- Datas essenciais
- CPF/CNPJ

### Campos Opcionais (AVISOS)
Avisos não impedem a aprovação:
- `cod_empresa`, `telefone`, `cod_cbo`
- `nome_social`, `trabalho_em_altura`
- `dt_admissao`, `pis_pasep`, `rg`
- `uf_do_rg`, `emissor_rg`, `ctps`
- `serie_ctps`, `uf_ctps`
- `endereco`, `numero`, `bairro`
- `cidade`, `uf`, `celular`, `cep`

### Integridade Referencial
- **Funcionários → Setores**: Valida `cod_setor`
- **Funcionários → Cargos**: Valida `cod_cargo`
- **Cargos → Setores**: Valida `cod_setor`

## 🔧 Scripts Disponíveis

### Gerar planilha normalizada localmente
```powershell
python generate_normalized.py
```

## 📝 Relatório de Erros

O relatório de erros gerado contém:
- **Código do Erro**: Identificador único
- **Descrição**: Explicação do erro
- **Mensagem Detalhada**: Contexto específico
- **Planilha**: Aba onde ocorreu
- **Linha**: Linha exata do erro
- **Coluna**: Campo com problema
- **Tipo**: Categoria do erro
- **Severidade**: CRÍTICO ou AVISO
