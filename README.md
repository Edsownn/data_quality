# data-quality

Projeto para validação de dados de setores de empresas utilizando Pandas, Pandera, PyJanitor e Streamlit.

## Estrutura do Projeto

```
main.py
pyproject.toml
README.md
uv.lock
app/
    core/
        schemas.py 
        util.py
    aplicacao.py
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
- [Streamlit](https://streamlit.io/): Interface web para upload e validação de planilhas
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
   uv venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Instale as dependências:
   ```powershell
   uv pip install -r requirements.txt
   ```

## Uso

### Rodar a aplicação web (Streamlit)

Para iniciar a interface web para upload e validação de planilhas:
```powershell
streamlit run app/aplicacao.py
```

ou no back end

```powershell
python app\app.py
```
## Testes

Para rodar os testes automatizados:
```powershell
pytest
```

## Licença

Este projeto está sob a licença MIT.
