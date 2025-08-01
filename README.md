
# data-quality

Projeto para validação de dados de setores de empresas utilizando Pandas, Pandera e PyJanitor.

## Estrutura do Projeto

```
main.py
pyproject.toml
README.md
uv.lock
app/
    app.py
    contrato.py
    __init__.py
data/
    Template_ModeloF.xlsx
tests/
    test_contrato.py
```

## Principais Tecnologias

- [Pandas](https://pandas.pydata.org/): Manipulação de dados
- [Pandera](https://pandera.readthedocs.io/): Validação de DataFrames
- [PyJanitor](https://pyjanitor-devs.github.io/pyjanitor/): Limpeza de dados
- [pytest](https://pytest.org/): Testes automatizados
- [uv](https://github.com/astral-sh/uv): Gerenciamento de ambiente e dependências

## Instalação

1. Clone o repositório:
   ```powershell
   git clone <url-do-repositorio>
   cd data_quality
   ```
2. Crie e ative o ambiente virtual com uv:
   ```powershell
   uv venv .venv ; .\.venv\Scripts\Activate.ps1
   ```
3. Instale as dependências:
   ```powershell
   uv pip install -r uv.lock
   ```

## Uso

Execute o script principal:
```powershell
uv run python main.py
```
Ou rode diretamente os scripts em `app/` conforme necessidade.

## Testes

Para rodar os testes automatizados:
```powershell
uv run pytest
```

## Exemplo de Validação

O modelo de validação está em `app/contrato.py`:
```python
class MetricasSetores(pa.DataFrameModel):
    CodSetor: Series[int] = pa.Field(alias="Cod Setor")
    NomeSetor: Series[str] = pa.Field(alias="Nome Setor")
    cnpjEmpresa: Series[str] = pa.Field(alias="CNPJ da Empresa")

    class Config:
        coerce = True
        strict = True
```

## Licença

Este projeto está sob a licença MIT.
