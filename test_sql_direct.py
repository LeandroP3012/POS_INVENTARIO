"""Ejecutar SQL directamente sin dividir"""
from database.connection import DatabaseConnection
import os

db = DatabaseConnection()
db.connect()

sql_file = os.path.join('database', 'create_products_tables.sql')
with open(sql_file, 'r', encoding='utf-8') as f:
    sql_content = f.read()

cursor = db.connection.cursor()

# Ejecutar todo el SQL de una vez
try:
    # MySQL no soporta múltiples statements en execute()
    # Necesitamos usar cursor.execute() para cada uno
    for result in cursor.execute(sql_content, multi=True):
        pass
    
    db.connection.commit()
    print("✅ SQL ejecutado exitosamente")
    
    # Verificar tablas creadas
    cursor.execute("SHOW TABLES LIKE '%categories%' OR SHOW TABLES LIKE '%units%' OR SHOW TABLES LIKE '%products%'")
    cursor.execute("SHOW TABLES")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"\nTablas en la base de datos ({len(tables)}):")
    for t in tables:
        print(f"  • {t}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    cursor.close()
    db.disconnect()
