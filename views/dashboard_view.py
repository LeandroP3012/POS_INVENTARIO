"""
Vista del Dashboard Principal - Interfaz de Módulos
Diseño moderno con cards/tarjetas por módulo
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Callable
from views.base_view import BaseView


class DashboardView(BaseView):
    """Vista del dashboard principal con diseño de módulos/tarjetas"""
    
    def __init__(self, root: tk.Tk, user_data: Dict[str, Any] = None):
        super().__init__(root)
        self.user_data = user_data or {}
        self.module_callbacks = {}
        self.setup_dashboard()
    
    def setup_dashboard(self):
        """Configurar interfaz del dashboard"""
        self.setup_main_window()
        self.create_header()
        self.create_modules_grid()
        self.create_status_footer()
    
    def setup_main_window(self):
        """Configurar ventana principal"""
        self.root.title("Sistema POS - Dashboard Principal")
        self.root.geometry("1200x800")
        self.root.state('zoomed')
        self.root.configure(bg='#f8f9fa')
    
    def create_header(self):
        """Crear header con información del usuario"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Contenedor interno para centrar contenido
        content_frame = tk.Frame(header_frame, bg='#2c3e50')
        content_frame.pack(expand=True, fill='both', padx=40, pady=20)
        
        # Título del sistema
        title_label = tk.Label(
            content_frame,
            text="🏪 ManagementPro POS",
            font=('Segoe UI', 24, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(side='left')
        
        # Información del usuario (lado derecho)
        user_frame = tk.Frame(content_frame, bg='#2c3e50')
        user_frame.pack(side='right')
        
        welcome_text = f"Bienvenido, {self.user_data.get('full_name', self.user_data.get('username', 'Usuario'))}"
        user_label = tk.Label(
            user_frame,
            text=welcome_text,
            font=('Segoe UI', 14),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        user_label.pack(anchor='e')
        
        role_text = f"Rol: {self.user_data.get('user_type', 'Usuario').title()}"
        role_label = tk.Label(
            user_frame,
            text=role_text,
            font=('Segoe UI', 12),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        role_label.pack(anchor='e')
    
    def create_modules_grid(self):
        """Crear grid de módulos principales"""
        # Subtitle
        subtitle_frame = tk.Frame(self.root, bg='#f8f9fa', pady=30)
        subtitle_frame.pack(fill='x')
        
        subtitle_label = tk.Label(
            subtitle_frame,
            text="Bienvenido a tu sistema de punto de venta\n¡Comienza a registrar tu información!",
            font=('Segoe UI', 18, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa',
            justify='center'
        )
        subtitle_label.pack()
        
        # Línea decorativa
        line_frame = tk.Frame(subtitle_frame, bg='#3498db', height=3)
        line_frame.pack(fill='x', padx=200, pady=(20, 0))
        
        # Grid principal de módulos
        modules_frame = tk.Frame(self.root, bg='#f8f9fa')
        modules_frame.pack(fill='both', expand=True, padx=80, pady=40)
        
        # Definir módulos con sus colores y permisos
        modules = self.get_available_modules()
        
        # Crear grid 3x3
        for i, module in enumerate(modules):
            row = i // 3
            col = i % 3
            
            self.create_module_card(modules_frame, module, row, col)
    
    def get_available_modules(self):
        """Obtener módulos disponibles según permisos del usuario"""
        base_modules = [
            {
                'id': 'clients',
                'title': 'Clientes',
                'icon': '👥',
                'color': '#1abc9c',
                'description': 'Gestionar clientes',
                'permission': None  # Disponible para todos
            },
            {
                'id': 'products',
                'title': 'Productos',
                'icon': '📦',
                'color': '#f39c12',
                'description': 'Inventario y catálogo',
                'permission': 'inventory_view'
            },
            {
                'id': 'purchases',
                'title': 'Compras',
                'icon': '🛍️',
                'color': '#e74c3c',
                'description': 'Registro de compras',
                'permission': 'purchases_manage'
            },
            {
                'id': 'quick_sale',
                'title': 'Venta rápida',
                'icon': '💰',
                'color': '#e67e22',
                'description': 'Ventas directas',
                'permission': None  # Disponible para todos
            },
            {
                'id': 'results',
                'title': 'Resultados',
                'icon': '📊',
                'color': '#9b59b6',
                'description': 'Reportes y análisis',
                'permission': 'reports_basic'
            },
            {
                'id': 'business',
                'title': 'Mi negocio',
                'icon': '🏢',
                'color': '#3498db',
                'description': 'Configuración general',
                'permission': 'business_config'
            },
            {
                'id': 'support',
                'title': 'Chat de soporte',
                'icon': '💬',
                'color': '#2ecc71',
                'description': 'Ayuda y soporte',
                'permission': None  # Disponible para todos
            },
            {
                'id': 'help',
                'title': 'Ayuda',
                'icon': '❓',
                'color': '#e74c3c',
                'description': 'Manual y guías',
                'permission': None  # Disponible para todos
            },
            {
                'id': 'reports',
                'title': 'Reportes',
                'icon': '📋',
                'color': '#34495e',
                'description': 'Informes detallados',
                'permission': 'reports_full'
            }
        ]
        
        # Filtrar módulos según permisos (por ahora devolvemos todos)
        # TODO: Implementar filtrado real basado en permisos del usuario
        return base_modules
    
    def create_module_card(self, parent, module, row, col):
        """Crear tarjeta de módulo individual"""
        # Frame principal de la tarjeta
        card_frame = tk.Frame(
            parent,
            bg='white',
            relief='solid',
            bd=1,
            padx=20,
            pady=20
        )
        card_frame.grid(
            row=row, 
            col=col, 
            padx=20, 
            pady=20, 
            sticky='nsew',
            ipadx=10,
            ipady=10
        )
        
        # Configurar grid weights para responsive
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Contenedor del icono circular
        icon_container = tk.Frame(card_frame, bg='white')
        icon_container.pack(pady=(0, 15))
        
        # Círculo de color para el icono
        icon_circle = tk.Frame(
            icon_container,
            bg=module['color'],
            width=80,
            height=80
        )
        icon_circle.pack()
        icon_circle.pack_propagate(False)
        
        # Hacer el círculo redondo (aproximado)
        icon_circle.configure(relief='solid', bd=2)
        
        # Icono dentro del círculo
        icon_label = tk.Label(
            icon_circle,
            text=module['icon'],
            font=('Segoe UI', 28),
            bg=module['color'],
            fg='white'
        )
        icon_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Título del módulo
        title_label = tk.Label(
            card_frame,
            text=module['title'],
            font=('Segoe UI', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        title_label.pack(pady=(0, 5))
        
        # Descripción del módulo
        desc_label = tk.Label(
            card_frame,
            text=module['description'],
            font=('Segoe UI', 11),
            fg='#7f8c8d',
            bg='white'
        )
        desc_label.pack()
        
        # Efectos hover
        self.setup_card_hover_effects(card_frame, icon_circle, module)
        
        # Bind click
        self.setup_card_click(card_frame, module)
        
        return card_frame
    
    def setup_card_hover_effects(self, card_frame, icon_circle, module):
        """Configurar efectos hover para las tarjetas"""
        def on_enter(event):
            card_frame.configure(bg='#f8f9fa', relief='solid', bd=2)
            icon_circle.configure(bg=self.darken_color(module['color']))
        
        def on_leave(event):
            card_frame.configure(bg='white', relief='solid', bd=1)
            icon_circle.configure(bg=module['color'])
        
        # Aplicar hover a todos los widgets de la tarjeta
        widgets_to_bind = [card_frame] + list(card_frame.winfo_children())
        for widget in widgets_to_bind:
            try:
                widget.bind('<Enter>', on_enter)
                widget.bind('<Leave>', on_leave)
            except:
                pass  # Algunos widgets pueden no soportar bind
    
    def setup_card_click(self, card_frame, module):
        """Configurar click en las tarjetas"""
        def on_click(event):
            self.on_module_click(module['id'])
        
        # Aplicar click a todos los widgets de la tarjeta
        widgets_to_bind = [card_frame] + self.get_all_children(card_frame)
        for widget in widgets_to_bind:
            try:
                widget.bind('<Button-1>', on_click)
                widget.configure(cursor='hand2')
            except:
                pass
    
    def get_all_children(self, widget):
        """Obtener todos los widgets hijos recursivamente"""
        children = []
        for child in widget.winfo_children():
            children.append(child)
            children.extend(self.get_all_children(child))
        return children
    
    def darken_color(self, color_hex):
        """Oscurecer un color hexadecimal para efectos hover"""
        # Convertir hex a RGB
        hex_color = color_hex.replace('#', '')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Oscurecer cada componente
        darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
        
        # Convertir de vuelta a hex
        return '#{:02x}{:02x}{:02x}'.format(*darkened)
    
    def create_status_footer(self):
        """Crear footer con información de estado"""
        footer_frame = tk.Frame(self.root, bg='#ecf0f1', height=50)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        # Información del sistema
        info_frame = tk.Frame(footer_frame, bg='#ecf0f1')
        info_frame.pack(expand=True, fill='both', padx=20)
        
        # Estado del sistema (izquierda)
        status_label = tk.Label(
            info_frame,
            text="🟢 Sistema funcionando correctamente",
            font=('Segoe UI', 10),
            fg='#27ae60',
            bg='#ecf0f1'
        )
        status_label.pack(side='left', pady=15)
        
        # Versión (derecha)
        version_label = tk.Label(
            info_frame,
            text="Sistema POS v1.0 • 2025",
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='#ecf0f1'
        )
        version_label.pack(side='right', pady=15)
    
    def bind_module_callback(self, module_id: str, callback: Callable):
        """Registrar callback para un módulo específico"""
        self.module_callbacks[module_id] = callback
    
    def on_module_click(self, module_id: str):
        """Manejar click en módulo"""
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
