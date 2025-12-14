"""
Vista de Gestión de Categorías
Interfaz para administrar categorías de productos
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, List, Callable, Optional
from utils.responsive_utils import ResponsiveManager
from services.permission_service import PermissionService


class CategoryManagementView:
    """Vista principal de gestión de categorías"""
    
    def __init__(self, parent, current_user: Dict[str, Any]):
        self.parent = parent
        self.current_user = current_user
        self.root = tk.Frame(parent, bg='#ecf0f1')
        self.root.pack(fill='both', expand=True)
        
        # Inicializar gestor responsivo
        self.responsive = ResponsiveManager(parent)

        self.permission_service = PermissionService()
        
        # Callbacks
        self.on_refresh_callback = None
        self.on_search_callback = None
        self.on_create_callback = None
        self.on_edit_callback = None
        self.on_delete_callback = None
        self.on_back_callback = None
        
        # Callbacks para navegación (navbar)
        self.callbacks = {}
        
        # Variables
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search_changed)
        
        # Crear interfaz base (sin navbar todavía)
        self.create_widgets()

    def has_permission(self, permission: str) -> bool:
        """Verificar permisos del usuario actual"""
        try:
            return self.permission_service.check_permission(self.current_user, permission)
        except Exception as exc:
            print(f"Error verificando permiso {permission}: {exc}")
            return False
    
    def create_widgets(self):
        """Crear widgets de la interfaz"""
        # Header
        self.create_header()
        
        # El navbar se creará después de registrar callbacks
        # en el método build_navbar()
        
        # Toolbar
        self.create_toolbar()
        
        # Contenido principal
        main_content = tk.Frame(self.root, bg='#ecf0f1')
        main_content.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Tabla de categorías
        self.create_table(main_content)
        
        # Footer con estadísticas
        self.create_footer()
    
    def create_header(self):
        """Crear header"""
        header = tk.Frame(self.root, bg='#2c3e50', height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg='#2c3e50')
        header_content.pack(fill='both', expand=True, padx=30)
        
        tk.Label(
            header_content,
            text="🏷️  Gestión de Categorías",
            font=('Segoe UI', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(side='left', pady=15)
        
        # Usuario actual (derecha, antes del botón)
        tk.Label(
            header_content,
            text=f"Usuario: {self.current_user.get('full_name', 'N/A')}",
            font=('Segoe UI', 10),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack(side='right', padx=10)
        
        # Botón volver
        tk.Button(
            header_content,
            text="← Volver",
            command=self._on_back,
            font=('Segoe UI', 11),
            bg='#34495e',
            fg='white',
            activebackground='#2c3e50',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8
        ).pack(side='right', pady=15)
    
    def build_navbar(self):
        """Construir navbar DESPUÉS de registrar callbacks"""
        # Encontrar el widget header para insertar el navbar después
        header_widget = None
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') == '#2c3e50':
                header_widget = widget
                break
        
        if header_widget:
            self.create_navbar(header_widget)
    
    def create_navbar(self, after_widget):
        """Crear navbar personalizado - GLOBAL para todos los módulos"""
        navbar_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        navbar_frame.pack(fill='x', after=after_widget)
        navbar_frame.pack_propagate(False)
        
        # Estilo de botones
        btn_style = {
            'font': ('Segoe UI', 11, 'bold'),
            'bg': '#2c3e50',
            'fg': 'white',
            'activebackground': '#34495e',
            'activeforeground': 'white',
            'relief': 'flat',
            'bd': 0,
            'padx': 15,
            'pady': 10,
            'cursor': 'hand2'
        }
        
        # Contenedor de botones
        buttons_container = tk.Frame(navbar_frame, bg='#2c3e50')
        buttons_container.pack(side='left', padx=10, pady=5)
        
        # Helper para ejecutar callbacks de forma segura
        def safe_call(callback_name):
            def wrapper():
                print(f"🔄 Navbar: Intentando ejecutar '{callback_name}'")
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
        file_menu = tk.Menu(file_btn, tearoff=0, font=('Segoe UI', 10))
        file_btn.config(menu=file_menu)
        file_menu.add_command(label="Nueva Venta", command=safe_call('new_sale'))
        file_menu.add_separator()
        file_menu.add_command(label="Volver al Dashboard", command=self._on_back)
        
        # Botón Ventas
        sales_btn = tk.Menubutton(buttons_container, text="💰 Ventas", **btn_style)
        sales_btn.pack(side='left', padx=2)
        sales_menu = tk.Menu(sales_btn, tearoff=0, font=('Segoe UI', 10))
        sales_btn.config(menu=sales_menu)
        if self.has_permission('sales.create'):
            file_menu.add_command(label="Nueva Venta", command=safe_call('new_sale'))
            file_menu.add_separator()
        
        # Botón Inventario (ACTIVO)
        inv_btn = tk.Menubutton(buttons_container, text="📦 Inventario", **btn_style)
        inv_btn.config(bg='#34495e')  # Resaltar activo
        inv_btn.pack(side='left', padx=2)
        inv_menu = tk.Menu(inv_btn, tearoff=0, font=('Segoe UI', 10))
        if self.has_permission('sales.create'):
            sales_menu.add_command(label="Nueva Venta", command=safe_call('new_sale'))
        if self.has_permission('sales.view'):
            sales_menu.add_command(label="Historial de Ventas", command=safe_call('sales_history'))
        if sales_menu.index('end') is None:
            sales_menu.add_command(label="Sin accesos disponibles", state='disabled')
        inv_menu.add_command(label="Gestionar Categorías ✓", command=lambda: None)  # Actual
        inv_menu.add_command(label="Control de Stock", command=safe_call('stock_control'))
        
        # Botón Reportes
        reports_btn = tk.Menubutton(buttons_container, text="📊 Reportes", **btn_style)
        reports_btn.pack(side='left', padx=2)
        reports_menu = tk.Menu(reports_btn, tearoff=0, font=('Segoe UI', 10))
        reports_btn.config(menu=reports_menu)
        reports_menu.add_command(label="Reporte Diario", command=safe_call('daily_report'))
        reports_menu.add_command(label="Reporte Completo", command=safe_call('full_report'))
        
        # Botón Administración
        admin_btn = tk.Menubutton(buttons_container, text="⚙️ Administración", **btn_style)
        admin_btn.pack(side='left', padx=2)
        admin_menu = tk.Menu(admin_btn, tearoff=0, font=('Segoe UI', 10))
        admin_btn.config(menu=admin_menu)
        admin_menu.add_command(label="Gestionar Usuarios", command=safe_call('manage_users'))
        admin_menu.add_command(label="Gestionar Roles", command=safe_call('manage_roles'))
        admin_menu.add_command(label="Configuración", command=safe_call('system_config'))
        
        # Botón Ayuda
        help_btn = tk.Menubutton(buttons_container, text="❓ Ayuda", **btn_style)
        help_btn.pack(side='left', padx=2)
        help_menu = tk.Menu(help_btn, tearoff=0, font=('Segoe UI', 10))
        help_btn.config(menu=help_menu)
        help_menu.add_command(label="Manual de Usuario", command=safe_call('show_manual'))
        help_menu.add_command(label="Acerca de", command=safe_call('show_about'))
    
    def create_toolbar(self):
        """Crear toolbar con búsqueda y botones"""
        # Toolbar
        toolbar = tk.Frame(self.root, bg='white', height=70)
        toolbar.pack(fill='x')
        toolbar.pack_propagate(False)
        
        toolbar_content = tk.Frame(toolbar, bg='white')
        toolbar_content.pack(fill='both', expand=True, padx=30, pady=15)
        
        # Búsqueda
        search_frame = tk.Frame(toolbar_content, bg='white')
        search_frame.pack(side='left', fill='x', expand=True)
        
        tk.Label(
            search_frame,
            text="🔍",
            font=('Segoe UI', 14),
            bg='white'
        ).pack(side='left', padx=(0, 10))
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 11),
            relief='solid',
            bd=1,
            width=40
        )
        search_entry.pack(side='left', fill='x', expand=True)
        search_entry.insert(0, "Buscar categoría...")
        search_entry.config(fg='#95a5a6')
        
        def on_focus_in(e):
            if search_entry.get() == "Buscar categoría...":
                search_entry.delete(0, tk.END)
                search_entry.config(fg='#2c3e50')
        
        def on_focus_out(e):
            if not search_entry.get():
                search_entry.insert(0, "Buscar categoría...")
                search_entry.config(fg='#95a5a6')
        
        search_entry.bind('<FocusIn>', on_focus_in)
        search_entry.bind('<FocusOut>', on_focus_out)
        
        # Botón Nueva Categoría
        tk.Button(
            toolbar_content,
            text="➕ Nueva Categoría",
            command=self._on_create_click,
            font=('Segoe UI', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=10
        ).pack(side='right', padx=(10, 0))
        # Atajo: Ctrl+N para nueva categoría
        self.root.bind_all('<Control-n>', lambda e: self._on_create_click())
        self.root.bind_all('<Control-N>', lambda e: self._on_create_click())
    
    def create_table(self, parent):
        """Crear tabla de categorías"""
        # Frame de la tabla
        table_frame = tk.Frame(parent, bg='white', relief='solid', bd=1)
        table_frame.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview
        columns = ('ID', 'Nombre', 'Productos', 'Estado', 'Categoría Padre')
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set,
            selectmode='browse',
            height=15
        )
        
        # Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre de Categoría')
        self.tree.heading('Productos', text='Productos')
        self.tree.heading('Estado', text='Estado')
        self.tree.heading('Categoría Padre', text='Categoría Padre')
        
        self.tree.column('ID', width=60, anchor='center')
        self.tree.column('Nombre', width=300, anchor='w')
        self.tree.column('Productos', width=100, anchor='center')
        self.tree.column('Estado', width=100, anchor='center')
        self.tree.column('Categoría Padre', width=200, anchor='w')
        
        # Estilo para filas
        self.tree.tag_configure('active', background='#ffffff')
        self.tree.tag_configure('inactive', background='#ffebee')
        
        # Eventos
        self.tree.bind('<Double-Button-1>', lambda e: self._on_edit_click())
        self.tree.bind('<<TreeviewSelect>>', self._on_select)
        
        scrollbar.config(command=self.tree.yview)
        self.tree.pack(fill='both', expand=True)
        
        # Panel de acciones (derecha)
        actions_frame = tk.Frame(parent, bg='white', width=200, relief='solid', bd=1)
        actions_frame.pack(side='right', fill='y', padx=(20, 0))
        actions_frame.pack_propagate(False)
        
        tk.Label(
            actions_frame,
            text="⚙️ Acciones",
            font=('Segoe UI', 12, 'bold'),
            bg='#f8f9fa',
            fg='#2c3e50',
            pady=15
        ).pack(fill='x')
        
        self.edit_btn = tk.Button(
            actions_frame,
            text="✏️ Editar",
            command=self._on_edit_click,
            font=('Segoe UI', 10),
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            relief='flat',
            cursor='hand2',
            state='disabled',
            pady=10
        )
        self.edit_btn.pack(fill='x', padx=15, pady=5)
        
        self.delete_btn = tk.Button(
            actions_frame,
            text="🗑️ Eliminar",
            command=self._on_delete_click,
            font=('Segoe UI', 10),
            bg='#e74c3c',
            fg='white',
            activebackground='#c0392b',
            relief='flat',
            cursor='hand2',
            state='disabled',
            pady=10
        )
        self.delete_btn.pack(fill='x', padx=15, pady=5)
    
    def create_footer(self):
        """Crear footer con estadísticas"""
        footer = tk.Frame(self.root, bg='#34495e', height=50)
        footer.pack(fill='x', side='bottom')
        footer.pack_propagate(False)
        
        footer_content = tk.Frame(footer, bg='#34495e')
        footer_content.pack(fill='both', expand=True, padx=30)
        
        self.stats_label = tk.Label(
            footer_content,
            text="Total: 0 categorías",
            font=('Segoe UI', 10),
            bg='#34495e',
            fg='white'
        )
        self.stats_label.pack(side='left', pady=12)
    
    def load_categories(self, categories: List[Dict[str, Any]]):
        """Cargar categorías en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Cargar datos
        for category in categories:
            status_text = "✅ Activo" if category.get('status') == 'active' else "❌ Inactivo"
            parent_name = category.get('parent_name', '-')
            
            tag = 'active' if category.get('status') == 'active' else 'inactive'
            
            self.tree.insert('', 'end', values=(
                category.get('id', ''),
                category.get('name', ''),
                category.get('product_count', 0),
                status_text,
                parent_name
            ), tags=(tag,))
        
        # Actualizar estadísticas
        self.stats_label.config(text=f"Total: {len(categories)} categorías")
    
    def get_selected_category(self) -> Optional[Dict[str, Any]]:
        """Obtener categoría seleccionada"""
        selection = self.tree.selection()
        if not selection:
            return None
        
        item = self.tree.item(selection[0])
        values = item['values']
        
        return {
            'id': values[0],
            'name': values[1],
            'product_count': values[2]
        }
    
    def _on_select(self, event):
        """Manejar selección de categoría"""
        if self.tree.selection():
            self.edit_btn.config(state='normal')
            self.delete_btn.config(state='normal')
        else:
            self.edit_btn.config(state='disabled')
            self.delete_btn.config(state='disabled')
    
    def _on_search_changed(self, *args):
        """Manejar cambio en búsqueda"""
        search_text = self.search_var.get()
        if search_text and search_text != "Buscar categoría..." and self.on_search_callback:
            self.on_search_callback(search_text)
        elif self.on_refresh_callback:
            self.on_refresh_callback()
    
    def _on_create_click(self):
        """Manejar clic en crear"""
        if self.on_create_callback:
            self.on_create_callback()
    
    def _on_edit_click(self):
        """Manejar clic en editar"""
        if self.on_edit_callback:
            category = self.get_selected_category()
            if category:
                self.on_edit_callback(category['id'])
    
    def _on_delete_click(self):
        """Manejar clic en eliminar"""
        if self.on_delete_callback:
            category = self.get_selected_category()
            if category:
                if messagebox.askyesno(
                    "Confirmar eliminación",
                    f"¿Estás seguro de que deseas eliminar la categoría '{category['name']}'?",
                    parent=self.root
                ):
                    self.on_delete_callback(category['id'])
    
    def _on_back(self):
        """Volver al dashboard"""
        if hasattr(self, 'on_back_callback') and self.on_back_callback:
            self.on_back_callback()
        else:
            # Limpiar la vista actual
            for widget in self.root.winfo_children():
                widget.destroy()
    
    def register_callbacks(self, refresh, search, create, edit, delete, back=None, **kwargs):
        """Registrar callbacks"""
        self.on_refresh_callback = refresh
        self.on_search_callback = search
        self.on_create_callback = create
        self.on_edit_callback = edit
        self.on_delete_callback = delete
        self.on_back_callback = back
        
        # Registrar callbacks de navegación del navbar
        self.callbacks = {
            'new_sale': kwargs.get('new_sale'),
            'sales_history': kwargs.get('sales_history'),
            'view_products': kwargs.get('view_products'),
            'view_categories': kwargs.get('view_categories'),
            'stock_control': kwargs.get('stock_control'),
            'daily_report': kwargs.get('daily_report'),
            'full_report': kwargs.get('full_report'),
            'manage_users': kwargs.get('manage_users'),
            'manage_roles': kwargs.get('manage_roles'),
            'system_config': kwargs.get('system_config'),
            'show_manual': kwargs.get('show_manual'),
            'show_about': kwargs.get('show_about')
        }
        
        # Debug: Verificar callbacks registrados
        print(f"📋 Callbacks registrados: {len(self.callbacks)} callbacks")
        for key, value in self.callbacks.items():
            print(f"   - {key}: {'✓ OK' if value else '✗ None'}")
        
        # IMPORTANTE: Crear el navbar DESPUÉS de registrar los callbacks
        # Usar after() para asegurar que la interfaz esté lista
        self.root.after(100, self.build_navbar)
