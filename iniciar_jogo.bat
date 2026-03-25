@echo off
title Iniciando Jogo da Cobrinha (Snake Game)...
cls

echo ===========================================
echo   VERIFICANDO AMBIENTE PYTHON...
echo ===========================================

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado! 
    echo Por favor, instale o Python em: https://python.org
    pause
    exit
)

echo [OK] Python detectado. Prepare os reflexos!
python main.py
pause
