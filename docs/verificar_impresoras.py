"""
Script para verificar las impresoras disponibles en el sistema
"""

import win32print

def listar_impresoras():
    """Lista todas las impresoras disponibles en el sistema"""
    print("=" * 70)
    print("VERIFICACIÓN DE IMPRESORAS DISPONIBLES")
    print("=" * 70)
    print()
    
    try:
        # Obtener impresoras locales y de red
        printers = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
        )
        
        if not printers:
            print("❌ No se encontraron impresoras instaladas")
            print()
            print("SUGERENCIAS:")
            print("  1. Verifica que tu impresora GP-L80180 Series esté instalada")
            print("  2. Ve a Configuración > Dispositivos > Impresoras y escáneres")
            print("  3. Instala los drivers más recientes desde el sitio del fabricante")
            return
        
        print(f"✅ Se encontraron {len(printers)} impresora(s):\n")
        
        # Obtener impresora predeterminada
        try:
            default_printer = win32print.GetDefaultPrinter()
        except:
            default_printer = None
        
        for idx, printer in enumerate(printers, 1):
            printer_name = printer[2]
            is_default = " [PREDETERMINADA]" if printer_name == default_printer else ""
            
            print(f"{idx}. {printer_name}{is_default}")
            
            # Verificar si es la GP-L80180
            if "GP-L80180" in printer_name.upper() or "L80180" in printer_name.upper():
                print(f"   ✅ Esta es tu impresora GP-L80180 Series!")
        
        print()
        print("=" * 70)
        
        # Buscar específicamente la GP-L80180
        gp_printers = [p[2] for p in printers if "GP-L80180" in p[2].upper() or "L80180" in p[2].upper()]
        
        if gp_printers:
            print("\n🎯 IMPRESORA GP-L80180 DETECTADA:")
            for gp_printer in gp_printers:
                print(f"   • {gp_printer}")
            print("\n✅ Tu impresora está correctamente instalada.")
            print("   Ahora puedes seleccionarla en Configuración > Impresión")
        else:
            print("\n⚠️  IMPRESORA GP-L80180 NO DETECTADA")
            print("\nPARA INSTALARLA:")
            print("  1. Asegúrate de que la impresora esté conectada y encendida")
            print("  2. Ve a Configuración de Windows > Dispositivos > Impresoras y escáneres")
            print("  3. Haz clic en 'Agregar una impresora o un escáner'")
            print("  4. Selecciona 'GP-L80180 Series' cuando aparezca")
            print("  5. Instala los drivers si se te solicita")
            print("  6. Vuelve a ejecutar este script para verificar")
        
        print()
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error al obtener las impresoras: {e}")
        print()
        print("POSIBLE CAUSA:")
        print("  - El módulo win32print no está instalado correctamente")
        print("  - Ejecuta: pip install pywin32")

if __name__ == "__main__":
    listar_impresoras()
    print("\nPresiona Enter para salir...")
    input()
