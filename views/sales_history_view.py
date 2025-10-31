"""Vista de Historial de Ventas"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, Any, Callable, List, Optional
from datetime import datetime
from decimal import Decimal

from views.base_view import BaseView
from services.permission_service import PermissionService
from utils.responsive_utils import ResponsiveManager


class SalesHistoryView(BaseView):
    """Vista para visualizar y administrar el historial de ventas"""

    def __init__(self, parent, user_data: Dict[str, Any]):
        self.parent = parent
        self.user_data = user_data or {}
        super().__init__(parent)

        self.permission_service = PermissionService()
        self.responsive = ResponsiveManager(self.root)

        self.callbacks: Dict[str, Callable] = {}
        self.navbar_built = False

        # Datos
        self.sales_data: List[Dict[str, Any]] = []
        self.sales_index: Dict[int, Dict[str, Any]] = {}
        self.selected_sale: Optional[Dict[str, Any]] = None

        # Variables de filtro
        self.filter_sale_number = tk.StringVar()
        self.filter_customer = tk.StringVar()
        self.filter_status = tk.StringVar(value='completed')
        self.filter_date_from = tk.StringVar()
        self.filter_date_to = tk.StringVar()
        self.filter_cashier = tk.StringVar()

        # Widgets iniciales
        self.main_frame: Optional[tk.Frame] = None
        self.sales_tree: Optional[ttk.Treeview] = None
        self.detail_text: Optional[tk.Text] = None
        self.items_tree: Optional[ttk.Treeview] = None
        self.payments_tree: Optional[ttk.Treeview] = None
        self.summary_label: Optional[tk.Label] = None
        self.delete_button: Optional[tk.Button] = None

        self.setup_sales_history_view()

    def has_permission(self, permission: str) -> bool:
        """Verificar si el usuario actual tiene un permiso específico"""
        try:
            return self.permission_service.check_permission(self.user_data, permission)
        except Exception as exc:  # pragma: no cover - defensivo
            print(f"Error verificando permiso {permission}: {exc}")
            return False

    # ------------------------------------------------------------------
    # Construcción de interfaz
    # ------------------------------------------------------------------
    def setup_sales_history_view(self):
        """Configurar estructura completa de la vista"""
        self.root.configure(bg='#f5f6fa')

        self.main_frame = tk.Frame(self.parent, bg='#f5f6fa')
        self.main_frame.pack(fill='both', expand=True)

        self.create_header()
        # El navbar se arma después de registrar callbacks
        self.create_toolbar()
        self.create_content()
        self.create_footer()

    def create_header(self):
        """Crear encabezado principal"""
        header = tk.Frame(self.main_frame, bg='#2c3e50', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)

        content = tk.Frame(header, bg='#2c3e50')
        content.pack(expand=True, fill='both', padx=25, pady=15)

        title = tk.Label(
            content,
            text="📜 Historial de Ventas",
            font=('Segoe UI', 22, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title.pack(side='left')

        user_label = tk.Label(
            content,
            text=f"Usuario: {self.user_data.get('full_name', self.user_data.get('username', 'Desconocido'))}",
            font=('Segoe UI', 12),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        user_label.pack(side='right')

        back_btn = tk.Button(
            content,
            text="⬅️ Regresar",
            font=('Segoe UI', 10, 'bold'),
            bg='#34495e',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8,
            command=lambda: self.trigger_callback('back_to_dashboard')
        )
        back_btn.pack(side='right', padx=20)

    def create_navbar(self, after_widget=None):
        """Crear navbar reutilizable"""
        navbar = tk.Frame(self.main_frame, bg='#2c3e50', height=50)
        if after_widget:
            navbar.pack(fill='x', after=after_widget)
        else:
            navbar.pack(fill='x')
        navbar.pack_propagate(False)

        btn_style = {
            'font': ('Segoe UI', 12, 'bold'),
            'bg': '#2c3e50',
            'fg': 'white',
            'activebackground': '#34495e',
            'activeforeground': 'white',
            'relief': 'flat',
            'bd': 0,
            'padx': 18,
            'pady': 8,
            'cursor': 'hand2'
        }

        container = tk.Frame(navbar, bg='#2c3e50')
        container.pack(side='left', padx=10, pady=5)

        def safe_call(name):
            def wrapper():
                callback = self.callbacks.get(name)
                if callback:
                    callback()
            return wrapper

        file_btn = tk.Menubutton(container, text="📁 Archivo", **btn_style)
        file_btn.pack(side='left', padx=3)
        file_menu = tk.Menu(file_btn, tearoff=0, font=('Segoe UI', 10))
        file_btn.config(menu=file_menu)
        if self.has_permission('sales.create'):
            file_menu.add_command(label="Nueva Venta", command=safe_call('new_sale'))
        file_menu.add_command(label="Regresar al Dashboard", command=safe_call('back_to_dashboard'))

        sales_btn = tk.Menubutton(container, text="💰 Ventas", **btn_style)
        sales_btn.config(bg='#34495e')  # Módulo activo
        sales_btn.pack(side='left', padx=3)
        sales_menu = tk.Menu(sales_btn, tearoff=0, font=('Segoe UI', 10))
        sales_btn.config(menu=sales_menu)
        if self.has_permission('sales.create'):
            sales_menu.add_command(label="Nueva Venta", command=safe_call('new_sale'))
        if self.has_permission('sales.view'):
            sales_menu.add_command(label="Historial de Ventas", command=safe_call('sales_history'))
        if sales_menu.index('end') is None:
            sales_menu.add_command(label="Sin accesos disponibles", state='disabled')

        inv_btn = tk.Menubutton(container, text="📦 Inventario", **btn_style)
        inv_btn.pack(side='left', padx=3)
        inv_menu = tk.Menu(inv_btn, tearoff=0, font=('Segoe UI', 10))
        inv_btn.config(menu=inv_menu)
        inv_menu.add_command(label="Ver Productos", command=safe_call('view_products'))
        inv_menu.add_command(label="Gestionar Categorías", command=safe_call('view_categories'))
        inv_menu.add_command(label="Control de Stock", command=safe_call('stock_control'))

        reports_btn = tk.Menubutton(container, text="📊 Reportes", **btn_style)
        reports_btn.pack(side='left', padx=3)
        reports_menu = tk.Menu(reports_btn, tearoff=0, font=('Segoe UI', 10))
        reports_btn.config(menu=reports_menu)
        reports_menu.add_command(label="Ventas del Día", command=safe_call('daily_report'))
        reports_menu.add_command(label="Reporte Completo", command=safe_call('full_report'))

        admin_btn = tk.Menubutton(container, text="⚙️ Administración", **btn_style)
        admin_btn.pack(side='left', padx=3)
        admin_menu = tk.Menu(admin_btn, tearoff=0, font=('Segoe UI', 10))
        admin_btn.config(menu=admin_menu)
        admin_menu.add_command(label="Gestionar Usuarios", command=safe_call('manage_users'))
        admin_menu.add_command(label="Gestionar Roles", command=safe_call('manage_roles'))
        admin_menu.add_separator()
        admin_menu.add_command(label="Configuración del Sistema", command=safe_call('system_config'))

        help_btn = tk.Menubutton(container, text="❓ Ayuda", **btn_style)
        help_btn.pack(side='left', padx=3)
        help_menu = tk.Menu(help_btn, tearoff=0, font=('Segoe UI', 10))
        help_btn.config(menu=help_menu)
        help_menu.add_command(label="Manual de Usuario", command=safe_call('show_manual'))
        help_menu.add_command(label="Acerca de", command=safe_call('show_about'))

    def create_toolbar(self):
        """Crear barra de filtros y acciones"""
        toolbar = tk.Frame(self.main_frame, bg='white', height=120)
        toolbar.pack(fill='x', padx=25, pady=(20, 0))
        toolbar.pack_propagate(False)

        inner = tk.Frame(toolbar, bg='white')
        inner.pack(fill='both', expand=True, padx=25, pady=15)

        filters_frame = tk.Frame(inner, bg='white')
        filters_frame.pack(side='left', fill='x', expand=True)

        # Primera fila de filtros
        tk.Label(filters_frame, text="Número de venta", font=('Segoe UI', 10, 'bold'), bg='white').grid(row=0, column=0, sticky='w')
        tk.Label(filters_frame, text="Cliente", font=('Segoe UI', 10, 'bold'), bg='white').grid(row=0, column=1, sticky='w', padx=(15, 0))
        tk.Label(filters_frame, text="Cajero", font=('Segoe UI', 10, 'bold'), bg='white').grid(row=0, column=2, sticky='w', padx=(15, 0))

        sale_entry = ttk.Entry(filters_frame, textvariable=self.filter_sale_number, width=20)
        sale_entry.grid(row=1, column=0, sticky='we', pady=5)

        customer_entry = ttk.Entry(filters_frame, textvariable=self.filter_customer, width=25)
        customer_entry.grid(row=1, column=1, sticky='we', padx=(15, 0), pady=5)

        cashier_entry = ttk.Entry(filters_frame, textvariable=self.filter_cashier, width=25)
        cashier_entry.grid(row=1, column=2, sticky='we', padx=(15, 0), pady=5)

        # Segunda fila de filtros
        tk.Label(filters_frame, text="Desde (AAAA-MM-DD)", font=('Segoe UI', 10, 'bold'), bg='white').grid(row=2, column=0, sticky='w', pady=(10, 0))
        tk.Label(filters_frame, text="Hasta (AAAA-MM-DD)", font=('Segoe UI', 10, 'bold'), bg='white').grid(row=2, column=1, sticky='w', padx=(15, 0), pady=(10, 0))
        tk.Label(filters_frame, text="Estado", font=('Segoe UI', 10, 'bold'), bg='white').grid(row=2, column=2, sticky='w', padx=(15, 0), pady=(10, 0))

        date_from_entry = ttk.Entry(filters_frame, textvariable=self.filter_date_from, width=20)
        date_from_entry.grid(row=3, column=0, sticky='we', pady=5)

        date_to_entry = ttk.Entry(filters_frame, textvariable=self.filter_date_to, width=20)
        date_to_entry.grid(row=3, column=1, sticky='we', padx=(15, 0), pady=5)

        status_combo = ttk.Combobox(
            filters_frame,
            textvariable=self.filter_status,
            values=['completed', 'all', 'cancelled'],
            state='readonly',
            width=20
        )
        status_combo.grid(row=3, column=2, sticky='we', padx=(15, 0), pady=5)
        status_combo.set('completed')

        # Botones de acción
        actions = tk.Frame(inner, bg='white')
        actions.pack(side='right', anchor='e')

        refresh_btn = tk.Button(
            actions,
            text="🔄 Actualizar",
            font=('Segoe UI', 10, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8,
            command=self.on_refresh_clicked
        )
        refresh_btn.pack(side='top', pady=5, anchor='e')

        search_btn = tk.Button(
            actions,
            text="🔍 Buscar",
            font=('Segoe UI', 10, 'bold'),
            bg='#1abc9c',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8,
            command=self.on_search_clicked
        )
        search_btn.pack(side='top', pady=5, anchor='e')

        reset_btn = tk.Button(
            actions,
            text="🧼 Limpiar",
            font=('Segoe UI', 10, 'bold'),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8,
            command=self.on_reset_filters
        )
        reset_btn.pack(side='top', pady=5, anchor='e')

        self.delete_button = tk.Button(
            actions,
            text="🗑 Eliminar Venta",
            font=('Segoe UI', 10, 'bold'),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8,
            command=self.on_delete_sale,
            state='disabled'
        )
        self.delete_button.pack(side='top', pady=5, anchor='e')

    def create_content(self):
        """Crear panel principal con listado y detalle"""
        content = tk.Frame(self.main_frame, bg='#f5f6fa')
        content.pack(fill='both', expand=True, padx=25, pady=25)

        list_frame = tk.Frame(content, bg='#f5f6fa')
        list_frame.pack(side='left', fill='both', expand=True)

        columns = (
            'sale_number',
            'sale_date',
            'customer',
            'cashier',
            'total',
            'payment_method',
            'status'
        )

        self.sales_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show='headings',
            height=18
        )

        headings = {
            'sale_number': 'N° Venta',
            'sale_date': 'Fecha',
            'customer': 'Cliente',
            'cashier': 'Cajero',
            'total': 'Total',
            'payment_method': 'Pago',
            'status': 'Estado'
        }

        widths = {
            'sale_number': 120,
            'sale_date': 150,
            'customer': 180,
            'cashier': 160,
            'total': 100,
            'payment_method': 120,
            'status': 110
        }

        for col in columns:
            self.sales_tree.heading(col, text=headings[col])
            self.sales_tree.column(col, width=widths[col], anchor='w')

        vsb = ttk.Scrollbar(list_frame, orient='vertical', command=self.sales_tree.yview)
        hsb = ttk.Scrollbar(list_frame, orient='horizontal', command=self.sales_tree.xview)
        self.sales_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.sales_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        self.sales_tree.bind("<<TreeviewSelect>>", self.on_sale_selected)

        # Panel de detalle
        detail_frame = tk.Frame(content, bg='white', bd=1, relief='solid')
        detail_frame.pack(side='right', fill='y', padx=(20, 0))

        detail_header = tk.Label(
            detail_frame,
            text="Detalle de la venta",
            font=('Segoe UI', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        detail_header.pack(fill='x', padx=15, pady=(15, 5))

        self.detail_text = tk.Text(
            detail_frame,
            height=12,
            width=50,
            font=('Segoe UI', 10),
            state='disabled',
            bg='white',
            relief='flat'
        )
        self.detail_text.pack(fill='both', expand=True, padx=15, pady=(0, 10))

        self.items_tree = ttk.Treeview(
            detail_frame,
            columns=('product', 'quantity', 'unit_price', 'total'),
            show='headings',
            height=6
        )
        self.items_tree.heading('product', text='Producto')
        self.items_tree.heading('quantity', text='Cantidad')
        self.items_tree.heading('unit_price', text='Precio')
        self.items_tree.heading('total', text='Total')
        self.items_tree.column('product', width=180, anchor='w')
        self.items_tree.column('quantity', width=80, anchor='center')
        self.items_tree.column('unit_price', width=90, anchor='e')
        self.items_tree.column('total', width=90, anchor='e')
        self.items_tree.pack(fill='x', padx=15, pady=(0, 10))

        self.payments_tree = ttk.Treeview(
            detail_frame,
            columns=('method', 'amount', 'reference'),
            show='headings',
            height=4
        )
        self.payments_tree.heading('method', text='Método')
        self.payments_tree.heading('amount', text='Monto')
        self.payments_tree.heading('reference', text='Referencia')
        self.payments_tree.column('method', width=120, anchor='w')
        self.payments_tree.column('amount', width=90, anchor='e')
        self.payments_tree.column('reference', width=140, anchor='w')
        self.payments_tree.pack(fill='x', padx=15, pady=(0, 10))

        self.summary_label = tk.Label(
            detail_frame,
            text="Selecciona una venta para ver el detalle",
            font=('Segoe UI', 10, 'italic'),
            bg='white',
            fg='#7f8c8d'
        )
        self.summary_label.pack(fill='x', padx=15, pady=(0, 15))

    def create_footer(self):
        """Crear pie con estadísticas"""
        footer = tk.Frame(self.main_frame, bg='white', height=40)
        footer.pack(fill='x')
        footer.pack_propagate(False)

        self.stats_value = tk.StringVar(value="Ventas listadas: 0 | Total: S/ 0.00")
        stats_label = tk.Label(
            footer,
            textvariable=self.stats_value,
            font=('Segoe UI', 10),
            bg='white',
            fg='#2c3e50'
        )
        stats_label.pack(side='left', padx=25)

    # ------------------------------------------------------------------
    # Gestión de datos
    # ------------------------------------------------------------------
    def load_sales(self, sales: List[Dict[str, Any]]):
        """Cargar listado de ventas"""
        self.sales_data = sales or []
        self.sales_index = {int(sale['id']): sale for sale in self.sales_data if sale.get('id') is not None}

        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)

        total_amount = Decimal('0.00')
        count = 0

        for sale in self.sales_data:
            sale_id = sale.get('id')
            if sale_id is None:
                continue

            sale_date = sale.get('sale_date')
            if isinstance(sale_date, datetime):
                sale_date_str = sale_date.strftime('%Y-%m-%d %H:%M')
            else:
                sale_date_str = str(sale_date) if sale_date else ''

            total = Decimal(str(sale.get('total_amount', 0) or 0))
            total_amount += total
            count += 1

            self.sales_tree.insert(
                '',
                'end',
                iid=str(sale_id),
                values=(
                    sale.get('sale_number', ''),
                    sale_date_str,
                    sale.get('customer_name', 'Cliente'),
                    sale.get('cashier_name', ''),
                    self._format_currency(total),
                    sale.get('payment_method', ''),
                    sale.get('status', '')
                ),
                tags=('cancelled',) if sale.get('status') == 'cancelled' else ('completed',)
            )

        self.sales_tree.tag_configure('cancelled', foreground='#c0392b')
        self.sales_tree.tag_configure('completed', foreground='#2c3e50')

        self.stats_value.set(f"Ventas listadas: {count} | Total: {self._format_currency(total_amount)}")
        self.clear_sale_detail()
        if self.delete_button:
            self.delete_button.config(state='disabled')

    def clear_sale_detail(self):
        """Limpiar panel de detalle"""
        self._set_detail_message("Selecciona una venta para ver el detalle")
        self._clear_tree(self.items_tree)
        self._clear_tree(self.payments_tree)
        self.summary_label.config(text="Selecciona una venta para ver el detalle")

    def show_sale_detail(self, sale: Dict[str, Any]):
        """Mostrar detalle completo de una venta"""
        if not sale:
            self._set_detail_message("No se encontró información de la venta seleccionada")
            return

        header_lines = [
            f"Número: {sale.get('sale_number', '')}",
            f"Fecha: {self._format_datetime(sale.get('sale_date'))}",
            f"Cliente: {sale.get('customer_name', 'Cliente Genérico')} ({sale.get('customer_document', 'N/A')})",
            f"Cajero: {sale.get('cashier_name', '')}",
            f"Estado: {sale.get('status', '').upper()}"
        ]

        notes = sale.get('notes')
        if notes:
            header_lines.append(f"Notas: {notes}")

        self._set_detail_message('\n'.join(header_lines))

        # Items
        self._clear_tree(self.items_tree)
        for item in sale.get('items', []):
            self.items_tree.insert(
                '',
                'end',
                values=(
                    item.get('product_name', ''),
                    f"{item.get('quantity', 0)}",
                    self._format_currency(item.get('unit_price', 0)),
                    self._format_currency(item.get('total', 0)),
                )
            )

        # Pagos
        self._clear_tree(self.payments_tree)
        payments = sale.get('payments') or []
        if payments:
            for payment in payments:
                self.payments_tree.insert(
                    '',
                    'end',
                    values=(
                        payment.get('payment_method', sale.get('payment_method', '')),
                        self._format_currency(payment.get('amount', sale.get('total_amount', 0))),
                        payment.get('transaction_reference', '')
                    )
                )
        else:
            # Pago único (información de la venta)
            self.payments_tree.insert(
                '',
                'end',
                values=(
                    sale.get('payment_method', ''),
                    self._format_currency(sale.get('paid_amount', sale.get('total_amount', 0))),
                    ''
                )
            )

        summary_text = (
            f"Subtotal: {self._format_currency(sale.get('subtotal', 0))}  |  "
            f"Impuestos: {self._format_currency(sale.get('tax_amount', 0))}  |  "
            f"Descuento: {self._format_currency(sale.get('discount_amount', 0))}  |  "
            f"Total: {self._format_currency(sale.get('total_amount', 0))}"
        )
        self.summary_label.config(text=summary_text)

        # Habilitar / deshabilitar eliminación
        status = (sale.get('status') or '').lower()
        if self.delete_button:
            if status == 'completed' and self.has_permission('sales.delete'):
                self.delete_button.config(state='normal')
            else:
                self.delete_button.config(state='disabled')

    # ------------------------------------------------------------------
    # Eventos
    # ------------------------------------------------------------------
    def on_sale_selected(self, _event=None):
        sale_id = self.get_selected_sale_id()
        if sale_id is None:
            return

        self.selected_sale = self.sales_index.get(sale_id)
        self._set_detail_message("Cargando detalle...")
        if self.delete_button:
            self.delete_button.config(state='disabled')
        self.trigger_callback('get_sale_detail', sale_id)

    def on_refresh_clicked(self):
        self.trigger_callback('refresh')

    def on_search_clicked(self):
        filters = self.get_filters()
        self.trigger_callback('apply_filters', filters)

    def on_reset_filters(self):
        self.filter_sale_number.set('')
        self.filter_customer.set('')
        self.filter_cashier.set('')
        self.filter_date_from.set('')
        self.filter_date_to.set('')
        self.filter_status.set('completed')
        self.trigger_callback('reset_filters')

    def on_delete_sale(self):
        sale_id = self.get_selected_sale_id()
        if sale_id is None:
            messagebox.showwarning("Eliminar venta", "Selecciona una venta para eliminar")
            return

        sale = self.sales_index.get(sale_id)
        if not sale:
            messagebox.showerror("Eliminar venta", "No se pudo determinar la venta seleccionada")
            return

        status = (sale.get('status') or '').lower()
        if status != 'completed':
            messagebox.showwarning("Eliminar venta", "Solo se pueden eliminar ventas completadas")
            return

        if not self.has_permission('sales.delete'):
            messagebox.showerror("Permisos", "No tienes permisos para eliminar ventas")
            return

        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Seguro que deseas eliminar esta venta?\n" \
            "Se devolverá el stock de los productos vendidos."
        )
        if not confirm:
            return

        reason = simpledialog.askstring(
            "Motivo",
            "Ingresa el motivo de la eliminación",
            parent=self.root
        )

        self.trigger_callback('delete_sale', sale_id, reason or 'Eliminada desde historial de ventas')

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    def get_filters(self) -> Dict[str, Any]:
        filters: Dict[str, Any] = {}
        if self.filter_sale_number.get().strip():
            filters['sale_number'] = self.filter_sale_number.get().strip()
        if self.filter_customer.get().strip():
            filters['customer_text'] = self.filter_customer.get().strip()
        if self.filter_cashier.get().strip():
            filters['cashier_text'] = self.filter_cashier.get().strip()
        if self.filter_date_from.get().strip():
            filters['date_from'] = self.filter_date_from.get().strip()
        if self.filter_date_to.get().strip():
            filters['date_to'] = self.filter_date_to.get().strip()

        status = self.filter_status.get().strip().lower()
        if status and status != 'all':
            filters['status'] = status

        return filters

    def get_selected_sale_id(self) -> Optional[int]:
        if not self.sales_tree:
            return None
        selection = self.sales_tree.selection()
        if not selection:
            return None
        try:
            return int(selection[0])
        except (ValueError, TypeError):
            return None

    def _set_detail_message(self, message: str):
        if not self.detail_text:
            return
        self.detail_text.config(state='normal')
        self.detail_text.delete('1.0', tk.END)
        self.detail_text.insert(tk.END, message)
        self.detail_text.config(state='disabled')

    def _clear_tree(self, tree: Optional[ttk.Treeview]):
        if not tree:
            return
        for item in tree.get_children():
            tree.delete(item)

    @staticmethod
    def _format_currency(value) -> str:
        try:
            decimal_value = Decimal(str(value))
        except Exception:
            decimal_value = Decimal('0')
        return f"S/ {decimal_value:,.2f}"

    @staticmethod
    def _format_datetime(value) -> str:
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M')
        return str(value) if value else ''

    # ------------------------------------------------------------------
    # Callbacks y navegación
    # ------------------------------------------------------------------
    def bind_callback(self, event_name: str, callback: Callable):
        self.callbacks[event_name] = callback
        if not self.navbar_built and event_name in {
            'back_to_dashboard',
            'new_sale',
            'sales_history',
            'view_products',
            'view_categories'
        }:
            self.main_frame.after(120, self._try_build_navbar)

    def _try_build_navbar(self):
        if not self.navbar_built:
            self.create_navbar(after_widget=self.main_frame.winfo_children()[0])
            self.navbar_built = True
