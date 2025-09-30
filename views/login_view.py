import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from PIL import Image, ImageTk
from views.base_view import BaseView

class LoginView(BaseView):
    def __init__(self, parent, controller, auth_controller):
        super().__init__(parent)  # BaseView solo acepta parent
        self.controller = controller
        self.auth_controller = auth_controller
        self.logo_label = None  # Logo dinámico
        self.setup_ui()
        self.load_company_info()  # Cargar info de la empresa
        
    def setup_ui(self):
        # Configuración del estilo visual - fondo gris claro como en la imagen
        self.root.configure(bg='#f5f5f5')
        self.create_widgets()
        self.setup_layout()
        
    def create_widgets(self):
        # Marco para el logo (FUERA del cuadro blanco)
        logo_frame = tk.Frame(self.root, bg='#f5f5f5', width=140, height=140)
        logo_frame.pack_propagate(False)
        
        # Logo dinámico de la empresa - fondo azul con diamante
        self.logo_bg_frame = tk.Frame(logo_frame, bg='#2196f3', width=120, height=120)
        self.logo_bg_frame.pack_propagate(False)
        
        # Canvas para crear el rombo/diamante azul MÁS GRANDE
        logo_canvas = tk.Canvas(
            logo_frame,
            width=140,
            height=140,
            bg='#f5f5f5',
            highlightthickness=0
        )
        logo_canvas.pack()
        
        # Crear el diamante azul MÁS GRANDE
        points = [70, 20, 120, 70, 70, 120, 20, 70]  # Coordenadas del diamante más grande
        logo_canvas.create_polygon(points, fill='#2196f3', outline='#1976d2', width=2)
        
        # Signo de interrogación blanco en el centro MÁS GRANDE
        logo_canvas.create_text(70, 70, text='?', font=('Arial', 36, 'bold'), fill='white')
        
        # Almacenar canvas para poder actualizarlo después
        self.logo_canvas = logo_canvas
        
        # Logo dinámico (se posicionará encima del canvas si hay imagen)
        self.logo_label = tk.Label(
            logo_frame,
            text="",  # Inicialmente vacío
            font=('Segoe UI Emoji', 32),
            bg='#f5f5f5',
            fg='#2196f3'
        )
        
        # Título IPV (dinámico - FUERA del cuadro blanco)
        self.title_label = tk.Label(
            self.root,
            text="IPV",
            font=('Arial', 36, 'bold'),
            bg='#f5f5f5',
            fg='#2196f3'
        )
        
        # Subtítulo dinámico de la empresa (FUERA del cuadro blanco)
        self.company_label = tk.Label(
            self.root,
            text="Importadora Punto de Venta",
            font=('Arial', 20, 'bold'),
            bg='#f5f5f5',
            fg='#333333'
        )
        
        # Mensaje de bienvenida (FUERA del cuadro blanco)
        welcome_label = tk.Label(
            self.root,
            text="Inicia sesión para continuar",
            font=('Arial', 14),
            bg='#f5f5f5',
            fg='#666666'
        )
        
        # CUADRO BLANCO - Solo para campos de entrada
        self.login_frame = tk.Frame(self.root, bg='#ffffff', width=380, height=350, relief='solid', bd=1)
        self.login_frame.pack_propagate(False)
        
        # Campo de usuario con icono (DENTRO del cuadro blanco)
        user_frame = tk.Frame(self.login_frame, bg='#ffffff')
        
        user_icon_label = tk.Label(
            user_frame,
            text="👤 Usuario",
            font=('Arial', 12, 'bold'),
            bg='#ffffff',
            fg='#555555'
        )
        
        self.user_entry = tk.Entry(
            user_frame,
            font=('Arial', 12),
            width=32,
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
            font=('Arial', 12, 'bold'),
            bg='#ffffff',
            fg='#555555'
        )
        
        # Frame para contraseña y botón de mostrar
        password_input_frame = tk.Frame(password_frame, bg='#ffffff', relief='solid', bd=1)
        
        self.password_entry = tk.Entry(
            password_input_frame,
            font=('Arial', 12),
            width=28,
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
            font=('Arial', 12),
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
            font=('Arial', 11),
            bg='#ffffff',
            fg='#666666',
            selectcolor='#ffffff',
            activebackground='#ffffff',
            activeforeground='#2196f3',
            relief='flat'
        )
        
        # Botón de login (DENTRO del cuadro blanco)
        self.login_button = tk.Button(
            self.login_frame,
            text="🔓 Iniciar Sesión",
            font=('Arial', 13, 'bold'),
            bg='#2196f3',
            fg='white',
            width=32,
            height=2,
            cursor='hand2',
            relief='flat',
            bd=0,
            command=self.handle_login,
            activebackground='#1976d2',
            activeforeground='white'
        )
        
        # Footer (FUERA del cuadro blanco)
        footer_frame = tk.Frame(self.root, bg='#f5f5f5')
        
        help_label = tk.Label(
            footer_frame,
            text="¿Problemas para acceder? Contacta al administrador",
            font=('Arial', 10),
            bg='#f5f5f5',
            fg='#999999'
        )
        
        version_label = tk.Label(
            footer_frame,
            text="Sistema POS v1.0 • 2025",
            font=('Arial', 9),
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
    
    def setup_layout(self):
        # Layout NUEVO con elementos organizados correctamente
        
        # PARTE SUPERIOR (fuera del cuadro blanco)
        # Logo
        self.logo_frame.pack(pady=(30, 20))
        
        # Título IPV
        self.title_label.pack(pady=(0, 8))
        
        # Nombre de empresa  
        self.company_label.pack(pady=(0, 12))
        
        # Mensaje de bienvenida
        self.welcome_label.pack(pady=(0, 25))
        
        # CUADRO BLANCO CENTRADO con campos de entrada
        self.login_frame.pack(pady=(0, 25))
        
        # DENTRO del cuadro blanco:
        # Campo de usuario
        self.user_frame.pack(fill='x', padx=30, pady=(25, 15))
        self.user_icon_label.pack(anchor='w', pady=(0, 5))
        self.user_entry.pack(fill='x', ipady=8)
        
        # Campo de contraseña
        self.password_frame.pack(fill='x', padx=30, pady=(0, 15))
        self.password_icon_label.pack(anchor='w', pady=(0, 5))
        self.password_input_frame.pack(fill='x')
        self.password_entry.pack(side='left', fill='x', expand=True, ipady=8, padx=(8, 0))
        self.show_password_button.pack(side='right', padx=(0, 8))
        
        # Checkbox recordar
        self.remember_frame.pack(fill='x', padx=30, pady=(0, 20))
        self.remember_checkbox.pack(anchor='w')
        
        # Botón de login
        self.login_button.pack(padx=30, pady=(0, 25), fill='x', ipady=6)
        
        # PARTE INFERIOR (fuera del cuadro blanco)
        # Footer
        self.footer_frame.pack(fill='x', padx=30, pady=(0, 20))
        self.help_label.pack()
        self.version_label.pack(pady=(5, 0))
        
        # Focus inicial (después de que se cargue todo)
        self.root.after(100, lambda: self.user_entry.focus())
        
    def load_company_info(self):
        """Carga la información dinámica de la empresa desde la configuración"""
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'system_config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                # Actualizar nombre de empresa
                company_name = config.get('company_name', 'Importadora Punto de Venta')
                if company_name and company_name.strip():
                    self.company_label.config(text=company_name)
                    
                    # Actualizar iniciales (IPV por defecto)
                    initials = self.get_company_initials(company_name)
                    self.title_label.config(text=initials)
                
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
        """Intenta actualizar el logo de la empresa"""
        try:
            logo_path = config.get('logo_path', '')
            if logo_path and os.path.exists(logo_path) and 'no encontrado' not in logo_path:
                # Cargar y redimensionar imagen para el diamante MÁS GRANDE
                pil_image = Image.open(logo_path)
                pil_image = pil_image.resize((80, 80), Image.Resampling.LANCZOS)
                
                # Convertir a PhotoImage
                photo = ImageTk.PhotoImage(pil_image)
                
                # Limpiar el canvas y dibujar el diamante con la imagen
                self.logo_canvas.delete("all")
                
                # Crear el diamante azul MÁS GRANDE
                points = [70, 20, 120, 70, 70, 120, 20, 70]
                self.logo_canvas.create_polygon(points, fill='#2196f3', outline='#1976d2', width=2)
                
                # Colocar la imagen en el centro del diamante MÁS GRANDE
                self.logo_canvas.create_image(70, 70, image=photo)
                
                # Mantener referencia de la imagen
                self.logo_canvas.image = photo
                
                print(f"Logo actualizado: {logo_path}")
            else:
                print(f"Logo no disponible: {logo_path}")
                
        except Exception as e:
            print(f"Error actualizando logo: {e}")
    
    def _draw_default_logo(self):
        """Dibujar el logo por defecto (diamante con ?) MÁS GRANDE"""
        try:
            self.logo_canvas.delete("all")
            # Crear el diamante azul MÁS GRANDE
            points = [70, 20, 120, 70, 70, 120, 20, 70]
            self.logo_canvas.create_polygon(points, fill='#2196f3', outline='#1976d2', width=2)
            # Signo de interrogación blanco en el centro MÁS GRANDE
            self.logo_canvas.create_text(70, 70, text='?', font=('Arial', 36, 'bold'), fill='white')
        except Exception as e:
            print(f"Error dibujando logo por defecto: {e}")
    
    def handle_login(self):
        """Maneja el proceso de autenticación"""
        username = self.user_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validar que no sean los placeholders
        if username == "Ingresa tu usuario" or not username:
            messagebox.showerror("Error", "Por favor ingrese un usuario válido")
            self.user_entry.focus()
            return
            
        if not password:
            messagebox.showerror("Error", "Por favor ingrese su contraseña")
            self.password_entry.focus()
            return
        
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
            messagebox.showerror("Error", "Sistema de autenticación no disponible")
            self.password_entry.delete(0, tk.END)
            
    def update_company_info(self):
        """Método público para actualizar info de empresa (callback desde configuración)"""
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'system_config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                # Actualizar nombre de empresa
                company_name = config.get('company_name', 'Importadora Punto de Venta')
                if company_name and company_name.strip():
                    self.company_label.config(text=company_name)
                    
                    # Actualizar iniciales
                    initials = self.get_company_initials(company_name)
                    self.title_label.config(text=initials)
                
                # Actualizar logo
                logo_path = config.get('logo_path', '')
                if logo_path and os.path.exists(logo_path) and 'no encontrado' not in logo_path:
                    try:
                        # Cargar y redimensionar imagen para el diamante MÁS GRANDE
                        pil_image = Image.open(logo_path)
                        pil_image = pil_image.resize((80, 80), Image.Resampling.LANCZOS)
                        
                        # Convertir a PhotoImage
                        photo = ImageTk.PhotoImage(pil_image)
                        
                        # Limpiar el canvas y dibujar el diamante con la imagen
                        self.logo_canvas.delete("all")
                        
                        # Crear el diamante azul MÁS GRANDE
                        points = [70, 20, 120, 70, 70, 120, 20, 70]
                        self.logo_canvas.create_polygon(points, fill='#2196f3', outline='#1976d2', width=2)
                        
                        # Colocar la imagen en el centro del diamante MÁS GRANDE
                        self.logo_canvas.create_image(70, 70, image=photo)
                        
                        # Mantener referencia de la imagen
                        self.logo_canvas.image = photo
                        
                        print(f"Logo actualizado dinámicamente: {logo_path}")
                    except Exception as e:
                        print(f"Error actualizando logo dinámicamente: {e}")
                        # Volver al diamante por defecto
                        self._draw_default_logo()
                else:
                    # Volver al diamante por defecto si no hay logo válido
                    self._draw_default_logo()
                    
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
        messagebox.showinfo("Éxito", f"Bienvenido {user_data.get('username', 'Usuario')}")
        if hasattr(self, '_success_callback') and self._success_callback:
            self._success_callback(user_data)
    
    def on_login_error(self, error_message):
        """Manejar error de login"""
        messagebox.showerror("Error", error_message)
        self.password_entry.delete(0, tk.END)
        if hasattr(self, '_error_callback') and self._error_callback:
            self._error_callback(error_message)
    
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
