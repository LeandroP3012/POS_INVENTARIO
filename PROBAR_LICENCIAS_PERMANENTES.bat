@echo off
chcp 65001 > nul
cls
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║      PRUEBA: GENERACIÓN DE LICENCIAS PERMANENTES             ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🧪 Esta prueba generará 5 licencias PERMANENTES para verificar
echo    que el sistema funciona correctamente.
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

:: Verificar Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no está instalado
    echo Por favor instale Python 3.8 o superior
    pause
    exit /b 1
)

echo 🔑 Generando 5 licencias de prueba PERMANENTES...
echo.

:: Crear archivo temporal con inputs
(
echo 5
echo 1
echo PruebaCliente
echo S
) > temp_input.txt

:: Ejecutar generador con inputs
python generar_licencias.py < temp_input.txt

:: Eliminar archivo temporal
del temp_input.txt > nul 2>&1

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    VERIFICACIÓN                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 📁 Revisa los archivos generados:
echo.
echo    📄 licenses_individual\LICENSE_PruebaCliente0001.txt
echo.

if exist "licenses_individual\LICENSE_PruebaCliente0001.txt" (
    echo ✅ Archivo de prueba encontrado. Mostrando contenido:
    echo ═══════════════════════════════════════════════════════════════
    type "licenses_individual\LICENSE_PruebaCliente0001.txt"
    echo ═══════════════════════════════════════════════════════════════
    echo.
    echo ✅ VERIFICA que la "Fecha de Expiración" sea "PERMANENTE"
    echo ✅ VERIFICA que la "Vigencia" sea "LIFETIME"
) else (
    echo ❌ No se encontró el archivo de prueba
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo.

pause
