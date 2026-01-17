@echo off
REM Script para aplicar la corrección de IGV en reportes
REM Fecha: 2026-01-10

echo ================================================================
echo APLICAR CORRECCION DE IGV EN REPORTES
echo ================================================================
echo.
echo Este script agregara el campo 'include_tax' a la tabla 'sales'
echo para registrar si cada venta incluye IGV o no.
echo.
echo IMPORTANTE: Necesitas tener MySQL instalado y corriendo.
echo.
pause

echo.
echo Ingresa la contraseña de MySQL cuando se solicite...
echo.

mysql -u root -p pos_system < database\add_include_tax_field.sql

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================
    echo CORRECCION APLICADA EXITOSAMENTE
    echo ================================================================
    echo.
    echo Ahora ejecuta el script de verificacion:
    echo python verificar_correccion_igv.py
    echo.
) else (
    echo.
    echo ================================================================
    echo ERROR AL APLICAR LA CORRECCION
    echo ================================================================
    echo.
    echo Posibles causas:
    echo 1. MySQL no esta corriendo
    echo 2. La contraseña es incorrecta
    echo 3. La base de datos 'pos_system' no existe
    echo.
)

pause
