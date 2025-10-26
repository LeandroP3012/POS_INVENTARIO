"""
Script rápido para probar conexión a base de datos
"""
import mysql.connector
import json

print("=" * 60)
print("🔍 PRUEBA DE CONEXIÓN A BASE DE DATOS")
print("=" * 60)

# Leer configuración
try:
    with open('config/database.json', 'r') as f:
        db_config = json.load(f)
    print("\n✅ Configuración cargada:")
    print(f"   Host: {db_config['host']}")
    print(f"   Puerto: {db_config['port']}")
    print(f"   Base de datos: {db_config['name']}")
    print(f"   Usuario: {db_config['user']}")
except Exception as e:
    print(f"\n❌ Error cargando configuración: {e}")
    exit(1)

# Intentar conexión
try:
    print("\n🔌 Intentando conectar...")
    connection = mysql.connector.connect(
        host=db_config['host'],
        port=int(db_config['port']),
        database=db_config['name'],
        user=db_config['user'],
        password=db_config['password']
    )
    
    if connection.is_connected():
        print("✅ CONEXIÓN EXITOSA!")
        
        # Información del servidor
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"\n📊 MySQL Versión: {version[0]}")
        
        # Probar consulta de productos
        print("\n🔍 Probando consulta de productos...")
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]
        print(f"   ✅ Total de productos: {count}")
        
        if count > 0:
            cursor.execute("SELECT id, name, stock_quantity FROM products LIMIT 5")
            products = cursor.fetchall()
            print("\n📦 Primeros 5 productos:")
            for p in products:
                print(f"   - ID: {p[0]}, Nombre: {p[1]}, Stock: {p[2]}")
        
        # Probar usuarios
        print("\n👥 Probando consulta de usuarios...")
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"   ✅ Total de usuarios: {user_count}")
        
        cursor.close()
        connection.close()
        print("\n✅ Conexión cerrada correctamente")
        print("=" * 60)
        
except mysql.connector.Error as e:
    print(f"\n❌ ERROR DE CONEXIÓN:")
    print(f"   Código de error: {e.errno}")
    print(f"   Mensaje: {e.msg}")
    print("\n💡 Posibles causas:")
    print("   1. MySQL no está corriendo")
    print("   2. Credenciales incorrectas")
    print("   3. Base de datos 'pos_system' no existe")
    print("   4. Firewall bloqueando conexión")
    print("=" * 60)
except Exception as e:
    print(f"\n❌ ERROR INESPERADO: {e}")
    print("=" * 60)
