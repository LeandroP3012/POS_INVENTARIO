"""
Diálogo para Crear/Editar Productos
Formulario modal para gestión de productos
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional, List
from decimal import Decimal
import logging


class ProductFormDialog:
    """Diálogo para crear o editar productos"""
    
    def __init__(self, parent, product: Optional[Dict[str, Any]] = None, 
                 categories: List[Dict[str, Any]] = None, 
                 units: List[Dict[str, Any]] = None):
        self.parent = parent
        self.product = product
        self.categories = categories or []
        self.units = units or []
        self.logger = logging.getLogger('view.ProductFormDialog')
        self.result = None
        
        # Crear ventana
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Editar Producto" if product else "Nuevo Producto")
        self.dialog.geometry("700x800")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Configurar protocolo de cierre (X)
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
        # Centrar ventana
        self.center_window()
        
        # Variables
        self.setup_variables()
        
        # Crear interfaz
        self.create_widgets()
        
        # Si es edición, cargar datos
        if self.product:
            self.load_product_data()
        else:
            # Si es nuevo producto, auto-generar SKU y código de barras
            self.dialog.after(200, self.auto_generate_on_new)
    
    def auto_generate_on_new(self):
        """Auto-generar SKU y código de barras para nuevos productos"""
        try:
            from models.product_model import ProductModel
            product_model = ProductModel()
            
            # Generar SKU (código)
            next_sku = product_model.generate_next_code()
            self.sku_var.set(next_sku)
            
            # Generar código de barras
            barcode = product_model.generate_barcode_from_code(next_sku)
            self.barcode_var.set(barcode)
            
            # Forzar actualización visual de los Entry widgets
            self.sku_entry.delete(0, tk.END)
            self.sku_entry.insert(0, next_sku)
            
            self.barcode_entry.delete(0, tk.END)
            self.barcode_entry.insert(0, barcode)
            
            # Log para debugging
            print(f"✅ Auto-generado: SKU={next_sku}, Código={barcode}")
            
            # Focus en el campo de nombre
            self.dialog.after(50, lambda: self.dialog.focus())
        except Exception as e:
            self.logger.error(f"Error en auto-generación: {e}")
            print(f"❌ Error en auto-generación: {e}")
            # Si falla, solo hacer focus en SKU
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
        # Crear variables (sin master, tkinter usa el root por defecto)
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
        self.status_var = tk.StringVar(value="active")
        
        # NO configurar trace aquí - lo haremos después de crear los widgets
    
    def create_widgets(self):
        """Crear widgets del formulario"""
        # Header mejorado
        header = tk.Frame(self.dialog, bg='#2c3e50', height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        icon = "✏️" if self.product else "➕"
        title = "Editar Producto" if self.product else "Nuevo Producto"
        
        tk.Label(
            header,
            text=f"{icon}  {title}",
            font=('Segoe UI', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=20)
        
        # Contenido principal con scroll mejorado
        main_container = tk.Frame(self.dialog, bg='#ecf0f1')
        main_container.pack(fill='both', expand=True)
        
        # Canvas con scrollbar - Guardar como atributo de instancia
        self.canvas = tk.Canvas(main_container, bg='#ecf0f1', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=self.canvas.yview)
        scrollable_frame = tk.Frame(self.canvas, bg='#ecf0f1')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=680)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # === SECCIÓN: INFORMACIÓN BÁSICA ===
        basic_section = self.create_card(scrollable_frame)
        self.create_section_title(basic_section, "📋", "Información Básica")
        
        # SKU con botón de auto-generar
        sku_row = tk.Frame(basic_section, bg='white')
        sku_row.pack(fill='x', padx=20, pady=(0, 15))
        
        tk.Label(
            sku_row,
            text="SKU *",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#2c3e50',
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        sku_input_row = tk.Frame(sku_row, bg='white')
        sku_input_row.pack(fill='x')
        
        self.sku_entry = tk.Entry(
            sku_input_row,
            textvariable=self.sku_var,
            font=('Segoe UI', 11),
            relief='solid',
            bd=1,
            bg='#f8f9fa'
        )
        self.sku_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        # Botón generar SKU
        tk.Button(
            sku_input_row,
            text="🔄 Auto-generar",
            font=('Segoe UI', 9),
            bg='#3498db',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=5,
            command=self.generate_sku
        ).pack(side='left')
        
        # Nombre
        name_container = tk.Frame(basic_section, bg='white')
        name_container.pack(fill='x', padx=20, pady=(0, 15))
        
        tk.Label(
            name_container,
            text="Nombre del Producto *",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#2c3e50',
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        self.name_entry = tk.Entry(
            name_container,
            textvariable=self.name_var,
            font=('Segoe UI', 11),
            relief='solid',
            bd=1,
            bg='#f8f9fa'
        )
        self.name_entry.pack(fill='x')
        
        # Descripción (Text widget más grande)
        desc_label = tk.Label(
            basic_section,
            text="Descripción",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#2c3e50',
            anchor='w'
        )
        desc_label.pack(fill='x', padx=20, pady=(10, 5))
        
        desc_container = tk.Frame(basic_section, bg='white')
        desc_container.pack(fill='x', padx=20, pady=(0, 15))
        
        self.description_text = tk.Text(
            desc_container,
            height=4,
            font=('Segoe UI', 10),
            relief='solid',
            bd=1,
            wrap='word',
            bg='#f8f9fa'
        )
        self.description_text.pack(fill='x')
        
        # Código de barras con botones
        barcode_row = tk.Frame(basic_section, bg='white')
        barcode_row.pack(fill='x', padx=20, pady=(0, 15))
        
        tk.Label(
            barcode_row,
            text="Código de Barras",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#2c3e50',
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        barcode_input_row = tk.Frame(barcode_row, bg='white')
        barcode_input_row.pack(fill='x')
        
        self.barcode_entry = tk.Entry(
            barcode_input_row,
            textvariable=self.barcode_var,
            font=('Segoe UI', 11),
            relief='solid',
            bd=1,
            bg='#f8f9fa'
        )
        self.barcode_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        # Botón generar código de barras
        tk.Button(
            barcode_input_row,
            text="🔄 Generar",
            font=('Segoe UI', 9),
            bg='#2ecc71',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=5,
            command=self.generate_barcode
        ).pack(side='left', padx=(0, 5))
        
        # Botón imprimir código de barras
        tk.Button(
            barcode_input_row,
            text="🖨️ Imprimir",
            font=('Segoe UI', 9),
            bg='#9b59b6',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=5,
            command=self.print_barcode
        ).pack(side='left')
        
        # === SECCIÓN: CATEGORIZACIÓN ===
        cat_section = self.create_card(scrollable_frame)
        self.create_section_title(cat_section, "🏷️", "Categorización")
        
        # Categoría y Unidad en fila
        cat_row = tk.Frame(cat_section, bg='white')
        cat_row.pack(fill='x', padx=20, pady=(0, 15))
        
        # Columna de categoría
        cat_col = tk.Frame(cat_row, bg='white')
        cat_col.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        tk.Label(
            cat_col,
            text="Categoría *",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#2c3e50',
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        self.category_combo = ttk.Combobox(
            cat_col,
            textvariable=self.category_var,
            font=('Segoe UI', 11),
            state='readonly',
            height=8
        )
        category_values = [cat['name'] for cat in self.categories]
        self.category_combo['values'] = category_values
        if category_values:
            self.category_combo.current(0)
        self.category_combo.pack(fill='x')
        
        # Columna de unidad
        unit_col = tk.Frame(cat_row, bg='white')
        unit_col.pack(side='left', fill='both', expand=True)
        
        tk.Label(
            unit_col,
            text="Unidad de Medida *",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#2c3e50',
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        self.unit_combo = ttk.Combobox(
            unit_col,
            textvariable=self.unit_var,
            font=('Segoe UI', 11),
            state='readonly',
            height=8
        )
        unit_values = [f"{unit['name']} ({unit['symbol']})" for unit in self.units]
        self.unit_combo['values'] = unit_values
        if unit_values:
            self.unit_combo.current(0)
        self.unit_combo.pack(fill='x')
        
        # === SECCIÓN: PRECIOS Y COSTOS ===
        price_section = self.create_card(scrollable_frame)
        self.create_section_title(price_section, "💰", "Precios y Costos")
        
        # Fila de precio y costo
        price_row = tk.Frame(price_section, bg='white')
        price_row.pack(fill='x', padx=20, pady=(0, 10))
        
        # Precio de venta
        price_col = tk.Frame(price_row, bg='white')
        price_col.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        tk.Label(
            price_col,
            text="Precio de Venta *",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#2c3e50',
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        price_entry = tk.Entry(
            price_col,
            font=('Segoe UI', 12),
            relief='solid',
            bd=1,
            bg='#f8f9fa'
        )
        price_entry.pack(fill='x')
        
        # Solución: actualizar StringVar manualmente en cada KeyRelease
        def sync_price(*args):
            value = price_entry.get()
            self.price_var.set(value)
            print(f"💰 Sincronizando price: {value}")
        
        price_entry.bind('<KeyRelease>', sync_price)
        price_entry.bind('<FocusOut>', sync_price)
        
        # Guardar referencia al entry
        self.price_entry = price_entry
        
        # Costo
        cost_col = tk.Frame(price_row, bg='white')
        cost_col.pack(side='left', fill='both', expand=True)
        
        tk.Label(
            cost_col,
            text="Costo de Adquisición *",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#2c3e50',
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        cost_entry = tk.Entry(
            cost_col,
            font=('Segoe UI', 12),
            relief='solid',
            bd=1,
            bg='#f8f9fa'
        )
        cost_entry.pack(fill='x')
        
        # Solución: actualizar StringVar manualmente en cada KeyRelease
        def sync_cost(*args):
            value = cost_entry.get()
            self.cost_var.set(value)
            print(f"💵 Sincronizando cost: {value}")
        
        cost_entry.bind('<KeyRelease>', sync_cost)
        cost_entry.bind('<FocusOut>', sync_cost)
        
        # Guardar referencia al entry
        self.cost_entry = cost_entry
        
        # Margen de ganancia (destacado)
        self.margin_frame = tk.Frame(price_section, bg='#e8f5e9', relief='solid', bd=1)
        self.margin_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        margin_inner = tk.Frame(self.margin_frame, bg='#e8f5e9')
        margin_inner.pack(fill='x', padx=15, pady=12)
        
        tk.Label(
            margin_inner,
            text="💹 Margen de Ganancia:",
            font=('Segoe UI', 10, 'bold'),
            bg='#e8f5e9',
            fg='#2c3e50'
        ).pack(side='left')
        
        self.margin_label = tk.Label(
            margin_inner,
            text="0.00%",
            font=('Segoe UI', 14, 'bold'),
            bg='#e8f5e9',
            fg='#27ae60'
        )
        self.margin_label.pack(side='right')
        
        # AHORA configurar trace para calcular margen automáticamente
        print("🔧 Configurando trace DESPUÉS de crear margin_label")
        self.price_var.trace_add('write', self.calculate_margin)
        self.cost_var.trace_add('write', self.calculate_margin)
        print(f"   ✅ Trace configurado con trace_add")
        
        # Calcular margen inicial
        self.dialog.after(100, self.calculate_margin)
        
        # === SECCIÓN: GESTIÓN DE INVENTARIO ===
        inventory_section = self.create_card(scrollable_frame)
        self.create_section_title(inventory_section, "📦", "Gestión de Inventario")
        
        # Nota informativa - TODO el inventario se maneja desde Control de Stock
        note_frame = tk.Frame(inventory_section, bg='#fff3cd', relief='solid', bd=1)
        note_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        tk.Label(
            note_frame,
            text="ℹ️ Stock Inicial",
            font=('Segoe UI', 10, 'bold'),
            bg='#fff3cd',
            fg='#856404',
            anchor='w'
        ).pack(padx=15, pady=(10, 5))
        
        tk.Label(
            note_frame,
            text="El producto se creará con stock inicial = 0.\nPara agregar inventario, utilice el módulo 'Control de Stock' (📊) desde el dashboard.",
            font=('Segoe UI', 9),
            bg='#fff3cd',
            fg='#856404',
            anchor='w',
            wraplength=600,
            justify='left'
        ).pack(padx=15, pady=(0, 10))
        
        # === SECCIÓN: ESTADO ===
        status_section = self.create_card(scrollable_frame)
        self.create_section_title(status_section, "⚡", "Estado del Producto")
        
        status_container = tk.Frame(status_section, bg='white')
        status_container.pack(fill='x', padx=20, pady=(0, 15))
        
        tk.Label(
            status_container,
            text="Estado:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 10))
        
        radio_frame = tk.Frame(status_container, bg='white')
        radio_frame.pack(anchor='w')
        
        tk.Radiobutton(
            radio_frame,
            text="✅ Activo",
            variable=self.status_var,
            value="active",
            font=('Segoe UI', 11),
            bg='white',
            activebackground='white',
            selectcolor='#e8f5e9'
        ).pack(side='left', padx=(0, 30))
        
        tk.Radiobutton(
            radio_frame,
            text="❌ Inactivo",
            variable=self.status_var,
            value="inactive",
            font=('Segoe UI', 11),
            bg='white',
            activebackground='white',
            selectcolor='#ffebee'
        ).pack(side='left')
        
        # Empaquetar canvas y scrollbar
        self.canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Habilitar scroll con rueda del mouse - SOLO en el canvas, no globalmente
        def _on_mousewheel(event):
            try:
                if self.canvas.winfo_exists():
                    self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                # El canvas ya fue destruido, ignorar
                pass
        
        # Bind solo al canvas, no a toda la aplicación
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))
        
        # Footer con botones mejorados
        footer = tk.Frame(self.dialog, bg='#ecf0f1', height=80)
        footer.pack(fill='x')
        footer.pack_propagate(False)
        
        button_container = tk.Frame(footer, bg='#ecf0f1')
        button_container.pack(expand=True)
        
        # Botón Guardar
        save_btn = tk.Button(
            button_container,
            text="💾 Guardar",
            command=self.on_save,
            font=('Segoe UI', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=30,
            pady=12
        )
        save_btn.pack(side='left', padx=10)
        
        # Botón Cancelar
        cancel_btn = tk.Button(
            button_container,
            text="❌ Cancelar",
            command=self.on_cancel,
            font=('Segoe UI', 12),
            bg='#95a5a6',
            fg='white',
            activebackground='#7f8c8d',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=30,
            pady=12
        )
        cancel_btn.pack(side='left', padx=10)
    
    def create_card(self, parent):
        """Crear tarjeta de sección con fondo blanco"""
        card = tk.Frame(parent, bg='white', relief='solid', bd=1)
        card.pack(fill='x', padx=15, pady=10)
        return card
    
    def create_section_title(self, parent, icon, title):
        """Crear título de sección"""
        title_frame = tk.Frame(parent, bg='#f8f9fa')
        title_frame.pack(fill='x')
        
        tk.Label(
            title_frame,
            text=f"{icon}  {title}",
            font=('Segoe UI', 12, 'bold'),
            bg='#f8f9fa',
            fg='#2c3e50',
            anchor='w'
        ).pack(fill='x', padx=20, pady=12)
    
    def create_input_field(self, parent, label_text, variable, placeholder=""):
        """Crear campo de entrada con etiqueta"""
        container = tk.Frame(parent, bg='white')
        container.pack(fill='x', padx=20, pady=(0, 15))
        
        label = tk.Label(
            container,
            text=label_text,
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#2c3e50',
            anchor='w'
        )
        label.pack(fill='x', pady=(0, 5))
        
        entry = tk.Entry(
            container,
            textvariable=variable,
            font=('Segoe UI', 11),
            relief='solid',
            bd=1,
            bg='#f8f9fa'
        )
        entry.pack(fill='x')
        
        return entry
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
        return entry
    
    def calculate_margin(self, *args):
        """Calcular margen de ganancia"""
        try:
            # Debug
            print(f"🧮 calculate_margin llamado")
            print(f"   price_var: {self.price_var.get()}")
            print(f"   cost_var: {self.cost_var.get()}")
            
            # Verificar que el label existe
            if not hasattr(self, 'margin_label'):
                print(f"   ⚠️ margin_label aún no existe, saltando cálculo")
                return
            
            price = float(self.price_var.get() or 0)
            cost = float(self.cost_var.get() or 0)
            
            print(f"   price (float): {price}")
            print(f"   cost (float): {cost}")
            
            if cost > 0:
                margin = ((price - cost) / cost) * 100
                color = '#27ae60' if margin > 0 else '#e74c3c'
                self.margin_label.config(text=f"{margin:.1f}%", fg=color)
                print(f"   ✅ Margen calculado: {margin:.1f}%")
            else:
                self.margin_label.config(text="0.0%", fg='#95a5a6')
                print(f"   ⚠️ Costo es 0, margen = 0.0%")
        except ValueError as e:
            print(f"   ❌ Error de conversión: {e}")
            if hasattr(self, 'margin_label'):
                self.margin_label.config(text="0.0%", fg='#95a5a6')
        except Exception as e:
            print(f"   ❌ Error inesperado: {e}")
            if hasattr(self, 'margin_label'):
                self.margin_label.config(text="0.0%", fg='#95a5a6')
    
    def load_product_data(self):
        """Cargar datos del producto para edición"""
        if not self.product:
            return
        
        print(f"\n🔄 Cargando datos del producto: {self.product.get('sku', 'N/A')}")
        
        # SKU - Cargar en Entry directamente
        sku_value = self.product.get('sku', '')
        if hasattr(self, 'sku_entry'):
            try:
                self.sku_entry.delete(0, tk.END)
                self.sku_entry.insert(0, str(sku_value))
                print(f"   ✅ SKU: {sku_value}")
            except Exception as e:
                print(f"   ⚠️ Error cargando SKU: {e}")
        
        # Nombre - Cargar en Entry directamente
        name_value = self.product.get('name', '')
        if hasattr(self, 'name_entry'):
            try:
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, str(name_value))
                print(f"   ✅ Nombre: {name_value}")
            except Exception as e:
                print(f"   ⚠️ Error cargando Nombre: {e}")
        
        # Descripción - Cargar en Text widget con validación
        description_value = self.product.get('description', '')
        if hasattr(self, 'description_text'):
            try:
                self.description_text.delete('1.0', tk.END)
                if description_value:
                    self.description_text.insert('1.0', str(description_value))
                print(f"   ✅ Descripción cargada")
            except Exception as e:
                print(f"   ⚠️ Error cargando descripción: {e}")
        
        # Código de Barras - Cargar en Entry directamente
        barcode_value = self.product.get('barcode', '')
        if hasattr(self, 'barcode_entry'):
            try:
                self.barcode_entry.delete(0, tk.END)
                self.barcode_entry.insert(0, str(barcode_value))
                print(f"   ✅ Barcode: {barcode_value}")
            except Exception as e:
                print(f"   ⚠️ Error cargando Barcode: {e}")
        
        # Categoría - Cargar en Combobox directamente
        category_name = self.product.get('category_name', '')
        if category_name and hasattr(self, 'category_combo'):
            try:
                self.category_combo.set(str(category_name))
                print(f"   ✅ Categoría: {category_name}")
            except Exception as e:
                print(f"   ⚠️ Error cargando Categoría: {e}")
        
        # Unidad - Cargar en Combobox directamente
        unit_name = self.product.get('unit_name', '')
        unit_symbol = self.product.get('unit_symbol', '')
        if unit_name and hasattr(self, 'unit_combo'):
            try:
                unit_display = f"{unit_name} ({unit_symbol})"
                self.unit_combo.set(str(unit_display))
                print(f"   ✅ Unidad: {unit_display}")
            except Exception as e:
                print(f"   ⚠️ Error cargando Unidad: {e}")
        
        # Precio - Cargar en Entry directamente
        price_value = self.product.get('price', 0)
        if hasattr(self, 'price_entry'):
            try:
                self.price_entry.delete(0, tk.END)
                self.price_entry.insert(0, str(price_value))
                print(f"   ✅ Precio: {price_value}")
            except Exception as e:
                print(f"   ⚠️ Error cargando Precio: {e}")
        
        # Costo - Cargar en Entry directamente
        cost_value = self.product.get('cost', 0)
        if hasattr(self, 'cost_entry'):
            try:
                self.cost_entry.delete(0, tk.END)
                self.cost_entry.insert(0, str(cost_value))
                print(f"   ✅ Costo: {cost_value}")
            except Exception as e:
                print(f"   ⚠️ Error cargando Costo: {e}")
        
        # Estado - Cargar en RadioButtons (via StringVar)
        status_value = self.product.get('status', 'active')
        if hasattr(self, 'status_var'):
            try:
                self.status_var.set(str(status_value))
                print(f"   ✅ Estado: {status_value}")
            except Exception as e:
                print(f"   ⚠️ Error cargando Estado: {e}")
        
        print(f"✅ Datos del producto cargados completamente\n")
    
    def validate_data(self) -> tuple[bool, str]:
        """Validar datos del formulario"""
        print("\n   🔹 Validando SKU...")
        # SKU
        sku = self.sku_var.get().strip()
        print(f"      StringVar SKU: '{sku}'")
        if not sku:
            sku = self.sku_entry.get().strip()
            print(f"      Entry SKU (fallback): '{sku}'")
        if not sku:
            print(f"      ❌ FALLO: SKU vacío")
            return False, "El SKU es requerido"
        print(f"      ✅ SKU válido: '{sku}'")
        
        print("\n   🔹 Validando Nombre...")
        # Nombre - obtener del Entry directamente si StringVar está vacío
        name = self.name_var.get().strip()
        print(f"      StringVar Nombre: '{name}'")
        if not name and hasattr(self, 'name_entry'):
            name = self.name_entry.get().strip()
            print(f"      Entry Nombre (fallback): '{name}'")
        if not name:
            print(f"      ❌ FALLO: Nombre vacío")
            return False, "El nombre es requerido"
        print(f"      ✅ Nombre válido: '{name}'")
        
        print("\n   🔹 Validando Categoría...")
        category_value = self.category_var.get()
        print(f"      StringVar Categoría: '{category_value}'")
        # Fallback: obtener directamente del Combobox
        if not category_value and hasattr(self, 'category_combo'):
            category_value = self.category_combo.get()
            print(f"      Combobox Categoría (fallback): '{category_value}'")
        if not category_value:
            print(f"      ❌ FALLO: Categoría vacía")
            return False, "La categoría es requerida"
        print(f"      ✅ Categoría válida: '{category_value}'")
        
        print("\n   🔹 Validando Unidad...")
        unit_value = self.unit_var.get()
        print(f"      StringVar Unidad: '{unit_value}'")
        # Fallback: obtener directamente del Combobox
        if not unit_value and hasattr(self, 'unit_combo'):
            unit_value = self.unit_combo.get()
            print(f"      Combobox Unidad (fallback): '{unit_value}'")
        if not unit_value:
            print(f"      ❌ FALLO: Unidad vacía")
            return False, "La unidad de medida es requerida"
        print(f"      ✅ Unidad válida: '{unit_value}'")
        
        print("\n   🔹 Validando Precio...")
        price_value = self.price_var.get()
        print(f"      StringVar Precio: '{price_value}'")
        # Precio
        try:
            price = float(self.price_var.get())
            if price < 0:
                print(f"      ❌ FALLO: Precio negativo: {price}")
                return False, "El precio no puede ser negativo"
            print(f"      ✅ Precio válido: {price}")
        except ValueError:
            print(f"      ❌ FALLO: Precio no es número válido")
            return False, "El precio debe ser un número válido"
        
        print("\n   🔹 Validando Costo...")
        cost_value = self.cost_var.get()
        print(f"      StringVar Costo: '{cost_value}'")
        # Costo
        try:
            cost = float(self.cost_var.get())
            if cost < 0:
                print(f"      ❌ FALLO: Costo negativo: {cost}")
                return False, "El costo no puede ser negativo"
            print(f"      ✅ Costo válido: {cost}")
        except ValueError:
            print(f"      ❌ FALLO: Costo no es número válido")
            return False, "El costo debe ser un número válido"
        
        # Stock, min_stock y max_stock ya no se validan - siempre serán 0
        print("\n   🔹 Stock se establecerá en 0 (se gestiona desde Control de Stock)")
        
        print("\n   ✅ TODAS LAS VALIDACIONES PASARON")
        return True, ""
    
    def get_product_data(self) -> Dict[str, Any]:
        """Obtener datos del formulario"""
        # Obtener ID de categoría con fallback
        category_id = None
        category_name = self.category_var.get()
        if not category_name and hasattr(self, 'category_combo'):
            category_name = self.category_combo.get()
        
        for cat in self.categories:
            if cat['name'] == category_name:
                category_id = cat['id']
                break
        
        # Obtener ID de unidad con fallback
        unit_id = None
        unit_text = self.unit_var.get()
        if not unit_text and hasattr(self, 'unit_combo'):
            unit_text = self.unit_combo.get()
        
        for unit in self.units:
            if f"{unit['name']} ({unit['symbol']})" == unit_text:
                unit_id = unit['id']
                break
        
        # Obtener valores con fallback a Entry widgets directos
        sku = self.sku_var.get().strip() or self.sku_entry.get().strip()
        name = self.name_var.get().strip()
        if not name and hasattr(self, 'name_entry'):
            name = self.name_entry.get().strip()
        barcode = self.barcode_var.get().strip() or self.barcode_entry.get().strip()
        
        # Stock siempre será 0 - se gestiona desde Control de Stock
        # Min stock y max stock también en 0 por defecto
        return {
            'sku': sku,
            'name': name,
            'description': self.description_text.get('1.0', tk.END).strip(),
            'category_id': category_id,
            'unit_id': unit_id,
            'barcode': barcode,
            'price': float(self.price_var.get()),
            'cost': float(self.cost_var.get()),
            'stock_quantity': 0.0,  # Siempre 0 - se gestiona desde Control de Stock
            'min_stock': 0.0,
            'max_stock': 0.0,
            'status': self.status_var.get()
        }
    
    def cleanup(self):
        """Limpiar bindings antes de cerrar"""
        try:
            # Desvincular todos los eventos de mousewheel
            self.canvas.unbind_all("<MouseWheel>")
        except:
            pass
    
    def generate_sku(self):
        """Generar SKU automáticamente"""
        try:
            from models.product_model import ProductModel
            product_model = ProductModel()
            next_sku = product_model.generate_next_code()
            
            # Actualizar variable y Entry directamente
            self.sku_var.set(next_sku)
            self.sku_entry.delete(0, tk.END)
            self.sku_entry.insert(0, next_sku)
            
            # También generar código de barras automáticamente
            self.generate_barcode()
            
            messagebox.showinfo(
                "SKU Generado",
                f"Se ha generado el SKU: {next_sku}\nY su código de barras asociado."
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al generar SKU: {str(e)}"
            )
    
    def generate_barcode(self):
        """Generar código de barras basado en el SKU"""
        try:
            sku = self.sku_var.get().strip()
            
            if not sku:
                # Intentar obtenerlo del Entry directamente
                sku = self.sku_entry.get().strip()
            
            if not sku:
                messagebox.showwarning(
                    "SKU Requerido",
                    "Primero debes ingresar o generar un SKU para crear el código de barras."
                )
                return
            
            from models.product_model import ProductModel
            product_model = ProductModel()
            barcode = product_model.generate_barcode_from_code(sku)
            
            # Actualizar variable y Entry directamente
            self.barcode_var.set(barcode)
            self.barcode_entry.delete(0, tk.END)
            self.barcode_entry.insert(0, barcode)
            
            messagebox.showinfo(
                "Código de Barras Generado",
                f"Código de barras EAN-13 generado:\n{barcode}"
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al generar código de barras: {str(e)}"
            )
    
    def print_barcode(self):
        """Imprimir código de barras en la impresora configurada"""
        try:
            barcode_code = self.barcode_var.get().strip()
            if not barcode_code:
                barcode_code = self.barcode_entry.get().strip()
                
            sku = self.sku_var.get().strip()
            if not sku:
                sku = self.sku_entry.get().strip()
                
            name = self.name_var.get().strip()
            
            if not barcode_code:
                messagebox.showwarning(
                    "Código de Barras Requerido",
                    "Primero debes generar un código de barras para imprimirlo."
                )
                return
            
            # Verificar e importar librerías necesarias
            missing_modules = []
            
            try:
                import barcode
                from barcode.writer import ImageWriter
            except ImportError:
                missing_modules.append("python-barcode[images]")
            
            try:
                from PIL import Image, ImageDraw, ImageFont
            except ImportError:
                missing_modules.append("Pillow")
            
            try:
                import win32print
                import win32ui
                from PIL import ImageWin
            except ImportError:
                missing_modules.append("pywin32")
            
            if missing_modules:
                response = messagebox.askyesno(
                    "Módulos Requeridos",
                    f"Para imprimir códigos de barras necesitas instalar:\n\n" +
                    "\n".join(f"  • {m}" for m in missing_modules) +
                    "\n\n¿Deseas instalarlos ahora?\n\n" +
                    "Se ejecutará: pip install " + " ".join(missing_modules)
                )
                
                if response:
                    # Intentar instalar módulos
                    import subprocess
                    import sys
                    
                    try:
                        messagebox.showinfo(
                            "Instalando...",
                            "Por favor espera mientras se instalan los módulos.\n" +
                            "Esto puede tomar algunos minutos."
                        )
                        
                        cmd = [sys.executable, "-m", "pip", "install"] + missing_modules
                        subprocess.check_call(cmd)
                        
                        messagebox.showinfo(
                            "Instalación Completa",
                            "Módulos instalados correctamente.\n\n" +
                            "Por favor, reinicia la aplicación para usar la función de impresión."
                        )
                    except Exception as e:
                        messagebox.showerror(
                            "Error de Instalación",
                            f"No se pudieron instalar los módulos automáticamente:\n{str(e)}\n\n" +
                            "Por favor, instálalos manualmente ejecutando:\n" +
                            f"pip install {' '.join(missing_modules)}"
                        )
                return
            
            # Si llegamos aquí, todos los módulos están instalados
            import barcode
            from barcode.writer import ImageWriter
            from PIL import Image, ImageDraw, ImageFont, ImageWin
            import tempfile
            import os
            import win32print
            import win32ui
            
            # Generar imagen del código de barras
            EAN = barcode.get_barcode_class('ean13')
            ean = EAN(barcode_code, writer=ImageWriter())
            
            # Crear archivo temporal
            temp_dir = tempfile.gettempdir()
            barcode_filename = os.path.join(temp_dir, f'barcode_{sku}')
            
            # Guardar imagen
            options = {
                'module_width': 0.3,
                'module_height': 15.0,
                'quiet_zone': 6.5,
                'font_size': 10,
                'text_distance': 5.0,
                'background': 'white',
                'foreground': 'black',
            }
            ean.save(barcode_filename, options=options)
            
            # Abrir imagen generada
            img_path = f"{barcode_filename}.png"
            img = Image.open(img_path)
            
            # Agregar nombre del producto arriba del código de barras
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", 12)
            except:
                font = ImageFont.load_default()
            
            # Crear nueva imagen con espacio para el nombre
            new_img = Image.new('RGB', (img.width, img.height + 30), 'white')
            draw = ImageDraw.Draw(new_img)
            
            # Dibujar nombre centrado
            text = name[:40] if len(name) > 40 else name
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = (new_img.width - text_width) // 2
            draw.text((text_x, 5), text, fill='black', font=font)
            
            # Pegar código de barras
            new_img.paste(img, (0, 30))
            
            # Obtener impresora configurada
            printer_name = None
            try:
                # Intentar leer configuración del sistema
                import json
                config_path = os.path.join('config', 'system_config.json')
                if os.path.exists(config_path):
                    with open(config_path, 'r', encoding='utf-8') as f:
                        system_config = json.load(f)
                        # La impresora está directamente en la raíz del JSON
                        printer_name = system_config.get('printer')
                        print(f"📄 Configuración leída: printer='{printer_name}'")
            except Exception as e:
                print(f"⚠️ No se pudo leer configuración de impresora: {e}")
            
            if not printer_name or printer_name == "":
                # Usar impresora predeterminada
                try:
                    printer_name = win32print.GetDefaultPrinter()
                    print(f"📄 Usando impresora predeterminada del sistema: {printer_name}")
                except Exception as e:
                    messagebox.showerror(
                        "Error",
                        f"No se pudo detectar ninguna impresora:\n{str(e)}\n\n" +
                        "Verifica que tengas al menos una impresora instalada."
                    )
                    return
            else:
                print(f"✅ Usando impresora configurada en sistema: {printer_name}")
            
            # Verificar que la impresora existe
            try:
                available_printers = [printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)]
                print(f"🖨️ Impresoras disponibles: {available_printers}")
                
                if printer_name not in available_printers:
                    print(f"⚠️ Impresora '{printer_name}' no encontrada en el sistema")
                    messagebox.showwarning(
                        "Impresora No Encontrada",
                        f"La impresora configurada '{printer_name}' no está disponible.\n\n" +
                        f"Impresoras disponibles:\n" + "\n".join(f"  • {p}" for p in available_printers) +
                        f"\n\nSe usará la impresora predeterminada."
                    )
                    printer_name = win32print.GetDefaultPrinter()
                    print(f"📄 Usando impresora predeterminada: {printer_name}")
            except Exception as e:
                print(f"⚠️ Error al verificar impresoras: {e}")
            
            # Imprimir
            print(f"🖨️ Iniciando impresión en: {printer_name}")
            hDC = win32ui.CreateDC()
            hDC.CreatePrinterDC(printer_name)
            hDC.StartDoc(f"Código de Barras - {sku}")
            hDC.StartPage()
            
            # Convertir imagen para Windows
            dib = ImageWin.Dib(new_img)
            
            # Calcular posición centrada en la página
            printer_size = hDC.GetDeviceCaps(110), hDC.GetDeviceCaps(111)  # PHYSICALWIDTH, PHYSICALHEIGHT
            img_size = new_img.size
            
            # Escalar imagen para que quepa bien (no muy grande)
            scale = min(printer_size[0] / img_size[0], printer_size[1] / img_size[1]) * 0.5
            scaled_width = int(img_size[0] * scale)
            scaled_height = int(img_size[1] * scale)
            
            # Centrar
            x = (printer_size[0] - scaled_width) // 2
            y = (printer_size[1] - scaled_height) // 4  # Más arriba
            
            # Dibujar en la página
            dib.draw(hDC.GetHandleOutput(), (x, y, x + scaled_width, y + scaled_height))
            
            hDC.EndPage()
            hDC.EndDoc()
            hDC.DeleteDC()
            
            # Limpiar archivo temporal
            try:
                os.remove(img_path)
            except:
                pass
            
            messagebox.showinfo(
                "Impresión Exitosa",
                f"Código de barras enviado a la impresora:\n{printer_name}"
            )
            
        except Exception as e:
            messagebox.showerror(
                "Error de Impresión",
                f"Error al imprimir código de barras:\n{str(e)}\n\n"
                "Verifica que:\n"
                "1. La impresora esté conectada y encendida\n"
                "2. Tengas los módulos instalados (python-barcode, Pillow, pywin32)"
            )
    
    def on_save(self):
        """Manejar guardar"""
        print("\n" + "="*60)
        print("🔍 DEBUG: Iniciando validación de formulario")
        print("="*60)
        
        # DEBUG: Mostrar valores de todas las variables
        print("\n📋 VALORES DE VARIABLES:")
        print(f"   SKU (var): '{self.sku_var.get()}'")
        print(f"   SKU (entry): '{self.sku_entry.get()}'")
        
        print(f"   Nombre (var): '{self.name_var.get()}'")
        if hasattr(self, 'name_entry'):
            print(f"   Nombre (entry): '{self.name_entry.get()}'")
        
        print(f"   Categoría (var): '{self.category_var.get()}'")
        if hasattr(self, 'category_combo'):
            print(f"   Categoría (combo): '{self.category_combo.get()}'")
        
        print(f"   Unidad (var): '{self.unit_var.get()}'")
        if hasattr(self, 'unit_combo'):
            print(f"   Unidad (combo): '{self.unit_combo.get()}'")
        
        print(f"   Código de Barras (var): '{self.barcode_var.get()}'")
        print(f"   Código de Barras (entry): '{self.barcode_entry.get()}'")
        
        print(f"   Precio (var): '{self.price_var.get()}'")
        print(f"   Costo (var): '{self.cost_var.get()}'")
        print(f"   Estado (var): '{self.status_var.get()}'")
        print(f"   ℹ️ Stock se establecerá en 0 (gestión desde Control de Stock)")
        
        print("\n📦 CATEGORÍAS DISPONIBLES:")
        for i, cat in enumerate(self.categories):
            print(f"   {i+1}. {cat.get('name')} (ID: {cat.get('id')})")
        
        print("\n📏 UNIDADES DISPONIBLES:")
        for i, unit in enumerate(self.units):
            print(f"   {i+1}. {unit.get('name')} ({unit.get('symbol')}) (ID: {unit.get('id')})")
        
        # Validar
        print("\n🔍 Ejecutando validación...")
        is_valid, error_msg = self.validate_data()
        
        if not is_valid:
            print(f"\n❌ VALIDACIÓN FALLIDA: {error_msg}")
            print("="*60 + "\n")
            messagebox.showerror("Error de validación", error_msg, parent=self.dialog)
            return
        
        print("\n✅ VALIDACIÓN EXITOSA")
        
        # Obtener datos
        print("\n📊 Obteniendo datos del producto...")
        self.result = self.get_product_data()
        
        print("\n📦 DATOS DEL PRODUCTO:")
        for key, value in self.result.items():
            print(f"   {key}: {value}")
        
        print("\n✅ GUARDADO EXITOSO")
        print("="*60 + "\n")
        
        # Limpiar bindings antes de destruir
        self.cleanup()
        self.dialog.destroy()
    
    def on_cancel(self):
        """Manejar cancelar"""
        self.result = None
        
        # Limpiar bindings antes de destruir
        self.cleanup()
        self.dialog.destroy()
    
    def show(self) -> Optional[Dict[str, Any]]:
        """Mostrar diálogo y retornar resultado"""
        self.dialog.wait_window()
        return self.result
