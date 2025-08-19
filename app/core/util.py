from unidecode import unidecode
import re

def tratar_caracteres(texto):
        if isinstance(texto, str):
            texto = texto.replace('Ç', 'C').replace('ç', 'c')
            texto = unidecode(texto)
        return texto

def validar_sexo(df):
    if 'sexo' in df.columns:
        mapping = {'feminino':'F','f':'F','masculino':'M','m':'M'}
        df['sexo'] = (df['sexo']
                      .fillna('')
                      .astype(str)
                      .str.strip()
                      .str.lower()
                      .map(mapping)
                      .where(lambda s: s.isin(['F','M'])))