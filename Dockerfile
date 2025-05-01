FROM python:3.9-slim

WORKDIR /app

# Instala o Poetry
RUN pip install poetry

# Copia os arquivos de configuração do Poetry
COPY pyproject.toml poetry.lock* ./

# Configura o Poetry para não criar um ambiente virtual
RUN poetry config virtualenvs.create false

# Instala as dependências
RUN poetry install --no-dev --no-interaction --no-ansi

# Copia o código da aplicação e o arquivo .env
COPY app ./app
COPY .env ./.env

# Expõe a porta 8008
EXPOSE 8008

# Comando para iniciar a aplicação
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8008"] 