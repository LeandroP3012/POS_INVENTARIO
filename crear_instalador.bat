@echo off
chcp 65001 > nul
echo ========================================
echo   CONSTRUCCIÓN DE INSTALADOR - POS
echo ========================================
echo.

echo 📋 Verificando requisitos...
echo.

:: Verificar Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no está instalado
    echo Por favor instale Python 3.8 o superior
    pause
    exit /b 1
)
echo ✅ Python instalado

:: Verificar PyInstaller
python -c "import PyInstaller" > nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  PyInstaller no encontrado. Instalando...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ❌ Error al instalar PyInstaller
        pause
        exit /b 1
    )
)
echo ✅ PyInstaller instalado

echo.
echo ========================================
echo   Iniciando construcción...
echo ========================================
echo.

:: Ejecutar script de construcción
python build_installer.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error durante la construcción
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Construcción completada
echo ========================================
echo.
echo 📁 Archivos generados en: dist\POS_Sistema\
echo.
echo 📝 Próximos pasos:
echo    1. Verificar que el ejecutable funciona
echo    2. Abrir Inno Setup Compiler
echo    3. Compilar el archivo: installer_script.iss
echo    4. El instalador estará en: Output\POS_Setup.exe
echo.
echo ¿Desea abrir la carpeta dist?
set /p OPEN_DIST="(S/N): "

if /i "%OPEN_DIST%"=="S" (
    explorer dist\POS_Sistema
)

echo.
echo ¿Desea abrir Inno Setup para crear el instalador?
set /p OPEN_INNO="(S/N): "

if /i "%OPEN_INNO%"=="S" (
    if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
        "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_script.iss
    ) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
        "C:\Program Files\Inno Setup 6\ISCC.exe" installer_script.iss
    ) else (
        echo ⚠️  Inno Setup no encontrado en la ruta por defecto
        echo Por favor compile manualmente installer_script.iss
        pause
    )
)

echo.
echo ✅ Proceso completado
pause
