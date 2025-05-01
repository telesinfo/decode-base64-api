# Decode Base64 API

API para decodificar arquivos base64 em diferentes formatos.

## Requisitos

- Python 3.9+
- Poetry
- Docker e Docker Compose (opcional)

## Configuração

1. Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
```bash
API_TOKEN="seu_token_aqui"
```

## Instalação e Execução Local

1. Instale as dependências usando Poetry:
```bash
poetry install
```

2. Execute a aplicação:
```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8008 --reload
```

## Padrões de Código

Este projeto segue rigorosos padrões de código e formatação:

### Formatação

- **PEP 8**: Seguimos as diretrizes do PEP 8 para estilo de código Python
- **Blue**: Formatador de código baseado no Black, com configurações específicas
- **isort**: Organização automática de imports
- **EditorConfig**: Configurações consistentes entre diferentes editores

### Comandos de Formatação

```bash
# Verificar formatação
poetry run task lint

# Aplicar formatação automaticamente
poetry run task format
```

### Configurações

- Comprimento máximo de linha: 79 caracteres
- Indentação: 4 espaços
- Ordenação de imports: Compatível com Black
- Encoding: UTF-8
- Final de linha: LF (Unix-style)

## Execução com Docker

### Usando Docker Compose (Recomendado)

1. Certifique-se de que o arquivo `.env` está presente na raiz do projeto

2. Execute a aplicação:
```bash
docker-compose up -d
```

3. Para parar a aplicação:
```bash
docker-compose down
```

### Usando Docker diretamente

1. Construa a imagem:
```bash
docker build -t decode-base64-api .
```

2. Execute o container:
```bash
docker run -p 8008:8008 decode-base64-api
```

## Uso da API

A API estará disponível em `http://localhost:8008`

### Autenticação

A API requer autenticação via token no header da requisição. O token deve ser o mesmo configurado no arquivo `.env`:

```
Token: seu_token_aqui
```

### Endpoints

#### POST /decode
Decodifica um arquivo base64 e retorna o arquivo original.

Exemplo de requisição:
```bash
curl -X POST http://localhost:8008/decode \
  -H "Token: seu_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "base64_string": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",
    "file_extension": "png"
}'
```

#### GET /health
Verifica o status da API.

## Documentação da API

A documentação completa da API está disponível em:
- Swagger UI: `http://localhost:8008/docs`
- ReDoc: `http://localhost:8008/redoc`

## Segurança

- O token de autenticação é armazenado no arquivo `.env` que não deve ser commitado no controle de versão
- Adicione `.env` ao seu arquivo `.gitignore` 