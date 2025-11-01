"""
Script de prueba para verificar la generación de SKU y códigos de barras
Prueba el autoincremento y la generación correcta de EAN-13
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.product_model import ProductModel

def test_sku_generation():
    """Probar la generación automática de SKU"""
    print("=" * 80)
    print("TEST 1: Generación Automática de SKU (Autoincremento)")
    print("=" * 80)
    
    product_model = ProductModel()
    
    # Generar 3 SKU consecutivos
    for i in range(3):
        sku = product_model.generate_next_code()
        print(f"\n🔢 SKU #{i+1} generado: {sku}")
    
    print("\n")

def test_barcode_generation():
    """Probar la generación de códigos de barras desde diferentes SKU"""
    print("=" * 80)
    print("TEST 2: Generación de Códigos de Barras EAN-13")
    print("=" * 80)
    
    product_model = ProductModel()
    
    # Casos de prueba
    test_cases = [
        "PROD-000001",
        "PROD-000002",
        "PROD-000010",
        "PROD-000100",
        "PROD-001000",
        "PROD-123456",
    ]
    
    for sku in test_cases:
        print(f"\n{'─' * 60}")
        barcode = product_model.generate_barcode_from_code(sku)
        print(f"Resultado: {barcode}")
        
        # Verificar longitud
        if len(barcode) == 13:
            print("✅ Longitud correcta (13 dígitos)")
        else:
            print(f"❌ ERROR: Longitud incorrecta ({len(barcode)} dígitos)")
        
        # Verificar que sea numérico
        if barcode.isdigit():
            print("✅ Solo contiene dígitos")
        else:
            print("❌ ERROR: Contiene caracteres no numéricos")
    
    print("\n")

def test_manual_sku_to_barcode():
    """Probar conversión manual de SKU a código de barras"""
    print("=" * 80)
    print("TEST 3: Conversión Manual SKU → Código de Barras")
    print("=" * 80)
    
    product_model = ProductModel()
    
    print("\nIngresa SKU manualmente (o presiona Enter para terminar):")
    
    while True:
        sku = input("\nSKU (formato PROD-XXXXXX): ").strip()
        
        if not sku:
            break
        
        if not sku.startswith('PROD-'):
            print("⚠️ Advertencia: El SKU debería empezar con 'PROD-'")
        
        barcode = product_model.generate_barcode_from_code(sku)
        print(f"\n📊 Código de barras generado: {barcode}")
        print(f"   Longitud: {len(barcode)} dígitos")
        print(f"   Válido: {'✅ Sí' if len(barcode) == 13 and barcode.isdigit() else '❌ No'}")

if __name__ == "__main__":
    try:
        # Ejecutar tests
        test_sku_generation()
        test_barcode_generation()
        
        # Test interactivo
        response = input("\n¿Deseas probar conversiones manuales? (s/n): ").strip().lower()
        if response == 's':
            test_manual_sku_to_barcode()
        
        print("\n" + "=" * 80)
        print("✅ Tests completados")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
