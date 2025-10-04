"""
Controlador Principal del Sistema POS
Maneja la aplicación completa y coordina entre controladores
"""

import tkinter as tk
from tkinter import messagebox
import logging
import sys
import os
from typing import Dict, Any, Optional
from controllers.auth_controller import AuthController
from views.login_view import LoginView
from config.settings import SystemSettings
from models.role_model import RoleModel

class MainController:
    """Controlador principal de la aplicación"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.settings = SystemSettings()
        
        # Estado de la aplicación
        self.is_running = False
        self.current_user = None
        
        # Controladores
        self.auth_controller = AuthController()
        
        # Ventana principal (se crea después del login)
        self.main_window = None
        
        # Configurar logging
        self._setup_logging()
        
        # Configurar controladores
        self._setup_controllers()
        
        self.logger.info("Sistema POS iniciado")
    
    def _setup_logging(self):
        """Configurar sistema de logging"""
        try:
            # Crear directorio de logs si no existe
            os.makedirs('logs', exist_ok=True)
            
            # Configurar logging si no está configurado
            if not logging.getLogger().handlers:
                logging.basicConfig(
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('logs/app.log', encoding='utf-8'),
                        logging.StreamHandler()
                    ]
                )
            
        except Exception as e:
            print(f"Error configurando logging: {e}")
    
    def _setup_controllers(self):
        """Configurar callbacks de controladores"""
        # Configurar callbacks del controlador de autenticación
        self.auth_controller.set_login_success_callback(self._on_login_success)
        self.auth_controller.set_login_failure_callback(self._on_login_failure)
        self.auth_controller.set_logout_callback(self._on_logout)
    
    def start(self):
        """Iniciar la aplicación"""
        try:
            self.is_running = True
            self.logger.info("Iniciando aplicación POS")
            
            # Mostrar pantalla de login
            self._show_login()
            
        except Exception as e:
            self.logger.error(f"Error iniciando aplicación: {e}")
            self._show_error("Error Fatal", f"No se pudo iniciar la aplicación: {str(e)}")
            sys.exit(1)
    
    def _show_login(self):
        """Mostrar pantalla de login"""
        try:
            self.logger.info("Mostrando pantalla de login")
            self.auth_controller.show_login()
            
        except Exception as e:
            self.logger.error(f"Error mostrando login: {e}")
            self._show_error("Error de Login", f"No se pudo mostrar la pantalla de login: {str(e)}")
    
    def _on_login_success(self, user_data: Dict[str, Any]):
        """Manejar login exitoso"""
        try:
            self.current_user = user_data
            username = user_data.get('username', 'Usuario')
            user_type = user_data.get('user_type', 'user')
            
            self.logger.info(f"Login exitoso para {user_type}: {username}")
            
            # Crear y mostrar ventana principal
            self._create_main_window()
            
        except Exception as e:
            self.logger.error(f"Error después del login exitoso: {e}")
            self._show_error("Error", f"Error al inicializar la aplicación: {str(e)}")
    
    def _on_login_failure(self, error_message: str):
        """Manejar fallo de login"""
        self.logger.warning(f"Fallo de login: {error_message}")
        # El error ya se muestra en la vista de login
    
    def _on_logout(self, username: str, reason: str):
        """Manejar logout"""
        try:
            self.logger.info(f"Logout de usuario {username}, razón: {reason}")
            
            # Cerrar ventana principal si existe
            if self.main_window:
                self.main_window.destroy()
                self.main_window = None
            
            # Limpiar datos del usuario actual
            self.current_user = None
            
            # Mostrar login nuevamente si el logout no fue por cierre de aplicación
            if reason != 'cleanup' and self.is_running:
                self._show_login()
            
        except Exception as e:
            self.logger.error(f"Error en logout: {e}")
    
    def _create_main_window(self):
        """Crear ventana principal del sistema"""
        try:
            # Crear ventana principal
            self.main_window = tk.Tk()
            self.main_window.title("Sistema POS - Panel Principal")
            self.main_window.geometry("1200x800")
            self.main_window.state('zoomed')  # Maximizar en Windows
            
            # Configurar protocolo de cierre
            self.main_window.protocol("WM_DELETE_WINDOW", self._on_main_window_close)
            
            # Configurar colores
            colors = self.settings.get_colors()
            self.main_window.configure(bg=colors['background'])
            
            # Crear interfaz principal
            self._create_main_interface()
            
            # Mostrar ventana
            self.main_window.deiconify()
            self.main_window.lift()
            self.main_window.focus_force()
            
            # Iniciar loop principal
            self.main_window.mainloop()
            
        except Exception as e:
            self.logger.error(f"Error creando ventana principal: {e}")
            self._show_error("Error", f"No se pudo crear la ventana principal: {str(e)}")
    
    def _create_main_interface(self):
        """Crear interfaz principal"""
        try:
            # Crear barra de menú
            self._create_menu_bar()
            
            # Crear barra de herramientas
            self._create_toolbar()
            
            # Crear área principal
            self._create_main_area()
            
            # Crear barra de estado
            self._create_status_bar()
            
        except Exception as e:
            self.logger.error(f"Error creando interfaz principal: {e}")
            raise
    
    def _create_menu_bar(self):
        """Crear barra de menú"""
        menubar = tk.Menu(self.main_window)
        self.main_window.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nueva Venta", command=self._new_sale)
        file_menu.add_separator()
        file_menu.add_command(label="Cerrar Sesión", command=self._logout)
        file_menu.add_command(label="Salir", command=self._exit_application)
        
        # Menú Ventas
        sales_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ventas", menu=sales_menu)
        sales_menu.add_command(label="Nueva Venta", command=self._new_sale)
        sales_menu.add_command(label="Historial de Ventas", command=self._sales_history)
        
        # Menú Inventario (solo si tiene permisos)
        if self.auth_controller.has_permission('inventory_view'):
            inventory_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Inventario", menu=inventory_menu)
            inventory_menu.add_command(label="Ver Productos", command=self._view_products)
            
            if self.auth_controller.has_permission('inventory_manage'):
                inventory_menu.add_command(label="Agregar Producto", command=self._add_product)
                inventory_menu.add_command(label="Gestionar Inventario", command=self._manage_inventory)
        
        # Menú Reportes (solo supervisores y admins)
        if self.auth_controller.has_permission('reports_basic'):
            reports_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Reportes", menu=reports_menu)
            reports_menu.add_command(label="Ventas del Día", command=self._daily_sales_report)
            
            if self.auth_controller.has_permission('reports_full'):
                reports_menu.add_command(label="Reporte Completo", command=self._full_report)
        
        # Menú Administración (solo admins)
        if self.auth_controller.has_permission('users_manage'):
            admin_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Administración", menu=admin_menu)
            admin_menu.add_command(label="Gestionar Usuarios", command=self._manage_users)
            admin_menu.add_command(label="Gestionar Roles", command=self._manage_roles)
            admin_menu.add_separator()
            admin_menu.add_command(label="Configuración", command=self._system_config)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Manual de Usuario", command=self._show_manual)
        help_menu.add_command(label="Acerca de", command=self._show_about)
    
    def _create_toolbar(self):
        """Crear barra de herramientas"""
        toolbar_frame = tk.Frame(self.main_window, bg=self.settings.get_colors()['surface'])
        toolbar_frame.pack(fill='x', padx=5, pady=5)
        
        # Información del usuario
        user_info = f"Usuario: {self.current_user.get('full_name', self.current_user.get('username'))}"
        user_info += f" ({self.current_user.get('user_type', 'user').title()})"
        
        user_label = tk.Label(
            toolbar_frame,
            text=user_info,
            bg=self.settings.get_colors()['surface'],
            fg=self.settings.get_colors()['on_surface'],
            font=('Segoe UI', 10, 'bold')
        )
        user_label.pack(side='left', padx=10)
        
        # Botones de acción rápida
        quick_buttons_frame = tk.Frame(toolbar_frame, bg=self.settings.get_colors()['surface'])
        quick_buttons_frame.pack(side='right', padx=10)
        
        # Botón Nueva Venta
        new_sale_btn = tk.Button(
            quick_buttons_frame,
            text="Nueva Venta",
            command=self._new_sale,
            bg=self.settings.get_colors()['primary'],
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            padx=20,
            pady=5
        )
        new_sale_btn.pack(side='left', padx=5)
        
        # Botón Cerrar Sesión
        logout_btn = tk.Button(
            quick_buttons_frame,
            text="Cerrar Sesión",
            command=self._logout,
            bg=self.settings.get_colors()['secondary'],
            fg='white',
            font=('Segoe UI', 10),
            padx=15,
            pady=5
        )
        logout_btn.pack(side='left', padx=5)
    
    def _create_main_area(self):
        """Crear área principal con dashboard moderno"""
        # Frame principal para el contenido
        main_frame = tk.Frame(self.main_window, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True)
        
        # Decidir qué tipo de dashboard mostrar
        dashboard_type = self._get_dashboard_type()
        
        if dashboard_type == 'modules':
            self._create_modules_dashboard(main_frame)
        elif dashboard_type == 'stats':
            self._create_stats_dashboard(main_frame)
        else:
            # Dashboard híbrido (por defecto)
            self._create_hybrid_dashboard(main_frame)
    
    def _get_dashboard_type(self):
        """Obtener tipo de dashboard según preferencias/permisos"""
        # Por ahora, usar dashboard híbrido por defecto
        # TODO: Permitir al usuario elegir su dashboard preferido
        return 'hybrid'
    
    def _create_modules_dashboard(self, parent):
        """Crear dashboard tipo módulos/tarjetas"""
        from views.dashboard_view import DashboardView
        
        self.dashboard_view = DashboardView(self.main_window, self.current_user)
        
        # Registrar callbacks para los módulos
        self.dashboard_view.bind_module_callback('clients', lambda: self._manage_clients())
        self.dashboard_view.bind_module_callback('products', lambda: self._view_products())
        self.dashboard_view.bind_module_callback('purchases', lambda: self._manage_purchases())
        self.dashboard_view.bind_module_callback('quick_sale', lambda: self._new_sale())
        self.dashboard_view.bind_module_callback('results', lambda: self._daily_sales_report())
        self.dashboard_view.bind_module_callback('business', lambda: self._system_config())
        self.dashboard_view.bind_module_callback('support', lambda: self._show_support())
        self.dashboard_view.bind_module_callback('help', lambda: self._show_manual())
        self.dashboard_view.bind_module_callback('reports', lambda: self._full_report())
    
    def _create_stats_dashboard(self, parent):
        """Crear dashboard con estadísticas"""
        from views.stats_dashboard_view import StatsDashboardView
        
        self.stats_dashboard = StatsDashboardView(parent, self.current_user)
    
    def _create_hybrid_dashboard(self, parent):
        """Crear dashboard híbrido (estadísticas + accesos rápidos)"""
        # Header con información del usuario
        self._create_dashboard_header(parent)
        
        # Sección de estadísticas rápidas
        self._create_quick_stats_section(parent)
        
        # Sección de módulos principales
        self._create_quick_modules_section(parent)
        
        # Footer con actividad reciente
        self._create_activity_footer(parent)
    
    def _create_dashboard_header(self, parent):
        """Crear header del dashboard híbrido"""
        header_frame = tk.Frame(parent, bg='#2c3e50', height=120)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Contenido del header
        content_frame = tk.Frame(header_frame, bg='#2c3e50')
        content_frame.pack(expand=True, fill='both', padx=40, pady=20)
        
        # Lado izquierdo - Saludo y fecha
        left_frame = tk.Frame(content_frame, bg='#2c3e50')
        left_frame.pack(side='left', fill='both', expand=True)
        
        # Saludo personalizado
        greeting = self._get_time_greeting()
        user_name = self.current_user.get('full_name', self.current_user.get('username', 'Usuario'))
        
        greeting_label = tk.Label(
            left_frame,
            text=f"{greeting}, {user_name}",
            font=('Segoe UI', 20, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        greeting_label.pack(anchor='w')
        
        # Fecha y hora actual
        from datetime import datetime
        now = datetime.now()
        date_str = now.strftime("%A, %d de %B de %Y")
        time_str = now.strftime("%H:%M")
        
        date_label = tk.Label(
            left_frame,
            text=f"📅 {date_str} • ⏰ {time_str}",
            font=('Segoe UI', 12),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        date_label.pack(anchor='w', pady=(5, 0))
        
        # Lado derecho - Estado del sistema
        right_frame = tk.Frame(content_frame, bg='#2c3e50')
        right_frame.pack(side='right')
        
        status_label = tk.Label(
            right_frame,
            text="🟢 Sistema Activo",
            font=('Segoe UI', 14, 'bold'),
            fg='#2ecc71',
            bg='#2c3e50'
        )
        status_label.pack(anchor='e')
        
        # Obtener nombre real del rol
        role_display_name = self._get_user_role_display_name()
        
        role_label = tk.Label(
            right_frame,
            text=f"Rol: {role_display_name}",
            font=('Segoe UI', 12),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        role_label.pack(anchor='e', pady=(5, 0))
    
    def _create_quick_stats_section(self, parent):
        """Crear sección de estadísticas rápidas"""
        stats_frame = tk.Frame(parent, bg='#f8f9fa')
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        # Título de la sección
        title_label = tk.Label(
            stats_frame,
            text="📊 Resumen del Día",
            font=('Segoe UI', 16, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        )
        title_label.pack(pady=(0, 15))
        
        # Grid de mini-estadísticas
        stats_grid = tk.Frame(stats_frame, bg='#f8f9fa')
        stats_grid.pack(fill='x')
        
        # Estadísticas simuladas (en producción vendrían de la BD)
        quick_stats = [
            {'title': 'Ventas Hoy', 'value': '$1,247', 'icon': '💰', 'color': '#27ae60'},
            {'title': 'Transacciones', 'value': '23', 'icon': '🧾', 'color': '#3498db'},
            {'title': 'Productos Vendidos', 'value': '48', 'icon': '📦', 'color': '#e74c3c'},
            {'title': 'Promedio Ticket', 'value': '$54', 'icon': '💳', 'color': '#9b59b6'},
        ]
        
        for i, stat in enumerate(quick_stats):
            self._create_mini_stat_card(stats_grid, stat, i)
    
    def _create_mini_stat_card(self, parent, stat_data, index):
        """Crear mini tarjeta de estadística"""
        card_frame = tk.Frame(
            parent,
            bg='white',
            relief='solid',
            bd=1,
            padx=15,
            pady=12
        )
        card_frame.grid(row=0, column=index, padx=8, sticky='ew')
        parent.grid_columnconfigure(index, weight=1)
        
        # Icono
        icon_label = tk.Label(
            card_frame,
            text=stat_data['icon'],
            font=('Segoe UI', 16),
            bg='white'
        )
        icon_label.pack()
        
        # Valor
        value_label = tk.Label(
            card_frame,
            text=stat_data['value'],
            font=('Segoe UI', 18, 'bold'),
            fg=stat_data['color'],
            bg='white'
        )
        value_label.pack(pady=(2, 0))
        
        # Título
        title_label = tk.Label(
            card_frame,
            text=stat_data['title'],
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='white'
        )
        title_label.pack()
    
    def _create_quick_modules_section(self, parent):
        """Crear sección de módulos de acceso rápido"""
        modules_frame = tk.Frame(parent, bg='#f8f9fa')
        modules_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Título
        title_label = tk.Label(
            modules_frame,
            text="🚀 Accesos Rápidos",
            font=('Segoe UI', 16, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        )
        title_label.pack(pady=(0, 15))
        
        # Grid de módulos principales
        modules_grid = tk.Frame(modules_frame, bg='#f8f9fa')
        modules_grid.pack(fill='both', expand=True)
        
        # Módulos principales según permisos
        modules = self._get_main_modules()
        
        # Crear grid 2x3 o 2x4 según módulos disponibles
        cols = 4 if len(modules) > 6 else 3
        for i, module in enumerate(modules[:8]):  # Máximo 8 módulos
            row = i // cols
            col = i % cols
            self._create_quick_module_button(modules_grid, module, row, col)
    
    def _get_main_modules(self):
        """Obtener módulos principales según permisos"""
        modules = [
            {
                'title': 'Nueva Venta',
                'icon': '🛒',
                'color': '#27ae60',
                'command': self._new_sale,
                'permission': None  # Todos
            },
            {
                'title': 'Historial',
                'icon': '📋',
                'color': '#3498db',
                'command': self._sales_history,
                'permission': None  # Todos
            }
        ]
        
        # Módulos según permisos
        if self.auth_controller.has_permission('inventory_view'):
            modules.append({
                'title': 'Productos',
                'icon': '📦',
                'color': '#e74c3c',
                'command': self._view_products,
                'permission': 'inventory_view'
            })
        
        if self.auth_controller.has_permission('reports_basic'):
            modules.append({
                'title': 'Reportes',
                'icon': '📊',
                'color': '#9b59b6',
                'command': self._daily_sales_report,
                'permission': 'reports_basic'
            })
        
        if self.auth_controller.has_permission('users_manage'):
            modules.append({
                'title': 'Usuarios',
                'icon': '👥',
                'color': '#f39c12',
                'command': self._manage_users,
                'permission': 'users_manage'
            })
        
        modules.extend([
            {
                'title': 'Configuración',
                'icon': '⚙️',
                'color': '#34495e',
                'command': self._system_config,
                'permission': None
            },
            {
                'title': 'Ayuda',
                'icon': '❓',
                'color': '#e67e22',
                'command': self._show_manual,
                'permission': None
            },
            {
                'title': 'Soporte',
                'icon': '💬',
                'color': '#1abc9c',
                'command': self._show_support,
                'permission': None
            }
        ])
        
        return modules
    
    def _create_quick_module_button(self, parent, module, row, col):
        """Crear botón de módulo rápido"""
        btn = tk.Button(
            parent,
            text=f"{module['icon']}\n{module['title']}",
            command=module['command'],
            bg=module['color'],
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            width=12,
            height=3,
            relief='flat',
            cursor='hand2',
            borderwidth=0
        )
        btn.grid(row=row, column=col, padx=8, pady=8, sticky='nsew')
        
        # Configurar expansión
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Efectos hover
        def on_enter(event):
            btn.configure(bg=self._darken_color(module['color']))
        
        def on_leave(event):
            btn.configure(bg=module['color'])
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
    
    def _create_activity_footer(self, parent):
        """Crear footer con actividad reciente"""
        footer_frame = tk.Frame(parent, bg='#ecf0f1', height=60)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        content_frame = tk.Frame(footer_frame, bg='#ecf0f1')
        content_frame.pack(expand=True, fill='both', padx=20, pady=15)
        
        # Actividad reciente (izquierda)
        activity_label = tk.Label(
            content_frame,
            text="🔔 Última actividad: Venta #1234 completada (14:32)",
            font=('Segoe UI', 11),
            fg='#2c3e50',
            bg='#ecf0f1'
        )
        activity_label.pack(side='left')
        
        # Estado del sistema (derecha)
        system_label = tk.Label(
            content_frame,
            text="Sistema POS v1.0 • Base de datos conectada ✅",
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='#ecf0f1'
        )
        system_label.pack(side='right')
    
    def _get_time_greeting(self):
        """Obtener saludo según la hora del día"""
        from datetime import datetime
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            return "¡Buenos días"
        elif 12 <= hour < 18:
            return "¡Buenas tardes"
        else:
            return "¡Buenas noches"
    
    def _darken_color(self, color_hex):
        """Oscurecer un color para efectos hover"""
        # Remover # si existe
        hex_color = color_hex.replace('#', '')
        
        # Convertir a RGB
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Oscurecer (multiplicar por 0.8)
        darker_rgb = tuple(max(0, int(c * 0.8)) for c in rgb)
        
        # Convertir de vuelta a hex
        return '#{:02x}{:02x}{:02x}'.format(*darker_rgb)
    
    def _clear_main_content(self):
        """Limpiar contenido principal de la ventana"""
        # Destruir todos los widgets hijos excepto la barra de menú
        for widget in self.main_window.winfo_children():
            if not isinstance(widget, tk.Menu):
                widget.destroy()
    
    def _check_user_permission(self, permission):
        """Verificar permisos del usuario"""
        try:
            if not self.current_user:
                return False
            
            # Verificar primero si el usuario tiene permisos específicos
            user_permissions = self.current_user.get('permissions', {})
            if user_permissions.get(permission):
                return True
            
            # Usar el servicio de permisos centralizado
            return self.auth_controller.has_permission(permission)
        except Exception as e:
            print(f"   ❌ Error verificando permisos: {e}")
            self.logger.error(f"Error verificando permisos: {e}")
            return False
    
    def _back_to_dashboard(self):
        """Volver al dashboard principal"""
        try:
            # Limpiar contenido actual
            self._clear_main_content()
            
            # Recrear interfaz principal
            self._create_main_interface()
            
        except Exception as e:
            self.logger.error(f"Error volviendo al dashboard: {e}")
            messagebox.showerror("Error", f"Error volviendo al dashboard:\n{str(e)}")
    
    def _create_quick_access_panel(self, parent):
        """Crear panel de accesos rápidos"""
        panel_frame = tk.Frame(parent, bg=self.settings.get_colors()['surface'])
        panel_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        title_label = tk.Label(
            panel_frame,
            text="Accesos Rápidos",
            bg=self.settings.get_colors()['surface'],
            fg=self.settings.get_colors()['on_surface'],
            font=('Segoe UI', 14, 'bold')
        )
        title_label.pack(pady=20)
        
        # Grid de botones
        buttons_frame = tk.Frame(panel_frame, bg=self.settings.get_colors()['surface'])
        buttons_frame.pack(expand=True)
        
        # Definir botones según permisos
        buttons = []
        
        # Botón Nueva Venta (todos los usuarios)
        buttons.append({
            'text': '🛒\nNueva Venta',
            'command': self._new_sale,
            'color': self.settings.get_colors()['primary']
        })
        
        # Botón Historial (todos los usuarios)
        buttons.append({
            'text': '📋\nHistorial',
            'command': self._sales_history,
            'color': self.settings.get_colors()['secondary']
        })
        
        # Botón Productos (si tiene permisos)
        if self.auth_controller.has_permission('inventory_view'):
            buttons.append({
                'text': '📦\nProductos',
                'command': self._view_products,
                'color': self.settings.get_colors()['success']
            })
        
        # Botón Reportes (si tiene permisos)
        if self.auth_controller.has_permission('reports_basic'):
            buttons.append({
                'text': '📊\nReportes',
                'command': self._daily_sales_report,
                'color': self.settings.get_colors()['warning']
            })
        
        # Botón Administración (solo admins)
        if self.auth_controller.has_permission('users_manage'):
            buttons.append({
                'text': '⚙️\nAdministración',
                'command': self._manage_users,
                'color': self.settings.get_colors()['danger']
            })
        
        # Crear botones en grid
        cols = 3
        for i, btn_config in enumerate(buttons):
            row = i // cols
            col = i % cols
            
            btn = tk.Button(
                buttons_frame,
                text=btn_config['text'],
                command=btn_config['command'],
                bg=btn_config['color'],
                fg='white',
                font=('Segoe UI', 12, 'bold'),
                width=15,
                height=4,
                relief='flat',
                cursor='hand2'
            )
            btn.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
        
        # Configurar grid
        for i in range(cols):
            buttons_frame.grid_columnconfigure(i, weight=1)
    
    def _create_status_bar(self):
        """Crear barra de estado"""
        status_frame = tk.Frame(self.main_window, bg=self.settings.get_colors()['surface'])
        status_frame.pack(fill='x', side='bottom')
        
        # Información de sesión
        session_info = self.auth_controller.get_session_info()
        if session_info.get('authenticated'):
            time_remaining = session_info.get('time_remaining', {})
            hours = time_remaining.get('hours', 0)
            minutes = time_remaining.get('minutes', 0)
            
            status_text = f"Sesión activa - Tiempo restante: {hours}h {minutes}m"
        else:
            status_text = "Sin sesión activa"
        
        status_label = tk.Label(
            status_frame,
            text=status_text,
            bg=self.settings.get_colors()['surface'],
            fg=self.settings.get_colors()['on_surface'],
            font=('Segoe UI', 9)
        )
        status_label.pack(side='left', padx=10, pady=5)
        
        # Versión del sistema
        version_label = tk.Label(
            status_frame,
            text="Sistema POS v1.0",
            bg=self.settings.get_colors()['surface'],
            fg=self.settings.get_colors()['on_surface_variant'],
            font=('Segoe UI', 9)
        )
        version_label.pack(side='right', padx=10, pady=5)
    
    # Métodos de acción (placeholder - se implementarán con los módulos correspondientes)
    def _new_sale(self):
        """Iniciar nueva venta"""
        messagebox.showinfo("Nueva Venta", "Módulo de ventas en desarrollo")
    
    def _sales_history(self):
        """Mostrar historial de ventas"""
        messagebox.showinfo("Historial", "Módulo de historial en desarrollo")
    
    def _view_products(self):
        """Ver productos"""
        messagebox.showinfo("Productos", "Módulo de productos en desarrollo")
    
    def _add_product(self):
        """Agregar producto"""
        messagebox.showinfo("Agregar Producto", "Función en desarrollo")
    
    def _manage_inventory(self):
        """Gestionar inventario"""
        messagebox.showinfo("Inventario", "Módulo de inventario en desarrollo")
    
    def _daily_sales_report(self):
        """Reporte de ventas diarias"""
        messagebox.showinfo("Reporte Diario", "Módulo de reportes en desarrollo")
    
    def _full_report(self):
        """Reporte completo"""
        messagebox.showinfo("Reporte Completo", "Función en desarrollo")
    
    def _manage_users(self):
        """Gestionar usuarios"""
        try:
            print("👥 DEBUG: Abriendo gestión de usuarios desde main_controller")
            print(f"   - main_window tipo: {type(self.main_window)}")
            print(f"   - current_user: {self.current_user}")
            
            # Verificar permisos del usuario
            if not self._check_user_permission('users_manage'):
                messagebox.showerror("Acceso Denegado", "No tienes permisos para acceder a la gestión de usuarios")
                return
            
            # Limpiar la ventana principal
            self._clear_main_content()
            print("   ✅ Ventana principal limpiada")
            
            # Crear contenido de gestión de usuarios en la ventana principal
            from views.user_management_view import UserManagementView
            print("   🔄 Creando UserManagementView...")
            
            # Pasar el current_user como diccionario con la estructura esperada
            user_data = {
                'id': self.current_user.get('id', 0),
                'username': self.current_user.get('username', ''),
                'full_name': self.current_user.get('full_name', ''),
                'email': self.current_user.get('email', ''),
                'role': self.current_user.get('user_type', 'admin'),  # Mapear user_type a role
                'permissions': self.current_user.get('permissions', {})
            }
            
            self.users_view = UserManagementView(self.main_window, user_data, embedded=True)
            print("   ✅ UserManagementView creada exitosamente")
            
            # Registrar callbacks
            self.users_view.bind_callback('back_to_dashboard', self._back_to_dashboard)
            print("   ✅ Callbacks registrados")
            
        except Exception as e:
            print(f"   ❌ Error en _manage_users: {e}")
            import traceback
            traceback.print_exc()
            self.logger.error(f"Error abriendo gestión de usuarios: {e}")
            messagebox.showerror("Error", f"Error abriendo la gestión de usuarios:\n{str(e)}")
    
    def _manage_roles(self):
        """Gestionar roles y permisos"""
        try:
            print("🔐 DEBUG: Abriendo gestión de roles desde main_controller")
            print(f"   - main_window tipo: {type(self.main_window)}")
            print(f"   - current_user: {self.current_user}")
            
            # Verificar permisos del usuario
            if not self._check_user_permission('roles_manage'):
                messagebox.showerror("Acceso Denegado", "No tienes permisos para acceder a la gestión de roles")
                return
            
            # Limpiar la ventana principal
            self._clear_main_content()
            print("   ✅ Ventana principal limpiada")
            
            # Crear contenido de gestión de roles en la ventana principal
            from views.role_management_view import RoleManagementView
            print("   🔄 Creando RoleManagementView...")
            
            # Pasar el current_user como diccionario con la estructura esperada
            user_data = {
                'id': self.current_user.get('id', 0),
                'username': self.current_user.get('username', ''),
                'full_name': self.current_user.get('full_name', ''),
                'email': self.current_user.get('email', ''),
                'role': self.current_user.get('user_type', 'admin'),  # Mapear user_type a role
                'permissions': self.current_user.get('permissions', {})
            }
            
            self.roles_view = RoleManagementView(self.main_window, user_data, embedded=True)
            print("   ✅ RoleManagementView creada exitosamente")
            
            # Registrar callbacks
            self.roles_view.bind_callback('back_to_dashboard', self._back_to_dashboard)
            print("   ✅ Callbacks registrados")
            
        except Exception as e:
            print(f"   ❌ Error en _manage_roles: {e}")
            import traceback
            traceback.print_exc()
            self.logger.error(f"Error abriendo gestión de roles: {e}")
            messagebox.showerror("Error", f"Error abriendo la gestión de roles:\n{str(e)}")
    
    def _manage_clients(self):
        """Gestionar clientes"""
        messagebox.showinfo("Gestión de Clientes", "Módulo de clientes en desarrollo")
    
    def _manage_purchases(self):
        """Gestionar compras"""
        messagebox.showinfo("Gestión de Compras", "Módulo de compras en desarrollo")
    
    def _show_support(self):
        """Mostrar soporte"""
        messagebox.showinfo("Soporte Técnico", "Chat de soporte en desarrollo\n\nPara asistencia inmediata:\n📧 soporte@pos.com\n📞 +1-800-123-4567")
    
    def _system_config(self):
        """Configuración del sistema"""
        try:
            print("🔧 DEBUG: Abriendo configuración desde main_controller")
            print(f"   - main_window tipo: {type(self.main_window)}")
            print(f"   - current_user: {self.current_user}")
            
            # Limpiar la ventana principal
            self._clear_main_content()
            print("   ✅ Ventana principal limpiada")
            
            # Crear contenido de configuración en la ventana principal
            from views.configuration_view import ConfigurationView
            print("   🔄 Creando ConfigurationView...")
            
            self.config_view = ConfigurationView(self.main_window, self.current_user, embedded=True)
            print("   ✅ ConfigurationView creada exitosamente")
            
            # Registrar callbacks
            self.config_view.bind_callback('back_to_dashboard', self._back_to_dashboard)
            self.config_view.bind_callback('configuration_saved', self._on_configuration_saved)
            print("   ✅ Callbacks registrados")
            
        except Exception as e:
            print(f"   ❌ Error en _system_config: {e}")
            import traceback
            traceback.print_exc()
            self.logger.error(f"Error abriendo configuración: {e}")
            messagebox.showerror("Error", f"Error abriendo la configuración:\n{str(e)}")
    
    def _on_configuration_saved(self, config_data: dict):
        """Manejar cuando se guarda la configuración"""
        try:
            print(f"🔧 Configuración guardada, actualizando login...")
            
            # Verificar si el nombre de la empresa cambió
            if 'company_name' in config_data:
                company_name = config_data['company_name']
                print(f"   📝 Nuevo nombre de empresa: '{company_name}'")
                
                # Actualizar el login view si existe
                if hasattr(self.auth_controller, 'login_view') and self.auth_controller.login_view:
                    self.auth_controller.login_view.refresh_company_info()
                    print(f"   ✅ Login actualizado con nuevo nombre de empresa")
                
        except Exception as e:
            print(f"   ❌ Error actualizando información de empresa en login: {e}")
            self.logger.error(f"Error actualizando login después de guardar configuración: {e}")
    
    def _show_manual(self):
        """Mostrar manual"""
        messagebox.showinfo("Manual", "Manual de usuario en desarrollo")
    
    def _show_about(self):
        """Mostrar información del sistema"""
        about_text = """Sistema POS v1.0
        
