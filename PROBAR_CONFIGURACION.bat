@echo off
chcp 65001 > nul
cls
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║     PRUEBA: SISTEMA DE CONFIGURACIÓN EDITABLE                ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🧪 Probando PathManager...
echo.
python -c "from utils.path_manager import _path_manager; _path_manager.print_paths_info(); _path_manager.ensure_config_files()"

echo.
echo ═══════════════════════════════════════════════════════════════
echo.

echo 🧪 Probando carga de configuración...
echo.
python -c "from utils.path_manager import load_config, get_config_path; import json; config = load_config('database.json'); print(f'✅ Configuración cargada desde: {get_config_path(\"database.json\")}'); print(f'📄 Contenido:'); print(json.dumps(config, indent=2, ensure_ascii=False))"

echo.
echo ═══════════════════════════════════════════════════════════════
echo.

echo 🧪 Probando conexión a base de datos...
echo.
python database/connection.py

echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo ✅ PRUEBAS COMPLETADAS
echo.
echo 📝 Notas:
echo    • Los archivos de configuración se crearon en la carpeta correcta
echo    • Puedes editar database.json para configurar MySQL
echo    • La conexión funcionará una vez configurada la BD
echo.
pause
