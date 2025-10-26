"""
Vista de Gestión de Productos
Interfaz para CRUD de productos e inventario
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Callable, Optional, List
from views.base_view import BaseView
from decimal import Decimal
from services.permission_service import PermissionService
from utils.responsive_utils import ResponsiveManager


class ProductManagementView(BaseView):
    """Vista para gestión de productos"""
    
    def __init__(self, parent, user_data: Dict[str, Any]):
        self.parent = parent
        self.user_data = user_data
        super().__init__(parent)
        
        self.permission_service = PermissionService()
        
        # Inicializar gestor responsivo
        self.responsive = ResponsiveManager(self.root)
        
        self.callbacks = {}
        self.products = []
        self.categories = []
        self.units = []
        self.selected_product = None
        
        # Flag para saber si ya se creó el navbar
        self.navbar_built = False
        
        self.setup_product_view()
    
    def has_permission(self, permission: str) -> bool:
        """Verificar si el usuario actual tiene un permiso específico"""
        try:
            return self.permission_service.check_permission(self.user_data, permission)
        except Exception as e:
            print(f"Error verificando permiso {permission}: {e}")
            return False
    
    def setup_product_view(self):
        """Configurar vista principal"""
        # Frame principal
        self.main_frame = tk.Frame(self.parent, bg='#f5f6fa')
        self.main_frame.pack(fill='both', expand=True)
        
        # Header
        self.create_header()
        
        # El navbar se creará después de registrar callbacks
        # en build_navbar()
        
        # Toolbar con búsqueda y acciones
        self.create_toolbar()
        
        # Contenido principal: Lista de productos y panel de detalles
        self.create_main_content()
        
        # Footer con estadísticas
        self.create_footer()
    
    def create_header(self):
        """Crear header con navegación"""
        header = tk.Frame(self.main_frame, bg='#2c3e50', height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Título (izquierda)
        title_label = tk.Label(
            header,
            text="📦 Gestión de Productos",
            font=('Segoe UI', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(side='left', padx=20, pady=15)
        
        # Botón de regresar al dashboard (derecha)
        back_btn = tk.Button(
            header,
            text="⬅️ Regresar",
            font=('Segoe UI', 10, 'bold'),
            bg='#34495e',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8,
            command=self.on_back_to_dashboard
        )
        back_btn.pack(side='right', padx=20, pady=15)
        
        # Usuario actual (derecha, antes del botón)
        user_label = tk.Label(
            header,
            text=f"Usuario: {self.user_data.get('full_name', 'N/A')}",
            font=('Segoe UI', 10),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        user_label.pack(side='right', padx=10)
    
    def build_navbar(self):
        """Construir navbar DESPUÉS de registrar callbacks"""
        print("🔨 Construyendo navbar...")
        # Encontrar el widget header para insertar el navbar después
        header_widget = None
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') == '#2c3e50':
                header_widget = widget
                break
        
        if header_widget:
            self.create_navbar(header_widget)
            print("   ✅ Navbar construido")
        else:
            print("   ✗ No se encontró el header")
    
    def create_navbar(self, after_widget=None):
        """Crear navbar personalizado con menús - GLOBAL para todos los módulos"""
        navbar_frame = tk.Frame(self.main_frame, bg='#2c3e50', height=50)
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
        inv_menu.add_command(label="Ver Productos ✓", command=lambda: None)  # Actual
        inv_menu.add_command(label="Gestionar Categorías", command=safe_call('view_categories'))
        inv_menu.add_command(label="Control de Stock", command=safe_call('go_to_inventory'))
        
        # Botón Reportes
        rep_btn = tk.Menubutton(buttons_container, text="📊 Reportes", **btn_style)
        rep_btn.pack(side='left', padx=2)
        rep_menu = tk.Menu(rep_btn, tearoff=0, font=('Segoe UI', 11))
        rep_btn.config(menu=rep_menu)
        rep_menu.add_command(label="Ventas del Día", command=safe_call('daily_report'))
        rep_menu.add_command(label="Reporte Completo", command=safe_call('full_report'))
        
        # Botón Administración
        admin_btn = tk.Menubutton(buttons_container, text="⚙️ Administración", **btn_style)
        admin_btn.pack(side='left', padx=2)
        admin_menu = tk.Menu(admin_btn, tearoff=0, font=('Segoe UI', 11))
        admin_btn.config(menu=admin_menu)
        admin_menu.add_command(label="Gestionar Usuarios", command=safe_call('manage_users'))
        admin_menu.add_command(label="Gestionar Roles", command=safe_call('manage_roles'))
        admin_menu.add_separator()
        admin_menu.add_command(label="Configuración", command=safe_call('system_config'))
        
        # Botón Ayuda
        help_btn = tk.Menubutton(buttons_container, text="❓ Ayuda", **btn_style)
        help_btn.pack(side='left', padx=2)
        help_menu = tk.Menu(help_btn, tearoff=0, font=('Segoe UI', 11))
        help_btn.config(menu=help_menu)
        help_menu.add_command(label="Manual de Usuario", command=safe_call('show_manual'))
        help_menu.add_command(label="Acerca de", command=safe_call('show_about'))
    
    def create_toolbar(self):
        """Crear toolbar con búsqueda y botones"""
        toolbar = tk.Frame(self.main_frame, bg='#ecf0f1', height=60)
        toolbar.pack(fill='x', pady=(0, 10))
        toolbar.pack_propagate(False)
        
        # Frame izquierdo: Búsqueda
        left_frame = tk.Frame(toolbar, bg='#ecf0f1')
        left_frame.pack(side='left', fill='y', padx=20, pady=10)
        
        tk.Label(
            left_frame,
            text="🔍 Buscar:",
            font=('Segoe UI', 10),
            bg='#ecf0f1'
        ).pack(side='left', padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.on_search())
        
        search_entry = tk.Entry(
            left_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 10),
            width=40,
            relief='solid',
            bd=1
        )
        search_entry.pack(side='left')
        
        # Frame derecho: Botones de acción
        right_frame = tk.Frame(toolbar, bg='#ecf0f1')
        right_frame.pack(side='right', fill='y', padx=20, pady=10)
        
        # Botón Nuevo Producto - Solo si tiene permiso inventory.create
        if self.has_permission('inventory.create'):
            tk.Button(
                right_frame,
                text="➕ Nuevo Producto",
                font=('Segoe UI', 10, 'bold'),
                bg='#27ae60',
                fg='white',
                relief='flat',
                cursor='hand2',
                padx=15,
                pady=8,
                command=self.on_new_product
            ).pack(side='left', padx=5)
        
        # Botón Actualizar Stock - Solo si tiene permiso inventory.stock
        if self.has_permission('inventory.stock'):
            tk.Button(
                right_frame,
                text="📊 Actualizar Stock",
                font=('Segoe UI', 10),
                bg='#3498db',
                fg='white',
                relief='flat',
                cursor='hand2',
                padx=15,
                pady=8,
                command=self.on_go_to_inventory
            ).pack(side='left', padx=5)
        
        # Botón Exportar - Solo si tiene permiso inventory.export
        if self.has_permission('inventory.export'):
            tk.Button(
                right_frame,
                text="📥 Exportar",
                font=('Segoe UI', 10),
                bg='#95a5a6',
                fg='white',
                relief='flat',
                cursor='hand2',
                padx=15,
                pady=8,
                command=self.on_export
            ).pack(side='left', padx=5)
    
    def create_main_content(self):
        """Crear contenido principal"""
        content_frame = tk.Frame(self.main_frame, bg='#f5f6fa')
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Panel izquierdo: Lista de productos (70%)
        left_panel = tk.Frame(content_frame, bg='white', relief='solid', bd=1)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.create_products_table(left_panel)
        
        # Panel derecho: Detalles y acciones (30%)
        right_panel = tk.Frame(content_frame, bg='white', relief='solid', bd=1, width=350)
        right_panel.pack(side='right', fill='y')
        right_panel.pack_propagate(False)
        
        self.create_details_panel(right_panel)
    
    def create_products_table(self, parent):
        """Crear tabla de productos"""
        # Header de la tabla
        table_header = tk.Frame(parent, bg='#34495e', height=40)
        table_header.pack(fill='x')
        table_header.pack_propagate(False)
        
        tk.Label(
            table_header,
            text="Lista de Productos",
            font=('Segoe UI', 12, 'bold'),
            bg='#34495e',
            fg='white'
        ).pack(side='left', padx=15, pady=10)
        
        # Frame para el Treeview
        tree_frame = tk.Frame(parent, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        columns = ('sku', 'name', 'category', 'stock', 'price', 'status')
        self.products_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            selectmode='browse',
            height=20
        )
        
        # Configurar scrollbars
        vsb.config(command=self.products_tree.yview)
        hsb.config(command=self.products_tree.xview)
        
        # Definir columnas
        self.products_tree.heading('sku', text='SKU')
        self.products_tree.heading('name', text='Nombre')
        self.products_tree.heading('category', text='Categoría')
        self.products_tree.heading('stock', text='Stock')
        self.products_tree.heading('price', text='Precio')
        self.products_tree.heading('status', text='Estado')
        
        # Ancho de columnas
        self.products_tree.column('sku', width=100, anchor='center')
        self.products_tree.column('name', width=300, anchor='w')
        self.products_tree.column('category', width=150, anchor='w')
        self.products_tree.column('stock', width=80, anchor='center')
        self.products_tree.column('price', width=100, anchor='e')
        self.products_tree.column('status', width=100, anchor='center')
        
        # Eventos
        self.products_tree.bind('<<TreeviewSelect>>', self.on_product_select)
        self.products_tree.bind('<Double-1>', lambda e: self.on_edit_product())
        
        # Grid layout
        self.products_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Estilos para las filas
        self.products_tree.tag_configure('low_stock', background='#ffe6e6')
        self.products_tree.tag_configure('out_of_stock', background='#ffcccc')
        self.products_tree.tag_configure('normal', background='white')
    
    def create_details_panel(self, parent):
        """Crear panel de detalles"""
        # Header
        details_header = tk.Frame(parent, bg='#34495e', height=40)
        details_header.pack(fill='x')
        details_header.pack_propagate(False)
        
        tk.Label(
            details_header,
            text="Detalles del Producto",
            font=('Segoe UI', 11, 'bold'),
            bg='#34495e',
            fg='white'
        ).pack(side='left', padx=15, pady=10)
        
        # Contenido
        self.details_content = tk.Frame(parent, bg='white')
        self.details_content.pack(fill='both', expand=True, padx=15, pady=15)
        
        self.show_empty_details()
    
    def show_empty_details(self):
        """Mostrar mensaje cuando no hay producto seleccionado"""
        # Limpiar contenido
        for widget in self.details_content.winfo_children():
            widget.destroy()
        
        empty_frame = tk.Frame(self.details_content, bg='white')
        empty_frame.pack(expand=True, fill='both')
        
        tk.Label(
            empty_frame,
            text="📦",
            font=('Segoe UI Emoji', 48),
            bg='white',
            fg='#bdc3c7'
        ).pack(pady=(50, 20))
        
        tk.Label(
            empty_frame,
            text="Selecciona un producto\npara ver sus detalles",
            font=('Segoe UI', 11),
            bg='white',
            fg='#95a5a6',
            justify='center'
        ).pack()
    
    def show_product_details(self, product: Dict[str, Any]):
        """Mostrar detalles del producto seleccionado"""
        # Limpiar contenido
        for widget in self.details_content.winfo_children():
            widget.destroy()
        
        # Scrollable frame
        canvas = tk.Canvas(self.details_content, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.details_content, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        # Configurar ventana del canvas para que se expanda
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def on_frame_configure(event=None):
            # Actualizar región de scroll
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def on_canvas_configure(event):
            # Ajustar ancho del frame interno al ancho del canvas
            canvas.itemconfig(canvas_window, width=event.width)
        
        scrollable_frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Información del producto
        self._add_detail_row(scrollable_frame, "SKU:", product.get('sku', 'N/A'), is_header=True)
        self._add_detail_row(scrollable_frame, "Nombre:", product.get('name', 'N/A'))
        self._add_detail_row(scrollable_frame, "Categoría:", product.get('category_name', 'N/A'))
        self._add_detail_row(scrollable_frame, "Unidad:", f"{product.get('unit_name', 'N/A')} ({product.get('unit_symbol', '')})")
        
        # Separador
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Precios
        tk.Label(
            scrollable_frame,
            text="💰 Precios",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 5))
        
        self._add_detail_row(scrollable_frame, "Precio Venta:", f"${product.get('price', 0):,.2f}")
        self._add_detail_row(scrollable_frame, "Costo:", f"${product.get('cost', 0):,.2f}")
        self._add_detail_row(
            scrollable_frame, 
            "Margen:", 
            f"{product.get('profit_margin', 0):.1f}%",
            color='#27ae60' if product.get('profit_margin', 0) > 0 else '#e74c3c'
        )
        
        # Separador
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Stock
        stock_qty = product.get('stock_quantity', 0)
        min_stock = product.get('min_stock', 0)
        stock_status = product.get('stock_status', 'normal')
        
        tk.Label(
            scrollable_frame,
            text="📊 Inventario",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 5))
        
        stock_color = '#27ae60'  # Verde
        if stock_status == 'low_stock':
            stock_color = '#f39c12'  # Naranja
        elif stock_status == 'out_of_stock':
            stock_color = '#e74c3c'  # Rojo
        
        self._add_detail_row(scrollable_frame, "Stock Actual:", str(stock_qty), color=stock_color)
        self._add_detail_row(scrollable_frame, "Stock Mínimo:", str(min_stock))
        self._add_detail_row(scrollable_frame, "Stock Máximo:", str(product.get('max_stock', 0)))
        
        # Alerta de stock bajo
        if stock_status == 'low_stock':
            alert = tk.Frame(scrollable_frame, bg='#fff3cd', relief='solid', bd=1)
            alert.pack(fill='x', pady=5)
            tk.Label(
                alert,
                text="⚠️ Stock bajo",
                font=('Segoe UI', 9, 'bold'),
                bg='#fff3cd',
                fg='#856404'
            ).pack(pady=5)
        elif stock_status == 'out_of_stock':
            alert = tk.Frame(scrollable_frame, bg='#f8d7da', relief='solid', bd=1)
            alert.pack(fill='x', pady=5)
            tk.Label(
                alert,
                text="🚫 Sin stock",
                font=('Segoe UI', 9, 'bold'),
                bg='#f8d7da',
                fg='#721c24'
            ).pack(pady=5)
        
        # Separador
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Otros datos
        if product.get('barcode'):
            self._add_detail_row(scrollable_frame, "Código Barras:", product.get('barcode'))
        
        if product.get('tax_rate'):
            self._add_detail_row(scrollable_frame, "IVA:", f"{product.get('tax_rate')}%")
        
        if product.get('description'):
            tk.Label(
                scrollable_frame,
                text="📝 Descripción:",
                font=('Segoe UI', 9, 'bold'),
                bg='white',
                fg='#7f8c8d'
            ).pack(anchor='w', pady=(10, 5))
            
            desc_text = tk.Text(
                scrollable_frame,
                height=3,
                width=35,
                font=('Segoe UI', 9),
                bg='#f8f9fa',
                relief='flat',
                wrap='word'
            )
            desc_text.insert('1.0', product.get('description', ''))
            desc_text.config(state='disabled')
            desc_text.pack(fill='x', pady=(0, 10))
        
        # Botones de acción
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=15)
        
        action_frame = tk.Frame(scrollable_frame, bg='white')
        action_frame.pack(fill='x', pady=10)
        
        # Botón Editar - Solo si tiene permiso inventory.edit
        if self.has_permission('inventory.edit'):
            tk.Button(
                action_frame,
                text="✏️ Editar",
                font=('Segoe UI', 9, 'bold'),
                bg='#3498db',
                fg='white',
                relief='flat',
                cursor='hand2',
                command=self.on_edit_product,
                width=15,
                pady=8
            ).pack(fill='x', pady=2)
        
        # Botón Eliminar - Solo si tiene permiso inventory.delete
        if self.has_permission('inventory.delete'):
            tk.Button(
                action_frame,
                text="🗑️ Eliminar",
                font=('Segoe UI', 9),
                bg='#e74c3c',
                fg='white',
                relief='flat',
                cursor='hand2',
                command=self.on_delete_product,
                width=15,
                pady=8
            ).pack(fill='x', pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _add_detail_row(self, parent, label: str, value: str, is_header: bool = False, color: str = None):
        """Agregar fila de detalle"""
        row = tk.Frame(parent, bg='white')
        row.pack(fill='x', pady=2)
        
        label_font = ('Segoe UI', 10, 'bold') if is_header else ('Segoe UI', 9, 'bold')
        value_font = ('Segoe UI', 11, 'bold') if is_header else ('Segoe UI', 9)
        value_color = color if color else ('#2c3e50' if is_header else '#34495e')
        
        tk.Label(
            row,
            text=label,
            font=label_font,
            bg='white',
            fg='#7f8c8d',
            anchor='w'
        ).pack(side='left')
        
        tk.Label(
            row,
            text=value,
            font=value_font,
            bg='white',
            fg=value_color,
            anchor='e'
        ).pack(side='right')
    
    def create_footer(self):
        """Crear footer con estadísticas"""
        self.footer = tk.Frame(self.main_frame, bg='#34495e', height=40)
        self.footer.pack(fill='x', side='bottom')
        self.footer.pack_propagate(False)
        
        self.stats_label = tk.Label(
            self.footer,
            text="Total productos: 0 | Stock bajo: 0 | Sin stock: 0",
            font=('Segoe UI', 9),
            bg='#34495e',
            fg='white'
        )
        self.stats_label.pack(side='left', padx=20, pady=10)
    
    # Métodos de eventos
    def on_search(self):
        """Manejar búsqueda"""
        search_term = self.search_var.get().strip()
        if self.callbacks.get('search'):
            self.callbacks['search'](search_term)
    
    def on_new_product(self):
        """Crear nuevo producto"""
        # Validar permiso primero
        if not self.has_permission('inventory.create'):
            messagebox.showerror(
                "Acceso Denegado", 
                "❌ No tienes permisos para crear productos.\n\n"
                "Contacta al administrador del sistema."
            )
            return
            
        if self.callbacks.get('create'):
            self.callbacks['create']()
    
    def on_edit_product(self):
        """Editar producto seleccionado"""
        # Validar permiso primero
        if not self.has_permission('inventory.edit'):
            messagebox.showerror(
                "Acceso Denegado", 
                "❌ No tienes permisos para editar productos.\n\n"
                "Contacta al administrador del sistema."
            )
            return
            
        if self.selected_product and self.callbacks.get('edit'):
            self.callbacks['edit'](self.selected_product)
    
    def on_delete_product(self):
        """Eliminar producto seleccionado"""
        # Validar permiso primero
        if not self.has_permission('inventory.delete'):
            messagebox.showerror(
                "Acceso Denegado", 
                "❌ No tienes permisos para eliminar productos.\n\n"
                "Contacta al administrador del sistema."
            )
            return
            
        if self.selected_product and self.callbacks.get('delete'):
            if messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Estás seguro de eliminar el producto '{self.selected_product.get('name')}'?"
            ):
                self.callbacks['delete'](self.selected_product['id'])
    
    def on_update_stock(self):
        """Actualizar stock - OBSOLETO: usar botón "Actualizar Stock" del toolbar"""
        # Este método ya no se usa porque eliminamos el botón del panel de detalles
        # El botón del toolbar ahora dirige a Gestión de Inventario
        pass
    
    def on_go_to_inventory(self):
        """Ir a Gestión de Inventario"""
        if self.callbacks.get('go_to_inventory'):
            self.callbacks['go_to_inventory']()
    
    def on_back_to_dashboard(self):
        """Regresar al Dashboard"""
        if self.callbacks.get('back_to_dashboard'):
            self.callbacks['back_to_dashboard']()
    
    def on_export(self):
        """Exportar productos"""
        if self.callbacks.get('export'):
            self.callbacks['export']()
    
    def on_product_select(self, event):
        """Manejar selección de producto"""
        selection = self.products_tree.selection()
        if selection:
            item = self.products_tree.item(selection[0])
            product_id = item['values'][0] if item['values'] else None
            
            # Buscar producto completo
            for product in self.products:
                if str(product.get('id')) == str(product_id) or product.get('sku') == product_id:
                    self.selected_product = product
                    self.show_product_details(product)
                    break
    
    # Métodos públicos
    def load_products(self, products: List[Dict[str, Any]]):
        """Cargar productos en la tabla"""
        self.products = products
        
        # Limpiar tabla
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Agregar productos
        for product in products:
            stock_qty = product.get('stock_quantity', 0)
            stock_status = product.get('stock_status', 'normal')
            
            # Determinar tag para color
            tag = 'normal'
            if stock_status == 'low_stock':
                tag = 'low_stock'
            elif stock_status == 'out_of_stock':
                tag = 'out_of_stock'
            
            # Estado visual
            status_text = '✅ Activo' if product.get('status') == 'active' else '❌ Inactivo'
            
            self.products_tree.insert(
                '',
                'end',
                values=(
                    product.get('sku', ''),
                    product.get('name', ''),
                    product.get('category_name', 'Sin categoría'),
                    stock_qty,
                    f"${product.get('price', 0):,.2f}",
                    status_text
                ),
                tags=(tag,)
            )
        
        # Actualizar estadísticas
        self.update_statistics()
    
    def update_statistics(self):
        """Actualizar estadísticas en el footer"""
        total = len(self.products)
        low_stock = len([p for p in self.products if p.get('stock_status') == 'low_stock'])
        out_of_stock = len([p for p in self.products if p.get('stock_status') == 'out_of_stock'])
        
        self.stats_label.config(
            text=f"Total productos: {total} | Stock bajo: {low_stock} | Sin stock: {out_of_stock}"
        )
    
    def load_categories(self, categories: List[Dict[str, Any]]):
        """Cargar categorías"""
        self.categories = categories
    
    def load_units(self, units: List[Dict[str, Any]]):
        """Cargar unidades"""
        self.units = units
    
    def bind_callback(self, event_name: str, callback: Callable):
        """Registrar callback"""
        self.callbacks[event_name] = callback
        
        # Crear navbar en el primer callback de navegación que se registre
        if not self.navbar_built and event_name in ['back_to_dashboard', 'new_sale', 'view_products', 'view_categories']:
            print(f"📋 Primer callback de navegación detectado: {event_name}")
            print(f"   Total callbacks hasta ahora: {len(self.callbacks)}")
            # Esperar un poco para que se registren todos los callbacks
            self.main_frame.after(100, self._try_build_navbar)
    
    def _try_build_navbar(self):
        """Intentar construir navbar después de un delay"""
        if not self.navbar_built:
            print(f"📋 Callbacks totales registrados: {len(self.callbacks)}")
            for key in self.callbacks:
                print(f"   - {key}")
            self.build_navbar()
            self.navbar_built = True
    
    def refresh(self):
        """Refrescar vista"""
        if self.callbacks.get('refresh'):
            self.callbacks['refresh']()
