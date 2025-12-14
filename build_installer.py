"""
Script para construir el instalador del Sistema POS.
Prepara recursos, compila con PyInstaller y organiza los archivos resultantes
para facilitar la creacion del instalador y su despliegue en otras maquinas.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict

APP_NAME = "POS_Sistema"
PROJECT_ROOT = Path(__file__).parent.resolve()
DIST_ROOT = PROJECT_ROOT / "dist"
DIST_DIR = DIST_ROOT / APP_NAME
BUILD_DIR = PROJECT_ROOT / "build"
TEMP_DIR = PROJECT_ROOT / "build_temp"
RUNTIME_ASSETS_DIR = TEMP_DIR / "runtime_assets"
CONFIG_TEMPLATES_DIR = RUNTIME_ASSETS_DIR / "config_templates"
VERSION_FILE = PROJECT_ROOT / "version_file.txt"
ASSETS_DIR = PROJECT_ROOT / "assets"
ICON_PATH = ASSETS_DIR / "images" / "icon.ico"
SQL_SOURCE_DIR = PROJECT_ROOT / "database"
DATA_SEPARATOR = ";" if os.name == "nt" else ":"

REQUIRED_MODULES: Dict[str, str] = {
    "mysql.connector": "mysql-connector-python",
    "openpyxl": "openpyxl",
    "tkcalendar": "tkcalendar",
    "matplotlib": "matplotlib",
    "PIL": "Pillow",
}

CONFIG_TEMPLATE_DEFAULTS: Dict[str, Dict] = {
    "database.json": {
        "host": "localhost",
        "port": "3306",
        "name": "pos_system",
        "user": "root",
        "password": "D3v3l0p3r@@$",
        "max_connections": "10",
        "timeout": "30",
    },
    "system_config.json": {
        "company_name": "Sistema POS",
        "company_rut": "",
        "company_address": "",
        "company_phone": "",
        "company_email": "",
        "company_website": "",
        "logo_path": "",
        "currency": "PEN",
        "currency_symbol": "S/.",
        "tax_rate": "18",
        "language": "Español",
        "theme": "Claro",
        "auto_print": True,
        "printer": "",
        "copies": "1",
        "paper_size": "A4",
        "print_logo": True,
        "print_company_info": True,
        "print_customer_info": False,
        "print_barcode": False,
        "print_quality": "Normal",
        "save_pdf_copy": False,
        "session_timeout": "480",
        "auto_logout": True,
        "auto_backup": True,
        "backup_frequency": "Diario",
        "backup_path": "./backups",
        "auto_save": True,
        "include_tax": True,
        "tax_id": "",
        "min_password_length": "6",
        "require_special_chars": False,
        "show_animations": True,
        "sound_notifications": True,
    },
    "ticket_config.json": {
        "printer_name": "",
        "paper_width": 80,
        "print_logo": False,
        "logo_path": "",
        "header_text": "TICKET DE VENTA",
        "footer_text": "¡Gracias por su compra!",
        "show_barcode": False,
    },
}

CONFIG_INSTRUCTIONS = """
CONFIGURACION DEL SISTEMA POS
=============================

Los archivos editables se guardan en:
    %APPDATA%\\SistemaPOS\\config

Pasos recomendados:
1. Importe los scripts SQL que estan en database_scripts.
2. Ejecute POS_Sistema.exe una vez para generar los archivos config.
3. Edite los archivos generados en %APPDATA%\\SistemaPOS\\config segun su entorno:
   - database.json: parametros de MySQL.
   - system_config.json: datos de la empresa y preferencias.
   - ticket_config.json: opciones de impresion.

