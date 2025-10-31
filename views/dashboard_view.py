"""
Vista del Dashboard Principal - Interfaz de Módulos
Diseño moderno con cards/tarjetas por módulo
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Callable
from views.base_view import BaseView
from models.role_model import RoleModel
from services.permission_service import PermissionService
from utils.responsive_utils import ResponsiveManager
import os
import json
from PIL import Image, ImageTk


class DashboardView(BaseView):
    """Vista del dashboard principal con diseño de módulos/tarjetas"""
    
    def __init__(self, root: tk.Tk, user_data: Dict[str, Any] = None):
        super().__init__(root)
        self.user_data = user_data or {}
        self.module_callbacks = {}
        self.permission_service = PermissionService()
        self.logo_image = None  # Guardar referencia de la imagen
        
        # Inicializar gestor responsivo
        self.responsive = ResponsiveManager(self.root)
        
        self.setup_dashboard()
    
    def setup_dashboard(self):
        """Configurar interfaz del dashboard"""
        # NO limpiar widgets previos - ya están el menú y toolbar
        self.setup_main_window()
        self.create_header()
        self.create_modules_grid()
        self.create_status_footer()
    
    def setup_main_window(self):
        """Configurar ventana principal"""
        self.root.title("Sistema POS - Dashboard Principal")
        
        # Hacer ventana responsiva
        self.responsive.make_window_responsive(self.root)
        
        self.root.configure(bg='#f1f5f9')
    
    def create_header(self):
        """Crear header moderno con gradientes y efectos visuales auto-escalados"""
        # Tamaños escalados
        header_height = self.scaler.scale_value(80)
        gradient_height = max(2, self.scaler.scale_value(3))
        content_padx = self.scaler.scale_padding(20)
        content_pady = self.scaler.scale_padding(8)
        
        header_frame = tk.Frame(self.root, bg='#ffffff', height=header_height)
        header_frame.pack(fill='x', side='top', pady=0, padx=0)
        header_frame.pack_propagate(False)
        
        # Gradiente superior más sutil
        gradient_frame = tk.Frame(header_frame, bg='#1e3a8a', height=gradient_height)
        gradient_frame.pack(fill='x')
        
        # Contenedor principal con fondo más elegante
        main_content = tk.Frame(header_frame, bg='#ffffff')
        main_content.pack(expand=True, fill='both', padx=content_padx, pady=content_pady)
        
        # Frame izquierdo con logo animado
        left_frame = tk.Frame(main_content, bg='#ffffff')
        left_frame.pack(side='left', fill='y')
        
        # Cargar configuración de la empresa
        company_name, logo_path = self.load_company_config()
        
        # Contenedor del logo (escalado)
        logo_size = self.scaler.scale_value(50)
        logo_padx = self.scaler.scale_padding(18)
        
        self.logo_container = tk.Frame(left_frame, bg='#ffffff', width=logo_size, height=logo_size)
        self.logo_container.pack(side='left', padx=(0, logo_padx), pady=0)
        self.logo_container.pack_propagate(False)
        
        # Intentar cargar logo desde configuración
        if logo_path and os.path.exists(logo_path):
            self.load_company_logo(self.logo_container, logo_path)
        else:
            # Logo por defecto (emoji)
            self.create_default_logo(self.logo_container)
        
        # Contenedor de títulos con efectos
        title_frame = tk.Frame(left_frame, bg='#ffffff')
        title_frame.pack(side='left', fill='y', pady=0)
        
        # Título principal con nombre de la empresa (escalado)
        title_font_size = self.scaler.scale_font(20)
        subtitle_font_size = self.scaler.scale_font(10)
        
        main_title = tk.Label(
            title_frame,
            text=company_name.upper(),
            font=('Segoe UI', title_font_size, 'bold'),
            fg='#1e293b',
            bg='#ffffff',
            relief='flat'
        )
        main_title.pack(anchor='w')
        
        # Subtítulo con color degradado
        subtitle = tk.Label(
            title_frame,
            text="ManagementPro POS v1.0",
            font=('Segoe UI', subtitle_font_size),
            fg='#64748b',
            bg='#ffffff'
        )
        subtitle.pack(anchor='w', pady=(3, 0))
        
        # Panel del usuario con diseño card moderno
        user_container = tk.Frame(main_content, bg='#ffffff')
        user_container.pack(side='right', pady=0)
        
        # Contenido del user card (escalado)
        user_padx = self.scaler.scale_padding(15)
        user_pady = self.scaler.scale_padding(8)
        user_font_size = self.scaler.scale_font(11)
        role_font_size = self.scaler.scale_font(9)
        
        user_content = tk.Frame(user_container, bg='#ffffff')
        user_content.pack(padx=user_padx, pady=user_pady)
        
        # Información del usuario con iconos modernos
        welcome_text = f"👤 {self.user_data.get('full_name', self.user_data.get('username', 'Usuario'))}"
        user_label = tk.Label(
            user_content,
            text=welcome_text,
            font=('Segoe UI', user_font_size, 'bold'),
            fg='#1e293b',
            bg='#ffffff'
        )
        user_label.pack(anchor='e')
        
        # Rol con badge moderno
        role_text = f"{self._get_user_role_display_name()}"
        role_label = tk.Label(
            user_content,
            text=role_text,
            font=('Segoe UI', role_font_size),
            fg='#64748b',
            bg='#ffffff'
        )
        role_label.pack(anchor='e', pady=(3, 0))
    
    def create_modules_grid(self):
        """Crear grid de módulos con diseño profesional"""
        # Contenedor principal con fondo limpio
        main_container = tk.Frame(self.root, bg='#f1f5f9')
        main_container.pack(fill='both', expand=True, pady=0)
        
        # Grid principal de módulos con fondo mejorado
        modules_frame = tk.Frame(main_container, bg='#f1f5f9')
        modules_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Título de sección con estilo limpio
        section_title = tk.Label(
            modules_frame,
            text="Módulos del Sistema",
            font=('Segoe UI', 16, 'bold'),
            fg='#1e293b',
            bg='#f1f5f9'
        )
        section_title.pack(pady=(5, 10), anchor='w')
        
        # Obtener módulos disponibles
        modules = self.get_available_modules()
        
        # Crear layout dinámico con efectos visuales
        self.create_colorful_modules_grid(modules_frame, modules)
    

    
    def get_available_modules(self):
        """Obtener módulos disponibles según permisos del usuario"""
        base_modules = [
            {
                'id': 'products',
                'title': 'Registro de Productos',
                'icon': '📦',
                'color': '#2563eb',
                'description': 'Invoices',
                'permission': 'inventory.view'
            },
            {
                'id': 'clients',
                'title': 'Registro de Clientes',
                'icon': '👤',
                'color': '#7c3aed',
                'description': 'Clients',
                'permission': 'users.view'
            },
            {
                'id': 'suppliers',
                'title': 'Registro de Proveedores',
                'icon': '👥',
                'color': '#0891b2',
                'description': 'Application',
                'permission': 'suppliers.view'
            },
            {
                'id': 'categories',
                'title': 'Registro de Categorías',
                'icon': '📁',
                'color': '#dc2626',
                'description': 'Reports',
                'permission': 'categories.view'
            },
            {
                'id': 'user_management',
                'title': 'Gestión de Usuarios',
                'icon': '👥',
                'color': '#8b5cf6',
                'description': 'Administrar usuarios del sistema',
                'permission': 'users.view'
            },
            {
                'id': 'role_management',
                'title': 'Gestión de Roles',
                'icon': '🔐',
                'color': '#6366f1',
                'description': 'Administrar roles y permisos',
                'permission': 'roles.view'
            },
            {
                'id': 'stock_control',
                'title': 'Control de Stock',
                'icon': '📊',
                'color': '#f59e0b',
                'description': 'Actualizar inventario',
                'permission': 'inventory.edit'
            },
            {
                'id': 'expenses',
                'title': 'Registro de Egresos',
                'icon': '💰',
                'color': '#9333ea',
                'description': 'Reports',
                'permission': 'expenses.view'
            },
            {
                'id': 'cash_register',
                'title': 'Registro de Caja',
                'icon': '💵',
                'color': '#059669',
                'description': 'Help',
                'permission': 'cash.view'
            },
            {
                'id': 'sales_register',
                'title': 'Ventas - Registrar Ventas',
                'icon': '🛍️',
                'color': '#ea580c',
                'description': 'Reports',
                'permission': 'sales.create'
            },
            {
                'id': 'purchases',
                'title': 'Compras - Registrar Compras',
                'icon': '⚙️',
                'color': '#7c2d12',
                'description': 'DevComponents',
                'permission': 'inventory.create'
            },
            {
                'id': 'income_report',
                'title': 'Informe de Ingresos a Caja',
                'icon': '📊',
                'color': '#c026d3',
                'description': 'Invoices',
                'permission': 'sales.reports'
            },
            {
                'id': 'sales_history',
                'title': 'Ventas Realizadas',
                'icon': '📋',
                'color': '#be123c',
                'description': 'Reports',
                'permission': 'sales.view'
            },
            {
                'id': 'purchase_history',
                'title': 'Compras Realizadas',
                'icon': '📋',
                'color': '#65a30d',
                'description': 'Invoices',
                'permission': 'purchases.view'
            },
            {
                'id': 'monthly_sales',
                'title': 'Ventas Mensuales',
                'icon': '📈',
                'color': '#0369a1',
                'description': 'Reports',
                'permission': 'sales.reports'
            },
            {
                'id': 'business',
                'title': 'Mi negocio',
                'icon': '🏢',
                'color': '#0d9488',
                'description': 'Configuración general',
                'permission': 'system.config'
            },
            {
                'id': 'responsive_config',
                'title': 'Escalado Responsivo',
                'icon': '🖥️',
                'color': '#0891b2',
                'description': 'Ajustar tamaños por resolución',
                'permission': 'system.config'
            },
            {
                'id': 'ticket_config',
                'title': 'Configuración de Boletas',
                'icon': '🎫',
                'color': '#9b59b6',
                'description': 'Personalizar tickets',
                'permission': None
            },
            {
                'id': 'support',
                'title': 'Chat de soporte',
                'icon': '💬',
                'color': '#15803d',
                'description': 'Ayuda y soporte',
                'permission': None
            },
            {
                'id': 'help',
                'title': 'Ayuda',
                'icon': '❓',
                'color': '#b91c1c',
                'description': 'Manual y guías',
                'permission': None
            },
            {
                'id': 'reports',
                'title': 'Reportes',
                'icon': '📋',
                'color': '#475569',
                'description': 'Informes detallados',
                'permission': 'reports.sales'
            }
        ]
        
        # Filtrar módulos según permisos del usuario
        # Filtrar módulos según permisos del usuario
        available_modules = []
        
        for module in base_modules:
            # Si no requiere permiso específico, está disponible para todos
            if module['permission'] is None:
                available_modules.append(module)
                continue
            
            # Verificar si el usuario tiene el permiso requerido
            if self._user_has_permission(module['permission']):
                available_modules.append(module)
        
        return available_modules
    
    def create_colorful_modules_grid(self, parent, modules):
        """Crear grid centrado con scroll para muchos módulos"""
        num_modules = len(modules)
        
        if num_modules == 0:
            self.create_colorful_no_access_message(parent)
            return
        
        # Contenedor principal
        main_grid_container = tk.Frame(parent, bg='#f1f5f9')
        main_grid_container.pack(fill='both', expand=True)
        
        # Crear Canvas con scrollbar
        canvas = tk.Canvas(main_grid_container, bg='#f1f5f9', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_grid_container, orient="vertical", command=canvas.yview)
        
        # Frame scrollable principal
        scrollable_frame = tk.Frame(canvas, bg='#f1f5f9')
        
        # Configurar scroll
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Configurar exactamente 4 columnas
        cols_per_row = 4
        
        # Frame centrado para los módulos - usando pack con anchor center
        centered_modules_frame = tk.Frame(scrollable_frame, bg='#f1f5f9')
        centered_modules_frame.pack(expand=True, pady=20)
        
        # Crear grid
        for i, module in enumerate(modules):
            row = i // cols_per_row
            col = i % cols_per_row
            
            self.create_fullscreen_module_card(centered_modules_frame, module, row, col)
        
        # Crear ventana en el canvas después de crear los módulos
        def center_content():
            # Actualizar para obtener el tamaño real
            scrollable_frame.update_idletasks()
            
            # Obtener ancho del canvas y del contenido
            canvas_width = canvas.winfo_width()
            content_width = scrollable_frame.winfo_reqwidth()
            
            # Calcular posición x para centrar
            if canvas_width > content_width:
                x_position = (canvas_width - content_width) // 2
            else:
                x_position = 0
            
            # Crear o actualizar ventana centrada
            canvas.delete("all")
            canvas.create_window(x_position, 0, window=scrollable_frame, anchor="nw")
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack del canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        scrollbar.pack(side="right", fill="y")
        
        # Bind para recentrar cuando cambia el tamaño
        canvas.bind("<Configure>", lambda e: center_content())
        
        # Bind para scroll con rueda del mouse - solo en el canvas, no en toda la app
        def _on_mousewheel(event):
            # Verificar que el canvas todavía existe antes de hacer scroll
            if canvas.winfo_exists():
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Binding solo cuando el mouse está sobre el canvas
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        
        # Centrar después de que todo se haya dibujado
        canvas.after(100, center_content)
    
    def create_elegant_no_access_message(self, parent):
        """Crear mensaje elegante cuando no hay módulos disponibles"""
        message_container = tk.Frame(parent, bg='#f8f9fa')
        message_container.pack(expand=True, fill='both')
        
        # Espaciado superior
        tk.Frame(message_container, bg='#f8f9fa', height=80).pack()
        
        # Contenedor principal del mensaje
        main_message = tk.Frame(message_container, bg='white', relief='flat', bd=0)
        main_message.pack(pady=20, padx=60, fill='x')
        
        # Sombra simulada
        shadow = tk.Frame(message_container, bg='#e8e9ea', height=2)
        shadow.pack(fill='x', padx=65)
        
        # Icono principal
        icon_frame = tk.Frame(main_message, bg='white')
        icon_frame.pack(pady=(40, 20))
        
        # Círculo de icono
        icon_circle = tk.Frame(icon_frame, bg='#3498db', width=100, height=100)
        icon_circle.pack()
        icon_circle.pack_propagate(False)
        
        tk.Label(
            icon_circle,
            text="🔐",
            font=('Segoe UI', 40),
            bg='#3498db',
            fg='white'
        ).place(relx=0.5, rely=0.5, anchor='center')
        
        # Título
        tk.Label(
            main_message,
            text="Acceso Restringido",
            font=('Segoe UI', 24, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(pady=(0, 15))
        
        # Descripción
        tk.Label(
            main_message,
            text="Tu cuenta actual no tiene permisos asignados para acceder a los módulos del sistema.\nContacta a tu administrador para solicitar los permisos necesarios.",
            font=('Segoe UI', 13),
            fg='#5d6d7e',
            bg='white',
            justify='center'
        ).pack(pady=(0, 30))
        
        # Panel de ayuda
        help_panel = tk.Frame(main_message, bg='#eaf4fd', relief='flat')
        help_panel.pack(fill='x', pady=(0, 30), padx=40)
        
        tk.Label(
            help_panel,
            text="� Mientras tanto...",
            font=('Segoe UI', 14, 'bold'),
            fg='#2980b9',
            bg='#eaf4fd'
        ).pack(pady=(20, 10))
        
        tk.Label(
            help_panel,
            text="Puedes contactar al soporte técnico o consultar la ayuda del sistema",
            font=('Segoe UI', 11),
            fg='#5499c7',
            bg='#eaf4fd'
        ).pack(pady=(0, 20))
    
    def create_colorful_no_access_message(self, parent):
        """Crear mensaje colorido cuando no hay módulos disponibles"""
        # Contenedor principal colorido
        message_container = tk.Frame(parent, bg='#ecf0f1')
        message_container.pack(expand=True, fill='both', pady=30)
        
        # Panel principal con gradiente
        main_panel = tk.Frame(message_container, bg='#3498db', relief='raised', bd=3)
        main_panel.pack(padx=50, pady=20, fill='both', expand=True)
        
        # Header del panel
        header_frame = tk.Frame(main_panel, bg='#2980b9', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🔐 ACCESO RESTRINGIDO",
            font=('Segoe UI', 20, 'bold'),
            fg='white',
            bg='#2980b9'
        ).pack(expand=True)
        
        # Contenido principal
        content_frame = tk.Frame(main_panel, bg='#3498db')
        content_frame.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Icono grande
        tk.Label(
            content_frame,
            text="🚫",
            font=('Segoe UI', 64),
            fg='white',
            bg='#3498db'
        ).pack(pady=(0, 20))
        
        # Mensaje principal
        tk.Label(
            content_frame,
            text="Tu cuenta no tiene permisos asignados",
            font=('Segoe UI', 18, 'bold'),
            fg='white',
            bg='#3498db'
        ).pack(pady=(0, 10))
        
        tk.Label(
            content_frame,
            text="Contacta a tu administrador para obtener acceso a los módulos del sistema",
            font=('Segoe UI', 12),
            fg='#ecf0f1',
            bg='#3498db',
            justify='center'
        ).pack(pady=(0, 20))
        
        # Panel de ayuda colorido
        help_frame = tk.Frame(content_frame, bg='#2ecc71', relief='raised', bd=2)
        help_frame.pack(fill='x', pady=10)
        
        tk.Label(
            help_frame,
            text="💬 SOPORTE DISPONIBLE 24/7",
            font=('Segoe UI', 14, 'bold'),
            fg='white',
            bg='#2ecc71'
        ).pack(pady=15)
    
    def create_colorful_info_panel(self, parent):
        """Crear panel informativo colorido para acceso limitado"""
        info_panel = tk.Frame(parent, bg='#f39c12', height=80)
        info_panel.pack(fill='x', pady=(20, 0))
        info_panel.pack_propagate(False)
        
        content = tk.Frame(info_panel, bg='#f39c12')
        content.pack(expand=True, fill='both', pady=15)
        
        # Mensaje informativo
        tk.Label(
            content,
            text="⚡ ACCESO BÁSICO ACTIVO • Solicita más permisos para acceder a funciones adicionales",
            font=('Segoe UI', 12, 'bold'),
            fg='white',
            bg='#f39c12'
        ).pack()
    
    def create_elegant_limited_access_info(self, parent):
        """Mostrar información elegante cuando el acceso es limitado"""
        info_container = tk.Frame(parent, bg='#f8f9fa')
        info_container.pack(pady=(30, 0), fill='x')
        
        # Panel informativo elegante
        info_panel = tk.Frame(info_container, bg='#fff3cd', relief='flat', bd=0)
        info_panel.pack(fill='x', padx=80)
        
        # Línea superior decorativa
        top_line = tk.Frame(info_panel, bg='#ffc107', height=3)
        top_line.pack(fill='x')
        
        # Contenido del panel
        content_frame = tk.Frame(info_panel, bg='#fff3cd')
        content_frame.pack(fill='x', padx=30, pady=20)
        
        # Icono y título en línea
        header_frame = tk.Frame(content_frame, bg='#fff3cd')
        header_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            header_frame,
            text="⚡",
            font=('Segoe UI', 18),
            bg='#fff3cd',
            fg='#b7791f'
        ).pack(side='left', padx=(0, 10))
        
        tk.Label(
            header_frame,
            text="Acceso Básico Activo",
            font=('Segoe UI', 14, 'bold'),
            fg='#b7791f',
            bg='#fff3cd'
        ).pack(side='left')
        
        # Mensaje descriptivo
        tk.Label(
            content_frame,
            text="Tienes acceso a funciones básicas del sistema. Para acceder a más módulos, solicita permisos adicionales a tu administrador.",
            font=('Segoe UI', 10),
            fg='#856404',
            bg='#fff3cd',
            wraplength=400,
            justify='left'
        ).pack(anchor='w')
    
    def create_fullscreen_module_card(self, parent, module, row, col):
        """Crear tarjeta moderna con diseño limpio y auto-escalado"""
        
        # Obtener tamaños escalados automáticamente
        card_width = self.scaler.scale_value(220)
        card_height = self.scaler.scale_value(140)
        card_padding = self.scaler.scale_padding(12)
        
        # Contenedor principal con sombra - tamaño escalado
        shadow_container = tk.Frame(parent, bg='#e2e8f0', width=card_width, height=card_height)
        shadow_container.grid(row=row, column=col, padx=card_padding, pady=card_padding)
        shadow_container.grid_propagate(False)
        
        # Frame de la tarjeta con elevación
        card_container = tk.Frame(shadow_container, bg='#ffffff', relief='flat', bd=0)
        card_container.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Canvas principal con color del módulo
        canvas = tk.Canvas(
            card_container,
            bg=module['color'],
            highlightthickness=0,
            relief='flat',
            bd=0
        )
        canvas.pack(fill='both', expand=True)
        
        # Función para crear contenido con efectos visuales
        def on_canvas_configure(event):
            canvas_width = event.width if hasattr(event, 'width') else card_width
            canvas_height = event.height if hasattr(event, 'height') else card_height
            
            # Evitar tamaños muy pequeños
            if canvas_width < 50 or canvas_height < 50:
                return
            
            # Limpiar canvas
            canvas.delete("all")
            
            # Crear fondo del módulo
            canvas.create_rectangle(0, 0, canvas_width, canvas_height, fill=module['color'], outline='')
            
            # Calcular posiciones centradas
            center_x = canvas_width // 2
            icon_y = canvas_height * 0.35
            title_y = canvas_height * 0.72
            
            # Tamaños de fuente escalados
            icon_size = self.scaler.scale_font(36)
            title_size = self.scaler.scale_font(11)
            
            # Círculo blanco de fondo para el icono (escalado)
            icon_radius = self.scaler.scale_value(28)
            canvas.create_oval(
                center_x - icon_radius, icon_y - icon_radius,
                center_x + icon_radius, icon_y + icon_radius,
                fill='white', outline='', width=0
            )
            
            # Icono principal
            canvas.create_text(
                center_x, icon_y,
                text=module['icon'],
                font=('Segoe UI Emoji', icon_size),
                fill=module['color'],
                anchor='center'
            )
            
            # Título principal con buen contraste
            canvas.create_text(
                center_x, title_y,
                text=module['title'],
                font=('Segoe UI', title_size, 'bold'),
                fill='white',
                anchor='center',
                width=canvas_width - 20
            )
        
        # Bind para redimensionamiento
        canvas.bind('<Configure>', on_canvas_configure)
        
        # Dibujar contenido inicial inmediatamente con tamaños escalados
        canvas.after(1, lambda: on_canvas_configure(type('Event', (), {'width': card_width, 'height': card_height})()))
        
        # Sistema de eventos con efectos mejorados
        self.setup_enhanced_card_events(canvas, module, card_container)
        
        return shadow_container
    
    def create_card_gradient(self, canvas, base_color, width, height):
        """Crear efecto de gradiente en la tarjeta"""
        try:
            # Convertir color base a RGB
            hex_color = base_color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            # Crear gradiente vertical
            num_strips = 20
            strip_height = height // num_strips
            
            for i in range(num_strips):
                # Calcular color para cada tira
                factor = i / num_strips
                new_r = int(r + (255 - r) * factor * 0.1)
                new_g = int(g + (255 - g) * factor * 0.1)
                new_b = int(b + (255 - b) * factor * 0.1)
                
                strip_color = f"#{new_r:02x}{new_g:02x}{new_b:02x}"
                
                canvas.create_rectangle(
                    0, i * strip_height,
                    width, (i + 1) * strip_height,
                    fill=strip_color, outline='', width=0,
                    tags='gradient'
                )
        except:
            # Fallback: color sólido
            canvas.create_rectangle(0, 0, width, height, fill=base_color, outline='')
    
    def create_card_decorations(self, canvas, width, height):
        """Crear decoraciones geométricas en la tarjeta"""
        # Círculos decorativos en las esquinas
        circle_size = min(width, height) // 8
        
        # Círculo superior izquierdo
        canvas.create_oval(
            -circle_size//2, -circle_size//2,
            circle_size//2, circle_size//2,
            fill='white', outline='', width=0,
            stipple='gray25', tags='decoration'
        )
        
        # Círculo inferior derecho
        canvas.create_oval(
            width - circle_size//2, height - circle_size//2,
            width + circle_size//2, height + circle_size//2,
            fill='white', outline='', width=0,
            stipple='gray25', tags='decoration'
        )
        
        # Líneas decorativas
        canvas.create_line(
            0, height * 0.9, width * 0.3, height * 0.9,
            fill='white', width=2, stipple='gray50', tags='decoration'
        )
    
    def setup_enhanced_card_events(self, canvas, module, card_container):
        """Sistema de eventos simple - solo click sin efectos hover"""
        
        def on_click(event):
            """Click simple - ejecutar acción del módulo"""
            try:
                self.on_module_click(module['id'])
            except Exception as e:
                print(f"Error: {e}")
        
        # Solo cambiar cursor al pasar sobre el módulo
        def on_enter(event):
            canvas.configure(cursor='hand2')
        
        def on_leave(event):
            canvas.configure(cursor='')
        
        # Bind eventos simples
        canvas.bind("<Button-1>", on_click)
        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        
        return canvas
    
    def calculate_enhanced_hover_color(self, hex_color):
        """Calcular color hover con efecto más sutil"""
        try:
            hex_color = hex_color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            # Aclarar solo un poco para efecto sutil
            r = min(255, r + 20)
            g = min(255, g + 20)
            b = min(255, b + 20)
            
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return hex_color
    
    def calculate_enhanced_click_color(self, hex_color):
        """Calcular color click con efecto más sutil"""
        try:
            hex_color = hex_color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            # Oscurecer solo un poco para efecto sutil
            r = max(0, r - 20)
            g = max(0, g - 20)
            b = max(0, b - 20)
            
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return hex_color
    
    def create_colorful_module_card(self, parent, module, row, col):
        """Método mantenido para compatibilidad - redirige al nuevo método"""
        return self.create_fullscreen_module_card(parent, module, row, col)
    

        for child in widget.winfo_children():
            widgets.extend(self.get_all_card_widgets(child))
        return widgets
    

    
    def setup_professional_card_events(self, canvas, module):
        """Sistema de eventos profesional usando Canvas - sin interferencias"""
        
        # Variables de estado para ESTA tarjeta específica
        original_color = module['color']
        hover_color = self.calculate_hover_color(original_color)
        click_color = self.calculate_click_color(original_color)
        
        # Estado interno de la tarjeta
        card_state = {
            'is_hovered': False,
            'is_pressed': False
        }
        
        def on_enter_canvas(event):
            """Entrada al canvas - cambio visual"""
            if not card_state['is_hovered']:
                card_state['is_hovered'] = True
                canvas.configure(
                    bg=hover_color,
                    highlightbackground='#007acc',
                    highlightthickness=3,
                    cursor='hand2'
                )
        
        def on_leave_canvas(event):
            """Salida del canvas - restaurar"""
            if card_state['is_hovered']:
                card_state['is_hovered'] = False
                card_state['is_pressed'] = False
                canvas.configure(
                    bg=original_color,
                    highlightbackground='#cccccc',
                    highlightthickness=2,
                    cursor=''
                )
        
        def on_button_press(event):
            """Presionar botón - efecto visual"""
            card_state['is_pressed'] = True
            canvas.configure(
                bg=click_color,
                relief='sunken',
                bd=1
            )
        
        def on_button_release(event):
            """Soltar botón - ejecutar acción"""
            if card_state['is_pressed']:
                card_state['is_pressed'] = False
                
                # Restaurar apariencia
                if card_state['is_hovered']:
                    canvas.configure(bg=hover_color, relief='raised', bd=3)
                else:
                    canvas.configure(bg=original_color, relief='raised', bd=3)
                
                # Ejecutar acción del módulo
                try:
                    self.open_module(module['action'])
                except Exception as e:
                    print(f"Error ejecutando módulo {module['title']}: {e}")
        
        # Aplicar eventos SOLO al canvas (sin propagación problemática)
        canvas.bind("<Enter>", on_enter_canvas)
        canvas.bind("<Leave>", on_leave_canvas)
        canvas.bind("<Button-1>", on_button_press)
        canvas.bind("<ButtonRelease-1>", on_button_release)
        
        # Importante: configurar para que el canvas capture todos los eventos
        canvas.focus_set()
    
    def calculate_hover_color(self, hex_color):
        """Calcular color hover más claro"""
        try:
            # Remover # si existe
            hex_color = hex_color.lstrip('#')
            
            # Convertir a RGB
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            # Aclarar (aumentar hacia 255)
            r = min(255, r + 40)
            g = min(255, g + 40)
            b = min(255, b + 40)
            
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return hex_color
    
    def calculate_click_color(self, hex_color):
        """Calcular color click más oscuro"""
        try:
            # Remover # si existe
            hex_color = hex_color.lstrip('#')
            
            # Convertir a RGB
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            # Oscurecer (reducir hacia 0)
            r = max(0, r - 50)
            g = max(0, g - 50)
            b = max(0, b - 50)
            
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return hex_color
    

    

    

    

    

    
    def fill_empty_grid_spaces(self, parent, num_modules, cols_per_row):
        """Llenar espacios vacíos del grid con tarjetas informativas"""
        info_cards = [
            {
                'icon': '📈',
                'title': 'Estadísticas',
                'desc': 'Próximamente',
                'color': '#95a5a6'
            },
            {
                'icon': '🔔',
                'title': 'Notificaciones',
                'desc': 'Sin notificaciones',
                'color': '#34495e'
            },
            {
                'icon': '⚙️',
                'title': 'Configuración',
                'desc': 'Personalizar',
                'color': '#7f8c8d'
            },
            {
                'icon': '📊',
                'title': 'Análisis',
                'desc': 'En desarrollo',
                'color': '#16a085'
            },
            {
                'icon': '🎯',
                'title': 'Objetivos',
                'desc': 'Establecer metas',
                'color': '#8e44ad'
            }
        ]
        
        # Calcular cuántos espacios llenar (máximo hasta completar 3 filas)
        max_cards = 9
        spaces_to_fill = min(max_cards - num_modules, len(info_cards))
        
        for i in range(spaces_to_fill):
            card_index = num_modules + i
            row = card_index // cols_per_row
            col = card_index % cols_per_row
            
            info_card = info_cards[i]
            self.create_info_card(parent, info_card, row, col)
    
    def create_info_card(self, parent, info, row, col):
        """Crear tarjeta informativa para espacios vacíos"""
        card_frame = tk.Frame(
            parent,
            bg='#ecf0f1',
            relief='groove',
            bd=1,
            padx=15,
            pady=15
        )
        card_frame.grid(
            row=row, 
            column=col, 
            padx=15, 
            pady=15, 
            sticky='nsew',
            ipadx=10,
            ipady=10
        )
        
        # Icono
        icon_label = tk.Label(
            card_frame,
            text=info['icon'],
            font=('Segoe UI', 28),
            bg='#ecf0f1',
            fg=info['color']
        )
        icon_label.pack(pady=(10, 5))
        
        # Título
        title_label = tk.Label(
            card_frame,
            text=info['title'],
            font=('Segoe UI', 14, 'bold'),
            fg='#34495e',
            bg='#ecf0f1'
        )
        title_label.pack(pady=(0, 5))
        
        # Descripción
        desc_label = tk.Label(
            card_frame,
            text=info['desc'],
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='#ecf0f1'
        )
        desc_label.pack()
    
    def darken_color(self, color_hex, factor=0.2):
        """Oscurecer un color hexadecimal para efectos hover"""
        try:
            # Convertir hex a RGB
            hex_color = color_hex.replace('#', '')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            
            # Oscurecer cada componente
            darkened = tuple(max(0, int(c * (1 - factor))) for c in rgb)
            
            # Convertir de vuelta a hex
            return '#{:02x}{:02x}{:02x}'.format(*darkened)
        except:
            # Si hay error, devolver color original
            return color_hex
    
    def create_status_footer(self):
        """Crear footer moderno minimalista"""
        # Footer principal
        footer_frame = tk.Frame(self.root, bg='#1e293b', height=40)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        # Línea superior
        top_line = tk.Frame(footer_frame, bg='#334155', height=1)
        top_line.pack(fill='x')
        
        # Contenedor principal del footer
        main_footer = tk.Frame(footer_frame, bg='#1e293b')
        main_footer.pack(expand=True, fill='both', padx=20, pady=8)
        
        # Panel izquierdo - Estado
        left_panel = tk.Frame(main_footer, bg='#1e293b')
        left_panel.pack(side='left', fill='y')
        
        status_label = tk.Label(
            left_panel,
            text="🟢 Sistema Activo",
            font=('Segoe UI', 9),
            fg='#94a3b8',
            bg='#1e293b'
        )
        status_label.pack(side='left')
        
        # Panel derecho - Versión
        right_panel = tk.Frame(main_footer, bg='#1e293b')
        right_panel.pack(side='right', fill='y')
        
        version_label = tk.Label(
            right_panel,
            text="ManagementPro POS v1.0 © 2025",
            font=('Segoe UI', 9),
            fg='#64748b',
            bg='#1e293b'
        )
        version_label.pack(side='right')
    
    def bind_module_callback(self, module_id: str, callback: Callable):
        """Registrar callback para un módulo específico"""
        self.module_callbacks[module_id] = callback
    
    def open_responsive_configurator(self):
        """Abrir el configurador de escalado responsivo"""
        import subprocess
        import sys
        
        try:
            # Obtener la ruta del configurador
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            configurator_path = os.path.join(script_dir, 'responsive_configurator.py')
            
            if not os.path.exists(configurator_path):
                from tkinter import messagebox
                messagebox.showerror("Error", 
                                   f"❌ No se encontró el configurador responsivo en:\n{configurator_path}")
                return
            
            # Abrir el configurador en un proceso separado
            subprocess.Popen([sys.executable, configurator_path])
            
            # Mostrar mensaje informativo
            from tkinter import messagebox
            messagebox.showinfo("Configurador Responsivo", 
                              "✅ Se ha abierto el configurador de escalado responsivo.\n\n"
                              "⚠️ Los cambios que realices requerirán reiniciar la aplicación para aplicarse.")
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", 
                               f"❌ Error al abrir el configurador responsivo:\n{str(e)}")
    
    def on_module_click(self, module_id: str):
        """Manejar click en módulo"""
        # Manejar módulos especiales
        if module_id == 'responsive_config':
            self.open_responsive_configurator()
            return
        
        if module_id in self.module_callbacks:
            self.module_callbacks[module_id]()
        else:
            # Callback por defecto si no hay uno específico
            self.trigger_callback('module_selected', {'module_id': module_id})
    
    def update_user_info(self, user_data: Dict[str, Any]):
        """Actualizar información del usuario en el header"""
        self.user_data = user_data
        # TODO: Actualizar labels del header con nueva información
    
    def show_notification(self, message: str, notification_type: str = 'info'):
        """Mostrar notificación temporal"""
        # TODO: Implementar sistema de notificaciones toast
        pass
    
    def load_company_config(self):
        """Cargar configuración de la empresa desde system_config.json"""
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'system_config.json')
            
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                company_name = config.get('company_name', 'MANAGEMENTPRO POS')
                logo_path = config.get('logo_path', '')
                
                return company_name, logo_path
        except Exception as e:
            # Error silencioso, usar valores por defecto
            pass
        
        return 'MANAGEMENTPRO POS', ''
    
    def load_company_logo(self, container, logo_path):
        """Cargar y mostrar el logo de la empresa"""
        try:
            # Cargar y redimensionar imagen
            pil_image = Image.open(logo_path)
            pil_image = pil_image.resize((50, 50), Image.Resampling.LANCZOS)
            
            # Convertir a PhotoImage usando self.root como master
            logo_image = ImageTk.PhotoImage(pil_image, master=self.root)
            
            # Crear label con la imagen
            logo_label = tk.Label(
                container,
                image=logo_image,
                bg='#ffffff',
                bd=0
            )
            # IMPORTANTE: Mantener referencia de la imagen en el label para evitar garbage collection
            logo_label.image = logo_image
            logo_label.place(relx=0.5, rely=0.5, anchor='center')
            
        except Exception as e:
            # Si falla, usar logo por defecto
            self.create_default_logo(container)
    
    def create_default_logo(self, container):
        """Crear logo por defecto con emoji"""
        logo_bg = tk.Frame(container, bg='#1e3a8a', width=50, height=50)
        logo_bg.place(relx=0.5, rely=0.5, anchor='center')
        logo_bg.pack_propagate(False)
        
        logo_label = tk.Label(
            logo_bg,
            text="🏪",
            font=('Segoe UI Emoji', 24),
            fg='white',
            bg='#1e3a8a'
        )
        logo_label.place(relx=0.5, rely=0.5, anchor='center')
    
    def _user_has_permission(self, permission: str) -> bool:
        """Verificar si el usuario actual tiene un permiso específico"""
        try:
            if not self.user_data:
                return False
            
            return self.permission_service.check_permission(self.user_data, permission)
            
        except Exception as e:
            # Log silencioso, no imprimir en consola
            return False
    
    def _get_user_role_display_name(self) -> str:
        """Obtener el nombre real del rol del usuario para mostrar en el dashboard"""
        try:
            if not self.user_data:
                return "Usuario"
            
            # Si ya tiene role_name en los datos del usuario, usarlo
            if 'role_name' in self.user_data:
                return self.user_data['role_name']
            
            # Si tiene role_id, buscar el nombre del rol
            role_id = self.user_data.get('role_id')
            if role_id:
                role_model = RoleModel()
                role_data = role_model.get_role_by_id(role_id)
                if role_data and 'name' in role_data:
                    return role_data['name']
            
            # Fallback: usar user_type pero capitalizado
            user_type = self.user_data.get('user_type', 'usuario')
            return user_type.title()
            
        except Exception as e:
            # En caso de error, usar fallback silencioso
            return self.user_data.get('user_type', 'Usuario').title()
