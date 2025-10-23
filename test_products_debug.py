"""
Script de diagnóstico para problemas con visualización de productos
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.product_model import ProductModel
from database.connection import DatabaseConnection
import traceback

def test_database_connection():
    """Probar conexión a la base de datos"""
    print("\n" + "="*60)
    print("1. PROBANDO CONEXIÓN A BASE DE DATOS")
    print("="*60)
    
    try:
        db = DatabaseConnection()
        if db.connect():
            print("✅ Conexión exitosa a la base de datos")
            print(f"   - Host: {db.config.get('host')}")
            print(f"   - Database: {db.config.get('database')}")
            print(f"   - User: {db.config.get('username')}")
            return True
        else:
            print("❌ No se pudo conectar a la base de datos")
            return False
    except Exception as e:
        print(f"❌ Error al conectar: {e}")
        traceback.print_exc()
        return False

def test_table_structure():
    """Verificar estructura de la tabla products"""
    print("\n" + "="*60)
    print("2. VERIFICANDO ESTRUCTURA DE TABLA 'products'")
    print("="*60)
    
    try:
        db = DatabaseConnection()
        if not db.connect():
            print("❌ No se pudo conectar a la base de datos")
            return False
        
        cursor = db.connection.cursor(dictionary=True)
        
        # Verificar si la tabla existe
        cursor.execute("SHOW TABLES LIKE 'products'")
        result = cursor.fetchone()
        
        if not result:
            print("❌ La tabla 'products' NO EXISTE")
            cursor.close()
            return False
        
        print("✅ La tabla 'products' existe")
        
        # Obtener estructura de la tabla
        cursor.execute("DESCRIBE products")
        columns = cursor.fetchall()
        
        print("\n📋 Columnas de la tabla 'products':")
        for col in columns:
            print(f"   - {col['Field']}: {col['Type']} {'NULL' if col['Null'] == 'YES' else 'NOT NULL'}")
        
        cursor.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar estructura: {e}")
        traceback.print_exc()
        return False

def test_products_count():
    """Contar productos en la base de datos"""
    print("\n" + "="*60)
    print("3. CONTANDO PRODUCTOS EN LA BASE DE DATOS")
    print("="*60)
    
    try:
        db = DatabaseConnection()
        if not db.connect():
            print("❌ No se pudo conectar a la base de datos")
            return
        
        cursor = db.connection.cursor(dictionary=True)
        
        # Contar todos los productos
        cursor.execute("SELECT COUNT(*) as total FROM products")
        result = cursor.fetchone()
        total = result['total']
        
        print(f"📊 Total de productos: {total}")
        
        # Contar por estado
        cursor.execute("SELECT status, COUNT(*) as count FROM products GROUP BY status")
        by_status = cursor.fetchall()
        
        print("\n📊 Productos por estado:")
        for row in by_status:
            print(f"   - {row['status']}: {row['count']}")
        
        cursor.close()
        
        if total == 0:
            print("\n⚠️  NO HAY PRODUCTOS EN LA BASE DE DATOS")
            print("   Esto explica por qué no ves productos en la lista.")
        
    except Exception as e:
        print(f"❌ Error al contar productos: {e}")
        traceback.print_exc()

def test_get_all_products():
    """Probar el método get_all_products del modelo"""
    print("\n" + "="*60)
    print("4. PROBANDO ProductModel.get_all_products()")
    print("="*60)
    
    try:
        product_model = ProductModel()
        
        print("\n🔍 Intentando obtener productos...")
        products = product_model.get_all_products(include_inactive=False)
        
        print(f"✅ Método ejecutado. Productos obtenidos: {len(products)}")
        
        if len(products) == 0:
            print("\n⚠️  EL MÉTODO RETORNA 0 PRODUCTOS")
            print("   Posibles causas:")
            print("   1. No hay productos en la tabla")
            print("   2. Todos los productos están con status='inactive'")
            print("   3. Error en las JOIN con tables/units")
            
            # Probar sin filtros
            print("\n🔍 Probando con productos inactivos incluidos...")
            products_all = product_model.get_all_products(include_inactive=True)
            print(f"   Productos totales: {len(products_all)}")
        else:
            print(f"\n✅ Se encontraron {len(products)} productos activos")
            print("\n📋 Primeros 3 productos:")
            for i, product in enumerate(products[:3], 1):
                print(f"\n   Producto {i}:")
                print(f"   - ID: {product.get('id')}")
                print(f"   - SKU: {product.get('sku')}")
                print(f"   - Nombre: {product.get('name')}")
                print(f"   - Categoría: {product.get('category_name', 'N/A')}")
                print(f"   - Stock: {product.get('stock_quantity')}")
                print(f"   - Precio: ${product.get('price')}")
                print(f"   - Estado: {product.get('status')}")
        
        return products
        
    except Exception as e:
        print(f"❌ Error al obtener productos: {e}")
        traceback.print_exc()
        return []

def test_categories_and_units():
    """Verificar tablas relacionadas"""
    print("\n" + "="*60)
    print("5. VERIFICANDO TABLAS RELACIONADAS")
    print("="*60)
    
    try:
        db = DatabaseConnection()
        if not db.connect():
            print("❌ No se pudo conectar a la base de datos")
            return
        
        cursor = db.connection.cursor(dictionary=True)
        
        # Verificar tabla categories
        cursor.execute("SHOW TABLES LIKE 'categories'")
        if cursor.fetchone():
            print("✅ Tabla 'categories' existe")
            cursor.execute("SELECT COUNT(*) as total FROM categories")
            result = cursor.fetchone()
            print(f"   - Total categorías: {result['total']}")
        else:
            print("❌ Tabla 'categories' NO existe")
        
        # Verificar tabla units
        cursor.execute("SHOW TABLES LIKE 'units'")
        if cursor.fetchone():
            print("✅ Tabla 'units' existe")
            cursor.execute("SELECT COUNT(*) as total FROM units")
            result = cursor.fetchone()
            print(f"   - Total unidades: {result['total']}")
        else:
            print("⚠️  Tabla 'units' NO existe (puede ser opcional)")
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Error al verificar tablas relacionadas: {e}")
        traceback.print_exc()

def test_direct_query():
    """Ejecutar query directa sin JOINs"""
    print("\n" + "="*60)
    print("6. PROBANDO QUERY DIRECTA (SIN JOINs)")
    print("="*60)
    
    try:
        db = DatabaseConnection()
        if not db.connect():
            print("❌ No se pudo conectar a la base de datos")
            return
        
        cursor = db.connection.cursor(dictionary=True)
        
        # Query simple sin JOINs
        cursor.execute("SELECT * FROM products WHERE status = 'active' LIMIT 5")
        products = cursor.fetchall()
        
        print(f"✅ Query ejecutada. Productos encontrados: {len(products)}")
        
        if len(products) > 0:
            print("\n📋 Productos encontrados:")
            for p in products:
                print(f"   - {p.get('id')}: {p.get('name')} (SKU: {p.get('sku')})")
        else:
            print("\n⚠️  NO SE ENCONTRARON PRODUCTOS ACTIVOS")
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Error en query directa: {e}")
        traceback.print_exc()

def provide_solutions():
    """Proporcionar soluciones basadas en el diagnóstico"""
    print("\n" + "="*60)
    print("7. POSIBLES SOLUCIONES")
    print("="*60)
    
    print("\n💡 Si no hay productos en la base de datos:")
    print("   1. Ejecuta el script: database/scriptDB.txt")
    print("   2. O crea productos manualmente desde la interfaz")
    print("   3. Verifica que los productos tengan status='active'")
    
    print("\n💡 Si la tabla 'units' no existe:")
    print("   1. Ejecuta: database/init_database_compatible.sql")
    print("   2. O modifica las queries para que 'units' sea opcional")
    
    print("\n💡 Si hay productos pero no se ven:")
    print("   1. Verifica permisos del usuario (inventory.view)")
    print("   2. Revisa los logs en: logs/")
    print("   3. Verifica que los productos no estén todos inactivos")

def main():
    """Ejecutar todos los diagnósticos"""
    print("\n" + "="*70)
    print("🔍 DIAGNÓSTICO: PROBLEMA CON VISUALIZACIÓN DE PRODUCTOS")
    print("="*70)
    
    # Ejecutar pruebas
    db_ok = test_database_connection()
    
    if db_ok:
        test_table_structure()
        test_products_count()
        test_categories_and_units()
        test_direct_query()
        products = test_get_all_products()
    
    # Proporcionar soluciones
    provide_solutions()
    
    print("\n" + "="*70)
    print("✅ DIAGNÓSTICO COMPLETADO")
    print("="*70)
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
