#!/bin/bash
# Script para iniciar o projeto AIRO.AI
echo "========================================="
echo "==   Iniciando o Servidor AIRO.AI      =="
echo "========================================="
echo ""
echo "--> Ativando o ambiente virtual (venv)..."
source backend/venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERRO: Não foi possível ativar o ambiente virtual."
    exit 1
fi
echo "--> Ambiente virtual ativado com sucesso."
echo ""
echo "--> Iniciando o servidor Flask em http://127.0.0.1:5000"
echo "--> Pressione CTRL+C nesta janela para parar o servidor."
echo ""
python3 backend/app.py
