@echo off
chcp 65001 > nul
cls
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║         COMPILAR SISTEMA POS CON ICONO                       ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Verificar que existe el icono
if not exist "assets\images\icon.ico" (
    echo ❌ ERROR: No se encontró el archivo de icono
    echo    Ruta esperada: assets\images\icon.ico
    echo.
    echo 💡 Solución:
    echo    1. Coloca tu archivo .ico en: assets\images\icon.ico
    echo    2. O convierte una imagen a .ico en: https://convertio.co/es/png-ico/
    echo.
    pause
    exit /b 1
)

echo ✅ Icono encontrado: assets\images\icon.ico
echo.

:: Verificar Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no está instalado
    pause
    exit /b 1
)

echo 🔨 Iniciando compilación con PyInstaller...
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

:: Ejecutar build_installer.py
python build_installer.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error en la compilación
    pause
    exit /b 1
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                  ✅ COMPILACIÓN EXITOSA                      ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 📁 Ejecutable generado en: dist\POS_Sistema\POS_Sistema.exe
echo 🎨 Icono aplicado correctamente
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 📝 PRÓXIMOS PASOS:
echo.
echo    1. Revisar el ejecutable en: dist\POS_Sistema\
echo    2. Compilar instalador con Inno Setup (installer_script.iss)
echo    3. El instalador también tendrá el icono configurado
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

pause
