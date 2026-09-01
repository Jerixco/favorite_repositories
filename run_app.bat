@echo off
:: Catálogo Web — launcher com venv ativado
:: Roda o app Flask usando o Python do hermes-agent venv

set "VENV_PYTHON=C:\Users\Bktech\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"

if not exist "%VENV_PYTHON%" (
    echo Erro: Python do venv não encontrado em %VENV_PYTHON%
    echo Instale o Flask com: pip install flask
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════
echo   Catálogo Web — http://localhost:5000
echo ═══════════════════════════════════════════════
echo.

"%VENV_PYTHON%" "%~dp0app.py" %*
