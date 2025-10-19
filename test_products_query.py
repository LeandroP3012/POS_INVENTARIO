"""
Script de prueba para verificar productos disponibles
"""

from models.product_model import ProductModel

def test_products():
    print("=" * 60)
    print("VERIFICACIÓN DE PRODUCTOS EN BASE DE DATOS")
    print("=" * 60)
    
    try:
        model = ProductModel()
        
        # Test 1: Obtener todos los productos
        print("\n1. Obtener TODOS los productos:")
        all_products = model.get_all_products(include_inactive=False)
        print(f"   Total productos activos: {len(all_products)}")
        
        if all_products:
            print("\n   Primeros 5 productos:")
            for i, p in enumerate(all_products[:5], 1):
                print(f"   {i}. {p.get('sku')} - {p.get('name')} - Stock: {p.get('stock_quantity')} - Status: {p.get('status')}")
        
        # Test 2: Filtrar solo con stock
        print("\n2. Productos con stock > 0:")
        with_stock = [p for p in all_products if p.get('stock_quantity', 0) > 0]
        print(f"   Total productos con stock: {len(with_stock)}")
        
        if with_stock:
            print("\n   Primeros 5 con stock:")
            for i, p in enumerate(with_stock[:5], 1):
                print(f"   {i}. {p.get('sku')} - {p.get('name')} - Stock: {p.get('stock_quantity')}")
        
        # Test 3: Buscar productos
        print("\n3. Búsqueda de productos (vacío):")
        search_result = model.search_products("")
        print(f"   Resultados con búsqueda vacía: {len(search_result)}")
        
        # Resumen
        print("\n" + "=" * 60)
        print("RESUMEN:")
        print(f"  - Productos totales activos: {len(all_products)}")
        print(f"  - Productos con stock: {len(with_stock)}")
        print(f"  - Productos sin stock: {len(all_products) - len(with_stock)}")
        print("=" * 60)
        
        if len(with_stock) == 0:
            print("\n⚠️  PROBLEMA DETECTADO:")
            print("   No hay productos con stock disponible!")
            print("   Solución: Agrega stock a tus productos en el módulo de inventario")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_products()
