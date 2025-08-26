# Sistema de Códigos de Erro - Guia de Uso

## Como Aplicar os Códigos de Erro ao seu Relatório

O sistema de códigos de erro foi integrado ao seu projeto para padronizar e categorizar todos os erros encontrados durante a validação de dados. Aqui está como usar:

## 1. Estrutura dos Códigos

### Grupo 001 – Campos Obrigatórios (nullable=False)
- **001.1**: Campo obrigatório vazio ou nulo
- **001.2**: Campo obrigatório preenchido apenas com espaços

### Grupo 002 – Restrições de Tamanho e Formato
- **002.1**: Campo com tamanho fora do limite permitido
- **002.2**: Campo com formato inválido

### Grupo 003 – Validações de Valores
- **003.1**: Valor numérico inválido (deve ser maior que zero)
- **003.2**: Valor fora da lista de opções válidas (sexo, situação)

### Grupo 005 – Validações de Data
- **005.1**: Data fora do intervalo válido (anterior a 1900 ou posterior a hoje)
- **005.2**: Data inconsistente entre campos relacionados

### Grupo 006 – Campos Opcionais (nullable=True)
- **006.1**: Campo opcional em branco (desejável preenchimento)
- **006.2**: Campo opcional com tamanho fora do limite permitido
- **006.3**: Campo opcional incompleto
- **006.4**: Endereço incompleto ou inconsistente
- **006.5**: Contato incompleto (telefone/celular)

## 2. Como Funciona a Atribuição Automática

O sistema automaticamente mapeia erros do Pandera para códigos baseado em:

1. **Tipo do campo**: Obrigatório vs Opcional
2. **Conteúdo da mensagem**: Palavras-chave específicas
3. **Nome da coluna**: Para casos específicos como endereço e telefone

### Exemplo de Mapeamento:
```python
# Erro original do Pandera:
"Nome Funcionario não pode ser vazio e deve ter até 150 caracteres"

# Resultado do mapeamento:
# Se campo obrigatório: Código 002.1 (tamanho fora do limite)
# Se campo opcional: Código 006.2 (campo opcional com tamanho incorreto)
```

## 3. Estrutura do Relatório

Agora seu relatório inclui:

### Colunas do Relatório:
- **codigoERRO**: Código padronizado (ex: "001.1")
- **Descrição do Código**: Explicação padrão do tipo de erro
- **Mensagem Detalhada**: Mensagem específica do Pandera
- **planilha**: Nome da aba/planilha
- **linha**: Linha no Excel onde ocorreu o erro
- **coluna**: Nome da coluna
- **tipo**: OBRIGATORIO ou OPCIONAL
- **severidade**: CRÍTICO ou AVISO

### Exemplo de Linha do Relatório:
```
codigoERRO: 001.1
Descrição do Código: Campo obrigatório vazio ou nulo
Mensagem Detalhada: Nome Funcionario não pode ser vazio
planilha: Modelo F
linha: 15
coluna: nome_funcionario
tipo: OBRIGATORIO
severidade: CRÍTICO
```

### Para Desenvolvedores:
```python
from core.codigos_erro import mapear_codigo_erro, obter_descricao_codigo

# Mapear um erro
codigo = mapear_codigo_erro("Campo vazio", "nome", nullable=False)
# Resultado: "001.1"

descricao = obter_descricao_codigo(codigo)
# Resultado: "Campo obrigatório vazio ou nulo"
```

### Para Analistas:
1. Execute sua validação normalmente no Streamlit
2. O sistema automaticamente aplicará os códigos
3. Baixe o relatório com códigos padronizados
4. Use o resumo por código para priorizar correções

## 6. Vantagens do Sistema

### Para Gestão:
- **Padronização**: Todos os erros seguem a mesma classificação
- **Priorização**: Códigos 001-003 são críticos, 006 são avisos
- **Rastreabilidade**: Histórico consistente de tipos de problemas

### Para Usuários:
- **Clareza**: Entendimento imediato do tipo de problema
- **Ação**: Saber exatamente o que corrigir
- **Eficiência**: Correção por lotes de mesmo tipo de erro

## 7. Personalização

### Adicionar Novos Códigos:
Edite `core/codigos_erro.py`:

```python
CODIGOS_ERRO = {
    # Seus códigos existentes...
    "007.1": "Nova categoria de erro",
    "007.2": "Outro tipo de erro específico"
}
```

### Personalizar Mapeamento:
Edite a função `mapear_codigo_erro()` para incluir novos padrões:

```python
if "sua_regra_especifica" in mensagem_lower:
    return "007.1"
```

## 8. Exemplos de Uso

Veja o arquivo `exemplo_uso_codigos.py` para:
- Validação customizada com códigos
- Criação de relatórios multi-aba
- Integração com outros sistemas
