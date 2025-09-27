@echo off
echo =============================
echo   SISTEMA POS - LOGIN
echo =============================
echo.

cd /d "%~dp0"

echo Iniciando sistema de login...
echo.
echo Usuarios disponibles:
echo   admin / 123 (Administrador)
echo   usuario1 / 123 (Usuario Normal)
echo.

python login_simple.py

if %errorlevel% neq 0 (
    echo.
    echo Error al ejecutar la aplicacion
    pause
)

echo.
echo Sistema cerrado.
pause
