FROM python:3.9-slim

WORKDIR /app

# Instala o Poetry e curl para healthcheck
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install poetry

# Copia os arquivos de configuração do Poetry e README
COPY pyproject.toml poetry.lock* README.md ./

# Configura o Poetry para não criar um ambiente virtual
RUN poetry config virtualenvs.create false

# Copia o código da aplicação
COPY src ./src
COPY app ./app
COPY .env ./.env

# Instala apenas as dependências de produção
RUN poetry install --only main --no-interaction --no-ansi

# Expõe a porta 8008
EXPOSE 8008

# Comando para iniciar a aplicação
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8008"] 