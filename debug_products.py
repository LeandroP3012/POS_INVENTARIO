"""
Script para debuggear por qué no aparecen productos
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.product_model import ProductModel
from controllers.sale_controller import SaleController
from controllers.main_controller import MainController

def debug_products():
    print("\n" + "="*60)
    print("🔍 DEBUG: Verificando productos en la base de datos")
    print("="*60)
    
    # Test 1: Verificar productos directamente desde el modelo
    print("\n📋 TEST 1: ProductModel.get_all_products()")
    product_model = ProductModel()
    all_products = product_model.get_all_products(include_inactive=False)
    
    print(f"   Total productos (activos): {len(all_products)}")
    
    if all_products:
        print(f"\n   ✅ Primeros 3 productos encontrados:")
        for i, p in enumerate(all_products[:3]):
            print(f"\n   {i+1}. Producto:")
            print(f"      - ID: {p.get('id')}")
            print(f"      - SKU: {p.get('sku')}")
            print(f"      - Nombre: {p.get('name')}")
            print(f"      - Precio: S/ {p.get('price', 0):.2f}")
            print(f"      - Stock: {p.get('stock_quantity', 0)}")
            print(f"      - Estado: {p.get('status')}")
    else:
        print("\n   ❌ NO HAY PRODUCTOS ACTIVOS")
    
    # Test 2: Verificar con include_inactive=True
    print("\n" + "-"*60)
    print("📋 TEST 2: ProductModel.get_all_products(include_inactive=True)")
    all_products_with_inactive = product_model.get_all_products(include_inactive=True)
    print(f"   Total productos (todos): {len(all_products_with_inactive)}")
    
    if all_products_with_inactive:
        print(f"\n   Estados de productos:")
        active_count = sum(1 for p in all_products_with_inactive if p.get('status') == 'active')
        inactive_count = sum(1 for p in all_products_with_inactive if p.get('status') == 'inactive')
        print(f"      - Activos: {active_count}")
        print(f"      - Inactivos: {inactive_count}")
    
    # Test 3: Verificar búsqueda
    print("\n" + "-"*60)
    print("📋 TEST 3: ProductModel.search_products('a')")
    search_results = product_model.search_products('a')
    print(f"   Productos encontrados con 'a': {len(search_results)}")
    
    # Test 4: Verificar desde el controller
    print("\n" + "-"*60)
    print("📋 TEST 4: SaleController.search_products_for_sale('')")
    main_controller = MainController()
    sale_controller = SaleController(main_controller)
    
    result = sale_controller.search_products_for_sale("")
    print(f"   Success: {result.get('success')}")
    print(f"   Productos devueltos: {len(result.get('products', []))}")
    
    if result.get('products'):
        print(f"\n   ✅ Primeros 3 productos del controller:")
        for i, p in enumerate(result['products'][:3]):
            print(f"\n   {i+1}. Producto:")
            print(f"      - SKU: {p.get('sku')}")
            print(f"      - Nombre: {p.get('name')}")
            print(f"      - Precio: S/ {p.get('price', 0):.2f}")
            print(f"      - Stock: {p.get('stock_quantity', 0)}")
    else:
        print(f"\n   ❌ NO HAY PRODUCTOS EN EL CONTROLLER")
        if not result.get('success'):
            print(f"   Error: {result.get('message')}")
    
    print("\n" + "="*60)
    print("✅ Debug completado")
    print("="*60 + "\n")

if __name__ == "__main__":
    debug_products()
