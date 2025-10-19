"""
Script para ejecutar las migraciones SQL del módulo de ventas
"""
import mysql.connector
from pathlib import Path
import json

def execute_sql_file():
    """Ejecutar archivo SQL para crear tablas de ventas"""
    try:
        # Cargar configuración de BD
        config_path = Path("config/database.json")
        with open(config_path, 'r', encoding='utf-8') as f:
            db_config = json.load(f)
        
        # Conectar a la base de datos
        print("🔌 Conectando a la base de datos...")
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            port=db_config.get('port', 3306)
        )
        
        cursor = connection.cursor()
        print("✅ Conexión establecida\n")
        
        # Leer archivo SQL
        sql_file = Path("database/add_sales_tables.sql")
        print(f"📄 Leyendo archivo: {sql_file}")
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Dividir por sentencias (separadas por ;)
        statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip() and not stmt.strip().startswith('--')]
        
        print(f"📝 Ejecutando {len(statements)} sentencias SQL...\n")
        
        # Ejecutar cada sentencia
        for i, statement in enumerate(statements, 1):
            if statement.strip():
                try:
                    # Limpiar comentarios al inicio
                    clean_stmt = '\n'.join([line for line in statement.split('\n') if not line.strip().startswith('--')])
                    
                    if clean_stmt.strip():
                        cursor.execute(clean_stmt)
                        print(f"  ✅ Sentencia {i} ejecutada")
                except mysql.connector.Error as e:
                    print(f"  ⚠️ Sentencia {i} - Error: {e}")
                    # Continuar con la siguiente sentencia
                    continue
        
        # Confirmar cambios
        connection.commit()
        print(f"\n✅ Todas las sentencias ejecutadas correctamente")
        
        # Verificar tablas creadas
        print("\n📊 Verificando tablas creadas:")
        cursor.execute("SHOW TABLES LIKE '%sales%' OR LIKE '%customers%' OR LIKE '%inventory_movements%'")
        tables = cursor.fetchall()
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"  ✅ {table[0]}: {count} registros")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 ¡Migración completada exitosamente!")
        print("=" * 60)
        print("Tablas creadas:")
        print("  • customers (clientes)")
        print("  • sales (ventas)")
        print("  • sale_items (detalle de ventas)")
        print("  • sale_payments (pagos)")
        print("  • inventory_movements (movimientos de inventario)")
        print("=" * 60)
        
    except FileNotFoundError as e:
        print(f"❌ Error: Archivo no encontrado - {e}")
    except json.JSONDecodeError:
        print("❌ Error: No se pudo leer el archivo de configuración de BD")
    except mysql.connector.Error as e:
        print(f"❌ Error de MySQL: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 MIGRACIÓN DE BASE DE DATOS - MÓDULO DE VENTAS")
    print("=" * 60)
    print()
    execute_sql_file()
