"""
Exemplo de uso dos códigos de erro em validações customizadas
"""

import pandas as pd
from core.codigos_erro import mapear_codigo_erro, obter_descricao_codigo, eh_campo_opcional

def validar_dados_com_codigos(df: pd.DataFrame, nome_planilha: str) -> list:
    """
    Exemplo de função que valida dados e retorna erros com códigos padronizados
    
    Args:
        df: DataFrame para validar
        nome_planilha: Nome da planilha/aba
    
    Returns:
        Lista de erros com códigos padronizados
    """
    erros = []
    
    for idx, row in df.iterrows():
        linha_excel = idx + 2  # +2 porque pandas é 0-indexed e Excel tem header
        
        # Exemplo: Validação de CPF
        if 'cpf' in df.columns:
            cpf = row.get('cpf', '')
            if pd.isna(cpf) or str(cpf).strip() == '':
                codigo = mapear_codigo_erro("Campo obrigatório vazio", 'cpf', False)
                erros.append({
                    "codigoERRO": codigo,
                    "Descrição do Código": obter_descricao_codigo(codigo),
                    "Mensagem Detalhada": "CPF não pode estar vazio",
                    "planilha": nome_planilha,
                    "linha": linha_excel,
                    "coluna": "cpf",
                    "tipo": "OBRIGATORIO",
                    "severidade": "CRÍTICO"
                })
            elif len(str(cpf).replace('.', '').replace('-', '')) != 11:
                codigo = mapear_codigo_erro("Campo com formato inválido", 'cpf', False)
                erros.append({
                    "codigoERRO": codigo,
                    "Descrição do Código": obter_descricao_codigo(codigo),
                    "Mensagem Detalhada": "CPF deve ter 11 dígitos",
                    "planilha": nome_planilha,
                    "linha": linha_excel,
                    "coluna": "cpf",
                    "tipo": "OBRIGATORIO",
                    "severidade": "CRÍTICO"
                })
        
        # Exemplo: Validação de telefone (campo opcional)
        if 'telefone' in df.columns:
            telefone = row.get('telefone', '')
            if pd.notna(telefone) and str(telefone).strip() != '':
                if len(str(telefone).replace('(', '').replace(')', '').replace('-', '').replace(' ', '')) < 10:
                    codigo = mapear_codigo_erro("Contato incompleto", 'telefone', True)
                    erros.append({
                        "codigoERRO": codigo,
                        "Descrição do Código": obter_descricao_codigo(codigo),
                        "Mensagem Detalhada": "Telefone incompleto - deve ter pelo menos 10 dígitos",
                        "planilha": nome_planilha,
                        "linha": linha_excel,
                        "coluna": "telefone",
                        "tipo": "OPCIONAL",
                        "severidade": "AVISO"
                    })
    
    return erros

def criar_relatorio_final(todos_erros: list, nome_arquivo: str = "relatorio_final.xlsx"):
    """
    Cria um relatório final consolidado com múltiplas abas
    
    Args:
        todos_erros: Lista com todos os erros encontrados
        nome_arquivo: Nome do arquivo de saída
    """
    if not todos_erros:
        print("Nenhum erro encontrado!")
        return
    
    df_erros = pd.DataFrame(todos_erros)
    
    with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
        # Aba 1: Todos os erros
        df_erros.to_excel(writer, sheet_name='Todos_os_Erros', index=False)
        
        # Aba 2: Resumo por código
        resumo_codigos = df_erros.groupby('codigoERRO').agg({
            'Descrição do Código': 'first',
            'linha': 'count',
            'planilha': lambda x: ', '.join(x.unique()),
            'coluna': lambda x: ', '.join(x.unique()),
            'severidade': 'first'
        }).rename(columns={'linha': 'Quantidade'}).reset_index()
        
        resumo_codigos.to_excel(writer, sheet_name='Resumo_por_Código', index=False)
        
        # Aba 3: Resumo por planilha
        resumo_planilhas = df_erros.groupby('planilha').agg({
            'linha': 'count',
            'codigoERRO': lambda x: ', '.join(x.unique()),
            'severidade': lambda x: 'CRÍTICO' if 'CRÍTICO' in x.values else 'AVISO'
        }).rename(columns={'linha': 'Total_Erros'}).reset_index()
        
        resumo_planilhas.to_excel(writer, sheet_name='Resumo_por_Planilha', index=False)
        
        # Aba 4: Apenas erros críticos
        erros_criticos = df_erros[df_erros['severidade'] == 'CRÍTICO']
        if not erros_criticos.empty:
            erros_criticos.to_excel(writer, sheet_name='Erros_Críticos', index=False)
    
    print(f"Relatório salvo como: {nome_arquivo}")

# Exemplo de uso
if __name__ == "__main__":
    # Dados de exemplo
    dados_exemplo = pd.DataFrame({
        'cpf': ['123.456.789-10', '', '12345', '987.654.321-00'],
        'telefone': ['(11) 99999-9999', '11 9999', '', '(21) 88888-8888'],
        'nome': ['João Silva', 'Maria Santos', 'Pedro Oliveira', 'Ana Costa']
    })
    
    # Validar dados
    erros_encontrados = validar_dados_com_codigos(dados_exemplo, 'Funcionários')
    
    # Criar relatório
    if erros_encontrados:
        criar_relatorio_final(erros_encontrados, 'exemplo_relatorio_erros.xlsx')
        print(f"Encontrados {len(erros_encontrados)} erros")
        for erro in erros_encontrados:
            print(f"  {erro['codigoERRO']}: {erro['Mensagem Detalhada']} (Linha {erro['linha']})")
    else:
        print("Nenhum erro encontrado nos dados de exemplo!")
