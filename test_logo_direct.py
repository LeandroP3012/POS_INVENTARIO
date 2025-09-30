#!/usr/bin/env python3
"""
Prueba directa del logo en login
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import tkinter as tk
from views.login_view import LoginView

def test_logo_direct():
    """Probar logo directamente"""
    print("🧪 Probando logo directamente...")
    
    # Crear login view
    login_view = LoginView()
    
    print("🔄 Intentando actualizar logo manualmente...")
    
    # Llamar directamente el método de actualización
    login_view.update_company_name()
    
    # Esperar un poco y luego intentar actualizar logo
    def delayed_update():
        print("⏰ Actualizando logo con delay...")
        login_view.try_update_logo()
        
        # Cerrar después de 3 segundos
        login_view.root.after(3000, login_view.root.quit)
    
    # Programar actualización después de que la interfaz esté lista
    login_view.root.after(500, delayed_update)
    
    print("👀 Mostrando login...")
    login_view.run()

if __name__ == "__main__":
    test_logo_direct()
