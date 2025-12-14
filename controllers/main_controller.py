"""
Controlador Principal del Sistema POS
Maneja la aplicación completa y coordina entre controladores
"""

import tkinter as tk
from tkinter import messagebox, font as tkfont
import logging
import sys
import os
from typing import Dict, Any, Optional
from controllers.auth_controller import AuthController
from views.login_view import LoginView
from config.settings import SystemSettings
from models.role_model import RoleModel
from services.permission_service import PermissionService
from utils.responsive_utils import ResponsiveManager

class MainController:
    """Controlador principal de la aplicación"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.settings = SystemSettings()
        
        # Estado de la aplicación
        self.is_running = False
        self.current_user = None
        
        # Controladores y servicios
        self.auth_controller = AuthController()
        self.permission_service = PermissionService()
        self.credit_note_controller = None
        self.sale_controller = None
        self.is_on_dashboard = False  # Estado para navegación con ESC
        
        # Ventana principal (se crea después del login)
        self.main_window = None
        
        # Gestor responsivo (se inicializa al crear ventana principal)
        self.responsive = None
        
        # Guardar geometría de ventana para mantenerla al cambiar de módulo
        self.saved_window_geometry = None

        # Ventanas flotantes auxiliares
        self.category_window = None
        self.stock_window = None
        
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
            
            # Inicializar gestor responsivo
            self.responsive = ResponsiveManager(self.main_window)
            
            # Aplicar configuración responsiva
            self.responsive.make_window_responsive(self.main_window)
            
            # Configurar protocolo de cierre
            self.main_window.protocol("WM_DELETE_WINDOW", self._on_main_window_close)
            
            # Configurar colores
            colors = self.settings.get_colors()
            self.main_window.configure(bg=colors['background'])
            
            # Configurar grid weights para responsividad
            self.responsive.apply_grid_weights(self.main_window, 'default')
            
            # Crear interfaz principal
            self._create_main_interface()

            # Atajos globales
            self._bind_global_shortcuts()
            
            # Mostrar ventana
            self.main_window.deiconify()
            self.main_window.lift()
            self.main_window.focus_force()

            # Maximizar al iniciar (se reintenta brevemente para asegurar)
            self._maximize_main_window()
            self.main_window.after(150, self._maximize_main_window)
            
            # Iniciar loop principal
            self.main_window.mainloop()
            
        except Exception as e:
            self.logger.error(f"Error creando ventana principal: {e}")
            self._show_error("Error", f"No se pudo crear la ventana principal: {str(e)}")
    
    def _create_main_interface(self):
        """Crear interfaz principal"""
        try:
            # Crear barra de navegación personalizada (GRANDE y visible)
            self._create_custom_navbar()
            
            # Crear barra de herramientas
            self._create_toolbar()
            
            # Crear área principal
            self._create_main_area()
            
            # Crear barra de estado
            self._create_status_bar()

            # Marcar que estamos en el dashboard principal
            self.is_on_dashboard = True
            
        except Exception as e:
            self.logger.error(f"Error creando interfaz principal: {e}")
            raise

    def _bind_global_shortcuts(self):
        """Configurar atajos globales de teclado (ESC)"""
        try:
            if not self.main_window:
                return

            # Limpiar binding previo para evitar duplicados
            self.main_window.unbind_all("<Escape>")
            self.main_window.bind_all("<Escape>", self._handle_escape)
        except Exception as exc:
            self.logger.warning(f"No se pudieron enlazar atajos globales: {exc}")

    def _maximize_main_window(self):
        """Intentar maximizar la ventana principal de forma segura"""
        if not self.main_window:
            return
        try:
            self.main_window.state('zoomed')
        except Exception:
            try:
                self.main_window.attributes('-zoomed', True)
            except Exception:
                pass

    def _handle_escape(self, event=None):
        """Manejar pulsación de ESC según contexto"""
        try:
            # Si hay ventanas flotantes prioritarias, cerrarlas primero
            if self.category_window and self.category_window.winfo_exists():
                self._close_category_window()
                return

            if self.stock_window and self.stock_window.winfo_exists():
                self._close_stock_window()
                return

            # Si estamos en un módulo, regresar al dashboard
            if not self.is_on_dashboard:
                self._back_to_dashboard()
                return

            # En el dashboard, ESC cierra sesión
            self._logout()

        except Exception as exc:
            self.logger.error(f"Error manejando ESC: {exc}")
    
    def _create_menu_bar(self):
        """Crear barra de menú"""
        # Configurar fuente predeterminada del sistema para menús (Windows)
        try:
            default_font = tkfont.nametofont("TkDefaultFont")
            default_font.configure(size=13, family="Segoe UI", weight="bold")
            
            menu_font = tkfont.nametofont("TkMenuFont")
            menu_font.configure(size=13, family="Segoe UI", weight="bold")
        except Exception as e:
            self.logger.warning(f"No se pudo configurar fuente del sistema: {e}")
        
        # Configurar fuente predeterminada para todos los menús
        self.main_window.option_add('*Menu.font', ('Segoe UI', 13, 'bold'))
        self.main_window.option_add('*Menu*font', ('Segoe UI', 13, 'bold'))
        
        menubar = tk.Menu(self.main_window)
        self.main_window.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu, font=('Segoe UI', 13, 'bold'))
        if self._check_user_permission('sales.create'):
            file_menu.add_command(label="Nueva Venta", command=self._new_sale)
        file_menu.add_separator()
        file_menu.add_command(label="Cerrar Sesión", command=self._logout)
        file_menu.add_command(label="Salir", command=self._exit_application)
        
        # Menú Ventas
        sales_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ventas", menu=sales_menu, font=('Segoe UI', 13, 'bold'))
        if self._check_user_permission('sales.create'):
            sales_menu.add_command(label="Nueva Venta", command=self._new_sale)
        if self._check_user_permission('sales.view'):
            sales_menu.add_command(label="Historial de Ventas", command=self._sales_history)
        if sales_menu.index('end') is None:
            sales_menu.add_command(label="Sin accesos disponibles", state='disabled')
        
        # Menú Inventario (solo si tiene permisos)
        if self.auth_controller.has_permission('inventory.view'):
            inventory_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Inventario", menu=inventory_menu, font=('Segoe UI', 13, 'bold'))
            inventory_menu.add_command(label="Ver Productos", command=self._view_products)
            inventory_menu.add_command(label="Gestionar Categorías", command=self._view_categories)
            
            if self.auth_controller.has_permission('inventory.edit'):
                inventory_menu.add_command(label="Agregar Producto", command=self._add_product)
                inventory_menu.add_command(label="Gestionar Inventario", command=self._manage_inventory)
        
        # Menú Reportes (solo supervisores y admins)
        if self.auth_controller.has_permission('reports.basic'):
            reports_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Reportes", menu=reports_menu, font=('Segoe UI', 13, 'bold'))
            reports_menu.add_command(label="Ventas del Día", command=self._daily_sales_report)
            
            if self.auth_controller.has_permission('reports.full'):
                reports_menu.add_command(label="Reporte Completo", command=self._full_report)
        
        # Menú Administración (solo admins)
        if self.auth_controller.has_permission('users.view'):
            admin_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Administración", menu=admin_menu, font=('Segoe UI', 13, 'bold'))
            admin_menu.add_command(label="Gestionar Usuarios", command=self._manage_users)
            admin_menu.add_command(label="Gestionar Roles", command=self._manage_roles)
            admin_menu.add_separator()
            admin_menu.add_command(label="Configuración", command=self._system_config)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu, font=('Segoe UI', 13, 'bold'))
        help_menu.add_command(label="Manual de Usuario", command=self._show_manual)
        help_menu.add_command(label="Acerca de", command=self._show_about)
    
    def _create_custom_navbar(self):
        """Crear barra de navegación personalizada con botones grandes"""
        navbar_frame = tk.Frame(self.main_window, bg='#2c3e50', height=50)
        navbar_frame.pack(fill='x', side='top')
        navbar_frame.pack_propagate(False)
        
        # Estilo de botones
        btn_style = {
            'font': ('Segoe UI', 12, 'bold'),
            'bg': '#2c3e50',
            'fg': 'white',
            'activebackground': '#34495e',
            'activeforeground': 'white',
            'relief': 'flat',
            'bd': 0,
            'padx': 20,
            'pady': 10,
            'cursor': 'hand2'
        }
        
        # Contenedor de botones
        buttons_container = tk.Frame(navbar_frame, bg='#2c3e50')
        buttons_container.pack(side='left', padx=10, pady=5)
        
        # Botón Archivo
        file_btn = tk.Menubutton(buttons_container, text="📁 Archivo", **btn_style)
        file_btn.pack(side='left', padx=2)
        file_menu = tk.Menu(file_btn, tearoff=0, font=('Segoe UI', 11))
        file_btn.config(menu=file_menu)
        if self._check_user_permission('sales.create'):
            file_menu.add_command(label="Nueva Venta", command=self._new_sale)
            file_menu.add_separator()
        file_menu.add_command(label="Cerrar Sesión", command=self._logout)
        file_menu.add_command(label="Salir", command=self._exit_application)
        
        # Botón Ventas
        sales_btn = tk.Menubutton(buttons_container, text="💰 Ventas", **btn_style)
        sales_btn.pack(side='left', padx=2)
        sales_menu = tk.Menu(sales_btn, tearoff=0, font=('Segoe UI', 11))
        sales_btn.config(menu=sales_menu)
        can_create_sales = self._check_user_permission('sales.create')
        can_view_sales = self._check_user_permission('sales.view')
        if can_create_sales:
            sales_menu.add_command(label="Nueva Venta", command=self._new_sale)
        if can_view_sales:
            sales_menu.add_command(label="Historial de Ventas", command=self._sales_history)
            sales_menu.add_command(label="Notas de Crédito", command=self._credit_notes_module)
        if sales_menu.index('end') is None:
            sales_menu.add_command(label="Sin accesos disponibles", state='disabled')
        
        # Botón Inventario
        if self.auth_controller.has_permission('inventory.view'):
            inv_btn = tk.Menubutton(buttons_container, text="📦 Inventario", **btn_style)
            inv_btn.pack(side='left', padx=2)
            inv_menu = tk.Menu(inv_btn, tearoff=0, font=('Segoe UI', 11))
            inv_btn.config(menu=inv_menu)
            inv_menu.add_command(label="Ver Productos", command=self._view_products)
            inv_menu.add_command(label="Gestionar Categorías", command=self._view_categories)
            inv_menu.add_command(label="Control de Stock", command=self._view_stock_control)
            
            if self.auth_controller.has_permission('inventory.edit'):
                inv_menu.add_separator()
                inv_menu.add_command(label="Agregar Producto", command=self._add_product)
                inv_menu.add_command(label="Gestionar Inventario", command=self._manage_inventory)
        
        # Botón Reportes
        if self.auth_controller.has_permission('reports.basic'):
            rep_btn = tk.Menubutton(buttons_container, text="📊 Reportes", **btn_style)
            rep_btn.pack(side='left', padx=2)
            rep_menu = tk.Menu(rep_btn, tearoff=0, font=('Segoe UI', 11))
            rep_btn.config(menu=rep_menu)
            rep_menu.add_command(label="Ventas del Día", command=self._daily_sales_report)
            
            if self.auth_controller.has_permission('reports.full'):
                rep_menu.add_command(label="Reporte Completo", command=self._full_report)
        
        # Botón Administración
        if self.permission_service.check_permission(self.current_user, 'users.view') or \
           self.permission_service.check_permission(self.current_user, 'roles.view') or \
           self.permission_service.check_permission(self.current_user, 'system.config'):
            admin_btn = tk.Menubutton(buttons_container, text="⚙️ Administración", **btn_style)
            admin_btn.pack(side='left', padx=2)
            admin_menu = tk.Menu(admin_btn, tearoff=0, font=('Segoe UI', 11))
            admin_btn.config(menu=admin_menu)
            
            # Gestionar Usuarios - solo si tiene permiso users.view
            if self.permission_service.check_permission(self.current_user, 'users.view'):
                admin_menu.add_command(label="Gestionar Usuarios", command=self._manage_users)
            
            # Gestionar Roles - solo si tiene permiso roles.view
            if self.permission_service.check_permission(self.current_user, 'roles.view'):
                admin_menu.add_command(label="Gestionar Roles", command=self._manage_roles)
            
            # Configuración del sistema - solo si tiene permiso system.config
            if self.permission_service.check_permission(self.current_user, 'system.config'):
                if admin_menu.index('end') is not None:  # Si hay items previos, agregar separador
                    admin_menu.add_separator()
                admin_menu.add_command(label="Configuración", command=self._system_config)
        
        # Botón Ayuda
        help_btn = tk.Menubutton(buttons_container, text="❓ Ayuda", **btn_style)
        help_btn.pack(side='left', padx=2)
        help_menu = tk.Menu(help_btn, tearoff=0, font=('Segoe UI', 11))
        help_btn.config(menu=help_menu)
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
        
        can_create_sales = self._check_user_permission('sales.create')
        if can_create_sales:
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
        
        # Botón Configuración de Boletas
        config_btn = tk.Button(
            quick_buttons_frame,
            text="🎫 Boletas",
            command=self._config_tickets,
            bg='#9b59b6',
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            padx=15,
            pady=5
        )
        config_btn.pack(side='left', padx=5)
        
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
        # Decidir qué tipo de dashboard mostrar
        dashboard_type = self._get_dashboard_type()
        
        if dashboard_type == 'modules':
            self._create_modules_dashboard(self.main_window)
        elif dashboard_type == 'stats':
            self._create_stats_dashboard(self.main_window)
        else:
            # Dashboard híbrido (por defecto)
            self._create_hybrid_dashboard(self.main_window)
    
    def _get_dashboard_type(self):
        """Obtener tipo de dashboard según preferencias/permisos"""
        # Temporalmente usar dashboard de módulos para probar permisos
        # TODO: Permitir al usuario elegir su dashboard preferido
        return 'modules'
    
    def _create_modules_dashboard(self, parent):
        """Crear dashboard tipo módulos/tarjetas"""
        from views.dashboard_view import DashboardView
        
        self.dashboard_view = DashboardView(self.main_window, self.current_user)
        
        # Registrar callbacks para los módulos realmente disponibles
        self.dashboard_view.bind_module_callback('products', lambda: self._view_products())
        self.dashboard_view.bind_module_callback('categories', lambda: self._view_categories())
        self.dashboard_view.bind_module_callback('stock_control', lambda: self._view_stock_control())
        self.dashboard_view.bind_module_callback('sales_register', lambda: self._new_sale())
        self.dashboard_view.bind_module_callback('sales_history', lambda: self._sales_history())
        self.dashboard_view.bind_module_callback('credit_notes', lambda: self._credit_notes_module())
        self.dashboard_view.bind_module_callback('user_management', lambda: self._manage_users())
        self.dashboard_view.bind_module_callback('role_management', lambda: self._manage_roles())
        self.dashboard_view.bind_module_callback('income_report', lambda: self._daily_sales_report())
        self.dashboard_view.bind_module_callback('reports', lambda: self._full_report())
        self.dashboard_view.bind_module_callback('business', lambda: self._system_config())
        self.dashboard_view.bind_module_callback('ticket_config', lambda: self._config_tickets())
        self.dashboard_view.bind_module_callback('support', lambda: self._show_support())
        self.dashboard_view.bind_module_callback('help', lambda: self._show_manual())
    
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

        if self._check_user_permission('sales.view'):
            modules.append({
                'title': 'Notas Crédito',
                'icon': '🧾',
                'color': '#1abc9c',
                'command': self._credit_notes_module,
                'permission': 'sales.view'
            })
        
        # Módulos según permisos
        if self.auth_controller.has_permission('inventory.view'):
            modules.append({
                'title': 'Productos',
                'icon': '📦',
                'color': '#e74c3c',
                'command': self._view_products,
                'permission': 'inventory.view'
            })

        if self.auth_controller.has_permission('reports.basic'):
            modules.append({
                'title': 'Reportes',
                'icon': '📊',
                'color': '#9b59b6',
                'command': self._daily_sales_report,
                'permission': 'reports.basic'
            })
        
        if self.auth_controller.has_permission('users.view'):
            modules.append({
                'title': 'Usuarios',
                'icon': '👥',
                'color': '#f39c12',
                'command': self._manage_users,
                'permission': 'users.view'
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
    
    def _save_window_geometry(self):
        """Guardar geometría actual de la ventana"""
        try:
            if self.main_window:
                self.saved_window_geometry = self.main_window.geometry()
                # También guardar estado de maximizado
                self.saved_window_state = self.main_window.state()
        except Exception as e:
            self.logger.error(f"Error guardando geometría: {e}")
    
    def _restore_window_geometry(self):
        """Restaurar geometría guardada de la ventana"""
        try:
            if self.main_window and self.saved_window_geometry:
                self.main_window.geometry(self.saved_window_geometry)
                # Restaurar estado de maximizado si corresponde
                if hasattr(self, 'saved_window_state') and self.saved_window_state == 'zoomed':
                    self.main_window.state('zoomed')
        except Exception as e:
            self.logger.error(f"Error restaurando geometría: {e}")
    
    def _center_window(self, window: tk.Toplevel, width: Optional[int] = None, height: Optional[int] = None):
        """Centrar ventana secundaria en la pantalla"""
        try:
            window.update_idletasks()
            win_width = width or window.winfo_width()
            win_height = height or window.winfo_height()

            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()

            x = max(0, (screen_width - win_width) // 2)
            y = max(0, (screen_height - win_height) // 2)

            window.geometry(f"{win_width}x{win_height}+{x}+{y}")
        except Exception as exc:
            self.logger.warning(f"No se pudo centrar la ventana: {exc}")

    def _clear_main_content(self):
        """Limpiar contenido principal de la ventana"""
        # PRIMERO: Guardar geometría actual ANTES de limpiar
        self._save_window_geometry()

        # Al limpiar contenido asumimos que salimos del dashboard
        self.is_on_dashboard = False
        
        # Destruir todos los widgets hijos excepto la barra de menú
        for widget in self.main_window.winfo_children():
            if not isinstance(widget, tk.Menu):
                widget.destroy()
    
    def _check_user_permission(self, permission):
        """Verificar permisos del usuario"""
        try:
            if not self.current_user:
                return False
            
            # Obtener permisos del usuario
            user_permissions = self.current_user.get('permissions')
            
            # Si no hay permisos, denegar
            if not user_permissions:
                print(f"   ⚠️ Usuario sin permisos asignados")
                return False
            
            # Si es una lista (sistema nuevo de roles)
            if isinstance(user_permissions, list):
                # Verificar si tiene el permiso o si tiene '*' (todos)
                has_perm = permission in user_permissions or '*' in user_permissions
                print(f"   🔍 Verificando permiso '{permission}': {has_perm}")
                return has_perm
            
            # Si es un dict (sistema antiguo de permisos individuales)
            elif isinstance(user_permissions, dict):
                # Verificar permisos especiales de super admin
                if user_permissions.get('all_modules', False) or user_permissions.get('super_admin', False):
                    print(f"   🔍 Verificando permiso '{permission}' (dict): True [SUPER ADMIN]")
                    return True
                
                # Verificar permiso específico
                has_perm = user_permissions.get(permission, False)
                print(f"   🔍 Verificando permiso '{permission}' (dict): {has_perm}")
                return has_perm
            
            # Fallback: usar servicio de permisos centralizado
            return self.auth_controller.has_permission(permission)
            
        except Exception as e:
            print(f"   ❌ Error verificando permisos: {e}")
            import traceback
            traceback.print_exc()
            self.logger.error(f"Error verificando permisos: {e}")
            return False
    
    def reload_current_user_permissions(self):
        """Recargar permisos del usuario actual desde la base de datos"""
        try:
            if not self.current_user:
                return False
            
            user_id = self.current_user.get('id')
            if not user_id:
                return False
            
            print(f"\n🔄 Recargando permisos para usuario ID={user_id}...")
            
            # Importar UserModel aquí para evitar circular imports
            from models.user_model import UserModel
            user_model = UserModel()
            
            # Obtener datos frescos del usuario desde la BD
            fresh_user = user_model.get_user_by_id(user_id)
            if not fresh_user:
                print(f"❌ Usuario no encontrado")
                return False
            
            # Preparar datos de usuario con permisos actualizados
            updated_user_data = user_model.prepare_user_data(fresh_user)
            
            # Actualizar current_user con los nuevos permisos
            old_permissions = self.current_user.get('permissions')
            self.current_user['permissions'] = updated_user_data.get('permissions')
            
            print(f"✅ Permisos actualizados!")
            print(f"   Permisos anteriores: {old_permissions}")
            print(f"   Permisos nuevos: {self.current_user.get('permissions')}")
            
            # Limpiar caché de permisos
            from services.permission_service import PermissionService
            permission_service = PermissionService()
            permission_service.clear_user_cache(user_id)
            print(f"🧹 Caché de permisos limpiado")
            
            return True
            
        except Exception as e:
            print(f"❌ Error recargando permisos: {e}")
            import traceback
            traceback.print_exc()
            self.logger.error(f"Error recargando permisos: {e}")
            return False
    
    def _back_to_dashboard(self):
        """Volver al dashboard principal"""
        try:
            # Limpiar contenido actual (guarda geometría automáticamente)
            self._clear_main_content()
            
            # Recrear interfaz principal
            self._create_main_interface()

            # Reaplicar atajos globales
            self._bind_global_shortcuts()
            
            # IMPORTANTE: Restaurar geometría después de recrear

            # Maximizar al iniciar (solo si el SO/gestor lo permite)
            try:
                self.main_window.state('zoomed')
            except Exception:
                pass
            self._restore_window_geometry()
            
        except Exception as e:
            self.logger.error(f"Error volviendo al dashboard: {e}")
            messagebox.showerror("Error", f"Error volviendo al dashboard:\n{str(e)}")
    
    def _show_dashboard(self):
        """Alias para volver al dashboard (usado por callbacks)"""
        self._back_to_dashboard()
    
    def _show_inventory_management(self):
        """Ir a Gestión de Inventario (Control de Stock)"""
        self._view_stock_control()
    
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

        if self.auth_controller.has_permission('sales.view'):
            buttons.append({
                'text': '🧾\nNotas Crédito',
                'command': self._credit_notes_module,
                'color': '#1abc9c'
            })
        
        # Botón Productos (si tiene permisos)
        if self.auth_controller.has_permission('inventory.view'):
            buttons.append({
                'text': '📦\nProductos',
                'command': self._view_products,
                'color': self.settings.get_colors()['success']
            })
        
        # Botón Configuración Boletas (disponible para todos)
        buttons.append({
            'text': '🎫\nBoletas',
            'command': self._config_tickets,
            'color': '#9b59b6'  # Color morado
        })
        
        # Botón Reportes (si tiene permisos)
        if self.auth_controller.has_permission('reports.basic'):
            buttons.append({
                'text': '📊\nReportes',
                'command': self._daily_sales_report,
                'color': self.settings.get_colors()['warning']
            })
        
        # Botón Administración (solo admins)
        if self.auth_controller.has_permission('users.view'):
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
        """Iniciar nueva venta - Abrir POS"""
        try:
            if not self._check_user_permission('sales.create'):
                messagebox.showerror("Acceso Denegado", "No tienes permisos para registrar nuevas ventas")
                return

            print("🛒 DEBUG: Abriendo Punto de Venta desde main_controller")
            print(f"   - main_window tipo: {type(self.main_window)}")
            print(f"   - current_user: {self.current_user}")
            
            # Limpiar la ventana principal (guarda geometría automáticamente)
            self._clear_main_content()
            print("   ✅ Ventana principal limpiada")
            
            # Crear vista POS en la ventana principal
            from views.pos_view import POSView
            from controllers.sale_controller import SaleController
            print("   🔄 Creando POSView...")
            
            # Crear controlador de ventas
            self.sale_controller = SaleController()
            
            # Crear vista POS
            self.pos_view = POSView(
                parent=self.main_window,
                controller=self.sale_controller,
                user_data=self.current_user,
                on_back=self._show_dashboard
            )
            print("   ✅ POSView creada exitosamente")
            
            # Cargar vista
            self.pos_view.show()
            print("   📺 Vista POS mostrada")
            
            # IMPORTANTE: Restaurar geometría después de cargar vista
            self._restore_window_geometry()
            
        except Exception as e:
            self.logger.error(f"Error al abrir módulo de ventas: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"No se pudo abrir el módulo de ventas:\n{str(e)}")
    
    def _sales_history(self):
        """Mostrar historial de ventas"""
        try:
            if not self._check_user_permission('sales.view'):
                messagebox.showerror("Acceso Denegado", "No tienes permisos para ver el historial de ventas")
                return

            print("💰 DEBUG: Abriendo historial de ventas desde main_controller")
            self._clear_main_content()

            from views.sales_history_view import SalesHistoryView
            from controllers.sale_controller import SaleController

            if not hasattr(self, 'sale_controller') or self.sale_controller is None:
                self.sale_controller = SaleController()

            self.sales_history_view = SalesHistoryView(self.main_window, self.current_user)

            # Navegación principal
            self.sales_history_view.bind_callback('back_to_dashboard', self._show_dashboard)
            self.sales_history_view.bind_callback('new_sale', self._new_sale)
            self.sales_history_view.bind_callback('sales_history', self._sales_history)
            self.sales_history_view.bind_callback('view_products', self._view_products)
            self.sales_history_view.bind_callback('view_categories', self._view_categories)
            self.sales_history_view.bind_callback('stock_control', self._show_inventory_management)
            self.sales_history_view.bind_callback('daily_report', self._daily_sales_report)
            self.sales_history_view.bind_callback('full_report', self._full_report)
            self.sales_history_view.bind_callback('manage_users', self._manage_users)
            self.sales_history_view.bind_callback('manage_roles', self._manage_roles)
            self.sales_history_view.bind_callback('system_config', self._system_config)
            self.sales_history_view.bind_callback('show_manual', self._show_manual)
            self.sales_history_view.bind_callback('show_about', self._show_about)

            # Eventos específicos del módulo
            self.sales_history_view.bind_callback('refresh', lambda: self._load_sales_history(self.sales_filters))
            self.sales_history_view.bind_callback('apply_filters', self._apply_sales_filters)
            self.sales_history_view.bind_callback('reset_filters', self._reset_sales_filters)
            self.sales_history_view.bind_callback('get_sale_detail', self._load_sale_detail)
            self.sales_history_view.bind_callback('delete_sale', self._delete_sale_from_history)

            # Estado inicial de filtros y carga
            self.sales_filters = {'status': 'completed'}
            self._load_sales_history(self.sales_filters)

            self._restore_window_geometry()

        except Exception as e:
            self.logger.error(f"Error al abrir historial de ventas: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"No se pudo abrir el historial de ventas:\n{str(e)}")

    def _load_sales_history(self, filters: dict | None = None):
        """Cargar ventas hacia la vista de historial"""
        try:
            if not hasattr(self, 'sale_controller') or self.sale_controller is None:
                from controllers.sale_controller import SaleController
                self.sale_controller = SaleController()

            filters = filters or {}
            result = self.sale_controller.get_sales_list(filters)

            if result.get('success'):
                sales = result.get('sales', [])
                if hasattr(self, 'sales_history_view') and self.sales_history_view:
                    self.sales_history_view.load_sales(sales)
            else:
                message = result.get('message', 'No se pudieron obtener las ventas')
                messagebox.showerror("Historial de ventas", message)

        except Exception as e:
            self.logger.error(f"Error cargando historial de ventas: {e}")
            messagebox.showerror("Error", f"Error cargando historial de ventas: {str(e)}")

    def _apply_sales_filters(self, filters: dict):
        """Aplicar filtros recibidos desde la vista"""
        self.sales_filters = filters.copy() if filters else {}
        self._load_sales_history(self.sales_filters)

    def _reset_sales_filters(self):
        """Restablecer filtros a los valores por defecto"""
        self.sales_filters = {'status': 'completed'}
        self._load_sales_history(self.sales_filters)

    def _load_sale_detail(self, sale_id: int):
        """Cargar detalle específico de una venta"""
        if sale_id is None:
            return

        try:
            result = self.sale_controller.get_sale_detail(sale_id)
            if result.get('success'):
                sale = result.get('sale')
                if sale and hasattr(self, 'sales_history_view'):
                    self.sales_history_view.show_sale_detail(sale)
            else:
                if hasattr(self, 'sales_history_view'):
                    self.sales_history_view.show_sale_detail(None)
                messagebox.showerror("Detalle de venta", result.get('message', 'No se pudo obtener el detalle'))

        except Exception as e:
            self.logger.error(f"Error obteniendo detalle de venta {sale_id}: {e}")
            messagebox.showerror("Error", f"Error al cargar el detalle de la venta: {str(e)}")

    def _delete_sale_from_history(self, sale_id: int, reason: str | None = None):
        """Eliminar (cancelar) una venta desde el historial"""
        if sale_id is None:
            return

        if not self._check_user_permission('sales.delete'):
            messagebox.showerror("Acceso Denegado", "No tienes permisos para eliminar ventas")
            return

        try:
            user_id = self.current_user.get('id') if self.current_user else None
            reason_text = reason or 'Eliminada desde historial de ventas'
            result = self.sale_controller.cancel_sale(sale_id, user_id, reason_text)

            if result.get('success'):
                if hasattr(self, 'sales_history_view'):
                    message = result.get('message', 'Venta eliminada exitosamente')
                    restored_items = result.get('restored_items') or []
                    if restored_items:
                        total_items = sum(item.get('quantity', 0) for item in restored_items)
                        message += f"\nStock restaurado para {len(restored_items)} producto(s), total devuelto: {total_items:.2f} unidades."
                    self.sales_history_view.show_success("Venta eliminada", message)
                    self.sales_history_view.clear_sale_detail()
                self._load_sales_history(self.sales_filters)
            else:
                if hasattr(self, 'sales_history_view'):
                    self.sales_history_view.show_error("Error", result.get('message', 'No se pudo eliminar la venta'))

        except Exception as e:
            self.logger.error(f"Error eliminando venta {sale_id}: {e}")
            messagebox.showerror("Error", f"No se pudo eliminar la venta: {str(e)}")

    # ==========================================
    # Notas de crédito
    # ==========================================

    def _credit_notes_module(self):
        """Abrir módulo de notas de crédito"""
        try:
            if not self._check_user_permission('sales.view'):
                messagebox.showerror("Acceso Denegado", "No tienes permisos para acceder a notas de crédito")
                return

            self._clear_main_content()

            from views.credit_notes_view import CreditNotesView
            from controllers.credit_note_controller import CreditNoteController

            if not self.credit_note_controller:
                self.credit_note_controller = CreditNoteController()

            self.credit_notes_view = CreditNotesView(self.main_window, self.current_user)
            self.credit_notes_view.bind_callback('back_to_dashboard', self._show_dashboard)
            self.credit_notes_view.bind_callback('refresh', self._load_credit_notes)
            self.credit_notes_view.bind_callback('generate_credit_note', self._generate_credit_note)
            self.credit_notes_view.bind_callback('show_credit_note_report', self._show_credit_note_report)
            self.credit_notes_view.bind_callback('fetch_credit_note_sales', self._fetch_sales_for_credit_notes)

            self._load_credit_notes()
            self._restore_window_geometry()

        except Exception as e:
            self.logger.error(f"Error al abrir notas de crédito: {e}")
            messagebox.showerror("Error", f"No se pudo abrir el módulo de notas de crédito:\n{str(e)}")

    def _ensure_credit_note_controller(self):
        if not self.credit_note_controller:
            from controllers.credit_note_controller import CreditNoteController
            self.credit_note_controller = CreditNoteController()

    def _ensure_sale_controller(self):
        if not self.sale_controller:
            from controllers.sale_controller import SaleController
            self.sale_controller = SaleController()

    def _load_credit_notes(self):
        try:
            self._ensure_credit_note_controller()
            result = self.credit_note_controller.list_credit_notes()
            if result.get('success'):
                if hasattr(self, 'credit_notes_view') and self.credit_notes_view:
                    self.credit_notes_view.load_notes(result.get('notes', []))
            else:
                messagebox.showerror("Notas de crédito", result.get('message', 'No se pudo cargar el listado'))
        except Exception as e:
            self.logger.error(f"Error cargando notas de crédito: {e}")
            messagebox.showerror("Notas de crédito", f"Error cargando notas de crédito: {str(e)}")

    def _fetch_sales_for_credit_notes(self, search_text: str | None = None):
        try:
            print(f"🔍 [DEBUG MAIN] _fetch_sales_for_credit_notes - Recibido: '{search_text}'")
            self._ensure_sale_controller()
            sale_code = (search_text or '').strip()
            print(f"🔍 [DEBUG MAIN] Llamando a get_recent_sales_for_credit_notes con: '{sale_code}'")
            return self.sale_controller.get_recent_sales_for_credit_notes(sale_code or None)
        except Exception as e:
            self.logger.error(f"Error obteniendo ventas para notas de crédito: {e}")
            return {'success': False, 'message': f'No se pudieron obtener las ventas: {str(e)}'}

    def _generate_credit_note(self, sale_id: int, reason: str = ""):
        try:
            self._ensure_credit_note_controller()
            user_id = self.current_user.get('id') if self.current_user else None
            if not user_id:
                messagebox.showerror("Sesión", "No se pudo identificar al usuario actual")
                return

            result = self.credit_note_controller.create_credit_note(sale_id, user_id, reason)
            if result.get('success'):
                if hasattr(self, 'credit_notes_view'):
                    self.credit_notes_view.show_success("Nota creada", result.get('message', 'Nota de crédito generada.'))
                self._load_credit_notes()
            else:
                messagebox.showerror("Notas de crédito", result.get('message', 'No se pudo generar la nota.'))
        except Exception as e:
            self.logger.error(f"Error generando nota de crédito: {e}")
            messagebox.showerror("Notas de crédito", f"No se pudo generar la nota: {str(e)}")

    def _show_credit_note_report(self):
        try:
            self._ensure_credit_note_controller()
            result = self.credit_note_controller.report()
            if result.get('success'):
                data = result.get('data', {})
                summary = data.get('summary', {})
                if hasattr(self, 'credit_notes_view'):
                    self.credit_notes_view.show_report_summary(summary)
                else:
                    messagebox.showinfo(
                        "Reporte de notas",
                        f"Total de notas: {summary.get('total_notes', 0)}\nMonto total acreditado: S/ {summary.get('total_amount', 0.0):.2f}"
                    )
            else:
                messagebox.showerror("Notas de crédito", result.get('message', 'No se pudo obtener el reporte.'))
        except Exception as e:
            self.logger.error(f"Error obteniendo reporte de notas: {e}")
            messagebox.showerror("Notas de crédito", f"No se pudo obtener el reporte: {str(e)}")
    
    def _view_products(self):
        """Ver productos - Abrir módulo de inventario"""
        try:
            print("📦 DEBUG: Abriendo gestión de productos desde main_controller")
            print(f"   - main_window tipo: {type(self.main_window)}")
            print(f"   - current_user: {self.current_user}")
            
            # Verificar permisos del usuario
            if not self._check_user_permission('inventory.view'):
                messagebox.showerror("Acceso Denegado", "No tienes permisos para acceder al módulo de inventario")
                return
            
            # Limpiar la ventana principal (guarda geometría automáticamente)
            self._clear_main_content()
            print("   ✅ Ventana principal limpiada")
            
            # Crear contenido de gestión de productos en la ventana principal
            from views.product_management_view import ProductManagementView
            from views.product_form_dialog import ProductFormDialog
            from controllers.product_controller import ProductController
            print("   🔄 Creando ProductManagementView...")
            
            # Crear controlador de productos
            self.product_controller = ProductController()
            
            # Crear vista
            self.product_view = ProductManagementView(self.main_window, self.current_user)
            print("   ✅ ProductManagementView creada exitosamente")
            
            # Registrar callbacks - NAVBAR COMPLETO
            self.product_view.bind_callback('refresh', self._load_products)
            self.product_view.bind_callback('search', self._search_products)
            self.product_view.bind_callback('create', self._create_product)
            self.product_view.bind_callback('edit', self._edit_product)
            self.product_view.bind_callback('delete', self._delete_product)
            self.product_view.bind_callback('export', self._export_products)
            # Navegación principal
            self.product_view.bind_callback('back_to_dashboard', self._show_dashboard)
            self.product_view.bind_callback('new_sale', self._new_sale)
            self.product_view.bind_callback('sales_history', self._sales_history)
            self.product_view.bind_callback('view_products', self._view_products)
            self.product_view.bind_callback('view_categories', self._view_categories)
            self.product_view.bind_callback('go_to_inventory', self._show_inventory_management)
            self.product_view.bind_callback('open_categories_window', self._open_categories_window)
            self.product_view.bind_callback('open_stock_window', self._open_stock_window)
            self.product_view.bind_callback('daily_report', self._daily_sales_report)
            self.product_view.bind_callback('full_report', self._full_report)
            self.product_view.bind_callback('manage_users', self._manage_users)
            self.product_view.bind_callback('manage_roles', self._manage_roles)
            self.product_view.bind_callback('system_config', self._system_config)
            self.product_view.bind_callback('show_manual', self._show_manual)
            self.product_view.bind_callback('show_about', self._show_about)
            print("   ✅ Callbacks registrados")
            
            # Cargar datos iniciales
            self._load_products()
            self._load_product_categories()
            self._load_product_units()
            
            # IMPORTANTE: Restaurar geometría después de cargar todo
            self._restore_window_geometry()
            
        except Exception as e:
            import traceback
            print(f"   ❌ ERROR: {e}")
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al abrir gestión de productos: {str(e)}")
    
    def _load_products(self):
        """Cargar lista de productos"""
        try:
            products = self.product_controller.get_all_products(self.current_user, include_inactive=False)
            self.product_view.load_products(products)
        except Exception as e:
            self.logger.error(f"Error cargando productos: {e}")
            messagebox.showerror("Error", f"Error al cargar productos: {str(e)}")
    
    def _load_product_categories(self):
        """Cargar categorías"""
        try:
            categories = self.product_controller.get_categories(self.current_user)
            self.product_view.load_categories(categories)
        except Exception as e:
            self.logger.error(f"Error cargando categorías: {e}")
    
    def _load_product_units(self):
        """Cargar unidades de medida"""
        try:
            units = self.product_controller.get_units(self.current_user)
            self.product_view.load_units(units)
        except Exception as e:
            self.logger.error(f"Error cargando unidades: {e}")
    
    def _search_products(self, search_term: str):
        """Buscar productos"""
        try:
            if search_term.strip():
                products = self.product_controller.search_products(search_term, self.current_user)
            else:
                products = self.product_controller.get_all_products(self.current_user)
            
            self.product_view.load_products(products)
        except Exception as e:
            self.logger.error(f"Error buscando productos: {e}")
            messagebox.showerror("Error", f"Error en la búsqueda: {str(e)}")
    
    def _create_product(self):
        """Crear nuevo producto"""
        try:
            from views.product_form_dialog import ProductFormDialog
            
            # Abrir diálogo
            next_sku = self.product_controller.generate_next_sku()
            dialog = ProductFormDialog(
                self.main_window,
                product=None,
                categories=self.product_view.categories,
                units=self.product_view.units,
                next_sku=next_sku
            )
            
            product_data = dialog.show()
            
            if product_data:
                try:
                    print("🔍 [DEBUG MAIN] Datos recibidos de diálogo de producto:")
                    for k, v in product_data.items():
                        print(f"   {k}: {v}")
                except Exception as _:
                    pass
                # Crear producto
                success, message, product_id = self.product_controller.create_product(
                    product_data, self.current_user
                )
                
                if success:
                    messagebox.showinfo("Éxito", message)
                    self._load_products()
                else:
                    messagebox.showerror("Error", message)
        
        except Exception as e:
            self.logger.error(f"Error creando producto: {e}")
            messagebox.showerror("Error", f"Error al crear producto: {str(e)}")
    
    def _edit_product(self, product: Dict[str, Any]):
        """Editar producto"""
        try:
            from views.product_form_dialog import ProductFormDialog
            
            # Abrir diálogo con datos del producto
            dialog = ProductFormDialog(
                self.main_window,
                product=product,
                categories=self.product_view.categories,
                units=self.product_view.units
            )
            
            product_data = dialog.show()
            
            if product_data:
                # Actualizar producto
                success, message = self.product_controller.update_product(
                    product['id'], product_data, self.current_user
                )
                
                if success:
                    messagebox.showinfo("Éxito", message)
                    self._load_products()
                else:
                    messagebox.showerror("Error", message)
        
        except Exception as e:
            self.logger.error(f"Error editando producto: {e}")
            messagebox.showerror("Error", f"Error al editar producto: {str(e)}")
    
    def _delete_product(self, product_id: int):
        """Eliminar producto"""
        try:
            success, message = self.product_controller.delete_product(product_id, self.current_user)
            
            if success:
                messagebox.showinfo("Éxito", message)
                self._load_products()
            else:
                messagebox.showerror("Error", message)
        
        except Exception as e:
            self.logger.error(f"Error eliminando producto: {e}")
            messagebox.showerror("Error", f"Error al eliminar producto: {str(e)}")
    
    def _update_product_stock(self, product: Dict[str, Any]):
        """Actualizar stock de producto"""
        try:
            # Crear diálogo simple para ajustar stock
            stock_dialog = tk.Toplevel(self.main_window)
            stock_dialog.title(f"Ajustar Stock - {product['name']}")
            stock_dialog.geometry("400x300")
            stock_dialog.resizable(False, False)
            stock_dialog.transient(self.main_window)
            stock_dialog.grab_set()
            
            # Centrar ventana
            stock_dialog.update_idletasks()
            x = (stock_dialog.winfo_screenwidth() // 2) - 200
            y = (stock_dialog.winfo_screenheight() // 2) - 150
            stock_dialog.geometry(f'400x300+{x}+{y}')
            
            # Header
            header = tk.Frame(stock_dialog, bg='#9b59b6', height=60)
            header.pack(fill='x')
            header.pack_propagate(False)
            
            tk.Label(
                header,
                text=f"📊 Ajustar Stock",
                font=('Segoe UI', 14, 'bold'),
                bg='#9b59b6',
                fg='white'
            ).pack(pady=15)
            
            # Contenido
            content = tk.Frame(stock_dialog, bg='white', padx=30, pady=20)
            content.pack(fill='both', expand=True)
            
            # Stock actual
            tk.Label(
                content,
                text=f"Stock Actual: {product['stock_quantity']}",
                font=('Segoe UI', 11),
                bg='white'
            ).pack(pady=(0, 20))
            
            # Tipo de movimiento
            tk.Label(
                content,
                text="Tipo de Ajuste:",
                font=('Segoe UI', 10, 'bold'),
                bg='white'
            ).pack(anchor='w')
            
            movement_var = tk.StringVar(value="adjustment")
            movement_frame = tk.Frame(content, bg='white')
            movement_frame.pack(fill='x', pady=5)
            
            tk.Radiobutton(
                movement_frame,
                text="Ajuste Manual",
                variable=movement_var,
                value="adjustment",
                bg='white'
            ).pack(side='left')
            
            # Cantidad
            tk.Label(
                content,
                text="Cantidad:",
                font=('Segoe UI', 10, 'bold'),
                bg='white'
            ).pack(anchor='w', pady=(10, 5))
            
            quantity_var = tk.StringVar(value="0")
            quantity_entry = tk.Entry(
                content,
                textvariable=quantity_var,
                font=('Segoe UI', 11),
                width=20
            )
            quantity_entry.pack(fill='x')
            
            tk.Label(
                content,
                text="(Positivo para agregar, negativo para quitar)",
                font=('Segoe UI', 8),
                bg='white',
                fg='#7f8c8d'
            ).pack(anchor='w')
            
            # Notas
            tk.Label(
                content,
                text="Notas:",
                font=('Segoe UI', 10, 'bold'),
                bg='white'
            ).pack(anchor='w', pady=(10, 5))
            
            notes_text = tk.Text(content, height=3, font=('Segoe UI', 10))
            notes_text.pack(fill='x')
            
            # Botones
            def on_save():
                try:
                    quantity = float(quantity_var.get())
                    notes = notes_text.get('1.0', tk.END).strip()
                    
                    success, message = self.product_controller.update_stock(
                        product['id'],
                        quantity,
                        movement_var.get(),
                        notes,
                        self.current_user
                    )
                    
                    if success:
                        messagebox.showinfo("Éxito", message, parent=stock_dialog)
                        stock_dialog.destroy()
                        self._load_products()
                    else:
                        messagebox.showerror("Error", message, parent=stock_dialog)
                
                except ValueError:
                    messagebox.showerror("Error", "La cantidad debe ser un número válido", parent=stock_dialog)
            
            button_frame = tk.Frame(stock_dialog, bg='#ecf0f1', height=60)
            button_frame.pack(fill='x', side='bottom')
            button_frame.pack_propagate(False)
            
            tk.Button(
                button_frame,
                text="💾 Guardar",
                font=('Segoe UI', 10, 'bold'),
                bg='#27ae60',
                fg='white',
                relief='flat',
                cursor='hand2',
                command=on_save,
                padx=20,
                pady=8
            ).pack(side='left', padx=20, pady=15)
            
            tk.Button(
                button_frame,
                text="❌ Cancelar",
                font=('Segoe UI', 10),
                bg='#95a5a6',
                fg='white',
                relief='flat',
                cursor='hand2',
                command=stock_dialog.destroy,
                padx=20,
                pady=8
            ).pack(side='left', pady=15)
        
        except Exception as e:
            self.logger.error(f"Error actualizando stock: {e}")
            messagebox.showerror("Error", f"Error al actualizar stock: {str(e)}")
    
    def _export_products(self):
        """Exportar productos a CSV/Excel"""
        try:
            messagebox.showinfo("Exportar", "Función de exportación en desarrollo")
        except Exception as e:
            self.logger.error(f"Error exportando productos: {e}")
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def _open_categories_window(self):
        """Mostrar gestión de categorías como ventana flotante"""
        try:
            if not self._check_user_permission('products.categories'):
                messagebox.showerror(
                    "Acceso denegado",
                    "No tienes permisos para gestionar categorías",
                    parent=self.main_window
                )
                return

            if self.category_window and self.category_window.winfo_exists():
                self.category_window.deiconify()
                self.category_window.lift()
                self.category_window.focus_force()
                return

            from views.category_management_view import CategoryManagementView
            from controllers.category_controller import CategoryController

            self.category_window = tk.Toplevel(self.main_window)
            self.category_window.title("Gestión de Categorías")
            self.category_window.geometry("1080x700")
            self._center_window(self.category_window, 1080, 700)
            self.category_window.transient(self.main_window)
            self.category_window.focus_force()

            # Cerrar correctamente
            self.category_window.protocol("WM_DELETE_WINDOW", self._close_category_window)

            category_controller = CategoryController()
            category_view = CategoryManagementView(self.category_window, self.current_user)

            def nav_callback(callback):
                def wrapper():
                    self._close_category_window()
                    if callable(callback):
                        callback()
                return wrapper

            category_view.register_callbacks(
                refresh=lambda: self._load_categories(category_view, category_controller),
                search=lambda term: self._search_categories(category_view, category_controller, term),
                create=lambda: self._create_category(
                    category_view,
                    category_controller,
                    parent_window=self.category_window
                ),
                edit=lambda cat_id: self._edit_category(
                    category_view,
                    category_controller,
                    cat_id,
                    parent_window=self.category_window
                ),
                delete=lambda cat_id: self._delete_category(
                    category_view,
                    category_controller,
                    cat_id,
                    parent_window=self.category_window
                ),
                back=self._close_category_window,
                new_sale=nav_callback(self._new_sale),
                sales_history=nav_callback(self._sales_history),
                view_products=nav_callback(self._view_products),
                view_categories=nav_callback(self._view_categories),
                stock_control=nav_callback(self._open_stock_window),
                daily_report=nav_callback(self._daily_sales_report),
                full_report=nav_callback(self._full_report),
                manage_users=nav_callback(self._manage_users),
                manage_roles=nav_callback(self._manage_roles),
                system_config=nav_callback(self._system_config),
                show_manual=nav_callback(self._show_manual),
                show_about=nav_callback(self._show_about)
            )

            self._load_categories(category_view, category_controller)

        except Exception as exc:
            self.logger.error(f"Error abriendo ventana de categorías: {exc}")
            import traceback
            traceback.print_exc()
            self._close_category_window()
            messagebox.showerror(
                "Error",
                f"No se pudo abrir la ventana de categorías: {exc}",
                parent=self.main_window
            )

    def _close_category_window(self):
        """Cerrar ventana flotante de categorías"""
        if self.category_window and self.category_window.winfo_exists():
            self.category_window.destroy()
        self.category_window = None
        if self.main_window:
            self.main_window.focus_force()

    def _open_stock_window(self):
        """Mostrar control de stock como ventana flotante"""
        try:
            if not self._check_user_permission('inventory.stock'):
                messagebox.showerror(
                    "Acceso denegado",
                    "No tienes permisos para controlar el stock",
                    parent=self.main_window
                )
                return

            if self.stock_window and self.stock_window.winfo_exists():
                self.stock_window.deiconify()
                self.stock_window.lift()
                self.stock_window.focus_force()
                return

            from views.stock_control_view import StockControlView
            from controllers.product_controller import ProductController

            self.stock_window = tk.Toplevel(self.main_window)
            self.stock_window.title("Control de Stock")
            self.stock_window.geometry("1200x720")
            self._center_window(self.stock_window, 1200, 720)
            self.stock_window.transient(self.main_window)
            self.stock_window.focus_force()
            self.stock_window.protocol("WM_DELETE_WINDOW", self._close_stock_window)

            stock_controller = ProductController()
            stock_view = StockControlView(self.stock_window, self.current_user)

            stock_view.register_callbacks(
                refresh=lambda: self._load_stock_products(stock_view, stock_controller),
                search=lambda term: self._search_stock_products(stock_view, stock_controller, term),
                update_stock=lambda data: self._update_product_stock(
                    stock_view,
                    stock_controller,
                    data,
                    parent_window=self.stock_window
                ),
                save_limits=lambda data: self._save_product_limits(
                    stock_view,
                    stock_controller,
                    data,
                    parent_window=self.stock_window
                ),
                back=self._close_stock_window
            )

            self._load_stock_products(stock_view, stock_controller)

        except Exception as exc:
            self.logger.error(f"Error abriendo ventana de stock: {exc}")
            import traceback
            traceback.print_exc()
            self._close_stock_window()
            messagebox.showerror(
                "Error",
                f"No se pudo abrir el control de stock: {exc}",
                parent=self.main_window
            )

    def _close_stock_window(self):
        """Cerrar ventana flotante de control de stock"""
        if self.stock_window and self.stock_window.winfo_exists():
            self.stock_window.destroy()
        self.stock_window = None
        if self.main_window:
            self.main_window.focus_force()

    def _view_categories(self):
        """Ver y gestionar categorías de productos"""
        try:
            print(f"🏷️ DEBUG: Abriendo gestión de categorías desde main_controller")
            print(f"   - main_window tipo: {type(self.main_window)}")
            print(f"   - current_user: {self.current_user}")
            
            # Limpiar ventana y marcar salida del dashboard
            self._clear_main_content()
            
            # Importar vista y controlador
            from views.category_management_view import CategoryManagementView
            from controllers.category_controller import CategoryController
            
            # Crear controlador
            category_controller = CategoryController()
            
            # Crear vista
            print("   🔄 Creando CategoryManagementView...")
            category_view = CategoryManagementView(self.main_window, self.current_user)
            print("   ✅ CategoryManagementView creada exitosamente")
            
            # Registrar callbacks
            category_view.register_callbacks(
                refresh=lambda: self._load_categories(category_view, category_controller),
                search=lambda term: self._search_categories(category_view, category_controller, term),
                create=lambda: self._create_category(category_view, category_controller),
                edit=lambda cat_id: self._edit_category(category_view, category_controller, cat_id),
                delete=lambda cat_id: self._delete_category(category_view, category_controller, cat_id),
                back=self._back_to_dashboard,
                # Callbacks de navegación del navbar
                new_sale=self._new_sale,
                sales_history=self._sales_history,
                view_products=self._view_products,
                view_categories=self._view_categories,
                stock_control=self._view_stock_control,
                daily_report=self._daily_sales_report,
                full_report=self._full_report,
                manage_users=self._manage_users,
                manage_roles=self._manage_roles,
                system_config=self._system_config,
                show_manual=self._show_manual,
                show_about=self._show_about
            )
            print("   ✅ Callbacks registrados")
            
            # Cargar categorías
            self._load_categories(category_view, category_controller)
            
            # IMPORTANTE: Restaurar geometría después de cargar todo
            self._restore_window_geometry()
            
        except Exception as e:
            self.logger.error(f"Error abriendo gestión de categorías: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al abrir gestión de categorías: {str(e)}")
    
    def _load_categories(self, view, controller):
        """Cargar categorías en la vista"""
        try:
            categories = controller.get_all_categories(self.current_user)
            view.load_categories(categories)
        except Exception as e:
            self.logger.error(f"Error cargando categorías: {e}")
            messagebox.showerror("Error", f"Error al cargar categorías: {str(e)}")
    
    def _search_categories(self, view, controller, search_term):
        """Buscar categorías"""
        try:
            categories = controller.search_categories(search_term, self.current_user)
            view.load_categories(categories)
        except Exception as e:
            self.logger.error(f"Error buscando categorías: {e}")
            messagebox.showerror("Error", f"Error al buscar: {str(e)}")
    
    def _create_category(self, view, controller, parent_window=None):
        """Crear nueva categoría"""
        try:
            from views.category_form_dialog import CategoryFormDialog
            
            # Obtener todas las categorías para el selector de padre
            categories = controller.get_all_categories(self.current_user)
            
            # Mostrar diálogo
            parent = parent_window or self.main_window
            dialog = CategoryFormDialog(parent, categories=categories)
            category_data = dialog.show()
            
            if category_data:
                success, message, category_id = controller.create_category(category_data, self.current_user)
                
                if success:
                    messagebox.showinfo("Éxito", message, parent=parent)
                    self._load_categories(view, controller)
                    if hasattr(self, 'product_controller') and self.product_controller:
                        self.product_controller.invalidate_category_cache()
                    if getattr(self, 'product_view', None) and getattr(self, 'product_controller', None):
                        self._load_product_categories()
                else:
                    messagebox.showerror("Error", message, parent=parent)
                    
        except Exception as e:
            self.logger.error(f"Error creando categoría: {e}")
            messagebox.showerror("Error", f"Error al crear categoría: {str(e)}", parent=parent_window or self.main_window)
    
    def _edit_category(self, view, controller, category_id, parent_window=None):
        """Editar categoría"""
        try:
            from views.category_form_dialog import CategoryFormDialog
            
            # Obtener categoría actual
            category = controller.get_category_by_id(category_id, self.current_user)
            if not category:
                messagebox.showerror("Error", "Categoría no encontrada", parent=parent_window or self.main_window)
                return
            
            # Obtener todas las categorías para el selector de padre
            categories = controller.get_all_categories(self.current_user, include_inactive=True)
            
            # Mostrar diálogo
            can_delete = self.permission_service.check_permission(self.current_user, 'inventory.delete')
            parent = parent_window or self.main_window
            dialog = CategoryFormDialog(
                parent,
                category=category,
                categories=categories,
                allow_delete=can_delete
            )
            category_data = dialog.show()
            
            if category_data:
                if category_data.get('__action__') == 'delete':
                    success, message = controller.delete_category(category_id, self.current_user)
                else:
                    success, message = controller.update_category(category_id, category_data, self.current_user)
                
                if success:
                    messagebox.showinfo("Éxito", message, parent=parent)
                    self._load_categories(view, controller)
                    if hasattr(self, 'product_controller') and self.product_controller:
                        self.product_controller.invalidate_category_cache()
                    if getattr(self, 'product_view', None) and getattr(self, 'product_controller', None):
                        self._load_product_categories()
                else:
                    messagebox.showerror("Error", message, parent=parent)
                    
        except Exception as e:
            self.logger.error(f"Error editando categoría: {e}")
            messagebox.showerror("Error", f"Error al editar categoría: {str(e)}", parent=parent_window or self.main_window)
    
    def _delete_category(self, view, controller, category_id, parent_window=None):
        """Eliminar categoría"""
        try:
            success, message = controller.delete_category(category_id, self.current_user)
            
            if success:
                messagebox.showinfo("Éxito", message, parent=parent_window or self.main_window)
                self._load_categories(view, controller)
                if hasattr(self, 'product_controller') and self.product_controller:
                    self.product_controller.invalidate_category_cache()
                if getattr(self, 'product_view', None) and getattr(self, 'product_controller', None):
                    self._load_product_categories()
            else:
                messagebox.showerror("Error", message, parent=parent_window or self.main_window)
                
        except Exception as e:
            self.logger.error(f"Error eliminando categoría: {e}")
            messagebox.showerror("Error", f"Error al eliminar: {str(e)}", parent=parent_window or self.main_window)
    
    def _view_stock_control(self):
        """Ver y controlar stock de productos"""
        try:
            print(f"📊 DEBUG: Abriendo control de stock desde main_controller")

            if not self._check_user_permission('inventory.stock'):
                messagebox.showerror(
                    "Acceso denegado",
                    "No tienes permisos para controlar el stock",
                    parent=self.main_window
                )
                return
            
            # Limpiar ventana y marcar salida del dashboard
            self._clear_main_content()
            
            # Importar vista y controlador
            from views.stock_control_view import StockControlView
            from controllers.product_controller import ProductController
            
            # Crear controlador
            product_controller = ProductController()
            
            # Crear vista
            print("   🔄 Creando StockControlView...")
            stock_view = StockControlView(self.main_window, self.current_user)
            print("   ✅ StockControlView creada exitosamente")
            
            # Registrar callbacks - Solo los que acepta el método
            stock_view.register_callbacks(
                refresh=lambda: self._load_stock_products(stock_view, product_controller),
                search=lambda term: self._search_stock_products(stock_view, product_controller, term),
                update_stock=lambda data: self._update_product_stock(stock_view, product_controller, data),
                save_limits=lambda data: self._save_product_limits(stock_view, product_controller, data),
                back=self._back_to_dashboard
            )
            print("   ✅ Callbacks registrados")
            
            # Cargar productos
            self._load_stock_products(stock_view, product_controller)
            
            # IMPORTANTE: Restaurar geometría después de cargar todo
            self._restore_window_geometry()
            
        except Exception as e:
            self.logger.error(f"Error abriendo control de stock: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al abrir control de stock: {str(e)}")
    
    def _load_stock_products(self, view, controller):
        """Cargar productos para control de stock"""
        try:
            products = controller.get_all_products(self.current_user, include_inactive=False)
            if products:
                view.load_products(products)
                print(f"   ✅ {len(products)} productos cargados")
        except Exception as e:
            self.logger.error(f"Error cargando productos: {e}")
            messagebox.showerror("Error", f"Error al cargar productos: {str(e)}")
    
    def _search_stock_products(self, view, controller, search_term):
        """Buscar productos para control de stock"""
        try:
            products = controller.search_products(search_term, self.current_user)
            if products is not None:
                view.load_products(products)
        except Exception as e:
            self.logger.error(f"Error buscando productos: {e}")
    
    def _update_product_stock(self, view, controller, update_data, parent_window=None):
        """Actualizar stock de un producto"""
        try:
            sku = update_data['sku']
            movement_type = update_data['movement_type']
            quantity = update_data['quantity']
            reason = update_data['reason']
            min_stock = update_data.get('min_stock', 0)
            max_stock = update_data.get('max_stock', 0)
            
            # Confirmar acción
            message = f"¿Confirmar {movement_type} de {quantity} unidades?"
            if not messagebox.askyesno("Confirmar", message, parent=parent_window or self.main_window):
                return
            
            # Actualizar stock según el tipo de movimiento
            success, message = controller.update_product_stock(
                sku=sku,
                movement_type=movement_type,
                quantity=quantity,
                user=self.current_user,
                reason=reason,
                min_stock=min_stock,
                max_stock=max_stock
            )
            
            if success:
                messagebox.showinfo("Éxito", message, parent=parent_window or self.main_window)
                view.clear_form()
                self._load_stock_products(view, controller)
                if getattr(self, 'product_view', None) and getattr(self, 'product_controller', None):
                    self._load_products()
            else:
                messagebox.showerror("Error", message, parent=parent_window or self.main_window)
                
        except Exception as e:
            self.logger.error(f"Error actualizando stock: {e}")
            messagebox.showerror(
                "Error",
                f"Error al actualizar stock: {str(e)}",
                parent=parent_window or self.main_window
            )
    
    def _save_product_limits(self, view, controller, limits_data, parent_window=None):
        """Guardar solo los límites de stock (min/max) sin afectar el stock actual"""
        try:
            print("\n" + "="*60)
            print("🔍 DEBUG: Guardando límites en controlador")
            print("="*60)
            
            sku = limits_data['sku']
            min_stock = limits_data['min_stock']
            max_stock = limits_data['max_stock']
            
            print(f"📦 SKU: {sku}")
            print(f"📊 Min: {min_stock}, Max: {max_stock}")
            
            # Confirmar acción
            message = f"¿Guardar límites de stock?\nMínimo: {min_stock}\nMáximo: {max_stock}"
            if not messagebox.askyesno("Confirmar", message, parent=parent_window or self.main_window):
                print("❌ Usuario canceló")
                return
            
            print("✅ Usuario confirmó, guardando...")
            
            # Guardar límites
            success, message = controller.save_product_limits(
                sku=sku,
                min_stock=min_stock,
                max_stock=max_stock,
                user=self.current_user
            )
            
            print(f"📊 Resultado: success={success}, message={message}")
            
            if success:
                messagebox.showinfo("Éxito", message, parent=parent_window or self.main_window)
                self._load_stock_products(view, controller)
                if getattr(self, 'product_view', None) and getattr(self, 'product_controller', None):
                    self._load_products()
                print("✅ Límites guardados y tabla recargada")
            else:
                messagebox.showerror("Error", message, parent=parent_window or self.main_window)
                print(f"❌ Error: {message}")
            
            print("="*60 + "\n")
                
        except Exception as e:
            self.logger.error(f"Error guardando límites: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror(
                "Error",
                f"Error al guardar límites: {str(e)}",
                parent=parent_window or self.main_window
            )
    
    def _add_product(self):
        """Agregar producto"""
        messagebox.showinfo("Agregar Producto", "Función en desarrollo")
    
    def _manage_inventory(self):
        """Gestionar inventario"""
        messagebox.showinfo("Inventario", "Módulo de inventario en desarrollo")
    
    def _daily_sales_report(self):
        """Reporte de ventas diarias - Muestra el reporte del día actual"""
        try:
            print("📊 DEBUG: Abriendo reporte diario de ventas")
            print(f"   - main_window tipo: {type(self.main_window)}")
            print(f"   - current_user: {self.current_user.get('username')}")
            
            # Limpiar ventana principal
            self._clear_main_content()
            print("   ✅ Ventana principal limpiada")
            
            # Importar vista de reporte diario
            from views.daily_sales_report_view import DailySalesReportView
            from controllers.report_controller import ReportController
            print("   🔄 Creando DailySalesReportView...")
            
            # Crear controlador de reportes
            report_controller = ReportController()
            
            # Crear vista de reporte diario
            daily_report_view = DailySalesReportView(
                self.main_window,
                report_controller,
                self.current_user,
                on_back=self._show_dashboard
            )
            
            print("   ✅ DailySalesReportView creada exitosamente")
            
        except Exception as e:
            print(f"❌ ERROR en _daily_sales_report: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror(
                "Error",
                f"No se pudo abrir el reporte diario:\n{str(e)}"
            )
    
    def _full_report(self):
        """Reporte completo"""
        self._open_reports_module()
    
    def _open_reports_module(self):
        """Abrir módulo de reportes"""
        try:
            print("📊 DEBUG: Abriendo módulo de reportes")
            print(f"   - main_window tipo: {type(self.main_window)}")
            print(f"   - current_user: {self.current_user.get('username')}")
            
            # Limpiar ventana principal
            self._clear_main_content()
            print("   ✅ Ventana principal limpiada")
            
            # Importar vista y controlador de reportes
            from views.reports_view import ReportsView
            from controllers.report_controller import ReportController
            print("   🔄 Creando ReportsView...")
            
            # Crear controlador de reportes
            self.report_controller = ReportController()
            
            # Crear vista de reportes
            self.reports_view = ReportsView(
                parent=self.main_window,
                controller=self.report_controller,
                user_data=self.current_user,
                on_back=self._show_dashboard
            )
            print("   ✅ ReportsView creada exitosamente")
            
            # Mostrar vista
            self.reports_view.show()
            print("   📺 Vista de reportes mostrada")
            
            # Restaurar geometría
            self._restore_window_geometry()
            
        except Exception as e:
            self.logger.error(f"Error abriendo módulo de reportes: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"No se pudo abrir el módulo de reportes:\n{str(e)}")
    
    def _config_tickets(self):
        """Configurar boletas"""
        try:
            print("🎫 DEBUG: Abriendo configuración de boletas")
            
            # Limpiar ventana principal
            self._clear_main_content()
            
            # Crear vista de configuración de tickets
            from views.ticket_config_view import TicketConfigView
            
            self.ticket_config_view = TicketConfigView(
                parent=self.main_window,
                on_back=self._show_dashboard
            )
            
            self.ticket_config_view.show()
            print("   ✅ Vista de configuración de boletas mostrada")
            
        except Exception as e:
            self.logger.error(f"Error abriendo configuración de boletas: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"No se pudo abrir configuración de boletas:\n{str(e)}")
    
    def _manage_users(self):
        """Gestionar usuarios"""
        try:
            print("👥 DEBUG: Abriendo gestión de usuarios desde main_controller")
            print(f"   - main_window tipo: {type(self.main_window)}")
            print(f"   - current_user: {self.current_user}")
            
            # Verificar permisos del usuario
            if not self._check_user_permission('users.view'):
                messagebox.showerror("Acceso Denegado", "No tienes permisos para acceder a la gestión de usuarios")
                return
            
            # Limpiar la ventana principal (guarda geometría automáticamente)
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
            
            # Registrar callbacks - NAVBAR COMPLETO
            self.users_view.bind_callback('back_to_dashboard', self._back_to_dashboard)
            self.users_view.bind_callback('new_sale', self._new_sale)
            self.users_view.bind_callback('sales_history', self._sales_history)
            self.users_view.bind_callback('view_products', self._view_products)
            self.users_view.bind_callback('view_categories', self._view_categories)
            self.users_view.bind_callback('stock_control', self._view_stock_control)
            self.users_view.bind_callback('daily_report', self._daily_sales_report)
            self.users_view.bind_callback('full_report', self._full_report)
            self.users_view.bind_callback('manage_roles', self._manage_roles)
            self.users_view.bind_callback('system_config', self._system_config)
            self.users_view.bind_callback('show_manual', self._show_manual)
            self.users_view.bind_callback('show_about', self._show_about)
            print("   ✅ Callbacks registrados")
            
            # IMPORTANTE: Restaurar geometría después de cargar vista
            self._restore_window_geometry()
            
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
            if not self._check_user_permission('roles.view'):
                messagebox.showerror("Acceso Denegado", "No tienes permisos para acceder a la gestión de roles")
                return
            
            # Limpiar la ventana principal (guarda geometría automáticamente)
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
            
            # Registrar callbacks - NAVBAR COMPLETO
            self.roles_view.bind_callback('back_to_dashboard', self._back_to_dashboard)
            self.roles_view.bind_callback('new_sale', self._new_sale)
            self.roles_view.bind_callback('sales_history', self._sales_history)
            self.roles_view.bind_callback('view_products', self._view_products)
            self.roles_view.bind_callback('view_categories', self._view_categories)
            self.roles_view.bind_callback('stock_control', self._view_stock_control)
            self.roles_view.bind_callback('daily_report', self._daily_sales_report)
            self.roles_view.bind_callback('full_report', self._full_report)
            self.roles_view.bind_callback('manage_users', self._manage_users)
            self.roles_view.bind_callback('system_config', self._system_config)
            self.roles_view.bind_callback('show_manual', self._show_manual)
            self.roles_view.bind_callback('show_about', self._show_about)
            
            # Callback especial para recargar permisos
            self.roles_view.bind_callback('reload_permissions', self.reload_current_user_permissions)
            
            print("   ✅ Callbacks registrados")
            
            # IMPORTANTE: Restaurar geometría después de cargar vista
            self._restore_window_geometry()
            
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
        messagebox.showinfo("Soporte Técnico", "Chat de Soporte\n\nPara asistencia inmediata comunicate con:\n📧 lmqpando@gmail.com\n📞 +51 960724886")
    
    def _system_config(self):
        """Configuración del sistema"""
        try:
            print("🔧 DEBUG: Abriendo configuración desde main_controller")
            print(f"   - main_window tipo: {type(self.main_window)}")
            print(f"   - current_user: {self.current_user}")
            
            # Limpiar la ventana principal (guarda geometría automáticamente)
            self._clear_main_content()
            print("   ✅ Ventana principal limpiada")
            
            # Crear contenido de configuración en la ventana principal
            from views.configuration_view import ConfigurationView
            print("   🔄 Creando ConfigurationView...")
            
            self.config_view = ConfigurationView(self.main_window, self.current_user, embedded=True)
            print("   ✅ ConfigurationView creada exitosamente")
            
            # Registrar callbacks - NAVBAR COMPLETO
            self.config_view.bind_callback('back_to_dashboard', self._back_to_dashboard)
            self.config_view.bind_callback('configuration_saved', self._on_configuration_saved)
            self.config_view.bind_callback('new_sale', self._new_sale)
            self.config_view.bind_callback('sales_history', self._sales_history)
            self.config_view.bind_callback('view_products', self._view_products)
            self.config_view.bind_callback('view_categories', self._view_categories)
            self.config_view.bind_callback('stock_control', self._view_stock_control)
            self.config_view.bind_callback('daily_report', self._daily_sales_report)
            self.config_view.bind_callback('full_report', self._full_report)
            self.config_view.bind_callback('manage_users', self._manage_users)
            self.config_view.bind_callback('manage_roles', self._manage_roles)
            self.config_view.bind_callback('show_manual', self._show_manual)
            self.config_view.bind_callback('show_about', self._show_about)
            print("   ✅ Callbacks registrados")
            
            # IMPORTANTE: Restaurar geometría después de cargar vista
            self._restore_window_geometry()
            
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
