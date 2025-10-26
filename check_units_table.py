"""
Verificar estructura de la tabla units
"""
import mysql.connector
import json

with open('config/database.json', 'r') as f:
    db_config = json.load(f)

connection = mysql.connector.connect(
    host=db_config['host'],
    port=int(db_config['port']),
    database=db_config['name'],
    user=db_config['user'],
    password=db_config['password']
)

cursor = connection.cursor()

print("=" * 70)
print("📋 ESTRUCTURA DE LA TABLA 'units'")
print("=" * 70)

try:
    cursor.execute("DESCRIBE units")
    columns = cursor.fetchall()
    
    print(f"\n📊 Columnas encontradas ({len(columns)} columnas):\n")
    for col in columns:
        print(f"   - {col[0]:20} | Tipo: {col[1]:25} | Null: {col[2]} | Key: {col[3]}")
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 La tabla 'units' probablemente NO existe")

cursor.close()
connection.close()
print("\n✅ Consulta completada")
