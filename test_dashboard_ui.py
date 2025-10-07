#!/usr/bin/env python3
"""
Script de prueba para verificar las mejoras de la interfaz del dashboard
"""

import sys
import os
sys.path.append(os.getcwd())

import tkinter as tk
from views.dashboard_view import DashboardView

def test_dashboard_with_limited_access():
    """Probar dashboard con acceso limitado (pocos módulos)"""
    print("=== PRUEBA DE DASHBOARD CON ACCESO LIMITADO ===")
    
    root = tk.Tk()
    
    # Simular usuario con acceso muy limitado (sin permisos)
    user_data = {
        'id': 1,
        'username': 'ModoEsclavoV1',
        'full_name': 'Usuario de Prueba',
        'user_type': 'user',
        'role_id': 5,  # Rol personalizado sin permisos
        'role_name': 'ModoEsclavoV1'
    }
    
    print(f"Usuario de prueba: {user_data['username']}")
    print(f"Rol: {user_data['role_name']}")
    
    try:
        dashboard = DashboardView(root, user_data)
        print("✅ Dashboard creado exitosamente")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error creando dashboard: {e}")
        import traceback
        traceback.print_exc()

def test_dashboard_with_full_access():
    """Probar dashboard con acceso completo"""
    print("=== PRUEBA DE DASHBOARD CON ACCESO COMPLETO ===")
    
    root = tk.Tk()
    
    # Simular usuario administrador
    user_data = {
        'id': 1,
        'username': 'admin',
        'full_name': 'Administrador',
        'user_type': 'admin',
        'role_id': 1,
        'role_name': 'Super Admin'
    }
    
    print(f"Usuario de prueba: {user_data['username']}")
    print(f"Rol: {user_data['role_name']}")
    
    try:
        dashboard = DashboardView(root, user_data)
        print("✅ Dashboard creado exitosamente")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error creando dashboard: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Función principal"""
    print("Selecciona el tipo de prueba:")
    print("1. Dashboard con acceso limitado")
    print("2. Dashboard con acceso completo")
    
    choice = input("Ingresa tu opción (1 o 2): ").strip()
    
    if choice == '1':
        test_dashboard_with_limited_access()
    elif choice == '2':
        test_dashboard_with_full_access()
    else:
        print("Opción no válida")

if __name__ == "__main__":
    main()
