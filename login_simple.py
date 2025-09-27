#!/usr/bin/env python3
"""
Sistema POS - Interfaz de Login Simple
Versión inicial con tipos de usuario
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import hashlib
import platform
import datetime

class LoginApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏪 Sistema POS - Login")
        # Hacer que ocupe toda la pantalla
        self.root.state('zoomed')  # Para Windows
        self.root.configure(bg='#2c3e50')
        self.root.resizable(True, True)
        
        # Usuarios de prueba (simulados, sin base de datos)
        self.usuarios = {
            'admin': {
                'password': self.hash_password('123'),
                'tipo': 'administrador',
                'nombre_completo': 'Administrador del Sistema'
            },
            'usuario1': {
                'password': self.hash_password('123'),
                'tipo': 'usuario',
                'nombre_completo': 'Usuario Normal'
            }
        }
        
        self.crear_interfaz()
        
    def centrar_ventana(self):
        """Centrar la ventana en la pantalla"""
        self.root.update_idletasks()
        ancho = 400
        alto = 450
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')
        
    def hash_password(self, password):
        """Crear hash SHA-256 de la contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
        
    def crear_interfaz(self):
        """Crear la interfaz de usuario del login"""
        
        # Header/Título
        frame_titulo = tk.Frame(self.root, bg='#34495e', height=100)
        frame_titulo.pack(fill='x')
        frame_titulo.pack_propagate(False)
        
        titulo = tk.Label(
            frame_titulo,
            text="🏪 SISTEMA POS - COMERCIO ELECTRÓNICO",
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#34495e'
        )
        titulo.pack(expand=True)
        
        # Frame contenedor principal (para centrar el formulario)
        frame_contenedor = tk.Frame(self.root, bg='#2c3e50')
        frame_contenedor.pack(fill='both', expand=True)
        
        # Frame principal del formulario (centrado)
        frame_formulario = tk.Frame(frame_contenedor, bg='#ecf0f1', relief='raised', bd=2)
        frame_formulario.place(relx=0.5, rely=0.5, anchor='center', width=500, height=600)
        
        # Título del login
        tk.Label(
            frame_formulario,
            text="🔐 INICIAR SESIÓN",
            font=('Arial', 20, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(pady=(30, 40))
        
        # Campo Usuario
        tk.Label(
            frame_formulario,
            text="👤 Usuario:",
            font=('Arial', 14, 'bold'),
            fg='#34495e',
            bg='#ecf0f1'
        ).pack(anchor='w', padx=50)
        
        self.entry_usuario = tk.Entry(
            frame_formulario,
            font=('Arial', 12),
            width=35,
            bd=2,
            relief='groove'
        )
        self.entry_usuario.pack(pady=(5, 20), ipady=8, padx=50)
        self.entry_usuario.focus()
        
        # Campo Contraseña
        tk.Label(
            frame_formulario,
            text="🔐 Contraseña:",
            font=('Arial', 14, 'bold'),
            fg='#34495e',
            bg='#ecf0f1'
        ).pack(anchor='w', padx=50)
        
        self.entry_password = tk.Entry(
            frame_formulario,
            font=('Arial', 12),
            width=35,
            show='*',
            bd=2,
            relief='groove'
        )
        self.entry_password.pack(pady=(5, 25), ipady=8, padx=50)
        
        # Selector de tipo de usuario
        tk.Label(
            frame_formulario,
            text="👥 Tipo de Usuario:",
            font=('Arial', 14, 'bold'),
            fg='#34495e',
            bg='#ecf0f1'
        ).pack(anchor='w', padx=50)
        
        self.tipo_usuario = tk.StringVar(value="usuario")
        
        frame_radio = tk.Frame(frame_formulario, bg='#ecf0f1')
        frame_radio.pack(pady=(5, 30), padx=50, anchor='w')
        
        tk.Radiobutton(
            frame_radio,
            text="👤 Usuario Normal",
            variable=self.tipo_usuario,
            value="usuario",
            font=('Arial', 12),
            bg='#ecf0f1',
            fg='#27ae60'
        ).pack(anchor='w')
        
        tk.Radiobutton(
            frame_radio,
            text="👑 Administrador",
            variable=self.tipo_usuario,
            value="administrador",
            font=('Arial', 12),
            bg='#ecf0f1',
            fg='#e74c3c'
        ).pack(anchor='w', pady=(10, 0))
        
        # Botón de Login
        btn_login = tk.Button(
            frame_formulario,
            text="🔐 INICIAR SESIÓN",
            font=('Arial', 14, 'bold'),
            bg='#3498db',
            fg='white',
            width=30,
            height=2,
            relief='flat',
            command=self.procesar_login
        )
        btn_login.pack(pady=20, padx=50)
        
        # Información de usuarios de prueba
        frame_info = tk.LabelFrame(
            frame_formulario, 
            text="👥 Usuarios de Prueba", 
            font=('Arial', 11, 'bold'),
            bg='#ecf0f1',
            fg='#34495e'
        )
        frame_info.pack(fill='x', pady=(20, 20), padx=50)
        
        tk.Label(
            frame_info,
            text="👑 admin / 123 (Administrador)",
            font=('Arial', 11),
            fg='#7f8c8d',
            bg='#ecf0f1'
        ).pack(pady=5)
        
        tk.Label(
            frame_info,
            text="👤 usuario1 / 123 (Usuario Normal)",
            font=('Arial', 11),
            fg='#7f8c8d',
            bg='#ecf0f1'
        ).pack(pady=5)
        
        # Bind Enter para login
        self.root.bind('<Return>', lambda e: self.procesar_login())
        
    def procesar_login(self):
        """Procesar el intento de login"""
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get()
        tipo_seleccionado = self.tipo_usuario.get()
        
        # Validaciones
        if not usuario:
            messagebox.showerror("Error", "Por favor ingrese el nombre de usuario")
            self.entry_usuario.focus()
            return
            
        if not password:
            messagebox.showerror("Error", "Por favor ingrese la contraseña")
            self.entry_password.focus()
            return
        
        # Verificar si el usuario existe
        if usuario not in self.usuarios:
            messagebox.showerror("Error", "Usuario no encontrado")
            self.limpiar_campos()
            return
        
        datos_usuario = self.usuarios[usuario]
        
        # Verificar contraseña
        if datos_usuario['password'] != self.hash_password(password):
            messagebox.showerror("Error", "Contraseña incorrecta")
            self.entry_password.delete(0, tk.END)
            self.entry_password.focus()
            return
        
        # Verificar tipo de usuario
        if datos_usuario['tipo'] != tipo_seleccionado:
            messagebox.showerror(
                "Error", 
                f"Este usuario es de tipo '{datos_usuario['tipo']}'\n"
                f"Seleccione '{datos_usuario['tipo']}' e intente nuevamente"
            )
            return
        
        # Login exitoso
        self.login_exitoso(usuario, datos_usuario)
        
    def login_exitoso(self, usuario, datos_usuario):
        """Manejar login exitoso"""
        messagebox.showinfo(
            "Login Exitoso", 
            f"¡Bienvenido!\n\n"
            f"Usuario: {datos_usuario['nombre_completo']}\n"
            f"Tipo: {datos_usuario['tipo'].title()}"
        )
        
        # Cerrar ventana de login
        self.root.destroy()
        
        # Abrir interfaz correspondiente según el tipo de usuario
        if datos_usuario['tipo'] == 'administrador':
            PanelAdministrador(usuario, datos_usuario)
        else:
            PanelUsuario(usuario, datos_usuario)
            
    def limpiar_campos(self):
        """Limpiar los campos de entrada"""
        self.entry_usuario.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_usuario.focus()

class PanelAdministrador:
    """Panel de administrador con funciones completas"""
    
    def __init__(self, usuario, datos_usuario):
        self.usuario = usuario
        self.datos_usuario = datos_usuario
        
        self.root = tk.Tk()
        self.root.title(f"🏪 Sistema POS - Panel Administrador ({datos_usuario['nombre_completo']})")
        # Hacer que ocupe toda la pantalla
        self.root.state('zoomed')  # Para Windows
        self.root.configure(bg='#ecf0f1')
        self.crear_interfaz()
        self.root.mainloop()
        
    def centrar_ventana(self):
        """Centrar ventana"""
        self.root.update_idletasks()
        ancho = 800
        alto = 600
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')
        
    def crear_interfaz(self):
        """Crear interfaz del panel de administrador con navbar"""
        
        # Header Principal
        frame_header = tk.Frame(self.root, bg='#2c3e50', height=80)
        frame_header.pack(fill='x')
        frame_header.pack_propagate(False)
        
        # Logo y título
        header_left = tk.Frame(frame_header, bg='#2c3e50')
        header_left.pack(side='left', fill='y', padx=20)
        
        tk.Label(
            header_left,
            text="🏪 SISTEMA POS",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        ).pack(anchor='w', pady=(10, 0))
        
        tk.Label(
            header_left,
            text=f"👑 Administrador: {self.datos_usuario['nombre_completo']}",
            font=('Arial', 11),
            fg='#bdc3c7',
            bg='#2c3e50'
        ).pack(anchor='w')
        
        # Información del usuario y logout
        header_right = tk.Frame(frame_header, bg='#2c3e50')
        header_right.pack(side='right', fill='y', padx=20)
        
        tk.Label(
            header_right,
            text=f"📅 {datetime.datetime.now().strftime('%d/%m/%Y')}",
            font=('Arial', 10),
            fg='#bdc3c7',
            bg='#2c3e50'
        ).pack(anchor='e', pady=(10, 0))
        
        tk.Button(
            header_right,
            text="🚪 Salir",
            font=('Arial', 10, 'bold'),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            command=self.logout
        ).pack(anchor='e', pady=(5, 10))
        
        # Navbar
        self.frame_navbar = tk.Frame(self.root, bg='#34495e', height=60)
        self.frame_navbar.pack(fill='x')
        self.frame_navbar.pack_propagate(False)
        
        # Botones del navbar
        navbar_buttons = [
            ("🏠", "Inicio", self.mostrar_inicio),
            ("💰", "Ventas", self.mostrar_ventas),
            ("📦", "Inventario", self.mostrar_inventario),
            ("👥", "Clientes", self.mostrar_clientes),
            ("👤", "Usuarios", self.mostrar_usuarios),
            ("📊", "Reportes", self.mostrar_reportes),
            ("⚙️", "Configuración", self.mostrar_configuracion)
        ]
        
        self.navbar_buttons = {}
        for emoji, texto, comando in navbar_buttons:
            btn = tk.Button(
                self.frame_navbar,
                text=f"{emoji} {texto}",
                font=('Arial', 11, 'bold'),
                bg='#34495e',
                fg='white',
                relief='flat',
                bd=0,
                padx=20,
                pady=10,
                command=comando
            )
            btn.pack(side='left', padx=2)
            self.navbar_buttons[texto] = btn
            
            # Efecto hover
            self.agregar_hover_effect(btn)
        
        # Contenedor principal para el contenido
        self.frame_contenido = tk.Frame(self.root, bg='#ecf0f1')
        self.frame_contenido.pack(fill='both', expand=True)
        
        # Mostrar inicio por defecto
        self.mostrar_inicio()
    
    def agregar_hover_effect(self, button):
        """Agregar efecto hover a los botones del navbar"""
        def on_enter(e):
            button.config(bg='#4a6741')
        
        def on_leave(e):
            button.config(bg='#34495e')
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def limpiar_contenido(self):
        """Limpiar el contenido actual"""
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
    
    def resaltar_boton_activo(self, boton_activo):
        """Resaltar el botón activo en el navbar"""
        for nombre, btn in self.navbar_buttons.items():
            if nombre == boton_activo:
                btn.config(bg='#27ae60')
            else:
                btn.config(bg='#34495e')
    
    def mostrar_inicio(self):
        """Mostrar página de inicio"""
        self.limpiar_contenido()
        self.resaltar_boton_activo('Inicio')
        
        # Título
        tk.Label(
            self.frame_contenido,
            text="🏠 PANEL DE INICIO",
            font=('Arial', 24, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(pady=(30, 40))
        
        # Estadísticas rápidas
        stats_frame = tk.Frame(self.frame_contenido, bg='#ecf0f1')
        stats_frame.pack(fill='x', padx=50, pady=20)
        
        # Tarjetas de estadísticas
        stats = [
            ("💰", "Ventas Hoy", "$12,450", "#27ae60"),
            ("📦", "Productos", "1,234", "#3498db"),
            ("👥", "Clientes", "456", "#9b59b6"),
            ("📊", "Transacciones", "89", "#e74c3c")
        ]
        
        for i, (emoji, titulo, valor, color) in enumerate(stats):
            card = tk.Frame(stats_frame, bg=color, relief='raised', bd=2)
            card.pack(side='left', fill='both', expand=True, padx=10)
            
            tk.Label(
                card,
                text=emoji,
                font=('Arial', 30),
                fg='white',
                bg=color
            ).pack(pady=(20, 5))
            
            tk.Label(
                card,
                text=titulo,
                font=('Arial', 12, 'bold'),
                fg='white',
                bg=color
            ).pack()
            
            tk.Label(
                card,
                text=valor,
                font=('Arial', 16, 'bold'),
                fg='white',
                bg=color
            ).pack(pady=(0, 20))
        
        # Acciones rápidas
        tk.Label(
            self.frame_contenido,
            text="⚡ Acciones Rápidas",
            font=('Arial', 18, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(pady=(40, 20))
        
        acciones_frame = tk.Frame(self.frame_contenido, bg='#ecf0f1')
        acciones_frame.pack(fill='x', padx=100, pady=20)
        
        acciones = [
            ("💰 Nueva Venta", "#27ae60", self.mostrar_ventas),
            ("📦 Ver Inventario", "#3498db", self.mostrar_inventario),
            ("👤 Gestionar Usuarios", "#9b59b6", self.mostrar_usuarios),
            ("📊 Ver Reportes", "#e67e22", self.mostrar_reportes)
        ]
        
        for texto, color, comando in acciones:
            tk.Button(
                acciones_frame,
                text=texto,
                font=('Arial', 12, 'bold'),
                bg=color,
                fg='white',
                relief='flat',
                command=comando,
                width=20,
                height=2
            ).pack(side='left', fill='x', expand=True, padx=10)
    
    def mostrar_ventas(self):
        """Mostrar módulo de ventas"""
        self.limpiar_contenido()
        self.resaltar_boton_activo('Ventas')
        
        tk.Label(
            self.frame_contenido,
            text="💰 MÓDULO DE VENTAS",
            font=('Arial', 24, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(pady=50)
        
        tk.Label(
            self.frame_contenido,
            text="🚧 En desarrollo...",
            font=('Arial', 16),
            fg='#7f8c8d',
            bg='#ecf0f1'
        ).pack()
    
    def mostrar_inventario(self):
        """Mostrar módulo de inventario"""
        self.limpiar_contenido()
        self.resaltar_boton_activo('Inventario')
        
        tk.Label(
            self.frame_contenido,
            text="📦 GESTIÓN DE INVENTARIO",
            font=('Arial', 24, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(pady=50)
        
        tk.Label(
            self.frame_contenido,
            text="🚧 En desarrollo...",
            font=('Arial', 16),
            fg='#7f8c8d',
            bg='#ecf0f1'
        ).pack()
    
    def mostrar_clientes(self):
        """Mostrar módulo de clientes"""
        self.limpiar_contenido()
        self.resaltar_boton_activo('Clientes')
        
        tk.Label(
            self.frame_contenido,
            text="👥 GESTIÓN DE CLIENTES",
            font=('Arial', 24, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(pady=50)
        
        tk.Label(
            self.frame_contenido,
            text="🚧 En desarrollo...",
            font=('Arial', 16),
            fg='#7f8c8d',
            bg='#ecf0f1'
        ).pack()
    
    def mostrar_reportes(self):
        """Mostrar módulo de reportes"""
        self.limpiar_contenido()
        self.resaltar_boton_activo('Reportes')
        
        tk.Label(
            self.frame_contenido,
            text="📊 REPORTES Y ESTADÍSTICAS",
            font=('Arial', 24, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(pady=50)
        
        tk.Label(
            self.frame_contenido,
            text="🚧 En desarrollo...",
            font=('Arial', 16),
            fg='#7f8c8d',
            bg='#ecf0f1'
        ).pack()
    
    def mostrar_usuarios(self):
        """Mostrar módulo de usuarios integrado"""
        self.limpiar_contenido()
        self.resaltar_boton_activo('Usuarios')
        
        # Crear el sistema de usuarios integrado en el contenido
        self.gestor_usuarios = GestorUsuariosIntegrado(self.frame_contenido)
    
    def mostrar_configuracion(self):
        """Mostrar módulo de configuración integrado"""
        self.limpiar_contenido()
        self.resaltar_boton_activo('Configuración')
        
        # Crear el sistema de configuración integrado en el contenido
        self.config_integrada = ConfiguracionIntegrada(self.frame_contenido)
    
    def logout(self):
        """Cerrar sesión y volver al login"""
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            self.root.destroy()
            LoginApp().root.mainloop()

class GestorUsuariosIntegrado:
    """Gestor de usuarios integrado en el panel principal"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.crear_interfaz()
    
    def crear_interfaz(self):
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(pady=(0, 25))
        
        # Grid de funciones
        frame_funciones = tk.Frame(frame_main, bg='#ecf0f1')
        frame_funciones.pack(fill='both', expand=True)
        
        # Primera fila de botones
        fila1 = tk.Frame(frame_funciones, bg='#ecf0f1')
        fila1.pack(fill='x', pady=10)
        
        self.crear_boton_funcion(
            fila1, "💰 Gestión de Ventas", "#27ae60", 
            lambda: self.mostrar_funcion("Gestión de Ventas", "• Procesar ventas\n• Ver historial\n• Anular ventas\n• Reportes de vendedores")
        ).pack(side='left', fill='both', expand=True, padx=5)
        
        self.crear_boton_funcion(
            fila1, "📦 Inventario", "#3498db",
            lambda: self.mostrar_funcion("Inventario", "• Agregar productos\n• Editar productos\n• Control de stock\n• Categorías")
        ).pack(side='left', fill='both', expand=True, padx=5)
        
        self.crear_boton_funcion(
            fila1, "👥 Clientes", "#9b59b6",
            lambda: self.mostrar_funcion("Gestión de Clientes", "• Registrar clientes\n• Editar información\n• Historial de compras\n• Estadísticas")
        ).pack(side='left', fill='both', expand=True, padx=5)
        
        # Segunda fila de botones
        fila2 = tk.Frame(frame_funciones, bg='#ecf0f1')
        fila2.pack(fill='x', pady=10)
        
        self.crear_boton_funcion(
            fila2, "👤 Usuarios", "#e67e22",
            self.abrir_gestion_usuarios
        ).pack(side='left', fill='both', expand=True, padx=5)
        
        self.crear_boton_funcion(
            fila2, "📊 Reportes", "#34495e",
            lambda: self.mostrar_funcion("Reportes", "• Ventas por período\n• Productos más vendidos\n• Ganancias\n• Exportar datos")
        ).pack(side='left', fill='both', expand=True, padx=5)
        
        self.crear_boton_funcion(
            fila2, "⚙️ Configuración", "#95a5a6",
            self.abrir_configuracion
        ).pack(side='left', fill='both', expand=True, padx=5)
        
        # Información del sistema
        frame_info = tk.LabelFrame(
            frame_main, 
            text="📊 Estado del Sistema", 
            font=('Arial', 11, 'bold'),
            bg='#ecf0f1'
        )
        frame_info.pack(fill='x', pady=(20, 0))
        
        info_text = tk.Text(frame_info, height=4, font=('Consolas', 9), bg='white')
        info_text.pack(fill='x', padx=10, pady=10)
        
        info_content = """✅ Sistema POS v1.0 - Activo
👤 Usuarios registrados: 2 (admin, usuario1)
📦 Productos en inventario: Por configurar
💰 Ventas del día: $0.00"""
        
        info_text.insert('1.0', info_content)
        info_text.config(state='disabled')
        
    def crear_boton_funcion(self, parent, texto, color, comando):
        """Crear botón de función estilizado"""
        return tk.Button(
            parent,
            text=texto,
            font=('Arial', 11, 'bold'),
            bg=color,
            fg='white',
            relief='flat',
            height=4,
            command=comando
        )
        
    def mostrar_funcion(self, titulo, descripcion):
        """Mostrar información de la función seleccionada"""
        messagebox.showinfo(
            titulo,
            f"{titulo}\n\nFuncionalidades:\n{descripcion}\n\n[Función por implementar]"
        )
        
    def abrir_configuracion(self):
        """Abrir ventana de configuración del sistema"""
        VentanaConfiguracion(self.root)
        
    def abrir_gestion_usuarios(self):
        """Abrir ventana de gestión de usuarios"""
        VentanaGestionUsuarios(self.root)
        
    def cerrar_sesion(self):
        """Cerrar sesión y volver al login"""
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            self.root.destroy()
            LoginApp().root.mainloop()

class PanelUsuario:
    """Panel de usuario normal con funciones limitadas"""
    
    def __init__(self, usuario, datos_usuario):
        self.usuario = usuario
        self.datos_usuario = datos_usuario
        
        self.root = tk.Tk()
        self.root.title(f"🏪 Sistema POS - Panel Usuario ({datos_usuario['nombre_completo']})")
        # Hacer que ocupe toda la pantalla
        self.root.state('zoomed')  # Para Windows
        self.root.configure(bg='#ecf0f1')
        self.crear_interfaz()
        self.root.mainloop()
        
    def centrar_ventana(self):
        """Centrar ventana"""
        self.root.update_idletasks()
        ancho = 700
        alto = 500
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')
        
    def crear_interfaz(self):
        """Crear interfaz del panel de usuario"""
        
        # Header
        frame_header = tk.Frame(self.root, bg='#27ae60', height=70)
        frame_header.pack(fill='x')
        frame_header.pack_propagate(False)
        
        tk.Label(
            frame_header,
            text=f"👤 PANEL USUARIO - {self.datos_usuario['nombre_completo']}",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#27ae60'
        ).pack(expand=True)
        
        # Botón cerrar sesión
        btn_cerrar = tk.Button(
            frame_header,
            text="🚪 Cerrar Sesión",
            font=('Arial', 9),
            bg='#229954',
            fg='white',
            relief='flat',
            command=self.cerrar_sesion
        )
        btn_cerrar.place(relx=0.95, rely=0.5, anchor='e')
        
        # Contenido principal
        frame_main = tk.Frame(self.root, bg='#ecf0f1')
        frame_main.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(
            frame_main,
            text="🛒 Funciones de Usuario",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(pady=(0, 25))
        
        # Funciones disponibles para usuario
        frame_funciones = tk.Frame(frame_main, bg='#ecf0f1')
        frame_funciones.pack(fill='both', expand=True)
        
        # Fila de botones
        fila = tk.Frame(frame_funciones, bg='#ecf0f1')
        fila.pack(fill='x', pady=20)
        
        self.crear_boton_funcion(
            fila, "💰 Procesar Ventas", "#27ae60",
            lambda: self.mostrar_funcion("Procesar Ventas", "• Registrar ventas\n• Buscar productos\n• Imprimir recibos")
        ).pack(side='left', fill='both', expand=True, padx=10)
        
        self.crear_boton_funcion(
            fila, "📦 Consultar Stock", "#3498db",
            lambda: self.mostrar_funcion("Consultar Stock", "• Ver productos disponibles\n• Consultar precios\n• Verificar existencias")
        ).pack(side='left', fill='both', expand=True, padx=10)
        
        # Segunda fila
        fila2 = tk.Frame(frame_funciones, bg='#ecf0f1')
        fila2.pack(fill='x', pady=20)
        
        self.crear_boton_funcion(
            fila2, "👥 Buscar Clientes", "#9b59b6",
            lambda: self.mostrar_funcion("Buscar Clientes", "• Buscar información de clientes\n• Ver historial de compras")
        ).pack(side='left', fill='both', expand=True, padx=10)
        
        self.crear_boton_funcion(
            fila2, "👤 Mi Perfil", "#34495e",
            lambda: self.mostrar_perfil()
        ).pack(side='left', fill='both', expand=True, padx=10)
        
        # Información del usuario
        frame_info = tk.LabelFrame(
            frame_main, 
            text="📊 Información del Usuario", 
            font=('Arial', 11, 'bold'),
            bg='#ecf0f1'
        )
        frame_info.pack(fill='x', pady=(20, 0))
        
        info_text = tk.Text(frame_info, height=3, font=('Consolas', 9), bg='white')
        info_text.pack(fill='x', padx=10, pady=10)
        
        info_content = f"""👤 Usuario: {self.datos_usuario['nombre_completo']}
🔑 Tipo de acceso: {self.datos_usuario['tipo'].title()}
⚠️  Funciones administrativas: No disponibles"""
        
        info_text.insert('1.0', info_content)
        info_text.config(state='disabled')
        
    def crear_boton_funcion(self, parent, texto, color, comando):
        """Crear botón de función estilizado"""
        return tk.Button(
            parent,
            text=texto,
            font=('Arial', 11, 'bold'),
            bg=color,
            fg='white',
            relief='flat',
            height=4,
            command=comando
        )
        
    def mostrar_funcion(self, titulo, descripcion):
        """Mostrar información de la función seleccionada"""
        messagebox.showinfo(
            titulo,
            f"{titulo}\n\nFuncionalidades disponibles:\n{descripcion}\n\n[Función por implementar]"
        )
        
    def mostrar_perfil(self):
        """Mostrar información del perfil del usuario"""
        messagebox.showinfo(
            "Mi Perfil",
            f"👤 Información del Perfil\n\n"
            f"Usuario: {self.usuario}\n"
            f"Nombre: {self.datos_usuario['nombre_completo']}\n"
            f"Tipo: {self.datos_usuario['tipo'].title()}\n\n"
            f"[Cambio de contraseña por implementar]"
        )
        
    def cerrar_sesion(self):
        """Cerrar sesión y volver al login"""
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            self.root.destroy()
            LoginApp().root.mainloop()

class VentanaConfiguracion:
    """Ventana de configuración del sistema"""
    
    def __init__(self, parent):
        self.parent = parent
        
        # Configuraciones por defecto (simuladas)
        self.config = {
            'empresa': {
                'nombre': 'Mi Empresa POS',
                'ruc': '20123456789',
                'direccion': 'Av. Principal 123',
                'telefono': '(01) 234-5678',
                'email': 'info@miempresa.com'
            },
            'sistema': {
                'moneda': 'PEN',
                'simbolo_moneda': 'S/.',
                'igv': 18.0,
                'decimales': 2,
                'tema': 'Claro'
            },
            'impresora': {
                'nombre': 'Impresora por defecto',
                'tipo': 'Térmica',
                'ancho_papel': '80mm',
                'pie_pagina': 'Gracias por su compra'
            },
            'backup': {
                'automatico': True,
                'frecuencia': 'Diario',
                'hora': '23:00',
                'ubicacion': 'C:\\Backup\\POS'
            }
        }
        
        self.crear_ventana()
        
    def crear_ventana(self):
        """Crear la ventana de configuración"""
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("⚙️ Configuración del Sistema")
        self.ventana.geometry("700x600")
        self.ventana.configure(bg='#f8f9fa')
        self.ventana.transient(self.parent)
        self.ventana.grab_set()
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Header
        header_frame = tk.Frame(self.ventana, bg='#95a5a6', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="⚙️ CONFIGURACIÓN DEL SISTEMA",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#95a5a6'
        ).pack(expand=True)
        
        # Notebook para pestañas
        notebook = ttk.Notebook(self.ventana)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.crear_tab_empresa(notebook)
        self.crear_tab_sistema(notebook)
        self.crear_tab_impresora(notebook)
        self.crear_tab_backup(notebook)
        self.crear_tab_informacion(notebook)
        
        # Botones inferiores
        frame_botones = tk.Frame(self.ventana, bg='#f8f9fa')
        frame_botones.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Button(
            frame_botones,
            text="💾 Guardar Configuración",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=self.guardar_configuracion
        ).pack(side='left', padx=5)
        
        tk.Button(
            frame_botones,
            text="🔄 Restaurar Valores",
            font=('Arial', 11, 'bold'),
            bg='#f39c12',
            fg='white',
            relief='flat',
            command=self.restaurar_valores
        ).pack(side='left', padx=5)
        
        tk.Button(
            frame_botones,
            text="❌ Cerrar",
            font=('Arial', 11, 'bold'),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            command=self.ventana.destroy
        ).pack(side='right', padx=5)
        
    def centrar_ventana(self):
        """Centrar ventana de configuración"""
        self.ventana.update_idletasks()
        ancho = 700
        alto = 600
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
        
    def crear_tab_empresa(self, notebook):
        """Crear pestaña de configuración de empresa"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="🏢 Empresa")
        
        # Scroll frame
        canvas = tk.Canvas(frame, bg='white')
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Campos de empresa
        tk.Label(scrollable_frame, text="📊 Información de la Empresa", font=('Arial', 12, 'bold')).pack(pady=(10, 20))
        
        # Nombre de empresa
        tk.Label(scrollable_frame, text="Nombre de la Empresa:", font=('Arial', 10, 'bold')).pack(anchor='w', padx=20)
        self.entry_empresa_nombre = tk.Entry(scrollable_frame, font=('Arial', 10), width=50)
        self.entry_empresa_nombre.pack(pady=(5, 15), padx=20, fill='x')
        self.entry_empresa_nombre.insert(0, self.config['empresa']['nombre'])
        
        # RUC
        tk.Label(scrollable_frame, text="RUC:", font=('Arial', 10, 'bold')).pack(anchor='w', padx=20)
        self.entry_empresa_ruc = tk.Entry(scrollable_frame, font=('Arial', 10), width=30)
        self.entry_empresa_ruc.pack(pady=(5, 15), padx=20, anchor='w')
        self.entry_empresa_ruc.insert(0, self.config['empresa']['ruc'])
        
        # Dirección
        tk.Label(scrollable_frame, text="Dirección:", font=('Arial', 10, 'bold')).pack(anchor='w', padx=20)
        self.entry_empresa_direccion = tk.Entry(scrollable_frame, font=('Arial', 10), width=50)
        self.entry_empresa_direccion.pack(pady=(5, 15), padx=20, fill='x')
        self.entry_empresa_direccion.insert(0, self.config['empresa']['direccion'])
        
        # Teléfono
        tk.Label(scrollable_frame, text="Teléfono:", font=('Arial', 10, 'bold')).pack(anchor='w', padx=20)
        self.entry_empresa_telefono = tk.Entry(scrollable_frame, font=('Arial', 10), width=30)
        self.entry_empresa_telefono.pack(pady=(5, 15), padx=20, anchor='w')
        self.entry_empresa_telefono.insert(0, self.config['empresa']['telefono'])
        
        # Email
        tk.Label(scrollable_frame, text="Email:", font=('Arial', 10, 'bold')).pack(anchor='w', padx=20)
        self.entry_empresa_email = tk.Entry(scrollable_frame, font=('Arial', 10), width=40)
        self.entry_empresa_email.pack(pady=(5, 15), padx=20, anchor='w')
        self.entry_empresa_email.insert(0, self.config['empresa']['email'])
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def crear_tab_sistema(self, notebook):
        """Crear pestaña de configuración del sistema"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="⚙️ Sistema")
        
        main_frame = tk.Frame(frame, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="⚙️ Parámetros del Sistema", font=('Arial', 12, 'bold'), bg='white').pack(pady=(0, 20))
        
        # Moneda
        tk.Label(main_frame, text="Moneda:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w')
        self.combo_moneda = ttk.Combobox(main_frame, values=['PEN', 'USD', 'EUR'], state='readonly', width=10)
        self.combo_moneda.pack(pady=(5, 15), anchor='w')
        self.combo_moneda.set(self.config['sistema']['moneda'])
        
        # Símbolo de moneda
        tk.Label(main_frame, text="Símbolo de Moneda:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w')
        self.entry_simbolo = tk.Entry(main_frame, font=('Arial', 10), width=10)
        self.entry_simbolo.pack(pady=(5, 15), anchor='w')
        self.entry_simbolo.insert(0, self.config['sistema']['simbolo_moneda'])
        
        # IGV
        tk.Label(main_frame, text="IGV (%):", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w')
        self.entry_igv = tk.Entry(main_frame, font=('Arial', 10), width=10)
        self.entry_igv.pack(pady=(5, 15), anchor='w')
        self.entry_igv.insert(0, str(self.config['sistema']['igv']))
        
        # Decimales
        tk.Label(main_frame, text="Decimales:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w')
        self.combo_decimales = ttk.Combobox(main_frame, values=['0', '1', '2', '3'], state='readonly', width=10)
        self.combo_decimales.pack(pady=(5, 15), anchor='w')
        self.combo_decimales.set(str(self.config['sistema']['decimales']))
        
        # Tema
        tk.Label(main_frame, text="Tema de la Aplicación:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w')
        self.combo_tema = ttk.Combobox(main_frame, values=['Claro', 'Oscuro', 'Azul'], state='readonly', width=15)
        self.combo_tema.pack(pady=(5, 15), anchor='w')
        self.combo_tema.set(self.config['sistema']['tema'])
        
    def crear_tab_impresora(self, notebook):
        """Crear pestaña de configuración de impresora"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="🖨️ Impresora")
        
        main_frame = tk.Frame(frame, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="🖨️ Configuración de Impresora", font=('Arial', 12, 'bold'), bg='white').pack(pady=(0, 20))
        
        # Nombre de impresora
        tk.Label(main_frame, text="Nombre de Impresora:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w')
        self.entry_impresora_nombre = tk.Entry(main_frame, font=('Arial', 10), width=40)
        self.entry_impresora_nombre.pack(pady=(5, 15), anchor='w')
        self.entry_impresora_nombre.insert(0, self.config['impresora']['nombre'])
        
        # Tipo de impresora
        tk.Label(main_frame, text="Tipo:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w')
        self.combo_tipo_impresora = ttk.Combobox(main_frame, values=['Térmica', 'Matricial', 'Inyección', 'Láser'], state='readonly', width=15)
        self.combo_tipo_impresora.pack(pady=(5, 15), anchor='w')
        self.combo_tipo_impresora.set(self.config['impresora']['tipo'])
        
        # Ancho de papel
        tk.Label(main_frame, text="Ancho de Papel:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w')
        self.combo_ancho_papel = ttk.Combobox(main_frame, values=['58mm', '80mm', 'A4'], state='readonly', width=15)
        self.combo_ancho_papel.pack(pady=(5, 15), anchor='w')
        self.combo_ancho_papel.set(self.config['impresora']['ancho_papel'])
        
        # Pie de página
        tk.Label(main_frame, text="Mensaje de Pie de Página:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w')
        self.entry_pie_pagina = tk.Entry(main_frame, font=('Arial', 10), width=50)
        self.entry_pie_pagina.pack(pady=(5, 15), anchor='w')
        self.entry_pie_pagina.insert(0, self.config['impresora']['pie_pagina'])
        
        # Botón de prueba
        tk.Button(
            main_frame,
            text="🖨️ Imprimir Prueba",
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=self.imprimir_prueba
        ).pack(pady=20)
        
    def crear_tab_backup(self, notebook):
        """Crear pestaña de configuración de backup"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="💾 Backup")
        
        main_frame = tk.Frame(frame, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="💾 Configuración de Respaldo", font=('Arial', 12, 'bold'), bg='white').pack(pady=(0, 20))
        
        # Backup automático
        self.var_backup_auto = tk.BooleanVar(value=self.config['backup']['automatico'])
        tk.Checkbutton(
            main_frame,
            text="Activar backup automático",
            variable=self.var_backup_auto,
            font=('Arial', 10, 'bold'),
            bg='white'
        ).pack(anchor='w', pady=10)
        
        # Frecuencia
        tk.Label(main_frame, text="Frecuencia:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w')
        self.combo_frecuencia = ttk.Combobox(main_frame, values=['Diario', 'Semanal', 'Mensual'], state='readonly', width=15)
        self.combo_frecuencia.pack(pady=(5, 15), anchor='w')
        self.combo_frecuencia.set(self.config['backup']['frecuencia'])
        
        # Hora
        tk.Label(main_frame, text="Hora:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w')
        self.entry_hora_backup = tk.Entry(main_frame, font=('Arial', 10), width=10)
        self.entry_hora_backup.pack(pady=(5, 15), anchor='w')
        self.entry_hora_backup.insert(0, self.config['backup']['hora'])
        
        # Ubicación
        tk.Label(main_frame, text="Carpeta de Respaldo:", font=('Arial', 10, 'bold'), bg='white').pack(anchor='w')
        frame_ubicacion = tk.Frame(main_frame, bg='white')
        frame_ubicacion.pack(fill='x', pady=(5, 15))
        
        self.entry_ubicacion = tk.Entry(frame_ubicacion, font=('Arial', 10), width=40)
        self.entry_ubicacion.pack(side='left')
        self.entry_ubicacion.insert(0, self.config['backup']['ubicacion'])
        
        tk.Button(
            frame_ubicacion,
            text="📂 Buscar",
            font=('Arial', 9),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=self.buscar_carpeta
        ).pack(side='left', padx=(5, 0))
        
        # Botones de backup
        frame_botones_backup = tk.Frame(main_frame, bg='white')
        frame_botones_backup.pack(fill='x', pady=20)
        
        tk.Button(
            frame_botones_backup,
            text="💾 Crear Backup Ahora",
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=self.crear_backup
        ).pack(side='left', padx=5)
        
        tk.Button(
            frame_botones_backup,
            text="📂 Restaurar Backup",
            font=('Arial', 10, 'bold'),
            bg='#f39c12',
            fg='white',
            relief='flat',
            command=self.restaurar_backup
        ).pack(side='left', padx=5)
        
    def crear_tab_informacion(self, notebook):
        """Crear pestaña de información del sistema"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="ℹ️ Información")
        
        main_frame = tk.Frame(frame, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="ℹ️ Información del Sistema", font=('Arial', 12, 'bold'), bg='white').pack(pady=(0, 20))
        
        info_text = tk.Text(main_frame, height=15, font=('Consolas', 10), bg='#f8f9fa', state='normal')
        info_text.pack(fill='both', expand=True)
        
        info_sistema = f"""🏪 SISTEMA POS - INFORMACIÓN DETALLADA

📋 Información del Software:
   • Nombre: Sistema POS Simple
   • Versión: 1.0.0
   • Fecha de compilación: {datetime.datetime.now().strftime("%d/%m/%Y")}
   • Desarrollador: Sistema Interno

💻 Información del Sistema:
   • Sistema Operativo: {platform.system()} {platform.release()}
   • Arquitectura: {platform.architecture()[0]}
   • Procesador: {platform.processor()}
   • Versión de Python: {platform.python_version()}

🔧 Módulos Instalados:
   • tkinter: ✅ Instalado
   • hashlib: ✅ Instalado
   • datetime: ✅ Instalado
   • platform: ✅ Instalado

📊 Estado Actual:
   • Base de datos: Simulada (en memoria)
   • Usuarios activos: 2
   • Configuración: Por defecto
   • Última actualización: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}

📞 Soporte Técnico:
   • Email: soporte@sistemapos.com
   • Teléfono: (01) 123-4567
   • Horario: Lunes a Viernes 9:00 - 18:00"""
        
        info_text.insert('1.0', info_sistema)
        info_text.config(state='disabled')
        
    def imprimir_prueba(self):
        """Simular impresión de prueba"""
        messagebox.showinfo(
            "Impresión de Prueba",
            "🖨️ PRUEBA DE IMPRESIÓN\n\n"
            f"Impresora: {self.entry_impresora_nombre.get()}\n"
            f"Tipo: {self.combo_tipo_impresora.get()}\n"
            f"Papel: {self.combo_ancho_papel.get()}\n\n"
            "✅ Impresión simulada exitosa"
        )
        
    def buscar_carpeta(self):
        """Buscar carpeta para backup"""
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta para backup")
        if carpeta:
            self.entry_ubicacion.delete(0, tk.END)
            self.entry_ubicacion.insert(0, carpeta)
            
    def crear_backup(self):
        """Crear backup del sistema"""
        messagebox.showinfo(
            "Crear Backup",
            "💾 BACKUP CREADO\n\n"
            f"Ubicación: {self.entry_ubicacion.get()}\n"
            f"Fecha: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
            f"Tamaño: 2.5 MB\n\n"
            "✅ Backup creado exitosamente"
        )
        
    def restaurar_backup(self):
        """Restaurar backup del sistema"""
        if messagebox.askyesno("Restaurar Backup", "⚠️ ¿Está seguro que desea restaurar un backup?\n\nEsto sobrescribirá la configuración actual."):
            messagebox.showinfo(
                "Restaurar Backup",
                "📂 BACKUP RESTAURADO\n\n"
                "✅ Sistema restaurado exitosamente\n"
                "ℹ️ Reinicie la aplicación para aplicar cambios"
            )
            
    def guardar_configuracion(self):
        """Guardar configuración"""
        # Actualizar configuración con valores de los campos
        self.config['empresa']['nombre'] = self.entry_empresa_nombre.get()
        self.config['empresa']['ruc'] = self.entry_empresa_ruc.get()
        self.config['empresa']['direccion'] = self.entry_empresa_direccion.get()
        self.config['empresa']['telefono'] = self.entry_empresa_telefono.get()
        self.config['empresa']['email'] = self.entry_empresa_email.get()
        
        self.config['sistema']['moneda'] = self.combo_moneda.get()
        self.config['sistema']['simbolo_moneda'] = self.entry_simbolo.get()
        self.config['sistema']['igv'] = float(self.entry_igv.get())
        self.config['sistema']['decimales'] = int(self.combo_decimales.get())
        self.config['sistema']['tema'] = self.combo_tema.get()
        
        self.config['impresora']['nombre'] = self.entry_impresora_nombre.get()
        self.config['impresora']['tipo'] = self.combo_tipo_impresora.get()
        self.config['impresora']['ancho_papel'] = self.combo_ancho_papel.get()
        self.config['impresora']['pie_pagina'] = self.entry_pie_pagina.get()
        
        self.config['backup']['automatico'] = self.var_backup_auto.get()
        self.config['backup']['frecuencia'] = self.combo_frecuencia.get()
        self.config['backup']['hora'] = self.entry_hora_backup.get()
        self.config['backup']['ubicacion'] = self.entry_ubicacion.get()
        
        messagebox.showinfo(
            "Configuración Guardada",
            "💾 CONFIGURACIÓN GUARDADA\n\n"
            "✅ Todos los cambios han sido guardados exitosamente\n"
            "ℹ️ Algunos cambios requieren reiniciar la aplicación"
        )
        
    def restaurar_valores(self):
        """Restaurar valores por defecto"""
        if messagebox.askyesno("Restaurar Valores", "⚠️ ¿Está seguro que desea restaurar los valores por defecto?\n\nSe perderán todos los cambios no guardados."):
            # Limpiar y restaurar campos
            self.entry_empresa_nombre.delete(0, tk.END)
            self.entry_empresa_nombre.insert(0, 'Mi Empresa POS')
            
            self.entry_empresa_ruc.delete(0, tk.END)
            self.entry_empresa_ruc.insert(0, '20123456789')
            
            messagebox.showinfo("Valores Restaurados", "🔄 Valores por defecto restaurados")

class VentanaGestionUsuarios:
    """Ventana de gestión de usuarios del sistema"""
    
    def __init__(self, parent):
        self.parent = parent
        
        # Base de datos simulada de usuarios (expandida)
        self.usuarios_db = {
            'admin': {
                'nombre_completo': 'Administrador del Sistema',
                'email': 'admin@empresa.com',
                'telefono': '123-456-7890',
                'tipo': 'administrador',
                'activo': True,
                'fecha_creacion': '01/01/2025',
                'ultimo_acceso': '23/09/2025 14:30',
                'intentos_fallidos': 0,
                'permisos': ['todos']
            },
            'usuario1': {
                'nombre_completo': 'Usuario Normal',
                'email': 'usuario1@empresa.com',
                'telefono': '123-456-7891',
                'tipo': 'usuario',
                'activo': True,
                'fecha_creacion': '02/01/2025',
                'ultimo_acceso': '23/09/2025 10:15',
                'intentos_fallidos': 0,
                'permisos': ['ventas', 'consultas']
            },
            'vendedor1': {
                'nombre_completo': 'Juan Pérez',
                'email': 'juan.perez@empresa.com',
                'telefono': '123-456-7892',
                'tipo': 'usuario',
                'activo': True,
                'fecha_creacion': '15/01/2025',
                'ultimo_acceso': '22/09/2025 18:45',
                'intentos_fallidos': 0,
                'permisos': ['ventas']
            },
            'supervisor1': {
                'nombre_completo': 'María García',
                'email': 'maria.garcia@empresa.com',
                'telefono': '123-456-7893',
                'tipo': 'supervisor',
                'activo': False,
                'fecha_creacion': '10/02/2025',
                'ultimo_acceso': '20/09/2025 16:20',
                'intentos_fallidos': 1,
                'permisos': ['ventas', 'reportes', 'usuarios_consulta']
            }
        }
        
        self.usuario_seleccionado = None
        self.crear_ventana()
        
    def crear_ventana(self):
        """Crear la ventana de gestión de usuarios"""
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("👤 Gestión de Usuarios")
        self.ventana.geometry("900x700")
        self.ventana.configure(bg='#f8f9fa')
        self.ventana.transient(self.parent)
        self.ventana.grab_set()
        
        self.centrar_ventana()
        
        # Header
        header_frame = tk.Frame(self.ventana, bg='#e67e22', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="👤 GESTIÓN DE USUARIOS",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#e67e22'
        ).pack(expand=True)
        
        # Frame principal
        main_frame = tk.Frame(self.ventana, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Lista de usuarios
        left_panel = tk.LabelFrame(main_frame, text="👥 Lista de Usuarios", font=('Arial', 11, 'bold'))
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Barra de herramientas
        toolbar_frame = tk.Frame(left_panel)
        toolbar_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(
            toolbar_frame,
            text="➕ Nuevo Usuario",
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=self.nuevo_usuario
        ).pack(side='left', padx=2)
        
        tk.Button(
            toolbar_frame,
            text="✏️ Editar",
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=self.editar_usuario
        ).pack(side='left', padx=2)
        
        tk.Button(
            toolbar_frame,
            text="🔒 Bloquear/Activar",
            font=('Arial', 10, 'bold'),
            bg='#f39c12',
            fg='white',
            relief='flat',
            command=self.toggle_estado_usuario
        ).pack(side='left', padx=2)
        
        tk.Button(
            toolbar_frame,
            text="🗑️ Eliminar",
            font=('Arial', 10, 'bold'),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            command=self.eliminar_usuario
        ).pack(side='left', padx=2)
        
        # Buscador
        search_frame = tk.Frame(left_panel)
        search_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Label(search_frame, text="🔍 Buscar:", font=('Arial', 10)).pack(side='left')
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filtrar_usuarios)
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 10))
        search_entry.pack(side='left', fill='x', expand=True, padx=(5, 0))
        
        # Lista de usuarios (TreeView)
        list_frame = tk.Frame(left_panel)
        list_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        columns = ('usuario', 'nombre', 'tipo', 'estado', 'ultimo_acceso')
        self.tree_usuarios = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.tree_usuarios.heading('usuario', text='Usuario')
        self.tree_usuarios.heading('nombre', text='Nombre Completo')
        self.tree_usuarios.heading('tipo', text='Tipo')
        self.tree_usuarios.heading('estado', text='Estado')
        self.tree_usuarios.heading('ultimo_acceso', text='Último Acceso')
        
        self.tree_usuarios.column('usuario', width=100)
        self.tree_usuarios.column('nombre', width=180)
        self.tree_usuarios.column('tipo', width=100)
        self.tree_usuarios.column('estado', width=80)
        self.tree_usuarios.column('ultimo_acceso', width=120)
        
        # Scrollbar para la lista
        scrollbar_usuarios = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree_usuarios.yview)
        self.tree_usuarios.configure(yscrollcommand=scrollbar_usuarios.set)
        
        self.tree_usuarios.pack(side='left', fill='both', expand=True)
        scrollbar_usuarios.pack(side='right', fill='y')
        
        # Evento de selección
        self.tree_usuarios.bind('<<TreeviewSelect>>', self.on_usuario_select)
        
        # Panel derecho - Detalles del usuario
        right_panel = tk.LabelFrame(main_frame, text="📋 Detalles del Usuario", font=('Arial', 11, 'bold'))
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Información del usuario seleccionado
        self.info_frame = tk.Frame(right_panel)
        self.info_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Botones inferiores
        bottom_frame = tk.Frame(self.ventana, bg='#f8f9fa')
        bottom_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Button(
            bottom_frame,
            text="📊 Generar Reporte",
            font=('Arial', 10, 'bold'),
            bg='#9b59b6',
            fg='white',
            relief='flat',
            command=self.generar_reporte
        ).pack(side='left', padx=5)
        
        tk.Button(
            bottom_frame,
            text="🔄 Actualizar",
            font=('Arial', 10, 'bold'),
            bg='#34495e',
            fg='white',
            relief='flat',
            command=self.actualizar_lista
        ).pack(side='left', padx=5)
        
        tk.Button(
            bottom_frame,
            text="❌ Cerrar",
            font=('Arial', 10, 'bold'),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=self.ventana.destroy
        ).pack(side='right', padx=5)
        
        # Cargar datos iniciales
        self.cargar_usuarios()
        self.mostrar_info_vacia()
        
    def centrar_ventana(self):
        """Centrar ventana de gestión de usuarios"""
        self.ventana.update_idletasks()
        ancho = 900
        alto = 700
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
        
    def cargar_usuarios(self):
        """Cargar usuarios en la tabla"""
        # Limpiar tabla
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
            
        # Agregar usuarios
        for username, datos in self.usuarios_db.items():
            estado = "🟢 Activo" if datos['activo'] else "🔴 Inactivo"
            tipo_emoji = {"administrador": "👑", "supervisor": "👨‍💼", "usuario": "👤"}
            tipo_display = f"{tipo_emoji.get(datos['tipo'], '👤')} {datos['tipo'].title()}"
            
            self.tree_usuarios.insert('', 'end', values=(
                username,
                datos['nombre_completo'],
                tipo_display,
                estado,
                datos['ultimo_acceso']
            ))
            
    def filtrar_usuarios(self, *args):
        """Filtrar usuarios por búsqueda"""
        busqueda = self.search_var.get().lower()
        
        # Limpiar tabla
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
            
        # Agregar usuarios filtrados
        for username, datos in self.usuarios_db.items():
            if (busqueda in username.lower() or 
                busqueda in datos['nombre_completo'].lower() or
                busqueda in datos['tipo'].lower() or
                busqueda in datos['email'].lower()):
                
                estado = "🟢 Activo" if datos['activo'] else "🔴 Inactivo"
                tipo_emoji = {"administrador": "👑", "supervisor": "👨‍💼", "usuario": "👤"}
                tipo_display = f"{tipo_emoji.get(datos['tipo'], '👤')} {datos['tipo'].title()}"
                
                self.tree_usuarios.insert('', 'end', values=(
                    username,
                    datos['nombre_completo'],
                    tipo_display,
                    estado,
                    datos['ultimo_acceso']
                ))
                
    def on_usuario_select(self, event):
        """Manejar selección de usuario"""
        selection = self.tree_usuarios.selection()
        if selection:
            item = self.tree_usuarios.item(selection[0])
            username = item['values'][0]
            self.usuario_seleccionado = username
            self.mostrar_info_usuario(username)
        else:
            self.mostrar_info_vacia()
            
    def mostrar_info_vacia(self):
        """Mostrar información vacía cuando no hay selección"""
        # Limpiar frame
        for widget in self.info_frame.winfo_children():
            widget.destroy()
            
        tk.Label(
            self.info_frame,
            text="👤 Seleccione un usuario para ver los detalles",
            font=('Arial', 12),
            fg='#7f8c8d'
        ).pack(expand=True)
        
    def mostrar_info_usuario(self, username):
        """Mostrar información detallada del usuario"""
        # Limpiar frame
        for widget in self.info_frame.winfo_children():
            widget.destroy()
            
        if username not in self.usuarios_db:
            return
            
        datos = self.usuarios_db[username]
        
        # Crear canvas con scroll para la información
        canvas = tk.Canvas(self.info_frame, bg='white')
        scrollbar = ttk.Scrollbar(self.info_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Información del usuario
        tk.Label(
            scrollable_frame,
            text=f"👤 {datos['nombre_completo']}",
            font=('Arial', 14, 'bold'),
            fg='#2c3e50'
        ).pack(pady=(10, 20))
        
        # Datos básicos
        info_basica = [
            ("🔑 Usuario:", username),
            ("📧 Email:", datos['email']),
            ("📞 Teléfono:", datos['telefono']),
            ("👑 Tipo:", datos['tipo'].title()),
            ("📅 Creado:", datos['fecha_creacion']),
            ("🕐 Último acceso:", datos['ultimo_acceso']),
            ("❌ Intentos fallidos:", str(datos['intentos_fallidos'])),
            ("🟢 Estado:", "Activo" if datos['activo'] else "Inactivo")
        ]
        
        for label, valor in info_basica:
            frame_info = tk.Frame(scrollable_frame, bg='white')
            frame_info.pack(fill='x', padx=20, pady=2)
            
            tk.Label(
                frame_info,
                text=label,
                font=('Arial', 10, 'bold'),
                bg='white',
                width=15,
                anchor='w'
            ).pack(side='left')
            
            tk.Label(
                frame_info,
                text=valor,
                font=('Arial', 10),
                bg='white',
                anchor='w'
            ).pack(side='left', fill='x', expand=True)
            
        # Permisos
        tk.Label(
            scrollable_frame,
            text="🔐 Permisos:",
            font=('Arial', 12, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(pady=(20, 10), anchor='w', padx=20)
        
        permisos_frame = tk.Frame(scrollable_frame, bg='white')
        permisos_frame.pack(fill='x', padx=40, pady=(0, 20))
        
        permisos_todos = {
            'todos': '🔓 Acceso completo',
            'ventas': '💰 Módulo de ventas',
            'inventario': '📦 Gestión de inventario',
            'clientes': '👥 Gestión de clientes',
            'reportes': '📊 Ver reportes',
            'usuarios_consulta': '👤 Consultar usuarios',
            'configuracion': '⚙️ Configuración del sistema',
            'consultas': '🔍 Solo consultas'
        }
        
        for permiso in datos['permisos']:
            tk.Label(
                permisos_frame,
                text=f"✅ {permisos_todos.get(permiso, permiso)}",
                font=('Arial', 9),
                bg='white',
                fg='#27ae60'
            ).pack(anchor='w')
            
        # Acciones rápidas
        tk.Label(
            scrollable_frame,
            text="⚡ Acciones Rápidas:",
            font=('Arial', 12, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(pady=(20, 10), anchor='w', padx=20)
        
        acciones_frame = tk.Frame(scrollable_frame, bg='white')
        acciones_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Button(
            acciones_frame,
            text="🔑 Cambiar Contraseña",
            font=('Arial', 9, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=lambda: self.cambiar_password(username)
        ).pack(fill='x', pady=2)
        
        tk.Button(
            acciones_frame,
            text="🔐 Gestionar Permisos",
            font=('Arial', 9, 'bold'),
            bg='#9b59b6',
            fg='white',
            relief='flat',
            command=lambda: self.gestionar_permisos(username)
        ).pack(fill='x', pady=2)
        
        estado_text = "🔒 Bloquear Usuario" if datos['activo'] else "🔓 Activar Usuario"
        estado_color = "#e74c3c" if datos['activo'] else "#27ae60"
        
        tk.Button(
            acciones_frame,
            text=estado_text,
            font=('Arial', 9, 'bold'),
            bg=estado_color,
            fg='white',
            relief='flat',
            command=lambda: self.toggle_estado_usuario()
        ).pack(fill='x', pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def nuevo_usuario(self):
        """Crear nuevo usuario"""
        VentanaUsuario(self.ventana, self, modo='nuevo')
        
    def editar_usuario(self):
        """Editar usuario seleccionado"""
        if not self.usuario_seleccionado:
            messagebox.showwarning("Selección", "Por favor seleccione un usuario para editar")
            return
            
        VentanaUsuario(self.ventana, self, modo='editar', usuario=self.usuario_seleccionado)
        
    def eliminar_usuario(self):
        """Eliminar usuario seleccionado"""
        if not self.usuario_seleccionado:
            messagebox.showwarning("Selección", "Por favor seleccione un usuario para eliminar")
            return
            
        if self.usuario_seleccionado == 'admin':
            messagebox.showerror("Error", "No se puede eliminar el usuario administrador")
            return
            
        if messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar el usuario '{self.usuario_seleccionado}'?\n\nEsta acción no se puede deshacer."):
            del self.usuarios_db[self.usuario_seleccionado]
            messagebox.showinfo("Usuario Eliminado", f"Usuario '{self.usuario_seleccionado}' eliminado exitosamente")
            self.actualizar_lista()
            
    def toggle_estado_usuario(self):
        """Activar/desactivar usuario"""
        if not self.usuario_seleccionado:
            messagebox.showwarning("Selección", "Por favor seleccione un usuario")
            return
            
        if self.usuario_seleccionado == 'admin':
            messagebox.showerror("Error", "No se puede desactivar el usuario administrador")
            return
            
        estado_actual = self.usuarios_db[self.usuario_seleccionado]['activo']
        nuevo_estado = not estado_actual
        
        accion = "activar" if nuevo_estado else "desactivar"
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro que desea {accion} el usuario '{self.usuario_seleccionado}'?"):
            self.usuarios_db[self.usuario_seleccionado]['activo'] = nuevo_estado
            estado_texto = "activado" if nuevo_estado else "desactivado"
            messagebox.showinfo("Estado Cambiado", f"Usuario '{self.usuario_seleccionado}' {estado_texto} exitosamente")
            self.actualizar_lista()
            
    def cambiar_password(self, username):
        """Cambiar contraseña del usuario"""
        messagebox.showinfo(
            "Cambiar Contraseña",
            f"🔑 Cambio de Contraseña\n\n"
            f"Usuario: {username}\n\n"
            f"✅ Nueva contraseña generada automáticamente\n"
            f"📧 Enviada por email al usuario\n\n"
            f"[Función simulada]"
        )
        
    def gestionar_permisos(self, username):
        """Gestionar permisos del usuario"""
        VentanaPermisos(self.ventana, self, username)
        
    def generar_reporte(self):
        """Generar reporte de usuarios"""
        total = len(self.usuarios_db)
        activos = sum(1 for u in self.usuarios_db.values() if u['activo'])
        inactivos = total - activos
        admins = sum(1 for u in self.usuarios_db.values() if u['tipo'] == 'administrador')
        supervisores = sum(1 for u in self.usuarios_db.values() if u['tipo'] == 'supervisor')
        usuarios = sum(1 for u in self.usuarios_db.values() if u['tipo'] == 'usuario')
        
        messagebox.showinfo(
            "Reporte de Usuarios",
            f"📊 REPORTE DE USUARIOS\n\n"
            f"👥 Total de usuarios: {total}\n"
            f"🟢 Activos: {activos}\n"
            f"🔴 Inactivos: {inactivos}\n\n"
            f"Por tipo:\n"
            f"👑 Administradores: {admins}\n"
            f"👨‍💼 Supervisores: {supervisores}\n"
            f"👤 Usuarios: {usuarios}\n\n"
            f"📅 Fecha: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )
        
    def actualizar_lista(self):
        """Actualizar lista de usuarios"""
        self.cargar_usuarios()
        if self.usuario_seleccionado:
            self.mostrar_info_usuario(self.usuario_seleccionado)
        else:
            self.mostrar_info_vacia()

class VentanaUsuario:
    """Ventana para crear/editar usuario"""
    
    def __init__(self, parent, gestor, modo='nuevo', usuario=None):
        self.parent = parent
        self.gestor = gestor
        self.modo = modo
        self.usuario = usuario
        
        self.crear_ventana()
        
    def crear_ventana(self):
        """Crear ventana de usuario"""
        titulo = "➕ Nuevo Usuario" if self.modo == 'nuevo' else f"✏️ Editar Usuario - {self.usuario}"
        
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title(titulo)
        self.ventana.geometry("500x600")
        self.ventana.configure(bg='#f8f9fa')
        self.ventana.transient(self.parent)
        self.ventana.grab_set()
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Header
        color = "#27ae60" if self.modo == 'nuevo' else "#3498db"
        header_frame = tk.Frame(self.ventana, bg=color, height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text=titulo,
            font=('Arial', 12, 'bold'),
            fg='white',
            bg=color
        ).pack(expand=True)
        
        # Formulario
        form_frame = tk.Frame(self.ventana, bg='#f8f9fa')
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Campos del formulario
        self.crear_campos(form_frame)
        
        # Botones
        self.crear_botones()
        
        # Cargar datos si es edición
        if self.modo == 'editar' and self.usuario:
            self.cargar_datos()
            
    def centrar_ventana(self):
        """Centrar ventana"""
        self.ventana.update_idletasks()
        ancho = 500
        alto = 600
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
        
    def crear_campos(self, parent):
        """Crear campos del formulario"""
        
        # Usuario
        tk.Label(parent, text="🔑 Usuario:", font=('Arial', 10, 'bold'), bg='#f8f9fa').pack(anchor='w')
        self.entry_usuario = tk.Entry(parent, font=('Arial', 10), width=40)
        self.entry_usuario.pack(pady=(5, 15), ipady=3)
        
        # Nombre completo
        tk.Label(parent, text="👤 Nombre Completo:", font=('Arial', 10, 'bold'), bg='#f8f9fa').pack(anchor='w')
        self.entry_nombre = tk.Entry(parent, font=('Arial', 10), width=40)
        self.entry_nombre.pack(pady=(5, 15), ipady=3)
        
        # Email
        tk.Label(parent, text="📧 Email:", font=('Arial', 10, 'bold'), bg='#f8f9fa').pack(anchor='w')
        self.entry_email = tk.Entry(parent, font=('Arial', 10), width=40)
        self.entry_email.pack(pady=(5, 15), ipady=3)
        
        # Teléfono
        tk.Label(parent, text="📞 Teléfono:", font=('Arial', 10, 'bold'), bg='#f8f9fa').pack(anchor='w')
        self.entry_telefono = tk.Entry(parent, font=('Arial', 10), width=40)
        self.entry_telefono.pack(pady=(5, 15), ipady=3)
        
        # Tipo de usuario
        tk.Label(parent, text="👑 Tipo de Usuario:", font=('Arial', 10, 'bold'), bg='#f8f9fa').pack(anchor='w')
        self.combo_tipo = ttk.Combobox(parent, values=['usuario', 'supervisor', 'administrador'], state='readonly', width=37)
        self.combo_tipo.pack(pady=(5, 15))
        self.combo_tipo.set('usuario')
        
        # Contraseña (solo para nuevo usuario)
        if self.modo == 'nuevo':
            tk.Label(parent, text="🔐 Contraseña:", font=('Arial', 10, 'bold'), bg='#f8f9fa').pack(anchor='w')
            self.entry_password = tk.Entry(parent, font=('Arial', 10), width=40, show='*')
            self.entry_password.pack(pady=(5, 15), ipady=3)
            
            tk.Label(parent, text="🔐 Confirmar Contraseña:", font=('Arial', 10, 'bold'), bg='#f8f9fa').pack(anchor='w')
            self.entry_password_confirm = tk.Entry(parent, font=('Arial', 10), width=40, show='*')
            self.entry_password_confirm.pack(pady=(5, 15), ipady=3)
        
        # Estado activo
        self.var_activo = tk.BooleanVar(value=True)
        tk.Checkbutton(
            parent,
            text="✅ Usuario activo",
            variable=self.var_activo,
            font=('Arial', 10, 'bold'),
            bg='#f8f9fa'
        ).pack(anchor='w', pady=10)
        
    def crear_botones(self):
        """Crear botones del formulario"""
        buttons_frame = tk.Frame(self.ventana, bg='#f8f9fa')
        buttons_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        texto_boton = "💾 Crear Usuario" if self.modo == 'nuevo' else "💾 Guardar Cambios"
        color_boton = "#27ae60" if self.modo == 'nuevo' else "#3498db"
        
        tk.Button(
            buttons_frame,
            text=texto_boton,
            font=('Arial', 11, 'bold'),
            bg=color_boton,
            fg='white',
            relief='flat',
            command=self.guardar_usuario
        ).pack(side='left', padx=5)
        
        tk.Button(
            buttons_frame,
            text="❌ Cancelar",
            font=('Arial', 11, 'bold'),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            command=self.ventana.destroy
        ).pack(side='right', padx=5)
        
    def cargar_datos(self):
        """Cargar datos del usuario para edición"""
        if self.usuario in self.gestor.usuarios_db:
            datos = self.gestor.usuarios_db[self.usuario]
            
            self.entry_usuario.insert(0, self.usuario)
            self.entry_usuario.config(state='disabled')  # No se puede cambiar el username
            
            self.entry_nombre.insert(0, datos['nombre_completo'])
            self.entry_email.insert(0, datos['email'])
            self.entry_telefono.insert(0, datos['telefono'])
            self.combo_tipo.set(datos['tipo'])
            self.var_activo.set(datos['activo'])
            
    def guardar_usuario(self):
        """Guardar usuario (crear o editar)"""
        # Validaciones
        usuario = self.entry_usuario.get().strip()
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()
        telefono = self.entry_telefono.get().strip()
        tipo = self.combo_tipo.get()
        
        if not all([usuario, nombre, email, tipo]):
            messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
            return
            
        if self.modo == 'nuevo':
            password = self.entry_password.get()
            password_confirm = self.entry_password_confirm.get()
            
            if not password:
                messagebox.showerror("Error", "Por favor ingrese una contraseña")
                return
                
            if password != password_confirm:
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return
                
            if usuario in self.gestor.usuarios_db:
                messagebox.showerror("Error", f"El usuario '{usuario}' ya existe")
                return
        
        # Guardar usuario
        datos_usuario = {
            'nombre_completo': nombre,
            'email': email,
            'telefono': telefono,
            'tipo': tipo,
            'activo': self.var_activo.get(),
            'fecha_creacion': datetime.datetime.now().strftime('%d/%m/%Y'),
            'ultimo_acceso': 'Nunca' if self.modo == 'nuevo' else self.gestor.usuarios_db[self.usuario]['ultimo_acceso'],
            'intentos_fallidos': 0,
            'permisos': self.obtener_permisos_por_tipo(tipo)
        }
        
        self.gestor.usuarios_db[usuario] = datos_usuario
        
        accion = "creado" if self.modo == 'nuevo' else "actualizado"
        messagebox.showinfo("Éxito", f"Usuario '{usuario}' {accion} exitosamente")
        
        self.gestor.actualizar_lista()
        self.ventana.destroy()
        
    def obtener_permisos_por_tipo(self, tipo):
        """Obtener permisos por defecto según el tipo de usuario"""
        permisos_map = {
            'administrador': ['todos'],
            'supervisor': ['ventas', 'reportes', 'usuarios_consulta', 'clientes'],
            'usuario': ['ventas', 'consultas']
        }
        return permisos_map.get(tipo, ['consultas'])

class VentanaPermisos:
    """Ventana para gestionar permisos de usuario"""
    
    def __init__(self, parent, gestor, usuario):
        self.parent = parent
        self.gestor = gestor
        self.usuario = usuario
        
        self.crear_ventana()
        
    def crear_ventana(self):
        """Crear ventana de permisos"""
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title(f"🔐 Permisos - {self.usuario}")
        self.ventana.geometry("450x500")
        self.ventana.configure(bg='#f8f9fa')
        self.ventana.transient(self.parent)
        self.ventana.grab_set()
        
        self.centrar_ventana()
        
        # Header
        header_frame = tk.Frame(self.ventana, bg='#9b59b6', height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text=f"🔐 Gestión de Permisos - {self.usuario}",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#9b59b6'
        ).pack(expand=True)
        
        # Contenido
        content_frame = tk.Frame(self.ventana, bg='#f8f9fa')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            content_frame,
            text="Seleccione los permisos para el usuario:",
            font=('Arial', 11, 'bold'),
            bg='#f8f9fa'
        ).pack(anchor='w', pady=(0, 15))
        
        # Permisos disponibles
        permisos_disponibles = {
            'todos': '🔓 Acceso completo al sistema',
            'ventas': '💰 Módulo de ventas',
            'inventario': '📦 Gestión de inventario',
            'clientes': '👥 Gestión de clientes',
            'reportes': '📊 Ver y generar reportes',
            'usuarios_consulta': '👤 Consultar usuarios',
            'configuracion': '⚙️ Configuración del sistema',
            'consultas': '🔍 Solo realizar consultas'
        }
        
        # Obtener permisos actuales
        permisos_actuales = self.gestor.usuarios_db[self.usuario]['permisos']
        
        # Variables para checkboxes
        self.vars_permisos = {}
        
        for permiso, descripcion in permisos_disponibles.items():
            var = tk.BooleanVar(value=permiso in permisos_actuales)
            self.vars_permisos[permiso] = var
            
            tk.Checkbutton(
                content_frame,
                text=descripcion,
                variable=var,
                font=('Arial', 10),
                bg='#f8f9fa',
                anchor='w'
            ).pack(fill='x', pady=2)
            
        # Botones
        buttons_frame = tk.Frame(self.ventana, bg='#f8f9fa')
        buttons_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Button(
            buttons_frame,
            text="💾 Guardar Permisos",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=self.guardar_permisos
        ).pack(side='left', padx=5)
        
        tk.Button(
            buttons_frame,
            text="❌ Cancelar",
            font=('Arial', 11, 'bold'),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            command=self.ventana.destroy
        ).pack(side='right', padx=5)
        
    def centrar_ventana(self):
        """Centrar ventana"""
        self.ventana.update_idletasks()
        ancho = 450
        alto = 500
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
        
    def guardar_permisos(self):
        """Guardar permisos del usuario"""
        nuevos_permisos = [permiso for permiso, var in self.vars_permisos.items() if var.get()]
        
        if not nuevos_permisos:
            messagebox.showerror("Error", "Debe seleccionar al menos un permiso")
            return
            
        self.gestor.usuarios_db[self.usuario]['permisos'] = nuevos_permisos
        
        messagebox.showinfo("Permisos Actualizados", f"Permisos del usuario '{self.usuario}' actualizados exitosamente")
        
        self.gestor.actualizar_lista()
        self.ventana.destroy()

def main():
    """Función principal para ejecutar la aplicación"""
    print("=" * 40)
    print("🏪 SISTEMA POS - LOGIN")
    print("=" * 40)
    print("Iniciando interfaz de login...")
    print("\n👥 Usuarios disponibles:")
    print("👑 admin / 123 (Administrador)")
    print("👤 usuario1 / 123 (Usuario Normal)")
    print("=" * 40)
    
    try:
        app = LoginApp()
        app.root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        input("Presione Enter para continuar...")

if __name__ == "__main__":
    main()
