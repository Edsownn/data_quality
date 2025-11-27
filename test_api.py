"""Script de teste para a API de validação."""

import httpx
import json
from pathlib import Path

# Configurações
API_BASE_URL = "http://localhost:8000"
USER_AUTH_ID = 1
TENANT_ID = 1

# Nome do arquivo que deve estar no S3
# Substitua pelo nome real do arquivo no seu bucket S3
FILE_NAME_IN_S3 = "Modelo Y - Oficial_CALI_20250820.xlsx"


def test_api():
    """Teste completo da API de validação."""
    
    with httpx.Client() as client:
        print("=== Teste da API de Validação ===")
        print(f"URL base: {API_BASE_URL}")
        print(f"Arquivo para validar: {FILE_NAME_IN_S3}")
        print()
        
        # 1. Health check
        print("1. Testando health check...")
        try:
            response = client.get(f"{API_BASE_URL}/health")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                health_data = response.json()
                print(f"Database: {health_data.get('database')}")
                print(f"S3: {health_data.get('s3')}")
            else:
                print(f"Erro: {response.text}")
        except Exception as e:
            print(f"Erro na conexão: {e}")
            return
        print()
        
        # 2. Listar tipos de validação disponíveis
        print("2. Obtendo tipos de validação...")
        try:
            response = client.get(f"{API_BASE_URL}/validation-types")
            if response.status_code == 200:
                types = response.json()
                print("Tipos disponíveis:")
                for vtype in types:
                    print(f"  - {vtype['key']}: {vtype['name']}")
            else:
                print(f"Erro: {response.text}")
        except Exception as e:
            print(f"Erro: {e}")
        print()
        
        # 3. Validar arquivo
        print("3. Validando arquivo...")
        validation_request = {
            "file_name": FILE_NAME_IN_S3,
            "user_auth_id": USER_AUTH_ID,
            "tenant_id": TENANT_ID,
            "validation_type": "auto"  # ou específico: "funcionarios", "empresas", etc.
        }
        
        try:
            response = client.post(
                f"{API_BASE_URL}/validate-file",
                json=validation_request,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Validação bem-sucedida: {result['success']}")
                print(f"Tipo de validação: {result['validation_type']}")
                print(f"Total de linhas: {result['data_quality']['total_rows']}")
                print(f"Total de colunas: {result['data_quality']['total_columns']}")
                print(f"Erros encontrados: {len(result['errors'])}")
                print(f"Avisos: {len(result['warnings'])}")
                print(f"Score de qualidade: {result['summary']['data_quality_score']:.2f}/100")
                
                if result['errors']:
                    print("\nPrimeiros 5 erros:")
                    for i, error in enumerate(result['errors'][:5]):
                        print(f"  {i+1}. Linha {error.get('row', 'N/A')}, Coluna {error['column']}: {error['error_message']}")
                
                validation_id = result.get('validation_id')
                print(f"\nID da validação salva: {validation_id}")
                
            else:
                error_data = response.json()
                print(f"Erro na validação: {error_data.get('detail', response.text)}")
                
        except Exception as e:
            print(f"Erro na validação: {e}")
        print()
        
        # 4. Obter validações recentes
        print("4. Obtendo validações recentes...")
        try:
            response = client.get(f"{API_BASE_URL}/validations/recent/{TENANT_ID}?limit=5")
            if response.status_code == 200:
                validations = response.json()
                print(f"Encontradas {len(validations)} validações recentes:")
                for val in validations:
                    success_status = "✅ Sucesso" if val['success'] else "❌ Falhou"
                    print(f"  - {val['file_name']} | {success_status} | {val['validated_at']}")
            else:
                print(f"Erro: {response.text}")
        except Exception as e:
            print(f"Erro: {e}")
        print()
        
        # 5. Obter estatísticas
        print("5. Obtendo estatísticas...")
        try:
            response = client.get(f"{API_BASE_URL}/stats/{TENANT_ID}")
            if response.status_code == 200:
                stats = response.json()
                print(f"Total de validações: {stats['total']}")
                print(f"Sucessos: {stats['successful']}")
                print(f"Falhas: {stats['failed']}")
                print(f"Taxa de sucesso: {stats['success_rate']:.2f}%")
            else:
                print(f"Erro: {response.text}")
        except Exception as e:
            print(f"Erro: {e}")
        print()


def test_different_validation_types():
    """Testa diferentes tipos de validação."""
    validation_types = ["auto", "funcionarios", "empresas", "setores", "cargos"]
    
    with httpx.Client() as client:
        print("=== Teste de Diferentes Tipos de Validação ===")
        
        for vtype in validation_types:
            print(f"\nTestando validação tipo: {vtype}")
            
            validation_request = {
                "file_name": FILE_NAME_IN_S3,
                "user_auth_id": USER_AUTH_ID,
                "tenant_id": TENANT_ID,
                "validation_type": vtype
            }
            
            try:
                response = client.post(
                    f"{API_BASE_URL}/validate-file",
                    json=validation_request
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"  ✅ Sucesso: {result['success']}")
                    print(f"  📊 Erros: {len(result['errors'])}")
                    print(f"  ⚠️ Avisos: {len(result['warnings'])}")
                else:
                    print(f"  ❌ Erro: {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Exceção: {e}")


def test_error_cases():
    """Testa casos de erro."""
    
    with httpx.Client() as client:
        print("=== Teste de Casos de Erro ===")
        
        # Arquivo inexistente
        print("\n1. Testando arquivo inexistente...")
        validation_request = {
            "file_name": "arquivo_que_nao_existe.xlsx",
            "user_auth_id": USER_AUTH_ID,
            "tenant_id": TENANT_ID,
            "validation_type": "auto"
        }
        
        try:
            response = client.post(f"{API_BASE_URL}/validate-file", json=validation_request)
            print(f"Status: {response.status_code}")
            if response.status_code == 404:
                print("✅ Erro 404 retornado corretamente para arquivo inexistente")
            else:
                print(f"❌ Status inesperado: {response.status_code}")
        except Exception as e:
            print(f"Erro: {e}")
        
        # Dados inválidos
        print("\n2. Testando dados inválidos...")
        invalid_request = {
            "file_name": "",  # Nome vazio
            "user_auth_id": USER_AUTH_ID,
            "tenant_id": TENANT_ID
        }
        
        try:
            response = client.post(f"{API_BASE_URL}/validate-file", json=invalid_request)
            print(f"Status: {response.status_code}")
            if response.status_code == 422:
                print("✅ Erro de validação retornado corretamente")
            else:
                print(f"❌ Status inesperado: {response.status_code}")
        except Exception as e:
            print(f"Erro: {e}")


if __name__ == "__main__":
    print("Escolha o tipo de teste:")
    print("1. Teste completo")
    print("2. Teste de diferentes tipos de validação")
    print("3. Teste de casos de erro")
    print("4. Todos os testes")
    
    choice = input("\nDigite sua opção (1-4): ").strip()
    
    if choice == "1":
        test_api()
    elif choice == "2":
        test_different_validation_types()
    elif choice == "3":
        test_error_cases()
    elif choice == "4":
        test_api()
        test_different_validation_types()
        test_error_cases()
    else:
        print("Opção inválida. Executando teste completo...")
        test_api()