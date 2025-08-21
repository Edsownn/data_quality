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
