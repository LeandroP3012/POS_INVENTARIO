@echo off
chcp 65001 > nul
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║         GENERADOR DE LICENCIAS - SISTEMA POS                 ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo.

:: Verificar Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no está instalado
    echo Por favor instale Python 3.8 o superior
    pause
    exit /b 1
)

echo 🔑 Ejecutando generador de licencias...
echo.

python generar_licencias.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error al generar licencias
    pause
    exit /b 1
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    PROCESO COMPLETADO                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 📁 Archivos generados:
echo.
echo    📄 licenses_database.json      - Base de datos completa
echo    📊 licenses_list.csv           - Lista en formato Excel
echo    📋 LICENCIAS_MAESTRAS.txt      - Lista maestra (CONFIDENCIAL)
echo    📁 licenses_individual\        - Archivos para distribuir a clientes
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

pause
