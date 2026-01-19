"""
Script de verificación pre-instalador
Verifica que todos los archivos y dependencias estén listos
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Imprimir encabezado"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_python_version():
    """Verificar versión de Python"""
    print("\n🐍 Verificando Python...")
    version = sys.version_info
    
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (se requiere 3.8+)")
        return False

def check_dependencies():
    """Verificar dependencias instaladas"""
    print("\n📦 Verificando dependencias...")
    
    required = {
        'mysql.connector': 'mysql-connector-python',
        'PIL': 'Pillow',
        'openpyxl': 'openpyxl',
        'reportlab': 'reportlab',
        'PyInstaller': 'pyinstaller'
    }
    
    missing = []
    
    for module, package in required.items():
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (faltante)")
            missing.append(package)
    
    return missing

def check_required_files():
    """Verificar archivos necesarios"""
    print("\n📄 Verificando archivos necesarios...")
    
    required_files = [
        'main.py',
        'requirements.txt',
        'README.md',
        'build_installer.py',
        'installer_script.iss'
    ]
    
    required_dirs = [
        'assets',
        'config',
        'controllers',
        'models',
        'views',
        'database'
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (faltante)")
            missing_files.append(file)
    
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            print(f"   ✅ {dir_name}/")
        else:
            print(f"   ❌ {dir_name}/ (faltante)")
            missing_dirs.append(dir_name)
    
    return missing_files, missing_dirs

def check_database_scripts():
    """Verificar scripts SQL de base de datos"""
    print("\n🗄️  Verificando scripts SQL...")
    
    sql_files = [
        'database/create_tables.sql',
        'database/add_roles_system.sql',
        'database/add_user_sessions_table.sql'
    ]
    
    missing = []
    
    for sql_file in sql_files:
        if os.path.exists(sql_file):
            print(f"   ✅ {sql_file}")
        else:
            print(f"   ⚠️  {sql_file} (opcional)")
            missing.append(sql_file)
    
    return missing

def check_config_files():
    """Verificar archivos de configuración"""
    print("\n⚙️  Verificando configuración...")
    
    config_files = [
        'config/database.json',
        'config/settings.py',
        'config/system_config.json'
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"   ✅ {config_file}")
        else:
            print(f"   ⚠️  {config_file} (se creará plantilla)")
    
    return True

def check_icon():
    """Verificar icono de la aplicación"""
    print("\n🎨 Verificando icono...")
    
    icon_paths = [
        'assets/images/icon.ico',
        'icon.ico'
    ]
    
    for icon_path in icon_paths:
        if os.path.exists(icon_path):
            print(f"   ✅ {icon_path}")
            return True
    
    print(f"   ⚠️  Icono no encontrado (se usará predeterminado)")
    return False

def estimate_size():
    """Estimar tamaño del instalador"""
    print("\n📏 Estimando tamaño...")
    
    total_size = 0
    
    for root, dirs, files in os.walk('.'):
        # Ignorar directorios de build
        dirs[:] = [d for d in dirs if d not in ['build', 'dist', '__pycache__', '.git', 'venv']]
        
        for file in files:
            file_path = os.path.join(root, file)
            try:
                total_size += os.path.getsize(file_path)
            except:
                pass
    
    size_mb = total_size / (1024 * 1024)
    estimated_installer = size_mb * 1.5  # PyInstaller aumenta ~50%
    
    print(f"   📊 Tamaño del proyecto: {size_mb:.1f} MB")
    print(f"   📦 Instalador estimado: {estimated_installer:.1f} MB")
    
    return True

def main():
    """Función principal"""
    print_header("VERIFICACIÓN PRE-INSTALADOR")
    
    all_ok = True
    
    # Verificar Python
    if not check_python_version():
        all_ok = False
    
    # Verificar dependencias
    missing_deps = check_dependencies()
    if missing_deps:
        all_ok = False
        print("\n   📝 Para instalar dependencias faltantes:")
        print(f"      pip install {' '.join(missing_deps)}")
    
    # Verificar archivos
    missing_files, missing_dirs = check_required_files()
    if missing_files or missing_dirs:
        all_ok = False
    
    # Verificar SQL
    check_database_scripts()
    
    # Verificar configuración
    check_config_files()
    
    # Verificar icono
    check_icon()
    
    # Estimar tamaño
    estimate_size()
    
    # Resumen final
    print_header("RESUMEN")
    
    if all_ok:
        print("\n✅ SISTEMA LISTO PARA CREAR INSTALADOR")
        print("\n📝 Próximos pasos:")
        print("   1. Ejecutar: python build_installer.py")
        print("   2. O ejecutar: crear_instalador.bat")
        print("   3. Compilar con Inno Setup: installer_script.iss")
    else:
        print("\n⚠️  SE ENCONTRARON ALGUNOS PROBLEMAS")
        print("\n📝 Solucione los problemas marcados con ❌ antes de continuar")
        
        if missing_deps:
            print("\n   Instalar dependencias:")
            print(f"   pip install {' '.join(missing_deps)}")
    
    print("\n" + "=" * 60)
    
    return all_ok

if __name__ == '__main__':
    try:
        success = main()
        input("\n\nPresione ENTER para salir...")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Verificación cancelada")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        input("\n\nPresione ENTER para salir...")
        sys.exit(1)
