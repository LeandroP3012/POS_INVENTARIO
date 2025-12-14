"""
Vista de Configuración del Sistema
Panel completo de configuración con múltiples categorías
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, Any, Callable
import json
import os
from datetime import datetime
from views.base_view import BaseView
from controllers.configuration_controller import ConfigurationController
from utils.responsive_utils import ResponsiveManager


class ConfigurationView(BaseView):
    """Vista completa de configuración del sistema"""
    
    def __init__(self, root: tk.Tk, user_data: Dict[str, Any] = None, embedded: bool = False):
        # Constructor ConfigurationView inicializado
        
        super().__init__(root)
        self.user_data = user_data or {}
        self.config_data = {}
        self.changes_made = False
        self.embedded = embedded
        self.loading_data = True  # Flag para evitar marcar cambios durante la carga
        self.saving_data = False  # Flag para evitar marcar cambios durante el guardado
        
        # Inicializar gestor responsivo
        self.responsive = ResponsiveManager(self.root)
        
        # Callbacks para navegación del navbar
        self.callbacks = {}
        self.navbar_built = False
        
        # Inicializar controlador de configuración
        self.config_controller = ConfigurationController()
        # Controlador de configuración inicializado
        
        # Cargar configuración
        self.load_configuration()
        
        # Crear interfaz
        self.setup_configuration_window()
        
        # Actualizar interfaz con los datos cargados
        self.update_ui_with_config()
        
        # Programar una segunda actualización para asegurar que todo se aplique
        if hasattr(self, 'root'):
            self.root.after(100, self.force_ui_refresh)
    
    def setup_configuration_window(self):
        """Configurar ventana de configuración"""
        if not self.embedded:
            # Configuración para ventana independiente
            self.root.title("Sistema POS - Configuración")
            self.root.geometry("1000x700")
            self.root.configure(bg='#f8f9fa')
            
            # Centrar ventana
            self.center_window(1000, 700)
            
            # Configurar protocolo de cierre
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        else:
            # Configuración para modo embebido
            self.root.configure(bg='#f8f9fa')
        
        self.create_configuration_interface()
    
    def create_configuration_interface(self):
        """Crear interfaz de configuración"""
        # Header
        self.create_header()
        
        # El navbar se creará después de registrar callbacks
        # en build_navbar()
        
        # Notebook para las categorías
        self.create_categories_notebook()
        
        # Footer con botones de acción
        self.create_action_buttons()
    
    def create_header(self):
        """Crear header de configuración"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        content_frame = tk.Frame(header_frame, bg='#2c3e50')
        content_frame.pack(expand=True, fill='both', padx=30, pady=15)
        
        # Título (izquierda)
        title_label = tk.Label(
            content_frame,
            text="⚙️ Configuración del Sistema",
            font=('Segoe UI', 20, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(side='left')
        
        # Botón de volver (derecha) - solo en modo embebido
        if self.embedded:
            back_button = tk.Button(
                content_frame,
                text="⬅️ Volver al Dashboard",
                command=self.go_back_to_dashboard,
                bg='#34495e',
                fg='white',
                font=('Segoe UI', 10, 'bold'),
                relief='flat',
                cursor='hand2',
                padx=15,
                pady=8
            )
            back_button.pack(side='right', padx=10)
        
        # Usuario actual (derecha, antes del botón)
        user_text = f"Usuario: {self.user_data.get('full_name', self.user_data.get('username', 'Admin'))}"
        user_label = tk.Label(
            content_frame,
            text=user_text,
            font=('Segoe UI', 12),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        user_label.pack(side='right')
    
    def create_navbar(self, after_widget=None):
        """Crear navbar personalizado - GLOBAL para todos los módulos"""
        navbar_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        if after_widget:
            navbar_frame.pack(fill='x', after=after_widget)
        else:
            navbar_frame.pack(fill='x')
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
        
        # Helper para ejecutar callbacks de forma segura
        def safe_call(callback_name):
            def wrapper():
                print(f"🔄 Navbar (config): Intentando ejecutar '{callback_name}'")
                callback = self.callbacks.get(callback_name)
                if callback:
                    print(f"   ✓ Callback encontrado, ejecutando...")
                    callback()
                else:
                    print(f"   ✗ Callback no encontrado o es None")
            return wrapper
        
        # Botón Archivo
        file_btn = tk.Menubutton(buttons_container, text="📁 Archivo", **btn_style)
        file_btn.pack(side='left', padx=2)
        file_menu = tk.Menu(file_btn, tearoff=0, font=('Segoe UI', 11))
        file_btn.config(menu=file_menu)
        file_menu.add_command(label="Nueva Venta", command=safe_call('new_sale'))
        file_menu.add_separator()
        file_menu.add_command(label="Volver al Dashboard", command=safe_call('back_to_dashboard'))
        
        # Botón Ventas
        sales_btn = tk.Menubutton(buttons_container, text="💰 Ventas", **btn_style)
        sales_btn.pack(side='left', padx=2)
        sales_menu = tk.Menu(sales_btn, tearoff=0, font=('Segoe UI', 11))
        sales_btn.config(menu=sales_menu)
        sales_menu.add_command(label="Nueva Venta", command=safe_call('new_sale'))
        sales_menu.add_command(label="Historial de Ventas", command=safe_call('sales_history'))
        
        # Botón Inventario
        inv_btn = tk.Menubutton(buttons_container, text="📦 Inventario", **btn_style)
        inv_btn.pack(side='left', padx=2)
        inv_menu = tk.Menu(inv_btn, tearoff=0, font=('Segoe UI', 11))
        inv_btn.config(menu=inv_menu)
        inv_menu.add_command(label="Ver Productos", command=safe_call('view_products'))
        inv_menu.add_command(label="Gestionar Categorías", command=safe_call('view_categories'))
        inv_menu.add_command(label="Control de Stock", command=safe_call('stock_control'))
        
        # Botón Reportes
        rep_btn = tk.Menubutton(buttons_container, text="📊 Reportes", **btn_style)
        rep_btn.pack(side='left', padx=2)
        rep_menu = tk.Menu(rep_btn, tearoff=0, font=('Segoe UI', 11))
        rep_btn.config(menu=rep_menu)
        rep_menu.add_command(label="Ventas del Día", command=safe_call('daily_report'))
        rep_menu.add_command(label="Reporte Completo", command=safe_call('full_report'))
        
        # Botón Administración (ACTIVO)
        admin_btn = tk.Menubutton(buttons_container, text="⚙️ Administración", **btn_style)
        admin_btn.config(bg='#34495e')  # Resaltar activo
        admin_btn.pack(side='left', padx=2)
        admin_menu = tk.Menu(admin_btn, tearoff=0, font=('Segoe UI', 11))
        admin_btn.config(menu=admin_menu)
        admin_menu.add_command(label="Gestionar Usuarios", command=safe_call('manage_users'))
        admin_menu.add_command(label="Gestionar Roles", command=safe_call('manage_roles'))
        admin_menu.add_separator()
        admin_menu.add_command(label="Configuración del Sistema ✓", command=lambda: None)  # Actual
        
        # Botón Ayuda
        help_btn = tk.Menubutton(buttons_container, text="❓ Ayuda", **btn_style)
        help_btn.pack(side='left', padx=2)
        help_menu = tk.Menu(help_btn, tearoff=0, font=('Segoe UI', 11))
        help_btn.config(menu=help_menu)
        help_menu.add_command(label="Manual de Usuario", command=safe_call('show_manual'))
        help_menu.add_command(label="Acerca de", command=safe_call('show_about'))
    
    def create_categories_notebook(self):
        """Crear notebook con categorías de configuración"""
        # Frame para el notebook
        notebook_frame = tk.Frame(self.root, bg='#f8f9fa')
        notebook_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Crear notebook
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Configurar estilo
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[20, 8])
        
        # Crear pestañas
        self.create_company_tab()
        self.create_system_tab()
        self.create_printer_tab()
        self.create_database_tab()
        self.create_security_tab()
        self.create_backup_tab()
    
    def create_company_tab(self):
        """Crear pestaña de configuración de empresa"""
        # Frame de la pestaña
        company_frame = ttk.Frame(self.notebook)
        self.notebook.add(company_frame, text="🏢 Empresa")
        
        # Scroll frame
        canvas = tk.Canvas(company_frame, bg='white')
        scrollbar = ttk.Scrollbar(company_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Contenido de la pestaña
        self.create_company_content(scrollable_frame)
    
    def create_company_content(self, parent):
        """Crear contenido de configuración de empresa"""
        # Título de sección
        title_frame = tk.Frame(parent, bg='white')
        title_frame.pack(fill='x', padx=30, pady=(30, 20))
        
        tk.Label(
            title_frame,
            text="🏢 Información de la Empresa",
            font=('Segoe UI', 18, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w')
        
        tk.Label(
            title_frame,
            text="Configure los datos de su empresa que aparecerán en facturas, reportes y documentos oficiales",
            font=('Segoe UI', 11),
            fg='#7f8c8d',
            bg='white'
        ).pack(anchor='w', pady=(5, 0))
        
        # Frame principal con dos columnas
        main_frame = tk.Frame(parent, bg='white')
        main_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Columna izquierda - Información básica
        left_column = tk.Frame(main_frame, bg='white')
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        # Título columna izquierda
        left_title = tk.Label(
            left_column,
            text="📋 Datos Básicos",
            font=('Segoe UI', 14, 'bold'),
            fg='#34495e',
            bg='white'
        )
        left_title.pack(anchor='w', pady=(0, 15))
        
        # Campos básicos
        self.create_config_field_improved(
            left_column, "Nombre de la Empresa:", "company_name", 
            "Mi Negocio POS", "Nombre que aparecerá en facturas y reportes"
        )
        
        self.create_config_field_improved(
            left_column, "RUT/NIT:", "company_rut", 
            "12.345.678-9", "Identificación tributaria de la empresa"
        )
        
        self.create_config_field_improved(
            left_column, "Dirección:", "company_address", 
            "Calle Principal #123", "Dirección física de la empresa"
        )
        
        # Columna derecha - Información de contacto
        right_column = tk.Frame(main_frame, bg='white')
        right_column.pack(side='right', fill='both', expand=True, padx=(15, 0))
        
        # Título columna derecha
        right_title = tk.Label(
            right_column,
            text="📞 Información de Contacto",
            font=('Segoe UI', 14, 'bold'),
            fg='#34495e',
            bg='white'
        )
        right_title.pack(anchor='w', pady=(0, 15))
        
        # Campos de contacto
        self.create_config_field_improved(
            right_column, "Teléfono:", "company_phone", 
            "+56 9 1234 5678", "Teléfono de contacto principal"
        )
        
        self.create_config_field_improved(
            right_column, "Email:", "company_email", 
            "contacto@minegocio.com", "Email de contacto oficial"
        )
        
        self.create_config_field_improved(
            right_column, "Sitio Web:", "company_website", 
            "www.minegocio.com", "Sitio web de la empresa (opcional)"
        )
        
        # Sección del logo que ocupa todo el ancho
        logo_section = tk.Frame(parent, bg='#f8f9fa', relief='solid', bd=1)
        logo_section.pack(fill='x', padx=30, pady=20)
        
        logo_inner = tk.Frame(logo_section, bg='#f8f9fa')
        logo_inner.pack(fill='x', padx=20, pady=20)
        
        # Título de logo
        logo_title = tk.Label(
            logo_inner,
            text="🖼️ Logo de la Empresa",
            font=('Segoe UI', 14, 'bold'),
            fg='#34495e',
            bg='#f8f9fa'
        )
        logo_title.pack(anchor='w')
        
        logo_desc = tk.Label(
            logo_inner,
            text="Seleccione el logo que aparecerá en recibos, facturas y documentos del sistema",
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='#f8f9fa'
        )
        logo_desc.pack(anchor='w', pady=(5, 15))
        
        # Frame para logo con preview
        logo_content_frame = tk.Frame(logo_inner, bg='#f8f9fa')
        logo_content_frame.pack(fill='x')
        
        # Información del archivo
        logo_info_frame = tk.Frame(logo_content_frame, bg='#f8f9fa')
        logo_info_frame.pack(side='left', fill='both', expand=True)
        
        self.logo_path_var = tk.StringVar(value=self.config_data.get('logo_path', 'No se ha seleccionado ningún logo'))
        logo_path_label = tk.Label(
            logo_info_frame,
            textvariable=self.logo_path_var,
            font=('Segoe UI', 11),
            fg='#2c3e50',
            bg='#f8f9fa',
            anchor='w',
            justify='left'
        )
        logo_path_label.pack(fill='x', pady=(0, 10))
        
        # Botones de logo
        logo_buttons_frame = tk.Frame(logo_info_frame, bg='#f8f9fa')
        logo_buttons_frame.pack(fill='x')
        
        logo_button = tk.Button(
            logo_buttons_frame,
            text="📁 Seleccionar Logo",
            command=self.select_company_logo,
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8
        )
        logo_button.pack(side='left', padx=(0, 10))
        
        clear_logo_button = tk.Button(
            logo_buttons_frame,
            text="🗑️ Quitar Logo",
            command=self.clear_company_logo,
            bg='#e74c3c',
            fg='white',
            font=('Segoe UI', 11),
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8
        )
        clear_logo_button.pack(side='left')
    
    def create_system_tab(self):
        """Crear pestaña de configuración del sistema"""
        system_frame = ttk.Frame(self.notebook)
        self.notebook.add(system_frame, text="💻 Sistema")
        
        # Scroll frame
        canvas = tk.Canvas(system_frame, bg='white')
        scrollbar = ttk.Scrollbar(system_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.create_system_content(scrollable_frame)
    
    def create_system_content(self, parent):
        """Crear contenido de configuración del sistema"""
        # Título principal
        title_frame = tk.Frame(parent, bg='white')
        title_frame.pack(fill='x', padx=30, pady=(30, 20))
        
        tk.Label(
            title_frame,
            text="💻 Configuración del Sistema",
            font=('Segoe UI', 18, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w')
        
        tk.Label(
            title_frame,
            text="Personalice el comportamiento y apariencia del sistema según sus necesidades",
            font=('Segoe UI', 11),
            fg='#7f8c8d',
            bg='white'
        ).pack(anchor='w', pady=(5, 0))
        
        # Frame principal con dos columnas
        main_frame = tk.Frame(parent, bg='white')
        main_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Columna izquierda - Configuración monetaria y fiscal
        left_column = tk.Frame(main_frame, bg='white')
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        # Configuración de moneda
        currency_section = tk.Frame(left_column, bg='#f8f9fa', relief='solid', bd=1)
        currency_section.pack(fill='x', pady=(0, 20))
        
        currency_inner = tk.Frame(currency_section, bg='#f8f9fa')
        currency_inner.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            currency_inner,
            text="💰 Configuración Monetaria",
            font=('Segoe UI', 14, 'bold'),
            fg='#34495e',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        tk.Label(
            currency_inner,
            text="Configure la moneda y formato de precios",
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='#f8f9fa'
        ).pack(anchor='w', pady=(5, 15))
        
        # Moneda
        tk.Label(
            currency_inner,
            text="Moneda Principal:",
            font=('Segoe UI', 12, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        # CREAR COMBOBOX SIN TEXTVARIABLE - APLICAR FIX MANUAL
        currency_combo = ttk.Combobox(
            currency_inner,
            values=['CLP', 'USD', 'EUR', 'ARS', 'PEN', 'MXN'],
            state='readonly',
            font=('Segoe UI', 11)
        )
        currency_combo.pack(fill='x', pady=(5, 15), ipady=5)
        
        # ESTABLECER VALOR INICIAL DIRECTAMENTE
        initial_currency = self.config_data.get('currency', 'CLP')
        currency_combo.set(initial_currency)
        
        # CREAR VARIABLE PARA TRACKING MANUAL
        self.currency_var = tk.StringVar(value=initial_currency)
        
        # SINCRONIZACIÓN MANUAL BIDIRECCIONAL
        def on_currency_change(event):
            """Sincronizar Combobox → Variable"""
            new_value = currency_combo.get()
            self.currency_var.set(new_value)
            self.mark_changes_made()
        
        def on_currency_var_change(*args):
            """Sincronizar Variable → Combobox"""
            new_value = self.currency_var.get()
            if currency_combo.get() != new_value:
                currency_combo.set(new_value)
        
        currency_combo.bind('<<ComboboxSelected>>', on_currency_change)
        self.currency_var.trace_add('write', on_currency_var_change)
        
        # REGISTRO EN MAPA DE WIDGETS MANUALES
        if not hasattr(self, 'widget_var_map'):
            self.widget_var_map = {}
        self.widget_var_map[currency_combo] = ('currency', self.currency_var)
        
        print(f"      👀 Combobox creado para currency: valor='{currency_combo.get()}' | ✅ SINCRONIZADO MANUALMENTE")
        
        # Símbolo de moneda
        tk.Label(
            currency_inner,
            text="Símbolo de Moneda:",
            font=('Segoe UI', 12, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        # CREAR ENTRY SIN TEXTVARIABLE - APLICAR FIX MANUAL
        currency_symbol_entry = tk.Entry(
            currency_inner,
            font=('Segoe UI', 12),
            relief='solid',
            bd=1,
            bg='white'
        )
        currency_symbol_entry.pack(fill='x', pady=5, ipady=8)
        
        # ESTABLECER VALOR INICIAL DIRECTAMENTE
        initial_symbol = self.config_data.get('currency_symbol', 'S/')
        currency_symbol_entry.delete(0, tk.END)
        currency_symbol_entry.insert(0, initial_symbol)
        
        # CREAR VARIABLE PARA TRACKING MANUAL
        self.currency_symbol_var = tk.StringVar(value=initial_symbol)
        
        # SINCRONIZACIÓN MANUAL BIDIRECCIONAL
        def on_symbol_change(event):
            """Sincronizar Entry → Variable"""
            new_value = currency_symbol_entry.get()
            self.currency_symbol_var.set(new_value)
            self.mark_changes_made()
        
        def on_symbol_var_change(*args):
            """Sincronizar Variable → Entry"""
            new_value = self.currency_symbol_var.get()
            if currency_symbol_entry.get() != new_value:
                currency_symbol_entry.delete(0, tk.END)
                currency_symbol_entry.insert(0, new_value)
        
        currency_symbol_entry.bind('<KeyRelease>', on_symbol_change)
        currency_symbol_entry.bind('<FocusOut>', on_symbol_change)
        self.currency_symbol_var.trace_add('write', on_symbol_var_change)
        
        # REGISTRO EN MAPA DE WIDGETS MANUALES
        self.widget_var_map[currency_symbol_entry] = ('currency_symbol', self.currency_symbol_var)
        
        print(f"      👀 Entry creado para currency_symbol: valor='{currency_symbol_entry.get()}' | ✅ SINCRONIZADO MANUALMENTE")
        
        # Configuración de impuestos
        tax_section = tk.Frame(left_column, bg='#f8f9fa', relief='solid', bd=1)
        tax_section.pack(fill='x')
        
        tax_inner = tk.Frame(tax_section, bg='#f8f9fa')
        tax_inner.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            tax_inner,
            text="📊 Configuración Fiscal",
            font=('Segoe UI', 14, 'bold'),
            fg='#34495e',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        tk.Label(
            tax_inner,
            text="Configure impuestos y su aplicación",
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='#f8f9fa'
        ).pack(anchor='w', pady=(5, 15))
        
        # IVA
        tk.Label(
            tax_inner,
            text="Tasa de IVA (%):",
            font=('Segoe UI', 12, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        # CREAR ENTRY SIN TEXTVARIABLE - APLICAR FIX MANUAL
        tax_entry = tk.Entry(
            tax_inner,
            font=('Segoe UI', 12),
            relief='solid',
            bd=1,
            bg='white'
        )
        tax_entry.pack(fill='x', pady=(5, 15), ipady=8)
        
        # ESTABLECER VALOR INICIAL DIRECTAMENTE
        initial_tax = self.config_data.get('tax_rate', '19')
        tax_entry.delete(0, tk.END)
        tax_entry.insert(0, initial_tax)
        
        # CREAR VARIABLE PARA TRACKING MANUAL
        self.tax_rate_var = tk.StringVar(value=initial_tax)
        
        # SINCRONIZACIÓN MANUAL BIDIRECCIONAL
        def on_tax_change(event):
            """Sincronizar Entry → Variable"""
            new_value = tax_entry.get()
            self.tax_rate_var.set(new_value)
            self.mark_changes_made()
        
        def on_tax_var_change(*args):
            """Sincronizar Variable → Entry"""
            new_value = self.tax_rate_var.get()
            if tax_entry.get() != new_value:
                tax_entry.delete(0, tk.END)
                tax_entry.insert(0, new_value)
        
        tax_entry.bind('<KeyRelease>', on_tax_change)
        tax_entry.bind('<FocusOut>', on_tax_change)
        self.tax_rate_var.trace_add('write', on_tax_var_change)
        
        # REGISTRO EN MAPA DE WIDGETS MANUALES
        self.widget_var_map[tax_entry] = ('tax_rate', self.tax_rate_var)
        
        print(f"      👀 Entry creado para tax_rate: valor='{tax_entry.get()}' | ✅ SINCRONIZADO MANUALMENTE")
        
        # Incluir impuestos en precio
        self.include_tax_var = tk.BooleanVar(value=self.config_data.get('include_tax', True))
        self.include_tax_var.trace_add('write', self.safe_mark_changes)
        tax_check = tk.Checkbutton(
            tax_inner,
            text="Incluir impuestos en el precio mostrado",
            variable=self.include_tax_var,
            font=('Segoe UI', 11),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        tax_check.pack(anchor='w', pady=5)
        
        # Columna derecha - Configuración de interfaz
        right_column = tk.Frame(main_frame, bg='white')
        right_column.pack(side='right', fill='both', expand=True, padx=(15, 0))
        
        # Configuración de interfaz
        ui_section = tk.Frame(right_column, bg='#f8f9fa', relief='solid', bd=1)
        ui_section.pack(fill='x', pady=(0, 20))
        
        ui_inner = tk.Frame(ui_section, bg='#f8f9fa')
        ui_inner.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            ui_inner,
            text="🎨 Personalización de Interfaz",
            font=('Segoe UI', 14, 'bold'),
            fg='#34495e',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        tk.Label(
            ui_inner,
            text="Personalice la apariencia del sistema",
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='#f8f9fa'
        ).pack(anchor='w', pady=(5, 15))
        
        # Tema
        tk.Label(
            ui_inner,
            text="Tema de la Interfaz:",
            font=('Segoe UI', 12, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        # CREAR COMBOBOX SIN TEXTVARIABLE - APLICAR FIX MANUAL
        theme_combo = ttk.Combobox(
            ui_inner,
            values=['Claro', 'Oscuro', 'Automático'],
            state='readonly',
            font=('Segoe UI', 11)
        )
        theme_combo.pack(fill='x', pady=(5, 15), ipady=5)
        
        # ESTABLECER VALOR INICIAL DIRECTAMENTE
        initial_theme = self.config_data.get('theme', 'Claro')
        theme_combo.set(initial_theme)
        
        # CREAR VARIABLE PARA TRACKING MANUAL
        self.theme_var = tk.StringVar(value=initial_theme)
        
        # SINCRONIZACIÓN MANUAL BIDIRECCIONAL
        def on_theme_change(event):
            """Sincronizar Combobox → Variable"""
            new_value = theme_combo.get()
            self.theme_var.set(new_value)
            self.mark_changes_made()
        
        def on_theme_var_change(*args):
            """Sincronizar Variable → Combobox"""
            new_value = self.theme_var.get()
            if theme_combo.get() != new_value:
                theme_combo.set(new_value)
        
        theme_combo.bind('<<ComboboxSelected>>', on_theme_change)
        self.theme_var.trace_add('write', on_theme_var_change)
        
        # REGISTRO EN MAPA DE WIDGETS MANUALES
        self.widget_var_map[theme_combo] = ('theme', self.theme_var)
        
        print(f"      👀 Combobox creado para theme: valor='{theme_combo.get()}' | ✅ SINCRONIZADO MANUALMENTE")
        
        # Idioma
        tk.Label(
            ui_inner,
            text="Idioma del Sistema:",
            font=('Segoe UI', 12, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        # CREAR COMBOBOX SIN TEXTVARIABLE - APLICAR FIX MANUAL
        language_combo = ttk.Combobox(
            ui_inner,
            values=['Español', 'English', 'Português'],
            state='readonly',
            font=('Segoe UI', 11)
        )
        language_combo.pack(fill='x', pady=5, ipady=5)
        
        # ESTABLECER VALOR INICIAL DIRECTAMENTE
        initial_language = self.config_data.get('language', 'Español')
        language_combo.set(initial_language)
        
        # CREAR VARIABLE PARA TRACKING MANUAL
        self.language_var = tk.StringVar(value=initial_language)
        
        # SINCRONIZACIÓN MANUAL BIDIRECCIONAL
        def on_language_change(event):
            """Sincronizar Combobox → Variable"""
            new_value = language_combo.get()
            self.language_var.set(new_value)
            self.mark_changes_made()
        
        def on_language_var_change(*args):
            """Sincronizar Variable → Combobox"""
            new_value = self.language_var.get()
            if language_combo.get() != new_value:
                language_combo.set(new_value)
        
        language_combo.bind('<<ComboboxSelected>>', on_language_change)
        self.language_var.trace_add('write', on_language_var_change)
        
        # REGISTRO EN MAPA DE WIDGETS MANUALES
        self.widget_var_map[language_combo] = ('language', self.language_var)
        
        print(f"      👀 Combobox creado para language: valor='{language_combo.get()}' | ✅ SINCRONIZADO MANUALMENTE")
        
        # Configuración adicional del sistema
        system_section = tk.Frame(right_column, bg='#f8f9fa', relief='solid', bd=1)
        system_section.pack(fill='x')
        
        system_inner = tk.Frame(system_section, bg='#f8f9fa')
        system_inner.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            system_inner,
            text="⚙️ Configuración Adicional",
            font=('Segoe UI', 14, 'bold'),
            fg='#34495e',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        tk.Label(
            system_inner,
            text="Opciones adicionales del sistema",
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='#f8f9fa'
        ).pack(anchor='w', pady=(5, 15))
        
        # Opciones adicionales
        self.show_animations_var = tk.BooleanVar(value=self.config_data.get('show_animations', True))
        self.show_animations_var.trace_add('write', self.safe_mark_changes)
        animations_check = tk.Checkbutton(
            system_inner,
            text="Mostrar animaciones en la interfaz",
            variable=self.show_animations_var,
            font=('Segoe UI', 11),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        animations_check.pack(anchor='w', pady=5)
        
        self.sound_notifications_var = tk.BooleanVar(value=self.config_data.get('sound_notifications', True))
        self.sound_notifications_var.trace_add('write', self.safe_mark_changes)
        sound_check = tk.Checkbutton(
            system_inner,
            text="Reproducir sonidos de notificación",
            variable=self.sound_notifications_var,
            font=('Segoe UI', 11),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        sound_check.pack(anchor='w', pady=5)
        
        self.auto_save_var = tk.BooleanVar(value=self.config_data.get('auto_save', True))
        self.auto_save_var.trace_add('write', self.safe_mark_changes)
        auto_save_check = tk.Checkbutton(
            system_inner,
            text="Guardar automáticamente los cambios",
            variable=self.auto_save_var,
            font=('Segoe UI', 11),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        auto_save_check.pack(anchor='w', pady=5)
    
    def create_printer_tab(self):
        """Crear pestaña de configuración de impresora"""
        printer_frame = ttk.Frame(self.notebook)
        self.notebook.add(printer_frame, text="🖨️ Impresora")
        
        # Scroll frame
        canvas = tk.Canvas(printer_frame, bg='white')
        scrollbar = ttk.Scrollbar(printer_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.create_printer_content(scrollable_frame)
    
    def create_printer_content(self, parent):
        """Crear contenido de configuración de impresora"""
        # Título principal
        title_frame = tk.Frame(parent, bg='white')
        title_frame.pack(fill='x', padx=30, pady=(30, 20))
        
        tk.Label(
            title_frame,
            text="🖨️ Configuración de Impresión",
            font=('Segoe UI', 18, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w')
        
        tk.Label(
            title_frame,
            text="Configure las opciones de impresión para recibos, facturas y reportes",
            font=('Segoe UI', 11),
            fg='#7f8c8d',
            bg='white'
        ).pack(anchor='w', pady=(5, 0))
        
        # Frame principal con dos columnas
        main_frame = tk.Frame(parent, bg='white')
        main_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Columna izquierda - Configuración de impresora
        left_column = tk.Frame(main_frame, bg='white')
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        # Impresora por defecto
        printer_section = tk.Frame(left_column, bg='#f8f9fa', relief='solid', bd=1)
        printer_section.pack(fill='x', pady=(0, 20))
        
        printer_inner = tk.Frame(printer_section, bg='#f8f9fa')
        printer_inner.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            printer_inner,
            text="🖨️ Impresora Principal",
            font=('Segoe UI', 14, 'bold'),
            fg='#34495e',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        tk.Label(
            printer_inner,
            text="Seleccione la impresora predeterminada",
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='#f8f9fa'
        ).pack(anchor='w', pady=(5, 15))
        
        tk.Label(
            printer_inner,
            text="Impresora por Defecto:",
            font=('Segoe UI', 12, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        # CREAR COMBOBOX SIN TEXTVARIABLE - APLICAR FIX MANUAL
        printer_combo = ttk.Combobox(
            printer_inner,
            values=self.config_controller.get_available_printers(),
            state='readonly',
            font=('Segoe UI', 11)
        )
        printer_combo.pack(fill='x', pady=(5, 15), ipady=5)
        
        # ESTABLECER VALOR INICIAL DIRECTAMENTE
        initial_printer = self.config_data.get('printer', 'Impresora del sistema')
        printer_combo.set(initial_printer)
        
        # CREAR VARIABLE PARA TRACKING MANUAL
        self.printer_var = tk.StringVar(value=initial_printer)
        
        # SINCRONIZACIÓN MANUAL BIDIRECCIONAL
        def on_printer_change(event):
            """Sincronizar Combobox → Variable"""
            new_value = printer_combo.get()
            self.printer_var.set(new_value)
            self.mark_changes_made()
        
        def on_printer_var_change(*args):
            """Sincronizar Variable → Combobox"""
            new_value = self.printer_var.get()
            if printer_combo.get() != new_value:
                printer_combo.set(new_value)
        
        printer_combo.bind('<<ComboboxSelected>>', on_printer_change)
        self.printer_var.trace_add('write', on_printer_var_change)
        
        # REGISTRO EN MAPA DE WIDGETS MANUALES
        self.widget_var_map[printer_combo] = ('printer', self.printer_var)
        
        print(f"      👀 Combobox creado para printer: valor='{printer_combo.get()}' | ✅ SINCRONIZADO MANUALMENTE")
        
        # Botón para refrescar impresoras
        refresh_button = tk.Button(
            printer_inner,
            text="🔄 Actualizar Lista de Impresoras",
            command=self.refresh_printers,
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 10),
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8
        )
        refresh_button.pack(anchor='w')
        
        # Configuración de formato
        format_section = tk.Frame(left_column, bg='#f8f9fa', relief='solid', bd=1)
        format_section.pack(fill='x')
        
        format_inner = tk.Frame(format_section, bg='#f8f9fa')
        format_inner.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            format_inner,
            text="📄 Formato de Impresión",
            font=('Segoe UI', 14, 'bold'),
            fg='#34495e',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        tk.Label(
            format_inner,
            text="Configure el formato de los documentos",
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='#f8f9fa'
        ).pack(anchor='w', pady=(5, 15))
        
        # Tamaño de papel
        tk.Label(
            format_inner,
            text="Tamaño de Papel:",
            font=('Segoe UI', 12, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        # CREAR COMBOBOX SIN TEXTVARIABLE - APLICAR FIX MANUAL
        paper_combo = ttk.Combobox(
            format_inner,
            values=['A4', 'Carta', 'Recibo (80mm)', 'Recibo (58mm)'],
            state='readonly',
            font=('Segoe UI', 11)
        )
        paper_combo.pack(fill='x', pady=(5, 15), ipady=5)
        
        # ESTABLECER VALOR INICIAL DIRECTAMENTE
        initial_paper = self.config_data.get('paper_size', 'A4')
        paper_combo.set(initial_paper)
        
        # CREAR VARIABLE PARA TRACKING MANUAL
        self.paper_size_var = tk.StringVar(value=initial_paper)
        
        # SINCRONIZACIÓN MANUAL BIDIRECCIONAL
        def on_paper_change(event):
            """Sincronizar Combobox → Variable"""
            new_value = paper_combo.get()
            self.paper_size_var.set(new_value)
            self.mark_changes_made()
        
        def on_paper_var_change(*args):
            """Sincronizar Variable → Combobox"""
            new_value = self.paper_size_var.get()
            if paper_combo.get() != new_value:
                paper_combo.set(new_value)
        
        paper_combo.bind('<<ComboboxSelected>>', on_paper_change)
        self.paper_size_var.trace_add('write', on_paper_var_change)
        
        # REGISTRO EN MAPA DE WIDGETS MANUALES
        self.widget_var_map[paper_combo] = ('paper_size', self.paper_size_var)
        
        print(f"      👀 Combobox creado para paper_size: valor='{paper_combo.get()}' | ✅ SINCRONIZADO MANUALMENTE")
        
        # Número de copias
        tk.Label(
            format_inner,
            text="Número de Copias:",
            font=('Segoe UI', 12, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        # CREAR ENTRY SIN TEXTVARIABLE - APLICAR FIX MANUAL
        copies_entry = tk.Entry(
            format_inner,
            font=('Segoe UI', 12),
            relief='solid',
            bd=1,
            bg='white',
            width=10
        )
        copies_entry.pack(anchor='w', pady=5, ipady=8)
        
        # ESTABLECER VALOR INICIAL DIRECTAMENTE
        initial_copies = self.config_data.get('copies', '1')
        copies_entry.delete(0, 'end')
        copies_entry.insert(0, initial_copies)
        
        # CREAR VARIABLE PARA TRACKING MANUAL
        self.copies_var = tk.StringVar(value=initial_copies)
        
        # SINCRONIZACIÓN MANUAL BIDIRECCIONAL
        def on_copies_change(*args):
            """Sincronizar Entry → Variable"""
            new_value = copies_entry.get()
            self.copies_var.set(new_value)
            self.mark_changes_made()
        
        def on_copies_var_change(*args):
            """Sincronizar Variable → Entry"""
            new_value = self.copies_var.get()
            if copies_entry.get() != new_value:
                copies_entry.delete(0, 'end')
                copies_entry.insert(0, new_value)
        
        copies_entry.bind('<KeyRelease>', on_copies_change)
        copies_entry.bind('<FocusOut>', on_copies_change)
        self.copies_var.trace_add('write', on_copies_var_change)
        
        # REGISTRO EN MAPA DE WIDGETS MANUALES
        self.widget_var_map[copies_entry] = ('copies', self.copies_var)
        
        print(f"      👀 Entry creado para copies: valor='{copies_entry.get()}' | ✅ SINCRONIZADO MANUALMENTE")
        
        # Columna derecha - Configuración de recibo
        right_column = tk.Frame(main_frame, bg='white')
        right_column.pack(side='right', fill='both', expand=True, padx=(15, 0))
        
        # Configuración de recibo
        receipt_section = tk.Frame(right_column, bg='#f8f9fa', relief='solid', bd=1)
        receipt_section.pack(fill='x', pady=(0, 20))
        
        receipt_inner = tk.Frame(receipt_section, bg='#f8f9fa')
        receipt_inner.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            receipt_inner,
            text="🧾 Configuración de Recibos",
            font=('Segoe UI', 14, 'bold'),
            fg='#34495e',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        tk.Label(
            receipt_inner,
            text="Configure qué información incluir en los recibos",
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='#f8f9fa'
        ).pack(anchor='w', pady=(5, 15))
        
        # Opciones de recibo
        self.auto_print_var = tk.BooleanVar(value=self.config_data.get('auto_print', True))
        self.auto_print_var.trace_add('write', self.safe_mark_changes)
        auto_print_check = tk.Checkbutton(
            receipt_inner,
            text="Imprimir recibo automáticamente después de cada venta",
            variable=self.auto_print_var,
            font=('Segoe UI', 11),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        auto_print_check.pack(anchor='w', pady=5)
        
        self.print_logo_var = tk.BooleanVar(value=self.config_data.get('print_logo', True))
        self.print_logo_var.trace_add('write', self.safe_mark_changes)
        print_logo_check = tk.Checkbutton(
            receipt_inner,
            text="Incluir logo de la empresa en el recibo",
            variable=self.print_logo_var,
            font=('Segoe UI', 11),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        print_logo_check.pack(anchor='w', pady=5)
        
        self.print_company_info_var = tk.BooleanVar(value=self.config_data.get('print_company_info', True))
        self.print_company_info_var.trace_add('write', self.safe_mark_changes)
        company_info_check = tk.Checkbutton(
            receipt_inner,
            text="Incluir información completa de la empresa",
            variable=self.print_company_info_var,
            font=('Segoe UI', 11),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        company_info_check.pack(anchor='w', pady=5)
        
        self.print_customer_info_var = tk.BooleanVar(value=self.config_data.get('print_customer_info', False))
        self.print_customer_info_var.trace_add('write', self.safe_mark_changes)
        customer_info_check = tk.Checkbutton(
            receipt_inner,
            text="Incluir información del cliente (si disponible)",
            variable=self.print_customer_info_var,
            font=('Segoe UI', 11),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        customer_info_check.pack(anchor='w', pady=5)
        
        # Configuración avanzada
        advanced_section = tk.Frame(right_column, bg='#f8f9fa', relief='solid', bd=1)
        advanced_section.pack(fill='x')
        
        advanced_inner = tk.Frame(advanced_section, bg='#f8f9fa')
        advanced_inner.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            advanced_inner,
            text="⚙️ Configuración Avanzada",
            font=('Segoe UI', 14, 'bold'),
            fg='#34495e',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        tk.Label(
            advanced_inner,
            text="Opciones avanzadas de impresión",
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='#f8f9fa'
        ).pack(anchor='w', pady=(5, 15))
        
        # Calidad de impresión
        tk.Label(
            advanced_inner,
            text="Calidad de Impresión:",
            font=('Segoe UI', 12, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        # CREAR COMBOBOX SIN TEXTVARIABLE - APLICAR FIX MANUAL
        quality_combo = ttk.Combobox(
            advanced_inner,
            values=['Borrador', 'Normal', 'Alta', 'Máxima'],
            state='readonly',
            font=('Segoe UI', 11)
        )
        quality_combo.pack(fill='x', pady=(5, 15), ipady=5)
        
        # ESTABLECER VALOR INICIAL DIRECTAMENTE
        initial_quality = self.config_data.get('print_quality', 'Normal')
        quality_combo.set(initial_quality)
        
        # CREAR VARIABLE PARA TRACKING MANUAL
        self.print_quality_var = tk.StringVar(value=initial_quality)
        
        # SINCRONIZACIÓN MANUAL BIDIRECCIONAL
        def on_quality_change(event):
            """Sincronizar Combobox → Variable"""
            new_value = quality_combo.get()
            self.print_quality_var.set(new_value)
            self.mark_changes_made()
        
        def on_quality_var_change(*args):
            """Sincronizar Variable → Combobox"""
            new_value = self.print_quality_var.get()
            if quality_combo.get() != new_value:
                quality_combo.set(new_value)
        
        quality_combo.bind('<<ComboboxSelected>>', on_quality_change)
        self.print_quality_var.trace_add('write', on_quality_var_change)
        
        # REGISTRO EN MAPA DE WIDGETS MANUALES
        self.widget_var_map[quality_combo] = ('print_quality', self.print_quality_var)
        
        print(f"      👀 Combobox creado para print_quality: valor='{quality_combo.get()}' | ✅ SINCRONIZADO MANUALMENTE")
        
        # Opciones adicionales
        self.print_barcode_var = tk.BooleanVar(value=self.config_data.get('print_barcode', False))
        self.print_barcode_var.trace_add('write', self.safe_mark_changes)
        barcode_check = tk.Checkbutton(
            advanced_inner,
            text="Incluir código de barras en recibos",
            variable=self.print_barcode_var,
            font=('Segoe UI', 11),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        barcode_check.pack(anchor='w', pady=5)
        
        self.save_pdf_copy_var = tk.BooleanVar(value=self.config_data.get('save_pdf_copy', False))
        self.save_pdf_copy_var.trace_add('write', self.safe_mark_changes)
        pdf_check = tk.Checkbutton(
            advanced_inner,
            text="Guardar copia en PDF automáticamente",
            variable=self.save_pdf_copy_var,
            font=('Segoe UI', 11),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        pdf_check.pack(anchor='w', pady=5)
    
    def refresh_printers(self):
        """Actualizar lista de impresoras disponibles"""
        try:
            printers = self.config_controller.get_available_printers()
            # Actualizar el combobox con la nueva lista
            # Nota: Esto requeriría mantener una referencia al combobox
            messagebox.showinfo("Impresoras", f"Lista actualizada. {len(printers)} impresoras encontradas.")
        except Exception as e:
            messagebox.showerror("Error", f"Error actualizando impresoras:\n{str(e)}")
    
    def create_database_tab(self):
        """Crear pestaña de configuración de base de datos"""
        db_frame = ttk.Frame(self.notebook)
        self.notebook.add(db_frame, text="🗄️ Base de Datos")
        
        # Scroll frame
        canvas = tk.Canvas(db_frame, bg='white')
        scrollbar = ttk.Scrollbar(db_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.create_database_content(scrollable_frame)
    
    def create_database_content(self, parent):
        """Crear contenido de configuración de base de datos"""
        # Título principal
        title_frame = tk.Frame(parent, bg='white')
        title_frame.pack(fill='x', padx=30, pady=(30, 20))
        
        tk.Label(
            title_frame,
            text="🗄️ Configuración de Base de Datos",
            font=('Segoe UI', 18, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).pack(anchor='w')
        
        tk.Label(
            title_frame,
            text="Configure la conexión a la base de datos del sistema",
            font=('Segoe UI', 11),
            fg='#7f8c8d',
            bg='white'
        ).pack(anchor='w', pady=(5, 0))
        
        # Advertencia
        warning_frame = tk.Frame(parent, bg='#fff3cd', relief='solid', bd=2)
        warning_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        warning_inner = tk.Frame(warning_frame, bg='#fff3cd')
        warning_inner.pack(fill='x', padx=20, pady=15)
        
        tk.Label(
            warning_inner,
            text="⚠️ IMPORTANTE",
            font=('Segoe UI', 12, 'bold'),
            fg='#856404',
            bg='#fff3cd'
        ).pack(anchor='w')
        
        warning_label = tk.Label(
            warning_inner,
            text="Cambiar la configuración de base de datos puede afectar el funcionamiento del sistema.\nSolo modifique estos valores si tiene conocimientos técnicos y sabe lo que está haciendo.\nSiempre haga un backup antes de realizar cambios.",
            font=('Segoe UI', 10),
            fg='#856404',
            bg='#fff3cd',
            justify='left'
        )
        warning_label.pack(anchor='w', pady=(5, 0))
        
        # Frame principal con dos columnas
        main_frame = tk.Frame(parent, bg='white')
        main_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Columna izquierda - Estado y pruebas
        left_column = tk.Frame(main_frame, bg='white')
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        # Estado de la conexión
        status_section = tk.Frame(left_column, bg='#f8f9fa', relief='solid', bd=1)
        status_section.pack(fill='x', pady=(0, 20))
        
        status_inner = tk.Frame(status_section, bg='#f8f9fa')
        status_inner.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            status_inner,
            text="📊 Estado de la Conexión",
            font=('Segoe UI', 14, 'bold'),
            fg='#34495e',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        tk.Label(
            status_inner,
            text="Estado actual de la conexión a la base de datos",
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='#f8f9fa'
        ).pack(anchor='w', pady=(5, 15))
        
        self.db_status_label = tk.Label(
            status_inner,
            text="🟢 Conectado a MySQL Server",
            font=('Segoe UI', 13, 'bold'),
            fg='#27ae60',
            bg='#f8f9fa'
        )
        self.db_status_label.pack(anchor='w', pady=(0, 15))
        
        # Botones de prueba
        buttons_frame = tk.Frame(status_inner, bg='#f8f9fa')
        buttons_frame.pack(fill='x')
        
        test_button = tk.Button(
            buttons_frame,
            text="🔍 Probar Conexión",
            command=self.test_database_connection,
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8
        )
        test_button.pack(side='left', padx=(0, 10))
        
        info_button = tk.Button(
            buttons_frame,
            text="ℹ️ Información DB",
            command=self.show_database_info,
            bg='#9b59b6',
            fg='white',
            font=('Segoe UI', 11),
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8
        )
        info_button.pack(side='left')
        
        # Configuración de rendimiento
        performance_section = tk.Frame(left_column, bg='#f8f9fa', relief='solid', bd=1)
        performance_section.pack(fill='x')
        
        performance_inner = tk.Frame(performance_section, bg='#f8f9fa')
        performance_inner.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            performance_inner,
            text="⚡ Configuración de Rendimiento",
            font=('Segoe UI', 14, 'bold'),
            fg='#34495e',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        tk.Label(
            performance_inner,
            text="Opciones para optimizar el rendimiento",
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='#f8f9fa'
        ).pack(anchor='w', pady=(5, 15))
        
        # Pool de conexiones
        tk.Label(
            performance_inner,
            text="Máximo de Conexiones:",
            font=('Segoe UI', 12, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        self.db_max_connections_var = tk.StringVar(value=self.config_data.get('db_max_connections', '10'))
        self.db_max_connections_var.trace_add('write', self.safe_mark_changes)
        max_conn_entry = tk.Entry(
            performance_inner,
            textvariable=self.db_max_connections_var,
            font=('Segoe UI', 12),
            relief='solid',
            bd=1,
            bg='white',
            width=10
        )
        max_conn_entry.pack(anchor='w', pady=(5, 15), ipady=8)
        
        # Timeout
        tk.Label(
            performance_inner,
            text="Timeout de Conexión (segundos):",
            font=('Segoe UI', 12, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        self.db_timeout_var = tk.StringVar(value=self.config_data.get('db_timeout', '30'))
        self.db_timeout_var.trace_add('write', self.safe_mark_changes)
        timeout_entry = tk.Entry(
            performance_inner,
            textvariable=self.db_timeout_var,
            font=('Segoe UI', 12),
            relief='solid',
            bd=1,
            bg='white',
            width=10
        )
        timeout_entry.pack(anchor='w', pady=5, ipady=8)
        
        # Columna derecha - Configuración de conexión
        right_column = tk.Frame(main_frame, bg='white')
        right_column.pack(side='right', fill='both', expand=True, padx=(15, 0))
        
        # Configuración de conexión
        conn_section = tk.Frame(right_column, bg='#f8f9fa', relief='solid', bd=1)
        conn_section.pack(fill='x')
        
        conn_inner = tk.Frame(conn_section, bg='#f8f9fa')
        conn_inner.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            conn_inner,
            text="🔗 Parámetros de Conexión",
            font=('Segoe UI', 14, 'bold'),
            fg='#34495e',
            bg='#f8f9fa'
        ).pack(anchor='w')
        
        tk.Label(
            conn_inner,
            text="Configure los parámetros de conexión a MySQL",
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='#f8f9fa'
        ).pack(anchor='w', pady=(5, 15))
        
        # Cargar configuración actual de BD
        self.load_database_config()
        
        # Campos de configuración de BD
        db_fields = [
            ("🖥️ Servidor/Host:", "db_host", "localhost", "Dirección del servidor de base de datos"),
            ("🔌 Puerto:", "db_port", "3306", "Puerto de conexión (por defecto: 3306)"),
            ("🗄️ Base de Datos:", "db_name", "pos_system", "Nombre de la base de datos"),
            ("👤 Usuario:", "db_user", "root", "Usuario de la base de datos"),
            ("🔒 Contraseña:", "db_password", "", "Contraseña del usuario", True)  # True indica que es password
        ]
        
        self.db_vars = {}
        for field_name, var_name, default_value, description, *is_password in db_fields:
            is_pwd = is_password and is_password[0]
            
            # Crear frame para cada campo
            field_frame = tk.Frame(conn_inner, bg='#f8f9fa')
            field_frame.pack(fill='x', pady=8)
            
            tk.Label(
                field_frame,
                text=field_name,
                font=('Segoe UI', 12, 'bold'),
                fg='#2c3e50',
                bg='#f8f9fa'
            ).pack(anchor='w')
            
            # CREAR ENTRY SIN TEXTVARIABLE - APLICAR FIX MANUAL
            entry = tk.Entry(
                field_frame,
                font=('Segoe UI', 12),
                show='*' if is_pwd else None,
                relief='solid',
                bd=1,
                bg='white',
                fg='#2c3e50',
                insertbackground='#3498db'
            )
            entry.pack(fill='x', pady=(5, 8), ipady=8)
            
            # ESTABLECER VALOR INICIAL DIRECTAMENTE
            initial_value = self.config_data.get(var_name, default_value)
            entry.delete(0, 'end')
            entry.insert(0, initial_value)
            
            # CREAR VARIABLE PARA TRACKING MANUAL
            self.db_vars[var_name] = tk.StringVar(value=initial_value)
            
            # SINCRONIZACIÓN MANUAL BIDIRECCIONAL (con closure para capturar var_name)
            def create_db_callbacks(entry_widget, var_name_captured, var_obj):
                def on_entry_change(*args):
                    """Sincronizar Entry → Variable"""
                    new_value = entry_widget.get()
                    var_obj.set(new_value)
                    self.mark_changes_made()
                
                def on_var_change(*args):
                    """Sincronizar Variable → Entry"""
                    new_value = var_obj.get()
                    if entry_widget.get() != new_value:
                        entry_widget.delete(0, 'end')
                        entry_widget.insert(0, new_value)
                
                return on_entry_change, on_var_change
            
            # Crear callbacks específicos para este campo
            entry_cb, var_cb = create_db_callbacks(entry, var_name, self.db_vars[var_name])
            
            entry.bind('<KeyRelease>', entry_cb)
            entry.bind('<FocusOut>', entry_cb)
            self.db_vars[var_name].trace_add('write', var_cb)
            
            # REGISTRO EN MAPA DE WIDGETS MANUALES
            self.widget_var_map[entry] = (var_name, self.db_vars[var_name])
            
            print(f"      👀 Entry DB creado para {var_name}: valor='{entry.get()}' | ✅ SINCRONIZADO MANUALMENTE")
            
            # Descripción
            tk.Label(
                field_frame,
                text=description,
                font=('Segoe UI', 10),
                fg='#7f8c8d',
                bg='#f8f9fa'
            ).pack(anchor='w')
    
    def show_database_info(self):
        """Mostrar información de la base de datos"""
        try:
            info = self.config_controller.get_database_info()
            info_text = f"""
Información de la Base de Datos:

🏷️ Nombre: {info.get('database', 'No disponible')}
📊 Versión: {info.get('version', 'No disponible')}
📅 Última conexión: {info.get('last_connection', 'No disponible')}
📈 Tablas: {info.get('tables_count', 'No disponible')}
💾 Tamaño: {info.get('size', 'No disponible')}

Estado: {'🟢 Operativa' if info.get('status') == 'OK' else '🔴 Con problemas'}
            """
            messagebox.showinfo("Información de la Base de Datos", info_text.strip())
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener la información:\n{str(e)}")
    
    def create_security_tab(self):
        """Crear pestaña de configuración de seguridad"""
        security_frame = ttk.Frame(self.notebook)
        self.notebook.add(security_frame, text="🔒 Seguridad")
        
        content_frame = tk.Frame(security_frame, bg='white')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Configuración de sesión
        session_frame = tk.LabelFrame(content_frame, text="👤 Configuración de Sesión", font=('Segoe UI', 12, 'bold'))
        session_frame.pack(fill='x', pady=10)
        
        session_inner = tk.Frame(session_frame, bg='white')
        session_inner.pack(fill='x', padx=15, pady=15)
        
        # Tiempo de sesión
        tk.Label(
            session_inner,
            text="Tiempo máximo de sesión (minutos):",
            font=('Segoe UI', 11, 'bold'),
            bg='white'
        ).pack(anchor='w')
        
        # CREAR ENTRY SIN TEXTVARIABLE - APLICAR FIX MANUAL
        session_entry = tk.Entry(
            session_inner,
            font=('Segoe UI', 11),
            width=10
        )
        session_entry.pack(anchor='w', pady=5)
        
        # ESTABLECER VALOR INICIAL DIRECTAMENTE
        initial_timeout = self.config_data.get('session_timeout', '480')
        session_entry.delete(0, 'end')
        session_entry.insert(0, initial_timeout)
        
        # CREAR VARIABLE PARA TRACKING MANUAL
        self.session_timeout_var = tk.StringVar(value=initial_timeout)
        
        # SINCRONIZACIÓN MANUAL BIDIRECCIONAL
        def on_timeout_change(*args):
            """Sincronizar Entry → Variable"""
            new_value = session_entry.get()
            self.session_timeout_var.set(new_value)
            self.mark_changes_made()
        
        def on_timeout_var_change(*args):
            """Sincronizar Variable → Entry"""
            new_value = self.session_timeout_var.get()
            if session_entry.get() != new_value:
                session_entry.delete(0, 'end')
                session_entry.insert(0, new_value)
        
        session_entry.bind('<KeyRelease>', on_timeout_change)
        session_entry.bind('<FocusOut>', on_timeout_change)
        self.session_timeout_var.trace_add('write', on_timeout_var_change)
        
        # REGISTRO EN MAPA DE WIDGETS MANUALES
        self.widget_var_map[session_entry] = ('session_timeout', self.session_timeout_var)
        
        print(f"      👀 Entry creado para session_timeout: valor='{session_entry.get()}' | ✅ SINCRONIZADO MANUALMENTE")
        
        # Auto logout
        self.auto_logout_var = tk.BooleanVar(value=self.config_data.get('auto_logout', True))
        auto_logout_check = tk.Checkbutton(
            session_inner,
            text="Cerrar sesión automáticamente por inactividad",
            variable=self.auto_logout_var,
            font=('Segoe UI', 10),
            bg='white'
        )
        auto_logout_check.pack(anchor='w', pady=5)
        
        # Configuración de contraseñas
        password_frame = tk.LabelFrame(content_frame, text="🔐 Configuración de Contraseñas", font=('Segoe UI', 12, 'bold'))
        password_frame.pack(fill='x', pady=10)
        
        password_inner = tk.Frame(password_frame, bg='white')
        password_inner.pack(fill='x', padx=15, pady=15)
        
        # Longitud mínima
        tk.Label(
            password_inner,
            text="Longitud mínima de contraseña:",
            font=('Segoe UI', 11, 'bold'),
            bg='white'
        ).pack(anchor='w')
        
        # CREAR ENTRY SIN TEXTVARIABLE - APLICAR FIX MANUAL
        password_length_entry = tk.Entry(
            password_inner,
            font=('Segoe UI', 11),
            width=10
        )
        password_length_entry.pack(anchor='w', pady=5)
        
        # ESTABLECER VALOR INICIAL DIRECTAMENTE
        initial_pwd_length = self.config_data.get('min_password_length', '6')
        password_length_entry.delete(0, 'end')
        password_length_entry.insert(0, initial_pwd_length)
        
        # CREAR VARIABLE PARA TRACKING MANUAL
        self.min_password_length_var = tk.StringVar(value=initial_pwd_length)
        
        # SINCRONIZACIÓN MANUAL BIDIRECCIONAL
        def on_pwd_length_change(*args):
            """Sincronizar Entry → Variable"""
            new_value = password_length_entry.get()
            self.min_password_length_var.set(new_value)
            self.mark_changes_made()
        
        def on_pwd_length_var_change(*args):
            """Sincronizar Variable → Entry"""
            new_value = self.min_password_length_var.get()
            if password_length_entry.get() != new_value:
                password_length_entry.delete(0, 'end')
                password_length_entry.insert(0, new_value)
        
        password_length_entry.bind('<KeyRelease>', on_pwd_length_change)
        password_length_entry.bind('<FocusOut>', on_pwd_length_change)
        self.min_password_length_var.trace_add('write', on_pwd_length_var_change)
        
        # REGISTRO EN MAPA DE WIDGETS MANUALES
        self.widget_var_map[password_length_entry] = ('min_password_length', self.min_password_length_var)
        
        print(f"      👀 Entry creado para min_password_length: valor='{password_length_entry.get()}' | ✅ SINCRONIZADO MANUALMENTE")
        
        # Requerir caracteres especiales
        self.require_special_chars_var = tk.BooleanVar(value=self.config_data.get('require_special_chars', False))
        special_chars_check = tk.Checkbutton(
            password_inner,
            text="Requerir caracteres especiales en contraseñas",
            variable=self.require_special_chars_var,
            font=('Segoe UI', 10),
            bg='white'
        )
        special_chars_check.pack(anchor='w', pady=5)
    
    def create_backup_tab(self):
        """Crear pestaña de configuración de backup"""
        backup_frame = ttk.Frame(self.notebook)
        self.notebook.add(backup_frame, text="💾 Backup")
        
        content_frame = tk.Frame(backup_frame, bg='white')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Backup automático
        auto_backup_frame = tk.LabelFrame(content_frame, text="⏰ Backup Automático", font=('Segoe UI', 12, 'bold'))
        auto_backup_frame.pack(fill='x', pady=10)
        
        auto_backup_inner = tk.Frame(auto_backup_frame, bg='white')
        auto_backup_inner.pack(fill='x', padx=15, pady=15)
        
        # Habilitar backup automático
        self.auto_backup_var = tk.BooleanVar(value=self.config_data.get('auto_backup', True))
        auto_backup_check = tk.Checkbutton(
            auto_backup_inner,
            text="Habilitar backup automático",
            variable=self.auto_backup_var,
            font=('Segoe UI', 11, 'bold'),
            bg='white'
        )
        auto_backup_check.pack(anchor='w', pady=5)
        
        # Frecuencia
        tk.Label(
            auto_backup_inner,
            text="Frecuencia:",
            font=('Segoe UI', 11, 'bold'),
            bg='white'
        ).pack(anchor='w', pady=(10, 0))
        
        # CREAR COMBOBOX SIN TEXTVARIABLE - APLICAR FIX MANUAL
        frequency_combo = ttk.Combobox(
            auto_backup_inner,
            values=['Cada hora', 'Diario', 'Semanal', 'Mensual'],
            state='readonly'
        )
        frequency_combo.pack(fill='x', pady=5)
        
        # ESTABLECER VALOR INICIAL DIRECTAMENTE
        initial_frequency = self.config_data.get('backup_frequency', 'Diario')
        frequency_combo.set(initial_frequency)
        
        # CREAR VARIABLE PARA TRACKING MANUAL
        self.backup_frequency_var = tk.StringVar(value=initial_frequency)
        
        # SINCRONIZACIÓN MANUAL BIDIRECCIONAL
        def on_frequency_change(event):
            """Sincronizar Combobox → Variable"""
            new_value = frequency_combo.get()
            self.backup_frequency_var.set(new_value)
            self.mark_changes_made()
        
        def on_frequency_var_change(*args):
            """Sincronizar Variable → Combobox"""
            new_value = self.backup_frequency_var.get()
            if frequency_combo.get() != new_value:
                frequency_combo.set(new_value)
        
        frequency_combo.bind('<<ComboboxSelected>>', on_frequency_change)
        self.backup_frequency_var.trace_add('write', on_frequency_var_change)
        
        # REGISTRO EN MAPA DE WIDGETS MANUALES
        self.widget_var_map[frequency_combo] = ('backup_frequency', self.backup_frequency_var)
        
        print(f"      👀 Combobox creado para backup_frequency: valor='{frequency_combo.get()}' | ✅ SINCRONIZADO MANUALMENTE")
        
        # Carpeta de backup
        tk.Label(
            auto_backup_inner,
            text="Carpeta de backup:",
            font=('Segoe UI', 11, 'bold'),
            bg='white'
        ).pack(anchor='w', pady=(10, 0))
        
        backup_path_frame = tk.Frame(auto_backup_inner, bg='white')
        backup_path_frame.pack(fill='x', pady=5)
        
        # CREAR ENTRY SIN TEXTVARIABLE - APLICAR FIX MANUAL
        backup_path_entry = tk.Entry(
            backup_path_frame,
            font=('Segoe UI', 11)
        )
        backup_path_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        # ESTABLECER VALOR INICIAL DIRECTAMENTE
        initial_backup_path = self.config_data.get('backup_path', './backups')
        backup_path_entry.delete(0, 'end')
        backup_path_entry.insert(0, initial_backup_path)
        
        # CREAR VARIABLE PARA TRACKING MANUAL
        self.backup_path_var = tk.StringVar(value=initial_backup_path)
        
        # SINCRONIZACIÓN MANUAL BIDIRECCIONAL
        def on_backup_path_change(*args):
            """Sincronizar Entry → Variable"""
            new_value = backup_path_entry.get()
            self.backup_path_var.set(new_value)
            self.mark_changes_made()
        
        def on_backup_path_var_change(*args):
            """Sincronizar Variable → Entry"""
            new_value = self.backup_path_var.get()
            if backup_path_entry.get() != new_value:
                backup_path_entry.delete(0, 'end')
                backup_path_entry.insert(0, new_value)
        
        backup_path_entry.bind('<KeyRelease>', on_backup_path_change)
        backup_path_entry.bind('<FocusOut>', on_backup_path_change)
        self.backup_path_var.trace_add('write', on_backup_path_var_change)
        
        # REGISTRO EN MAPA DE WIDGETS MANUALES
        self.widget_var_map[backup_path_entry] = ('backup_path', self.backup_path_var)
        
        print(f"      👀 Entry creado para backup_path: valor='{backup_path_entry.get()}' | ✅ SINCRONIZADO MANUALMENTE")
        
        browse_button = tk.Button(
            backup_path_frame,
            text="📁 Examinar",
            command=self.select_backup_folder,
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 10),
            relief='flat',
            cursor='hand2'
        )
        browse_button.pack(side='right')
        
        # Backup manual
        manual_backup_frame = tk.LabelFrame(content_frame, text="🔧 Backup Manual", font=('Segoe UI', 12, 'bold'))
        manual_backup_frame.pack(fill='x', pady=10)
        
        manual_backup_inner = tk.Frame(manual_backup_frame, bg='white')
        manual_backup_inner.pack(fill='x', padx=15, pady=15)
        
        tk.Label(
            manual_backup_inner,
            text="Crear una copia de seguridad inmediata de la base de datos:",
            font=('Segoe UI', 11),
            bg='white'
        ).pack(anchor='w', pady=(0, 10))
        
        backup_buttons_frame = tk.Frame(manual_backup_inner, bg='white')
        backup_buttons_frame.pack(fill='x')
        
        create_backup_button = tk.Button(
            backup_buttons_frame,
            text="💾 Crear Backup",
            command=self.create_manual_backup,
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            cursor='hand2',
            width=15
        )
        create_backup_button.pack(side='left', padx=(0, 10))
        
        restore_backup_button = tk.Button(
            backup_buttons_frame,
            text="📥 Restaurar Backup",
            command=self.restore_backup,
            bg='#e74c3c',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            cursor='hand2',
            width=15
        )
        restore_backup_button.pack(side='left')
        
        # Último backup
        tk.Label(
            manual_backup_inner,
            text="Último backup realizado: No disponible",
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='white'
        ).pack(anchor='w', pady=(20, 0))
    
    def create_action_buttons(self):
        """Crear botones de acción"""
        buttons_frame = tk.Frame(self.root, bg='#f8f9fa', height=60)
        buttons_frame.pack(fill='x', side='bottom')
        buttons_frame.pack_propagate(False)
        
        inner_frame = tk.Frame(buttons_frame, bg='#f8f9fa')
        inner_frame.pack(expand=True, fill='both', padx=20, pady=15)
        
        # Botón cancelar/volver
        if self.embedded:
            cancel_button = tk.Button(
                inner_frame,
                text="← Volver",
                command=self.go_back_to_dashboard,
                bg='#95a5a6',
                fg='white',
                font=('Segoe UI', 11, 'bold'),
                relief='flat',
                cursor='hand2',
                width=12
            )
        else:
            cancel_button = tk.Button(
                inner_frame,
                text="❌ Cancelar",
                command=self.cancel_changes,
                bg='#95a5a6',
                fg='white',
                font=('Segoe UI', 11, 'bold'),
                relief='flat',
                cursor='hand2',
                width=12
            )
        cancel_button.pack(side='left')
        
        # Botón restaurar
        restore_button = tk.Button(
            inner_frame,
            text="🔄 Restaurar",
            command=self.restore_defaults,
            bg='#f39c12',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            cursor='hand2',
            width=12
        )
        restore_button.pack(side='left', padx=10)
        
        # Botón exportar
        export_button = tk.Button(
            inner_frame,
            text="📤 Exportar",
            command=self.export_configuration,
            bg='#9b59b6',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            cursor='hand2',
            width=12
        )
        export_button.pack(side='left', padx=5)
        
        # Botón importar
        import_button = tk.Button(
            inner_frame,
            text="📥 Importar",
            command=self.import_configuration,
            bg='#34495e',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            cursor='hand2',
            width=12
        )
        import_button.pack(side='left', padx=5)
        
        # Botón guardar
        save_button = tk.Button(
            inner_frame,
            text="💾 Guardar Cambios",
            command=self.save_configuration,
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            cursor='hand2',
            width=15
        )
        save_button.pack(side='right')
        
        # Botón aplicar
        apply_button = tk.Button(
            inner_frame,
            text="✅ Aplicar",
            command=self.apply_configuration,
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            cursor='hand2',
            width=12
        )
        apply_button.pack(side='right', padx=(0, 10))
    
    def create_config_field(self, parent, label_text, var_name, placeholder, description):
        """Crear campo de configuración genérico"""
        field_frame = tk.Frame(parent, bg='white')
        field_frame.pack(fill='x', pady=8)
        
        # Label
        label = tk.Label(
            field_frame,
            text=label_text,
            font=('Segoe UI', 11, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        label.pack(anchor='w')
        
        # Entry
        if not hasattr(self, f'{var_name}_var'):
            setattr(self, f'{var_name}_var', tk.StringVar(value=self.config_data.get(var_name, placeholder)))
        
        var = getattr(self, f'{var_name}_var')
        var.trace_add('write', lambda *args: self.safe_mark_changes())
        
        entry = tk.Entry(
            field_frame,
            textvariable=var,
            font=('Segoe UI', 11),
            relief='solid',
            bd=1
        )
        entry.pack(fill='x', pady=2)
        
        # Description
        desc_label = tk.Label(
            field_frame,
            text=description,
            font=('Segoe UI', 9),
            fg='#7f8c8d',
            bg='white'
        )
        desc_label.pack(anchor='w')
    
    def create_config_field_improved(self, parent, label_text, var_name, placeholder, description):
        """Crear campo de configuración mejorado con mejor diseño"""
        field_frame = tk.Frame(parent, bg='white')
        field_frame.pack(fill='x', pady=12)
        
        # Label con icono
        label = tk.Label(
            field_frame,
            text=label_text,
            font=('Segoe UI', 12, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        label.pack(anchor='w')
        
        # Entry mejorado - usar datos cargados si existen
        initial_value = self.config_data.get(var_name, placeholder)
        print(f"   🔧 Creando campo {var_name} con valor: '{initial_value}' (desde config_data)")
        
        # CREAR ENTRY SIN TEXTVARIABLE - INSERTAR VALOR DIRECTAMENTE
        entry = tk.Entry(
            field_frame,
            font=('Segoe UI', 12),
            relief='solid',
            bd=1,
            bg='white',
            fg='#2c3e50',
            insertbackground='#3498db',
            selectbackground='#3498db',
            selectforeground='white'
        )
        entry.pack(fill='x', pady=(5, 8), ipady=8)
        
        # INSERTAR VALOR DIRECTAMENTE EN EL ENTRY
        entry.delete(0, tk.END)
        entry.insert(0, initial_value)
        
        # CREAR VARIABLE PARA TRACKING MANUAL
        if not hasattr(self, f'{var_name}_var'):
            var = tk.StringVar(value=initial_value)
            setattr(self, f'{var_name}_var', var)
            print(f"      ✅ Variable creada: {var_name}_var = '{var.get()}' (ID: {id(var)})")
        else:
            var = getattr(self, f'{var_name}_var')
            var.set(initial_value)
            print(f"      🔄 Variable actualizada: {var_name}_var = '{var.get()}' (ID: {id(var)})")
        
        # CREAR REFERENCIA ENTRY-VARIABLE MANUAL
        if not hasattr(self, 'entry_var_map'):
            self.entry_var_map = {}
        self.entry_var_map[entry] = (var_name, var)
        
        # AGREGAR CALLBACKS PARA SINCRONIZAR
        def on_entry_change(event):
            """Sincronizar Entry → Variable"""
            new_value = entry.get()
            var.set(new_value)
            self.safe_mark_changes()
        
        def on_var_change(*args):
            """Sincronizar Variable → Entry"""
            new_value = var.get()
            if entry.get() != new_value:
                entry.delete(0, tk.END)
                entry.insert(0, new_value)
        
        entry.bind('<KeyRelease>', on_entry_change)
        entry.bind('<FocusOut>', on_entry_change)
        var.trace_add('write', on_var_change)
        
        print(f"      👀 Entry creado para {var_name}: valor='{entry.get()}' | ✅ SINCRONIZADO MANUALMENTE")
        print(f"         Entry widget ID: {id(entry)} | Variable ID: {id(var)}")
        
        # Description mejorada
        desc_label = tk.Label(
            field_frame,
            text=description,
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='white',
            wraplength=300,
            justify='left'
        )
        desc_label.pack(anchor='w')
    
    def clear_company_logo(self):
        """Quitar logo de la empresa"""
        self.logo_path_var.set('No se ha seleccionado ningún logo')
        self.config_data['company_logo'] = ''
        self.mark_changes_made()
    
    def load_configuration(self):
        """Cargar configuración actual"""
        try:
            print("🔄 Cargando configuración desde archivos...")
            self.config_data = self.config_controller.load_configuration()
            print(f"📊 Configuración cargada: {len(self.config_data)} elementos")
            
            # Mostrar algunos datos cargados para debug
            key_fields = ['company_name', 'currency', 'theme', 'db_host', 'db_name']
            for field in key_fields:
                if field in self.config_data:
                    print(f"   • {field}: {self.config_data[field]}")
            
            # NO llamar update_ui_with_config aquí - se hará después de crear la interfaz
            
        except Exception as e:
            print(f"❌ Error cargando configuración: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error cargando configuración:\n{str(e)}")
            self.config_data = self.config_controller.get_default_configuration()
    
    def load_database_config(self):
        """Cargar configuración de base de datos"""
        try:
            # Usar PathManager para cargar configuración
            from utils.path_manager import load_config
            db_config = load_config('database.json')
            if db_config:
                self.config_data.update(db_config)
        except Exception as e:
            print(f"Error cargando configuración de BD: {e}")
    
    def get_default_config(self):
        """Obtener configuración por defecto"""
        return {
            'company_name': 'Mi Negocio POS',
            'company_rut': '',
            'company_address': '',
            'company_phone': '',
            'company_email': '',
            'company_website': '',
            'company_logo': '',
            'currency': 'CLP',
            'currency_symbol': 'S/',
            'tax_rate': '19',
            'include_tax_in_price': True,
            'theme': 'Claro',
            'language': 'Español',
            'default_printer': 'Impresora del sistema',
            'auto_print_receipt': True,
            'print_logo': True,
            'receipt_copies': '1',
            'session_timeout': '480',
            'auto_logout': True,
            'min_password_length': '6',
            'require_special_chars': False,
            'auto_backup_enabled': True,
            'backup_frequency': 'Diario',
            'backup_path': './backups'
        }
    
    def select_company_logo(self):
        """Seleccionar logo de la empresa"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar Logo de la Empresa",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("Todos los archivos", "*.*")
            ]
        )
        if file_path:
            # Actualizar la variable de UI con el path completo
            self.logo_path_var.set(file_path)
            # Guardar el path real en config_data
            self.config_data['logo_path'] = file_path
            self.mark_changes_made()
            print(f"🖼️ Logo seleccionado: {file_path}")
    
    def select_backup_folder(self):
        """Seleccionar carpeta de backup"""
        folder_path = filedialog.askdirectory(title="Seleccionar Carpeta de Backup")
        if folder_path:
            self.backup_path_var.set(folder_path)
            self.mark_changes_made()
    
    def test_database_connection(self):
        """Probar conexión a la base de datos"""
        try:
            # Obtener configuración actual de BD
            db_config = {}
            if hasattr(self, 'db_vars'):
                db_config = {k: v.get() for k, v in self.db_vars.items()}
            
            # Probar conexión usando el controlador
            success, message = self.config_controller.test_database_connection(db_config)
            
            if success:
                self.db_status_label.configure(
                    text="🟢 Conexión exitosa",
                    fg='#27ae60'
                )
                messagebox.showinfo("Conexión", f"✅ {message}")
            else:
                self.db_status_label.configure(
                    text="🔴 Error de conexión",
                    fg='#e74c3c'
                )
                messagebox.showerror("Error de Conexión", f"❌ {message}")
                
        except Exception as e:
            self.db_status_label.configure(
                text="🔴 Error de conexión",
                fg='#e74c3c'
            )
            messagebox.showerror("Error de Conexión", f"❌ Error inesperado:\n{str(e)}")
    
    def create_manual_backup(self):
        """Crear backup manual"""
        try:
            success, message = self.config_controller.create_backup()
            if success:
                messagebox.showinfo("Backup", f"✅ {message}")
            else:
                messagebox.showerror("Error", f"❌ {message}")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error creando backup:\n{str(e)}")
    
    def restore_backup(self):
        """Restaurar desde backup"""
        if messagebox.askyesno("Confirmar Restauración", 
                               "⚠️ ¿Está seguro de que desea restaurar desde un backup?\n\n"
                               "Esta acción sobrescribirá todos los datos actuales."):
            file_path = filedialog.askopenfilename(
                title="Seleccionar Archivo de Backup",
                filetypes=[("SQL", "*.sql"), ("Todos los archivos", "*.*")]
            )
            if file_path:
                try:
                    success, message = self.config_controller.restore_backup(file_path)
                    if success:
                        messagebox.showinfo("Restauración", f"✅ {message}")
                    else:
                        messagebox.showerror("Error", f"❌ {message}")
                except Exception as e:
                    messagebox.showerror("Error", f"❌ Error restaurando backup:\n{str(e)}")
    
    def save_configuration(self):
        """Guardar configuración"""
        print(f"\n🔧 INICIANDO SAVE_CONFIGURATION - changes_made: {self.changes_made}")
        
        # Activar flag de guardado para evitar cambios durante el proceso
        self.saving_data = True
        print(f"🔒 ACTIVADO saving_data - No se marcarán cambios durante el guardado")
        
        try:
            # Obtener configuración actual para comparación
            old_config = self.config_data.copy()
            
            # Recopilar todos los valores de las variables
            config_to_save = self.collect_config_data()
            
            # Verificar si requiere reinicio
            needs_restart, changed_field = self.requires_restart(old_config, config_to_save)
            
            # Validar configuración
            is_valid, errors = self.config_controller.validate_configuration(config_to_save)
            if not is_valid:
                messagebox.showerror("Error de Validación", 
                                   f"❌ Errores en la configuración:\n\n" + "\n".join(f"• {error}" for error in errors))
                return
            
            # Guardar usando el controlador
            if self.config_controller.save_configuration(config_to_save):
                print(f"💾 GUARDADO EXITOSO - RESETEANDO changes_made: {self.changes_made} → False")
                self.changes_made = False
                
                # Mostrar mensaje apropiado según si requiere reinicio
                if needs_restart:
                    field_names = {
                        'company_name': 'nombre de la empresa',
                        'logo_path': 'imagen del logo'
                    }
                    field_desc = field_names.get(changed_field, 'configuración')
                    
                    messagebox.showwarning("Reinicio Requerido", 
                                         f"✅ Configuración guardada exitosamente.\n\n"
                                         f"⚠️ IMPORTANTE: Has cambiado el {field_desc}.\n"
                                         f"Para que este cambio se aplique completamente,\n"
                                         f"necesitas reiniciar la aplicación.")
                else:
                    messagebox.showinfo("Configuración", "✅ Configuración guardada exitosamente")
                
                # Emitir callback de configuración guardada (para actualizar login si es necesario)
                self.trigger_callback('configuration_saved', config_to_save)
                
                print(f"💾 DESPUÉS DEL CALLBACK - changes_made: {self.changes_made}")
            else:
                messagebox.showerror("Error", "❌ Error guardando la configuración")
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error guardando configuración:\n{str(e)}")
    
    def apply_configuration(self):
        """Aplicar configuración sin cerrar ventana"""
        try:
            # Obtener configuración actual para comparación
            old_config = self.config_data.copy()
            
            # Recopilar configuración
            config_to_save = self.collect_config_data()
            
            # Verificar si requiere reinicio
            needs_restart, changed_field = self.requires_restart(old_config, config_to_save)
            
            # Validar configuración
            is_valid, errors = self.config_controller.validate_configuration(config_to_save)
            if not is_valid:
                messagebox.showerror("Error de Validación", 
                                   f"❌ Errores en la configuración:\n\n" + "\n".join(f"• {error}" for error in errors))
                return
            
            # Guardar configuración
            if self.config_controller.save_configuration(config_to_save):
                # Aplicar cambios al sistema
                if self.config_controller.apply_configuration(config_to_save):
                    print(f"✅ APLICADO EXITOSO - RESETEANDO changes_made: {self.changes_made} → False")
                    self.changes_made = False
                    
                    # Mostrar mensaje apropiado según si requiere reinicio
                    if needs_restart:
                        field_names = {
                            'company_name': 'nombre de la empresa',
                            'logo_path': 'imagen del logo'
                        }
                        field_desc = field_names.get(changed_field, 'configuración')
                        
                        messagebox.showwarning("Reinicio Requerido", 
                                             f"✅ Configuración aplicada exitosamente.\n\n"
                                             f"⚠️ IMPORTANTE: Has cambiado el {field_desc}.\n"
                                             f"Para que este cambio se aplique completamente,\n"
                                             f"necesitas reiniciar la aplicación.")
                    else:
                        messagebox.showinfo("Configuración", "✅ Configuración aplicada exitosamente")
                else:
                    messagebox.showwarning("Advertencia", "⚠️ Configuración guardada pero algunos cambios requieren reiniciar la aplicación")
                
                # Emitir callback de configuración guardada (para actualizar login si es necesario)
                self.trigger_callback('configuration_saved', config_to_save)
                
                # Asegurar que changes_made sigue siendo False después del callback
                if self.changes_made:
                    print(f"⚠️ CALLBACK CAMBIÓ changes_made a True - Reseteando a False")
                    self.changes_made = False
                
                print(f"✅ DESPUÉS DEL CALLBACK - changes_made: {self.changes_made}")
            else:
                messagebox.showerror("Error", "❌ Error aplicando la configuración")
                
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error aplicando configuración:\n{str(e)}")
        finally:
            # Desactivar flag de guardado al final del proceso
            self.saving_data = False
            print(f"🔓 DESACTIVADO saving_data - Cambios pueden ser marcados nuevamente")
        
        print(f"🔧 FINALIZANDO SAVE_CONFIGURATION - changes_made: {self.changes_made}\n")
    
    def cancel_changes(self):
        """Cancelar cambios"""
        if self.changes_made:
            if messagebox.askyesno("Confirmar", "¿Desea descartar los cambios realizados?"):
                if self.embedded:
                    self.trigger_callback('back_to_dashboard')
                else:
                    self.root.destroy()
        else:
            if self.embedded:
                self.trigger_callback('back_to_dashboard')
            else:
                self.root.destroy()
    
    def restore_defaults(self):
        """Restaurar configuración por defecto"""
        if messagebox.askyesno("Confirmar", "¿Desea restaurar la configuración por defecto?\n\nTodos los cambios actuales se perderán."):
            self.config_data = self.config_controller.get_default_configuration()
            self.update_ui_with_config()
            self.changes_made = True
            messagebox.showinfo("Configuración", "✅ Configuración restaurada a valores por defecto")
    
    def go_back_to_dashboard(self):
        """Volver al dashboard principal"""
        if self.changes_made:
            result = messagebox.askyesnocancel(
                "Cambios sin guardar", 
                "Hay cambios sin guardar. ¿Desea guardarlos antes de volver?"
            )
            if result is True:  # Sí, guardar
                self.save_configuration()
                self.trigger_callback('back_to_dashboard')
            elif result is False:  # No, descartar
                self.trigger_callback('back_to_dashboard')
            # Si es None (Cancelar), no hacer nada
        else:
            self.trigger_callback('back_to_dashboard')
    
    def bind_callback(self, event_name: str, callback: Callable):
        """Registrar callback para navegación"""
        self.callbacks[event_name] = callback
        print(f"📋 Config: Callback '{event_name}' registrado")
        
        # Crear navbar cuando se registre el primer callback de navegación
        if not self.navbar_built and event_name in ['back_to_dashboard', 'new_sale', 'view_products']:
            print(f"   📋 Primer callback de navegación detectado")
            # Esperar un poco para que se registren todos los callbacks
            self.root.after(100, self._try_build_navbar)
    
    def _try_build_navbar(self):
        """Intentar construir navbar después de un delay"""
        if not self.navbar_built:
            print(f"📋 Callbacks totales registrados en config: {len(self.callbacks)}")
            for key in self.callbacks:
                print(f"   - {key}")
            self.build_navbar()
            self.navbar_built = True
    
    def build_navbar(self):
        """Construir navbar DESPUÉS de registrar callbacks"""
        print("🔨 Construyendo navbar en configuration_view...")
        # Encontrar el widget header para insertar el navbar después
        header_widget = None
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                try:
                    if widget.cget('bg') == '#2c3e50' and widget.cget('height') != 50:
                        header_widget = widget
                        break
                except:
                    pass
        
        if header_widget:
            self.create_navbar(header_widget)
            print("   ✅ Navbar construido")
        else:
            print("   ✗ No se encontró el header, creando navbar sin after")
            self.create_navbar()
    
    def on_close(self):
        """Manejar cierre de ventana"""
        if self.embedded:
            # En modo embebido, usar el método de volver
            self.go_back_to_dashboard()
        else:
            # En modo ventana independiente
            if self.changes_made:
                result = messagebox.askyesnocancel(
                    "Cambios sin guardar", 
                    "Hay cambios sin guardar. ¿Desea guardarlos antes de cerrar?"
                )
                if result is True:  # Sí, guardar
                    self.save_configuration()
                    self.root.destroy()
                elif result is False:  # No, descartar
                    self.root.destroy()
                # Si es None (Cancelar), no hacer nada
            else:
                self.root.destroy()
    
    def collect_config_data(self) -> Dict[str, Any]:
        """Recopilar todos los datos de configuración de la UI"""
        config_to_save = {}
        
        # Variables de la empresa y sistema
        for attr_name in dir(self):
            if attr_name.endswith('_var') and hasattr(self, attr_name):
                var = getattr(self, attr_name)
                if isinstance(var, (tk.StringVar, tk.BooleanVar)):
                    key = attr_name.replace('_var', '')
                    value = var.get()
                    
                    # Manejo especial para logo_path
                    if key == 'logo_path':
                        # Si contiene texto de UI, extraer el path real o usar el path del config_data
                        if "Logo seleccionado:" in value:
                            # Usar el path real del config_data si existe
                            if 'logo_path' in self.config_data and not "Logo seleccionado:" in self.config_data['logo_path']:
                                config_to_save[key] = self.config_data['logo_path']
                            else:
                                # Limpiar el formato de UI
                                filename = value.replace("Logo seleccionado: ", "")
                                # Si es solo un nombre de archivo, mantenerlo así o buscar path completo
                                config_to_save[key] = filename
                        elif value == 'No se ha seleccionado ningún logo':
                            config_to_save[key] = ''
                        else:
                            # Path completo directo
                            config_to_save[key] = value
                    else:
                        config_to_save[key] = value
        
        # Variables de base de datos
        if hasattr(self, 'db_vars'):
            config_to_save.update({k: v.get() for k, v in self.db_vars.items()})
        
        return config_to_save
    
    def mark_changes_made(self):
        """Marcar que se han hecho cambios"""
        # Solo marcar cambios si no estamos cargando datos
        if not getattr(self, 'loading_data', False):
            old_value = self.changes_made
            self.changes_made = True
            if not old_value:  # Solo imprimir cuando cambie de False a True
                import traceback
                print(f"🔄 CAMBIOS MARCADOS: {old_value} → {self.changes_made}")
                print("📍 Stack trace del cambio:")
                for line in traceback.format_stack()[-3:-1]:
                    print(f"   {line.strip()}")
        else:
            print("🔄 Cambio detectado durante carga - ignorando...")
    
    def safe_mark_changes(self, *args):
        """Versión segura de mark_changes_made para usar en callbacks"""
        print(f"🔔 SAFE_MARK_CHANGES LLAMADO - args: {args}")
        
        # No marcar cambios si estamos cargando o guardando datos
        if self.loading_data:
            print("🚫 IGNORADO: loading_data=True")
            return
            
        if self.saving_data:
            print("🚫 IGNORADO: saving_data=True") 
            return
            
        self.mark_changes_made()
    
    def requires_restart(self, old_config, new_config):
        """Verificar si los cambios requieren reiniciar la aplicación"""
        restart_fields = ['company_name', 'logo_path']
        
        for field in restart_fields:
            old_value = old_config.get(field, '')
            new_value = new_config.get(field, '')
            if old_value != new_value:
                return True, field
        
        return False, None
    
    def update_ui_with_config(self):
        """Actualizar UI con datos de configuración cargados"""
        try:
            print(f"🔄 Actualizando UI con {len(self.config_data)} elementos de configuración...")
            
            # FORZAR actualización de campos específicos que sabemos que tienen datos
            specific_fields = {
                'company_name': 'Mi Negocio POS',
                'currency': 'CLP', 
                'currency_symbol': '$',
                'theme': 'Claro',
                'language': 'Español',
                'tax_rate': '19'
            }
            
            print("🔧 FORZANDO actualización de campos específicos...")
            for field, expected_value in specific_fields.items():
                var_name = f"{field}_var"
                if hasattr(self, var_name):
                    var = getattr(self, var_name)
                    actual_config_value = self.config_data.get(field, '')
                    print(f"   🎯 {field}:")
                    print(f"      - Valor en config_data: '{actual_config_value}'")
                    print(f"      - Valor en variable antes: '{var.get()}'")
                    
                    # Usar el valor real del config_data
                    if actual_config_value:
                        var.set(actual_config_value)
                        print(f"      ✅ Variable actualizada a: '{var.get()}'")
                    else:
                        print(f"      ⚠️ Valor vacío en config_data para {field}")
                else:
                    print(f"   ❌ Variable {var_name} no existe")
            
            # ACTUALIZAR SOLO LOS VALORES DE LAS VARIABLES EXISTENTES (SIN RECREARLAS)
            print("\n🔄 Actualizando valores de variables existentes (sin recrear)...")
            for attr_name in dir(self):
                if attr_name.endswith('_var') and hasattr(self, attr_name):
                    var = getattr(self, attr_name)
                    key = attr_name.replace('_var', '')
                    if key in self.config_data and isinstance(var, (tk.StringVar, tk.BooleanVar)):
                        old_value = var.get()
                        new_value = self.config_data[key]
                        var_id = id(var)
                        
                        # Solo actualizar si el valor cambió y mantener la misma referencia
                        if str(old_value) != str(new_value):
                            var.set(new_value)
                            new_var_id = id(getattr(self, attr_name))
                            id_status = "✅ MISMA REF" if var_id == new_var_id else "❌ REF CAMBIÓ"
                            print(f"   ✅ {key}: '{old_value}' → '{new_value}' | {id_status}")
                        else:
                            print(f"   ✓ {key}: valor ya correcto '{old_value}'")
            
            # Actualizar variables de base de datos si existen (SIN RECREAR)
            if hasattr(self, 'db_vars'):
                print(f"\n🗄️ Actualizando {len(self.db_vars)} variables de base de datos (sin recrear)...")
                for key, var in self.db_vars.items():
                    if key in self.config_data:
                        old_value = var.get()
                        new_value = self.config_data[key]
                        var_id = id(var)
                        
                        if str(old_value) != str(new_value):
                            var.set(new_value)
                            new_var_id = id(self.db_vars[key])
                            id_status = "✅ MISMA REF" if var_id == new_var_id else "❌ REF CAMBIÓ"
                            print(f"   ✅ DB {key}: '{old_value}' → '{new_value}' | {id_status}")
                        else:
                            print(f"   ✓ DB {key}: valor ya correcto '{old_value}'")
            
            # Verificación final - asegurar que los valores están en las variables
            print("\n🔍 VERIFICACIÓN FINAL de variables importantes:")
            verification_fields = ['company_name', 'currency', 'theme', 'tax_rate']
            for field in verification_fields:
                var_name = f"{field}_var"
                if hasattr(self, var_name):
                    var = getattr(self, var_name)
                    current_value = var.get()
                    expected_value = self.config_data.get(field, '')
                    status = "✅" if current_value == expected_value else "❌"
                    print(f"   {status} {field}: variable='{current_value}' | config='{expected_value}'")
                    
                    # Si no coinciden, forzar la actualización
                    if current_value != expected_value and expected_value:
                        print(f"      🔧 FORZANDO {field} = '{expected_value}'")
                        var.set(expected_value)
                        final_value = var.get()
                        print(f"      ✅ Valor final: '{final_value}'")
            
            # Actualizar logo path si existe
            if hasattr(self, 'logo_path_var') and 'logo_path' in self.config_data:
                logo_path = self.config_data['logo_path']
                print(f"\n🖼️ Logo path cargado: '{logo_path}'")
                if logo_path and logo_path != '':
                    import os
                    if "Logo seleccionado:" in logo_path:
                        # Ya está en formato de UI, mantenerlo
                        self.logo_path_var.set(logo_path)
                        print(f"   ✅ Logo UI format mantenido: {logo_path}")
                    elif os.path.exists(logo_path):
                        # Path completo válido, mantenerlo tal como está para uso interno
                        # pero mostrar solo el nombre en la UI
                        filename = os.path.basename(logo_path)
                        self.logo_path_var.set(logo_path)  # Mantener path completo en la variable
                        print(f"   ✅ Logo encontrado - path completo mantenido: {logo_path}")
                    else:
                        # Buscar archivo por nombre en directorios comunes
                        possible_paths = [
                            os.path.join(os.path.expanduser("~"), "Downloads", logo_path),
                            os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "images", logo_path),
                        ]
                        found = False
                        for possible_path in possible_paths:
                            if os.path.exists(possible_path):
                                self.logo_path_var.set(possible_path)
                                self.config_data['logo_path'] = possible_path
                                print(f"   ✅ Logo encontrado en: {possible_path}")
                                found = True
                                break
                        
                        if not found:
                            self.logo_path_var.set('No se ha seleccionado ningún logo')
                            print(f"   ⚠️ Logo no encontrado: {logo_path}")
                else:
                    self.logo_path_var.set('No se ha seleccionado ningún logo')
                    print("   ℹ️ No hay logo configurado")
            
            # Resetear estado de cambios después de cargar
            self.changes_made = False
            self.loading_data = False  # Terminar modo de carga
            print("\n✅ UI actualizada correctamente con datos guardados")
            
            # Ahora agregar callbacks para detectar cambios futuros
            self.setup_change_callbacks()
            
            # Forzar actualización de la ventana
            if hasattr(self, 'root'):
                self.root.update_idletasks()
                print("✅ Ventana actualizada")
            
        except Exception as e:
            print(f"❌ Error actualizando UI: {e}")
            import traceback
            traceback.print_exc()
    
    def setup_change_callbacks(self):
        """Configurar callbacks para detectar cambios después de la carga inicial"""
        try:
            print("🔗 Configurando callbacks para detectar cambios...")
            
            # Configurar callbacks para variables principales
            for attr_name in dir(self):
                if attr_name.endswith('_var') and hasattr(self, attr_name):
                    var = getattr(self, attr_name)
                    if isinstance(var, (tk.StringVar, tk.BooleanVar)) and not hasattr(var, '_change_callback_added'):
                        var.trace_add('write', self.safe_mark_changes)
                        var._change_callback_added = True
                        key = attr_name.replace('_var', '')
                        print(f"   ✅ Callback agregado para {key}")
            
            # Configurar callbacks para variables de base de datos
            if hasattr(self, 'db_vars'):
                for key, var in self.db_vars.items():
                    if not hasattr(var, '_change_callback_added'):
                        var.trace_add('write', self.safe_mark_changes)
                        var._change_callback_added = True
                        print(f"   ✅ Callback DB agregado para {key}")
            
            print("✅ Callbacks configurados correctamente")
            
        except Exception as e:
            print(f"❌ Error configurando callbacks: {e}")
    
    def force_ui_refresh(self):
        """Forzar actualización de la interfaz después de un retraso"""
        try:
            print("🔄 FUERZA: Actualizando interfaz con retraso...")
            
            # Verificar variables críticas y forzar valores si es necesario
            critical_fields = {
                'company_name': 'Mi Negocio POS',
                'currency': 'CLP',
                'theme': 'Claro'
            }
            
            for field, test_value in critical_fields.items():
                var_name = f"{field}_var"
                if hasattr(self, var_name):
                    var = getattr(self, var_name)
                    config_value = self.config_data.get(field, '')
                    current_value = var.get()
                    
                    print(f"🔍 {field}: actual='{current_value}' | config='{config_value}'")
                    
                    if not current_value and config_value:
                        print(f"🔧 FORZANDO {field} = '{config_value}'")
                        var.set(config_value)
                        new_value = var.get()
                        print(f"✅ Valor forzado: '{new_value}'")
            
            # Forzar actualización de todos los Entry widgets específicamente
            self.force_entry_widgets_update()
            
            # Forzar redibujado completo
            if hasattr(self, 'root'):
                self.root.update_idletasks()
                self.root.update()
                print("✅ Interfaz completamente actualizada con retraso")
            
        except Exception as e:
            print(f"❌ Error en force_ui_refresh: {e}")
    
    def force_entry_widgets_update(self):
        """Forzar actualización visual de todos los Entry widgets"""
        try:
            print("🎯 FORZANDO actualización de Entry widgets...")
            
            # Buscar todos los Entry widgets en la ventana
            def find_entries(widget):
                entries = []
                for child in widget.winfo_children():
                    if isinstance(child, tk.Entry):
                        entries.append(child)
                    entries.extend(find_entries(child))
                return entries
            
            if hasattr(self, 'root'):
                all_entries = find_entries(self.root)
                print(f"🔍 Encontrados {len(all_entries)} Entry widgets")
                
                # Para cada Entry, verificar si tiene una variable asociada
                updated_count = 0
                for entry in all_entries:
                    try:
                        if hasattr(entry, 'textvariable') and entry['textvariable']:
                            var_name = str(entry['textvariable'])
                            # Buscar la variable en nuestros atributos
                            for attr_name in dir(self):
                                if attr_name.endswith('_var') and hasattr(self, attr_name):
                                    var = getattr(self, attr_name)
                                    if str(var) == var_name:
                                        current_value = var.get()
                                        if current_value:
                                            # Forzar actualización del Entry
                                            entry.delete(0, tk.END)
                                            entry.insert(0, current_value)
                                            print(f"   ✅ Entry actualizado: {attr_name} = '{current_value}'")
                                            updated_count += 1
                                        break
                    except Exception as e:
                        print(f"   ⚠️ Error actualizando Entry: {e}")
                
                print(f"✅ {updated_count} Entry widgets actualizados manualmente")
            
        except Exception as e:
            print(f"❌ Error en force_entry_widgets_update: {e}")
    
    def export_configuration(self):
        """Exportar configuración a archivo"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Exportar Configuración",
                defaultextension=".json",
                filetypes=[("JSON", "*.json"), ("Todos los archivos", "*.*")]
            )
            if file_path:
                if self.config_controller.export_configuration(file_path):
                    messagebox.showinfo("Exportar", f"✅ Configuración exportada exitosamente a:\n{file_path}")
                else:
                    messagebox.showerror("Error", "❌ Error exportando la configuración")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error exportando configuración:\n{str(e)}")
    
    def import_configuration(self):
        """Importar configuración desde archivo"""
        try:
            if messagebox.askyesno("Confirmar Importación", 
                                 "⚠️ ¿Está seguro de que desea importar una configuración?\n\n"
                                 "Esto sobrescribirá toda la configuración actual."):
                file_path = filedialog.askopenfilename(
                    title="Importar Configuración",
                    filetypes=[("JSON", "*.json"), ("Todos los archivos", "*.*")]
                )
                if file_path:
                    success, message = self.config_controller.import_configuration(file_path)
                    if success:
                        # Recargar configuración en la UI
                        self.config_data = self.config_controller.load_configuration()
                        self.update_ui_with_config()
                        self.changes_made = True
                        messagebox.showinfo("Importar", f"✅ {message}")
                    else:
                        messagebox.showerror("Error", f"❌ {message}")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error importando configuración:\n{str(e)}")
    
    def center_window(self, width, height):
        """Centrar ventana en la pantalla"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
