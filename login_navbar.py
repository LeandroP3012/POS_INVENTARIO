import tkinter as tk
from tkinter import messagebox, ttk, simpledialog, filedialog
import hashlib
import platform
import datetime

from controllers.credit_note_controller import CreditNoteController

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
                'nombre_completo': 'Administrador del Sistema',
                'id': 1
            },
            'usuario1': {
                'password': self.hash_password('123'),
                'tipo': 'usuario',
                'nombre_completo': 'Usuario Normal',
                'id': 2
            }
        }
        
        self.crear_interfaz()
        
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
        
        # Bind Enter key
        self.root.bind('<Return>', lambda event: self.procesar_login())
        
    def procesar_login(self):
        """Procesar intento de login"""
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get()
        tipo_seleccionado = self.tipo_usuario.get()
        
        if not usuario or not password:
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
            
        # Verificar credenciales
        if usuario in self.usuarios:
            datos_usuario = self.usuarios[usuario]
            password_hash = self.hash_password(password)
            
            if (password_hash == datos_usuario['password'] and 
                tipo_seleccionado == datos_usuario['tipo']):
                
                messagebox.showinfo(
                    "Login Exitoso", 
                    f"¡Bienvenido {datos_usuario['nombre_completo']}!\n\n"
                    f"Tipo: {datos_usuario['tipo'].title()}"
                )
                
                # Ocultar ventana de login
                self.root.withdraw()
                
                # Abrir panel correspondiente
                if datos_usuario['tipo'] == 'administrador':
                    PanelAdministrador(usuario, datos_usuario)
                else:
                    PanelUsuario(usuario, datos_usuario)
                    
            else:
                messagebox.showerror("Error de Login", "Credenciales incorrectas o tipo de usuario incorrecto")
        else:
            messagebox.showerror("Error de Login", "Usuario no encontrado")

class PanelAdministrador:
    """Panel de administrador con navbar"""
    
    def __init__(self, usuario, datos_usuario):
        self.usuario = usuario
        self.datos_usuario = datos_usuario
        self.usuario_id = datos_usuario.get('id', 2)
        self.usuario_id = datos_usuario.get('id', 1)
        
        self.root = tk.Tk()
        self.root.title(f"🏪 Sistema POS - Panel Administrador ({datos_usuario['nombre_completo']})")
        # Hacer que ocupe toda la pantalla
        self.root.state('zoomed')  # Para Windows
        self.root.configure(bg='#ecf0f1')
        self.crear_interfaz()
        self.root.mainloop()
        
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
            ("🧾", "Notas de Crédito", self.mostrar_notas_credito),
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
        
        # Crear el sistema de ventas integrado
        VentasIntegradas(self.frame_contenido)
    
    def mostrar_inventario(self):
        """Mostrar módulo de inventario"""
        self.limpiar_contenido()
        self.resaltar_boton_activo('Inventario')
        
        # Crear el sistema de inventario integrado
        InventarioIntegrado(self.frame_contenido)
    
    def mostrar_clientes(self):
        """Mostrar módulo de clientes"""
        self.limpiar_contenido()
        self.resaltar_boton_activo('Clientes')
        
        # Crear el sistema de clientes integrado
        ClientesIntegrados(self.frame_contenido)

    def mostrar_notas_credito(self):
        """Mostrar módulo de notas de crédito"""
        self.limpiar_contenido()
        self.resaltar_boton_activo('Notas de Crédito')
        CreditNotesIntegradas(self.frame_contenido, modo_basico=False, usuario_id=self.usuario_id)
    
    def mostrar_reportes(self):
        """Mostrar módulo de reportes"""
        self.limpiar_contenido()
        self.resaltar_boton_activo('Reportes')
        
        # Crear el sistema de reportes integrado
        ReportesIntegrados(self.frame_contenido)
    
    def mostrar_usuarios(self):
        """Mostrar módulo de usuarios integrado"""
        self.limpiar_contenido()
        self.resaltar_boton_activo('Usuarios')
        
        # Crear el sistema de usuarios integrado en el contenido
        GestorUsuariosIntegrado(self.frame_contenido)
    
    def mostrar_configuracion(self):
        """Mostrar módulo de configuración integrado"""
        self.limpiar_contenido()
        self.resaltar_boton_activo('Configuración')
        
        # Crear el sistema de configuración integrado en el contenido
        ConfiguracionIntegrada(self.frame_contenido)
    
    def logout(self):
        """Cerrar sesión y volver al login"""
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            self.root.destroy()
            LoginApp().root.mainloop()

