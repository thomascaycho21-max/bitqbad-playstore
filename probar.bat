@echo off
chcp 65001 >nul
title BitQbad PlayStore - Probar (sin venv)
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 ( echo [ERROR] Python no encontrado & pause & exit /b 1 )

echo.
echo ============================================
echo   BitQbad PlayStore - Modo Prueba
echo   (sin venv - usa Python global)
echo ============================================
echo.
echo   [1] Web (navegador)
echo   [2] Windows (ventana nativa)
echo   [3] Android (requiere dispositivo/emulador)
echo   [4] Instalar/actualizar dependencias
echo   [5] Salir
echo.
set /p OPC="Elige [1-5]: "

if "%OPC%"=="1" (
    python -m pip install -r requirements.txt
    flet run --web --port 8550 main.py
    pause
) else if "%OPC%"=="2" (
    python -m pip install -r requirements.txt
    flet run main.py
    pause
) else if "%OPC%"=="3" (
    python -m pip install -r requirements.txt
    flet run --android main.py
    pause
) else if "%OPC%"=="4" (
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    echo [OK] Dependencias instaladas.
    pause
) else (
    exit /b 0
)