Si prefiere configurarlos antes, copie el contenido de config_templates hacia la
ruta anterior y edite los valores antes del primer inicio.
""".strip()


def _remove_path(path: Path, attempts: int = 3, delay: float = 0.75) -> None:
    """Eliminar archivos o carpetas con reintentos para manejos de bloqueo en Windows."""
    if not path.exists():
        return

    for attempt in range(1, attempts + 1):
        try:
            if path.is_file() or path.is_symlink():
                path.unlink()
            else:
                shutil.rmtree(path)
            return
        except PermissionError as error:
            if attempt == attempts:
                raise RuntimeError(
                    f"No se pudo eliminar {path} porque está siendo usado por otro proceso. "
                    "Cierra ventanas del Explorador, terminales o programas que estén usando "
                    "este directorio y vuelve a ejecutar el script."
                ) from error

            print(
                f"   ⚠️  {path.name} está en uso (intento {attempt}/{attempts}). "
                "Reintentando en breve..."
            )
            time.sleep(delay)


def module_available(module_name: str) -> bool:
    """Verificar si un modulo esta disponible sin importarlo."""
    try:
        return importlib.util.find_spec(module_name) is not None
    except (ImportError, AttributeError, ValueError):
        return False


def ensure_project_root() -> None:
    """Validar que el script se ejecute desde la raiz del proyecto."""
    if not (PROJECT_ROOT / "main.py").exists():
        raise FileNotFoundError(
            "main.py no encontrado. Ejecuta build_installer.py desde la raiz del proyecto."
        )


def ensure_pyinstaller() -> None:
    """Verificar PyInstaller e instalarlo si es necesario."""
    try:
        subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--version"],
            capture_output=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n⚠️  PyInstaller no está instalado. Instalando...\n")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)


def check_required_modules() -> None:
    """Validar que todas las dependencias obligatorias esten presentes."""
    missing = []
    for module_name, pip_name in REQUIRED_MODULES.items():
        if not module_available(module_name):
            missing.append(f"- {module_name} (pip install {pip_name})")
    if missing:
        message = "\n❌ Faltan dependencias obligatorias:\n   " + "\n   ".join(missing)
        raise RuntimeError(message)


def clean_build_dirs() -> None:
    """Eliminar directorios temporales y artefactos previos."""
    print("🧹 Limpiando artefactos anteriores...")

    for path in (BUILD_DIR, DIST_ROOT, TEMP_DIR):
        if path.exists():
            _remove_path(path)
            print(f"   ✓ {path.name} eliminado")

    root_pycache = PROJECT_ROOT / "__pycache__"
    if root_pycache.exists():
        _remove_path(root_pycache)
        print("   ✓ __pycache__ eliminado")

    for spec_file in PROJECT_ROOT.glob("*.spec"):
        spec_file.unlink()
        print(f"   ✓ {spec_file.name} eliminado")


def create_version_file() -> None:
    """Generar el archivo de version para incrustar en el ejecutable."""
    print("📝 Creando archivo de version...")
    version_content = """
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Tu Empresa'),
        StringStruct(u'FileDescription', u'Sistema POS - Punto de Venta'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'POS Sistema'),
        StringStruct(u'LegalCopyright', u'Copyright  2025'),
        StringStruct(u'OriginalFilename', u'POS.exe'),
        StringStruct(u'ProductName', u'Sistema POS'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    VERSION_FILE.write_text(version_content, encoding="utf-8")
    print(f"   ✓ {VERSION_FILE.name} creado")


def prepare_runtime_assets() -> Dict[str, object]:
    """Crear plantillas y recursos que deben incluirse en el ejecutable."""
    print("📦 Preparando plantillas de configuracion...")

    if RUNTIME_ASSETS_DIR.exists():
        shutil.rmtree(RUNTIME_ASSETS_DIR)

    CONFIG_TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

    config_defaults = copy.deepcopy(CONFIG_TEMPLATE_DEFAULTS)
    for file_name, content in config_defaults.items():
        target = CONFIG_TEMPLATES_DIR / file_name
        with target.open("w", encoding="utf-8") as handle:
            json.dump(content, handle, indent=4, ensure_ascii=False)
        print(f"   ✓ Plantilla generada: {file_name}")

    return {
        "config_templates": CONFIG_TEMPLATES_DIR,
        "config_defaults": config_defaults,
    }


def build_executable(runtime_assets: Dict[str, object]) -> bool:
    """Ejecutar PyInstaller con los parametros necesarios."""
    print("\n🔨 Compilando aplicacion con PyInstaller...")

    pyinstaller_cmd = [
        str(sys.executable),
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        f"--name={APP_NAME}",
        "--onedir",
        "--windowed",
        f"--version-file={VERSION_FILE}",
        f"--paths={PROJECT_ROOT}",
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=mysql.connector",
        "--collect-all=mysql.connector",
        "--collect-all=openpyxl",
        "--collect-all=tkcalendar",
        "--collect-submodules=matplotlib",
        "--collect-data=matplotlib",
        "--hidden-import=matplotlib.backends.backend_tkagg",
    ]

    if ICON_PATH.exists():
        pyinstaller_cmd.append(f"--icon={ICON_PATH}")
    else:
        print(f"   ⚠️  Icono no encontrado en {ICON_PATH}, se usará el icono por defecto")

    if ASSETS_DIR.exists():
        pyinstaller_cmd.append(f"--add-data={ASSETS_DIR}{DATA_SEPARATOR}assets")
    else:
        print("   ⚠️  Carpeta assets no encontrada, se omitirá del paquete")

    templates_path = runtime_assets["config_templates"]
    pyinstaller_cmd.append(
        f"--add-data={templates_path}{DATA_SEPARATOR}config_templates"
    )

    if module_available("reportlab"):
        pyinstaller_cmd.append("--collect-all=reportlab")
        print("   ✓ reportlab detectado: se incluirán recursos JSON/PDF opcionales")
    else:
        print("   ℹ️  reportlab no encontrado (reportes PDF opcionales)")

    if os.name == "nt":
        if module_available("win32print"):
            for mod in ("pythoncom", "pywintypes", "win32timezone", "win32print", "win32ui"):
                if module_available(mod):
                    pyinstaller_cmd.append(f"--hidden-import={mod}")
            print("   ✓ pywin32 detectado: se habilitará soporte de impresion nativa")
        else:
            print("   ⚠️  No se detecto pywin32. Instala pywin32 para habilitar impresion termica")

    pyinstaller_cmd.append("main.py")

    printable_cmd = " ".join(shlex.quote(str(arg)) for arg in pyinstaller_cmd)
    print("\n📋 Comando PyInstaller:")
    print(f"   {printable_cmd}\n")

    try:
        subprocess.run(pyinstaller_cmd, check=True)
        print("   ✅ Compilacion exitosa")
        return True
    except subprocess.CalledProcessError as error:
        print("   ❌ Error en la compilacion de PyInstaller")
        print(f"      Codigo de salida: {error.returncode}")
        return False


def copy_additional_files(runtime_assets: Dict[str, object]) -> bool:
    """Copiar archivos y directorios necesarios al resultado final."""
    print("\n📋 Copiando archivos adicionales...")

    if not DIST_DIR.exists():
        print("   ❌ Directorio de salida no encontrado. Asegurate de que PyInstaller termino correctamente.")
        return False

    for file_name in ("README.md", "requirements.txt", "installer_script.iss"):
        source = PROJECT_ROOT / file_name
        if source.exists():
            shutil.copy2(source, DIST_DIR / file_name)
            print(f"   ✓ {file_name} copiado")
        else:
            if file_name != "installer_script.iss":
                print(f"   ⚠️  {file_name} no encontrado en el proyecto")

    config_templates_dist = DIST_DIR / "config_templates"
    if config_templates_dist.exists():
        shutil.rmtree(config_templates_dist)
    shutil.copytree(runtime_assets["config_templates"], config_templates_dist)
    print("   ✓ Plantillas copiadas a config_templates/")

    config_dir = DIST_DIR / "config"
    config_dir.mkdir(exist_ok=True)
    for file_name, content in runtime_assets["config_defaults"].items():
        template_name = file_name.replace(".json", "_template.json")
        target = config_dir / template_name
        with target.open("w", encoding="utf-8") as handle:
            json.dump(content, handle, indent=4, ensure_ascii=False)
        print(f"   ✓ Plantilla editable creada: config/{template_name}")

    instructions_path = DIST_DIR / "CONFIGURACION_BD.txt"
    instructions_path.write_text(CONFIG_INSTRUCTIONS + "\n", encoding="utf-8")
    print("   ✓ Instrucciones de configuracion generadas")

    for folder_name in ("logs", "backups", "tickets", "reports"):
        folder = DIST_DIR / folder_name
        folder.mkdir(exist_ok=True)
        print(f"   ✓ Directorio creado: {folder_name}/")

    database_scripts_dir = DIST_DIR / "database_scripts"
    database_scripts_dir.mkdir(exist_ok=True)
    if SQL_SOURCE_DIR.exists():
        copied = 0
        for sql_file in sorted(SQL_SOURCE_DIR.glob("*.sql")):
            shutil.copy2(sql_file, database_scripts_dir / sql_file.name)
            copied += 1
        if copied:
            print(f"   ✓ {copied} script(s) SQL copiados a database_scripts/")
        else:
            print("   ⚠️  No se encontraron archivos .sql en database/")
    else:
        print("   ⚠️  Carpeta database/ no encontrada. Revisa la estructura del proyecto")

    return True


def cleanup_runtime_assets() -> None:
    """Eliminar directorios temporales creados para el build."""
    if TEMP_DIR.exists():
        _remove_path(TEMP_DIR)


def cleanup_intermediate_dirs() -> None:
    """Eliminar artefactos intermedios para dejar solo la carpeta dist."""
    if BUILD_DIR.exists():
        _remove_path(BUILD_DIR)
        print("\n🧹 Directorio build eliminado (artefactos intermedios)")

    spec_file = PROJECT_ROOT / f"{APP_NAME}.spec"
    if spec_file.exists():
        _remove_path(spec_file)
        print("   🗑️  Archivo POS_Sistema.spec eliminado")


def print_success_summary() -> None:
    """Mostrar resumen final con los proximos pasos."""
    print("\n" + "=" * 60)
    print("✅ COMPILACION COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    print(f"\n📁 Archivos generados en: {DIST_DIR}")
    print("\nPasos siguientes:")
    print("  1. Revisar el contenido de dist/POS_Sistema.")
    print("  2. Ejecutar Inno Setup con installer_script.iss para crear el instalador.")
    print("  3. Probar el ejecutable en una maquina limpia antes de distribuirlo.")


def main() -> bool:
    print("=" * 60)
    print("  CONSTRUCCION DE INSTALADOR - SISTEMA POS")
    print("=" * 60)

    runtime_assets: Dict[str, object] | None = None

    try:
        ensure_project_root()
        ensure_pyinstaller()
        check_required_modules()
        clean_build_dirs()
        create_version_file()
        runtime_assets = prepare_runtime_assets()

        if not build_executable(runtime_assets):
            return False

        if not copy_additional_files(runtime_assets):
            print("\n⚠️  Advertencia: faltaron archivos al copiar recursos adicionales")

        cleanup_intermediate_dirs()
        print_success_summary()
        return True

    except KeyboardInterrupt:
        print("\n❌ Construccion cancelada por el usuario")
        return False
    except Exception as exc:
        print(f"\n❌ Error inesperado: {exc}")
        return False
    finally:
        cleanup_runtime_assets()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
