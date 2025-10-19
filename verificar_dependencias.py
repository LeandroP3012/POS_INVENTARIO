#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificación de Dependencias - Sistema POS
Verifica que todas las dependencias estén correctamente instaladas
"""

import sys

def verificar_dependencias():
    """Verifica todas las dependencias del sistema"""
    
    print("=" * 70)
    print("🔍 VERIFICACIÓN DE DEPENDENCIAS - SISTEMA POS")
    print("=" * 70)
    
    # Verificar versión de Python
    version = sys.version_info
    print(f"\n✅ Python {version.major}.{version.minor}.{version.micro} instalado")
    
    if version < (3, 8):
        print("   ⚠️  ADVERTENCIA: Se requiere Python 3.8 o superior")
        print("   ❌ Tu versión es demasiado antigua")
        return False
    elif version >= (3, 8) and version < (3, 13):
        print("   ✅ Versión compatible")
    else:
        print("   ⚠️  Versión muy nueva, puede tener problemas de compatibilidad")
    
    # Dependencias requeridas
    print("\n" + "=" * 70)
    print("📦 DEPENDENCIAS REQUERIDAS:")
    print("=" * 70)
    
    dependencias_requeridas = {
        'mysql.connector': {
            'nombre': 'mysql-connector-python',
            'instalacion': 'pip install mysql-connector-python',
            'version_check': lambda: __import__('mysql.connector').__version__,
        },
        'PIL': {
            'nombre': 'Pillow',
            'instalacion': 'pip install Pillow',
            'version_check': lambda: __import__('PIL').__version__,
        },
        'tkinter': {
            'nombre': 'tkinter (Python estándar)',
            'instalacion': 'Viene con Python - Ver DEPENDENCIAS.md si falla',
            'version_check': lambda: __import__('tkinter').TkVersion,
        },
    }
    
    errores = []
    
    for modulo, info in dependencias_requeridas.items():
        try:
            __import__(modulo)
            try:
                version = info['version_check']()
                print(f"✅ {info['nombre']:<30} (versión: {version})")
            except:
                print(f"✅ {info['nombre']:<30}")
        except ImportError:
            print(f"❌ {info['nombre']:<30} - NO INSTALADO")
            print(f"   Instalar con: {info['instalacion']}")
            errores.append(info['nombre'])
    
    # Librerías estándar de Python
    print("\n" + "=" * 70)
    print("🐍 LIBRERÍAS ESTÁNDAR DE PYTHON:")
    print("=" * 70)
    
    librerias_estandar = {
        'json': 'JSON (manejo de configuraciones)',
        'datetime': 'Fechas y tiempo',
        'logging': 'Sistema de logs',
        'os': 'Sistema operativo',
        'hashlib': 'Hashing (contraseñas)',
        'decimal': 'Aritmética decimal (dinero)',
        'pathlib': 'Rutas de archivos',
        'typing': 'Type hints',
    }
    
    for lib, descripcion in librerias_estandar.items():
        try:
            __import__(lib)
            print(f"✅ {lib:<15} → {descripcion}")
        except ImportError:
            print(f"❌ {lib:<15} → {descripcion}")
            errores.append(lib)
    
    # Verificar conexión a base de datos
    print("\n" + "=" * 70)
    print("🗄️  VERIFICACIÓN DE BASE DE DATOS:")
    print("=" * 70)
    
    try:
        import json
        import os
        
        # Leer configuración de BD
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'database.json')
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                db_config = json.load(f)
            
            print(f"✅ Archivo de configuración encontrado")
            print(f"   Host: {db_config.get('host', 'N/A')}")
            print(f"   Puerto: {db_config.get('port', 'N/A')}")
            print(f"   Base de datos: {db_config.get('database', 'N/A')}")
            
            # Intentar conexión
            try:
                import mysql.connector
                conn = mysql.connector.connect(
                    host=db_config.get('host'),
                    port=db_config.get('port', 3306),
                    user=db_config.get('user'),
                    password=db_config.get('password'),
                    database=db_config.get('database')
                )
                print(f"✅ Conexión a MySQL exitosa")
                
                # Verificar tablas
                cursor = conn.cursor()
                cursor.execute("SHOW TABLES")
                tablas = cursor.fetchall()
                print(f"✅ Base de datos tiene {len(tablas)} tablas")
                
                cursor.close()
                conn.close()
                
            except mysql.connector.Error as e:
                print(f"❌ Error de conexión a MySQL: {e}")
                print(f"   Verifica que MySQL esté ejecutándose")
                print(f"   Verifica usuario y contraseña en config/database.json")
        else:
            print(f"⚠️  Archivo de configuración no encontrado")
            print(f"   Esperado en: {config_path}")
            print(f"   Crea el archivo siguiendo database/README_DATABASE.md")
    
    except Exception as e:
        print(f"⚠️  No se pudo verificar base de datos: {e}")
    
    # Dependencias opcionales
    print("\n" + "=" * 70)
    print("📦 DEPENDENCIAS OPCIONALES:")
    print("=" * 70)
    
    dependencias_opcionales = {
        'barcode': 'python-barcode (códigos de barras)',
        'reportlab': 'reportlab (reportes PDF)',
        'openpyxl': 'openpyxl (exportar Excel)',
        'win32com': 'pywin32 (integración Windows)',
    }
    
    print("Las siguientes son opcionales y no afectan la funcionalidad básica:")
    
    for modulo, nombre in dependencias_opcionales.items():
        try:
            __import__(modulo)
            print(f"✅ {nombre}")
        except ImportError:
            print(f"⚪ {nombre} - No instalado (opcional)")
    
    # Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN:")
    print("=" * 70)
    
    if not errores:
        print("✅ ¡Todas las dependencias requeridas están instaladas!")
        print("✅ El sistema está listo para ejecutarse")
        print("\n💡 Siguiente paso: python main.py")
        return True
    else:
        print(f"❌ Faltan {len(errores)} dependencia(s):")
        for error in errores:
            print(f"   - {error}")
        print("\n💡 Instala las dependencias faltantes con:")
        print("   pip install -r requirements.txt")
        return False
    
    print("=" * 70)


if __name__ == '__main__':
    try:
        exito = verificar_dependencias()
        sys.exit(0 if exito else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Verificación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
