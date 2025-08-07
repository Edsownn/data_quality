from unidecode import unidecode
import re

def tratar_caracteres(texto):
        if isinstance(texto, str):
            texto = texto.replace('Ç', 'C').replace('ç', 'c')
            texto = unidecode(texto)
        return texto