from unidecode import unidecode
import re

def tratar_caracteres(texto):
        if isinstance(texto, str):
            texto = texto.replace('Ç', 'C').replace('ç', 'c')
            texto = unidecode(texto)
        return texto

def validar_sexo(df, coluna='sexo'):
    if coluna not in df.columns:
        return df
    ser = df[coluna].astype(str).str.strip()
    ser_norm = (ser
                .str.lower()
                .map({'f': 'F',
                      'feminino': 'F',
                      'm': 'M',
                      'masculino': 'M'}))
    df[coluna] = ser_norm.where(ser_norm.isin(['F','M']))
    return df
         

def tratar_cep(valor):
    if valor is None:
        return valor
    
    digits = re.sub(r'\D', '', str(valor))
    if len(digits) != 8:
        return valor
    return f"{digits[:5]}-{digits[5:]}"

def normalizar_coluna_cep(df, coluna='cep'):
    if coluna in df.columns:
        df[coluna] = df[coluna].apply(tratar_cep)
    return df

def verificar_integridade(df_fk, df_pk, coluna_fk, coluna_pk):
    erros = []
    
    # Verifica se as colunas existem
    if coluna_fk not in df_fk.columns:
        return [{
            "codigo_invalido": "N/A",
            "quantidade_registros": 0,
            "linhas_afetadas": [],
            "erro": f"Coluna '{coluna_fk}' não encontrada na tabela principal"
        }]
    
    if coluna_pk not in df_pk.columns:
        return [{
            "codigo_invalido": "N/A", 
            "quantidade_registros": 0,
            "linhas_afetadas": [],
            "erro": f"Coluna '{coluna_pk}' não encontrada na tabela de referência"
        }]
    
    valores_pk = set(df_pk[coluna_pk].dropna().unique())  # Chaves primárias válidas
    valores_fk = set(df_fk[coluna_fk].dropna().unique())  # Chaves estrangeiras usadas
    
    fks_invalidas = valores_fk - valores_pk
    
    if fks_invalidas:
        for fk_invalida in fks_invalidas:
            linhas_com_erro = df_fk[df_fk[coluna_fk] == fk_invalida].index.tolist()
            linhas_excel = [linha + 2 for linha in linhas_com_erro]
            
            erros.append({
                "codigo_invalido": fk_invalida,  # Nome genérico em vez de "codigo_setor_invalido"
                "quantidade_registros": len(linhas_com_erro),
                "linhas_afetadas": linhas_excel,
                "erro": f"Código '{fk_invalida}' da coluna '{coluna_fk}' não existe na tabela de referência"
            })
    
    return erros