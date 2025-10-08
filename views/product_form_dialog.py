"""
Diálogo para Crear/Editar Productos
Formulario modal para gestión de productos
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional, List
from decimal import Decimal


class ProductFormDialog:
    """Diálogo para crear o editar productos"""
    
    def __init__(self, parent, product: Optional[Dict[str, Any]] = None, 
                 categories: List[Dict[str, Any]] = None, 
                 units: List[Dict[str, Any]] = None):
        self.parent = parent
        self.product = product
        self.categories = categories or []
        self.units = units or []
        self.result = None
        
        # Crear ventana
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Editar Producto" if product else "Nuevo Producto")
        self.dialog.geometry("600x700")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar ventana
        self.center_window()
        
        # Variables
        self.setup_variables()
        
        # Crear interfaz
        self.create_widgets()
        
        # Si es edición, cargar datos
        if self.product:
            self.load_product_data()
        
        # Focus en primer campo
        self.sku_entry.focus()
    
    def center_window(self):
        """Centrar ventana en la pantalla"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_variables(self):
        """Configurar variables de los campos"""
        self.sku_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.unit_var = tk.StringVar()
        self.barcode_var = tk.StringVar()
        self.price_var = tk.StringVar(value="0.00")
        self.cost_var = tk.StringVar(value="0.00")
        self.stock_var = tk.StringVar(value="0")
        self.min_stock_var = tk.StringVar(value="0")
        self.max_stock_var = tk.StringVar(value="0")
        self.tax_rate_var = tk.StringVar(value="0.0")
        self.status_var = tk.StringVar(value="active")
    
    def create_widgets(self):
        """Crear widgets del formulario"""
        # Header
        header = tk.Frame(self.dialog, bg='#3498db', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        icon = "✏️" if self.product else "➕"
        title = "Editar Producto" if self.product else "Nuevo Producto"
        
        tk.Label(
            header,
            text=f"{icon} {title}",
            font=('Segoe UI', 16, 'bold'),
            bg='#3498db',
            fg='white'
        ).pack(pady=15)
        
        # Contenido con scroll
        main_frame = tk.Frame(self.dialog, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        canvas = tk.Canvas(main_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # === SECCIÓN: INFORMACIÓN BÁSICA ===
        self.create_section_header(scrollable_frame, "📋 Información Básica")
        
        # SKU
        self.sku_entry = self.create_field(
            scrollable_frame, "SKU *", self.sku_var,
            placeholder="Código único del producto"
        )
        
        # Nombre
        self.create_field(
            scrollable_frame, "Nombre del Producto *", self.name_var,
            placeholder="Ej: Laptop Dell Inspiron 15"
        )
        
        # Descripción
        desc_frame = self.create_label_frame(scrollable_frame, "Descripción")
        self.description_text = tk.Text(
            desc_frame,
            height=3,
            font=('Segoe UI', 10),
            relief='solid',
            bd=1,
            wrap='word'
        )
        self.description_text.pack(fill='x', pady=(5, 0))
        
        # Código de barras
        self.create_field(
            scrollable_frame, "Código de Barras", self.barcode_var,
            placeholder="Código de barras EAN/UPC"
        )
        
        # === SECCIÓN: CATEGORIZACIÓN ===
        self.create_section_header(scrollable_frame, "🏷️ Categorización")
        
        # Categoría
        cat_frame = self.create_label_frame(scrollable_frame, "Categoría *")
        self.category_combo = ttk.Combobox(
            cat_frame,
            textvariable=self.category_var,
            font=('Segoe UI', 10),
            state='readonly'
        )
        category_values = [f"{cat['name']}" for cat in self.categories]
        self.category_combo['values'] = category_values
        if category_values:
            self.category_combo.current(0)
        self.category_combo.pack(fill='x', pady=(5, 0))
        
        # Unidad de medida
        unit_frame = self.create_label_frame(scrollable_frame, "Unidad de Medida *")
        self.unit_combo = ttk.Combobox(
            unit_frame,
            textvariable=self.unit_var,
            font=('Segoe UI', 10),
            state='readonly'
        )
        unit_values = [f"{unit['name']} ({unit['symbol']})" for unit in self.units]
        self.unit_combo['values'] = unit_values
        if unit_values:
            self.unit_combo.current(0)
        self.unit_combo.pack(fill='x', pady=(5, 0))
        
        # === SECCIÓN: PRECIOS ===
        self.create_section_header(scrollable_frame, "💰 Precios y Costos")
        
        # Fila de precio y costo
        price_row = tk.Frame(scrollable_frame, bg='white')
        price_row.pack(fill='x', pady=5)
        
        # Precio de venta
        price_col = tk.Frame(price_row, bg='white')
        price_col.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.create_field(
            price_col, "Precio de Venta *", self.price_var,
            placeholder="0.00", width=20
        )
        
        # Costo
        cost_col = tk.Frame(price_row, bg='white')
        cost_col.pack(side='left', fill='x', expand=True)
        self.create_field(
            cost_col, "Costo *", self.cost_var,
            placeholder="0.00", width=20
        )
        
        # Margen de ganancia (calculado)
        margin_frame = tk.Frame(scrollable_frame, bg='#e8f5e9', relief='solid', bd=1)
        margin_frame.pack(fill='x', pady=5)
        
        tk.Label(
            margin_frame,
            text="📊 Margen de Ganancia:",
            font=('Segoe UI', 9, 'bold'),
            bg='#e8f5e9'
        ).pack(side='left', padx=10, pady=8)
        
        self.margin_label = tk.Label(
            margin_frame,
            text="0.0%",
            font=('Segoe UI', 11, 'bold'),
            bg='#e8f5e9',
            fg='#27ae60'
        )
        self.margin_label.pack(side='right', padx=10, pady=8)
        
        # Bind para calcular margen
        self.price_var.trace('w', self.calculate_margin)
        self.cost_var.trace('w', self.calculate_margin)
        
        # Tasa de impuesto
        self.create_field(
            scrollable_frame, "Tasa de Impuesto (%)", self.tax_rate_var,
            placeholder="0.0"
        )
        
        # === SECCIÓN: INVENTARIO ===
        self.create_section_header(scrollable_frame, "📦 Inventario")
        
        # Fila de stock
        stock_row = tk.Frame(scrollable_frame, bg='white')
        stock_row.pack(fill='x', pady=5)
        
        # Stock actual
        stock_col = tk.Frame(stock_row, bg='white')
        stock_col.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.create_field(
            stock_col, "Stock Actual", self.stock_var,
            placeholder="0", width=15
        )
        
        # Stock mínimo
        min_col = tk.Frame(stock_row, bg='white')
        min_col.pack(side='left', fill='x', expand=True, padx=5)
        self.create_field(
            min_col, "Stock Mínimo", self.min_stock_var,
            placeholder="0", width=15
        )
        
        # Stock máximo
        max_col = tk.Frame(stock_row, bg='white')
        max_col.pack(side='left', fill='x', expand=True, padx=(5, 0))
        self.create_field(
            max_col, "Stock Máximo", self.max_stock_var,
            placeholder="0", width=15
        )
        
        # === SECCIÓN: ESTADO ===
        self.create_section_header(scrollable_frame, "⚙️ Estado")
        
        status_frame = tk.Frame(scrollable_frame, bg='white')
        status_frame.pack(fill='x', pady=5)
        
        tk.Radiobutton(
            status_frame,
            text="✅ Activo",
            variable=self.status_var,
            value="active",
            font=('Segoe UI', 10),
            bg='white',
            activebackground='white'
        ).pack(side='left', padx=(0, 20))
        
        tk.Radiobutton(
            status_frame,
            text="❌ Inactivo",
            variable=self.status_var,
            value="inactive",
            font=('Segoe UI', 10),
            bg='white',
            activebackground='white'
        ).pack(side='left')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Footer con botones
        self.create_footer()
    
    def create_section_header(self, parent, title: str):
        """Crear encabezado de sección"""
        header_frame = tk.Frame(parent, bg='white')
        header_frame.pack(fill='x', pady=(15, 10))
        
        tk.Label(
            header_frame,
            text=title,
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left')
        
        # Línea separadora
        separator = tk.Frame(header_frame, bg='#bdc3c7', height=2)
        separator.pack(side='left', fill='x', expand=True, padx=(10, 0))
    
    def create_label_frame(self, parent, label: str):
        """Crear frame con etiqueta"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='x', pady=5)
        
        tk.Label(
            frame,
            text=label,
            font=('Segoe UI', 9, 'bold'),
            bg='white',
            fg='#34495e'
        ).pack(anchor='w')
        
        return frame
    
    def create_field(self, parent, label: str, variable: tk.StringVar, 
                    placeholder: str = "", width: int = 40) -> tk.Entry:
        """Crear campo de entrada con etiqueta"""
        frame = self.create_label_frame(parent, label)
        
        entry = tk.Entry(
            frame,
            textvariable=variable,
            font=('Segoe UI', 10),
            width=width,
            relief='solid',
            bd=1
        )
        entry.pack(fill='x', pady=(5, 0))
        
        # Placeholder
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(fg='#95a5a6')
            
            def on_focus_in(e):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg='#2c3e50')
            
            def on_focus_out(e):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(fg='#95a5a6')
            
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)
        
        return entry
    
    def create_footer(self):
        """Crear footer con botones"""
        footer = tk.Frame(self.dialog, bg='#ecf0f1', height=70)
        footer.pack(fill='x', side='bottom')
        footer.pack_propagate(False)
        
        button_frame = tk.Frame(footer, bg='#ecf0f1')
        button_frame.pack(expand=True)
        
        # Botón Guardar
        tk.Button(
            button_frame,
            text="💾 Guardar",
            font=('Segoe UI', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=30,
            pady=10,
            command=self.on_save
        ).pack(side='left', padx=10)
        
        # Botón Cancelar
        tk.Button(
            button_frame,
            text="❌ Cancelar",
            font=('Segoe UI', 11),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=30,
            pady=10,
            command=self.on_cancel
        ).pack(side='left', padx=10)
    
    def calculate_margin(self, *args):
        """Calcular margen de ganancia"""
        try:
            price = float(self.price_var.get() or 0)
            cost = float(self.cost_var.get() or 0)
            
            if cost > 0:
                margin = ((price - cost) / cost) * 100
                color = '#27ae60' if margin > 0 else '#e74c3c'
                self.margin_label.config(text=f"{margin:.1f}%", fg=color)
            else:
                self.margin_label.config(text="0.0%", fg='#95a5a6')
        except ValueError:
            self.margin_label.config(text="0.0%", fg='#95a5a6')
    
    def load_product_data(self):
        """Cargar datos del producto para edición"""
        if not self.product:
            return
        
        self.sku_var.set(self.product.get('sku', ''))
        self.name_var.set(self.product.get('name', ''))
        self.description_text.delete('1.0', tk.END)
        self.description_text.insert('1.0', self.product.get('description', ''))
        self.barcode_var.set(self.product.get('barcode', ''))
        
        # Categoría
        category_name = self.product.get('category_name', '')
        if category_name:
            self.category_var.set(category_name)
        
        # Unidad
        unit_name = self.product.get('unit_name', '')
        unit_symbol = self.product.get('unit_symbol', '')
        if unit_name:
            self.unit_var.set(f"{unit_name} ({unit_symbol})")
        
        self.price_var.set(str(self.product.get('price', 0)))
        self.cost_var.set(str(self.product.get('cost', 0)))
        self.stock_var.set(str(self.product.get('stock_quantity', 0)))
        self.min_stock_var.set(str(self.product.get('min_stock', 0)))
        self.max_stock_var.set(str(self.product.get('max_stock', 0)))
        self.tax_rate_var.set(str(self.product.get('tax_rate', 0)))
        self.status_var.set(self.product.get('status', 'active'))
    
    def validate_data(self) -> tuple[bool, str]:
        """Validar datos del formulario"""
        # SKU
        if not self.sku_var.get().strip():
            return False, "El SKU es requerido"
        
        # Nombre
        if not self.name_var.get().strip():
            return False, "El nombre es requerido"
        
        # Categoría
        if not self.category_var.get():
            return False, "La categoría es requerida"
        
        # Unidad
        if not self.unit_var.get():
            return False, "La unidad de medida es requerida"
        
        # Precio
        try:
            price = float(self.price_var.get())
            if price < 0:
                return False, "El precio no puede ser negativo"
        except ValueError:
            return False, "El precio debe ser un número válido"
        
        # Costo
        try:
            cost = float(self.cost_var.get())
            if cost < 0:
                return False, "El costo no puede ser negativo"
        except ValueError:
            return False, "El costo debe ser un número válido"
        
        # Stock
        try:
            stock = float(self.stock_var.get())
            if stock < 0:
                return False, "El stock no puede ser negativo"
        except ValueError:
            return False, "El stock debe ser un número válido"
        
        # Stock mínimo
        try:
            min_stock = float(self.min_stock_var.get())
            if min_stock < 0:
                return False, "El stock mínimo no puede ser negativo"
        except ValueError:
            return False, "El stock mínimo debe ser un número válido"
        
        # Stock máximo
        try:
            max_stock = float(self.max_stock_var.get())
            if max_stock < 0:
                return False, "El stock máximo no puede ser negativo"
        except ValueError:
            return False, "El stock máximo debe ser un número válido"
        
        # Tasa de impuesto
        try:
            tax = float(self.tax_rate_var.get())
            if tax < 0 or tax > 100:
                return False, "La tasa de impuesto debe estar entre 0 y 100"
        except ValueError:
            return False, "La tasa de impuesto debe ser un número válido"
        
        return True, ""
    
    def get_product_data(self) -> Dict[str, Any]:
        """Obtener datos del formulario"""
        # Obtener ID de categoría
        category_id = None
        category_name = self.category_var.get()
        for cat in self.categories:
            if cat['name'] == category_name:
                category_id = cat['id']
                break
        
        # Obtener ID de unidad
        unit_id = None
        unit_text = self.unit_var.get()
        for unit in self.units:
            if f"{unit['name']} ({unit['symbol']})" == unit_text:
                unit_id = unit['id']
                break
        
        return {
            'sku': self.sku_var.get().strip(),
            'name': self.name_var.get().strip(),
            'description': self.description_text.get('1.0', tk.END).strip(),
            'category_id': category_id,
            'unit_id': unit_id,
            'barcode': self.barcode_var.get().strip(),
            'price': float(self.price_var.get()),
            'cost': float(self.cost_var.get()),
            'stock_quantity': float(self.stock_var.get()),
            'min_stock': float(self.min_stock_var.get()),
            'max_stock': float(self.max_stock_var.get()),
            'tax_rate': float(self.tax_rate_var.get()),
            'status': self.status_var.get()
        }
    
    def on_save(self):
        """Manejar guardar"""
        # Validar
        is_valid, error_msg = self.validate_data()
        if not is_valid:
            messagebox.showerror("Error de validación", error_msg, parent=self.dialog)
            return
        
        # Obtener datos
        self.result = self.get_product_data()
        self.dialog.destroy()
    
    def on_cancel(self):
        """Manejar cancelar"""
        self.result = None
        self.dialog.destroy()
    
    def show(self) -> Optional[Dict[str, Any]]:
        """Mostrar diálogo y retornar resultado"""
        self.dialog.wait_window()
        return self.result
