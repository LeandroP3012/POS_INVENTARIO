"""
Script para crear las tablas del módulo de productos/inventario
Ejecuta el archivo SQL create_products_tables.sql
"""

import mysql.connector
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database.connection import DatabaseConnection

def run_migration():
    """Ejecutar migración de tablas de productos"""
    print("=" * 60)
    print("🔧 MIGRACIÓN: Crear tablas de Productos/Inventario")
    print("=" * 60)
    
    try:
        # Conectar a la base de datos
        db = DatabaseConnection()
        
        if not db.connect():
            print("❌ Error: No se pudo conectar a la base de datos")
            return False
        
        print("✅ Conexión establecida")
        
        # Leer archivo SQL
        sql_file = os.path.join('database', 'create_products_tables.sql')
        
        if not os.path.exists(sql_file):
            print(f"❌ Error: No se encontró el archivo {sql_file}")
            return False
        
        print(f"📄 Leyendo {sql_file}...")
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Dividir en statements individuales
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        print(f"📋 Ejecutando {len(statements)} statements SQL...")
        
        cursor = db.connection.cursor()
        
        for i, statement in enumerate(statements, 1):
            try:
                # Skip comentarios
                if statement.startswith('--'):
                    continue
                
                cursor.execute(statement)
                print(f"  ✓ Statement {i}/{len(statements)} ejecutado")
                
            except mysql.connector.Error as e:
                # Ignorar errores de tabla ya existente
                if e.errno == 1050:  # Table already exists
                    print(f"  ⚠ Statement {i}: Tabla ya existe, continuando...")
                else:
                    print(f"  ❌ Error en statement {i}: {e}")
                    raise
        
        db.connection.commit()
        cursor.close()
        
        print("\n" + "=" * 60)
        print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print("\nTablas creadas/actualizadas:")
        print("  📁 categories - Categorías de productos")
        print("  📏 units - Unidades de medida")
        print("  📦 products - Productos")
        print("  📊 product_movements - Movimientos de inventario")
        print("\nDatos de ejemplo insertados:")
        print("  • 8 categorías por defecto")
        print("  • 10 unidades de medida")
        print("  • 5 productos de ejemplo")
        print("\n¡El módulo de inventario está listo para usar! 🎉")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR FATAL: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        if db:
            db.disconnect()
            print("\n🔒 Conexión cerrada")

if __name__ == '__main__':
    success = run_migration()
    sys.exit(0 if success else 1)
