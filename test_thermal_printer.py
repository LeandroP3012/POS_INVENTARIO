"""
Script de prueba para impresora térmica TP-300
Verifica que la impresora esté configurada correctamente
"""

import os
import sys

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("🖨️  TEST DE IMPRESORA TÉRMICA - SISTEMA POS")
print("=" * 60)

try:
    from utils.thermal_printer import load_printer_from_config
    
    print("\n✅ Módulo thermal_printer importado correctamente")
    
    # Cargar impresora desde configuración
    print("\n📄 Cargando configuración de impresora...")
    printer = load_printer_from_config()
    
    # Mostrar impresoras disponibles
    print("\n📋 Impresoras disponibles en el sistema:")
    printers = printer.get_available_printers()
    
    if not printers:
        print("   ⚠️  No se encontraron impresoras instaladas")
    else:
        for i, p in enumerate(printers, 1):
            marker = "✓" if p == printer.printer_name else " "
            print(f"   [{marker}] {i}. {p}")
    
    print(f"\n🖨️  Impresora configurada: {printer.printer_name}")
    
    # Preguntar si imprimir prueba
    print("\n" + "=" * 60)
    print("¿Desea imprimir un ticket de prueba?")
    print("NOTA: Esto enviará un ticket a la impresora configurada")
    print("=" * 60)
    response = input("\nEscribir 's' para imprimir, cualquier otra tecla para cancelar: ").strip().lower()
    
    if response == 's':
        print("\n🖨️  Enviando ticket de prueba a la impresora...")
        print(f"   Impresora: {printer.printer_name}")
        
        if printer.test_printer():
            print("\n" + "=" * 60)
            print("✅ ¡ÉXITO! Ticket de prueba enviado correctamente")
            print("=" * 60)
            print("\nSi la impresora no imprimió:")
            print("  1. Verifique que la impresora esté encendida")
            print("  2. Verifique que tenga papel")
            print("  3. Verifique que el nombre en system_config.json sea correcto")
            print("  4. Intente reiniciar la impresora")
        else:
            print("\n" + "=" * 60)
            print("❌ ERROR al enviar ticket a la impresora")
            print("=" * 60)
            print("\nPosibles soluciones:")
            print("  1. Verificar que la impresora esté encendida y conectada")
            print("  2. Verificar nombre en config/system_config.json")
            print("  3. Revisar el archivo de logs para más detalles")
    else:
        print("\n🚫 Prueba de impresión cancelada")
    
    print("\n" + "=" * 60)
    print("✅ Test completado")
    print("=" * 60)

except ImportError as e:
    print(f"\n❌ ERROR: No se pudo importar el módulo thermal_printer")
    print(f"   Detalles: {e}")
    print("\n📦 Asegúrese de tener instalado pywin32:")
    print("   pip install pywin32>=306")

except Exception as e:
    print(f"\n❌ ERROR INESPERADO: {e}")
    import traceback
    traceback.print_exc()
    
    print("\n💡 Soluciones posibles:")
    print("  1. Verificar que config/system_config.json existe")
    print("  2. Verificar que pywin32 está instalado")
    print("  3. Ejecutar como administrador si es necesario")

print("\n")
