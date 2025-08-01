import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import numpy as np
import pandera as pa
import pytest
from app.contrato import MetricasSetores

def test_contrato_correto():
    df_test = pd.DataFrame({
        "Cod Setor": [1, 2, 3],
        "Nome Setor": ["Administratico", "Obras", "Operacional"],
        "CNPJ da Empresa": ["12.345.678/0001-90", "98.765.432/0001-55", "32.165.498/0001-77"]
    })

    MetricasSetores.validate(df_test)

def test_contrato_incorreto():
    df_test = pd.DataFrame({
        "Cod Setor": [1, 2, "três"],
        "Nome Setor": ["Administratico", "Obras", 123],
        "CNPJ da Empresa": ["12.345.678/0001-90", "98.765.432/0001-55", "32.165.498/0001-77"]
    })

    MetricasSetores.validate(df_test)

def test_coluna_faltando():
    df_test = pd.DataFrame({
        "Cod Setor": [1, 2, 3],
        "Nome Setor": ["Administratico", "Obras", "Operacional"]
    })

    MetricasSetores.validate(df_test)