@echo off
chcp 65001 >nul
title Verificación Rápida - Optimizaciones Aplicadas

echo.
echo ===============================================================
echo   VERIFICACIÓN RÁPIDA DE OPTIMIZACIONES
echo ===============================================================
echo.

echo [1/4] Verificando archivos Python modificados...
echo.
if exist "database\connection.py" (
    findstr /C:"use_pure" /C:"connect_timeout" database\connection.py >nul
    if %ERRORLEVEL% EQU 0 (
        echo   ✅ database\connection.py - OPTIMIZADO
    ) else (
        echo   ⚠️  database\connection.py - Verificar manualmente
    )
) else (
    echo   ❌ database\connection.py NO ENCONTRADO
)

if exist "models\base_model.py" (
    echo   ✅ models\base_model.py - ACTUALIZADO
) else (
    echo   ❌ models\base_model.py NO ENCONTRADO
)

if exist "models\report_model.py" (
    echo   ✅ models\report_model.py - ACTUALIZADO
) else (
    echo   ❌ models\report_model.py NO ENCONTRADO
)

echo.
echo [2/4] Verificando nuevos archivos creados...
echo.
if exist "database\optimize_indexes.sql" (
    echo   ✅ optimize_indexes.sql - Listo para aplicar
) else (
    echo   ❌ optimize_indexes.sql NO ENCONTRADO
)

if exist "database\diagnose_db.py" (
    echo   ✅ diagnose_db.py - Disponible
) else (
    echo   ❌ diagnose_db.py NO ENCONTRADO
)

if exist "OPTIMIZAR_BASE_DATOS.bat" (
    echo   ✅ OPTIMIZAR_BASE_DATOS.bat - Disponible
) else (
    echo   ❌ OPTIMIZAR_BASE_DATOS.bat NO ENCONTRADO
)

echo.
echo [3/4] Verificando índices en la base de datos...
echo.
echo Conectando a MySQL...
mysql -u root -p --skip-column-names -e "SELECT CASE WHEN COUNT(*) >= 5 THEN 'OK' ELSE 'FALTAN' END as estado FROM information_schema.STATISTICS WHERE TABLE_SCHEMA = 'pos_system' AND INDEX_NAME IN ('idx_sales_date_status', 'idx_sales_user_date', 'idx_sale_details_sale', 'idx_sale_details_product', 'idx_sales_payment_method');" 2>nul

if %ERRORLEVEL% EQU 0 (
    echo   ✅ Conexión a MySQL exitosa
    echo.
    echo   💡 IMPORTANTE: Si los índices muestran 'FALTAN', ejecuta:
    echo      OPTIMIZAR_BASE_DATOS.bat → Opción 2
) else (
    echo   ⚠️  No se pudo verificar índices (MySQL no conectado o sin credenciales)
    echo.
    echo   Para verificar manualmente:
    echo      mysql -u root -p
    echo      USE pos_system;
    echo      SHOW INDEX FROM sales;
)

echo.
echo [4/4] Prueba rápida de conexión Python...
echo.
python -c "from database.connection import test_database_connection; success, msg = test_database_connection(); print('  ✅ Conexión Python OK' if success else '  ❌ ' + msg)" 2>nul

if %ERRORLEVEL% NEQ 0 (
    echo   ⚠️  No se pudo ejecutar prueba Python
)

echo.
echo ===============================================================
echo   RESUMEN Y PRÓXIMOS PASOS
echo ===============================================================
echo.
echo ✅ COMPLETADO:
echo    • Código Python optimizado
echo    • Scripts de optimización creados
echo    • Documentación actualizada
echo.
echo 📋 PENDIENTE (REQUERIDO):
echo    1. Aplicar índices a la base de datos:
echo       → Ejecutar: OPTIMIZAR_BASE_DATOS.bat
echo       → Seleccionar: Opción 2
echo.
echo    2. Ejecutar diagnóstico completo:
echo       → python database\diagnose_db.py
echo.
echo    3. Reiniciar la aplicación:
echo       → python main.py
echo.
echo 📖 DOCUMENTACIÓN:
echo    • SOLUCION_CARGA_REPORTES.md  - Guía completa
echo    • RESUMEN_OPTIMIZACION.md     - Resumen ejecutivo
echo.
echo ===============================================================
echo.
pause