class GestorUsuariosIntegrado:
    """Gestor de usuarios integrado en el panel principal"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        
        # Base de datos simulada de usuarios (expandida)
        self.usuarios_db = {
            'admin': {
                'nombre_completo': 'Administrador del Sistema',
                'email': 'admin@empresa.com',
                'telefono': '123-456-7890',
                'tipo': 'administrador',
                'activo': True,
                'fecha_creacion': '01/01/2025',
                'ultimo_acceso': '24/09/2025 14:30',
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
                'ultimo_acceso': '24/09/2025 10:15',
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
                'ultimo_acceso': '23/09/2025 18:45',
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
                'ultimo_acceso': '22/09/2025 16:20',
                'intentos_fallidos': 1,
                'permisos': ['ventas', 'reportes', 'usuarios_consulta']
            }
        }
        
        self.usuario_seleccionado = None
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crear interfaz del gestor de usuarios integrado"""
        # Título
        title_frame = tk.Frame(self.parent_frame, bg='#ecf0f1')
        title_frame.pack(fill='x', pady=(20, 20))
        
        tk.Label(
            title_frame,
            text="👤 GESTIÓN DE USUARIOS",
            font=('Arial', 24, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack()
        
        # Frame principal con dos paneles
        main_frame = tk.Frame(self.parent_frame, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, padx=20)
        
        # Panel izquierdo - Lista de usuarios
        left_panel = tk.LabelFrame(main_frame, text="👥 Lista de Usuarios", font=('Arial', 12, 'bold'), bg='#ecf0f1')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Barra de herramientas
        toolbar_frame = tk.Frame(left_panel, bg='#ecf0f1')
        toolbar_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(
            toolbar_frame,
            text="➕ Nuevo Usuario",
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=self.nuevo_usuario
        ).pack(side='left', padx=5)
        
        tk.Button(
            toolbar_frame,
            text="✏️ Editar",
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=self.editar_usuario
        ).pack(side='left', padx=5)
        
        tk.Button(
            toolbar_frame,
            text="🔒 Activar/Bloquear",
            font=('Arial', 10, 'bold'),
            bg='#f39c12',
            fg='white',
            relief='flat',
            command=self.toggle_estado_usuario
        ).pack(side='left', padx=5)
        
        tk.Button(
            toolbar_frame,
            text="🗑️ Eliminar",
            font=('Arial', 10, 'bold'),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            command=self.eliminar_usuario
        ).pack(side='left', padx=5)
        
        # Buscador
        search_frame = tk.Frame(left_panel, bg='#ecf0f1')
        search_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Label(search_frame, text="🔍 Buscar:", font=('Arial', 10), bg='#ecf0f1').pack(side='left')
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filtrar_usuarios)
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 10))
        search_entry.pack(side='left', fill='x', expand=True, padx=(5, 0))
        
        # Lista de usuarios (TreeView)
        list_frame = tk.Frame(left_panel, bg='#ecf0f1')
        list_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        columns = ('usuario', 'nombre', 'tipo', 'estado')
        self.tree_usuarios = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        # Configurar columnas
        self.tree_usuarios.heading('usuario', text='Usuario')
        self.tree_usuarios.heading('nombre', text='Nombre Completo')
        self.tree_usuarios.heading('tipo', text='Tipo')
        self.tree_usuarios.heading('estado', text='Estado')
        
        self.tree_usuarios.column('usuario', width=100)
        self.tree_usuarios.column('nombre', width=180)
        self.tree_usuarios.column('tipo', width=100)
        self.tree_usuarios.column('estado', width=80)
        
        # Scrollbar para la lista
        scrollbar_usuarios = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree_usuarios.yview)
        self.tree_usuarios.configure(yscrollcommand=scrollbar_usuarios.set)
        
        self.tree_usuarios.pack(side='left', fill='both', expand=True)
        scrollbar_usuarios.pack(side='right', fill='y')
        
        # Evento de selección
        self.tree_usuarios.bind('<<TreeviewSelect>>', self.on_usuario_select)
        
        # Panel derecho - Detalles del usuario
        right_panel = tk.LabelFrame(main_frame, text="📋 Detalles del Usuario", font=('Arial', 12, 'bold'), bg='#ecf0f1')
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Frame para información del usuario seleccionado
        self.info_frame = tk.Frame(right_panel, bg='#ecf0f1')
        self.info_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Botones inferiores
        bottom_frame = tk.Frame(self.parent_frame, bg='#ecf0f1')
        bottom_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Button(
            bottom_frame,
            text="📊 Generar Reporte",
            font=('Arial', 11, 'bold'),
            bg='#9b59b6',
            fg='white',
            relief='flat',
            command=self.generar_reporte,
            padx=15
        ).pack(side='left', padx=10)
        
        tk.Button(
            bottom_frame,
            text="🔄 Actualizar Lista",
            font=('Arial', 11, 'bold'),
            bg='#34495e',
            fg='white',
            relief='flat',
            command=self.actualizar_lista,
            padx=15
        ).pack(side='left', padx=10)
        
        # Cargar datos iniciales
        self.cargar_usuarios()
        self.mostrar_info_vacia()
    
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
                estado
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
                    estado
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
            font=('Arial', 14),
            fg='#7f8c8d',
            bg='#ecf0f1'
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
        canvas = tk.Canvas(self.info_frame, bg='#ecf0f1')
        scrollbar = ttk.Scrollbar(self.info_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ecf0f1')
        
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
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
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
            frame_info = tk.Frame(scrollable_frame, bg='#ecf0f1')
            frame_info.pack(fill='x', padx=20, pady=3)
            
            tk.Label(
                frame_info,
                text=label,
                font=('Arial', 11, 'bold'),
                bg='#ecf0f1',
                width=18,
                anchor='w'
            ).pack(side='left')
            
            tk.Label(
                frame_info,
                text=valor,
                font=('Arial', 11),
                bg='#ecf0f1',
                anchor='w'
            ).pack(side='left', fill='x', expand=True)
        
        # Permisos
        tk.Label(
            scrollable_frame,
            text="🔐 Permisos:",
            font=('Arial', 13, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(pady=(20, 10), anchor='w', padx=20)
        
        permisos_frame = tk.Frame(scrollable_frame, bg='#ecf0f1')
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
                font=('Arial', 10),
                bg='#ecf0f1',
                fg='#27ae60'
            ).pack(anchor='w')
        
        # Acciones rápidas
        tk.Label(
            scrollable_frame,
            text="⚡ Acciones Rápidas:",
            font=('Arial', 13, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(pady=(20, 10), anchor='w', padx=20)
        
        acciones_frame = tk.Frame(scrollable_frame, bg='#ecf0f1')
        acciones_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Button(
            acciones_frame,
            text="🔑 Cambiar Contraseña",
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=lambda: self.cambiar_password(username)
        ).pack(fill='x', pady=2)
        
        tk.Button(
            acciones_frame,
            text="🔐 Gestionar Permisos",
            font=('Arial', 10, 'bold'),
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
            font=('Arial', 10, 'bold'),
            bg=estado_color,
            fg='white',
            relief='flat',
            command=lambda: self.toggle_estado_usuario()
        ).pack(fill='x', pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def nuevo_usuario(self):
        """Crear nuevo usuario"""
        messagebox.showinfo("Nuevo Usuario", "🚧 Función de nuevo usuario en desarrollo...\n\nAquí se abrirá un formulario para crear un nuevo usuario.")
    
    def editar_usuario(self):
        """Editar usuario seleccionado"""
        if not self.usuario_seleccionado:
            messagebox.showwarning("Selección", "Por favor seleccione un usuario para editar")
            return
        
        messagebox.showinfo("Editar Usuario", f"🚧 Función de editar usuario en desarrollo...\n\nEditando: {self.usuario_seleccionado}")
    
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
        messagebox.showinfo(
            "Gestionar Permisos",
            f"🔐 Gestión de Permisos\n\n"
            f"Usuario: {username}\n\n"
            f"🚧 Interfaz de permisos en desarrollo...\n"
            f"Aquí se podrán asignar permisos específicos.\n\n"
            f"[Función simulada]"
        )
    
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

class ConfiguracionIntegrada:
    """Sistema de configuración integrado en el panel principal"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        
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
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crear interfaz de configuración integrada"""
        # Título
        title_frame = tk.Frame(self.parent_frame, bg='#ecf0f1')
        title_frame.pack(fill='x', pady=(20, 30))
        
        tk.Label(
            title_frame,
            text="⚙️ CONFIGURACIÓN DEL SISTEMA",
            font=('Arial', 24, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack()
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(self.parent_frame)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Crear pestañas
        self.crear_tab_empresa()
        self.crear_tab_sistema()
        self.crear_tab_impresora()
        self.crear_tab_backup()
        self.crear_tab_informacion()
        
        # Botones inferiores
        frame_botones = tk.Frame(self.parent_frame, bg='#ecf0f1')
        frame_botones.pack(fill='x', padx=20, pady=20)
        
        tk.Button(
            frame_botones,
            text="💾 Guardar Configuración",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=self.guardar_configuracion,
            padx=20,
            pady=10
        ).pack(side='left', padx=10)
        
        tk.Button(
            frame_botones,
            text="🔄 Restaurar Valores",
            font=('Arial', 12, 'bold'),
            bg='#f39c12',
            fg='white',
            relief='flat',
            command=self.restaurar_valores,
            padx=20,
            pady=10
        ).pack(side='left', padx=10)
    
    def crear_tab_empresa(self):
        """Crear pestaña de configuración de empresa"""
        frame_empresa = ttk.Frame(self.notebook)
        self.notebook.add(frame_empresa, text="🏢 Empresa")
        
        # Crear canvas y scrollbar
        canvas = tk.Canvas(frame_empresa, bg='white')
        scrollbar = ttk.Scrollbar(frame_empresa, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Campos de empresa
        self.entries_empresa = {}
        
        campos_empresa = [
            ("Nombre de la Empresa:", 'nombre'),
            ("RUC:", 'ruc'),
            ("Dirección:", 'direccion'),
            ("Teléfono:", 'telefono'),
            ("Email:", 'email')
        ]
        
        for i, (label_text, key) in enumerate(campos_empresa):
            tk.Label(
                scrollable_frame,
                text=label_text,
                font=('Arial', 11, 'bold'),
                bg='white'
            ).pack(anchor='w', padx=20, pady=(20 if i == 0 else 10, 5))
            
            entry = tk.Entry(
                scrollable_frame,
                font=('Arial', 11),
                width=50,
                bd=2,
                relief='groove'
            )
            entry.pack(padx=20, pady=(0, 10), ipady=5)
            entry.insert(0, self.config['empresa'][key])
            self.entries_empresa[key] = entry
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def crear_tab_sistema(self):
        """Crear pestaña de configuración del sistema"""
        frame_sistema = ttk.Frame(self.notebook)
        self.notebook.add(frame_sistema, text="🖥️ Sistema")
        
        # Crear canvas y scrollbar
        canvas = tk.Canvas(frame_sistema, bg='white')
        scrollbar = ttk.Scrollbar(frame_sistema, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Campos de sistema
        self.entries_sistema = {}
        
        # Moneda
        tk.Label(
            scrollable_frame,
            text="Moneda:",
            font=('Arial', 11, 'bold'),
            bg='white'
        ).pack(anchor='w', padx=20, pady=(20, 5))
        
        combo_moneda = ttk.Combobox(
            scrollable_frame,
            values=['PEN', 'USD', 'EUR'],
            state='readonly',
            width=47
        )
        combo_moneda.pack(padx=20, pady=(0, 10))
        combo_moneda.set(self.config['sistema']['moneda'])
        self.entries_sistema['moneda'] = combo_moneda
        
        # Símbolo de moneda
        tk.Label(
            scrollable_frame,
            text="Símbolo de Moneda:",
            font=('Arial', 11, 'bold'),
            bg='white'
        ).pack(anchor='w', padx=20, pady=(10, 5))
        
        entry_simbolo = tk.Entry(
            scrollable_frame,
            font=('Arial', 11),
            width=50,
            bd=2,
            relief='groove'
        )
        entry_simbolo.pack(padx=20, pady=(0, 10), ipady=5)
        entry_simbolo.insert(0, self.config['sistema']['simbolo_moneda'])
        self.entries_sistema['simbolo_moneda'] = entry_simbolo
        
        # IGV
        tk.Label(
            scrollable_frame,
            text="IGV (%):",
            font=('Arial', 11, 'bold'),
            bg='white'
        ).pack(anchor='w', padx=20, pady=(10, 5))
        
        entry_igv = tk.Entry(
            scrollable_frame,
            font=('Arial', 11),
            width=50,
            bd=2,
            relief='groove'
        )
        entry_igv.pack(padx=20, pady=(0, 10), ipady=5)
        entry_igv.insert(0, str(self.config['sistema']['igv']))
        self.entries_sistema['igv'] = entry_igv
        
        # Decimales
        tk.Label(
            scrollable_frame,
            text="Decimales:",
            font=('Arial', 11, 'bold'),
            bg='white'
        ).pack(anchor='w', padx=20, pady=(10, 5))
        
        combo_decimales = ttk.Combobox(
            scrollable_frame,
            values=['0', '1', '2', '3', '4'],
            state='readonly',
            width=47
        )
        combo_decimales.pack(padx=20, pady=(0, 10))
        combo_decimales.set(str(self.config['sistema']['decimales']))
        self.entries_sistema['decimales'] = combo_decimales
        
        # Tema
        tk.Label(
            scrollable_frame,
            text="Tema:",
            font=('Arial', 11, 'bold'),
            bg='white'
        ).pack(anchor='w', padx=20, pady=(10, 5))
        
        combo_tema = ttk.Combobox(
            scrollable_frame,
            values=['Claro', 'Oscuro', 'Azul', 'Verde'],
            state='readonly',
            width=47
        )
        combo_tema.pack(padx=20, pady=(0, 20))
        combo_tema.set(self.config['sistema']['tema'])
        self.entries_sistema['tema'] = combo_tema
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def crear_tab_impresora(self):
        """Crear pestaña de configuración de impresora"""
        frame_impresora = ttk.Frame(self.notebook)
        self.notebook.add(frame_impresora, text="🖨️ Impresora")
        
        # Crear canvas y scrollbar
        canvas = tk.Canvas(frame_impresora, bg='white')
        scrollbar = ttk.Scrollbar(frame_impresora, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        self.entries_impresora = {}
        
        # Nombre de impresora
        tk.Label(
            scrollable_frame,
            text="Nombre de Impresora:",
            font=('Arial', 11, 'bold'),
            bg='white'
        ).pack(anchor='w', padx=20, pady=(20, 5))
        
        entry_nombre = tk.Entry(
            scrollable_frame,
            font=('Arial', 11),
            width=50,
            bd=2,
            relief='groove'
        )
        entry_nombre.pack(padx=20, pady=(0, 10), ipady=5)
        entry_nombre.insert(0, self.config['impresora']['nombre'])
        self.entries_impresora['nombre'] = entry_nombre
        
        # Tipo de impresora
        tk.Label(
            scrollable_frame,
            text="Tipo de Impresora:",
            font=('Arial', 11, 'bold'),
            bg='white'
        ).pack(anchor='w', padx=20, pady=(10, 5))
        
        combo_tipo = ttk.Combobox(
            scrollable_frame,
            values=['Térmica', 'Láser', 'Inyección de tinta', 'Matriz de puntos'],
            state='readonly',
            width=47
        )
        combo_tipo.pack(padx=20, pady=(0, 10))
        combo_tipo.set(self.config['impresora']['tipo'])
        self.entries_impresora['tipo'] = combo_tipo
        
        # Ancho de papel
        tk.Label(
            scrollable_frame,
            text="Ancho de Papel:",
            font=('Arial', 11, 'bold'),
            bg='white'
        ).pack(anchor='w', padx=20, pady=(10, 5))
        
        combo_ancho = ttk.Combobox(
            scrollable_frame,
            values=['58mm', '80mm', 'A4', 'Letter'],
            state='readonly',
            width=47
        )
        combo_ancho.pack(padx=20, pady=(0, 10))
        combo_ancho.set(self.config['impresora']['ancho_papel'])
        self.entries_impresora['ancho_papel'] = combo_ancho
        
        # Pie de página
        tk.Label(
            scrollable_frame,
            text="Pie de Página:",
            font=('Arial', 11, 'bold'),
            bg='white'
        ).pack(anchor='w', padx=20, pady=(10, 5))
        
        text_pie = tk.Text(
            scrollable_frame,
            font=('Arial', 11),
            width=50,
            height=4,
            bd=2,
            relief='groove'
        )
        text_pie.pack(padx=20, pady=(0, 20))
        text_pie.insert('1.0', self.config['impresora']['pie_pagina'])
        self.entries_impresora['pie_pagina'] = text_pie
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def crear_tab_backup(self):
        """Crear pestaña de configuración de backup"""
        frame_backup = ttk.Frame(self.notebook)
        self.notebook.add(frame_backup, text="💾 Backup")
        
        # Crear canvas y scrollbar
        canvas = tk.Canvas(frame_backup, bg='white')
        scrollbar = ttk.Scrollbar(frame_backup, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        self.entries_backup = {}
        
        # Backup automático
        self.var_backup_auto = tk.BooleanVar(value=self.config['backup']['automatico'])
        
        check_auto = tk.Checkbutton(
            scrollable_frame,
            text="Realizar backup automático",
            variable=self.var_backup_auto,
            font=('Arial', 11, 'bold'),
            bg='white'
        )
        check_auto.pack(anchor='w', padx=20, pady=(20, 10))
        
        # Frecuencia
        tk.Label(
            scrollable_frame,
            text="Frecuencia:",
            font=('Arial', 11, 'bold'),
            bg='white'
        ).pack(anchor='w', padx=20, pady=(10, 5))
        
        combo_frecuencia = ttk.Combobox(
            scrollable_frame,
            values=['Diario', 'Semanal', 'Mensual'],
            state='readonly',
            width=47
        )
        combo_frecuencia.pack(padx=20, pady=(0, 10))
        combo_frecuencia.set(self.config['backup']['frecuencia'])
        self.entries_backup['frecuencia'] = combo_frecuencia
        
        # Hora
        tk.Label(
            scrollable_frame,
            text="Hora:",
            font=('Arial', 11, 'bold'),
            bg='white'
        ).pack(anchor='w', padx=20, pady=(10, 5))
        
        entry_hora = tk.Entry(
            scrollable_frame,
            font=('Arial', 11),
            width=50,
            bd=2,
            relief='groove'
        )
        entry_hora.pack(padx=20, pady=(0, 10), ipady=5)
        entry_hora.insert(0, self.config['backup']['hora'])
        self.entries_backup['hora'] = entry_hora
        
        # Ubicación
        tk.Label(
            scrollable_frame,
            text="Ubicación:",
            font=('Arial', 11, 'bold'),
            bg='white'
        ).pack(anchor='w', padx=20, pady=(10, 5))
        
        frame_ubicacion = tk.Frame(scrollable_frame, bg='white')
        frame_ubicacion.pack(fill='x', padx=20, pady=(0, 10))
        
        entry_ubicacion = tk.Entry(
            frame_ubicacion,
            font=('Arial', 11),
            bd=2,
            relief='groove'
        )
        entry_ubicacion.pack(side='left', fill='x', expand=True, ipady=5)
        entry_ubicacion.insert(0, self.config['backup']['ubicacion'])
        self.entries_backup['ubicacion'] = entry_ubicacion
        
        tk.Button(
            frame_ubicacion,
            text="📁 Explorar",
            font=('Arial', 9),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=lambda: self.seleccionar_carpeta_backup(entry_ubicacion)
        ).pack(side='right', padx=(10, 0))
        
        # Botones de backup
        frame_botones_backup = tk.Frame(scrollable_frame, bg='white')
        frame_botones_backup.pack(fill='x', padx=20, pady=(20, 20))
        
        tk.Button(
            frame_botones_backup,
            text="💾 Realizar Backup Ahora",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=self.realizar_backup_manual
        ).pack(side='left', padx=5)
        
        tk.Button(
            frame_botones_backup,
            text="📂 Restaurar Backup",
            font=('Arial', 11, 'bold'),
            bg='#e67e22',
            fg='white',
            relief='flat',
            command=self.restaurar_backup
        ).pack(side='left', padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def crear_tab_informacion(self):
        """Crear pestaña de información del sistema"""
        frame_info = ttk.Frame(self.notebook)
        self.notebook.add(frame_info, text="ℹ️ Información")
        
        # Crear canvas y scrollbar
        canvas = tk.Canvas(frame_info, bg='white')
        scrollbar = ttk.Scrollbar(frame_info, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Título
        tk.Label(
            scrollable_frame,
            text="📊 Información del Sistema",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(pady=20)
        
        # Información del sistema
        info_items = [
            ("🏪 Sistema:", "POS - Punto de Venta"),
            ("📅 Versión:", "2.0.0"),
            ("👨‍💻 Desarrollador:", "Tu Empresa"),
            ("📅 Fecha:", datetime.datetime.now().strftime('%d/%m/%Y')),
            ("🕐 Hora:", datetime.datetime.now().strftime('%H:%M:%S')),
            ("💻 Sistema Operativo:", f"{platform.system()} {platform.release()}"),
            ("🐍 Python:", platform.python_version()),
            ("🖥️ Arquitectura:", platform.architecture()[0]),
            ("🏷️ Nombre del Equipo:", platform.node()),
            ("👤 Usuario:", platform.node())
        ]
        
        for label, valor in info_items:
            frame_item = tk.Frame(scrollable_frame, bg='white')
            frame_item.pack(fill='x', padx=40, pady=5)
            
            tk.Label(
                frame_item,
                text=label,
                font=('Arial', 11, 'bold'),
                bg='white',
                width=20,
                anchor='w'
            ).pack(side='left')
            
            tk.Label(
                frame_item,
                text=valor,
                font=('Arial', 11),
                bg='white',
                anchor='w'
            ).pack(side='left', fill='x', expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def seleccionar_carpeta_backup(self, entry_widget):
        """Seleccionar carpeta para backup"""
        from tkinter import filedialog
        carpeta = filedialog.askdirectory(
            title="Seleccionar carpeta para backup",
            initialdir=entry_widget.get()
        )
        if carpeta:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, carpeta)
    
    def realizar_backup_manual(self):
        """Realizar backup manual"""
        messagebox.showinfo(
            "Backup Manual", 
            "💾 Backup Manual\n\n"
            "✅ Backup realizado exitosamente\n"
            f"📅 Fecha: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
            f"📁 Ubicación: {self.config['backup']['ubicacion']}\n\n"
            "[Función simulada]"
        )
    
    def restaurar_backup(self):
        """Restaurar desde backup"""
        if messagebox.askyesno("Restaurar Backup", "⚠️ ¿Está seguro que desea restaurar desde un backup?\n\nEsta acción reemplazará los datos actuales."):
            messagebox.showinfo(
                "Restaurar Backup",
                "📂 Restauración de Backup\n\n"
                "✅ Datos restaurados exitosamente\n"
                f"📅 Fecha: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
                "[Función simulada]"
            )
    
    def guardar_configuracion(self):
        """Guardar configuración"""
        try:
            # Actualizar configuración desde los campos
            self.config['empresa']['nombre'] = self.entries_empresa['nombre'].get()
            self.config['empresa']['ruc'] = self.entries_empresa['ruc'].get()
            self.config['empresa']['direccion'] = self.entries_empresa['direccion'].get()
            self.config['empresa']['telefono'] = self.entries_empresa['telefono'].get()
            self.config['empresa']['email'] = self.entries_empresa['email'].get()
            
            self.config['sistema']['moneda'] = self.entries_sistema['moneda'].get()
            self.config['sistema']['simbolo_moneda'] = self.entries_sistema['simbolo_moneda'].get()
            self.config['sistema']['igv'] = float(self.entries_sistema['igv'].get())
            self.config['sistema']['decimales'] = int(self.entries_sistema['decimales'].get())
            self.config['sistema']['tema'] = self.entries_sistema['tema'].get()
            
            self.config['impresora']['nombre'] = self.entries_impresora['nombre'].get()
            self.config['impresora']['tipo'] = self.entries_impresora['tipo'].get()
            self.config['impresora']['ancho_papel'] = self.entries_impresora['ancho_papel'].get()
            self.config['impresora']['pie_pagina'] = self.entries_impresora['pie_pagina'].get('1.0', tk.END).strip()
            
            self.config['backup']['automatico'] = self.var_backup_auto.get()
            self.config['backup']['frecuencia'] = self.entries_backup['frecuencia'].get()
            self.config['backup']['hora'] = self.entries_backup['hora'].get()
            self.config['backup']['ubicacion'] = self.entries_backup['ubicacion'].get()
            
            messagebox.showinfo("Configuración Guardada", "✅ Configuración guardada exitosamente")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los datos ingresados: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar configuración: {str(e)}")
    
    def restaurar_valores(self):
        """Restaurar valores por defecto"""
        if messagebox.askyesno("Restaurar Valores", "¿Está seguro que desea restaurar los valores por defecto?"):
            # Restaurar valores por defecto
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
            
            # Actualizar campos
            self.actualizar_campos()
            messagebox.showinfo("Valores Restaurados", "🔄 Valores por defecto restaurados")
    
    def actualizar_campos(self):
        """Actualizar campos con los valores actuales"""
        # Empresa
        for key, entry in self.entries_empresa.items():
            entry.delete(0, tk.END)
            entry.insert(0, self.config['empresa'][key])
        
        # Sistema
        self.entries_sistema['moneda'].set(self.config['sistema']['moneda'])
        self.entries_sistema['simbolo_moneda'].delete(0, tk.END)
        self.entries_sistema['simbolo_moneda'].insert(0, self.config['sistema']['simbolo_moneda'])
        self.entries_sistema['igv'].delete(0, tk.END)
        self.entries_sistema['igv'].insert(0, str(self.config['sistema']['igv']))
        self.entries_sistema['decimales'].set(str(self.config['sistema']['decimales']))
        self.entries_sistema['tema'].set(self.config['sistema']['tema'])
        
        # Impresora
        self.entries_impresora['nombre'].delete(0, tk.END)
        self.entries_impresora['nombre'].insert(0, self.config['impresora']['nombre'])
        self.entries_impresora['tipo'].set(self.config['impresora']['tipo'])
        self.entries_impresora['ancho_papel'].set(self.config['impresora']['ancho_papel'])
        self.entries_impresora['pie_pagina'].delete('1.0', tk.END)
        self.entries_impresora['pie_pagina'].insert('1.0', self.config['impresora']['pie_pagina'])
        
        # Backup
        self.var_backup_auto.set(self.config['backup']['automatico'])
        self.entries_backup['frecuencia'].set(self.config['backup']['frecuencia'])
        self.entries_backup['hora'].delete(0, tk.END)
        self.entries_backup['hora'].insert(0, self.config['backup']['hora'])
        self.entries_backup['ubicacion'].delete(0, tk.END)
        self.entries_backup['ubicacion'].insert(0, self.config['backup']['ubicacion'])

class VentasIntegradas:
    """Sistema de ventas integrado en el panel principal"""
    
    def __init__(self, parent_frame, modo_usuario=False):
        self.parent_frame = parent_frame
        self.modo_usuario = modo_usuario
        
        # Base de datos simulada de productos
        self.productos_db = {
            'P001': {'nombre': 'Coca Cola 2L', 'precio': 5.50, 'stock': 25, 'categoria': 'Bebidas'},
            'P002': {'nombre': 'Pan Integral', 'precio': 3.25, 'stock': 12, 'categoria': 'Panadería'},
            'P003': {'nombre': 'Leche Entera 1L', 'precio': 4.80, 'stock': 18, 'categoria': 'Lácteos'},
            'P004': {'nombre': 'Arroz 1kg', 'precio': 2.75, 'stock': 30, 'categoria': 'Granos'},
            'P005': {'nombre': 'Aceite Girasol 1L', 'precio': 6.90, 'stock': 8, 'categoria': 'Aceites'},
            'P006': {'nombre': 'Jabón Líquido', 'precio': 4.50, 'stock': 15, 'categoria': 'Limpieza'}
        }
        
        self.carrito = []
        self.total_venta = 0.0
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crear interfaz de ventas"""
        # Título
        titulo = "💰 REALIZAR VENTA" if self.modo_usuario else "💰 MÓDULO DE VENTAS"
        tk.Label(
            self.parent_frame,
            text=titulo,
            font=('Arial', 22, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(pady=(20, 30))
        
        # Frame principal dividido
        main_frame = tk.Frame(self.parent_frame, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Panel izquierdo - Productos
        left_panel = tk.LabelFrame(main_frame, text="📦 Productos Disponibles", font=('Arial', 12, 'bold'))
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Buscador de productos
        search_frame = tk.Frame(left_panel)
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_frame, text="🔍 Buscar:", font=('Arial', 10)).pack(side='left')
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filtrar_productos)
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 10))
        search_entry.pack(side='left', fill='x', expand=True, padx=(5, 0))
        
        # Lista de productos
        productos_frame = tk.Frame(left_panel)
        productos_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        columns = ('codigo', 'nombre', 'precio', 'stock', 'categoria')
        self.tree_productos = ttk.Treeview(productos_frame, columns=columns, show='headings', height=12)
        
        self.tree_productos.heading('codigo', text='Código')
        self.tree_productos.heading('nombre', text='Producto')
        self.tree_productos.heading('precio', text='Precio')
        self.tree_productos.heading('stock', text='Stock')
        self.tree_productos.heading('categoria', text='Categoría')
        
        self.tree_productos.column('codigo', width=80)
        self.tree_productos.column('nombre', width=150)
        self.tree_productos.column('precio', width=80)
        self.tree_productos.column('stock', width=60)
        self.tree_productos.column('categoria', width=100)
        
        # Scrollbar para productos
        scrollbar_productos = ttk.Scrollbar(productos_frame, orient='vertical', command=self.tree_productos.yview)
        self.tree_productos.configure(yscrollcommand=scrollbar_productos.set)
        
        self.tree_productos.pack(side='left', fill='both', expand=True)
        scrollbar_productos.pack(side='right', fill='y')
        
        # Botón agregar al carrito
        tk.Button(
            left_panel,
            text="➕ Agregar al Carrito",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=self.agregar_al_carrito
        ).pack(pady=10)
        
        # Panel derecho - Carrito y venta
        right_panel = tk.LabelFrame(main_frame, text="🛒 Carrito de Compras", font=('Arial', 12, 'bold'))
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Lista del carrito
        carrito_frame = tk.Frame(right_panel)
        carrito_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns_carrito = ('producto', 'cantidad', 'precio_unit', 'subtotal')
        self.tree_carrito = ttk.Treeview(carrito_frame, columns=columns_carrito, show='headings', height=10)
        
        self.tree_carrito.heading('producto', text='Producto')
        self.tree_carrito.heading('cantidad', text='Cant.')
        self.tree_carrito.heading('precio_unit', text='Precio Unit.')
        self.tree_carrito.heading('subtotal', text='Subtotal')
        
        self.tree_carrito.column('producto', width=120)
        self.tree_carrito.column('cantidad', width=60)
        self.tree_carrito.column('precio_unit', width=80)
        self.tree_carrito.column('subtotal', width=80)
        
        # Scrollbar para carrito
        scrollbar_carrito = ttk.Scrollbar(carrito_frame, orient='vertical', command=self.tree_carrito.yview)
        self.tree_carrito.configure(yscrollcommand=scrollbar_carrito.set)
        
        self.tree_carrito.pack(side='left', fill='both', expand=True)
        scrollbar_carrito.pack(side='right', fill='y')
        
        # Botones del carrito
        botones_carrito = tk.Frame(right_panel)
        botones_carrito.pack(fill='x', padx=10, pady=5)
        
        tk.Button(
            botones_carrito,
            text="🗑️ Quitar",
            font=('Arial', 10, 'bold'),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            command=self.quitar_del_carrito
        ).pack(side='left', padx=2)
        
        tk.Button(
            botones_carrito,
            text="🧹 Limpiar Todo",
            font=('Arial', 10, 'bold'),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            command=self.limpiar_carrito
        ).pack(side='left', padx=2)
        
        # Total
        total_frame = tk.Frame(right_panel, bg='#2c3e50')
        total_frame.pack(fill='x', padx=10, pady=10)
        
        self.label_total = tk.Label(
            total_frame,
            text="💰 TOTAL: $0.00",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        self.label_total.pack(pady=10)
        
        # Botón de venta
        tk.Button(
            right_panel,
            text="💳 PROCESAR VENTA",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=self.procesar_venta,
            height=2
        ).pack(fill='x', padx=10, pady=10)
        
        # Cargar productos iniciales
        self.cargar_productos()
    
    def cargar_productos(self):
        """Cargar productos en la tabla"""
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
            
        for codigo, datos in self.productos_db.items():
            self.tree_productos.insert('', 'end', values=(
                codigo,
                datos['nombre'],
                f"${datos['precio']:.2f}",
                datos['stock'],
                datos['categoria']
            ))
    
    def filtrar_productos(self, *args):
        """Filtrar productos por búsqueda"""
        busqueda = self.search_var.get().lower()
        
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
            
        for codigo, datos in self.productos_db.items():
            if (busqueda in codigo.lower() or 
                busqueda in datos['nombre'].lower() or
                busqueda in datos['categoria'].lower()):
                
                self.tree_productos.insert('', 'end', values=(
                    codigo,
                    datos['nombre'],
                    f"${datos['precio']:.2f}",
                    datos['stock'],
                    datos['categoria']
                ))
    
    def agregar_al_carrito(self):
        """Agregar producto seleccionado al carrito"""
        selection = self.tree_productos.selection()
        if not selection:
            messagebox.showwarning("Selección", "Por favor seleccione un producto")
            return
            
        item = self.tree_productos.item(selection[0])
        codigo = item['values'][0]
        
        if codigo not in self.productos_db:
            return
            
        producto = self.productos_db[codigo]
        
        if producto['stock'] <= 0:
            messagebox.showerror("Sin Stock", f"El producto {producto['nombre']} no tiene stock disponible")
            return
        
        # Solicitar cantidad
        cantidad_str = tk.simpledialog.askstring(
            "Cantidad",
            f"Ingrese la cantidad para {producto['nombre']}:",
            initialvalue="1"
        )
        
        if not cantidad_str:
            return
            
        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida")
            return
            
        if cantidad > producto['stock']:
            messagebox.showerror("Stock Insuficiente", f"Solo hay {producto['stock']} unidades disponibles")
            return
        
        # Buscar si ya existe en el carrito
        for i, item_carrito in enumerate(self.carrito):
            if item_carrito['codigo'] == codigo:
                nueva_cantidad = item_carrito['cantidad'] + cantidad
                if nueva_cantidad > producto['stock']:
                    messagebox.showerror("Stock Insuficiente", f"Total excede el stock disponible ({producto['stock']} unidades)")
                    return
                self.carrito[i]['cantidad'] = nueva_cantidad
                self.carrito[i]['subtotal'] = nueva_cantidad * producto['precio']
                break
        else:
            # Agregar nuevo item al carrito
            self.carrito.append({
                'codigo': codigo,
                'nombre': producto['nombre'],
                'cantidad': cantidad,
                'precio_unit': producto['precio'],
                'subtotal': cantidad * producto['precio']
            })
        
        self.actualizar_carrito()
    
    def actualizar_carrito(self):
        """Actualizar vista del carrito"""
        # Limpiar carrito
        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)
            
        # Agregar items del carrito
        self.total_venta = 0
        for item in self.carrito:
            self.tree_carrito.insert('', 'end', values=(
                item['nombre'],
                item['cantidad'],
                f"${item['precio_unit']:.2f}",
                f"${item['subtotal']:.2f}"
            ))
            self.total_venta += item['subtotal']
        
        # Actualizar total
        self.label_total.config(text=f"💰 TOTAL: ${self.total_venta:.2f}")
    
    def quitar_del_carrito(self):
        """Quitar item seleccionado del carrito"""
        selection = self.tree_carrito.selection()
        if not selection:
            messagebox.showwarning("Selección", "Por favor seleccione un item del carrito")
            return
            
        item_index = self.tree_carrito.index(selection[0])
        self.carrito.pop(item_index)
        self.actualizar_carrito()
    
    def limpiar_carrito(self):
        """Limpiar todo el carrito"""
        if self.carrito and messagebox.askyesno("Confirmar", "¿Está seguro que desea limpiar todo el carrito?"):
            self.carrito.clear()
            self.actualizar_carrito()
    
    def procesar_venta(self):
        """Procesar la venta"""
        if not self.carrito:
            messagebox.showwarning("Carrito Vacío", "Agregue productos al carrito antes de procesar la venta")
            return
        
        # Simular procesamiento de venta
        venta_id = f"V{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Actualizar stock (simulado)
        for item in self.carrito:
            codigo = item['codigo']
            if codigo in self.productos_db:
                self.productos_db[codigo]['stock'] -= item['cantidad']
        
        # Mostrar comprobante
        comprobante = f"🧾 COMPROBANTE DE VENTA\n\n"
        comprobante += f"Venta ID: {venta_id}\n"
        comprobante += f"Fecha: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        comprobante += f"{'='*40}\n\n"
        
        for item in self.carrito:
            comprobante += f"{item['nombre']}\n"
            comprobante += f"  {item['cantidad']} x ${item['precio_unit']:.2f} = ${item['subtotal']:.2f}\n\n"
        
        comprobante += f"{'='*40}\n"
        comprobante += f"TOTAL: ${self.total_venta:.2f}\n\n"
        comprobante += "¡Gracias por su compra!"
        
        messagebox.showinfo("Venta Procesada", comprobante)
        
        # Limpiar carrito
        self.carrito.clear()
        self.actualizar_carrito()
        self.cargar_productos()  # Actualizar stock en la vista

class InventarioIntegrado:
    """Sistema de inventario integrado en el panel principal"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        
        # Base de datos simulada de productos (expandida)
        self.productos_db = {
            'P001': {'nombre': 'Coca Cola 2L', 'precio': 5.50, 'stock': 25, 'categoria': 'Bebidas', 'proveedor': 'Coca-Cola Company', 'stock_min': 10},
            'P002': {'nombre': 'Pan Integral', 'precio': 3.25, 'stock': 12, 'categoria': 'Panadería', 'proveedor': 'Panadería Central', 'stock_min': 5},
            'P003': {'nombre': 'Leche Entera 1L', 'precio': 4.80, 'stock': 18, 'categoria': 'Lácteos', 'proveedor': 'Lácteos del Valle', 'stock_min': 8},
            'P004': {'nombre': 'Arroz 1kg', 'precio': 2.75, 'stock': 30, 'categoria': 'Granos', 'proveedor': 'Granos y Cereales SA', 'stock_min': 15},
            'P005': {'nombre': 'Aceite Girasol 1L', 'precio': 6.90, 'stock': 8, 'categoria': 'Aceites', 'proveedor': 'Aceites Premium', 'stock_min': 12},
            'P006': {'nombre': 'Jabón Líquido', 'precio': 4.50, 'stock': 15, 'categoria': 'Limpieza', 'proveedor': 'Productos de Limpieza XYZ', 'stock_min': 6}
        }
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crear interfaz de inventario"""
        # Título
        tk.Label(
            self.parent_frame,
            text="📦 GESTIÓN DE INVENTARIO",
            font=('Arial', 22, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(pady=(20, 30))
        
        # Toolbar
        toolbar_frame = tk.Frame(self.parent_frame, bg='#ecf0f1')
        toolbar_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(
            toolbar_frame,
            text="➕ Nuevo Producto",
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            command=self.nuevo_producto
        ).pack(side='left', padx=2)
        
        tk.Button(
            toolbar_frame,
            text="✏️ Editar",
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=self.editar_producto
        ).pack(side='left', padx=2)
        
        tk.Button(
            toolbar_frame,
            text="🗑️ Eliminar",
            font=('Arial', 10, 'bold'),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            command=self.eliminar_producto
        ).pack(side='left', padx=2)
        
        tk.Button(
            toolbar_frame,
            text="📊 Stock Bajo",
            font=('Arial', 10, 'bold'),
            bg='#f39c12',
            fg='white',
            relief='flat',
            command=self.mostrar_stock_bajo
        ).pack(side='left', padx=2)
        
        # Buscador
        search_frame = tk.Frame(self.parent_frame, bg='#ecf0f1')
        search_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(search_frame, text="🔍 Buscar:", font=('Arial', 10), bg='#ecf0f1').pack(side='left')
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filtrar_productos)
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 10))
        search_entry.pack(side='left', fill='x', expand=True, padx=(5, 0))
        
        # Lista de productos
        lista_frame = tk.Frame(self.parent_frame)
        lista_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('codigo', 'nombre', 'precio', 'stock', 'stock_min', 'categoria', 'proveedor', 'estado')
        self.tree_productos = ttk.Treeview(lista_frame, columns=columns, show='headings', height=15)
        
        self.tree_productos.heading('codigo', text='Código')
        self.tree_productos.heading('nombre', text='Producto')
        self.tree_productos.heading('precio', text='Precio')
        self.tree_productos.heading('stock', text='Stock')
        self.tree_productos.heading('stock_min', text='Stock Mín.')
        self.tree_productos.heading('categoria', text='Categoría')
        self.tree_productos.heading('proveedor', text='Proveedor')
        self.tree_productos.heading('estado', text='Estado')
        
        self.tree_productos.column('codigo', width=80)
        self.tree_productos.column('nombre', width=150)
        self.tree_productos.column('precio', width=80)
        self.tree_productos.column('stock', width=60)
        self.tree_productos.column('stock_min', width=80)
        self.tree_productos.column('categoria', width=100)
        self.tree_productos.column('proveedor', width=150)
        self.tree_productos.column('estado', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(lista_frame, orient='vertical', command=self.tree_productos.yview)
        self.tree_productos.configure(yscrollcommand=scrollbar.set)
        
        self.tree_productos.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Estadísticas
        stats_frame = tk.Frame(self.parent_frame, bg='#ecf0f1')
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        self.actualizar_estadisticas(stats_frame)
        
        # Cargar productos
        self.cargar_productos()
    
    def cargar_productos(self):
        """Cargar productos en la tabla"""
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
            
        for codigo, datos in self.productos_db.items():
            estado = "🔴 Stock Bajo" if datos['stock'] <= datos['stock_min'] else "🟢 Normal"
            
            self.tree_productos.insert('', 'end', values=(
                codigo,
                datos['nombre'],
                f"${datos['precio']:.2f}",
                datos['stock'],
                datos['stock_min'],
                datos['categoria'],
                datos['proveedor'],
                estado
            ))
    
    def filtrar_productos(self, *args):
        """Filtrar productos por búsqueda"""
        busqueda = self.search_var.get().lower()
        
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
            
        for codigo, datos in self.productos_db.items():
            if (busqueda in codigo.lower() or 
                busqueda in datos['nombre'].lower() or
                busqueda in datos['categoria'].lower() or
                busqueda in datos['proveedor'].lower()):
                
                estado = "🔴 Stock Bajo" if datos['stock'] <= datos['stock_min'] else "🟢 Normal"
                
                self.tree_productos.insert('', 'end', values=(
                    codigo,
                    datos['nombre'],
                    f"${datos['precio']:.2f}",
                    datos['stock'],
                    datos['stock_min'],
                    datos['categoria'],
                    datos['proveedor'],
                    estado
                ))
    
    def actualizar_estadisticas(self, parent):
        """Actualizar estadísticas del inventario"""
        # Limpiar estadísticas anteriores
        for widget in parent.winfo_children():
            widget.destroy()
        
        total_productos = len(self.productos_db)
        stock_bajo = sum(1 for p in self.productos_db.values() if p['stock'] <= p['stock_min'])
        valor_total = sum(p['precio'] * p['stock'] for p in self.productos_db.values())
        
        stats = [
            ("📦 Total Productos", str(total_productos), "#3498db"),
            ("⚠️ Stock Bajo", str(stock_bajo), "#e74c3c"),
            ("💰 Valor Inventario", f"${valor_total:.2f}", "#27ae60")
        ]
        
        for titulo, valor, color in stats:
            card = tk.Frame(parent, bg=color, relief='raised', bd=2)
            card.pack(side='left', fill='x', expand=True, padx=5)
            
            tk.Label(card, text=titulo, font=('Arial', 10, 'bold'), fg='white', bg=color).pack(pady=(10, 5))
            tk.Label(card, text=valor, font=('Arial', 12, 'bold'), fg='white', bg=color).pack(pady=(0, 10))
    
    def nuevo_producto(self):
        """Agregar nuevo producto"""
        messagebox.showinfo("Nuevo Producto", "🚧 Función de agregar producto en desarrollo...")
    
    def editar_producto(self):
        """Editar producto seleccionado"""
        selection = self.tree_productos.selection()
        if not selection:
            messagebox.showwarning("Selección", "Por favor seleccione un producto para editar")
            return
        messagebox.showinfo("Editar Producto", "🚧 Función de editar producto en desarrollo...")
    
    def eliminar_producto(self):
        """Eliminar producto seleccionado"""
        selection = self.tree_productos.selection()
        if not selection:
            messagebox.showwarning("Selección", "Por favor seleccione un producto para eliminar")
            return
        messagebox.showinfo("Eliminar Producto", "🚧 Función de eliminar producto en desarrollo...")
    
    def mostrar_stock_bajo(self):
        """Mostrar productos con stock bajo"""
        productos_bajo = [codigo for codigo, datos in self.productos_db.items() 
                         if datos['stock'] <= datos['stock_min']]
        
        if not productos_bajo:
            messagebox.showinfo("Stock", "✅ Todos los productos tienen stock suficiente")
            return
        
        mensaje = "⚠️ PRODUCTOS CON STOCK BAJO:\n\n"
        for codigo in productos_bajo:
            datos = self.productos_db[codigo]
            mensaje += f"• {datos['nombre']} (Stock: {datos['stock']}, Mín: {datos['stock_min']})\n"
        
        messagebox.showwarning("Stock Bajo", mensaje)

class ClientesIntegrados:
    """Sistema de clientes integrado en el panel principal"""
    
    def __init__(self, parent_frame, modo_consulta=False):
        self.parent_frame = parent_frame
        self.modo_consulta = modo_consulta
        
        # Base de datos simulada de clientes
        self.clientes_db = {
            'C001': {
                'nombre': 'Juan Pérez García',
                'email': 'juan.perez@email.com',
                'telefono': '123-456-7890',
                'direccion': 'Av. Principal 123, Ciudad',
                'fecha_registro': '15/01/2025',
                'total_compras': 1250.75,
                'compras_realizadas': 12,
                'estado': 'Activo'
            },
            'C002': {
                'nombre': 'María López Rodríguez',
                'email': 'maria.lopez@email.com',
                'telefono': '098-765-4321',
                'direccion': 'Calle Secundaria 456, Ciudad',
                'fecha_registro': '22/02/2025',
                'total_compras': 890.50,
                'compras_realizadas': 8,
                'estado': 'Activo'
            },
            'C003': {
                'nombre': 'Carlos Martínez Silva',
                'email': 'carlos.martinez@email.com',
                'telefono': '555-123-4567',
                'direccion': 'Plaza Central 789, Ciudad',
                'fecha_registro': '10/03/2025',
                'total_compras': 2150.25,
                'compras_realizadas': 18,
                'estado': 'VIP'
            },
            'C004': {
                'nombre': 'Ana Fernández Torres',
                'email': 'ana.fernandez@email.com',
                'telefono': '777-888-9999',
                'direccion': 'Barrio Norte 321, Ciudad',
                'fecha_registro': '05/04/2025',
                'total_compras': 450.00,
                'compras_realizadas': 4,
                'estado': 'Activo'
            }
        }
        
        self.cliente_seleccionado = None
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crear interfaz de clientes"""
        # Título
        titulo = "👥 CONSULTAR CLIENTES" if self.modo_consulta else "👥 GESTIÓN DE CLIENTES"
        tk.Label(
            self.parent_frame,
            text=titulo,
            font=('Arial', 22, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(pady=(20, 30))
        
        # Frame principal
        main_frame = tk.Frame(self.parent_frame, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Panel izquierdo - Lista de clientes
        left_panel = tk.LabelFrame(main_frame, text="👥 Lista de Clientes", font=('Arial', 12, 'bold'))
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Toolbar (solo si no es modo consulta)
        if not self.modo_consulta:
            toolbar_frame = tk.Frame(left_panel)
            toolbar_frame.pack(fill='x', padx=10, pady=10)
            
            tk.Button(
                toolbar_frame,
                text="➕ Nuevo Cliente",
                font=('Arial', 10, 'bold'),
                bg='#27ae60',
                fg='white',
                relief='flat',
                command=self.nuevo_cliente
            ).pack(side='left', padx=2)
            
            tk.Button(
                toolbar_frame,
                text="✏️ Editar",
                font=('Arial', 10, 'bold'),
                bg='#3498db',
                fg='white',
                relief='flat',
                command=self.editar_cliente
            ).pack(side='left', padx=2)
            
            tk.Button(
                toolbar_frame,
                text="🗑️ Eliminar",
                font=('Arial', 10, 'bold'),
                bg='#e74c3c',
                fg='white',
                relief='flat',
                command=self.eliminar_cliente
            ).pack(side='left', padx=2)
        
        # Buscador
        search_frame = tk.Frame(left_panel)
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_frame, text="🔍 Buscar:", font=('Arial', 10)).pack(side='left')
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filtrar_clientes)
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 10))
        search_entry.pack(side='left', fill='x', expand=True, padx=(5, 0))
        
        # Lista de clientes
        lista_frame = tk.Frame(left_panel)
        lista_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        columns = ('codigo', 'nombre', 'telefono', 'total_compras', 'estado')
        self.tree_clientes = ttk.Treeview(lista_frame, columns=columns, show='headings', height=12)
        
        self.tree_clientes.heading('codigo', text='Código')
        self.tree_clientes.heading('nombre', text='Nombre')
        self.tree_clientes.heading('telefono', text='Teléfono')
        self.tree_clientes.heading('total_compras', text='Total Compras')
        self.tree_clientes.heading('estado', text='Estado')
        
        self.tree_clientes.column('codigo', width=80)
        self.tree_clientes.column('nombre', width=150)
        self.tree_clientes.column('telefono', width=100)
        self.tree_clientes.column('total_compras', width=100)
        self.tree_clientes.column('estado', width=80)
        
        # Scrollbar para clientes
        scrollbar_clientes = ttk.Scrollbar(lista_frame, orient='vertical', command=self.tree_clientes.yview)
        self.tree_clientes.configure(yscrollcommand=scrollbar_clientes.set)
        
        self.tree_clientes.pack(side='left', fill='both', expand=True)
        scrollbar_clientes.pack(side='right', fill='y')
        
        # Evento de selección
        self.tree_clientes.bind('<<TreeviewSelect>>', self.on_cliente_select)
        
        # Panel derecho - Detalles del cliente
        right_panel = tk.LabelFrame(main_frame, text="📋 Detalles del Cliente", font=('Arial', 12, 'bold'))
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Frame para información del cliente
        self.info_frame = tk.Frame(right_panel)
        self.info_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Estadísticas
        if not self.modo_consulta:
            stats_frame = tk.Frame(self.parent_frame, bg='#ecf0f1')
            stats_frame.pack(fill='x', padx=20, pady=10)
            self.actualizar_estadisticas(stats_frame)
        
        # Cargar clientes
        self.cargar_clientes()
        self.mostrar_info_vacia()
    
    def cargar_clientes(self):
        """Cargar clientes en la tabla"""
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
            
        for codigo, datos in self.clientes_db.items():
            estado_emoji = {"Activo": "🟢", "VIP": "⭐", "Inactivo": "🔴"}
            estado_display = f"{estado_emoji.get(datos['estado'], '🟢')} {datos['estado']}"
            
            self.tree_clientes.insert('', 'end', values=(
                codigo,
                datos['nombre'],
                datos['telefono'],
                f"${datos['total_compras']:.2f}",
                estado_display
            ))
    
    def filtrar_clientes(self, *args):
        """Filtrar clientes por búsqueda"""
        busqueda = self.search_var.get().lower()
        
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
            
        for codigo, datos in self.clientes_db.items():
            if (busqueda in codigo.lower() or 
                busqueda in datos['nombre'].lower() or
                busqueda in datos['email'].lower() or
                busqueda in datos['telefono'].lower()):
                
                estado_emoji = {"Activo": "🟢", "VIP": "⭐", "Inactivo": "🔴"}
                estado_display = f"{estado_emoji.get(datos['estado'], '🟢')} {datos['estado']}"
                
                self.tree_clientes.insert('', 'end', values=(
                    codigo,
                    datos['nombre'],
                    datos['telefono'],
                    f"${datos['total_compras']:.2f}",
                    estado_display
                ))
    
    def on_cliente_select(self, event):
        """Manejar selección de cliente"""
        selection = self.tree_clientes.selection()
        if selection:
            item = self.tree_clientes.item(selection[0])
            codigo = item['values'][0]
            self.cliente_seleccionado = codigo
            self.mostrar_info_cliente(codigo)
        else:
            self.mostrar_info_vacia()
    
    def mostrar_info_vacia(self):
        """Mostrar información vacía cuando no hay selección"""
        for widget in self.info_frame.winfo_children():
            widget.destroy()
            
        tk.Label(
            self.info_frame,
            text="👥 Seleccione un cliente para ver los detalles",
            font=('Arial', 12),
            fg='#7f8c8d'
        ).pack(expand=True)
    
    def mostrar_info_cliente(self, codigo):
        """Mostrar información detallada del cliente"""
        for widget in self.info_frame.winfo_children():
            widget.destroy()
            
        if codigo not in self.clientes_db:
            return
            
        datos = self.clientes_db[codigo]
        
        # Título con nombre del cliente
        tk.Label(
            self.info_frame,
            text=f"👤 {datos['nombre']}",
            font=('Arial', 14, 'bold'),
            fg='#2c3e50'
        ).pack(pady=(10, 20))
        
        # Información del cliente
        info_cliente = [
            ("🆔 Código:", codigo),
            ("📧 Email:", datos['email']),
            ("📞 Teléfono:", datos['telefono']),
            ("📍 Dirección:", datos['direccion']),
            ("📅 Registro:", datos['fecha_registro']),
            ("💰 Total Compras:", f"${datos['total_compras']:.2f}"),
            ("🛒 Compras Realizadas:", str(datos['compras_realizadas'])),
            ("⭐ Estado:", datos['estado'])
        ]
        
        for label, valor in info_cliente:
            frame_info = tk.Frame(self.info_frame)
            frame_info.pack(fill='x', padx=20, pady=3)
            
            tk.Label(
                frame_info,
                text=label,
                font=('Arial', 10, 'bold'),
                width=15,
                anchor='w'
            ).pack(side='left')
            
            tk.Label(
                frame_info,
                text=valor,
                font=('Arial', 10),
                anchor='w'
            ).pack(side='left', fill='x', expand=True)
        
        # Botones de acción (solo si no es modo consulta)
        if not self.modo_consulta:
            acciones_frame = tk.Frame(self.info_frame)
            acciones_frame.pack(fill='x', padx=20, pady=20)
            
            tk.Button(
                acciones_frame,
                text="📊 Ver Historial",
                font=('Arial', 9, 'bold'),
                bg='#3498db',
                fg='white',
                relief='flat',
                command=lambda: self.ver_historial(codigo)
            ).pack(fill='x', pady=2)
            
            tk.Button(
                acciones_frame,
                text="✏️ Editar Cliente",
                font=('Arial', 9, 'bold'),
                bg='#f39c12',
                fg='white',
                relief='flat',
                command=lambda: self.editar_cliente()
            ).pack(fill='x', pady=2)
    
    def actualizar_estadisticas(self, parent):
        """Actualizar estadísticas de clientes"""
        for widget in parent.winfo_children():
            widget.destroy()
        
        total_clientes = len(self.clientes_db)
        clientes_vip = sum(1 for c in self.clientes_db.values() if c['estado'] == 'VIP')
        total_ventas = sum(c['total_compras'] for c in self.clientes_db.values())
        
        stats = [
            ("👥 Total Clientes", str(total_clientes), "#3498db"),
            ("⭐ Clientes VIP", str(clientes_vip), "#f39c12"),
            ("💰 Total Ventas", f"${total_ventas:.2f}", "#27ae60")
        ]
        
        for titulo, valor, color in stats:
            card = tk.Frame(parent, bg=color, relief='raised', bd=2)
            card.pack(side='left', fill='x', expand=True, padx=5)
            
            tk.Label(card, text=titulo, font=('Arial', 10, 'bold'), fg='white', bg=color).pack(pady=(10, 5))
            tk.Label(card, text=valor, font=('Arial', 12, 'bold'), fg='white', bg=color).pack(pady=(0, 10))
    
    def nuevo_cliente(self):
        """Agregar nuevo cliente"""
        messagebox.showinfo("Nuevo Cliente", "🚧 Función de agregar cliente en desarrollo...")
    
    def editar_cliente(self):
        """Editar cliente seleccionado"""
        if not self.cliente_seleccionado:
            messagebox.showwarning("Selección", "Por favor seleccione un cliente para editar")
            return
        messagebox.showinfo("Editar Cliente", "🚧 Función de editar cliente en desarrollo...")
    
    def eliminar_cliente(self):
        """Eliminar cliente seleccionado"""
        if not self.cliente_seleccionado:
            messagebox.showwarning("Selección", "Por favor seleccione un cliente para eliminar")
            return
        messagebox.showinfo("Eliminar Cliente", "🚧 Función de eliminar cliente en desarrollo...")
    
    def ver_historial(self, codigo):
        """Ver historial de compras del cliente"""
        messagebox.showinfo("Historial", f"🚧 Historial de compras para {codigo} en desarrollo...")

class CreditNotesIntegradas:
    """Gestión integrada de notas de crédito"""

    def __init__(self, parent_frame, modo_basico=False, usuario_id: int = 1):
        self.parent_frame = parent_frame
        self.modo_basico = modo_basico
        self.controller = CreditNoteController()
        self.usuario_id = usuario_id or 1
        self._build_ui()
        self._load_notes()

    def _build_ui(self):
        titulo = "🧾 NOTAS DE CRÉDITO" + (" (Básico)" if self.modo_basico else "")
        tk.Label(
            self.parent_frame,
            text=titulo,
            font=('Arial', 22, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(pady=(20, 10))

        btns = tk.Frame(self.parent_frame, bg='#ecf0f1')
        btns.pack(fill='x', padx=20, pady=10)

        tk.Button(
            btns,
            text="🔄 Refrescar",
            font=('Arial', 11, 'bold'),
            bg='#3498db', fg='white', relief='flat', padx=12, pady=8,
            command=self._load_notes
        ).pack(side='left', padx=5)

        tk.Button(
            btns,
            text="➕ Generar desde venta",
            font=('Arial', 11, 'bold'),
            bg='#27ae60', fg='white', relief='flat', padx=12, pady=8,
            command=self._prompt_generate
        ).pack(side='left', padx=5)

        tk.Button(
            btns,
            text="📄 Reporte 30 días",
            font=('Arial', 11, 'bold'),
            bg='#8e44ad', fg='white', relief='flat', padx=12, pady=8,
            command=self._show_report
        ).pack(side='left', padx=5)

        cols = ("numero", "venta", "total", "estado", "fecha", "motivo")
        self.tree = ttk.Treeview(self.parent_frame, columns=cols, show='headings')
        headers = {
            "numero": "Nota",
            "venta": "Venta",
            "total": "Total",
            "estado": "Estado",
            "fecha": "Fecha",
            "motivo": "Motivo"
        }
        for col, text in headers.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=140 if col != 'motivo' else 260, anchor='center')

        self.tree.pack(fill='both', expand=True, padx=20, pady=10)

    def _load_notes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        notes = self.controller.list_credit_notes(limit=200)
        for note in notes:
            fecha = note.get('created_at')
            fecha_txt = fecha.strftime('%Y-%m-%d %H:%M') if hasattr(fecha, 'strftime') else str(fecha)
            self.tree.insert('', 'end', values=(
                note.get('credit_note_number'),
                note.get('sale_number'),
                f"{note.get('total_amount', 0):.2f}",
                note.get('status'),
                fecha_txt,
                (note.get('reason') or '')[:60]
            ))

    def _prompt_generate(self):
        sale_id = simpledialog.askinteger("Generar nota", "ID de la venta a acreditar:")
        if not sale_id:
            return
        reason = simpledialog.askstring("Motivo", "Motivo de la nota:", initialvalue="Devolución / cancelación") or ""
        result = self.controller.create_credit_note(sale_id, self.usuario_id, reason)
        if result.get('success'):
            messagebox.showinfo("Nota creada", result.get('message', 'Nota de crédito generada.'))
            self._load_notes()
        else:
            messagebox.showerror("Error", result.get('message', 'No se pudo generar la nota.'))

    def _show_report(self):
        data = self.controller.report(days_back=30)
        if not data.get('success'):
            messagebox.showerror("Reporte", data.get('message', 'Error al obtener reporte.'))
            return
        summary = data['data']['summary']
        messagebox.showinfo(
            "Reporte de notas (30 días)",
            f"Total notas: {summary['total_notes']}\nMonto total: {summary['total_amount']:.2f}"
        )


class ReportesIntegrados:
    """Sistema de reportes integrado en el panel principal"""
    
    def __init__(self, parent_frame, modo_basico=False):
        self.parent_frame = parent_frame
        self.modo_basico = modo_basico
        
        # Datos simulados para reportes
        self.ventas_data = [
            {'fecha': '23/09/2025', 'venta_id': 'V20250923001', 'cliente': 'Juan Pérez', 'total': 45.50, 'productos': 3},
            {'fecha': '23/09/2025', 'venta_id': 'V20250923002', 'cliente': 'María López', 'total': 67.80, 'productos': 5},
            {'fecha': '24/09/2025', 'venta_id': 'V20250924001', 'cliente': 'Carlos Martínez', 'total': 123.25, 'productos': 8},
            {'fecha': '24/09/2025', 'venta_id': 'V20250924002', 'cliente': 'Ana Fernández', 'total': 89.90, 'productos': 6},
            {'fecha': '25/09/2025', 'venta_id': 'V20250925001', 'cliente': 'Luis García', 'total': 156.75, 'productos': 10},
            {'fecha': '25/09/2025', 'venta_id': 'V20250925002', 'cliente': 'Elena Ruiz', 'total': 78.40, 'productos': 4},
            {'fecha': '26/09/2025', 'venta_id': 'V20250926001', 'cliente': 'Pedro Sánchez', 'total': 234.60, 'productos': 12},
            {'fecha': '26/09/2025', 'venta_id': 'V20250926002', 'cliente': 'Sofia Torres', 'total': 91.30, 'productos': 7},
            {'fecha': '27/09/2025', 'venta_id': 'V20250927001', 'cliente': 'Diego López', 'total': 167.85, 'productos': 9},
            {'fecha': '27/09/2025', 'venta_id': 'V20250927002', 'cliente': 'Carmen Díaz', 'total': 45.20, 'productos': 2}
        ]
        
        self.productos_vendidos = {
            'Coca Cola 2L': {'cantidad': 45, 'ingresos': 247.50},
            'Pan Integral': {'cantidad': 38, 'ingresos': 123.50},
            'Leche Entera 1L': {'cantidad': 29, 'ingresos': 139.20},
            'Arroz 1kg': {'cantidad': 52, 'ingresos': 143.00},
            'Aceite Girasol 1L': {'cantidad': 18, 'ingresos': 124.20},
            'Jabón Líquido': {'cantidad': 33, 'ingresos': 148.50}
        }
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crear interfaz de reportes"""
        # Título
        titulo = "📊 REPORTES BÁSICOS" if self.modo_basico else "📊 REPORTES Y ESTADÍSTICAS"
        tk.Label(
            self.parent_frame,
            text=titulo,
            font=('Arial', 22, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(pady=(20, 30))
        
        # Crear notebook para las pestañas
        self.notebook = ttk.Notebook(self.parent_frame)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Pestaña 1: Resumen General
        self.crear_tab_resumen()
        
        # Pestaña 2: Ventas Detalladas
        self.crear_tab_ventas()
        
        # Pestaña 3: Productos Más Vendidos
        self.crear_tab_productos()
        
        if not self.modo_basico:
            # Pestañas adicionales solo para administradores
            # Pestaña 4: Análisis de Clientes
            self.crear_tab_clientes()
            
            # Pestaña 5: Reportes Financieros
            self.crear_tab_financieros()
            
            # Pestaña 6: Exportar Datos
            self.crear_tab_exportar()
    
    def crear_tab_resumen(self):
        """Crear pestaña de resumen general"""
        tab_resumen = ttk.Frame(self.notebook)
        self.notebook.add(tab_resumen, text="📊 Resumen General")
        
        # Frame principal con scroll
        canvas = tk.Canvas(tab_resumen, bg='#ecf0f1')
        scrollbar = ttk.Scrollbar(tab_resumen, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Estadísticas principales
        stats_frame = tk.Frame(scrollable_frame, bg='#ecf0f1')
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        # Calcular estadísticas
        total_ventas = sum(venta['total'] for venta in self.ventas_data)
        total_transacciones = len(self.ventas_data)
        venta_promedio = total_ventas / total_transacciones if total_transacciones > 0 else 0
        productos_vendidos = sum(venta['productos'] for venta in self.ventas_data)
        
        # Tarjetas de estadísticas
        stats = [
            ("💰", "Ventas Totales", f"${total_ventas:.2f}", "#27ae60"),
            ("🛒", "Transacciones", str(total_transacciones), "#3498db"),
            ("📊", "Venta Promedio", f"${venta_promedio:.2f}", "#9b59b6"),
            ("📦", "Productos Vendidos", str(productos_vendidos), "#e74c3c")
        ]
        
        for emoji, titulo, valor, color in stats:
            card = tk.Frame(stats_frame, bg=color, relief='raised', bd=2, height=120)
            card.pack(side='left', fill='x', expand=True, padx=10)
            card.pack_propagate(False)
            
            tk.Label(card, text=emoji, font=('Arial', 24), fg='white', bg=color).pack(pady=(15, 5))
            tk.Label(card, text=titulo, font=('Arial', 10, 'bold'), fg='white', bg=color).pack()
            tk.Label(card, text=valor, font=('Arial', 14, 'bold'), fg='white', bg=color).pack(pady=(5, 15))
        
        # Gráfico de ventas por día (simulado con barras de texto)
        grafico_frame = tk.LabelFrame(scrollable_frame, text="📈 Ventas por Día", font=('Arial', 12, 'bold'))
        grafico_frame.pack(fill='x', padx=20, pady=20)
        
        # Agrupar ventas por día
        ventas_por_dia = {}
        for venta in self.ventas_data:
            fecha = venta['fecha']
            if fecha not in ventas_por_dia:
                ventas_por_dia[fecha] = 0
            ventas_por_dia[fecha] += venta['total']
        
        max_venta = max(ventas_por_dia.values()) if ventas_por_dia else 1
        
        for fecha, total in sorted(ventas_por_dia.items()):
            dia_frame = tk.Frame(grafico_frame, bg='#ecf0f1')
            dia_frame.pack(fill='x', padx=10, pady=5)
            
            # Fecha
            tk.Label(dia_frame, text=fecha, font=('Arial', 10, 'bold'), bg='#ecf0f1', width=12).pack(side='left')
            
            # Barra visual (usando caracteres)
            barra_length = int((total / max_venta) * 30)
            barra = "█" * barra_length
            tk.Label(dia_frame, text=barra, font=('Arial', 10), fg='#3498db', bg='#ecf0f1').pack(side='left', padx=5)
            
            # Valor
            tk.Label(dia_frame, text=f"${total:.2f}", font=('Arial', 10, 'bold'), bg='#ecf0f1').pack(side='left')
        
        # Top productos
        top_frame = tk.LabelFrame(scrollable_frame, text="🏆 Top 3 Productos", font=('Arial', 12, 'bold'))
        top_frame.pack(fill='x', padx=20, pady=20)
        
        productos_ordenados = sorted(self.productos_vendidos.items(), key=lambda x: x[1]['ingresos'], reverse=True)[:3]
        
        for i, (producto, datos) in enumerate(productos_ordenados, 1):
            medalla = ["🥇", "🥈", "🥉"][i-1]
            producto_frame = tk.Frame(top_frame, bg='#ecf0f1')
            producto_frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(producto_frame, text=f"{medalla} {producto}", font=('Arial', 11, 'bold'), bg='#ecf0f1').pack(side='left')
            tk.Label(producto_frame, text=f"Vendidos: {datos['cantidad']} | Ingresos: ${datos['ingresos']:.2f}", 
                    font=('Arial', 10), bg='#ecf0f1', fg='#7f8c8d').pack(side='right')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def crear_tab_ventas(self):
        """Crear pestaña de ventas detalladas"""
        tab_ventas = ttk.Frame(self.notebook)
        self.notebook.add(tab_ventas, text="💰 Ventas Detalladas")
        
        # Filtros
        filtros_frame = tk.Frame(tab_ventas, bg='#ecf0f1')
        filtros_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(filtros_frame, text="📅 Filtrar por fecha:", font=('Arial', 11, 'bold'), bg='#ecf0f1').pack(side='left')
        
        self.fecha_var = tk.StringVar(value="Todas")
        fechas = ["Todas"] + list(set(venta['fecha'] for venta in self.ventas_data))
        fecha_combo = ttk.Combobox(filtros_frame, textvariable=self.fecha_var, values=sorted(fechas), state='readonly')
        fecha_combo.pack(side='left', padx=10)
        fecha_combo.bind('<<ComboboxSelected>>', self.filtrar_ventas)
        
        tk.Button(
            filtros_frame,
            text="🔄 Actualizar",
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            command=self.filtrar_ventas
        ).pack(side='left', padx=10)
        
        # Tabla de ventas
        tabla_frame = tk.Frame(tab_ventas)
        tabla_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('fecha', 'venta_id', 'cliente', 'productos', 'total')
        self.tree_ventas = ttk.Treeview(tabla_frame, columns=columns, show='headings')
        
        self.tree_ventas.heading('fecha', text='Fecha')
        self.tree_ventas.heading('venta_id', text='ID Venta')
        self.tree_ventas.heading('cliente', text='Cliente')
        self.tree_ventas.heading('productos', text='Productos')
        self.tree_ventas.heading('total', text='Total')
        
        self.tree_ventas.column('fecha', width=100)
        self.tree_ventas.column('venta_id', width=120)
        self.tree_ventas.column('cliente', width=150)
        self.tree_ventas.column('productos', width=80)
        self.tree_ventas.column('total', width=100)
        
        # Scrollbar para ventas
        scrollbar_ventas = ttk.Scrollbar(tabla_frame, orient='vertical', command=self.tree_ventas.yview)
        self.tree_ventas.configure(yscrollcommand=scrollbar_ventas.set)
        
        self.tree_ventas.pack(side='left', fill='both', expand=True)
        scrollbar_ventas.pack(side='right', fill='y')
        
        # Cargar ventas iniciales
        self.cargar_ventas()
        
        # Resumen de ventas filtradas
        self.resumen_frame = tk.Frame(tab_ventas, bg='#34495e')
        self.resumen_frame.pack(fill='x', padx=20, pady=10)
        
        self.actualizar_resumen_ventas()
    
    def crear_tab_productos(self):
        """Crear pestaña de productos más vendidos"""
        tab_productos = ttk.Frame(self.notebook)
        self.notebook.add(tab_productos, text="📦 Productos Vendidos")
        
        # Tabla de productos
        tabla_frame = tk.Frame(tab_productos)
        tabla_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        columns = ('producto', 'cantidad', 'ingresos', 'porcentaje')
        tree_productos = ttk.Treeview(tabla_frame, columns=columns, show='headings')
        
        tree_productos.heading('producto', text='Producto')
        tree_productos.heading('cantidad', text='Cantidad Vendida')
        tree_productos.heading('ingresos', text='Ingresos')
        tree_productos.heading('porcentaje', text='% del Total')
        
        tree_productos.column('producto', width=200)
        tree_productos.column('cantidad', width=120)
        tree_productos.column('ingresos', width=100)
        tree_productos.column('porcentaje', width=100)
        
        # Scrollbar
        scrollbar_productos = ttk.Scrollbar(tabla_frame, orient='vertical', command=tree_productos.yview)
        tree_productos.configure(yscrollcommand=scrollbar_productos.set)
        
        tree_productos.pack(side='left', fill='both', expand=True)
        scrollbar_productos.pack(side='right', fill='y')
        
        # Cargar productos ordenados por ingresos
        total_ingresos = sum(datos['ingresos'] for datos in self.productos_vendidos.values())
        productos_ordenados = sorted(self.productos_vendidos.items(), key=lambda x: x[1]['ingresos'], reverse=True)
        
        for producto, datos in productos_ordenados:
            porcentaje = (datos['ingresos'] / total_ingresos * 100) if total_ingresos > 0 else 0
            tree_productos.insert('', 'end', values=(
                producto,
                datos['cantidad'],
                f"${datos['ingresos']:.2f}",
                f"{porcentaje:.1f}%"
            ))
    
    def crear_tab_clientes(self):
        """Crear pestaña de análisis de clientes (solo admin)"""
        tab_clientes = ttk.Frame(self.notebook)
        self.notebook.add(tab_clientes, text="👥 Análisis Clientes")
        
        tk.Label(
            tab_clientes,
            text="👥 ANÁLISIS DE CLIENTES",
            font=('Arial', 18, 'bold'),
            fg='#2c3e50'
        ).pack(pady=30)
        
        # Estadísticas de clientes
        stats_clientes_frame = tk.Frame(tab_clientes, bg='#ecf0f1')
        stats_clientes_frame.pack(fill='x', padx=50, pady=20)
        
        # Datos simulados de clientes
        clientes_stats = [
            ("👥", "Total Clientes", "156", "#3498db"),
            ("⭐", "Clientes VIP", "23", "#f39c12"),
            ("🔄", "Clientes Recurrentes", "89", "#27ae60"),
            ("📊", "Compra Promedio", "$87.50", "#9b59b6")
        ]
        
        for emoji, titulo, valor, color in clientes_stats:
            card = tk.Frame(stats_clientes_frame, bg=color, relief='raised', bd=2, height=100)
            card.pack(side='left', fill='x', expand=True, padx=10)
            card.pack_propagate(False)
            
            tk.Label(card, text=emoji, font=('Arial', 20), fg='white', bg=color).pack(pady=(10, 5))
            tk.Label(card, text=titulo, font=('Arial', 9, 'bold'), fg='white', bg=color).pack()
            tk.Label(card, text=valor, font=('Arial', 12, 'bold'), fg='white', bg=color).pack(pady=(5, 10))
        
        # Top clientes
        top_clientes_frame = tk.LabelFrame(tab_clientes, text="🏆 Top 5 Clientes", font=('Arial', 12, 'bold'))
        top_clientes_frame.pack(fill='x', padx=50, pady=20)
        
        top_clientes = [
            ("Carlos Martínez", "$2,150.25", "18 compras"),
            ("Juan Pérez", "$1,250.75", "12 compras"),
            ("María López", "$890.50", "8 compras"),
            ("Ana Fernández", "$650.00", "6 compras"),
            ("Luis García", "$480.25", "5 compras")
        ]
        
        for i, (nombre, total, compras) in enumerate(top_clientes, 1):
            cliente_frame = tk.Frame(top_clientes_frame, bg='#ecf0f1')
            cliente_frame.pack(fill='x', padx=20, pady=5)
            
            medallas = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
            
            tk.Label(cliente_frame, text=f"{medallas[i-1]} {nombre}", 
                    font=('Arial', 11, 'bold'), bg='#ecf0f1').pack(side='left')
            tk.Label(cliente_frame, text=f"{total} - {compras}", 
                    font=('Arial', 10), bg='#ecf0f1', fg='#7f8c8d').pack(side='right')
    
    def crear_tab_financieros(self):
        """Crear pestaña de reportes financieros (solo admin)"""
        tab_financieros = ttk.Frame(self.notebook)
        self.notebook.add(tab_financieros, text="💹 Financieros")
        
        tk.Label(
            tab_financieros,
            text="💹 REPORTES FINANCIEROS",
            font=('Arial', 18, 'bold'),
            fg='#2c3e50'
        ).pack(pady=30)
        
        # Métricas financieras
        metricas_frame = tk.Frame(tab_financieros, bg='#ecf0f1')
        metricas_frame.pack(fill='x', padx=50, pady=20)
        
        # Calcular métricas simuladas
        total_ingresos = sum(venta['total'] for venta in self.ventas_data)
        costos_estimados = total_ingresos * 0.6  # 60% costos
        ganancia_bruta = total_ingresos - costos_estimados
        margen_ganancia = (ganancia_bruta / total_ingresos * 100) if total_ingresos > 0 else 0
        
        metricas = [
            ("💰", "Ingresos Totales", f"${total_ingresos:.2f}", "#27ae60"),
            ("📉", "Costos Estimados", f"${costos_estimados:.2f}", "#e74c3c"),
            ("📈", "Ganancia Bruta", f"${ganancia_bruta:.2f}", "#3498db"),
            ("📊", "Margen (%)", f"{margen_ganancia:.1f}%", "#9b59b6")
        ]
        
        for emoji, titulo, valor, color in metricas:
            card = tk.Frame(metricas_frame, bg=color, relief='raised', bd=2, height=100)
            card.pack(side='left', fill='x', expand=True, padx=10)
            card.pack_propagate(False)
            
            tk.Label(card, text=emoji, font=('Arial', 20), fg='white', bg=color).pack(pady=(10, 5))
            tk.Label(card, text=titulo, font=('Arial', 9, 'bold'), fg='white', bg=color).pack()
            tk.Label(card, text=valor, font=('Arial', 12, 'bold'), fg='white', bg=color).pack(pady=(5, 10))
        
        # Proyecciones
        proyecciones_frame = tk.LabelFrame(tab_financieros, text="📈 Proyecciones Mensuales", font=('Arial', 12, 'bold'))
        proyecciones_frame.pack(fill='x', padx=50, pady=20)
        
        ventas_diarias = total_ingresos / 5  # Promedio últimos 5 días
        proyeccion_mensual = ventas_diarias * 30
        proyeccion_anual = proyeccion_mensual * 12
        
        tk.Label(proyecciones_frame, 
                text=f"📊 Venta Diaria Promedio: ${ventas_diarias:.2f}\n"
                     f"📅 Proyección Mensual: ${proyeccion_mensual:.2f}\n"
                     f"🗓️ Proyección Anual: ${proyeccion_anual:.2f}",
                font=('Arial', 12), bg='#ecf0f1', justify='left').pack(padx=20, pady=15)
    
    def crear_tab_exportar(self):
        """Crear pestaña de exportación de datos (solo admin)"""
        tab_exportar = ttk.Frame(self.notebook)
        self.notebook.add(tab_exportar, text="📤 Exportar")
        
        tk.Label(
            tab_exportar,
            text="📤 EXPORTAR DATOS",
            font=('Arial', 18, 'bold'),
            fg='#2c3e50'
        ).pack(pady=30)
        
        # Opciones de exportación
        export_frame = tk.Frame(tab_exportar, bg='#ecf0f1')
        export_frame.pack(fill='x', padx=100, pady=50)
        
        opciones_export = [
            ("📊 Exportar Reporte de Ventas", "Generar archivo CSV con todas las ventas", self.exportar_ventas),
            ("📦 Exportar Lista de Productos", "Generar archivo CSV con productos vendidos", self.exportar_productos),
            ("👥 Exportar Base de Clientes", "Generar archivo CSV con información de clientes", self.exportar_clientes),
            ("💹 Exportar Reporte Financiero", "Generar reporte PDF con análisis financiero", self.exportar_financiero)
        ]
        
        for titulo, descripcion, comando in opciones_export:
            option_frame = tk.Frame(export_frame, bg='white', relief='raised', bd=2)
            option_frame.pack(fill='x', pady=10)
            
            tk.Label(option_frame, text=titulo, font=('Arial', 12, 'bold'), 
                    fg='#2c3e50', bg='white').pack(anchor='w', padx=20, pady=(10, 5))
            
            tk.Label(option_frame, text=descripcion, font=('Arial', 10), 
                    fg='#7f8c8d', bg='white').pack(anchor='w', padx=20)
            
            tk.Button(option_frame, text="📥 Exportar", font=('Arial', 10, 'bold'),
                     bg='#27ae60', fg='white', relief='flat', command=comando).pack(anchor='e', padx=20, pady=10)
    
    def cargar_ventas(self):
        """Cargar ventas en la tabla"""
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)
            
        fecha_filtro = self.fecha_var.get()
        ventas_filtradas = self.ventas_data if fecha_filtro == "Todas" else [v for v in self.ventas_data if v['fecha'] == fecha_filtro]
        
        for venta in ventas_filtradas:
            self.tree_ventas.insert('', 'end', values=(
                venta['fecha'],
                venta['venta_id'],
                venta['cliente'],
                venta['productos'],
                f"${venta['total']:.2f}"
            ))
    
    def filtrar_ventas(self, event=None):
        """Filtrar ventas por fecha"""
        self.cargar_ventas()
        self.actualizar_resumen_ventas()
    
    def actualizar_resumen_ventas(self):
        """Actualizar resumen de ventas filtradas"""
        # Limpiar resumen anterior
        for widget in self.resumen_frame.winfo_children():
            widget.destroy()
        
        fecha_filtro = self.fecha_var.get()
        ventas_filtradas = self.ventas_data if fecha_filtro == "Todas" else [v for v in self.ventas_data if v['fecha'] == fecha_filtro]
        
        total = sum(v['total'] for v in ventas_filtradas)
        cantidad = len(ventas_filtradas)
        
        tk.Label(self.resumen_frame, 
                text=f"📊 Resumen: {cantidad} ventas | Total: ${total:.2f}",
                font=('Arial', 12, 'bold'), fg='white', bg='#34495e').pack(pady=10)
    
    def exportar_ventas(self):
        """Exportar reporte de ventas (simulado)"""
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Guardar Reporte de Ventas"
        )
        if archivo:
            messagebox.showinfo("Exportación", f"✅ Reporte de ventas exportado a:\n{archivo}")
    
    def exportar_productos(self):
        """Exportar lista de productos (simulado)"""
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Guardar Lista de Productos"
        )
        if archivo:
            messagebox.showinfo("Exportación", f"✅ Lista de productos exportada a:\n{archivo}")
    
    def exportar_clientes(self):
        """Exportar base de clientes (simulado)"""
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Guardar Base de Clientes"
        )
        if archivo:
            messagebox.showinfo("Exportación", f"✅ Base de clientes exportada a:\n{archivo}")
    
    def exportar_financiero(self):
        """Exportar reporte financiero (simulado)"""
        archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Guardar Reporte Financiero"
        )
        if archivo:
            messagebox.showinfo("Exportación", f"✅ Reporte financiero exportado a:\n{archivo}")

class PanelUsuario:
    """Panel de usuario normal con navbar"""
    
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
        
    def crear_interfaz(self):
        """Crear interfaz del panel de usuario con navbar"""
        
        # Header Principal
        frame_header = tk.Frame(self.root, bg='#27ae60', height=80)
        frame_header.pack(fill='x')
        frame_header.pack_propagate(False)
        
        # Logo y título
        header_left = tk.Frame(frame_header, bg='#27ae60')
        header_left.pack(side='left', fill='y', padx=20)
        
        tk.Label(
            header_left,
            text="🏪 SISTEMA POS",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#27ae60'
        ).pack(anchor='w', pady=(10, 0))
        
        tk.Label(
            header_left,
            text=f"👤 Usuario: {self.datos_usuario['nombre_completo']}",
            font=('Arial', 11),
            fg='#d5f4e6',
            bg='#27ae60'
        ).pack(anchor='w')
        
        # Información del usuario y logout
        header_right = tk.Frame(frame_header, bg='#27ae60')
        header_right.pack(side='right', fill='y', padx=20)
        
        tk.Label(
            header_right,
            text=f"📅 {datetime.datetime.now().strftime('%d/%m/%Y')}",
            font=('Arial', 10),
            fg='#d5f4e6',
            bg='#27ae60'
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
        
        # Navbar (limitado para usuarios)
        self.frame_navbar = tk.Frame(self.root, bg='#2ecc71', height=60)
        self.frame_navbar.pack(fill='x')
        self.frame_navbar.pack_propagate(False)
        
        # Botones del navbar (limitados)
        navbar_buttons = [
            ("🏠", "Inicio", self.mostrar_inicio),
            ("💰", "Ventas", self.mostrar_ventas),
            ("🧾", "Notas de Crédito", self.mostrar_notas_credito),
            ("👥", "Clientes", self.mostrar_clientes),
            ("📊", "Reportes", self.mostrar_reportes)
        ]
        
        self.navbar_buttons = {}
        for emoji, texto, comando in navbar_buttons:
            btn = tk.Button(
                self.frame_navbar,
                text=f"{emoji} {texto}",
                font=('Arial', 11, 'bold'),
                bg='#2ecc71',
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
            button.config(bg='#229954')
        
        def on_leave(e):
            button.config(bg='#2ecc71')
        
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
                btn.config(bg='#196f3d')
            else:
                btn.config(bg='#2ecc71')
    
    def mostrar_inicio(self):
        """Mostrar página de inicio para usuario"""
        self.limpiar_contenido()
        self.resaltar_boton_activo('Inicio')
        
        # Título
        tk.Label(
            self.frame_contenido,
            text="🏠 PANEL DE USUARIO",
            font=('Arial', 24, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(pady=(30, 40))
        
        # Acciones disponibles
        tk.Label(
            self.frame_contenido,
            text="⚡ Acciones Disponibles",
            font=('Arial', 18, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(pady=(40, 20))
        
        acciones_frame = tk.Frame(self.frame_contenido, bg='#ecf0f1')
        acciones_frame.pack(fill='x', padx=150, pady=20)
        
        acciones = [
            ("💰 Realizar Venta", "#27ae60", self.mostrar_ventas),
            ("👥 Ver Clientes", "#3498db", self.mostrar_clientes),
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
                width=25,
                height=2
            ).pack(side='left', fill='x', expand=True, padx=15)
    
    def mostrar_ventas(self):
        """Mostrar módulo de ventas"""
        self.limpiar_contenido()
        self.resaltar_boton_activo('Ventas')
        
        # Crear el sistema de ventas integrado (modo usuario)
        VentasIntegradas(self.frame_contenido, modo_usuario=True)
    
    def mostrar_clientes(self):
        """Mostrar módulo de clientes"""
        self.limpiar_contenido()
        self.resaltar_boton_activo('Clientes')
        
        # Crear el sistema de clientes integrado (modo consulta)
        ClientesIntegrados(self.frame_contenido, modo_consulta=True)

    def mostrar_notas_credito(self):
        """Mostrar módulo de notas de crédito"""
        self.limpiar_contenido()
        self.resaltar_boton_activo('Notas de Crédito')
        CreditNotesIntegradas(self.frame_contenido, modo_basico=True, usuario_id=self.usuario_id)
    
    def mostrar_reportes(self):
        """Mostrar módulo de reportes"""
        self.limpiar_contenido()
        self.resaltar_boton_activo('Reportes')
        
        # Crear el sistema de reportes integrado (modo básico para usuarios)
        ReportesIntegrados(self.frame_contenido, modo_basico=True)
    
    def logout(self):
        """Cerrar sesión y volver al login"""
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            self.root.destroy()
            LoginApp().root.mainloop()

def main():
    """Función principal"""
    app = LoginApp()
    app.root.mainloop()

if __name__ == "__main__":
    main()
