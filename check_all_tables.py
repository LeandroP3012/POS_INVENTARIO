"""
Verificar estructura de todas las tablas relevantes
"""
import mysql.connector
import json

# Leer configuración
with open('config/database.json', 'r') as f:
    db_config = json.load(f)

# Conectar
connection = mysql.connector.connect(
    host=db_config['host'],
    port=int(db_config['port']),
    database=db_config['name'],
    user=db_config['user'],
    password=db_config['password']
)

cursor = connection.cursor()

# Lista de tablas a verificar
tables = ['products', 'categories', 'units', 'product_units']

for table_name in tables:
    print("=" * 70)
    print(f"📋 ESTRUCTURA DE LA TABLA '{table_name}'")
    print("=" * 70)
    
    try:
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        
        print(f"\n📊 Columnas encontradas ({len(columns)} columnas):\n")
        for col in columns:
            null_str = "SI" if col[2] == "YES" else "NO"
            key_str = col[3] if col[3] else "-"
            print(f"   {col[0]:25} | {col[1]:30} | Null: {null_str:3} | Key: {key_str}")
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}\n")

cursor.close()
connection.close()
print("✅ Consulta completada")
