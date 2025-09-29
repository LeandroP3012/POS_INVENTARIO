"""
Vista de Login para el Sistema POS
Interfaz de autenticación con diseñ        # Logo provisional de la empresa
        logo_label = tk.Label(
            logo_bg,
            text="🏪",
            font=('Arial', 35),
            bg='#ffffff',
            fg='#1976d2'
        )
        logo_label.place(relx=0.5, rely=0.5, anchor='center')
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
        self.root.geometry("480x700")  # Tamaño optimizado y consistente
        self.root.resizable(False, False)
        
        # Gradiente de fondo moderno
        self.root.configure(bg='#f0f2f5')
        
        # Centrar ventana - DIMENSIONES CONSISTENTES
        self.center_window(self.root, 480, 800)
        
        # Configurar protocolo de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_login_form(self):
        """Crear formulario de login"""
        # Frame principal directo (sin canvas para evitar problemas de layout)
        main_frame = tk.Frame(self.root, bg='#f0f2f5')
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header con logo y título
        self.create_header(main_frame)
        
        # Formulario
        self.create_form(main_frame)
        
        # Footer
        self.create_footer(main_frame)
    
    def create_header(self, parent):
        """Crear header con logo y título"""
        header_frame = tk.Frame(parent, bg='#f0f2f5')
        header_frame.pack(fill='x', pady=(0, 15))  # Reducido de 30 a 15
        
        # Logo moderno con efecto sombra
        logo_frame = tk.Frame(header_frame, bg='#f0f2f5')
        logo_frame.pack(pady=(0, 10))  # Reducido de 20 a 10
        
        # Marco circular para el logo
        logo_bg = tk.Frame(logo_frame, bg='#ffffff', width=80, height=80)
        logo_bg.pack_propagate(False)
        logo_bg.pack()
        
        # Logo provisional de la empresa
        logo_label = tk.Label(
            logo_bg,
            text="�",
            font=('Segoe UI Emoji', 40),
            bg='#ffffff',
            fg='#1976d2'
        )
        logo_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Logo adicional en texto (provisional)
        logo_text_frame = tk.Frame(header_frame, bg='#f0f2f5')
        logo_text_frame.pack(pady=(5, 0))  # Reducido de 10 a 5
        
        logo_text = tk.Label(
            logo_text_frame,
            text="IPV",
            font=('Segoe UI', 18, 'bold'),  # Reducido de 24 a 18
            bg='#f0f2f5',
            fg='#1976d2'
        )
        logo_text.pack()
        
        # Título principal con estilo moderno
        title_label = tk.Label(
            header_frame,
            text="Importadora Punto de Venta",
            font=('Segoe UI', 16, 'bold'),  # Reducido de 22 a 16
            bg='#f0f2f5',
            fg="#1d2336"
        )
        title_label.pack(pady=(5, 0))  # Reducido padding
        
        # Subtítulo elegante
        subtitle_label = tk.Label(
            header_frame,
            text="Inicia sesión para continuar",
            font=('Segoe UI', 12),
            bg='#f0f2f5',
            fg='#666666'
        )
        subtitle_label.pack()
    
    def create_form(self, parent):
        """Crear formulario de login"""
        # Frame con sombra y bordes redondeados simulados
        form_frame = tk.Frame(parent, bg='#ffffff', relief='flat', bd=0)
        form_frame.pack(fill='x', pady=(10, 15), padx=20)  # Reducido pady
        
        # Simular sombra con frame de fondo
        shadow_frame = tk.Frame(parent, bg='#e0e0e0', height=2)
        shadow_frame.pack(fill='x', padx=22, pady=(0, 2))
        
        # Padding interno
        inner_frame = tk.Frame(form_frame, bg='#ffffff')
        inner_frame.pack(fill='both', expand=True, padx=25, pady=20)  # Reducido más el padding
        
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
        field_frame = tk.Frame(parent, bg='#ffffff')
        field_frame.pack(fill='x', pady=(0, 15))  # Reducido de 25 a 15
        
        # Etiqueta con icono
        label_frame = tk.Frame(field_frame, bg='#ffffff')
        label_frame.pack(fill='x', pady=(0, 8))
        
        username_label = tk.Label(
            label_frame,
            text="👤 Usuario",
            font=('Segoe UI', 11, 'bold'),
            bg='#ffffff',
            fg='#333333'
        )
        username_label.pack(anchor='w')
        
        # Frame para entrada con borde personalizado
        entry_frame = tk.Frame(field_frame, bg='#f8f9fa', relief='solid', bd=1)
        entry_frame.pack(fill='x', ipady=2)
        
        self.username_entry = tk.Entry(
            entry_frame,
            textvariable=self.username_var,
            font=('Segoe UI', 11),
            bg='#f8f9fa',
            fg='#333333',
            bd=0,
            relief='flat'
        )
        self.username_entry.pack(fill='x', padx=15, pady=12)
        
        # Bind eventos de navegación
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        
        # Efectos de foco visuales (se agregan después de los placeholders)
        self.username_entry.bind('<FocusIn>', lambda e: self.on_entry_focus_in(entry_frame), add='+')
        self.username_entry.bind('<FocusOut>', lambda e: self.on_entry_focus_out(entry_frame), add='+')
        
        # Agregar placeholder después de los eventos visuales
        self.add_custom_placeholder(self.username_entry, "Ingresa tu usuario")
    
    def create_password_field(self, parent):
        """Crear campo de contraseña"""
        field_frame = tk.Frame(parent, bg='#ffffff')
        field_frame.pack(fill='x', pady=(0, 15))  # Reducido de 25 a 15
        
        # Etiqueta con icono
        label_frame = tk.Frame(field_frame, bg='#ffffff')
        label_frame.pack(fill='x', pady=(0, 8))
        
        password_label = tk.Label(
            label_frame,
            text="🔒 Contraseña",
            font=('Segoe UI', 11, 'bold'),
            bg='#ffffff',
            fg='#333333'
        )
        password_label.pack(anchor='w')
        
        # Frame principal para entrada
        main_entry_frame = tk.Frame(field_frame, bg='#f8f9fa', relief='solid', bd=1)
        main_entry_frame.pack(fill='x', ipady=2)
        
        # Frame interno para entrada y botón
        entry_frame = tk.Frame(main_entry_frame, bg='#f8f9fa')
        entry_frame.pack(fill='x', padx=15, pady=12)
        
        self.password_entry = tk.Entry(
            entry_frame,
            textvariable=self.password_var,
            font=('Segoe UI', 11),
            bg='#f8f9fa',
            fg='#333333',
            bd=0,
            relief='flat',
            show='*'
        )
        self.password_entry.pack(side='left', fill='x', expand=True)
        
        # Botón mostrar/ocultar contraseña
        show_button = tk.Button(
            entry_frame,
            text="👁",
            font=('Segoe UI', 10),
            bg='#f8f9fa',
            fg='#666666',
            bd=0,
            relief='flat',
            cursor='hand2',
            command=self.toggle_password_visibility
        )
        show_button.pack(side='right', padx=(10, 0))
        
        # Bind eventos de navegación
        self.password_entry.bind('<Return>', lambda e: self.attempt_login())
        
        # Efectos de foco visuales (se agregan después de los placeholders)
        self.password_entry.bind('<FocusIn>', lambda e: self.on_entry_focus_in(main_entry_frame), add='+')
        self.password_entry.bind('<FocusOut>', lambda e: self.on_entry_focus_out(main_entry_frame), add='+')
        
        # Agregar placeholder después de los eventos visuales
        self.add_custom_placeholder(self.password_entry, "Ingresa tu contraseña")
    
    def create_remember_checkbox(self, parent):
        """Crear checkbox de recordar"""
        remember_frame = tk.Frame(parent, bg='#ffffff')
        remember_frame.pack(fill='x', pady=(0, 20))  # Reducido de 30 a 20
        
        remember_check = tk.Checkbutton(
            remember_frame,
            text="Recordar mis datos",
            variable=self.remember_var,
            font=('Segoe UI', 10),
            bg='#ffffff',
            fg='#666666',
            activebackground='#ffffff',
            activeforeground='#1976d2',
            selectcolor='#ffffff',
            cursor='hand2'
        )
        remember_check.pack(anchor='w')
    
    def create_login_button(self, parent):
        """Crear botones de login"""
        buttons_frame = tk.Frame(parent, bg='#ffffff')
        buttons_frame.pack(fill='x', pady=(0, 25))
        
        # Botón principal de login - OPTIMIZADO
        self.login_button = tk.Button(
            buttons_frame,
            text="🔐 Iniciar Sesión",
            font=('Segoe UI', 11, 'bold'),  # Reducido de 14 a 11
            bg='#1976d2',
            fg='white',
            activebackground='#1565c0',
            activeforeground='white',
            relief='raised',
            bd=2,  # Reducido de 3 a 2
            cursor='hand2',
            command=self.attempt_login,
            width=20,  # Reducido de 25 a 20
            height=1   # Reducido de 2 a 1
        )
        self.login_button.pack(fill='x', ipady=12, pady=8)  # Reducido padding
        
        # Efectos hover para botón principal
        self.login_button.bind('<Enter>', lambda e: self.login_button.configure(bg='#1565c0'))
        self.login_button.bind('<Leave>', lambda e: self.login_button.configure(bg='#1976d2'))
    
    def create_status_label(self, parent):
        """Crear label de estado"""
        self.status_label = tk.Label(
            parent,
            text="",
            font=('Segoe UI', 10),
            bg='#ffffff',
            fg='#d32f2f',
            wraplength=300,
            justify='center'
        )
        self.status_label.pack(fill='x', pady=(10, 0))
    
    def create_footer(self, parent):
        """Crear footer con información adicional"""
        footer_frame = tk.Frame(parent, bg='#f0f2f5')
        footer_frame.pack(fill='x', pady=(10, 0))  # Reducido de 20 a 10
        
        # Línea separadora sutil
        separator = tk.Frame(footer_frame, bg='#e0e0e0', height=1)
        separator.pack(fill='x', pady=(0, 15))
        
        help_label = tk.Label(
            footer_frame,
            text="¿Problemas para acceder? Contacta al administrador",
            font=('Segoe UI', 9),
            bg='#f0f2f5',
            fg='#888888'
        )
        help_label.pack(pady=(0, 8))
        
        version_label = tk.Label(
            footer_frame,
            text="Sistema POS v1.0 • 2025",
            font=('Segoe UI', 8),
            bg='#f0f2f5',
            fg='#aaaaaa'
        )
        version_label.pack()
    

    
    def add_custom_placeholder(self, entry, placeholder: str):
        """Agregar placeholder personalizado a un Entry de tkinter"""
        # Marcar el entry con el placeholder para identificarlo
        entry.placeholder_text = placeholder
        
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.configure(fg='#333333')
                if entry == self.password_entry:
                    entry.configure(show='*')
        
        def on_focus_out(event):
            if not entry.get().strip():
                entry.delete(0, tk.END)  # Limpiar primero
                entry.insert(0, placeholder)
                entry.configure(fg='#999999')
                if entry == self.password_entry:
                    entry.configure(show='')
        
        # Establecer placeholder inicial
        entry.delete(0, tk.END)
        entry.insert(0, placeholder)
        entry.configure(fg='#999999')
        if entry == self.password_entry:
            entry.configure(show='')
        
        # Bind eventos de placeholder (estos se ejecutan primero)
        entry.bind('<FocusIn>', on_focus_in, add='+')
        entry.bind('<FocusOut>', on_focus_out, add='+')
    
    def on_entry_focus_in(self, entry_frame):
        """Efecto visual cuando el campo recibe foco"""
        entry_frame.configure(relief='solid', bd=2)
        entry_frame.configure(bg='#ffffff')
    
    def on_entry_focus_out(self, entry_frame):
        """Efecto visual cuando el campo pierde foco"""
        entry_frame.configure(relief='solid', bd=1)
        entry_frame.configure(bg='#f8f9fa')
    
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
        
        # Verificar si los campos contienen solo placeholders
        if not username or username == "Ingresa tu usuario":
            self.show_status("Por favor ingresa tu usuario", 'error')
            self.username_entry.focus()
            return
        
        if not password or password == "Ingresa tu contraseña":
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
            'info': '#1976d2',
            'error': '#d32f2f',
            'success': '#388e3c',
            'warning': '#f57c00'
        }
        
        self.status_label.configure(
            text=message,
            fg=colors.get(status_type, '#333333')
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
            self.login_button.configure(
                text="🔐 Iniciar Sesión",
                bg='#1976d2'
            )
        else:
            self.login_button.configure(
                text="⏳ Verificando...",
                bg='#999999'
            )
    
    def on_login_success(self, user_data: dict):
        """Manejar login exitoso"""
        self.show_status(f"¡Bienvenido {user_data.get('full_name', user_data.get('username'))}!", 'success')
        self.password_var.set("")
        self.trigger_callback('login_success', user_data)
    
    def on_login_error(self, error_message: str):
        """Manejar error de login"""
        self.show_status(error_message, 'error')
        self.set_login_state(True)
        
        # Limpiar solo la contraseña y restaurar placeholder
        self.password_var.set("")
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, "Ingresa tu contraseña")
        self.password_entry.configure(fg='#999999', show='')
        
        self.password_entry.focus()
        self.trigger_callback('login_error', error_message)
    
    def reset_form(self):
        """Resetear formulario completamente"""
        # Limpiar variables
        self.username_var.set("")
        self.password_var.set("")
        self.remember_var.set(False)
        
        # Limpiar campos y restaurar placeholders
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, "Ingresa tu usuario")
        self.username_entry.configure(fg='#999999')
        
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, "Ingresa tu contraseña")
        self.password_entry.configure(fg='#999999', show='')
        
        # Limpiar estado
        self.clear_status()
        self.set_login_state(True)
        
        # Enfocar campo de usuario
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
