"""
Script para recrear las tablas del módulo de productos
ADVERTENCIA: Esto eliminará las tablas existentes y todos sus datos
"""

import mysql.connector
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database.connection import DatabaseConnection

def run_migration():
    """Recrear tablas de productos"""
    print("=" * 70)
    print("⚠️  MIGRACIÓN: Recrear tablas de Productos/Inventario")
    print("=" * 70)
    print("\n⚠️  ADVERTENCIA: Esto eliminará las tablas existentes:\n")
    print("  • categories")
    print("  • units")
    print("  • products")
    print("  • product_movements")
    print("\n¿Estás seguro? (escribe 'SI' para continuar): ", end='')
    
    confirmation = input().strip()
    if confirmation != 'SI':
        print("\n❌ Migración cancelada")
        return False
    
    print("\n" + "=" * 70)
    
    try:
        # Conectar a la base de datos
        db = DatabaseConnection()
        
        if not db.connect():
            print("❌ Error: No se pudo conectar a la base de datos")
            return False
        
        print("✅ Conexión establecida")
        
        cursor = db.connection.cursor()
        
        # Deshabilitar foreign key checks temporalmente
        print("\n🔧 Deshabilitando verificación de claves foráneas...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Eliminar tablas existentes
        print("\n🗑️  Eliminando tablas existentes...")
        tables_to_drop = ['product_movements', 'products', 'units', 'categories']
        
        for table in tables_to_drop:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
                print(f"  ✓ Tabla '{table}' eliminada")
            except Exception as e:
                print(f"  ⚠️  Error eliminando '{table}': {e}")
        
        db.connection.commit()
        
        # Rehabilitar foreign key checks
        print("\n🔧 Habilitando verificación de claves foráneas...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        # Leer archivo SQL
        sql_file = os.path.join('database', 'create_products_tables.sql')
        
        if not os.path.exists(sql_file):
            print(f"❌ Error: No se encontró el archivo {sql_file}")
            return False
        
        print(f"\n📄 Leyendo {sql_file}...")
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Dividir en statements individuales
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        print(f"\n📋 Ejecutando {len(statements)} statements SQL...")
        
        for i, statement in enumerate(statements, 1):
            try:
                # Skip comentarios
                if statement.startswith('--'):
                    continue
                
                cursor.execute(statement)
                
                # Mostrar progreso para statements importantes
                if 'CREATE TABLE' in statement.upper():
                    table_name = statement.split('CREATE TABLE IF NOT EXISTS')[1].split('(')[0].strip()
                    print(f"  ✓ Tabla '{table_name}' creada")
                elif 'INSERT INTO' in statement.upper():
                    table_name = statement.split('INSERT INTO')[1].split('(')[0].strip()
                    if i == len(statements) or 'INSERT INTO' not in statements[i]:
                        # Solo mostrar mensaje al final de cada bloque de INSERTs
                        pass
                else:
                    print(f"  ✓ Statement {i}/{len(statements)} ejecutado")
                
            except mysql.connector.Error as e:
                print(f"  ❌ Error en statement {i}: {e}")
                raise
        
        db.connection.commit()
        cursor.close()
        
        print("\n" + "=" * 70)
        print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 70)
        print("\nTablas creadas:")
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
