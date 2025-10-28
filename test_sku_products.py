"""
Script para verificar productos y sus SKUs
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.product_model import ProductModel

def test_products():
    model = ProductModel()
    
    print("\n=== TEST: Obtener todos los productos ===")
    products = model.get_all_products(include_inactive=False)
    
    print(f"\n✅ Total de productos: {len(products)}")
    
    if products:
        print("\n📋 Primeros 5 productos:")
        for i, p in enumerate(products[:5]):
            print(f"\n{i+1}. ID: {p.get('id')}")
            print(f"   SKU: {p.get('sku')}")
            print(f"   Nombre: {p.get('name')}")
            print(f"   Precio: S/ {p.get('price', 0):.2f}")
            print(f"   Stock: {p.get('stock_quantity', 0)}")
            print(f"   Estado: {p.get('status')}")
    else:
        print("\n⚠️ No hay productos")
    
    print("\n=== TEST: Buscar productos ===")
    search_result = model.search_products("a")
    print(f"✅ Productos encontrados: {len(search_result)}")
    
    if search_result:
        print("\n📋 Primeros 3 resultados de búsqueda:")
        for i, p in enumerate(search_result[:3]):
            print(f"\n{i+1}. ID: {p.get('id')}")
            print(f"   SKU: {p.get('sku')}")
            print(f"   Nombre: {p.get('name')}")

if __name__ == "__main__":
    test_products()
