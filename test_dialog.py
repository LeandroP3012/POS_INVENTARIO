#!/usr/bin/env python3
"""
Prueba específica del diálogo de usuario para debuggear el problema
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_user_dialog():
    """Probar solo el diálogo de usuario"""
    
    # Datos de roles de prueba
    test_roles = [
        {'id': 1, 'name': 'Super Admin', 'active': True},
        {'id': 2, 'name': 'Administrador', 'active': True},
        {'id': 3, 'name': 'Gerente', 'active': True},
        {'id': 4, 'name': 'Empleado', 'active': True},
        {'id': 5, 'name': 'Cajero', 'active': True}
    ]
    
    class SimpleUserDialog:
        """Versión simplificada del diálogo"""
        
        def __init__(self, parent):
            self.result = None
            
            # Crear ventana
            self.dialog = tk.Toplevel(parent)
            self.dialog.title("Test - Crear Usuario")
            self.dialog.geometry("500x600")
            self.dialog.configure(bg='white')
            self.dialog.transient(parent)
            self.dialog.grab_set()
            
            # Variables
            self.username_var = tk.StringVar()
            self.full_name_var = tk.StringVar()
            self.email_var = tk.StringVar()
            self.password_var = tk.StringVar()
            self.user_type_var = tk.StringVar(value='Cajero')
            
            self.create_interface()
            
        def create_interface(self):
            """Crear interfaz simple"""
            main_frame = tk.Frame(self.dialog, bg='white', padx=30, pady=30)
            main_frame.pack(fill='both', expand=True)
            
            # Username
            tk.Label(main_frame, text="Usuario:", bg='white', font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0, 5))
            username_entry = tk.Entry(main_frame, textvariable=self.username_var, font=('Arial', 11))
            username_entry.pack(fill='x', pady=(0, 15))
            username_entry.focus()
            
            # Full name
            tk.Label(main_frame, text="Nombre completo:", bg='white', font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0, 5))
            fullname_entry = tk.Entry(main_frame, textvariable=self.full_name_var, font=('Arial', 11))
            fullname_entry.pack(fill='x', pady=(0, 15))
            
            # Email
            tk.Label(main_frame, text="Email:", bg='white', font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0, 5))
            email_entry = tk.Entry(main_frame, textvariable=self.email_var, font=('Arial', 11))
            email_entry.pack(fill='x', pady=(0, 15))
            
            # Rol
            tk.Label(main_frame, text="Rol:", bg='white', font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0, 5))
            role_combo = ttk.Combobox(main_frame, textvariable=self.user_type_var, 
                                     values=['Super Admin', 'Administrador', 'Gerente', 'Empleado', 'Cajero'],
                                     state='readonly', font=('Arial', 11))
            role_combo.pack(fill='x', pady=(0, 15))
            
            # Password
            tk.Label(main_frame, text="Contraseña:", bg='white', font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0, 5))
            password_entry = tk.Entry(main_frame, textvariable=self.password_var, font=('Arial', 11), show='*')
            password_entry.pack(fill='x', pady=(0, 20))
            
            # Botones
            button_frame = tk.Frame(main_frame, bg='white')
            button_frame.pack(fill='x', pady=(20, 0))
            
            tk.Button(button_frame, text="Cancelar", command=self.cancel, 
                     bg='#95a5a6', fg='white', font=('Arial', 11, 'bold')).pack(side='left')
            
            tk.Button(button_frame, text="Crear Usuario", command=self.save,
                     bg='#27ae60', fg='white', font=('Arial', 11, 'bold')).pack(side='right')
            
            # Bind events
            self.dialog.bind('<Return>', lambda e: self.save())
            self.dialog.bind('<Escape>', lambda e: self.cancel())
            
        def validate_and_save(self):
            """Validar y guardar"""
            username = self.username_var.get().strip()
            full_name = self.full_name_var.get().strip()
            email = self.email_var.get().strip()
            password = self.password_var.get().strip()
            user_type = self.user_type_var.get().strip()
            
            print(f"VALIDACIÓN:")
            print(f"  Username: '{username}' (len: {len(username)})")
            print(f"  Full name: '{full_name}' (len: {len(full_name)})")
            print(f"  Email: '{email}' (len: {len(email)})")
            print(f"  Password: '{password}' (len: {len(password)})")
            print(f"  Role: '{user_type}' (len: {len(user_type)})")
            
            # Validación
            if not username:
                messagebox.showerror("Error", "El nombre de usuario es requerido")
                return False
                
            if not full_name:
                messagebox.showerror("Error", "El nombre completo es requerido")
                return False
                
            if not email:
                messagebox.showerror("Error", "El email es requerido")
                return False
                
            if not password:
                messagebox.showerror("Error", "La contraseña es requerida")
                return False
                
            # Todo OK - preparar datos
            self.result = {
                'username': username,
                'full_name': full_name,
                'email': email,
                'password': password,
                'user_type': user_type
            }
            
            # Intentar crear el usuario en la base de datos también
            try:
                from controllers.user_controller import UserController
                user_controller = UserController()
                
                # Crear usuario en la base de datos
                success = user_controller.create_user(self.result)
                
                if success:
                    messagebox.showinfo("Éxito", f"✅ Usuario '{username}' creado exitosamente en la base de datos!\n\nDatos:\n- Nombre: {full_name}\n- Email: {email}\n- Rol: {user_type}")
                else:
                    messagebox.showerror("Error BD", f"❌ Validación OK pero error creando usuario en BD.\n\nDatos validados:\n- Nombre: {full_name}\n- Email: {email}\n- Rol: {user_type}")
                    
            except Exception as e:
                messagebox.showerror("Error", f"❌ Error al crear usuario en BD:\n{str(e)}\n\nPero la validación funcionó correctamente.")
            
            return True
            
        def save(self):
            """Guardar"""
            if self.validate_and_save():
                self.dialog.destroy()
                
        def cancel(self):
            """Cancelar"""
            self.result = None
            self.dialog.destroy()
    
    # Crear ventana principal
    root = tk.Tk()
    root.title("Test de Validación de Usuario")
    root.geometry("300x200")
    root.configure(bg='lightgray')
    
    # Botón para abrir diálogo
    def open_dialog():
        dialog = SimpleUserDialog(root)
        root.wait_window(dialog.dialog)
        
        if dialog.result:
            print(f"\n✅ RESULTADO: {dialog.result}")
        else:
            print("\n❌ Diálogo cancelado")
    
    tk.Label(root, text="Test de Validación de Usuario", 
             font=('Arial', 14, 'bold'), bg='lightgray').pack(pady=30)
    
    tk.Button(root, text="Abrir Diálogo de Usuario", command=open_dialog,
             bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
             padx=20, pady=10).pack(pady=20)
    
    tk.Button(root, text="Salir", command=root.quit,
             bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
             padx=20, pady=10).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    print("=== TEST DE DIÁLOGO DE USUARIO ===")
    test_user_dialog()
