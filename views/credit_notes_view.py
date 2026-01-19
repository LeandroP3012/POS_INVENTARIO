"""Vista para gestión de notas de crédito"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, List, Optional
from datetime import datetime

from views.base_view import BaseView


class CreditNotesView(BaseView):
    """Listado y operaciones básicas de notas de crédito"""

    def __init__(self, parent, user_data: Optional[Dict[str, Any]] = None):
        self.parent = parent
        self.user_data = user_data or {}
        self.notes: List[Dict[str, Any]] = []
        self.summary_var: Optional[tk.StringVar] = None
        self.sale_selector_window: Optional[tk.Toplevel] = None
        self.sale_selector_tree: Optional[ttk.Treeview] = None
        self.sale_selector_data: List[Dict[str, Any]] = []
        self.sale_search_var: Optional[tk.StringVar] = None
        self.sale_reason_text: Optional[tk.Text] = None
        super().__init__(parent)
        self.summary_var = tk.StringVar(value="Sin notas de crédito registradas")
        self._build_view()

    # ------------------------------------------------------------------
    # Construcción de la vista
    # ------------------------------------------------------------------
    def _build_view(self):
        self.root.configure(bg=self.colors['background'])
        self.main_frame = tk.Frame(self.parent, bg=self.colors['background'])
        self.main_frame.pack(fill='both', expand=True)

        self._create_header()
        self._create_toolbar()
        self._create_table()
        self._create_footer()

    def _create_header(self):
        header = tk.Frame(self.main_frame, bg='#2c3e50', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)

        content = tk.Frame(header, bg='#2c3e50')
        content.pack(expand=True, fill='both', padx=25, pady=15)

        tk.Label(
            content,
            text="🧾 Notas de Crédito",
            font=('Segoe UI', 22, 'bold'),
            fg='white',
            bg='#2c3e50'
        ).pack(side='left')

        right = tk.Frame(content, bg='#2c3e50')
        right.pack(side='right')

        tk.Label(
            right,
            text=f"Usuario: {self.user_data.get('full_name', self.user_data.get('username', 'Desconocido'))}",
            font=('Segoe UI', 11),
            fg='#bdc3c7',
            bg='#2c3e50'
        ).pack(side='right')

        tk.Button(
            right,
            text="⬅️ Regresar",
            font=('Segoe UI', 10, 'bold'),
            bg='#34495e',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=18,
            pady=8,
            command=lambda: self.trigger_callback('back_to_dashboard')
        ).pack(side='right', padx=(0, 15))

    def _create_toolbar(self):
        toolbar = tk.Frame(self.main_frame, bg='white', height=90)
        toolbar.pack(fill='x', padx=25, pady=(20, 0))
        toolbar.pack_propagate(False)

        btn_frame = tk.Frame(toolbar, bg='white')
        btn_frame.pack(side='left', padx=15)

        actions = [
            ("🔄 Refrescar", '#3498db', self.on_refresh_clicked),
            ("➕ Generar desde venta", '#27ae60', self.on_generate_clicked),
            ("📄 Reporte 30 días", '#8e44ad', self.on_report_clicked)
        ]

        for text, color, cmd in actions:
            tk.Button(
                btn_frame,
                text=text,
                font=('Segoe UI', 10, 'bold'),
                bg=color,
                fg='white',
                relief='flat',
                cursor='hand2',
                padx=20,
                pady=10,
                command=cmd
            ).pack(side='left', padx=8)

        self.summary_label = tk.Label(
            toolbar,
            textvariable=self.summary_var,
            font=('Segoe UI', 11, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        self.summary_label.pack(side='right', padx=20)

    def _create_table(self):
        content = tk.Frame(self.main_frame, bg=self.colors['background'])
        content.pack(fill='both', expand=True, padx=25, pady=20)

        columns = ('credit_note_number', 'sale_number', 'total_amount', 'status', 'created_at', 'issued_by_name', 'reason')
        self.notes_tree = ttk.Treeview(content, columns=columns, show='headings', height=20)

        headings = {
            'credit_note_number': 'Nota',
            'sale_number': 'Venta',
            'total_amount': 'Total',
            'status': 'Estado',
            'created_at': 'Fecha',
            'issued_by_name': 'Emitido por',
            'reason': 'Motivo'
        }

        widths = {
            'credit_note_number': 140,
            'sale_number': 120,
            'total_amount': 110,
            'status': 110,
            'created_at': 160,
            'issued_by_name': 180,
            'reason': 260
        }

        for col in columns:
            self.notes_tree.heading(col, text=headings[col])
            anchor = 'center' if col in {'total_amount', 'status', 'created_at'} else 'w'
            self.notes_tree.column(col, width=widths[col], anchor=anchor)

        vsb = ttk.Scrollbar(content, orient='vertical', command=self.notes_tree.yview)
        self.notes_tree.configure(yscrollcommand=vsb.set)

        self.notes_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')

        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)

    def _create_footer(self):
        footer = tk.Frame(self.main_frame, bg='#ecf0f1', height=50)
        footer.pack(fill='x', side='bottom')
        footer.pack_propagate(False)

        tk.Label(
            footer,
            text="Las notas de crédito revierten inventario y excluyen la venta de reportes.",
            font=('Segoe UI', 10),
            fg='#2c3e50',
            bg='#ecf0f1'
        ).pack(side='left', padx=20)

    # ------------------------------------------------------------------
    # Eventos
    # ------------------------------------------------------------------
    def on_refresh_clicked(self):
        self.trigger_callback('refresh')

    def on_generate_clicked(self):
        self._open_sale_selector_dialog()

    def on_report_clicked(self):
        self.trigger_callback('show_credit_note_report')

    # ------------------------------------------------------------------
    # Selección de venta
    # ------------------------------------------------------------------
    def _open_sale_selector_dialog(self):
        if self.sale_selector_window and self.sale_selector_window.winfo_exists():
            self.sale_selector_window.lift()
            return

        self.sale_selector_window = tk.Toplevel(self.root)
        self.sale_selector_window.title("Seleccionar venta a acreditar")
        self.sale_selector_window.configure(bg=self.colors['background'])
        dialog_width = 820
        dialog_height = 540
        self.sale_selector_window.geometry(f"{dialog_width}x{dialog_height}")
        self._center_window(self.sale_selector_window, dialog_width, dialog_height)
        self.sale_selector_window.transient(self.root)
        self.sale_selector_window.grab_set()
        self.sale_selector_window.protocol("WM_DELETE_WINDOW", self._close_sale_selector_dialog)

        header = tk.Frame(self.sale_selector_window, bg='#34495e', height=70)
        header.pack(fill='x')
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Selecciona una venta para generar la nota",
            font=('Segoe UI', 16, 'bold'),
            fg='white',
            bg='#34495e'
        ).pack(side='left', padx=25)

        content = tk.Frame(self.sale_selector_window, bg=self.colors['background'])
        content.pack(fill='both', expand=True, padx=25, pady=20)

        # Búsqueda
        search_frame = tk.Frame(content, bg=self.colors['background'])
        search_frame.pack(fill='x', pady=(0, 12))

        tk.Label(
            search_frame,
            text="Buscar (número, cliente, documento o cajero):",
            font=('Segoe UI', 11),
            bg=self.colors['background'],
            fg=self.colors['on_background']
        ).pack(side='left')

        self.sale_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.sale_search_var, width=30)
        search_entry.pack(side='left', padx=10)
        # Bind Enter to read the entry text explicitly to avoid empty StringVar edge cases
        search_entry.bind('<Return>', lambda _event: self._on_search_click(search_entry.get()))

        ttk.Button(
            search_frame,
            text="Buscar",
            command=lambda: self._on_search_click(search_entry.get())
        ).pack(side='left')

        ttk.Button(
            search_frame,
            text="Limpiar",
            command=self._reset_sale_selector_search
        ).pack(side='left', padx=6)

        # Tabla de ventas
        table_frame = tk.Frame(content, bg=self.colors['background'])
        table_frame.pack(fill='both', expand=True)

        columns = ('sale_number', 'customer', 'total', 'status', 'sale_date', 'cashier')
        self.sale_selector_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)

        headings = {
            'sale_number': 'Venta',
            'customer': 'Cliente',
            'total': 'Total',
            'status': 'Estado',
            'sale_date': 'Fecha',
            'cashier': 'Cajero'
        }

        widths = {
            'sale_number': 110,
            'customer': 150,
            'total': 90,
            'status': 90,
            'sale_date': 145,
            'cashier': 140
        }

        for col in columns:
            self.sale_selector_tree.heading(col, text=headings[col])
            anchor = 'center' if col in {'total', 'status', 'sale_date'} else 'w'
            self.sale_selector_tree.column(col, width=widths[col], anchor=anchor)

        vsb = ttk.Scrollbar(table_frame, orient='vertical', command=self.sale_selector_tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient='horizontal', command=self.sale_selector_tree.xview)
        self.sale_selector_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.sale_selector_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.sale_selector_tree.bind('<Double-1>', lambda _event: self._on_sale_selector_confirm())

        # Motivo y acciones
        footer = tk.Frame(content, bg='white', relief='groove', bd=1)
        footer.pack(fill='x', pady=(12, 0))

        reason_frame = tk.Frame(footer, bg='white')
        reason_frame.pack(fill='both', expand=True, padx=12, pady=(10, 8))

        tk.Label(
            reason_frame,
            text="Motivo de la nota:",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w')

        self.sale_reason_text = tk.Text(reason_frame, height=2, font=('Segoe UI', 10))
        self.sale_reason_text.pack(fill='x', pady=(8, 5))
        self.sale_reason_text.insert('1.0', 'Devolución / cancelación')

        info_label = tk.Label(
            reason_frame,
            text="La venta seleccionada será acreditada y su stock restaurado.",
            font=('Segoe UI', 9),
            bg='white',
            fg='#7f8c8d'
        )
        info_label.pack(anchor='w')

        actions = tk.Frame(footer, bg='white')
        actions.pack(fill='x', pady=(8, 0))

        tk.Button(
            actions,
            text="Cancelar",
            command=self._close_sale_selector_dialog,
            bg='#bdc3c7',
            fg='white',
            font=('Segoe UI', 9, 'bold'),
            padx=14,
            pady=6,
            relief='flat'
        ).pack(side='right', padx=8)

        tk.Button(
            actions,
            text="Generar Nota",
            command=self._on_sale_selector_confirm,
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', 9, 'bold'),
            padx=16,
            pady=6,
            relief='flat'
        ).pack(side='right')

        self._refresh_sale_selector_list()

    def _close_sale_selector_dialog(self):
        if self.sale_selector_window and self.sale_selector_window.winfo_exists():
            self.sale_selector_window.destroy()

        self.sale_selector_window = None
        self.sale_selector_tree = None
        self.sale_reason_text = None
        self.sale_search_var = None
        self.sale_selector_data = []

    def _center_window(self, window, width, height):
        """Centrar ventana secundaria según la resolución actual"""
        try:
            screen_w = window.winfo_screenwidth()
            screen_h = window.winfo_screenheight()
        except Exception:
            screen_w, screen_h = 1366, 768

        x = max((screen_w - width) // 2, 0)
        y = max((screen_h - height) // 2, 0)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def _reset_sale_selector_search(self):
        if self.sale_search_var:
            self.sale_search_var.set('')
        self._refresh_sale_selector_list(search_term="")

    def _on_search_click(self, term_from_event: Optional[str] = None):
        """Ejecuta la búsqueda cuando se hace clic en el botón o se presiona Enter"""
        raw = term_from_event if term_from_event is not None else (self.sale_search_var.get() if self.sale_search_var else '')
        search_term = raw.strip()
        print(f"🔍 [DEBUG VISTA] _on_search_click - Término capturado: '{search_term}' (raw='{raw}')")
        self._refresh_sale_selector_list(search_term)

    def _refresh_sale_selector_list(self, search_term: Optional[str] = None):
        if not self.sale_selector_tree:
            print("⚠️ [DEBUG VISTA] sale_selector_tree no existe")
            return

        print(f"🔍 [DEBUG VISTA] search_term recibido: '{search_term}' (tipo: {type(search_term).__name__})")
        term = search_term if search_term is not None else (self.sale_search_var.get().strip() if self.sale_search_var else "")
        print(f"🔍 [DEBUG VISTA] term final: '{term}' (longitud: {len(term)})")
        print(f"🔍 [DEBUG VISTA] Llamando trigger_callback con event='fetch_credit_note_sales', term='{term}'")
        result = self.trigger_callback('fetch_credit_note_sales', term)
        print(f"🔍 [DEBUG VISTA] Callback retornó: {result}")
        print(f"🔍 [DEBUG VISTA] Resultado del callback: success={result.get('success') if result else None}, ventas={len(result.get('sales', [])) if result else 0}")

        if not result or not result.get('success'):
            message = (result or {}).get('message', 'No se pudo obtener el listado de ventas')
            self.show_error("Ventas", message)
            return

        self.sale_selector_data = result.get('sales', [])

        # El backend ya aplica el filtro, usamos directamente los datos devueltos
        filtered_sales = self.sale_selector_data

        for item in self.sale_selector_tree.get_children():
            self.sale_selector_tree.delete(item)

        if not filtered_sales:
            return

        for sale in filtered_sales:
            sale_id = sale.get('id')
            sale_number = sale.get('sale_number') or f"Venta #{sale_id}"
            customer = sale.get('customer_name') or 'Cliente Genérico'
            total = float(sale.get('total_amount') or 0)
            status = (sale.get('status') or '').capitalize()
            cashier = sale.get('cashier_name') or sale.get('cashier_username') or 'Cajero'

            sale_date = sale.get('sale_date')
            if isinstance(sale_date, datetime):
                date_text = sale_date.strftime('%Y-%m-%d %H:%M')
            else:
                date_text = str(sale_date)

            iid = f"sale-{sale_id}"
            self.sale_selector_tree.insert(
                '',
                'end',
                iid=iid,
                values=(
                    sale_number,
                    customer[:40],
                    f"S/ {total:.2f}",
                    status or '-',
                    date_text,
                    cashier[:30]
                )
            )

    def _on_sale_selector_confirm(self):
        if not self.sale_selector_tree:
            return

        selection = self.sale_selector_tree.selection()
        if not selection:
            self.show_warning("Generar nota", "Selecciona una venta para continuar.")
            return

        sale_id = int(str(selection[0]).replace('sale-', ''))
        sale = next((item for item in self.sale_selector_data if item.get('id') == sale_id), None)
        if not sale:
            self.show_error("Generar nota", "No se pudo identificar la venta seleccionada.")
            return

        reason = self.sale_reason_text.get('1.0', tk.END).strip() if self.sale_reason_text else ''
        if not reason:
            self.show_warning("Motivo requerido", "Ingresa el motivo de la nota de crédito.")
            return

        self._close_sale_selector_dialog()
        self.trigger_callback('generate_credit_note', sale_id, reason)

    # ------------------------------------------------------------------
    # Datos
    # ------------------------------------------------------------------
    def load_notes(self, notes: Optional[List[Dict[str, Any]]] = None):
        self.notes = notes or []
        for row in self.notes_tree.get_children():
            self.notes_tree.delete(row)

        total_amount = 0.0
        for note in self.notes:
            total_amount += float(note.get('total_amount') or 0)
            created = note.get('created_at')
            if isinstance(created, datetime):
                created_txt = created.strftime('%Y-%m-%d %H:%M')
            else:
                created_txt = str(created)

            self.notes_tree.insert('', 'end', values=(
                note.get('credit_note_number'),
                note.get('sale_number'),
                f"{float(note.get('total_amount') or 0):.2f}",
                note.get('status'),
                created_txt,
                note.get('issued_by_name') or '-',
                (note.get('reason') or '')[:80]
            ))

        count = len(self.notes)
        self.summary_var.set(f"Notas: {count} • Monto total acreditado: S/ {total_amount:.2f}")

    def show_report_summary(self, summary: Dict[str, Any]):
        total_notes = summary.get('total_notes', 0)
        total_amount = summary.get('total_amount', 0.0)
        self.show_success(
            "Reporte de notas",
            f"Total de notas: {total_notes}\nMonto total acreditado: S/ {total_amount:.2f}"
        )
