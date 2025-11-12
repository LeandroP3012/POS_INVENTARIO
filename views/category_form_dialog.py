"""
Diálogo para Crear/Editar Categorías
Formulario modal para gestión de categorías
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional, List


class CategoryFormDialog:
    """Diálogo para crear o editar categorías"""
    
    def __init__(self, parent, category: Optional[Dict[str, Any]] = None, 
                 categories: List[Dict[str, Any]] = None,
                 allow_delete: bool = False):
        self.parent = parent
        self.category = category
        self.categories = categories or []
        self.result = None
        self.allow_delete = allow_delete and category is not None
        
        # Crear ventana
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Editar Categoría" if category else "Nueva Categoría")
        self.dialog.geometry("500x500")  # Aumentado de 400 a 500
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Configurar protocolo de cierre (X)
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
        # Centrar ventana
        self.center_window()
        
        # Variables
        self.setup_variables()
        
        # Crear interfaz
        self.create_widgets()
        
        # Si es edición, cargar datos
        if self.category:
            self.load_category_data()
        else:
            self.dialog.after(100, lambda: self.name_entry.focus())
    
    def center_window(self):
        """Centrar ventana en la pantalla"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_variables(self):
        """Configurar variables de los campos"""
        # Crear variables vinculadas al dialog
        self.name_var = tk.StringVar(master=self.dialog)
        self.description_var = tk.StringVar(master=self.dialog)
        self.parent_var = tk.StringVar(master=self.dialog)
        self.status_var = tk.StringVar(master=self.dialog, value="active")
        
        # Debug: verificar que las variables se crearon
        print(f"🔧 DEBUG - Variables creadas:")
        print(f"   - name_var: {self.name_var}")
        print(f"   - status_var: {self.status_var} (valor inicial: {self.status_var.get()})")
        
        # Agregar trace para monitorear cambios en name_var
        def on_name_change(*args):
            print(f"📝 DEBUG - name_var cambió a: '{self.name_var.get()}'")
        
        self.name_var.trace('w', on_name_change)
    
    def create_widgets(self):
        """Crear widgets del formulario"""
        # Header
        header = tk.Frame(self.dialog, bg='#2c3e50', height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        icon = "✏️" if self.category else "➕"
        title = "Editar Categoría" if self.category else "Nueva Categoría"
        
        tk.Label(
            header,
            text=f"{icon}  {title}",
            font=('Segoe UI', 16, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=20)
        
        # Contenido
        content = tk.Frame(self.dialog, bg='#ecf0f1')
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Card principal
        card = tk.Frame(content, bg='white', relief='solid', bd=1)
        card.pack(fill='both', expand=True)
        
        card_content = tk.Frame(card, bg='white')
        card_content.pack(fill='both', expand=True, padx=25, pady=20)
        
        # Nombre
        tk.Label(
            card_content,
            text="Nombre de la Categoría *",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#2c3e50',
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        self.name_entry = tk.Entry(
            card_content,
            textvariable=self.name_var,
            font=('Segoe UI', 11),
            relief='solid',
            bd=1,
            bg='#f8f9fa'
        )
        self.name_entry.pack(fill='x', pady=(0, 15))
        
        # Debug: Verificar vinculación
        print(f"🔧 DEBUG - Entry creado, vinculado a: {self.name_entry.cget('textvariable')}")
        
        # Descripción
        tk.Label(
            card_content,
            text="Descripción",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#2c3e50',
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        self.description_text = tk.Text(
            card_content,
            height=4,
            font=('Segoe UI', 10),
            relief='solid',
            bd=1,
            wrap='word',
            bg='#f8f9fa'
        )
        self.description_text.pack(fill='x', pady=(0, 15))
        
        # Estado
        tk.Label(
            card_content,
            text="Estado",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#2c3e50',
            anchor='w'
        ).pack(fill='x', pady=(10, 10))
        
        radio_frame = tk.Frame(card_content, bg='white')
        radio_frame.pack(fill='x')
        
        tk.Radiobutton(
            radio_frame,
            text="✅ Activo",
            variable=self.status_var,
            value="active",
            font=('Segoe UI', 10),
            bg='white',
            activebackground='white',
            selectcolor='#e8f5e9'
        ).pack(side='left', padx=(0, 30))
        
        tk.Radiobutton(
            radio_frame,
            text="❌ Inactivo",
            variable=self.status_var,
            value="inactive",
            font=('Segoe UI', 10),
            bg='white',
            activebackground='white',
            selectcolor='#ffebee'
        ).pack(side='left')
        
        # Footer con botones
        footer = tk.Frame(self.dialog, bg='#ecf0f1', height=70)
        footer.pack(fill='x', side='bottom')
        footer.pack_propagate(False)
        
        button_container = tk.Frame(footer, bg='#ecf0f1')
        button_container.pack(expand=True)
        
        tk.Button(
            button_container,
            text="💾 Guardar",
            command=self.on_save,
            font=('Segoe UI', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            relief='flat',
            cursor='hand2',
            padx=25,
            pady=10
        ).pack(side='left', padx=10)

        if self.allow_delete:
            tk.Button(
                button_container,
                text="🗑️ Eliminar",
                command=self.on_delete,
                font=('Segoe UI', 11),
                bg='#e74c3c',
                fg='white',
                activebackground='#c0392b',
                relief='flat',
                cursor='hand2',
                padx=25,
                pady=10
            ).pack(side='left', padx=10)

        tk.Button(
            button_container,
            text="❌ Cancelar",
            command=self.on_cancel,
            font=('Segoe UI', 11),
            bg='#95a5a6',
            fg='white',
            activebackground='#7f8c8d',
            relief='flat',
            cursor='hand2',
            padx=25,
            pady=10
        ).pack(side='left', padx=10)
    
    def load_category_data(self):
        """Cargar datos de la categoría para edición"""
        if not self.category:
            return
        
        print(f"📥 DEBUG - Cargando datos de categoría: {self.category}")
        
        self.name_var.set(self.category.get('name', ''))
        self.description_text.delete('1.0', tk.END)
        self.description_text.insert('1.0', self.category.get('description', ''))
        
        # Cargar estado
        status = self.category.get('status', 'active')
        print(f"📥 DEBUG - Estado de la categoría: '{status}'")
        self.status_var.set(status)
        print(f"📥 DEBUG - status_var después de set: '{self.status_var.get()}'")
    
    def validate_data(self) -> bool:
        """Validar datos del formulario"""
        if not self.name_var.get().strip():
            messagebox.showerror(
                "Error de validación",
                "El nombre de la categoría es requerido",
                parent=self.dialog
            )
            return False
        
        return True
    
    def get_category_data(self) -> Dict[str, Any]:
        """Obtener datos del formulario"""
        # Por ahora, sin categoría padre (siempre None)
        return {
            'name': self.name_var.get().strip(),
            'description': self.description_text.get('1.0', tk.END).strip(),
            'parent_id': None,  # Sin jerarquía por ahora
            'status': self.status_var.get()
        }
    
    def on_save(self):
        """Manejar guardar"""
        # Debug: Verificar el valor actual del nombre
        name_value = self.name_var.get()
        print(f"🔍 DEBUG - Valor del nombre antes de validar: '{name_value}' (len={len(name_value)})")
        print(f"🔍 DEBUG - Valor después de strip: '{name_value.strip()}' (len={len(name_value.strip())})")
        print(f"🔍 DEBUG - Estado seleccionado: '{self.status_var.get()}'")
        
        if not self.validate_data():
            print(f"❌ DEBUG - Validación falló")
            return
        
        print(f"✅ DEBUG - Validación exitosa")
        self.result = self.get_category_data()
        print(f"📦 DEBUG - Datos del resultado: {self.result}")
        self.dialog.destroy()
    
    def on_cancel(self):
        """Manejar cancelar"""
        self.result = None
        self.dialog.destroy()

    def on_delete(self):
        """Solicitar eliminación de la categoría actual"""
        if not self.category:
            return
        if messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Deseas eliminar la categoría '{self.category.get('name', '')}'?",
            parent=self.dialog
        ):
            self.result = {
                '__action__': 'delete',
                'category_id': self.category.get('id')
            }
            self.dialog.destroy()
    
    def show(self) -> Optional[Dict[str, Any]]:
        """Mostrar diálogo y retornar resultado"""
        self.dialog.wait_window()
        return self.result
