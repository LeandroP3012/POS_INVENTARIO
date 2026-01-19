"""
Vista de Control de Stock - Actualización de Inventario
Permite ajustar el stock de productos de manera rápida
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, List
import unicodedata
from views.base_view import BaseView
from utils.responsive_utils import ResponsiveManager
from services.permission_service import PermissionService


class StockControlView(BaseView):
    """Vista para control y actualización de stock"""
    
    def __init__(self, root: tk.Tk, user_data: Dict[str, Any] = None):
        super().__init__(root)
        self.user_data = user_data or {}
        self.products = []
        self.filtered_products = []
        self.all_products_cache = []  # Cache completo para búsqueda incremental
        self.permission_service = PermissionService()
        self.can_manage_stock = self.has_permission('inventory.stock')
        
        # Inicializar gestor responsivo
        self.responsive = ResponsiveManager(self.root)
        
        # Callbacks
        self.on_refresh_callback = None
        self.on_search_callback = None
        self.on_update_stock_callback = None
        self.on_save_limits_callback = None
        self.on_back_callback = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """Crear widgets de la vista"""
        # Main frame
        self.main_frame = tk.Frame(self.root, bg='#ecf0f1')
        self.main_frame.pack(fill='both', expand=True)
        
        # Header
        self.create_header()
        
        # Navbar
        self.create_navbar()
        
        # Toolbar
        self.create_toolbar()
        
        # Contenido: Tabla y Panel de Actualización
        self.create_main_content()
        
        # Footer
        self.create_footer()

    def has_permission(self, permission: str) -> bool:
        """Verificar permisos usando el servicio central"""
        try:
            return self.permission_service.check_permission(self.user_data, permission)
        except Exception as exc:  # pragma: no cover - defensivo
            print(f"Error verificando permiso {permission}: {exc}")
            return False
    
    def create_header(self):
        """Crear header"""
        header = tk.Frame(self.main_frame, bg='#2c3e50', height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Título (izquierda)
        tk.Label(
            header,
            text="📊 Control de Stock",
            font=('Segoe UI', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(side='left', padx=20, pady=15)
        
        # Botón volver (derecha)
        tk.Button(
            header,
            text="⬅️ Volver",
            command=self._on_back,
            font=('Segoe UI', 10, 'bold'),
            bg='#34495e',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8
        ).pack(side='right', padx=20)
        
        # Usuario (derecha, antes del botón)
        tk.Label(
            header,
            text=f"Usuario: {self.user_data.get('full_name', 'N/A')}",
            font=('Segoe UI', 10),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack(side='right', padx=10)
    
    def create_navbar(self):
        """Crear navbar personalizado - GLOBAL para todos los módulos"""
        navbar_frame = tk.Frame(self.main_frame, bg='#2c3e50', height=50)
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
        
        # Botón Archivo
        file_btn = tk.Menubutton(buttons_container, text="📁 Archivo", **btn_style)
        file_btn.pack(side='left', padx=2)
        file_menu = tk.Menu(file_btn, tearoff=0, font=('Segoe UI', 11))
        file_btn.config(menu=file_menu)
        if self.has_permission('sales.create'):
            file_menu.add_command(label="Nueva Venta", command=self.callbacks.get('new_sale', lambda: None))
            file_menu.add_separator()
        file_menu.add_command(label="Volver al Dashboard", command=self._on_back)
        
        # Botón Ventas
        sales_btn = tk.Menubutton(buttons_container, text="💰 Ventas", **btn_style)
        sales_btn.pack(side='left', padx=2)
        sales_menu = tk.Menu(sales_btn, tearoff=0, font=('Segoe UI', 11))
        sales_btn.config(menu=sales_menu)
        if self.has_permission('sales.create'):
            sales_menu.add_command(label="Nueva Venta", command=self.callbacks.get('new_sale', lambda: None))
        if self.has_permission('sales.view'):
            sales_menu.add_command(label="Historial de Ventas", command=self.callbacks.get('sales_history', lambda: None))
        if sales_menu.index('end') is None:
            sales_menu.add_command(label="Sin accesos disponibles", state='disabled')
        
        # Botón Inventario
        inv_btn = tk.Menubutton(buttons_container, text="📦 Inventario", **btn_style)
        inv_btn.pack(side='left', padx=2)
        inv_menu = tk.Menu(inv_btn, tearoff=0, font=('Segoe UI', 11))
        inv_btn.config(menu=inv_menu)
        inv_menu.add_command(label="Ver Productos", command=self.callbacks.get('view_products', lambda: None))
        inv_menu.add_command(label="Gestionar Categorías", command=self.callbacks.get('view_categories', lambda: None))
        inv_menu.add_command(label="Control de Stock", command=self.callbacks.get('refresh', lambda: None))
        
        # Botón Reportes
        rep_btn = tk.Menubutton(buttons_container, text="📊 Reportes", **btn_style)
        rep_btn.pack(side='left', padx=2)
        rep_menu = tk.Menu(rep_btn, tearoff=0, font=('Segoe UI', 11))
        rep_btn.config(menu=rep_menu)
        rep_menu.add_command(label="Ventas del Día", command=self.callbacks.get('daily_report', lambda: None))
        rep_menu.add_command(label="Reporte Completo", command=self.callbacks.get('full_report', lambda: None))
        
        # Botón Administración
        admin_btn = tk.Menubutton(buttons_container, text="⚙️ Administración", **btn_style)
        admin_btn.pack(side='left', padx=2)
        admin_menu = tk.Menu(admin_btn, tearoff=0, font=('Segoe UI', 11))
        admin_btn.config(menu=admin_menu)
        admin_menu.add_command(label="Gestionar Usuarios", command=self.callbacks.get('manage_users', lambda: None))
        admin_menu.add_command(label="Gestionar Roles", command=self.callbacks.get('manage_roles', lambda: None))
        admin_menu.add_separator()
        admin_menu.add_command(label="Configuración", command=self.callbacks.get('system_config', lambda: None))
        
        # Botón Ayuda
        help_btn = tk.Menubutton(buttons_container, text="❓ Ayuda", **btn_style)
        help_btn.pack(side='left', padx=2)
        help_menu = tk.Menu(help_btn, tearoff=0, font=('Segoe UI', 11))
        help_btn.config(menu=help_menu)
        help_menu.add_command(label="Manual de Usuario", command=self.callbacks.get('show_manual', lambda: None))
        help_menu.add_command(label="Acerca de", command=self.callbacks.get('show_about', lambda: None))
    
    def create_toolbar(self):
        """Crear toolbar con búsqueda"""
        toolbar = tk.Frame(self.main_frame, bg='#ecf0f1', height=70)
        toolbar.pack(fill='x', pady=(0, 10))
        toolbar.pack_propagate(False)
        
        # Frame izquierdo: Búsqueda
        left_frame = tk.Frame(toolbar, bg='#ecf0f1')
        left_frame.pack(side='left', fill='y', padx=20, pady=15)
        
        tk.Label(
            left_frame,
            text="🔍 Buscar Producto:",
            font=('Segoe UI', 11, 'bold'),
            bg='#ecf0f1'
        ).pack(side='left', padx=(0, 10))
        
        self.search_var = tk.StringVar()
        try:
            self.search_var.trace_add('write', lambda *args: self.on_search())
        except Exception:
            self.search_var.trace('w', lambda *args: self.on_search())

        self.search_entry = tk.Entry(
            left_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 11),
            width=50,
            relief='solid',
            bd=1
        )
        self.search_entry.pack(side='left')
        self.search_entry.bind('<KeyRelease>', lambda e: self.on_search())
        
        # Frame derecho: Botón refrescar
        right_frame = tk.Frame(toolbar, bg='#ecf0f1')
        right_frame.pack(side='right', fill='y', padx=20, pady=15)
        
        tk.Button(
            right_frame,
            text="🔄 Refrescar",
            font=('Segoe UI', 10, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8,
            command=self.on_refresh
        ).pack(side='left', padx=5)
    
    def create_main_content(self):
        """Crear contenido principal"""
        content_frame = tk.Frame(self.main_frame, bg='#ecf0f1')
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Tabla de productos (70%)
        table_frame = tk.Frame(content_frame, bg='white', relief='solid', bd=1)
        table_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame, orient='vertical')
        x_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal')
        
        # Treeview
        columns = ('sku', 'name', 'category', 'stock', 'min_stock', 'max_stock', 'status')
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set,
            selectmode='browse'
        )
        
        # Configurar scrollbars
        y_scrollbar.config(command=self.tree.yview)
        x_scrollbar.config(command=self.tree.xview)
        
        # Encabezados
        self.tree.heading('sku', text='SKU')
        self.tree.heading('name', text='Producto')
        self.tree.heading('category', text='Categoría')
        self.tree.heading('stock', text='Stock Actual')
        self.tree.heading('min_stock', text='Stock Mín.')
        self.tree.heading('max_stock', text='Stock Máx.')
        self.tree.heading('status', text='Estado')
        
        # Anchos de columnas
        self.tree.column('sku', width=100, anchor='w')
        self.tree.column('name', width=200, anchor='w')
        self.tree.column('category', width=120, anchor='w')
        self.tree.column('stock', width=100, anchor='center')
        self.tree.column('min_stock', width=100, anchor='center')
        self.tree.column('max_stock', width=100, anchor='center')
        self.tree.column('status', width=120, anchor='center')
        
        # Grid
        self.tree.grid(row=0, column=0, sticky='nsew')
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        x_scrollbar.grid(row=1, column=0, sticky='ew')
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Bind selección
        self.tree.bind('<<TreeviewSelect>>', self.on_product_select)
        
        # Panel de actualización (30%)
        self.create_update_panel(content_frame)
    
    def create_update_panel(self, parent):
        """Crear panel de actualización de stock"""
        panel = tk.Frame(parent, bg='white', relief='solid', bd=1, width=350)
        panel.pack(side='right', fill='y')
        panel.pack_propagate(False)
        
        # Título
        title_frame = tk.Frame(panel, bg='#3498db', height=50)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="⚡ Actualizar Stock",
            font=('Segoe UI', 14, 'bold'),
            bg='#3498db',
            fg='white'
        ).pack(pady=12)
        
        # === AGREGAR CANVAS CON SCROLLBAR ===
        # Frame contenedor para canvas + scrollbar
        canvas_frame = tk.Frame(panel, bg='white')
        canvas_frame.pack(fill='both', expand=True)
        
        # Canvas
        canvas = tk.Canvas(canvas_frame, bg='white', highlightthickness=0)
        canvas.pack(side='left', fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(canvas_frame, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')
        
        # Configurar canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame interno para el contenido
        content = tk.Frame(canvas, bg='white')
        canvas_window = canvas.create_window((0, 0), window=content, anchor='nw')
        
        # Función para actualizar la región de scroll
        def on_frame_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox('all'))
            # Ajustar el ancho del frame interno al ancho del canvas
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())
        
        content.bind('<Configure>', on_frame_configure)
        canvas.bind('<Configure>', on_frame_configure)
        
        # Bind mousewheel para scroll
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        
        canvas.bind_all('<MouseWheel>', on_mousewheel)
        
        # Agregar padding
        content_inner = tk.Frame(content, bg='white')
        content_inner.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Producto seleccionado
        tk.Label(            content_inner,
            text="Producto Seleccionado:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        self.selected_product_label = tk.Label(            content_inner,
            text="Ninguno",
            font=('Segoe UI', 11),
            bg='#f8f9fa',
            fg='#7f8c8d',
            anchor='w',
            wraplength=300,
            justify='left',
            relief='solid',
            bd=1,
            padx=10,
            pady=10
        )
        self.selected_product_label.pack(fill='x', pady=(0, 20))
        
        # Stock actual
        tk.Label(            content_inner,
            text="Stock Actual:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        self.current_stock_label = tk.Label(            content_inner,
            text="0",
            font=('Segoe UI', 20, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50',
            relief='solid',
            bd=1,
            pady=15
        )
        self.current_stock_label.pack(fill='x', pady=(0, 20))
        
        # Tipo de movimiento
        tk.Label(            content_inner,
            text="Tipo de Movimiento:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        self.movement_type_var = tk.StringVar(value="entrada")
        
        self.movement_combo = ttk.Combobox(
            content_inner,
            textvariable=self.movement_type_var,
            values=[
                "entrada",
                "salida",
                "ajuste"
            ],
            state='readonly',
            font=('Segoe UI', 11),
            width=25
        )
        self.movement_combo.pack(fill='x', pady=(0, 5))
        self.movement_combo.current(0)  # Establecer 'entrada' como selección inicial
        
        # Descripción del tipo seleccionado
        movement_descriptions = {
            'entrada': '📥 Agregar productos al inventario',
            'salida': '📤 Restar productos del inventario',
            'ajuste': '✏️ Establecer cantidad exacta de stock'
        }
        
        self.movement_desc_label = tk.Label(
            content_inner,
            text=movement_descriptions['entrada'],
            font=('Segoe UI', 9, 'italic'),
            bg='white',
            fg='#7f8c8d',
            anchor='w',
            wraplength=280
        )
        self.movement_desc_label.pack(fill='x', pady=(0, 20))
        
        # Actualizar descripción cuando cambie la selección
        def on_movement_change(event=None):
            selected = self.movement_type_var.get()
            self.movement_desc_label.config(text=movement_descriptions.get(selected, ''))
        
        self.movement_combo.bind('<<ComboboxSelected>>', on_movement_change)
        
        # Cantidad
        tk.Label(            content_inner,
            text="Cantidad:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        self.quantity_var = tk.StringVar(value="0")
        
        self.quantity_entry = tk.Entry(            content_inner,
            textvariable=self.quantity_var,
            font=('Segoe UI', 14),
            relief='solid',
            bd=1,
            justify='center'
        )
        self.quantity_entry.pack(fill='x', pady=(0, 20))
        
        # === STOCK MÍNIMO Y MÁXIMO ===
        stock_limits_frame = tk.Frame(content_inner, bg='#e8f5e9', relief='solid', bd=1)
        stock_limits_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            stock_limits_frame,
            text="📊 Límites de Stock",
            font=('Segoe UI', 10, 'bold'),
            bg='#e8f5e9',
            fg='#2e7d32'
        ).pack(fill='x', padx=10, pady=(10, 5))
        
        # Frame para min y max en dos columnas
        limits_row = tk.Frame(stock_limits_frame, bg='#e8f5e9')
        limits_row.pack(fill='x', padx=10, pady=(0, 10))
        
        # Columna Stock Mínimo
        min_col = tk.Frame(limits_row, bg='#e8f5e9')
        min_col.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        tk.Label(
            min_col,
            text="Stock Mínimo:",
            font=('Segoe UI', 9),
            bg='#e8f5e9',
            fg='#2e7d32'
        ).pack(anchor='w')
        
        self.min_stock_var = tk.StringVar(value="0")
        self.min_stock_entry = tk.Entry(
            min_col,
            textvariable=self.min_stock_var,
            font=('Segoe UI', 11),
            relief='solid',
            bd=1,
            justify='center'
        )
        self.min_stock_entry.pack(fill='x')
        
        # Columna Stock Máximo
        max_col = tk.Frame(limits_row, bg='#e8f5e9')
        max_col.pack(side='left', fill='x', expand=True, padx=(5, 0))
        
        tk.Label(
            max_col,
            text="Stock Máximo:",
            font=('Segoe UI', 9),
            bg='#e8f5e9',
            fg='#2e7d32'
        ).pack(anchor='w')
        
        self.max_stock_var = tk.StringVar(value="0")
        self.max_stock_entry = tk.Entry(
            max_col,
            textvariable=self.max_stock_var,
            font=('Segoe UI', 11),
            relief='solid',
            bd=1,
            justify='center'
        )
        self.max_stock_entry.pack(fill='x')
        
        # Botón para guardar solo los límites
        save_limits_btn = tk.Button(
            stock_limits_frame,
            text="💾 Guardar Límites",
            font=('Segoe UI', 10, 'bold'),
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8,
            command=self.on_save_limits,
            state='disabled'
        )
        save_limits_btn.pack(fill='x', padx=10, pady=(5, 10))
        self.save_limits_button = save_limits_btn
        
        # Separador
        tk.Frame(content_inner, bg='#bdc3c7', height=1).pack(fill='x', pady=15)
        
        # Motivo/Notas
        tk.Label(            content_inner,
            text="Motivo (opcional):",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        self.reason_text = tk.Text(
            content,
            height=3,
            font=('Segoe UI', 10),
            relief='solid',
            bd=1,
            wrap='word'
        )
        self.reason_text.pack(fill='x', pady=(0, 20))
        
        # Botón actualizar stock
        self.update_button = tk.Button(
            content,
            text="� Actualizar Stock",
            font=('Segoe UI', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=12,
            command=self.on_update_stock,
            state='disabled'
        )
        self.update_button.pack(fill='x')
    
    def create_footer(self):
        """Crear footer con estadísticas"""
        footer = tk.Frame(self.main_frame, bg='#2c3e50', height=50)
        footer.pack(fill='x', side='bottom')
        footer.pack_propagate(False)
        
        self.stats_label = tk.Label(
            footer,
            text="Total: 0 productos",
            font=('Segoe UI', 10),
            bg='#2c3e50',
            fg='white'
        )
        self.stats_label.pack(side='left', padx=20, pady=10)
    
    # Métodos de eventos
    def on_refresh(self):
        """Refrescar lista de productos"""
        if self.on_refresh_callback:
            self.on_refresh_callback()
    
    def on_search(self):
        """Buscar productos"""
        # Leer directo del widget para evitar quedarnos sin texto en algunos entornos
        if hasattr(self, 'search_entry'):
            search_term = self.search_entry.get().strip()
        else:
            search_term = self.search_var.get().strip()

        # Filtro inmediato local (SKU o Nombre, sin acentos)
        self._filter_products_local(search_term)

        # Notificar al controlador si hay callback
        if self.on_search_callback:
            self.on_search_callback(search_term)
    
    def on_product_select(self, event):
        """Manejar selección de producto"""
        selection = self.tree.selection()
        if not selection:
            self.selected_product_label.config(text="Ninguno", fg='#7f8c8d')
            self.current_stock_label.config(text="0")
            self.min_stock_var.set("0")
            self.max_stock_var.set("0")
            self.update_button.config(state='disabled')
            self.save_limits_button.config(state='disabled')
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        
        # Mostrar producto seleccionado
        product_name = f"{values[0]} - {values[1]}"
        self.selected_product_label.config(text=product_name, fg='#2c3e50')
        
        # Mostrar stock actual
        current_stock = values[3]
        self.current_stock_label.config(text=str(current_stock))
        
        # Cargar stock mínimo y máximo
        min_stock = values[4] if len(values) > 4 else 0
        max_stock = values[5] if len(values) > 5 else 0
        self.min_stock_var.set(str(min_stock))
        self.max_stock_var.set(str(max_stock))
        
        # Habilitar botones
        self.update_button.config(state='normal' if self.can_manage_stock else 'disabled')
        self.save_limits_button.config(state='normal')
    
    def on_update_stock(self):
        """Actualizar stock del producto seleccionado"""
        print("\n" + "="*60)
        print("🔍 DEBUG: Iniciando actualización de stock")
        print("="*60)

        if not self.can_manage_stock:
            messagebox.showerror("Permisos", "No tienes permiso para ajustar stock")
            return
        
        selection = self.tree.selection()
        if not selection:
            print("❌ No hay producto seleccionado")
            messagebox.showwarning("Selección", "Seleccione un producto primero")
            return
        
        print(f"✅ Producto seleccionado: {selection[0]}")
        
        # DEBUG: Leer DIRECTAMENTE de los widgets
        print(f"\n📊 VALORES DE WIDGETS:")
        quantity_from_entry = self.quantity_entry.get()
        quantity_from_var = self.quantity_var.get()
        movement_from_combo = self.movement_combo.get()
        movement_from_var = self.movement_type_var.get()
        
        print(f"   quantity_entry.get(): '{quantity_from_entry}'")
        print(f"   quantity_var.get(): '{quantity_from_var}'")
        print(f"   movement_combo.get(): '{movement_from_combo}'")
        print(f"   movement_type_var.get(): '{movement_from_var}'")
        
        # Validar cantidad
        try:
            # USAR VALORES DE LOS WIDGETS DIRECTAMENTE (no de StringVar)
            quantity_str = quantity_from_entry
            quantity = float(quantity_str) if quantity_str.strip() else 0.0
            movement_type = movement_from_combo.strip().lower()  # Leer directamente del Combobox
            
            print(f"\n📊 VALORES PROCESADOS:")
            print(f"   Cantidad: {quantity}")
            print(f"   Tipo de movimiento: '{movement_type}' (len={len(movement_type)})")
            print(f"   Es 'entrada': {movement_type == 'entrada'}")
            print(f"   Es 'salida': {movement_type == 'salida'}")
            print(f"   Es 'ajuste': {movement_type == 'ajuste'}")
            
            # Validación: Para entrada y salida, debe ser > 0
            # Para ajuste manual, puede ser cualquier valor (incluso 0 o negativo para resetear)
            if movement_type in ["entrada", "salida"] and quantity <= 0:
                print(f"❌ Validación fallida: cantidad debe ser > 0")
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return
            
            print(f"✅ Validación de cantidad pasada")
            
        except ValueError as e:
            print(f"❌ Error al convertir cantidad: {e}")
            messagebox.showerror("Error", "Ingrese una cantidad válida")
            return
        
        # Validar stock mínimo y máximo
        try:
            # LEER DIRECTAMENTE DE LOS ENTRY WIDGETS
            min_stock_str = self.min_stock_entry.get()
            max_stock_str = self.max_stock_entry.get()
            
            min_stock = float(min_stock_str) if min_stock_str.strip() else 0.0
            max_stock = float(max_stock_str) if max_stock_str.strip() else 0.0
            
            print(f"\n📊 LÍMITES DE STOCK:")
            print(f"   Stock mínimo: {min_stock}")
            print(f"   Stock máximo: {max_stock}")
            
            if min_stock < 0 or max_stock < 0:
                print(f"❌ Validación fallida: valores negativos")
                messagebox.showerror("Error", "Los valores de stock mínimo y máximo no pueden ser negativos")
                return
            
            if max_stock > 0 and min_stock > max_stock:
                print(f"❌ Validación fallida: mínimo > máximo")
                messagebox.showerror("Error", "El stock mínimo no puede ser mayor al stock máximo")
                return
            
            print(f"✅ Validación de límites pasada")
                
        except ValueError as e:
            print(f"❌ Error al convertir límites: {e}")
            messagebox.showerror("Error", "Ingrese valores numéricos válidos para stock mínimo y máximo")
            return
        
        # Obtener SKU del producto
        item = self.tree.item(selection[0])
        product_sku = item['values'][0]
        
        print(f"📦 SKU del producto: {product_sku}")
        
        # Obtener motivo
        reason = self.reason_text.get('1.0', tk.END).strip()
        
        print(f"📝 Motivo: '{reason}'")
        
        # Preparar datos
        update_data = {
            'sku': product_sku,
            'movement_type': movement_type,
            'quantity': quantity,
            'reason': reason,
            'min_stock': min_stock,
            'max_stock': max_stock
        }
        
        print(f"\n📦 Datos preparados para enviar:")
        for key, value in update_data.items():
            print(f"   {key}: {value}")
        
        # Ejecutar callback
        print(f"\n🔄 Ejecutando callback...")
        print(f"   Callback existe: {self.on_update_stock_callback is not None}")
        
        if self.on_update_stock_callback:
            print(f"   ✅ Llamando al callback...")
            self.on_update_stock_callback(update_data)
            print(f"   ✅ Callback ejecutado")
        else:
            print(f"   ❌ ERROR: No hay callback registrado!")
        
        print("="*60 + "\n")
    
    def on_save_limits(self):
        """Guardar solo los límites de stock (mín/máx) sin afectar el stock actual"""
        print("\n" + "="*60)
        print("🔍 DEBUG: Guardando límites de stock")
        print("="*60)
        
        selection = self.tree.selection()
        if not selection:
            print("❌ No hay producto seleccionado")
            messagebox.showwarning("Selección", "Seleccione un producto primero")
            return
        
        # DEBUG: Leer DIRECTAMENTE de los Entry widgets
        print(f"\n📊 VALORES DE ENTRY WIDGETS:")
        min_stock_from_entry = self.min_stock_entry.get()
        max_stock_from_entry = self.max_stock_entry.get()
        print(f"   min_stock_entry.get(): '{min_stock_from_entry}'")
        print(f"   max_stock_entry.get(): '{max_stock_from_entry}'")
        
        print(f"\n📊 VALORES DE STRINGVAR:")
        print(f"   min_stock_var.get(): '{self.min_stock_var.get()}'")
        print(f"   max_stock_var.get(): '{self.max_stock_var.get()}'")
        
        # Validar stock mínimo y máximo
        try:
            # USAR VALORES DEL ENTRY DIRECTAMENTE (no del StringVar)
            min_stock_str = min_stock_from_entry
            max_stock_str = max_stock_from_entry
            
            print(f"\n📊 VALORES SELECCIONADOS (de Entry):")
            print(f"   min_stock_str: '{min_stock_str}' (len={len(min_stock_str)})")
            print(f"   max_stock_str: '{max_stock_str}' (len={len(max_stock_str)})")
            
            # Convertir a float, usar 0 si está vacío
            min_stock = float(min_stock_str) if min_stock_str.strip() else 0.0
            max_stock = float(max_stock_str) if max_stock_str.strip() else 0.0
            
            print(f"\n📊 VALORES CONVERTIDOS:")
            print(f"   Stock mínimo: {min_stock}")
            print(f"   Stock máximo: {max_stock}")
            
            if min_stock < 0 or max_stock < 0:
                print(f"❌ Validación fallida: valores negativos")
                messagebox.showerror("Error", "Los valores no pueden ser negativos")
                return
            
            if max_stock > 0 and min_stock > max_stock:
                print(f"❌ Validación fallida: mínimo > máximo")
                messagebox.showerror("Error", "El stock mínimo no puede ser mayor al máximo")
                return
            
            print(f"✅ Validación pasada")
                
        except ValueError as e:
            print(f"❌ Error al convertir valores: {e}")
            messagebox.showerror("Error", "Ingrese valores numéricos válidos")
            return
        
        # Obtener SKU del producto
        item = self.tree.item(selection[0])
        product_sku = item['values'][0]
        
        print(f"📦 SKU del producto: {product_sku}")
        
        # Preparar datos
        limits_data = {
            'sku': product_sku,
            'min_stock': min_stock,
            'max_stock': max_stock
        }
        
        print(f"\n📦 Datos de límites:")
        print(f"   SKU: {product_sku}")
        print(f"   Min: {min_stock}")
        print(f"   Max: {max_stock}")
        
        # Ejecutar callback
        if self.on_save_limits_callback:
            print(f"✅ Ejecutando callback de límites...")
            self.on_save_limits_callback(limits_data)
            print(f"✅ Callback ejecutado")
        else:
            print(f"❌ ERROR: No hay callback de límites registrado!")
        
        print("="*60 + "\n")
    
    def _on_back(self):
        """Volver al dashboard"""
        if self.on_back_callback:
            self.on_back_callback()
    
    # Métodos públicos
    def load_products(self, products: List[Dict[str, Any]]):
        """Cargar productos; refrescar cache solo si no hay búsqueda activa"""
        current_term = ''
        if hasattr(self, 'search_entry'):
            current_term = self.search_entry.get().strip()
        elif hasattr(self, 'search_var'):
            current_term = self.search_var.get().strip()

        if current_term:
            # No sobrescribir cache completo mientras hay búsqueda activa
            self._render_products(products)
        else:
            self.all_products_cache = list(products) if products else []
            self._render_products(products)

    def _render_products(self, products: List[Dict[str, Any]]):
        """Renderizar productos en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.products = products or []
        self.filtered_products = self.products

        # Insertar productos
        for product in self.products:
            stock = product.get('stock_quantity', 0)
            min_stock = product.get('min_stock', 0)
            max_stock = product.get('max_stock', 0)

            if stock == 0:
                status = "🚫 Agotado"
                tag = 'out_of_stock'
            elif stock <= min_stock:
                status = "⚠️ Bajo"
                tag = 'low_stock'
            elif stock >= max_stock and max_stock > 0:
                status = "📦 Exceso"
                tag = 'over_stock'
            else:
                status = "✅ Normal"
                tag = 'normal'

            self.tree.insert('', 'end', values=(
                product.get('sku', ''),
                product.get('name', ''),
                product.get('category_name', ''),
                stock,
                min_stock,
                max_stock,
                status
            ), tags=(tag,))

        # Configurar colores
        self.tree.tag_configure('out_of_stock', background='#ffebee')
        self.tree.tag_configure('low_stock', background='#fff3cd')
        self.tree.tag_configure('over_stock', background='#e3f2fd')
        self.tree.tag_configure('normal', background='white')

        # Actualizar estadísticas
        self.update_statistics()

    def _filter_products_local(self, search_term: str):
        """Filtrado local por SKU o Nombre, sin acentos"""
        if not search_term:
            self.filtered_products = self.all_products_cache
            self._render_products(self.all_products_cache)
            return

        term = self._normalize_text(search_term)
        filtered = [
            p for p in self.all_products_cache
            if term in self._normalize_text(str(p.get('sku', '')))
            or term in self._normalize_text(str(p.get('name', '')))
        ]

        self.filtered_products = filtered
        self._render_products(filtered)

    def _normalize_text(self, text: str) -> str:
        """Normaliza texto a minúsculas y sin acentos"""
        if not text:
            return ''
        normalized = unicodedata.normalize('NFD', text)
        return ''.join(ch for ch in normalized if unicodedata.category(ch) != 'Mn').lower()
    
    def update_statistics(self):
        """Actualizar estadísticas"""
        total = len(self.filtered_products)
        self.stats_label.config(text=f"Total: {total} productos")
    
    def clear_form(self):
        """Limpiar formulario de actualización"""
        self.quantity_var.set("0")
        self.reason_text.delete('1.0', tk.END)
        self.movement_type_var.set("entrada")
        # Mantener los valores de min/max stock después de actualizar
        # ya que se actualizan automáticamente al seleccionar el producto
    
    def register_callbacks(self, refresh, search, update_stock, save_limits, back=None):
        """Registrar callbacks"""
        self.on_refresh_callback = refresh
        self.on_search_callback = search
        self.on_update_stock_callback = update_stock
        self.on_save_limits_callback = save_limits
        self.on_back_callback = back

