#!/usr/bin/env python3
"""
Script de prueba para verificar que el login carga el nombre de la empresa correctamente
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from views.login_view import LoginView
import json

def test_company_name_loading():
    """Probar carga del nombre de la empresa"""
    
    # Leer configuración directamente
    config_path = os.path.join('config', 'system_config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    expected_name = config.get('company_name', 'Sistema POS')
    print(f"🔍 Nombre esperado desde JSON: '{expected_name}'")
    
    # Crear instancia de LoginView (sin mostrar la ventana)
    login = LoginView()
    actual_name = login.company_name
    
    print(f"🔍 Nombre cargado en LoginView: '{actual_name}'")
    
    # Verificar que coincidan
    if actual_name == expected_name:
        print(f"✅ ¡ÉXITO! El nombre de la empresa se carga correctamente: '{actual_name}'")
        return True
    else:
        print(f"❌ ERROR: No coinciden los nombres")
        print(f"   Esperado: '{expected_name}'")
        print(f"   Actual:   '{actual_name}'")
        return False

def test_title_update():
    """Probar actualización del título"""
    
    # Crear instancia de LoginView
    login = LoginView()
    
    # Verificar que el título se establece correctamente
    if hasattr(login, 'title_label') and login.title_label:
        actual_title = login.title_label.cget('text')
        expected_title = login.company_name
        
        print(f"🔍 Título en el widget: '{actual_title}'")
        print(f"🔍 Nombre de empresa: '{expected_title}'")
        
        if actual_title == expected_title:
            print(f"✅ ¡ÉXITO! El título del login coincide con el nombre de la empresa")
            return True
        else:
            print(f"❌ ERROR: El título no coincide")
            return False
    else:
        print(f"❌ ERROR: No se encontró el widget title_label")
        return False

if __name__ == "__main__":
    print("🧪 INICIANDO PRUEBAS DE NOMBRE DE EMPRESA EN LOGIN")
    print("=" * 60)
    
    try:
        # Prueba 1: Carga del nombre
        print("\n📋 PRUEBA 1: Carga del nombre de empresa")
        test1_result = test_company_name_loading()
        
        # Prueba 2: Actualización del título
        print("\n📋 PRUEBA 2: Actualización del título en la interfaz")
        test2_result = test_title_update()
        
        # Resultado final
        print("\n" + "=" * 60)
        if test1_result and test2_result:
            print("🎉 ¡TODAS LAS PRUEBAS PASARON! El sistema funciona correctamente.")
        else:
            print("⚠️  Algunas pruebas fallaron. Revisar la implementación.")
            
    except Exception as e:
        print(f"❌ ERROR EN LAS PRUEBAS: {e}")
        import traceback
        traceback.print_exc()
