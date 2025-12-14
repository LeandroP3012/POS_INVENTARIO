import tkinter as tk
from tkinter import messagebox, ttk
import os
from PIL import Image, ImageTk
from views.base_view import BaseView
from utils.responsive_utils import ResponsiveManager
from utils.path_manager import get_config_path, load_config

class LoginView(BaseView):
    def __init__(self, parent, controller, auth_controller):
        super().__init__(parent)  # BaseView solo acepta parent
        self.controller = controller
        self.auth_controller = auth_controller
        self.logo_label = None  # Logo dinámico
        self.loading_animation = False  # Estado de animación
        self.loading_dots = 0  # Contador para animación
        
        # Inicializar gestor responsivo
        self.responsive = ResponsiveManager(self.root)
        self.ui_metrics = self._build_ui_metrics()
        self.fonts = self._build_font_config()
        
        self.setup_ui()
        self.load_company_info()  # Cargar info de la empresa

    def _build_ui_metrics(self):
        """Definir medidas según tipo de pantalla"""
        presets = {
            'small': {
                'window_width': 370,
                'window_height': 500,
                'min_width': 360,
                'min_height': 480,
                'form_width': 290,
                'form_height': 260,
                'entry_chars': 26,
                'button_chars': 26,
                'button_height': 2,
                'logo_size': 60,
                'company_font': 12,
                'welcome_font': 11,
                'label_font': 10,
                'input_font': 10,
                'button_font': 11,
                'status_font': 9,
                'footer_font': 8,
                'outer_top': 12,
                'outer_bottom': 12,
                'inner_padx': 16
            },
            'medium': {
                'window_width': 420,
                'window_height': 550,
                'min_width': 400,
                'min_height': 530,
                'form_width': 320,
                'form_height': 290,
                'entry_chars': 28,
                'button_chars': 28,
                'button_height': 2,
                'logo_size': 68,
                'company_font': 13,
                'welcome_font': 12,
                'label_font': 11,
                'input_font': 11,
                'button_font': 12,
                'status_font': 10,
                'footer_font': 9,
                'outer_top': 15,
                'outer_bottom': 15,
                'inner_padx': 19
            },
            'large': {
                'window_width': 470,
                'window_height': 600,
                'min_width': 450,
                'min_height': 580,
                'form_width': 360,
                'form_height': 320,
                'entry_chars': 32,
                'button_chars': 32,
                'button_height': 2,
                'logo_size': 78,
                'company_font': 14,
                'welcome_font': 12,
                'label_font': 12,
                'input_font': 12,
                'button_font': 13,
                'status_font': 11,
                'footer_font': 10,
                'outer_top': 16,
                'outer_bottom': 16,
                'inner_padx': 22
            },
            'xlarge': {
                'window_width': 500,
                'window_height': 620,
                'min_width': 480,
                'min_height': 600,
                'form_width': 380,
                'form_height': 340,
                'entry_chars': 34,
                'button_chars': 34,
                'button_height': 2,
                'logo_size': 82,
                'company_font': 15,
                'welcome_font': 13,
                'label_font': 12,
                'input_font': 12,
                'button_font': 13,
                'status_font': 11,
                'footer_font': 10,
                'outer_top': 18,
                'outer_bottom': 18,
                'inner_padx': 24
            }
        }
        screen_type = getattr(self.responsive, 'screen_type', 'medium')
        return presets.get(screen_type, presets['medium']).copy()

    def _build_font_config(self):
        """Configurar tipografías según métricas"""
        m = self.ui_metrics
        return {
            'company': ('Arial', m['company_font'], 'bold'),
            'welcome': ('Arial', m['welcome_font']),
            'label': ('Arial', m['label_font'], 'bold'),
            'input': ('Arial', m['input_font']),
            'button': ('Arial', m['button_font'], 'bold'),
            'status': ('Arial', m['status_font']),
            'footer': ('Arial', m['footer_font'])
        }
        
    def setup_ui(self):
        # Configuración del estilo visual - fondo gris claro como en la imagen
        self.root.configure(bg='#f5f5f5')
        
        metrics = self.ui_metrics
        width = metrics['window_width']
        height = metrics['window_height']
        
        self.root.geometry(f"{width}x{height}")
        
        # Centrar ventana de login
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Tamaño mínimo y máximo (login no debe redimensionarse)
        self.root.minsize(metrics['min_width'], metrics['min_height'])
        self.root.maxsize(metrics['window_width'], metrics['window_height'])
        self.root.resizable(False, False)
        
        self.create_widgets()
        self.setup_layout()
        
    def create_widgets(self):
        m = self.ui_metrics
        fonts = self.fonts
        inner_padx = m['inner_padx']
        
        # Marco para el logo (FUERA del cuadro blanco) - Tamaño FIJO original
        logo_frame = tk.Frame(self.root, bg='#f5f5f5', width=m['logo_size'] + 20, height=m['logo_size'] + 20)
        logo_frame.pack_propagate(False)
        
        # Logo dinámico de la empresa - fondo azul con diamante
        self.logo_bg_frame = tk.Frame(logo_frame, bg='#2196f3', width=m['logo_size'], height=m['logo_size'])
        self.logo_bg_frame.pack_propagate(False)
        
        # Logo dinámico simple - Tamaño FIJO original
        self.logo_label = tk.Label(
            logo_frame,
            text="🏪",  # Placeholder por defecto
            font=('Segoe UI Emoji', 24),
            bg='#f5f5f5',
            fg='#2196f3'
        )
        self.logo_label.pack(expand=True)
        
        # Título eliminado - ya no se muestra
        # self.title_label comentado
        
        # Subtítulo dinámico de la empresa - Fuente FIJA original
        self.company_label = tk.Label(
            self.root,
            text="Importadora Punto de Venta",
            font=fonts['company'],
            bg='#f5f5f5',
            fg='#333333'
        )
        
        # Mensaje de bienvenida - Fuente FIJA original
        welcome_label = tk.Label(
            self.root,
            text="Inicia sesión para continuar",
            font=fonts['welcome'],
            bg='#f5f5f5',
            fg='#666666'
        )
        
        # CUADRO BLANCO - Solo para campos de entrada (ampliado)
        self.login_frame = tk.Frame(self.root, bg='#ffffff', width=m['form_width'], height=m['form_height'], relief='solid', bd=1)
        self.login_frame.pack_propagate(False)
        
        # Campo de usuario con icono (DENTRO del cuadro blanco)
        user_frame = tk.Frame(self.login_frame, bg='#ffffff')
        
        user_icon_label = tk.Label(
            user_frame,
            text="👤 Usuario",
            font=fonts['label'],
            bg='#ffffff',
            fg='#555555'
        )
        
        self.user_entry = tk.Entry(
            user_frame,
            font=fonts['input'],
            width=m['entry_chars'],
            relief='solid',
            bd=1,
            bg='#ffffff',
            fg='#333333',
            insertbackground='#333333',
            highlightthickness=1,
            highlightcolor='#2196f3',
            highlightbackground='#e0e0e0'
        )
        self.user_entry.insert(0, "Ingresa tu usuario")
        self.user_entry.configure(fg='#aaaaaa')
        
        # Campo de contraseña con icono (DENTRO del cuadro blanco)
        password_frame = tk.Frame(self.login_frame, bg='#ffffff')
        
        password_icon_label = tk.Label(
            password_frame,
            text="🔒 Contraseña",
            font=fonts['label'],
            bg='#ffffff',
            fg='#555555'
        )
        
        # Frame para contraseña y botón de mostrar
        password_input_frame = tk.Frame(password_frame, bg='#ffffff', relief='solid', bd=1)
        
        self.password_entry = tk.Entry(
            password_input_frame,
            font=fonts['input'],
            width=max(m['entry_chars'] - 4, 24),
            show='*',
            relief='flat',
            bd=0,
            bg='#ffffff',
            fg='#333333',
            insertbackground='#333333'
        )
        
        # Botón para mostrar/ocultar contraseña
        self.show_password_button = tk.Button(
            password_input_frame,
            text="👁",
            font=fonts['input'],
            bg='#ffffff',
            fg='#999999',
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self.toggle_password_visibility,
            width=3
        )
        
        # Checkbox recordar datos (DENTRO del cuadro blanco)
        remember_frame = tk.Frame(self.login_frame, bg='#ffffff')
        
        self.remember_var = tk.BooleanVar()
        self.remember_checkbox = tk.Checkbutton(
            remember_frame,
            text="Recordar mis datos",
            variable=self.remember_var,
            font=('Arial', max(m['input_font'] - 1, 9)),
            bg='#ffffff',
            fg='#666666',
            selectcolor='#ffffff',
            activebackground='#ffffff',
            activeforeground='#2196f3',
            relief='flat'
        )
        
        # Botón de login (DENTRO del cuadro blanco) - Más ancho
        self.login_button = tk.Button(
            self.login_frame,
            text="🔓 Iniciar Sesión",
            font=fonts['button'],
            bg='#2196f3',
            fg='white',
            width=m['button_chars'],
            height=m['button_height'],
            cursor='hand2',
            relief='flat',
            bd=0,
            command=self.handle_login,
            activebackground='#1976d2',
            activeforeground='white'
        )
        
        # Mensaje de estado debajo del botón
        self.status_label = tk.Label(
            self.login_frame,
            text="",
            font=fonts['status'],
            bg='#ffffff',
            fg='#666666',
            wraplength=300,
            justify='center'
        )
        
        # Footer (FUERA del cuadro blanco)
        footer_frame = tk.Frame(self.root, bg='#f5f5f5')
        
        help_label = tk.Label(
            footer_frame,
            text="¿Problemas para acceder? Contacta al administrador",
            font=fonts['footer'],
            bg='#f5f5f5',
            fg='#999999'
        )
        
        version_label = tk.Label(
            footer_frame,
            text="Sistema POS v1.0 • 2025",
            font=('Arial', max(m['footer_font'] - 1, 8)),
            bg='#f5f5f5',
            fg='#cccccc'
        )
        
        # Asignar widgets a variables para layout
        self.logo_frame = logo_frame
        self.user_frame = user_frame
        self.password_frame = password_frame
        self.remember_frame = remember_frame
        self.footer_frame = footer_frame
        self.welcome_label = welcome_label
        self.user_icon_label = user_icon_label
        self.password_icon_label = password_icon_label
        self.password_input_frame = password_input_frame
        self.help_label = help_label
        self.version_label = version_label
        
        # Placeholder para usuario
        def on_user_focus_in(event):
            if self.user_entry.get() == "Ingresa tu usuario":
                self.user_entry.delete(0, tk.END)
                self.user_entry.configure(fg='#333333')
        
        def on_user_focus_out(event):
            if not self.user_entry.get():
                self.user_entry.insert(0, "Ingresa tu usuario")
                self.user_entry.configure(fg='#aaaaaa')
        
        self.user_entry.bind('<FocusIn>', on_user_focus_in)
        self.user_entry.bind('<FocusOut>', on_user_focus_out)
        
        # Configurar eventos de teclado
        self.password_entry.bind('<Return>', lambda event: self.handle_login())
        self.user_entry.bind('<Return>', lambda event: self.password_entry.focus())
    
    def toggle_password_visibility(self):
        """Alternar visibilidad de la contraseña"""
        if self.password_entry.cget('show') == '*':
            self.password_entry.config(show='')
            self.show_password_button.config(text='🙈')
        else:
            self.password_entry.config(show='*')
            self.show_password_button.config(text='👁')
    
    def show_status_message(self, message, msg_type="info"):
        """Mostrar mensaje de estado debajo del botón"""
        color_map = {
            "success": "#4caf50",  # Verde
            "error": "#f44336",    # Rojo
            "info": "#2196f3",     # Azul
            "warning": "#ff9800"   # Naranja
        }
        
        self.status_label.config(
            text=message,
            fg=color_map.get(msg_type, "#666666")
        )
        # Forzar actualización visual
        self.status_label.update()
    
    def clear_status_message(self):
        """Limpiar mensaje de estado"""
        self.status_label.config(text="")
    
    def start_loading_animation(self):
        """Iniciar animación de carga en el botón"""
        self.login_button.config(
            text="⏳ Iniciando sesión...",
            state="disabled",
            bg="#1976d2",
            cursor="wait"
        )
        self.show_status_message("Verificando credenciales...", "info")
        
        # Animación de puntos
        self.loading_dots = 0
        self.loading_animation = True
        self.animate_loading()
    
    def animate_loading(self):
        """Animar los puntos de carga"""
        if self.loading_animation:
            dots = "." * (self.loading_dots % 4)
            self.login_button.config(text=f"⏳ Iniciando sesión{dots}")
            self.loading_dots += 1
            # Continuar animación más lenta para que se aprecie mejor
            self.root.after(700, self.animate_loading)
    
    def stop_loading_animation(self):
        """Detener animación de carga"""
        self.loading_animation = False
        self.login_button.config(
            text="🔓 Iniciar Sesión",
            state="normal",
            bg="#2196f3",
            cursor="hand2"
        )
    
    def setup_layout(self):
        # Layout OPTIMIZADO con espaciados reducidos
        m = self.ui_metrics
        inner_padx = m['inner_padx']
        outer_top = m['outer_top']
        outer_bottom = m['outer_bottom']
        
        # PARTE SUPERIOR (fuera del cuadro blanco)
        # Logo
        self.logo_frame.pack(pady=(outer_top, 10))
        
        # Nombre de empresa (sin título de iniciales)
        self.company_label.pack(pady=(0, 6))
        
        # Mensaje de bienvenida
        self.welcome_label.pack(pady=(0, 12))
        
        # CUADRO BLANCO CENTRADO con campos de entrada
        self.login_frame.pack(pady=(0, 12))
        
        # DENTRO del cuadro blanco - ESPACIADOS COMPACTOS:
        # Campo de usuario
        self.user_frame.pack(fill='x', padx=inner_padx, pady=(18, 10))
        self.user_icon_label.pack(anchor='w', pady=(0, 4))
        self.user_entry.pack(fill='x', ipady=6)
        
        # Campo de contraseña
        self.password_frame.pack(fill='x', padx=inner_padx, pady=(0, 10))
        self.password_icon_label.pack(anchor='w', pady=(0, 4))
        self.password_input_frame.pack(fill='x')
        self.password_entry.pack(side='left', fill='x', expand=True, ipady=6, padx=(6, 0))
        self.show_password_button.pack(side='right', padx=(0, 6))
        
        # Checkbox recordar
        self.remember_frame.pack(fill='x', padx=inner_padx, pady=(0, 12))
        self.remember_checkbox.pack(anchor='w')
        
        # Botón de login
        self.login_button.pack(padx=inner_padx, pady=(0, 8), fill='x', ipady=4)
        
        # Mensaje de estado
        self.status_label.pack(padx=inner_padx, pady=(0, 10))
        
        # PARTE INFERIOR (fuera del cuadro blanco)
        # Footer
        self.footer_frame.pack(fill='x', padx=inner_padx + 5, pady=(0, outer_bottom))
        self.help_label.pack()
        self.version_label.pack(pady=(5, 0))
        
        # Focus inicial (después de que se cargue todo)
        self.root.after(100, lambda: self.user_entry.focus())
        
    def load_company_info(self):
        """Carga la información dinámica de la empresa desde la configuración"""
        try:
            # Usar PathManager para obtener la ruta correcta
            config = load_config('system_config.json')
            
            if config:
                # Actualizar nombre de empresa
                company_name = config.get('company_name', 'Importadora Punto de Venta')
                if company_name and company_name.strip():
                    self.company_label.config(text=company_name)
                    # Ya no mostramos iniciales
                
                # Actualizar logo
                self.try_update_logo(config)
                    
        except Exception as e:
            print(f"Error cargando configuración de empresa: {e}")
    
    def get_company_initials(self, company_name):
        """Obtener iniciales del nombre de la empresa"""
        try:
            words = company_name.upper().split()
            if len(words) >= 3:
                # Si tiene 3 o más palabras, tomar las primeras 3 iniciales
                return ''.join([word[0] for word in words[:3]])
            elif len(words) == 2:
                # Si tiene 2 palabras, tomar ambas iniciales
                return ''.join([word[0] for word in words])
            elif len(words) == 1:
                # Si tiene 1 palabra, tomar las primeras 3 letras
                return words[0][:3]
            else:
                return "IPV"  # Fallback
        except:
            return "IPV"  # Fallback en caso de error
    
    def try_update_logo(self, config):
        """Intenta actualizar el logo de la empresa (solo imagen, sin diamante)"""
        try:
            logo_path = config.get('logo_path', '')
            if logo_path and os.path.exists(logo_path) and 'no encontrado' not in logo_path:
                # Cargar y redimensionar imagen - TAMAÑO REDUCIDO
                pil_image = Image.open(logo_path)
                pil_image = pil_image.resize((80, 80), Image.Resampling.LANCZOS)
                
                # Convertir a PhotoImage
                photo = ImageTk.PhotoImage(pil_image)
                
                # Actualizar directamente el label con la imagen
                self.logo_label.config(image=photo, text="")
                self.logo_label.image = photo  # Mantener referencia
                
                print(f"Logo actualizado: {logo_path}")
            else:
                print(f"Logo no disponible: {logo_path}")
                # Mantener emoji por defecto
                self.logo_label.config(image="", text="🏪")
                
        except Exception as e:
            print(f"Error actualizando logo: {e}")
            # Volver al emoji por defecto en caso de error
            self.logo_label.config(image="", text="🏪")
    
    def handle_login(self):
        """Maneja el proceso de autenticación"""
        username = self.user_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Limpiar mensaje de estado anterior
        self.clear_status_message()
        
        # Validar que no sean los placeholders
        if username == "Ingresa tu usuario" or not username:
            self.show_status_message("Por favor ingrese un usuario válido", "error")
            self.user_entry.focus()
            return
            
        if not password:
            self.show_status_message("Por favor ingrese su contraseña", "error")
            self.password_entry.focus()
            return
        
        # Iniciar animación de carga
        self.loading_animation = True
        self.start_loading_animation()
        
        # Crear datos del formulario
        form_data = {
            'username': username,
            'password': password,
            'remember': self.remember_var.get()  # Usar el valor del checkbox
        }
        
        # Llamar al callback de login si existe
        if hasattr(self, '_login_callback') and self._login_callback:
            self._login_callback(form_data)
        else:
            # Fallback simple - solo para compatibilidad
            self.stop_loading_animation()
            self.show_status_message("Sistema de autenticación no disponible", "error")
            self.password_entry.delete(0, tk.END)
            
    def update_company_info(self):
        """Método público para actualizar info de empresa (callback desde configuración)"""
        try:
            config_path = get_config_path('system_config.json')
            config = load_config('system_config.json') or {}

            if config_path.exists() and config:
                # Actualizar nombre de empresa
                company_name = config.get('company_name', 'Importadora Punto de Venta')
                if company_name and company_name.strip():
                    self.company_label.config(text=company_name)

                # Actualizar logo (solo imagen, sin diamante)
                self.try_update_logo(config)
            else:
                print(f"system_config.json no encontrado en: {config_path}")
                    
        except Exception as e:
            print(f"Error en update_company_info: {e}")
    
    # Métodos para compatibilidad con AuthController
    def bind_login_callback(self, callback):
        """Vincular callback de intento de login"""
        self._login_callback = callback
    
    def bind_success_callback(self, callback):
        """Vincular callback de éxito"""
        self._success_callback = callback
    
    def bind_error_callback(self, callback):
        """Vincular callback de error"""
        self._error_callback = callback
    
    def bind_callback(self, event_name, callback):
        """Vincular callback genérico"""
        setattr(self, f'_{event_name}_callback', callback)
    
    def reset_form(self):
        """Limpiar formulario"""
        self.user_entry.delete(0, tk.END)
        self.user_entry.insert(0, "Ingresa tu usuario")
        self.user_entry.configure(fg='#aaaaaa')
        self.password_entry.delete(0, tk.END)
        self.remember_var.set(False)
        self.clear_status_message()
        self.stop_loading_animation()
        self.user_entry.focus()
    
    def show(self):
        """Mostrar ventana"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
    
    def hide(self):
        """Ocultar ventana"""
        self.root.withdraw()
    
    def run(self):
        """Ejecutar loop principal"""
        self.root.mainloop()
    
    def on_login_success(self, user_data):
        """Manejar éxito de login"""
        self.stop_loading_animation()
        username = user_data.get('username', 'Usuario')
        self.show_status_message(f"✅ ¡Bienvenido {username}! Accediendo al sistema...", "success")
        
        # Pequeña pausa para mostrar el mensaje antes de proceder
        self.root.after(1500, lambda: self._proceed_with_success(user_data))
    
    def on_login_error(self, error_message):
        """Manejar error de login"""
        self.stop_loading_animation()
        self.show_status_message(f"❌ {error_message}", "error")
        self.password_entry.delete(0, tk.END)
        self.password_entry.focus()
        
        if hasattr(self, '_error_callback') and self._error_callback:
            self._error_callback(error_message)
    
    def _proceed_with_success(self, user_data):
        """Proceder con el éxito después de mostrar el mensaje"""
        # Este método ahora no hace nada porque el auth_controller maneja la transición
        # El auth_controller espera 3 segundos antes de proceder
        pass
    
    def load_remembered_user(self, username):
        """Cargar usuario recordado"""
        self.user_entry.delete(0, tk.END)
        self.user_entry.insert(0, username)
        self.user_entry.configure(fg='#333333')
        self.remember_var.set(True)
        self.password_entry.focus()
    
    def on_destroy(self):
        """Limpiar recursos"""
        self.root.destroy()
