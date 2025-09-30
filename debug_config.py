#!/usr/bin/env python3
"""
Debug script para verificar la funcionalidad de configuración
"""

import json
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_config():
    """Verificar el estado actual de la configuración"""
    print("🔍 DEBUG: Estado de la configuración")
    print("=" * 50)
    
    config_path = "config/system_config.json"
    
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"📋 Configuración cargada: {len(config)} elementos")
        print(f"🏢 Empresa: {config.get('company_name', 'N/A')}")
        print(f"🖼️ Logo: {config.get('logo_path', 'N/A')}")
        
        # Verificar si el logo existe
        logo_path = config.get('logo_path', '')
        if logo_path:
            if os.path.exists(logo_path):
                print(f"✅ Logo encontrado en: {logo_path}")
            else:
                print(f"❌ Logo NO encontrado en: {logo_path}")
        else:
            print("ℹ️ No hay logo configurado")
        
        print("\n🧪 Para probar:")
        print("1. Cambia el nombre de la empresa en configuración")
        print("2. Verifica que el botón 'Guardar' se habilite")
        print("3. Cambia el logo y verifica que persista")
        print("4. Al presionar 'Volver' sin guardar, debería preguntar")
        
    else:
        print(f"❌ Archivo de configuración no encontrado: {config_path}")

if __name__ == "__main__":
    debug_config()
