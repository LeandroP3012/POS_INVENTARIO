#!/usr/bin/env python3
"""
Script de prueba para la gestión de usuarios con roles
"""

import sys
import os
sys.path.append(os.getcwd())

import tkinter as tk
from views.user_management_view import UserManagementView

def test_user_management():
    """Probar la interfaz de gestión de usuarios"""
    
    # Crear ventana principal
    root = tk.Tk()
    
    # Datos de usuario simulados (como si fuera un admin logueado)
    user_data = {
        'id': 1,
        'username': 'admin',
        'full_name': 'Administrador del Sistema',
        'user_type': 'admin'
    }
    
    try:
        # Crear vista de gestión de usuarios
        user_view = UserManagementView(root, user_data, embedded=False)
        
        print("Vista de gestión de usuarios creada exitosamente")
        print("Roles disponibles en el sistema:")
        
        for role in user_view.roles_data:
            print(f"  - {role.get('name')} (ID: {role.get('id')})")
        
        # Ejecutar la aplicación
        root.mainloop()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=== PRUEBA DE GESTIÓN DE USUARIOS CON ROLES ===")
    test_user_management()
