CODIGOS_ERRO = {
    # Grupo 001 – Campos Obrigatórios (nullable=False)
    "101": "Campo obrigatório vazio ou nulo",
    "102": "Campo obrigatório preenchido apenas com espaços",
    
    # Grupo 2 – Restrições de Tamanho e Formato
    "201": "Campo com tamanho fora do limite permitido",
    "202": "Campo com formato inválido",
    
    # Grupo 3 – Validações de Valores
    "301": "Valor numérico inválido (deve ser maior que zero)",
    "302": "Valor fora da lista de opções válidas (sexo, situação)",

    # Grupo 4 – Validações de Data
    "401": "Data fora do intervalo válido (anterior a 1900 ou posterior a hoje)",
    "402": "Data inconsistente entre campos relacionados",

    # Grupo 5 – Campos Opcionais (nullable=True)
    "501": "Campo opcional em branco (desejável preenchimento)",
    "502": "Campo opcional com tamanho fora do limite permitido",
    "503": "Campo opcional incompleto",
    "504": "Endereço incompleto ou inconsistente",
    "505": "Contato incompleto (telefone/celular)",

    # Grupo 6 - Campos únicos e integridade referencial
    "601": "Valor duplicado em campo que deve ser único",
    "602": "Código não encontrado na tabela de referência",
}

def mapear_codigo_erro(mensagem_erro: str, coluna: str, nullable: bool = False) -> str:
    mensagem_lower = mensagem_erro.lower()
    
    # Verificações de integridade referencial e uniqueness PRIMEIRO
    if any(termo in mensagem_lower for termo in ["não existe na tabela", "referência", "integridade_referencial"]):
        return "602"
    
    if any(termo in mensagem_lower for termo in ["duplicado", "unique", "duplicates", "único"]):
        return "601"
    
    
    # Campos obrigatórios (nullable=False)
    if not nullable:
        if any(termo in mensagem_lower for termo in ["nulo", "null", "vazio", "não pode ser"]):
            return "101"
        if "espaços" in mensagem_lower or "trim" in mensagem_lower:
            return "102"

    # Restrições de tamanho
    if any(termo in mensagem_lower for termo in ["caracteres", "tamanho", "len", "between"]):
        return "201" if not nullable else "502"

    # Formato inválido
    if any(termo in mensagem_lower for termo in ["formato", "match", "pattern", "regex"]):
        return "202"

    # Valores numéricos
    if any(termo in mensagem_lower for termo in ["maior que zero", "> 0", "positivo"]):
        return "301"

    # Valores de lista (sexo, situação, etc.
    if any(termo in mensagem_lower for termo in ["sexo", "situação", "ativo", "inativo", "feminino", "masculino"]):
        return "302"

    # Datas
    if any(termo in mensagem_lower for termo in ["data", "1900", "atual", "timestamp"]):
        if "anterior" in mensagem_lower or "posterior" in mensagem_lower:
            return "401"
        else:
            return "402"

    # Campos opcionais específicos
    if nullable:
        if coluna in ["endereco", "numero", "bairro", "cidade", "uf", "cep"]:
            return "504"
        if coluna in ["telefone", "celular"]:
            return "505"
        if "incompleto" in mensagem_lower:
            return "503"
        return "501"
    
    # Padrão para casos não mapeados
    return "201"


def obter_descricao_codigo(codigo: str) -> str:
    return CODIGOS_ERRO.get(codigo, "Erro não catalogado")

COLUNAS_OPCIONAIS = {
    "cod_empresa", "telefone", "cod_cbo", "nome_social", 
    "trabalho_em_altura", "dt_admissao", "pis_pasep", "rg",
    "uf_do_rg", "emissor_rg", "ctps", "serie_ctps", "uf_ctps",
    "endereco", "numero", "bairro", "cidade", "uf", "celular", "cep",
    "descricao_detalhada_do_cargo"
}

def eh_campo_opcional(coluna: str) -> bool:
    return coluna in COLUNAS_OPCIONAIS

def mapear_codigo_erro_pandera(mensagem_erro: str, coluna: str) -> str:
    mensagem_lower = mensagem_erro.lower()
    
    # Detecção de violação unique (duplicatas)
    if any(termo in mensagem_lower for termo in ["duplicates", "unique", "duplicated values"]):
        return "601"
    
    # Outros erros específicos do pandera
    if "check" in mensagem_lower and "unique" in mensagem_lower:
        return "601"
    
    # Fallback para função padrão
    nullable = eh_campo_opcional(coluna)
    return mapear_codigo_erro(mensagem_erro, coluna, nullable)