Desarrollado con Python y Tkinter
Arquitectura MVC

Características:
- Autenticación por roles
- Gestión de ventas
- Control de inventario
- Reportes avanzados
- Base de datos MySQL

© 2024 Sistema POS"""
        
        messagebox.showinfo("Acerca de Sistema POS", about_text)
    
    def _logout(self):
        """Cerrar sesión"""
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que deseas cerrar sesión?"):
            self.auth_controller.logout('manual')
    
    def _exit_application(self):
        """Salir de la aplicación"""
        self._on_main_window_close()
    
    def _on_main_window_close(self):
        """Manejar cierre de ventana principal"""
        if messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir del sistema?"):
            self.shutdown()
    
    def _show_error(self, title: str, message: str):
        """Mostrar mensaje de error"""
        try:
            messagebox.showerror(title, message)
        except:
            print(f"ERROR: {title} - {message}")
    
    def _get_user_role_display_name(self) -> str:
        """Obtener el nombre real del rol del usuario actual para mostrar en el menú"""
        try:
            if not self.current_user:
                return "Usuario"
            
            # Si ya tiene role_name en los datos del usuario, usarlo
            if 'role_name' in self.current_user:
                return self.current_user['role_name']
            
            # Si tiene role_id, buscar el nombre del rol
            role_id = self.current_user.get('role_id')
            if role_id:
                role_model = RoleModel()
                role_data = role_model.get_role_by_id(role_id)
                if role_data and 'name' in role_data:
                    return role_data['name']
            
            # Fallback: usar user_type pero capitalizado
            user_type = self.current_user.get('user_type', 'usuario')
            return user_type.title()
            
        except Exception as e:
            self.logger.warning(f"Error obteniendo nombre del rol: {e}")
            return "Usuario"
    
    def shutdown(self):
        """Cerrar aplicación completamente"""
        try:
            self.logger.info("Cerrando aplicación POS")
            self.is_running = False
            
            # Cerrar sesión si existe
            if self.auth_controller.is_authenticated():
                self.auth_controller.logout('cleanup')
            
            # Limpiar controladores
            self.auth_controller.cleanup()
            
            # Cerrar ventana principal
            if self.main_window:
                self.main_window.quit()
                self.main_window.destroy()
            
            self.logger.info("Aplicación cerrada correctamente")
            
        except Exception as e:
            self.logger.error(f"Error cerrando aplicación: {e}")
        finally:
            sys.exit(0)
