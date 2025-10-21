import requests
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import json
import os
from jsonschema import validate

# Constantes
API_URL = "" # preenchida pelo Given

# Variável global para armazenar a última resposta da API
response = None

# Mapeia todos os cenários do arquivo .feature
scenarios('../features/usuarios.feature')

# --- Implementação dos Steps ---

@given(parsers.parse('que o serviço da API está acessível na url "{base_url}"'))
def api_service_available(base_url):
    global API_URL
    API_URL = base_url
    try:
        # Tenta fazer um request simples para a raiz para verificar a conexão
        ping_response = requests.get(API_URL, timeout=5)
        ping_response.raise_for_status() # Levanta erro se status for 4xx ou 5xx
        print(f"API acessível em: {API_URL}")
    except requests.exceptions.ConnectionError as e:
        pytest.fail(f"Erro de conexão ao tentar acessar {API_URL}. A API está rodando no Docker? Erro: {e}")
    except requests.exceptions.Timeout:
         pytest.fail(f"Timeout ao tentar acessar {API_URL}.")
    except requests.exceptions.RequestException as e:
         pytest.fail(f"Erro durante o ping na API em {API_URL}: {e}")

@when(parsers.parse('eu faço uma requisição GET para "{endpoint}"'))
def make_get_request(endpoint):
    global response
    full_url = API_URL + endpoint
    try:
        response = requests.get(full_url)
        print(f"GET request para {full_url} - Status: {response.status_code}")
    except Exception as e:
        pytest.fail(f"Erro inesperado durante a requisição GET para {full_url}: {e}")

@then(parsers.parse('o status code da resposta deve ser {status_code:d}'))
def check_status_code(status_code):
    global response
    assert response is not None, "Nenhuma resposta da API foi recebida antes de verificar o status code"
    assert response.status_code == status_code, f"Esperado status {status_code} mas recebido {response.status_code}. Resposta: {response.text[:200]}..." # Limita o tamanho da resposta no log

@then('o corpo da resposta (JSON) deve ser uma lista')
def check_response_body_is_list():
    global response
    assert response is not None, "Nenhuma resposta da API foi recebida antes de verificar o corpo"
    try:
        json_response = response.json()
        assert isinstance(json_response, list), f"Esperado uma lista, mas recebido {type(json_response)}. Resposta: {json_response}"
    except ValueError: # Erro ao decodificar JSON
        pytest.fail(f"A resposta não é um JSON válido: {response.text[:200]}...")

@then(parsers.parse('o corpo da resposta (JSON) deve corresponder ao schema "{schema_file}"'))
def check_response_schema(schema_file):
    global response
    assert response is not None, "Nenhuma resposta da API foi recebida antes de verificar o schema"
    schema_path = os.path.join('tests', 'schemas', schema_file)

    try:
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        response_json = response.json()
        validate(instance=response_json, schema=schema)
        print(f"Validação do schema {schema_file} passou!")
    except FileNotFoundError:
        pytest.fail(f"Arquivo de schema não encontrado em: {schema_path}")
    except json.JSONDecodeError:
        pytest.fail(f"Erro ao decodificar o arquivo de schema: {schema_path} ou a resposta da API: {response.text[:200]}...")
    except ValueError:
         pytest.fail(f"A resposta da API não é um JSON válido para validação de schema: {response.text[:200]}...")
    except Exception as e: # Captura erros de validação do jsonschema
        pytest.fail(f"Erro na validação do schema {schema_file}: {e}")