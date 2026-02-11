@echo off
chcp 65001 >nul
title Optimización Base de Datos - Sistema POS

echo.
echo ===============================================================
echo   OPTIMIZACIÓN DE BASE DE DATOS - SISTEMA POS
echo ===============================================================
echo.

:MENU
echo.
echo Selecciona una opción:
echo.
echo   1. Ejecutar diagnóstico completo
echo   2. Aplicar índices optimizados (SQL)
echo   3. Optimizar y analizar tablas
echo   4. Ver estado de conexiones
echo   5. Salir
echo.
set /p OPCION="Opción: "

if "%OPCION%"=="1" goto DIAGNOSTICO
if "%OPCION%"=="2" goto INDICES
if "%OPCION%"=="3" goto OPTIMIZAR
if "%OPCION%"=="4" goto CONEXIONES
if "%OPCION%"=="5" goto SALIR

echo.
echo ❌ Opción inválida
goto MENU

:DIAGNOSTICO
echo.
echo ===============================================================
echo   EJECUTANDO DIAGNÓSTICO COMPLETO
echo ===============================================================
echo.
python database\diagnose_db.py
pause
goto MENU

:INDICES
echo.
echo ===============================================================
echo   APLICANDO ÍNDICES OPTIMIZADOS
echo ===============================================================
echo.
echo Este proceso creará índices en la base de datos para mejorar
echo el rendimiento de las consultas de reportes.
echo.
set /p CONFIRMAR="¿Continuar? (s/n): "
if /i not "%CONFIRMAR%"=="s" goto MENU

echo.
echo Ejecutando script SQL...
mysql -u root -p pos_system < database\optimize_indexes.sql

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Índices aplicados exitosamente
) else (
    echo.
    echo ❌ Error aplicando índices
)
pause
goto MENU

:OPTIMIZAR
echo.
echo ===============================================================
echo   OPTIMIZACIÓN Y ANÁLISIS DE TABLAS
echo ===============================================================
echo.
python -c "from database.diagnose_db import optimize_tables; optimize_tables()"
pause
goto MENU

:CONEXIONES
echo.
echo ===============================================================
echo   ESTADO DE CONEXIONES MYSQL
echo ===============================================================
echo.
echo Procesos activos:
mysql -u root -p -e "SHOW PROCESSLIST;" pos_system
echo.
echo Variables de conexión:
mysql -u root -p -e "SHOW VARIABLES LIKE '%connection%';" pos_system
pause
goto MENU

:SALIR
echo.
echo ✅ Saliendo...
echo.
exit /b 0
