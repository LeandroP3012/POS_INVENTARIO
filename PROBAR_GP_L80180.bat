@echo off
chcp 65001 > nul
echo ================================================================
echo     VERIFICACIÓN DE IMPRESORA GP-L80180 SERIES
echo ================================================================
echo.
echo Este script verificará si tu impresora GP-L80180 está
echo correctamente configurada para el sistema POS.
echo.
echo Presiona cualquier tecla para continuar...
pause > nul
echo.

python test_gp_l80180.py

pause
