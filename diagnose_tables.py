"""Script para diagnosticar tablas de productos"""
from database.connection import DatabaseConnection

db = DatabaseConnection()
print("Conectando...")
if db.connect():
    print("✅ Conexión OK\n")
    cursor = db.connection.cursor()
    
    # Listar todas las tablas
    print("=" * 60)
    print("TABLAS EXISTENTES:")
    print("=" * 60)
    cursor.execute("SHOW TABLES")
    tables = [t[0] for t in cursor.fetchall()]
    for table in tables:
        print(f"  • {table}")
    
    # Verificar tablas de productos
    print("\n" + "=" * 60)
    print("VERIFICACIÓN DE TABLAS DE PRODUCTOS:")
    print("=" * 60)
    
    required_tables = ['categories', 'units', 'products', 'product_movements']
    for table in required_tables:
        if table in tables:
            print(f"\n✅ Tabla '{table}' existe")
            cursor.execute(f"DESC {table}")
            columns = cursor.fetchall()
            print(f"   Columnas ({len(columns)}):")
            for col in columns:
                print(f"     - {col[0]} ({col[1]})")
        else:
            print(f"\n❌ Tabla '{table}' NO existe")
    
    cursor.close()
    db.disconnect()
else:
    print("❌ Error de conexión")
