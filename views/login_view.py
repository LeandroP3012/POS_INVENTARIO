"""
Vista de Login para el Sistema POS
Interfaz de autenticación con diseño moderno
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from views.base_view import BaseView

class LoginView(BaseView):
    """Vista para el formulario de login"""
    
    def __init__(self):
        super().__init__()
        
        # Variables del formulario
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.remember_var = tk.BooleanVar()
        self.show_password_var = tk.BooleanVar()
        
        # Widgets principales
        self.username_entry = None
        self.password_entry = None
        self.login_button = None
        self.status_label = None
        
        # Configurar ventana principal
        self.setup_main_window()
        self.create_login_form()
        
    def setup_main_window(self):
        """Configurar ventana principal"""
        self.root.title("Sistema POS - Iniciar Sesión")
        self.root.geometry("450x600")
        self.root.resizable(False, False)
        self.root.configure(bg=self.colors['background'])
        
        # Centrar ventana
        self.center_window(self.root, 450, 600)
        
        # Configurar protocolo de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_login_form(self):
        """Crear formulario de login"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Header con logo y título
        self.create_header(main_frame)
        
        # Formulario
        self.create_form(main_frame)
        
        # Footer
        self.create_footer(main_frame)
    
    def create_header(self, parent):
        """Crear header con logo y título"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill='x', pady=(0, 40))
        
        # Logo placeholder
        logo_frame = ttk.Frame(header_frame)
        logo_frame.pack(pady=(0, 20))
        
        logo_label = ttk.Label(
            logo_frame,
            text="🏪",
            font=('Segoe UI', 48),
            background=self.colors['background']
        )
        logo_label.pack()
        
        # Título principal
        title_label = ttk.Label(
            header_frame,
            text="Sistema POS",
            style='Title.TLabel'
        )
        title_label.pack()
        
        # Subtítulo
        subtitle_label = ttk.Label(
            header_frame,
            text="Inicia sesión para continuar",
            font=self.fonts['default'],
            background=self.colors['background'],
            foreground=self.colors['on_surface_variant']
        )
        subtitle_label.pack(pady=(5, 0))
    
    def create_form(self, parent):
        """Crear formulario de entrada"""
        form_frame = ttk.Frame(parent, style='Card.TFrame')
        form_frame.pack(fill='x', pady=(0, 30))
        
        # Padding interno
        inner_frame = ttk.Frame(form_frame)
        inner_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Campo de usuario
        self.create_username_field(inner_frame)
        
        # Campo de contraseña
        self.create_password_field(inner_frame)
        
        # Checkbox recordar
        self.create_remember_checkbox(inner_frame)
        
        # Botón de login
        self.create_login_button(inner_frame)
        
        # Label de estado
        self.create_status_label(inner_frame)
    
    def create_username_field(self, parent):
        """Crear campo de usuario"""
        field_frame = ttk.Frame(parent)
        field_frame.pack(fill='x', pady=(0, 20))
        
        username_label = ttk.Label(
            field_frame,
            text="Usuario",
            font=self.fonts['default']
        )
        username_label.pack(anchor='w', pady=(0, 5))
        
        self.username_entry = ttk.Entry(
            field_frame,
            textvariable=self.username_var,
            font=self.fonts['default'],
            style='Custom.TEntry'
        )
        self.username_entry.pack(fill='x', ipady=10)
        
        self.add_placeholder(self.username_entry, "Ingresa tu usuario")
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
    
    def create_password_field(self, parent):
        """Crear campo de contraseña"""
        field_frame = ttk.Frame(parent)
        field_frame.pack(fill='x', pady=(0, 20))
        
        password_label = ttk.Label(
            field_frame,
            text="Contraseña",
            font=self.fonts['default']
        )
        password_label.pack(anchor='w', pady=(0, 5))
        
        entry_frame = ttk.Frame(field_frame)
        entry_frame.pack(fill='x')
        
        self.password_entry = ttk.Entry(
            entry_frame,
            textvariable=self.password_var,
            font=self.fonts['default'],
            style='Custom.TEntry',
            show='*'
        )
        self.password_entry.pack(side='left', fill='x', expand=True, ipady=10)
        
        show_button = ttk.Button(
            entry_frame,
            text="👁",
            width=3,
            command=self.toggle_password_visibility
        )
        show_button.pack(side='right', padx=(5, 0))
        
        self.add_placeholder(self.password_entry, "Ingresa tu contraseña")
        self.password_entry.bind('<Return>', lambda e: self.attempt_login())
    
    def create_remember_checkbox(self, parent):
        """Crear checkbox de recordar"""
        remember_frame = ttk.Frame(parent)
        remember_frame.pack(fill='x', pady=(0, 25))
        
        remember_check = ttk.Checkbutton(
            remember_frame,
            text="Recordar mis datos",
            variable=self.remember_var,
            style='TCheckbutton'
        )
        remember_check.pack(anchor='w')
    
    def create_login_button(self, parent):
        """Crear botón de login"""
        self.login_button = ttk.Button(
            parent,
            text="Iniciar Sesión",
            style='Primary.TButton',
            command=self.attempt_login
        )
        self.login_button.pack(fill='x', pady=(0, 20), ipady=5)
    
    def create_status_label(self, parent):
        """Crear label de estado"""
        self.status_label = ttk.Label(
            parent,
            text="",
            font=self.fonts['small'],
            background=self.colors['surface'],
            foreground=self.colors['danger']
        )
        self.status_label.pack(fill='x')
    
    def create_footer(self, parent):
        """Crear footer con información adicional"""
        footer_frame = ttk.Frame(parent)
        footer_frame.pack(fill='x', side='bottom')
        
        self.create_separator(footer_frame)
        
        help_label = ttk.Label(
            footer_frame,
            text="¿Problemas para acceder? Contacta al administrador",
            font=self.fonts['small'],
            background=self.colors['background'],
            foreground=self.colors['on_surface_variant']
        )
        help_label.pack(pady=(10, 0))
        
        version_label = ttk.Label(
            footer_frame,
            text="Sistema POS v1.0",
            font=self.fonts['small'],
            background=self.colors['background'],
            foreground=self.colors['on_surface_variant']
        )
        version_label.pack(pady=(5, 0))
    
    def toggle_password_visibility(self):
        """Alternar visibilidad de contraseña"""
        if self.password_entry.cget('show') == '*':
            self.password_entry.configure(show='')
        else:
            self.password_entry.configure(show='*')
    
    def attempt_login(self):
        """Intentar hacer login"""
        self.clear_status()
        
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username:
            self.show_status("Por favor ingresa tu usuario", 'error')
            self.username_entry.focus()
            return
        
        if not password:
            self.show_status("Por favor ingresa tu contraseña", 'error')
            self.password_entry.focus()
            return
        
        self.set_login_state(False)
        self.show_status("Verificando credenciales...", 'info')
        
        self.trigger_callback('login_attempt', {
            'username': username,
            'password': password,
            'remember': self.remember_var.get()
        })
    
    def show_status(self, message: str, status_type: str = 'info'):
        """Mostrar mensaje de estado"""
        colors = {
            'info': self.colors['primary'],
            'error': self.colors['danger'],
            'success': self.colors['success'],
            'warning': self.colors['warning']
        }
        
        self.status_label.configure(
            text=message,
            foreground=colors.get(status_type, self.colors['on_surface'])
        )
        
        if status_type == 'info':
            self.root.after(5000, self.clear_status)
    
    def clear_status(self):
        """Limpiar mensaje de estado"""
        self.status_label.configure(text="")
    
    def set_login_state(self, enabled: bool):
        """Habilitar/deshabilitar controles de login"""
        state = 'normal' if enabled else 'disabled'
        
        self.username_entry.configure(state=state)
        self.password_entry.configure(state=state)
        self.login_button.configure(state=state)
        
        if enabled:
            self.login_button.configure(text="Iniciar Sesión")
        else:
            self.login_button.configure(text="Verificando...")
    
    def on_login_success(self, user_data: dict):
        """Manejar login exitoso"""
        self.show_status(f"¡Bienvenido {user_data.get('full_name', user_data.get('username'))}!", 'success')
        self.password_var.set("")
        self.trigger_callback('login_success', user_data)
    
    def on_login_error(self, error_message: str):
        """Manejar error de login"""
        self.show_status(error_message, 'error')
        self.set_login_state(True)
        self.password_var.set("")
        self.password_entry.focus()
        self.trigger_callback('login_error', error_message)
    
    def reset_form(self):
        """Resetear formulario"""
        self.username_var.set("")
        self.password_var.set("")
        self.remember_var.set(False)
        self.clear_status()
        self.set_login_state(True)
        self.username_entry.focus()
    
    def load_remembered_user(self, username: str):
        """Cargar usuario recordado"""
        self.username_var.set(username)
        self.remember_var.set(True)
        self.password_entry.focus()
    
    def focus_username(self):
        """Enfocar campo de usuario"""
        self.username_entry.focus()
        self.username_entry.select_range(0, tk.END)
    
    def focus_password(self):
        """Enfocar campo de contraseña"""
        self.password_entry.focus()
        self.password_entry.select_range(0, tk.END)
    
    def get_form_data(self) -> dict:
        """Obtener datos del formulario"""
        return {
            'username': self.username_var.get().strip(),
            'password': self.password_var.get().strip(),
            'remember': self.remember_var.get()
        }
    
    def set_form_data(self, data: dict):
        """Establecer datos del formulario"""
        self.username_var.set(data.get('username', ''))
        self.password_var.set(data.get('password', ''))
        self.remember_var.set(data.get('remember', False))
    
    def bind_login_callback(self, callback: Callable):
        """Registrar callback de login"""
        self.bind_callback('login_attempt', callback)
    
    def bind_success_callback(self, callback: Callable):
        """Registrar callback de éxito"""
        self.bind_callback('login_success', callback)
    
    def bind_error_callback(self, callback: Callable):
        """Registrar callback de error"""
        self.bind_callback('login_error', callback)
    
    def on_close(self):
        """Manejar cierre de ventana"""
        if self.trigger_callback('before_close'):
            return
        
        self.root.quit()
        self.root.destroy()
    
    def show(self):
        """Mostrar ventana de login"""
        self.root.deiconify()
        self.root.lift()
        self.focus_username()
    
    def hide(self):
        """Ocultar ventana de login"""
        self.root.withdraw()
    
    def run(self):
        """Ejecutar loop principal"""
        self.focus_username()
        self.root.mainloop()
