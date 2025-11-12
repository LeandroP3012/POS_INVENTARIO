"""
Módulo de Gestión de Licencias
Para integrar en el Sistema POS
"""

import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path
from datetime import datetime
import hashlib


class LicenseManager:
    """Gestor de licencias para la aplicación"""
    
    def __init__(self, config_dir="config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.license_file = self.config_dir / "license.json"
        self.secret_key = "POS_SISTEMA_2025_SECRET"
    
    def generate_activation_code(self, license_key):
        """
        Genera código de activación esperado para una licencia
        (Debe ser idéntico al instalador y generador)
        """
        data = license_key + self.secret_key
        
        # Función hash simple compatible con Inno Setup
        def simple_hash(s):
            hash_val = 5381
            for c in s:
                hash_val = ((hash_val << 5) + hash_val) + ord(c)
                hash_val = hash_val & 0xFFFFFFFF  # Mantener 32 bits
            return format(hash_val, '08X')
        
        # Generar múltiples hashes
        hash1 = simple_hash(data)
        hash2 = simple_hash(data + '1')
        hash3 = simple_hash(data + '2')
        hash4 = simple_hash(data + '3')
        
        full_hash = (hash1 + hash2 + hash3 + hash4).upper()
        
        # Formatear como XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX
        parts = [full_hash[i:i+4] for i in range(0, 32, 4)]
        return "-".join(parts)

    
    def validate_license(self, license_key, activation_code):
        """Validar licencia y código de activación"""
        expected = self.generate_activation_code(license_key)
        return activation_code.upper() == expected.upper()
    
    def is_activated(self):
        """Verificar si la aplicación tiene licencia activada"""
        if not self.license_file.exists():
            return False
        
        try:
            with open(self.license_file, 'r') as f:
                license_data = json.load(f)
            
            return self.validate_license(
                license_data.get('license_key', ''),
                license_data.get('activation_code', '')
            )
        except:
            return False
    
    def activate(self, license_key, activation_code):
        """Activar licencia"""
        if not self.validate_license(license_key, activation_code):
            return False, "Licencia o código de activación inválido"
        
        license_data = {
            "license_key": license_key,
            "activation_code": activation_code,
            "activation_date": datetime.now().isoformat(),
            "status": "active"
        }
        
        with open(self.license_file, 'w') as f:
            json.dump(license_data, f, indent=2)
        
        return True, "Licencia activada correctamente"
    
    def get_license_info(self):
        """Obtener información de la licencia actual"""
        if not self.license_file.exists():
            return None
        
        try:
            with open(self.license_file, 'r') as f:
                return json.load(f)
        except:
            return None
    
    def show_activation_dialog(self, parent=None):
        """Mostrar diálogo de activación de licencia"""
        dialog = tk.Toplevel(parent) if parent else tk.Tk()
        dialog.title("Activación de Licencia")
        dialog.geometry("500x400")
        dialog.resizable(False, False)
        
        # Centrar ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Frame principal
        main_frame = tk.Frame(dialog, bg='white', padx=30, pady=30)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        tk.Label(
            main_frame,
            text="🔐 Activación de Licencia",
            font=('Segoe UI', 18, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=(0, 10))
        
        tk.Label(
            main_frame,
            text="Sistema POS - Punto de Venta",
            font=('Segoe UI', 11),
            bg='white',
            fg='#7f8c8d'
        ).pack(pady=(0, 30))
        
        # Clave de licencia
        tk.Label(
            main_frame,
            text="Clave de Licencia:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#34495e'
        ).pack(anchor='w')
        
        license_entry = tk.Entry(
            main_frame,
            font=('Courier New', 11),
            width=30,
            relief='solid',
            bd=1
        )
        license_entry.pack(fill='x', pady=(5, 15))
        license_entry.insert(0, "XXXX-XXXX-XXXX-XXXX")
        license_entry.bind('<FocusIn>', lambda e: license_entry.delete(0, 'end') if license_entry.get() == "XXXX-XXXX-XXXX-XXXX" else None)
        
        # Código de activación
        tk.Label(
            main_frame,
            text="Código de Activación:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#34495e'
        ).pack(anchor='w')
        
        activation_entry = tk.Entry(
            main_frame,
            font=('Courier New', 9),
            width=40,
            relief='solid',
            bd=1
        )
        activation_entry.pack(fill='x', pady=(5, 30))
        
        result_var = tk.BooleanVar(value=False)
        
        def activate_license():
            license_key = license_entry.get().strip().upper()
            activation_code = activation_entry.get().strip().upper()
            
            if not license_key or license_key == "XXXX-XXXX-XXXX-XXXX":
                messagebox.showerror("Error", "Ingrese la clave de licencia")
                return
            
            if not activation_code:
                messagebox.showerror("Error", "Ingrese el código de activación")
                return
            
            success, message = self.activate(license_key, activation_code)
            
            if success:
                messagebox.showinfo("✅ Éxito", message)
                result_var.set(True)
                dialog.destroy()
            else:
                messagebox.showerror("❌ Error", message)
        
        # Botones
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(fill='x')
        
        tk.Button(
            button_frame,
            text="✓ Activar",
            command=activate_license,
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            padx=30,
            pady=10,
            cursor='hand2'
        ).pack(side='left', padx=(0, 10))
        
        tk.Button(
            button_frame,
            text="✕ Cancelar",
            command=dialog.destroy,
            bg='#95a5a6',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            padx=30,
            pady=10,
            cursor='hand2'
        ).pack(side='left')
        
        # Info
        info_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='solid', bd=1)
        info_frame.pack(fill='x', pady=(30, 0), padx=0)
        
        tk.Label(
            info_frame,
            text="ℹ️ Información",
            font=('Segoe UI', 9, 'bold'),
            bg='#ecf0f1',
            fg='#34495e'
        ).pack(anchor='w', padx=10, pady=(10, 5))
        
        tk.Label(
            info_frame,
            text="• La clave de licencia y el código de activación\n  se encuentran en el archivo de licencia proporcionado\n• Para obtener una licencia, contacte a soporte",
            font=('Segoe UI', 8),
            bg='#ecf0f1',
            fg='#7f8c8d',
            justify='left'
        ).pack(anchor='w', padx=10, pady=(0, 10))
        
        dialog.wait_window()
        return result_var.get()


def check_license_on_startup(parent=None):
    """
    Verificar licencia al iniciar la aplicación
    Mostrar diálogo si no está activada
    """
    manager = LicenseManager()
    
    if not manager.is_activated():
        # Mostrar diálogo de activación
        activated = manager.show_activation_dialog(parent)
        
        if not activated:
            messagebox.showwarning(
                "Licencia Requerida",
                "La aplicación requiere una licencia válida para funcionar.\n\n"
                "La aplicación se cerrará."
            )
            return False
    
    return True


if __name__ == "__main__":
    # Prueba del diálogo
    root = tk.Tk()
    root.withdraw()
    
    if check_license_on_startup(root):
        messagebox.showinfo("✅ Éxito", "Licencia activada correctamente")
    else:
        messagebox.showerror("❌ Error", "No se pudo activar la licencia")
    
    root.destroy()
