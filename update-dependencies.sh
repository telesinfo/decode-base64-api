#!/bin/bash
# Script para atualizar as dependências do FastAPI e Starlette
# Execute: bash update-dependencies.sh

echo "Atualizando FastAPI e dependências relacionadas..."
poetry update fastapi

echo ""
echo "Verificando versões instaladas..."
poetry show fastapi starlette

echo ""
echo "Atualização concluída! Verifique se o Starlette está na versão 0.47.2 ou superior."

