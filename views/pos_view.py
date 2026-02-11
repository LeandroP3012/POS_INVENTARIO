"""
Vista de Punto de Venta (POS)
Sistema de ventas con carrito y procesamiento de pagos
Autor: Sistema POS
Fecha: 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from decimal import Decimal
import logging
from utils.responsive_utils import ResponsiveManager

class POSView:
    """Vista del Punto de Venta"""
    
    def __init__(self, parent, controller, user_data, on_back=None):
        self.parent = parent
        self.controller = controller
        self.user_data = user_data
        self.on_back = on_back
        
        # Inicializar gestor responsivo
        self.responsive = ResponsiveManager(parent)
        
        # Estado del carrito
        self.cart_items = []
        self.current_customer = None
        
        # Variables de cálculo
        self.current_total = 0.0
        
        # Configurar viewport responsivo
        self._configure_viewport()

        self.setup_ui()

    def _configure_viewport(self):
        """Adaptar la vista para resoluciones medias como 1366x768."""
        master = self.parent.winfo_toplevel() if hasattr(self.parent, 'winfo_toplevel') else self.parent

        try:
            screen_w = master.winfo_screenwidth()
            screen_h = master.winfo_screenheight()
        except Exception:
            screen_w, screen_h = 1366, 768

        # Calcular dimensiones responsivas basadas en pantalla real
        base_width, base_height = self.responsive.get_window_size()
        margin = 40
        usable_width = min(int(screen_w * 0.92), screen_w - margin)
        usable_height = min(int(screen_h * 0.9), screen_h - margin)

        target_width = max(min(usable_width, screen_w - margin), min(base_width, screen_w - margin))
        target_height = max(min(usable_height, screen_h - margin), min(int(base_height * 0.9), screen_h - margin))

        min_width = max(min(base_width, screen_w - margin), 1100)
        min_height = max(min(int(base_height * 0.75), screen_h - margin), 640)

        try:
            master.minsize(min_width, min_height)
            master.geometry(f"{target_width}x{target_height}")
        except Exception:
            pass

        self.viewport_container = tk.Frame(self.parent, bg='#ecf0f1')
        self.viewport_container.pack(fill='both', expand=True)

        self._viewport_canvas = tk.Canvas(
            self.viewport_container,
            bg='#ecf0f1',
            highlightthickness=0
        )
        v_scroll = ttk.Scrollbar(
            self.viewport_container,
            orient='vertical',
            command=self._viewport_canvas.yview
        )
        self._viewport_canvas.configure(yscrollcommand=v_scroll.set)

        self._viewport_canvas.pack(side='left', fill='both', expand=True)
        v_scroll.pack(side='right', fill='y')

        self.main_frame = tk.Frame(self._viewport_canvas, bg='#ecf0f1')
        self._viewport_window = self._viewport_canvas.create_window((0, 0), window=self.main_frame, anchor='nw')

        def _update_scroll_region(_event=None):
            self._viewport_canvas.configure(scrollregion=self._viewport_canvas.bbox('all'))
            self._ensure_content_height()

        self.main_frame.bind('<Configure>', _update_scroll_region)

        def _on_mousewheel(event):
            canvas = getattr(self, '_viewport_canvas', None)
            if canvas is None:
                return
            try:
                if not canvas.winfo_exists():
                    self._unbind_mousewheel()
                    return
            except Exception:
                return
            try:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
            except tk.TclError:
                self._unbind_mousewheel()

        self._viewport_canvas.bind_all('<MouseWheel>', _on_mousewheel)
        self._mousewheel_handler = _on_mousewheel

        # Ajustar altura inicial cuando el canvas cambie de tamaño
        self._viewport_canvas.bind('<Configure>', lambda _e: self._ensure_content_height())

        # Asegurar limpieza cuando se destruya la ventana
        self.parent.bind('<Destroy>', self._on_parent_destroy)

    def _ensure_content_height(self):
        """Asegurar que el contenido cubra toda la altura disponible"""
        if not hasattr(self, '_viewport_canvas') or not hasattr(self, '_viewport_window'):
            return

        self.main_frame.update_idletasks()
        content_height = self.main_frame.winfo_reqheight()
        viewport_height = max(self._viewport_canvas.winfo_height(), 600)
        target_height = max(content_height, viewport_height)

        try:
            self._viewport_canvas.itemconfigure(self._viewport_window, height=target_height)
        except Exception:
            pass

    def _unbind_mousewheel(self):
        """Eliminar binding global del mousewheel si sigue activo"""
        if getattr(self, '_mousewheel_handler', None) is None:
            return
        try:
            self.parent.unbind_all('<MouseWheel>')
        except Exception:
            pass
        self._mousewheel_handler = None

    def _on_parent_destroy(self, event):
        """Limpiar bindings cuando el contenedor se destruye"""
        # Solo interesa cuando se destruye la ventana principal
        if event.widget is self.parent or event.widget is getattr(self.parent, 'winfo_toplevel', lambda: None)():
            self._unbind_mousewheel()

    def setup_ui(self):
        """Configura la interfaz completa"""
        # Header
        self.create_header()
        
        # Contenedor principal (3 columnas)
        content_frame = tk.Frame(self.main_frame, bg='#ecf0f1')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)

        content_frame.columnconfigure(0, weight=3)
        content_frame.columnconfigure(1, weight=2)
        content_frame.columnconfigure(2, weight=0)
        content_frame.rowconfigure(0, weight=1)

        # Columna izquierda: Búsqueda y productos
        left_frame = tk.Frame(content_frame, bg='white', relief='solid', borderwidth=1)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        self.create_search_section(left_frame)
        
        # Columna central: Carrito
        center_frame = tk.Frame(content_frame, bg='white', relief='solid', borderwidth=1)
        center_frame.grid(row=0, column=1, sticky='nsew', padx=5)
        self.create_cart_section(center_frame)
        
        # Columna derecha: Totales y pago
        right_frame = tk.Frame(content_frame, bg='white', relief='solid', borderwidth=1, width=360)
        right_frame.grid(row=0, column=2, sticky='ns', padx=(5, 0))
        right_frame.grid_propagate(False)
        self.create_totals_section(right_frame)

        # Ajustar altura una vez montada la interfaz
        self.parent.after(200, self._ensure_content_height)
    
    def create_header(self):
        """Crea el header con información del cajero"""
        header = tk.Frame(self.main_frame, bg='#2c3e50', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Título
        title_label = tk.Label(
            header,
            text="💰 PUNTO DE VENTA",
            font=('Segoe UI', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(side='left', padx=20, pady=10)
        
        # Info del usuario
        user_info = tk.Frame(header, bg='#2c3e50')
        user_info.pack(side='right', padx=20, pady=10)
        
        tk.Label(
            user_info,
            text=f"👤 Cajero: {self.user_data.get('full_name', 'Usuario')}",
            font=('Segoe UI', 10),
            bg='#2c3e50',
            fg='white'
        ).pack()
        
        tk.Label(
            user_info,
            text=f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            font=('Segoe UI', 9),
            bg='#2c3e50',
            fg='#bdc3c7'
        ).pack()
        
        # Botón volver
        if self.on_back:
            back_btn = tk.Button(
                header,
                text="⬅️ Volver",
                command=self.on_back,
                font=('Segoe UI', 10),
                bg='#34495e',
                fg='white',
                relief='flat',
                padx=15,
                pady=5,
                cursor='hand2'
            )
            back_btn.pack(side='right', padx=10)
    
    def create_search_section(self, parent):
        """Crea sección de búsqueda de productos"""
        # Header de búsqueda
        search_header = tk.Frame(parent, bg='#3498db', height=50)
        search_header.pack(fill='x')
        search_header.pack_propagate(False)
        
        tk.Label(
            search_header,
            text="🔍  BUSCAR PRODUCTOS",
            font=('Segoe UI', 13, 'bold'),
            bg='#3498db',
            fg='white'
        ).pack(side='left', padx=15, pady=12)
        
        # Frame de búsqueda
        search_frame = tk.Frame(parent, bg='white')
        search_frame.pack(fill='x', padx=10, pady=10)
        
        # Campo de búsqueda con mejor diseño
        self.search_var = tk.StringVar()
        
        # Variable para controlar el delay de búsqueda
        self.search_timer = None
        
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 12),
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightcolor='#3498db',
            highlightbackground='#bdc3c7'
        )
        self.search_entry.pack(fill='x', pady=(0, 5), ipady=5)
        self.search_entry.focus()
        
        # USAR KeyRelease en lugar de trace para búsqueda autoincremental
        self.search_entry.bind('<KeyRelease>', lambda e: self.on_search_change())
        
        # Bind enter para agregar rápido
        # MODIFICADO: Ejecutar búsqueda síncrona antes de agregar
        self.search_entry.bind('<Return>', lambda e: self.quick_add_product_with_search())
        
        # Instrucciones mejoradas
        instruction_frame = tk.Frame(search_frame, bg='#e8f4f8', relief='solid', borderwidth=1)
        instruction_frame.pack(fill='x', pady=(5, 0), padx=1)
        
        tk.Label(
            instruction_frame,
            text="💡 Busca por nombre, SKU o código de barras | Enter: Agregar | Doble click: Seleccionar",
            font=('Segoe UI', 8),
            bg='#e8f4f8',
            fg='#2c3e50',
            anchor='w'
        ).pack(padx=8, pady=5)
        
        # Tabla de productos (Treeview como el carrito)
        tree_frame = tk.Frame(parent, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Scrollbars
        scrollbar_y = tk.Scrollbar(tree_frame)
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x = tk.Scrollbar(tree_frame, orient='horizontal')
        
        # Treeview de productos
        columns = ('sku', 'name', 'price', 'stock')
        self.products_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=15,
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        # Configurar columnas
        self.products_tree.heading('sku', text='SKU')
        self.products_tree.heading('name', text='Nombre del Producto')
        self.products_tree.heading('price', text='Precio')
        self.products_tree.heading('stock', text='Stock')
        
        self.products_tree.column('sku', width=120, anchor='w')
        self.products_tree.column('name', width=300, anchor='w')
        self.products_tree.column('price', width=100, anchor='e')
        self.products_tree.column('stock', width=80, anchor='center')
        
        self.products_tree.pack(fill='both', expand=True)
        scrollbar_x.pack(side='bottom', fill='x')
        scrollbar_y.config(command=self.products_tree.yview)
        scrollbar_x.config(command=self.products_tree.xview)
        
        # Estilos para el Treeview
        style = ttk.Style()
        style.configure("Treeview",
            background="#ffffff",
            foreground="#2c3e50",
            rowheight=30,
            fieldbackground="#ffffff",
            font=('Segoe UI', 10)
        )
        style.configure("Treeview.Heading",
            font=('Segoe UI', 10, 'bold'),
            background="#3498db",
            foreground="#ffffff"
        )
        style.map('Treeview', background=[('selected', '#3498db')])
        
        # Bind doble click y Enter para agregar
        self.products_tree.bind('<Double-Button-1>', lambda e: self.add_selected_product())
        self.products_tree.bind('<Return>', lambda e: self.add_selected_product())
        
        # Footer con total de productos y botón
        footer_frame = tk.Frame(parent, bg='white')
        footer_frame.pack(fill='x', padx=10, pady=(5, 10))
        
        # Label de total de productos (izquierda)
        self.products_count_label = tk.Label(
            footer_frame,
            text="📦 Total: 0 productos disponibles",
            font=('Segoe UI', 9),
            bg='white',
            fg='#7f8c8d'
        )
        self.products_count_label.pack(side='left')
        
        # Leyenda de stock (centro)
        legend_label = tk.Label(
            footer_frame,
            text="🟢 Stock OK  |  🟡 Stock Bajo  |  🔴 Stock Crítico",
            font=('Segoe UI', 8),
            bg='white',
            fg='#7f8c8d'
        )
        legend_label.pack(side='left', padx=20)
        
        # Botón agregar
        add_btn = tk.Button(
            footer_frame,
            text="➕ Agregar al Carrito",
            command=self.add_selected_product,
            font=('Segoe UI', 10, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2'
        )
        add_btn.pack(side='right')
        
        # Efecto hover para el botón
        add_btn.bind('<Enter>', lambda e: add_btn.config(bg='#2980b9'))
        add_btn.bind('<Leave>', lambda e: add_btn.config(bg='#3498db'))
        
        # Inicializar diccionario de productos
        self.product_data = {}
        
        # ✅ NO cargar productos aquí - esperar a que se muestre la vista
        
    def create_cart_section(self, parent):
        """Crea sección del carrito de compras"""
        # Header del carrito
        cart_header = tk.Frame(parent, bg='#e74c3c', height=50)
        cart_header.pack(fill='x')
        cart_header.pack_propagate(False)
        
        tk.Label(
            cart_header,
            text="🛒  CARRITO DE COMPRAS",
            font=('Segoe UI', 13, 'bold'),
            bg='#e74c3c',
            fg='white'
        ).pack(side='left', padx=15, pady=12)
        
        self.cart_count_label = tk.Label(
            cart_header,
            text="🛒 Carrito vacío",
            font=('Segoe UI', 10),
            bg='#e74c3c',
            fg='white'
        )
        self.cart_count_label.pack(side='right', padx=15)
        
        # Cliente seleccionado
        customer_frame = tk.Frame(parent, bg='#ecf0f1')
        customer_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            customer_frame,
            text="👤 Cliente:",
            font=('Segoe UI', 9, 'bold'),
            bg='#ecf0f1'
        ).pack(side='left')
        
        self.customer_label = tk.Label(
            customer_frame,
            text="Cliente Genérico",
            font=('Segoe UI', 9),
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        self.customer_label.pack(side='left', padx=5)
        
        # Botón cambiar cliente
        tk.Button(
            customer_frame,
            text="Cambiar",
            command=self.select_customer,
            font=('Segoe UI', 8),
            bg='#3498db',
            fg='white',
            relief='flat',
            cursor='hand2'
        ).pack(side='right')
        
        # Treeview del carrito
        tree_frame = tk.Frame(parent, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Scrollbars
        scrollbar_y = tk.Scrollbar(tree_frame)
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x = tk.Scrollbar(tree_frame, orient='horizontal')
        
        # Treeview
        columns = ('Producto', 'Cant.', 'Precio', 'Subtotal')
        self.cart_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=15,
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        # Configurar columnas
        self.cart_tree.heading('Producto', text='Producto')
        self.cart_tree.heading('Cant.', text='Cant.')
        self.cart_tree.heading('Precio', text='Precio')
        self.cart_tree.heading('Subtotal', text='Subtotal')
        
        self.cart_tree.column('Producto', width=200)
        self.cart_tree.column('Cant.', width=60, anchor='center')
        self.cart_tree.column('Precio', width=80, anchor='e')
        self.cart_tree.column('Subtotal', width=100, anchor='e')
        
        self.cart_tree.pack(fill='both', expand=True)
        scrollbar_x.pack(side='bottom', fill='x')
        scrollbar_y.config(command=self.cart_tree.yview)
        scrollbar_x.config(command=self.cart_tree.xview)
        
        # ✅ AGREGAR EVENTO DE DOBLE CLIC PARA EDITAR CANTIDAD
        self.cart_tree.bind('<Double-Button-1>', lambda e: self.edit_quantity())
        
        # Botones de carrito
        buttons_frame = tk.Frame(parent, bg='white')
        buttons_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Button(
            buttons_frame,
            text="➖ Quitar",
            command=self.remove_from_cart,
            font=('Segoe UI', 9),
            bg='#e67e22',
            fg='white',
            relief='flat',
            padx=10,
            cursor='hand2'
        ).pack(side='left', padx=2)
        
        tk.Button(
            buttons_frame,
            text="✏️ Editar Cantidad",
            command=self.edit_quantity,
            font=('Segoe UI', 9),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=10,
            cursor='hand2'
        ).pack(side='left', padx=2)
        
        tk.Button(
            buttons_frame,
            text="🗑️ Vaciar Carrito",
            command=self.clear_cart,
            font=('Segoe UI', 9),
            bg='#c0392b',
            fg='white',
            relief='flat',
            padx=10,
            cursor='hand2'
        ).pack(side='right', padx=2)
    
    def create_totals_section(self, parent):
        """Crea sección de totales y pago"""
        # Header
        totals_header = tk.Frame(parent, bg='#27ae60', height=50)
        totals_header.pack(fill='x')
        totals_header.pack_propagate(False)
        
        tk.Label(
            totals_header,
            text="💵  TOTALES Y PAGO",
            font=('Segoe UI', 13, 'bold'),
            bg='#27ae60',
            fg='white'
        ).pack(padx=15, pady=12)
        
        # Frame de totales
        totals_frame = tk.Frame(parent, bg='white')
        totals_frame.pack(fill='x', padx=15, pady=15)
        
        # Subtotal
        self.create_total_row(totals_frame, "Subtotal:", "0.00", 'subtotal')
        
        # Descuento
        discount_frame = tk.Frame(totals_frame, bg='white')
        discount_frame.pack(fill='x', pady=5)
        
        tk.Label(
            discount_frame,
            text="Descuento:",
            font=('Segoe UI', 11),
            bg='white'
        ).pack(side='left')
        
        self.discount_var = tk.StringVar(value="0.00")
        self.discount_entry = tk.Entry(
            discount_frame,
            textvariable=self.discount_var,
            font=('Segoe UI', 11),
            width=10,
            justify='right',
            relief='solid',
            borderwidth=1,
            highlightthickness=1,
            highlightcolor='#3498db',
            highlightbackground='#bdc3c7'
        )
        self.discount_entry.pack(side='right', ipady=2)
        self.discount_entry.bind('<KeyRelease>', lambda e: self.calculate_totals())
        
        # ===== TOGGLE SWITCH IGV =====
        igv_frame = tk.Frame(totals_frame, bg='white')
        igv_frame.pack(fill='x', pady=8)
        
        # Label IGV
        tk.Label(
            igv_frame,
            text="IGV:",
            font=('Segoe UI', 11, 'bold'),
            bg='white'
        ).pack(side='left')
        
        # Variable para el toggle
        self.include_tax_var = tk.BooleanVar(value=False)  # ✅ DESACTIVADO POR DEFECTO
        
        # Frame del toggle switch personalizado
        toggle_frame = tk.Frame(igv_frame, bg='white')
        toggle_frame.pack(side='left', padx=10)
        
        # Canvas para el toggle switch
        self.toggle_canvas = tk.Canvas(
            toggle_frame,
            width=50,
            height=24,
            bg='white',
            highlightthickness=0,
            cursor='hand2'
        )
        self.toggle_canvas.pack(side='left')
        
        # Dibujar el toggle switch - ESTADO INICIAL OFF
        self.toggle_bg = self.toggle_canvas.create_oval(2, 2, 48, 22, fill='#95a5a6', outline='')  # Gris cuando OFF
        self.toggle_circle = self.toggle_canvas.create_oval(6, 4, 22, 20, fill='white', outline='')  # Círculo a la izquierda
        
        # Bind click en el toggle
        self.toggle_canvas.bind('<Button-1>', self.toggle_tax)
        
        # Label de estado
        self.tax_status_label = tk.Label(
            toggle_frame,
            text="OFF",  # Estado inicial OFF
            font=('Segoe UI', 9, 'bold'),
            bg='white',
            fg='#95a5a6'  # Gris cuando OFF
        )
        self.tax_status_label.pack(side='left', padx=5)
        
        # Label de monto IGV (a la derecha)
        self.tax_label = tk.Label(
            igv_frame,
            text="S/ 0.00 (18%)",
            font=('Segoe UI', 11),
            bg='white',
            anchor='e'
        )
        self.tax_label.pack(side='right')
        
        # Separador
        tk.Frame(totals_frame, bg='#bdc3c7', height=2).pack(fill='x', pady=10)
        
        # Total
        total_frame = tk.Frame(totals_frame, bg='#ecf0f1', relief='solid', borderwidth=1)
        total_frame.pack(fill='x', pady=5)
        
        tk.Label(
            total_frame,
            text="TOTAL:",
            font=('Segoe UI', 14, 'bold'),
            bg='#ecf0f1'
        ).pack(side='left', padx=10, pady=10)
        
        self.total_label = tk.Label(
            total_frame,
            text="S/ 0.00",
            font=('Segoe UI', 18, 'bold'),
            bg='#ecf0f1',
            fg='#27ae60'
        )
        self.total_label.pack(side='right', padx=10, pady=10)
        
        # Método de pago
        payment_frame = tk.Frame(parent, bg='white')
        payment_frame.pack(fill='x', padx=15, pady=(10, 0))
        
        tk.Label(
            payment_frame,
            text="💳 Método de Pago:",
            font=('Segoe UI', 10, 'bold'),
            bg='white'
        ).pack(anchor='w', pady=(0, 5))
        
        self.payment_method_var = tk.StringVar(value='cash')
        
        # ComboBox para métodos de pago
        payment_combo = ttk.Combobox(
            payment_frame,
            textvariable=self.payment_method_var,
            values=['cash', 'card', 'transfer', 'yape', 'plin'],
            state='readonly',
            font=('Segoe UI', 10),
            width=20
        )
        payment_combo.pack(anchor='w', pady=2)
        
        # Función para mostrar texto amigable
        def format_payment_display(value):
            mapping = {
                'cash': '💵 Efectivo',
                'card': '💳 Tarjeta',
                'transfer': '🏦 Transferencia',
                'yape': '📱 Yape',
                'plin': '📱 Plin'
            }
            return mapping.get(value, value)
        
        # Configurar el display inicial
        payment_combo.set('cash')
        
        # Personalizar el display (aunque el combobox muestra los valores internos)
        # Para mejor UX, podríamos usar valores con emojis directamente
        payment_combo.configure(values=[
            '💵 Efectivo',
            '💳 Tarjeta', 
            '🏦 Transferencia',
            '📱 Yape',
            '📱 Plin'
        ])
        
        # Función para obtener el valor real
        def get_payment_value():
            display = self.payment_method_var.get()
            mapping = {
                '💵 Efectivo': 'cash',
                '💳 Tarjeta': 'card',
                '🏦 Transferencia': 'transfer',
                '📱 Yape': 'yape',
                '📱 Plin': 'plin'
            }
            return mapping.get(display, 'cash')
        
        # Guardar la función para usar en process_sale
        self.get_payment_value = get_payment_value
        
        # Establecer valor inicial con emoji
        payment_combo.set('💵 Efectivo')
        
        # Monto pagado (solo para efectivo)
        paid_frame = tk.Frame(parent, bg='white')
        paid_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(
            paid_frame,
            text="💰 Monto pagado:",
            font=('Segoe UI', 11, 'bold'),
            bg='white'
        ).pack(side='left')
        
        self.paid_var = tk.StringVar(value="0.00")
        self.paid_entry = tk.Entry(
            paid_frame,
            textvariable=self.paid_var,
            font=('Segoe UI', 12),
            width=12,
            justify='right',
            relief='solid',
            borderwidth=1,
            highlightthickness=2,
            highlightcolor='#27ae60',
            highlightbackground='#bdc3c7'
        )
        self.paid_entry.pack(side='right', ipady=3)
        
        # Limpiar valor al hacer focus
        self.paid_entry.bind('<FocusIn>', self.on_paid_focus_in)
        self.paid_entry.bind('<KeyRelease>', lambda e: self.calculate_change())
        
        # Vuelto
        change_frame = tk.Frame(parent, bg='#ecf0f1', relief='solid', borderwidth=1)
        change_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            change_frame,
            text="💵 VUELTO:",
            font=('Segoe UI', 12, 'bold'),
            bg='#ecf0f1'
        ).pack(side='left', padx=10, pady=12)
        
        self.change_label = tk.Label(
            change_frame,
            text="S/ 0.00",
            font=('Segoe UI', 13, 'bold'),
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        self.change_label.pack(side='right', padx=10, pady=12)
        
        # Botón procesar venta
        self.process_btn = tk.Button(
            parent,
            text="✅ PROCESAR VENTA",
            command=self.process_sale,
            font=('Segoe UI', 13, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=20,
            pady=18,
            cursor='hand2',
            state='disabled',
            activebackground='#229954',
            activeforeground='white',
            bd=0
        )
        self.process_btn.pack(fill='x', padx=15, pady=(0, 15))
        
        # Efecto hover
        self.process_btn.bind('<Enter>', lambda e: self.process_btn.config(bg='#229954') if self.process_btn['state'] == 'normal' else None)
        self.process_btn.bind('<Leave>', lambda e: self.process_btn.config(bg='#27ae60') if self.process_btn['state'] == 'normal' else None)

        # Atajo: Ctrl+P para procesar venta
        self.parent.bind_all('<Control-p>', lambda e: self.process_sale())
        self.parent.bind_all('<Control-P>', lambda e: self.process_sale())
    
    def create_total_row(self, parent, label, value, attr_name):
        """Crea una fila de total"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='x', pady=5)
        
        tk.Label(
            frame,
            text=label,
            font=('Segoe UI', 10),
            bg='white'
        ).pack(side='left')
        
        label_widget = tk.Label(
            frame,
            text=f"S/ {value}",
            font=('Segoe UI', 10, 'bold'),
            bg='white'
        )
        label_widget.pack(side='right')
        
        setattr(self, f'{attr_name}_label', label_widget)
    
    # ==========================================
    # MÉTODOS DE BÚSQUEDA
    # ==========================================
    
    def load_initial_products(self):
        """Carga los primeros 50 productos al inicio"""
        try:
            print("🔍 DEBUG: Cargando productos iniciales...")
            # Obtener productos activos con stock
            result = self.controller.search_products_for_sale("")
            
            print(f"   - Resultado success: {result.get('success')}")
            print(f"   - Productos encontrados: {len(result.get('products', []))}")
            
            if result['success'] and result['products']:
                # Mostrar todos los productos encontrados
                products = result['products']
                print(f"   - Mostrando {len(products)} productos")
                self.display_products(products)
            else:
                print(f"   ⚠️ No se encontraron productos o hubo un error")
                if not result['success']:
                    print(f"   - Error: {result.get('message')}")
                # Limpiar tabla
                for item in self.products_tree.get_children():
                    self.products_tree.delete(item)
                self.products_count_label.config(
                    text="📦 No hay productos disponibles con stock",
                    foreground='#e74c3c'
                )
        except Exception as e:
            print(f"❌ Error cargando productos iniciales: {e}")
            import traceback
            traceback.print_exc()
            for item in self.products_tree.get_children():
                self.products_tree.delete(item)
            self.products_count_label.config(
                text=f"❌ Error: {str(e)}",
                foreground='#e74c3c'
            )
    
    def on_search_change(self):
        """Maneja el cambio en la búsqueda con delay para evitar consultas excesivas"""
        # LEER DIRECTAMENTE DEL ENTRY WIDGET en lugar del StringVar
        search_text = self.search_entry.get().strip()
        print(f"\n🔍 DEBUG on_search_change:")
        print(f"   Texto actual: '{search_text}'")
        print(f"   Longitud: {len(search_text)}")
        
        # Cancelar búsqueda anterior si existe
        if self.search_timer:
            print(f"   ⏸️ Cancelando búsqueda anterior")
            self.main_frame.after_cancel(self.search_timer)
        
        # Si está vacío, mostrar productos iniciales
        if not search_text:
            print(f"   ↩️ Texto vacío - cargando productos iniciales en 300ms")
            self.search_timer = self.main_frame.after(300, self.load_initial_products)
            return
        
        # Si tiene menos de 2 caracteres, solo filtrar localmente
        if len(search_text) < 2:
            print(f"   ⏸️ Menos de 2 caracteres - esperando más texto")
            return
        
        # Buscar después de 300ms de inactividad (evita consultas mientras escribe)
        print(f"   ⏰ Programando búsqueda en 300ms para: '{search_text}'")
        self.search_timer = self.main_frame.after(300, lambda: self.perform_search(search_text))
    
    def refresh_product_list(self):
        """Fuerza la actualización de la lista de productos sin importar el texto de búsqueda"""
        search_text = self.search_entry.get().strip()
        
        if not search_text or len(search_text) < 2:
            # Si no hay búsqueda activa, cargar productos iniciales
            self.load_initial_products()
        else:
            # Si hay búsqueda, ejecutar búsqueda
            self.perform_search(search_text)
    
    def perform_search(self, search_text):
        """Realiza la búsqueda de productos"""
        try:
            print(f"\n🔍 DEBUG perform_search:")
            print(f"   Texto de búsqueda: '{search_text}'")
            print(f"   Controller tipo: {type(self.controller)}")
            print(f"   ¿Tiene search_products_for_sale? {hasattr(self.controller, 'search_products_for_sale')}")
            
            # Buscar productos
            result = self.controller.search_products_for_sale(search_text)
            
            print(f"   Resultado success: {result.get('success')}")
            print(f"   Productos encontrados: {len(result.get('products', []))}")
            
            if result['success']:
                if result['products']:
                    self.display_products(result['products'])
                else:
                    # No se encontraron productos - limpiar tabla
                    for item in self.products_tree.get_children():
                        self.products_tree.delete(item)
                    self.products_count_label.config(
                        text=f"❌ No se encontraron productos para: '{search_text}'",
                        foreground='#e74c3c'
                    )
            else:
                # Error en la búsqueda
                for item in self.products_tree.get_children():
                    self.products_tree.delete(item)
                self.products_count_label.config(
                    text=f"⚠️ Error: {result.get('message', 'Error desconocido')}",
                    foreground='#e74c3c'
                )
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            import traceback
            traceback.print_exc()
            for item in self.products_tree.get_children():
                self.products_tree.delete(item)
            self.products_count_label.config(
                text=f"❌ Error al buscar: {str(e)}",
                foreground='#e74c3c'
            )
    
    def display_products(self, products):
        """Muestra productos en la tabla Treeview"""
        print(f"📋 DEBUG: display_products() - Mostrando {len(products)} productos")
        
        # Limpiar tabla
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        if not products:
            print("   ⚠️ Lista de productos vacía")
            return
        
        self.product_data = {}
        
        for i, product in enumerate(products):
            # Obtener datos del producto
            stock_qty = float(product.get('stock_quantity', 0))
            price = float(product.get('price', 0))
            sku = product.get('sku', 'N/A')
            name = product.get('name', 'Sin nombre')
            product_id = product.get('id')
            
            # ✅ CALCULAR STOCK DISPONIBLE RESTANDO LO QUE ESTÁ EN EL CARRITO
            qty_in_cart = 0
            for cart_item in self.cart_items:
                if cart_item['id'] == product_id:
                    qty_in_cart = cart_item['quantity']
                    break
            
            # Stock disponible = stock total - cantidad en carrito
            available_stock = stock_qty - qty_in_cart
            
            # Indicador de stock con emoji (basado en stock disponible)
            if available_stock <= 0:
                stock_display = f"⚫ 0 (en carrito: {int(qty_in_cart)})"
            elif available_stock <= 5:
                stock_display = f"🔴 {int(available_stock)}"
                if qty_in_cart > 0:
                    stock_display += f" (en carrito: {int(qty_in_cart)})"
            elif available_stock <= 10:
                stock_display = f"🟡 {int(available_stock)}"
                if qty_in_cart > 0:
                    stock_display += f" (en carrito: {int(qty_in_cart)})"
            else:
                stock_display = f"🟢 {int(available_stock)}"
                if qty_in_cart > 0:
                    stock_display += f" (en carrito: {int(qty_in_cart)})"
            
            # Insertar en la tabla con colores alternados
            tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
            
            item_id = self.products_tree.insert('', 'end', 
                values=(
                    sku,
                    name,
                    f"S/ {price:.2f}",
                    stock_display
                ),
                tags=tags
            )
            
            # Guardar referencia del producto por item_id
            self.product_data[item_id] = product
            
            if i == 0:
                print(f"   - Primer producto: {sku} - {name}")
        
        # Configurar colores alternados
        self.products_tree.tag_configure('evenrow', background='#f9f9f9')
        self.products_tree.tag_configure('oddrow', background='#ffffff')
        
        # Actualizar contador de productos
        self.products_count_label.config(
            text=f"📦 Total: {len(products)} productos disponibles",
            foreground='#27ae60' if len(products) > 0 else '#7f8c8d'
        )
        
        print(f"   ✅ {len(products)} productos mostrados correctamente")
    
    def quick_add_product(self):
        """Agrega rápido el primer producto de la tabla (Enter en búsqueda)"""
        children = self.products_tree.get_children()
        if children:
            # Seleccionar el primer producto
            first_item = children[0]
            self.products_tree.selection_set(first_item)
            self.products_tree.focus(first_item)
            self.products_tree.see(first_item)
            self.add_selected_product()
    
    def quick_add_product_with_search(self):
        """
        Agregar producto con búsqueda síncrona (para pistola de código de barras)
        
        Este método resuelve el problema de que la pistola es más rápida que la búsqueda:
        1. Cancela cualquier búsqueda pendiente
        2. Ejecuta búsqueda inmediatamente (sin delay)
        3. Espera a que termine
        4. Luego agrega el producto
        """
        # Obtener texto de búsqueda actual
        search_text = self.search_entry.get().strip()
        
        print(f"\n🔫 DEBUG pistola de código de barras:")
        print(f"   Código escaneado: '{search_text}'")
        
        # Si está vacío, no hacer nada
        if not search_text:
            print(f"   ⚠️ Texto vacío - ignorando")
            return
        
        # Cancelar búsqueda programada si existe (importante!)
        if self.search_timer:
            print(f"   ⏸️ Cancelando búsqueda programada")
            self.main_frame.after_cancel(self.search_timer)
            self.search_timer = None
        
        # Ejecutar búsqueda INMEDIATAMENTE (sin delay)
        print(f"   🔍 Ejecutando búsqueda síncrona...")
        self.perform_search(search_text)
        
        # Ahora agregar el producto (la búsqueda ya terminó)
        print(f"   ➕ Agregando primer producto encontrado...")
        self.quick_add_product()
        
        # Limpiar campo de búsqueda para siguiente escaneo
        self.search_entry.delete(0, tk.END)
        print(f"   ✅ Campo de búsqueda limpiado")
    
    def add_selected_product(self):
        """Agrega el producto seleccionado al carrito"""
        selection = self.products_tree.selection()
        
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un producto")
            return
        
        item_id = selection[0]
        product = self.product_data.get(item_id)
        
        # Si no hay datos del producto, ignorar
        if not product:
            return
        
        # Verificar si ya está en el carrito
        for item in self.cart_items:
            if item['id'] == product['id']:
                # Incrementar cantidad
                if item['quantity'] < product['stock_quantity']:
                    item['quantity'] += 1
                    self.update_cart_display()
                    self.calculate_totals()
                    
                    # ✅ ACTUALIZAR VISTA DE PRODUCTOS EN TIEMPO REAL
                    self.refresh_product_list()
                else:
                    messagebox.showwarning(
                        "Stock insuficiente",
                        f"No hay más stock disponible\nStock actual: {product['stock_quantity']}"
                    )
                return
        
        # Agregar nuevo item
        self.cart_items.append({
            'id': product['id'],
            'sku': product['sku'],
            'name': product['name'],
            'price': float(product['price']),
            'quantity': 1,
            'stock_available': float(product['stock_quantity']),
            'subtotal': float(product['price'])  # Precio * cantidad (1)
        })
        
        self.update_cart_display()
        self.calculate_totals()
        
        # ✅ ACTUALIZAR VISTA DE PRODUCTOS EN TIEMPO REAL
        # Refrescar la lista de productos para mostrar stock actualizado
        self.refresh_product_list()
        
        # Opcional: Limpiar búsqueda (comentado para mantener la lista visible)
        # self.search_var.set('')
    
    # ==========================================
    # MÉTODOS DEL CARRITO
    # ==========================================
    
    def update_cart_display(self):
        """Actualiza la visualización del carrito con formato mejorado"""
        # Limpiar árbol
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # Agregar items con mejor formato
        for i, item in enumerate(self.cart_items):
            subtotal = item['price'] * item['quantity']
            
            # Alternar colores de fondo
            tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
            
            self.cart_tree.insert('', 'end', 
                values=(
                    item['name'][:30],  # Truncar nombre largo
                    f"{item['quantity']:.0f}",
                    f"S/ {item['price']:.2f}",
                    f"S/ {subtotal:.2f}"
                ),
                tags=tags
            )
        
        # Configurar colores alternados
        self.cart_tree.tag_configure('evenrow', background='#f0f0f0')
        self.cart_tree.tag_configure('oddrow', background='#ffffff')
        
        # Actualizar contador con emoji
        total_items = sum(item['quantity'] for item in self.cart_items)
        if total_items > 0:
            self.cart_count_label.config(
                text=f"🛒 {total_items} items",
                foreground='#27ae60',
                font=('Segoe UI', 10, 'bold')
            )
        else:
            self.cart_count_label.config(
                text="🛒 Carrito vacío",
                foreground='#7f8c8d',
                font=('Segoe UI', 10)
            )
        
        # Habilitar/deshabilitar botón de procesar
        if self.cart_items:
            self.process_btn.config(state='normal')
        else:
            self.process_btn.config(state='disabled')
    
    def remove_from_cart(self):
        """Quita un item del carrito"""
        selection = self.cart_tree.selection()
        
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un producto del carrito")
            return
        
        index = self.cart_tree.index(selection[0])
        self.cart_items.pop(index)
        
        self.update_cart_display()
        self.calculate_totals()
        
        # ✅ ACTUALIZAR VISTA DE PRODUCTOS EN TIEMPO REAL
        self.refresh_product_list()
    
    def edit_quantity(self):
        """Edita la cantidad de un item"""
        selection = self.cart_tree.selection()
        
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un producto del carrito")
            return
        
        index = self.cart_tree.index(selection[0])
        item = self.cart_items[index]
        
        print(f"\n📝 DEBUG edit_quantity - INICIO:")
        print(f"   Index seleccionado: {index}")
        print(f"   Total items en carrito: {len(self.cart_items)}")
        print(f"   Item a editar: {item['name']}")
        print(f"   Cantidad actual: {item['quantity']}")
        print(f"   Stock disponible: {item['stock_available']}")
        
        # Diálogo para nueva cantidad
        dialog = tk.Toplevel(self.main_frame)
        dialog.title("✏️ Editar Cantidad")
        dialog.configure(bg='white')
        dialog.geometry("400x320")
        dialog.resizable(False, False)
        dialog.transient(self.main_frame)
        dialog.grab_set()
        
        # ✅ CENTRAR EL DIÁLOGO EN LA PANTALLA
        dialog.update_idletasks()  # Actualizar para obtener dimensiones reales
        window_width = 400
        window_height = 320
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        dialog.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        tk.Label(
            dialog,
            text=f"Producto: {item['name'][:40]}",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg='#2c3e50',
            wraplength=360
        ).pack(pady=(15, 5))
        
        tk.Label(
            dialog,
            text=f"Stock disponible: {int(item['stock_available'])} unidades",
            font=('Segoe UI', 10),
            bg='white',
            fg='#27ae60'
        ).pack(pady=(0, 5))
        
        tk.Label(
            dialog,
            text="Nueva cantidad:",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=(10, 0))
        
        tk.Label(
            dialog,
            text="(Escribe el número total que deseas)",
            font=('Segoe UI', 9, 'italic'),
            bg='white',
            fg='#7f8c8d'
        ).pack(pady=(0, 5))
        
        quantity_var = tk.StringVar(value=str(int(item['quantity'])))  # Sin decimales
        quantity_entry = tk.Entry(
            dialog,
            textvariable=quantity_var,
            font=('Segoe UI', 18, 'bold'),  # Fuente MÁS grande
            justify='center',
            width=10,
            bg='#fff3cd',  # Fondo amarillo claro (destaca)
            fg='#2c3e50',
            relief='solid',
            bd=3,
            highlightthickness=2,
            highlightcolor='#3498db',
            highlightbackground='#95a5a6'
        )
        quantity_entry.pack(pady=10)
        
        # ✅ SELECCIONAR TODO AUTOMÁTICAMENTE al abrir
        # Para que el usuario pueda escribir directamente el nuevo número
        quantity_entry.focus()
        quantity_entry.select_range(0, tk.END)
        quantity_entry.icursor(tk.END)
        
        def save_quantity():
            print(f"\n🔵 DEBUG save_quantity - EJECUTANDO")
            try:
                # ✅ LEER DIRECTAMENTE DEL ENTRY WIDGET (no del StringVar)
                new_qty_str = quantity_entry.get().strip()
                print(f"   → Valor leído DIRECTAMENTE del Entry: '{new_qty_str}'")
                print(f"   → Valor del StringVar (comparación): '{quantity_var.get()}'")
                
                if not new_qty_str:
                    print(f"   ❌ Campo vacío!")
                    messagebox.showerror("Error", "Debes ingresar una cantidad")
                    return
                
                new_qty = float(new_qty_str)
                
                print(f"\n🔍 DEBUG edit_quantity:")
                print(f"   Producto: {item['name']}")
                print(f"   Cantidad actual: {item['quantity']}")
                print(f"   Nueva cantidad: {new_qty}")
                print(f"   Stock disponible: {item['stock_available']}")
                
                if new_qty <= 0:
                    print(f"   ❌ Cantidad inválida: debe ser mayor a 0")
                    messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                    return
                
                if new_qty > item['stock_available']:
                    print(f"   ❌ Stock insuficiente!")
                    messagebox.showerror(
                        "Error",
                        f"Stock insuficiente\nDisponible: {item['stock_available']}"
                    )
                    return
                
                # Actualizar cantidad en el item del carrito
                print(f"   → Actualizando cantidad...")
                item['quantity'] = new_qty
                item['subtotal'] = item['price'] * new_qty  # Actualizar subtotal también
                
                print(f"   ✅ Cantidad actualizada a: {item['quantity']}")
                print(f"   ✅ Subtotal actualizado a: S/ {item['subtotal']:.2f}")
                
                print(f"   → Actualizando display del carrito...")
                self.update_cart_display()
                
                print(f"   → Recalculando totales...")
                self.calculate_totals()
                
                print(f"   → Refrescando lista de productos...")
                # ✅ ACTUALIZAR VISTA DE PRODUCTOS EN TIEMPO REAL
                self.refresh_product_list()
                
                print(f"   → Cerrando diálogo...")
                dialog.destroy()
                print(f"   ✅ Proceso completado exitosamente!")
                
            except ValueError as e:
                print(f"   ❌ Error de conversión: {e}")
                messagebox.showerror("Error", "Cantidad inválida")
        
        tk.Button(
            dialog,
            text="✅ Guardar Cambios",
            command=lambda: (print("🟢 Botón Guardar presionado"), save_quantity()),
            font=('Segoe UI', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            activeforeground='white',
            padx=30,
            pady=10,
            relief='flat',
            cursor='hand2'
        ).pack(pady=15)
        
        quantity_entry.bind('<Return>', lambda e: (print("🟢 Enter presionado"), save_quantity()))
    
    def clear_cart(self, ask_confirmation=True):
        """Vacía el carrito
        
        Args:
            ask_confirmation: Si es True, pide confirmación al usuario
        """
        if not self.cart_items:
            return
        
        # Solo pedir confirmación si ask_confirmation=True
        if ask_confirmation:
            if not messagebox.askyesno("Confirmar", "¿Vaciar todo el carrito?"):
                return
        
        self.cart_items.clear()
        self.update_cart_display()
        self.calculate_totals()
        
        # ✅ ACTUALIZAR VISTA DE PRODUCTOS EN TIEMPO REAL
        self.refresh_product_list()
    
    # ==========================================
    # CÁLCULOS
    # ==========================================
    
    def on_paid_focus_in(self, event=None):
        """Selecciona todo el texto al hacer click para facilitar sobrescritura"""
        current_value = self.paid_var.get()
        print(f"\n🔍 DEBUG on_paid_focus_in:")
        print(f"   Valor actual en paid_var: '{current_value}'")
        
        # Seleccionar todo el texto en lugar de borrar
        self.paid_entry.select_range(0, tk.END)
        self.paid_entry.icursor(tk.END)
        print(f"   ✓ Texto seleccionado para sobrescritura")
    
    def toggle_tax(self, event=None):
        """Alterna el estado del toggle switch de IGV"""
        # Cambiar estado
        current = self.include_tax_var.get()
        self.include_tax_var.set(not current)
        
        # Actualizar visual del toggle
        if self.include_tax_var.get():
            # ON - Verde
            self.toggle_canvas.itemconfig(self.toggle_bg, fill='#27ae60')
            self.toggle_canvas.coords(self.toggle_circle, 28, 4, 44, 20)
            self.tax_status_label.config(text="ON", fg='#27ae60')
        else:
            # OFF - Gris
            self.toggle_canvas.itemconfig(self.toggle_bg, fill='#95a5a6')
            self.toggle_canvas.coords(self.toggle_circle, 6, 4, 22, 20)
            self.tax_status_label.config(text="OFF", fg='#95a5a6')
        
        # Recalcular totales inmediatamente
        self.calculate_totals()
    
    def calculate_totals(self):
        """Calcula los totales de la venta con formato mejorado"""
        if not self.cart_items:
            self.subtotal_label.config(
                text="S/ 0.00",
                foreground='#7f8c8d',
                font=('Segoe UI', 11)
            )
            self.tax_label.config(
                text="S/ 0.00 (0%)",
                foreground='#7f8c8d',
                font=('Segoe UI', 11)
            )
            self.total_label.config(
                text="S/ 0.00",
                foreground='#7f8c8d',
                font=('Segoe UI', 16, 'bold')
            )
            self.change_label.config(
                text="S/ 0.00",
                foreground='#7f8c8d',
                font=('Segoe UI', 13, 'bold')
            )
            self.current_total = 0.0
            return
        
        # Subtotal - redondear a 2 decimales para evitar problemas de precisión
        subtotal = round(sum(item['price'] * item['quantity'] for item in self.cart_items), 2)
        
        # Descuento
        try:
            discount = round(float(self.discount_var.get()), 2)
        except:
            discount = 0.0
        
        # Subtotal con descuento
        subtotal_after_discount = round(subtotal - discount, 2)
        
        # Leer tax_rate de la configuración (si no existe, usar 18%)
        try:
            from config.settings import load_system_config
            config = load_system_config()
            tax_rate = float(config.get('tax_rate', 18)) / 100
        except:
            tax_rate = 0.18  # Default 18%
        
        # IGV - solo si está activado
        if self.include_tax_var.get():
            tax = round(subtotal_after_discount * tax_rate, 2)
            total = round(subtotal_after_discount + tax, 2)
        else:
            tax = 0.0
            total = round(subtotal_after_discount, 2)
        
        # Guardar total actual como variable de instancia - REDONDEADO A 2 DECIMALES
        self.current_total = round(total, 2)
        
        # Actualizar labels con colores
        self.subtotal_label.config(
            text=f"S/ {subtotal:.2f}",
            foreground='#2c3e50',
            font=('Segoe UI', 11)
        )
        
        # Mostrar porcentaje del IGV
        tax_percentage = int(tax_rate * 100)
        if self.include_tax_var.get():
            self.tax_label.config(
                text=f"S/ {tax:.2f} ({tax_percentage}%)",
                foreground='#2c3e50',
                font=('Segoe UI', 11)
            )
        else:
            self.tax_label.config(
                text=f"S/ 0.00 (0%)",
                foreground='#95a5a6',
                font=('Segoe UI', 11)
            )
        
        self.total_label.config(
            text=f"S/ {total:.2f}",
            foreground='#27ae60',
            font=('Segoe UI', 16, 'bold')
        )
        
        # Calcular vuelto
        self.calculate_change()
    
    def calculate_change(self):
        """Calcula el vuelto con formato mejorado"""
        try:
            # Usar la variable de instancia current_total en lugar de leer el label
            total = round(getattr(self, 'current_total', 0.0), 2)
            
            # Debug completo de la lectura del valor
            print(f"\n💰 DEBUG calculate_change:")
            print(f"   Total: S/ {total:.2f}")
            
            # LEER DIRECTAMENTE DEL ENTRY WIDGET en lugar del StringVar
            paid_text = self.paid_entry.get().strip()
            print(f"   Leyendo paid_entry.get(): '{paid_text}'")
            
            # Si está vacío o es "0.00", no mostrar error
            if not paid_text or paid_text == "0.00":
                print(f"   ⚠️ Valor vacío o 0.00, mostrando S/ 0.00")
                self.change_label.config(
                    text="S/ 0.00",
                    foreground='#7f8c8d',
                    font=('Segoe UI', 13, 'bold')
                )
                return
            
            paid = round(float(paid_text), 2)
            print(f"   Convertido a float: {paid:.2f}")
            
            change = round(paid - total, 2)  # Redondear el vuelto también
            print(f"   Vuelto calculado: S/ {change:.2f}")
            
            if change >= -0.009:  # Tolerancia para problemas de precisión
                self.change_label.config(
                    text=f"S/ {max(0, change):.2f}",  # No mostrar vueltos negativos por redondeo
                    foreground='#27ae60',
                    font=('Segoe UI', 13, 'bold')
                )
            else:
                self.change_label.config(
                    text=f"Falta: S/ {abs(change):.2f}",
                    foreground='#e74c3c',
                    font=('Segoe UI', 13, 'bold')
                )
        except ValueError as e:
            print(f"❌ Error en calculate_change: {e}")
            self.change_label.config(
                text="S/ 0.00",
                foreground='#7f8c8d',
                font=('Segoe UI', 13)
            )

    def reset_payment_fields(self):
        """Reinicia los campos de pago después de procesar la venta"""
        # Limpiar entrada de monto pagado (no solo la variable)
        self.paid_var.set("")
        try:
            self.paid_entry.delete(0, tk.END)
        except Exception:
            pass

        # Restablecer método de pago a efectivo (display con emoji)
        try:
            self.payment_method_var.set('💵 Efectivo')
        except Exception:
            pass

        # Reiniciar etiqueta de vuelto
        self.change_label.config(
            text="S/ 0.00",
            foreground='#7f8c8d',
            font=('Segoe UI', 13, 'bold')
        )
    
    # ==========================================
    # CLIENTE
    # ==========================================
    
    def select_customer(self):
        """Abre diálogo para seleccionar cliente"""
        # TODO: Implementar diálogo de selección de cliente
        messagebox.showinfo("Info", "Función de selección de cliente pendiente")
    
    # ==========================================
    # PROCESAR VENTA
    # ==========================================
    
    def process_sale(self):
        """Procesa la venta"""
        if not self.cart_items:
            messagebox.showwarning("Advertencia", "El carrito está vacío")
            return
        
        # Validar monto pagado
        payment_method = self.get_payment_value()  # Usar la función helper
        
        try:
            # Usar la variable de instancia current_total (ya redondeado a 2 decimales)
            total = round(self.current_total, 2)
            
            # LEER DIRECTAMENTE DEL ENTRY WIDGET
            paid_text = self.paid_entry.get().strip()
            if not paid_text:
                paid = 0.0
            else:
                paid = round(float(paid_text), 2)  # Redondear a 2 decimales
            
            print(f"🔍 DEBUG process_sale:")
            print(f"   Total a pagar: S/ {total:.2f}")
            print(f"   Monto pagado: S/ {paid:.2f}")
            print(f"   Método de pago: {payment_method}")
            
            # Validar con tolerancia de 0.01 para evitar problemas de precisión
            # Esto permite pequeñas diferencias de redondeo
            if payment_method == 'cash' and paid < (total - 0.009):
                print(f"   ❌ Monto insuficiente!")
                messagebox.showerror(
                    "Error",
                    f"Monto insuficiente\nTotal: S/ {total:.2f}\nPagado: S/ {paid:.2f}"
                )
                return
            
            print(f"   ✅ Validación exitosa")
            
        except ValueError as e:
            print(f"   ❌ Error de conversión: {e}")
            messagebox.showerror("Error", "Monto pagado inválido")
            return
        
        # ✅ PROCESAR AUTOMÁTICAMENTE SIN CONFIRMACIÓN
        # (Comentado el diálogo de confirmación)
        # if not messagebox.askyesno("Confirmar", f"¿Procesar venta por S/ {total:.2f}?"):
        #     return
        
        print(f"   → Procesando venta automáticamente...")
        
        # Preparar datos de pago
        discount = 0.0
        try:
            discount = round(float(self.discount_var.get()), 2)
        except:
            pass
        
        # Obtener el estado del IGV
        include_tax = self.include_tax_var.get()
        
        # Calcular change redondeado para evitar problemas de precisión
        change_amount = round(max(0, paid - total), 2) if payment_method == 'cash' else 0
        
        payment_info = {
            'method': payment_method,
            'paid_amount': round(paid if payment_method == 'cash' else total, 2),
            'change_amount': change_amount,
            'discount_amount': discount,
            'include_tax': include_tax  # ✅ Pasar el estado del IGV al controlador
        }
        
        # Procesar en el controlador
        result = self.controller.process_sale(
            cart_items=self.cart_items,
            customer_id=self.current_customer['id'] if self.current_customer else None,
            user_id=self.user_data['id'],
            payment_info=payment_info,
            notes=""
        )
        
        if result['success']:
            # Mostrar mensaje de éxito PRIMERO (no bloqueante si usamos un popup personalizado)
            print(f"✅ Venta procesada: {result['sale_number']}")
            
            # Generar y mostrar boleta (esto abrirá la ventana de vista previa)
            self.generate_ticket(result, total, paid, payment_method, discount)
            
            # ✅ LIMPIAR CARRITO AUTOMÁTICAMENTE SIN CONFIRMACIÓN
            self.clear_cart(ask_confirmation=False)
            self.discount_var.set("0.00")
            self.reset_payment_fields()
            
            # ✅ ACTUALIZAR LISTA DE PRODUCTOS (refrescar stock)
            self.refresh_product_list()
            
            print(f"   ✅ Carrito limpiado automáticamente")
            
        else:
            messagebox.showerror("Error", f"❌ {result['message']}")
    
    def generate_ticket(self, sale_result, total, paid, payment_method, discount):
        """Generar e imprimir boleta de venta"""
        try:
            from utils.ticket_generator import TicketGenerator
            from datetime import datetime
            
            # Calcular IGV y subtotal SOLO si está activado
            if self.include_tax_var.get():  # ✅ Verificar si IGV está activado
                subtotal = total / 1.18  # Total sin IGV
                igv = total - subtotal
            else:
                subtotal = total  # Sin IGV, el subtotal es igual al total
                igv = 0  # No hay IGV
            
            # Preparar datos para el ticket
            ticket_data = {
                'sale_number': sale_result['sale_number'],
                'date': datetime.now(),
                'cashier': self.user_data.get('full_name', self.user_data.get('username')),
                'customer': self.current_customer if self.current_customer else {'name': 'Cliente Genérico'},
                'items': [],
                'subtotal': subtotal,
                'discount': discount,
                'igv': igv,  # Será 0 si IGV está desactivado
                'total': total,
                'payment_method': payment_method,
                'paid_amount': paid,
                'change_amount': max(0, paid - total) if payment_method == 'cash' else 0
            }
            
            # Agregar items con los nombres correctos de campos
            for item in self.cart_items:
                ticket_data['items'].append({
                    'name': item['name'],
                    'quantity': item['quantity'],
                    'price': item['price'],  # Precio unitario
                    'total': item['subtotal']  # Total del item
                })
            
            # Generar ticket
            generator = TicketGenerator()
            
            # Generar versión HTML con imagen (si está configurado el logo)
            ticket_html = generator.generate_ticket_html(ticket_data)
            ticket_html_path = generator.save_ticket_html(ticket_html, sale_result['sale_number'])
            
            # También generar versión texto (para impresoras térmicas)
            ticket_content = generator.generate_ticket(ticket_data)
            ticket_path = generator.save_ticket(ticket_content, sale_result['sale_number'])
            
            if ticket_html_path:
                print(f"✅ Ticket HTML guardado en: {ticket_html_path}")
            if ticket_path:
                print(f"✅ Ticket TXT guardado en: {ticket_path}")
            
            # Mostrar ventana de vista previa con opción de imprimir
            self.show_ticket_preview(ticket_content, generator, ticket_html, ticket_html_path, ticket_data)
        
        except Exception as e:
            print(f"❌ Error generando ticket: {e}")
            import traceback
            traceback.print_exc()
    
    def show_ticket_preview(self, ticket_content, generator, ticket_html=None, ticket_html_path=None, ticket_data=None):
        """Mostrar ventana con vista previa del ticket"""
        
        # Si auto_print está activado Y hay HTML, imprimir automáticamente
        if ticket_html_path and generator.config.get('print_copy', False):
            print("🖨️ Imprimiendo boleta automáticamente...")
            generator.print_ticket_html(ticket_html, ticket_html_path, ticket_data)
            return  # No mostrar la ventana de vista previa
        
        preview_window = tk.Toplevel(self.main_frame)
        preview_window.title('Boleta de Venta')
        preview_window.geometry('500x700')
        preview_window.configure(bg='white')
        preview_window.transient(self.main_frame)
        preview_window.grab_set()
        
        # Header
        header = tk.Frame(preview_window, bg='#27ae60')
        header.pack(fill='x')
        
        tk.Label(
            header,
            text='✅ VENTA PROCESADA - BOLETA',
            font=('Segoe UI', 16, 'bold'),
            bg='#27ae60',
            fg='white'
        ).pack(pady=15)
        
        # Texto del ticket
        text_frame = tk.Frame(preview_window, bg='white')
        text_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        text_widget = tk.Text(
            text_frame,
            font=('Courier New', 9),
            bg='#f8f9fa',
            relief='solid',
            borderwidth=1,
            padx=10,
            pady=10,
            wrap='none'
        )
        text_widget.pack(fill='both', expand=True)
        text_widget.insert('1.0', ticket_content)
        text_widget.config(state='disabled')
        
        # Botones
        button_frame = tk.Frame(preview_window, bg='white')
        button_frame.pack(fill='x', padx=20, pady=20)
        
        # Botón para ver versión HTML con imagen
        if ticket_html_path:
            tk.Button(
                button_frame,
                text='�️ Ver con Logo',
                command=lambda: self.open_html_ticket(ticket_html_path),
                bg='#9b59b6',
                fg='white',
                font=('Segoe UI', 11, 'bold'),
                cursor='hand2',
                relief='flat',
                padx=20,
                pady=10
            ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text='�🖨️ Imprimir Texto',
            command=lambda: self.print_ticket(generator, ticket_content, preview_window),
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            cursor='hand2',
            relief='flat',
            padx=20,
            pady=10
        ).pack(side='left', padx=5)
        
        # Botón para imprimir HTML con imagen
        if ticket_html:
            tk.Button(
                button_frame,
                text='🖨️ Imprimir con Logo',
                command=lambda: generator.print_ticket_html(ticket_html, ticket_html_path, ticket_data),
                bg='#e74c3c',
                fg='white',
                font=('Segoe UI', 11, 'bold'),
                cursor='hand2',
                relief='flat',
                padx=20,
                pady=10
            ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text='✓ Cerrar',
            command=preview_window.destroy,
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            cursor='hand2',
            relief='flat',
            padx=20,
            pady=10
        ).pack(side='left', padx=5)
    
    def open_html_ticket(self, html_path):
        """Abrir ticket HTML en navegador"""
        try:
            import webbrowser
            import os
            webbrowser.open('file://' + os.path.abspath(html_path))
        except Exception as e:
            print(f"❌ Error abriendo ticket HTML: {e}")
    
    def print_ticket(self, generator, ticket_content, window):
        """Imprimir ticket"""
        try:
            success = generator.print_ticket(ticket_content)
            if success:
                messagebox.showinfo('Éxito', '✅ Ticket enviado a impresora')
                window.destroy()
            else:
                messagebox.showerror('Error', 'No se pudo imprimir el ticket')
        except Exception as e:
            messagebox.showerror('Error', f'Error al imprimir:\n{str(e)}')
    
    def show(self):
        """Muestra la vista"""
        self.main_frame.pack(fill='both', expand=True)
        
        # ✅ Cargar productos DESPUÉS de que la vista esté visible
        self.main_frame.after(100, self.load_initial_products)
    
    def hide(self):
        """Oculta la vista"""
        self.main_frame.pack_forget()
    
    def destroy(self):
        """Destruye la vista"""
        self.main_frame.destroy()
