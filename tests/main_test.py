import base64
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app, verify_token

client = TestClient(app)

# Dados de exemplo para testes
VALID_TOKEN = 'test_token'
VALID_BASE64_PNG = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII='
INVALID_BASE64 = 'invalid_base64_string'


#def test_health_check():
#    """Testa o endpoint de verificação de saúde."""
#    response = client.get('/health')
#    assert response.status_code == 200
#    assert response.json() == {'status': 'healthy'}


@patch('app.main.API_TOKEN', VALID_TOKEN)
def test_valid_token():
    """Testa a autenticação com token válido."""
    response = client.post(
        '/decode',
        headers={'Token': VALID_TOKEN},
        json={'base64_string': VALID_BASE64_PNG, 'file_extension': 'png'},
    )
    assert response.status_code == 200


@patch('app.main.API_TOKEN', VALID_TOKEN)
def test_invalid_token():
    """Testa a rejeição de token inválido."""
    response = client.post(
        '/decode',
        headers={'Token': 'invalid_token'},
        json={'base64_string': VALID_BASE64_PNG, 'file_extension': 'png'},
    )
    assert response.status_code == 401


@patch('app.main.API_TOKEN', VALID_TOKEN)
def test_decode_valid_png():
    """Testa a decodificação de uma imagem PNG válida."""
    response = client.post(
        '/decode',
        headers={'Token': VALID_TOKEN},
        json={'base64_string': VALID_BASE64_PNG, 'file_extension': 'png'},
    )
    assert response.status_code == 200
    assert response.headers['content-type'] == 'image/png'


@patch('app.main.API_TOKEN', VALID_TOKEN)
def test_decode_invalid_base64():
    """Testa o tratamento de string base64 inválida."""
    response = client.post(
        '/decode',
        headers={'Token': VALID_TOKEN},
        json={'base64_string': INVALID_BASE64, 'file_extension': 'png'},
    )
    assert response.status_code == 400
    assert 'String base64 inválida' in response.json()['detail']


@patch('app.main.API_TOKEN', VALID_TOKEN)
def test_decode_unsupported_extension():
    """Testa a rejeição de extensão de arquivo não suportada."""
    response = client.post(
        '/decode',
        headers={'Token': VALID_TOKEN},
        json={
            'base64_string': VALID_BASE64_PNG,
            'file_extension': 'unsupported',
        },
    )
    assert response.status_code == 400
    assert 'Extensão de arquivo não suportada' in response.json()['detail']


@patch('app.main.API_TOKEN', VALID_TOKEN)
def test_missing_token():
    """Testa a requisição sem token de autenticação."""
    response = client.post(
        '/decode',
        json={'base64_string': VALID_BASE64_PNG, 'file_extension': 'png'},
    )
    assert response.status_code == 422


@patch('app.main.API_TOKEN', VALID_TOKEN)
def test_missing_required_fields():
    """Testa a requisição com campos obrigatórios ausentes."""
    response = client.post('/decode', headers={'Token': VALID_TOKEN}, json={})
    assert response.status_code == 422
