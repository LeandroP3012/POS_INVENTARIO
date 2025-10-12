"""
Vista de Control de Stock - Actualización de Inventario
Permite ajustar el stock de productos de manera rápida
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, List
from views.base_view import BaseView


class StockControlView(BaseView):
    """Vista para control y actualización de stock"""
    
    def __init__(self, root: tk.Tk, user_data: Dict[str, Any] = None):
        super().__init__(root)
        self.user_data = user_data or {}
        self.products = []
        self.filtered_products = []
        
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
        
        # Toolbar
        self.create_toolbar()
        
        # Contenido: Tabla y Panel de Actualización
        self.create_main_content()
        
        # Footer
        self.create_footer()
    
    def create_header(self):
        """Crear header"""
        header = tk.Frame(self.main_frame, bg='#2c3e50', height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Título
        tk.Label(
            header,
            text="📊 Control de Stock",
            font=('Segoe UI', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(side='left', padx=20, pady=15)
        
        # Botón volver
        tk.Button(
            header,
            text="← Volver",
            command=self._on_back,
            font=('Segoe UI', 10),
            bg='#34495e',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=5
        ).pack(side='right', padx=20)
        
        # Usuario
        tk.Label(
            header,
            text=f"Usuario: {self.user_data.get('full_name', 'N/A')}",
            font=('Segoe UI', 10),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack(side='right', padx=20)
    
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
        self.search_var.trace('w', lambda *args: self.on_search())
        
        search_entry = tk.Entry(
            left_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 11),
            width=50,
            relief='solid',
            bd=1
        )
        search_entry.pack(side='left')
        
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
        ).pack(fill='x', pady=(0, 10))
        
        self.movement_type_var = tk.StringVar(value="entrada")
        
        radio_frame = tk.Frame(content_inner, bg='white')
        radio_frame.pack(fill='x', pady=(0, 20))
        
        tk.Radiobutton(
            radio_frame,
            text="📥 Entrada (Agregar)",
            variable=self.movement_type_var,
            value="entrada",
            font=('Segoe UI', 10),
            bg='white',
            activebackground='white',
            selectcolor='#d4edda'
        ).pack(anchor='w', pady=5)
        
        tk.Radiobutton(
            radio_frame,
            text="📤 Salida (Restar)",
            variable=self.movement_type_var,
            value="salida",
            font=('Segoe UI', 10),
            bg='white',
            activebackground='white',
            selectcolor='#f8d7da'
        ).pack(anchor='w', pady=5)
        
        tk.Radiobutton(
            radio_frame,
            text="✏️ Ajuste Manual",
            variable=self.movement_type_var,
            value="ajuste",
            font=('Segoe UI', 10),
            bg='white',
            activebackground='white',
            selectcolor='#fff3cd'
        ).pack(anchor='w', pady=5)
        
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
        if self.on_search_callback:
            search_term = self.search_var.get()
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
        self.update_button.config(state='normal')
        self.save_limits_button.config(state='normal')
    
    def on_update_stock(self):
        """Actualizar stock del producto seleccionado"""
        print("\n" + "="*60)
        print("🔍 DEBUG: Iniciando actualización de stock")
        print("="*60)
        
        selection = self.tree.selection()
        if not selection:
            print("❌ No hay producto seleccionado")
            messagebox.showwarning("Selección", "Seleccione un producto primero")
            return
        
        print(f"✅ Producto seleccionado: {selection[0]}")
        
        # DEBUG: Leer DIRECTAMENTE del Entry widget
        print(f"\n📊 VALORES DE ENTRY Y STRINGVAR:")
        quantity_from_entry = self.quantity_entry.get()
        quantity_from_var = self.quantity_var.get()
        print(f"   quantity_entry.get(): '{quantity_from_entry}'")
        print(f"   quantity_var.get(): '{quantity_from_var}'")
        
        # Validar cantidad
        try:
            # USAR VALOR DEL ENTRY DIRECTAMENTE (no del StringVar)
            quantity_str = quantity_from_entry
            quantity = float(quantity_str) if quantity_str.strip() else 0.0
            movement_type = self.movement_type_var.get()
            
            print(f"\n📊 VALORES PROCESADOS:")
            print(f"   Cantidad: {quantity}")
            print(f"   Tipo de movimiento: {movement_type}")
            
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
        """Cargar productos en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.products = products
        self.filtered_products = products
        
        # Insertar productos
        for product in products:
            # Determinar estado del stock
            stock = product.get('stock_quantity', 0)
            min_stock = product.get('min_stock', 0)
            max_stock = product.get('max_stock', 0)
            
            if stock == 0:
                status = "🚫 Agotado"
                tag = 'out_of_stock'
            elif stock <= min_stock:
                status = "⚠️ Bajo"
                tag = 'low_stock'
            elif stock >= max_stock:
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

