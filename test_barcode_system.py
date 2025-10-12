"""
Script de Prueba: Generación de SKU y Códigos de Barras
Ejecutar para verificar que las funciones de generación funcionan correctamente
"""

import sys
sys.path.insert(0, '.')

from models.product_model import ProductModel

def test_sku_generation():
    """Probar generación de SKUs"""
    print("\n" + "="*60)
    print("🔍 PRUEBA 1: Generación de SKU")
    print("="*60)
    
    model = ProductModel()
    
    print("\n📝 Generando 5 SKUs consecutivos...")
    for i in range(1, 6):
        sku = model.generate_next_sku()
        print(f"   SKU {i}: {sku}")
    
    print("\n✅ Formato esperado: PROD-XXXXXX (6 dígitos)")
    print("✅ Capacidad máxima: 999,999 productos")

def test_barcode_generation():
    """Probar generación de códigos de barras"""
    print("\n" + "="*60)
    print("🔍 PRUEBA 2: Generación de Códigos de Barras EAN-13")
    print("="*60)
    
    model = ProductModel()
    
    test_skus = [
        "PROD-000001",
        "PROD-000100",
        "PROD-001000",
        "PROD-999999",
    ]
    
    print("\n📝 Generando códigos de barras para diferentes SKUs...")
    for sku in test_skus:
        barcode = model.generate_barcode_from_sku(sku)
        print(f"   SKU: {sku:15} → Código de Barras: {barcode}")
        
        # Validar estructura
        if len(barcode) == 13 and barcode.startswith('775'):
            print(f"      ✅ Válido: 13 dígitos, inicia con 775 (Perú)")
        else:
            print(f"      ❌ Error: Formato incorrecto")
    
    print("\n✅ Estructura EAN-13:")
    print("   - 775 (país) + 9 dígitos (basado en SKU) + 1 verificador")

def test_check_digit():
    """Probar cálculo de dígito verificador"""
    print("\n" + "="*60)
    print("🔍 PRUEBA 3: Cálculo de Dígito Verificador EAN-13")
    print("="*60)
    
    model = ProductModel()
    
    # Códigos conocidos con dígito verificador correcto
    test_cases = [
        ("775000001000", 3),  # PROD-000001
        ("400532805007", 7),  # Ejemplo real EAN-13
    ]
    
    print("\n📝 Verificando cálculo del dígito verificador...")
    for barcode_12, expected_digit in test_cases:
        calculated = model._calculate_ean13_check_digit(barcode_12)
        status = "✅" if calculated == expected_digit else "❌"
        print(f"   {status} Código: {barcode_12} → Dígito: {calculated} (esperado: {expected_digit})")

def test_database_connection():
    """Probar conexión a base de datos"""
    print("\n" + "="*60)
    print("🔍 PRUEBA 4: Conexión a Base de Datos")
    print("="*60)
    
    model = ProductModel()
    connection = model.get_connection()
    
    if connection and connection.is_connected():
        print("\n✅ Conexión exitosa a la base de datos")
        
        # Verificar último SKU en la base de datos
        cursor = connection.cursor()
        try:
            query = """
                SELECT sku, barcode, name 
                FROM products 
                WHERE sku REGEXP '^PROD-[0-9]{6}$'
                ORDER BY sku DESC 
                LIMIT 5
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            if results:
                print("\n📦 Últimos productos en la base de datos:")
                for row in results:
                    sku, barcode, name = row
                    print(f"   • {sku} | {barcode} | {name[:40]}")
            else:
                print("\n📦 No hay productos con formato PROD-XXXXXX en la BD")
                print("   El primer producto será: PROD-000001")
            
            cursor.close()
        except Exception as e:
            print(f"\n❌ Error al consultar productos: {e}")
    else:
        print("\n❌ No se pudo conectar a la base de datos")
        print("   Verifica la configuración en config/database.json")

def main():
    """Ejecutar todas las pruebas"""
    print("\n" + "🎯"*30)
    print("   SUITE DE PRUEBAS: Sistema de Códigos de Barras")
    print("🎯"*30)
    
    try:
        test_sku_generation()
        test_barcode_generation()
        test_check_digit()
        test_database_connection()
        
        print("\n" + "="*60)
        print("✅ TODAS LAS PRUEBAS COMPLETADAS")
        print("="*60)
        print("\n📋 Siguiente paso:")
        print("   1. Ejecuta la aplicación: python main.py")
        print("   2. Crea un nuevo producto")
        print("   3. Verifica que el SKU y código de barras se generen automáticamente")
        print("\n")
        
    except Exception as e:
        print("\n" + "="*60)
        print(f"❌ ERROR EN LAS PRUEBAS: {e}")
        print("="*60)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
