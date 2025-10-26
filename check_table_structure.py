"""
Verificar estructura de la tabla products
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

print("=" * 60)
print("📋 ESTRUCTURA DE LA TABLA 'products'")
print("=" * 60)

# Describir tabla
cursor.execute("DESCRIBE products")
columns = cursor.fetchall()

print("\n📊 Columnas encontradas:\n")
for col in columns:
    print(f"   - {col[0]:20} | Tipo: {col[1]:20} | Null: {col[2]} | Key: {col[3]}")

print("\n" + "=" * 60)
print("📋 ESTRUCTURA DE LA TABLA 'users'")
print("=" * 60)

cursor.execute("DESCRIBE users")
columns = cursor.fetchall()

print("\n📊 Columnas encontradas:\n")
for col in columns:
    print(f"   - {col[0]:20} | Tipo: {col[1]:20} | Null: {col[2]} | Key: {col[3]}")

cursor.close()
connection.close()
print("\n✅ Consulta completada")
