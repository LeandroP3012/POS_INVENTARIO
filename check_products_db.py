"""
Script para verificar productos existentes en la base de datos
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.base_model import BaseModel

def check_products():
    """Verificar productos en la base de datos"""
    print("=" * 80)
    print("VERIFICACIÓN DE PRODUCTOS EN BASE DE DATOS")
    print("=" * 80)
    
    base = BaseModel()
    connection = base.get_connection()
    
    if not connection:
        print("❌ No se pudo conectar a la base de datos")
        return
    
    cursor = connection.cursor(dictionary=True)
    
    # Primero verificar la estructura de la tabla
    print("\n📋 ESTRUCTURA DE LA TABLA 'products':")
    print("=" * 80)
    cursor.execute("DESCRIBE products")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col['Field']:<20} {col['Type']:<20} {col['Null']:<5} {col['Key']:<5} {col['Default'] or 'NULL':<10}")
    
    print("\n")
    
    # Contar todos los productos
    cursor.execute("SELECT COUNT(*) as total FROM products")
    total = cursor.fetchone()['total']
    print(f"📊 Total de productos: {total}")
    
    # Productos con formato PROD-
    query_prod = "SELECT COUNT(*) as total FROM products WHERE sku LIKE 'PROD-%'"
    print(f"\nQuery: {query_prod}")
    cursor.execute(query_prod)
    prod_count = cursor.fetchone()['total']
    print(f"📊 Productos con formato PROD-XXXXXX: {prod_count}")
    
    # Productos con formato P###
    query_p = "SELECT COUNT(*) as total FROM products WHERE sku LIKE 'P%' AND sku NOT LIKE 'PROD-%'"
    cursor.execute(query_p)
    p_count = cursor.fetchone()['total']
    print(f"📊 Productos con formato P###: {p_count}")
    
    # Mostrar los primeros 10 productos
    print("\n" + "=" * 80)
    print("PRIMEROS 10 PRODUCTOS")
    print("=" * 80)
    
    cursor.execute("""
        SELECT id, sku, name, barcode 
        FROM products 
        ORDER BY id DESC 
        LIMIT 10
    """)
    
    products = cursor.fetchall()
    
    if products:
        print(f"\n{'ID':<5} {'SKU':<15} {'Nombre':<30} {'Código de Barras':<15}")
        print("-" * 80)
        for p in products:
            print(f"{p['id']:<5} {p['sku']:<15} {p['name'][:30]:<30} {p['barcode'] or 'N/A':<15}")
    else:
        print("\n❌ No hay productos en la base de datos")
    
    # Último código PROD-
    print("\n" + "=" * 80)
    print("ÚLTIMO CÓDIGO PROD-XXXXXX")
    print("=" * 80)
    
    query = """
        SELECT sku
        FROM products 
        WHERE sku LIKE 'PROD-%'
          AND LENGTH(sku) = 11
          AND SUBSTRING(sku, 6) REGEXP '^[0-9]+$'
        ORDER BY CAST(SUBSTRING(sku, 6) AS UNSIGNED) DESC 
        LIMIT 1
    """
    
    print(f"\n🔍 Query SQL:")
    print(query)
    
    cursor.execute(query)
    result = cursor.fetchone()
    
    if result:
        last_code = result['sku']
        parts = last_code.split('-')
        number = parts[1] if len(parts) == 2 else 'ERROR'
        print(f"\n✅ Último código encontrado: {last_code}")
        print(f"   Número extraído: {number}")
        print(f"   Siguiente sería: PROD-{int(number)+1:06d}")
    else:
        print("\n⚠️ No se encontraron códigos con formato PROD-XXXXXX")
        print("   El primer código será: PROD-000001")
    
    cursor.close()
    connection.close()

if __name__ == "__main__":
    try:
        check_products()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
