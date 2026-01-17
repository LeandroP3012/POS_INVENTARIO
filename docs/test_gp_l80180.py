"""
Script de prueba para verificar detección y configuración de GP-L80180 Series
"""

import win32print
import json
import os

def verificar_deteccion_termica():
    """Verifica si la GP-L80180 se detecta como impresora térmica"""
    
    print("=" * 80)
    print("VERIFICACIÓN DE DETECCIÓN DE GP-L80180 SERIES")
    print("=" * 80)
    print()
    
    # 1. Listar todas las impresoras
    try:
        printers = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
        )
        
        print("📋 IMPRESORAS INSTALADAS:")
        print()
        
        gp_found = False
        gp_printer_name = None
        
        for idx, printer in enumerate(printers, 1):
            printer_name = printer[2]
            print(f"  {idx}. {printer_name}")
            
            if "GP-L80180" in printer_name.upper() or "L80180" in printer_name.upper():
                gp_found = True
                gp_printer_name = printer_name
                print(f"     ✅ ¡Esta es tu GP-L80180 Series!")
        
        print()
        print("-" * 80)
        print()
        
        if not gp_found:
            print("❌ NO SE ENCONTRÓ LA IMPRESORA GP-L80180 SERIES")
            print()
            print("VERIFICA:")
            print("  • La impresora está encendida")
            print("  • Los drivers están instalados")
            print("  • Aparece en 'Configuración > Impresoras y escáneres'")
            print()
            return False
        
        # 2. Verificar detección térmica
        print("🔍 VERIFICACIÓN DE DETECCIÓN TÉRMICA:")
        print()
        
        # Cargar configuración
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'system_config.json')
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                system_config = json.load(f)
            
            printer_mode = system_config.get('printer_mode', 'auto')
            extra_keywords = system_config.get('thermal_printer_keywords', [])
            
            print(f"  Modo de impresora configurado: {printer_mode}")
            print(f"  Palabras clave extra: {extra_keywords}")
            print()
            
        except Exception as e:
            print(f"  ⚠️ No se pudo cargar la configuración: {e}")
            printer_mode = 'auto'
            extra_keywords = []
        
        # Verificar con las mismas reglas que el sistema
        thermal_keywords = ['TP-', 'TM-', 'GP-', 'THERMAL', 'TERMICA', 'POS', '80MM', 'TICKET', 'GPRINTER']
        
        if isinstance(extra_keywords, list):
            thermal_keywords.extend([str(k).upper() for k in extra_keywords])
        
        normalized_name = gp_printer_name.upper()
        
        print(f"  Nombre normalizado: {normalized_name}")
        print(f"  Palabras clave de detección: {thermal_keywords}")
        print()
        
        # Verificar coincidencias
        matches = [kw for kw in thermal_keywords if kw in normalized_name]
        
        if printer_mode == 'thermal':
            print("  ✅ MODO FORZADO A TÉRMICA")
            print(f"     La impresora se usará como térmica independientemente del nombre")
            is_thermal = True
        elif printer_mode == 'standard':
            print("  ❌ MODO FORZADO A ESTÁNDAR")
            print(f"     La impresora NO se usará como térmica")
            is_thermal = False
        else:  # auto
            if matches:
                print(f"  ✅ DETECTADA COMO TÉRMICA (modo auto)")
                print(f"     Coincidencias encontradas: {matches}")
                is_thermal = True
            else:
                print(f"  ❌ NO DETECTADA COMO TÉRMICA (modo auto)")
                print(f"     No se encontraron palabras clave en el nombre")
                is_thermal = False
        
        print()
        print("-" * 80)
        print()
        
        # 3. Recomendaciones
        if is_thermal:
            print("✅ CONFIGURACIÓN CORRECTA")
            print()
            print("La GP-L80180 se detectará como impresora térmica.")
            print("El sistema usará comandos ESC/POS para la impresión.")
            print()
            print("PASOS SIGUIENTES:")
            print("  1. Abre el sistema POS")
            print("  2. Ve a Configuración > Impresión")
            print("  3. Selecciona 'GP-L80180 Series' en el desplegable")
            print("  4. Verifica que 'Modo de Impresora' esté en 'auto' o 'thermal'")
            print("  5. Guarda los cambios")
            print("  6. Realiza una venta de prueba")
        else:
            print("⚠️ CONFIGURACIÓN NECESARIA")
            print()
            print("La GP-L80180 NO se detectará automáticamente como térmica.")
            print()
            print("SOLUCIÓN - Opción 1 (Recomendada):")
            print("  1. Abre el sistema POS")
            print("  2. Ve a Configuración > Impresión")
            print("  3. Selecciona 'GP-L80180 Series' en el desplegable")
            print("  4. Cambia 'Modo de Impresora' a 'thermal' (forzar térmica)")
            print("  5. Guarda los cambios")
            print()
            print("SOLUCIÓN - Opción 2 (Manual):")
            print("  1. Edita config/system_config.json")
            print("  2. Cambia \"printer_mode\": \"auto\" a \"printer_mode\": \"thermal\"")
            print("  3. Guarda y reinicia el sistema")
        
        print()
        print("=" * 80)
        
        return is_thermal
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    resultado = verificar_deteccion_termica()
    print()
    print("Presiona Enter para salir...")
    input()
