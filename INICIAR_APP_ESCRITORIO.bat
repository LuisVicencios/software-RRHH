@echo off
title TalentHub HR - Software de Escritorio
chcp 65001 > nul
cd /d "%~dp0\cli_python"
python gui_app.py
if errorlevel 1 (
    echo.
    echo Ocurrio un error al iniciar la aplicacion de escritorio.
    echo Intentando abrir la version en consola...
    python main.py
    pause
)
