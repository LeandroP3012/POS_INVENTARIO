#!/usr/bin/env python3
"""
Script de prueba para verificar la actualización del logo en el login
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from views.login_view import LoginView
import time

def test_logo_update():
    """Probar la actualización del logo"""
    print("🧪 Probando actualización de logo en login...")
    
    # Crear vista de login
    login_view = LoginView()
    
    print("📋 Estado inicial:")
    print(f"   - Nombre empresa: {login_view.company_name}")
    
    # Probar actualización
    print("\n🔄 Probando actualización...")
    login_view.update_company_name()
    
    print("\n✅ Prueba completada")
    
    # Mostrar login por un momento para verificar visualmente
    print("👀 Mostrando login por 3 segundos...")
    login_view.root.after(3000, login_view.root.quit)
    login_view.run()

if __name__ == "__main__":
    test_logo_update()
