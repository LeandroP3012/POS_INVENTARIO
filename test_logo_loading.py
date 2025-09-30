#!/usr/bin/env python3
"""
Prueba específica para verificar que el logo se carga correctamente
"""

import sys
import os
import json
sys.path.append(os.path.dirname(__file__))

def test_logo_loading():
    """Probar la carga del logo"""
    print("🧪 Probando carga de logo...")
    
    # Verificar configuración
    config_path = os.path.join('config', 'system_config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        logo_path = config.get('logo_path', '')
        company_name = config.get('company_name', '')
        
        print(f"📋 Configuración actual:")
        print(f"   - Empresa: {company_name}")
        print(f"   - Logo: {logo_path}")
        
        # Verificar que el archivo del logo existe
        if logo_path and os.path.exists(logo_path):
            print(f"✅ Archivo de logo encontrado: {logo_path}")
            
            # Probar cargar la imagen
            try:
                from PIL import Image, ImageTk
                image = Image.open(logo_path)
                print(f"   - Tamaño original: {image.size}")
                
                # Redimensionar
                image.thumbnail((80, 80), Image.Resampling.LANCZOS)
                print(f"   - Tamaño redimensionado: {image.size}")
                
                # Crear PhotoImage
                photo = ImageTk.PhotoImage(image)
                print(f"✅ Logo cargado exitosamente como PhotoImage")
                
            except Exception as e:
                print(f"❌ Error cargando logo: {e}")
        else:
            print(f"❌ Archivo de logo no encontrado: {logo_path}")
    else:
        print("❌ Archivo de configuración no encontrado")

if __name__ == "__main__":
    test_logo_loading()
