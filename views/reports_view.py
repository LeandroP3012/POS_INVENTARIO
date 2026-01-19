"""
Vista de Reportes
Autor: Sistema POS
Fecha: 2025-10-27
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class ReportsView:
    """Vista para módulo de reportes"""
    
    def __init__(self, parent, controller, user_data, on_back=None):
        self.parent = parent
        self.controller = controller
        self.user_data = user_data
        self.on_back = on_back
        
        # Frame principal
        self.main_frame = tk.Frame(parent, bg='#ecf0f1')
        self.main_frame.pack(fill='both', expand=True)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interfaz"""
        # Header
        self.create_header()
        
        # Contenedor principal
        content = tk.Frame(self.main_frame, bg='#ecf0f1')
        content.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Panel izquierdo: Opciones de reportes
        left_panel = tk.Frame(content, bg='white', relief='solid', borderwidth=1, width=300)
        left_panel.pack(side='left', fill='y', padx=(0, 5))
        left_panel.pack_propagate(False)
        self.create_report_options(left_panel)
        
        # Panel derecho: Visualización
        self.right_panel = tk.Frame(content, bg='white', relief='solid', borderwidth=1)
        self.right_panel.pack(side='left', fill='both', expand=True, padx=(5, 0))
        self.create_welcome_screen()
    
    def create_header(self):
        """Crear header"""
        header = tk.Frame(self.main_frame, bg='#8e44ad', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📊 REPORTES Y ANÁLISIS",
            font=('Segoe UI', 20, 'bold'),
            bg='#8e44ad',
            fg='white'
        ).pack(side='left', padx=20, pady=10)
        
        # Info del usuario
        user_info = tk.Frame(header, bg='#8e44ad')
        user_info.pack(side='right', padx=20, pady=10)
        
        tk.Label(
            user_info,
            text=f"👤 Usuario: {self.user_data.get('full_name', 'Usuario')}",
            font=('Segoe UI', 10),
            bg='#8e44ad',
            fg='white'
        ).pack()
        
        tk.Label(
            user_info,
            text=f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            font=('Segoe UI', 9),
            bg='#8e44ad',
            fg='#ecf0f1'
        ).pack()
        
        # Botón volver
        if self.on_back:
            tk.Button(
                header,
                text="⬅️ Volver",
                command=self.on_back,
                font=('Segoe UI', 10),
                bg='#9b59b6',
                fg='white',
                relief='flat',
                padx=15,
                pady=5,
                cursor='hand2'
            ).pack(side='right', padx=10)
    
    def create_report_options(self, parent):
        """Crear opciones de reportes"""
        tk.Label(
            parent,
            text="TIPOS DE REPORTES",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=15)
        
        # Opciones de reportes
        reports = [
            {
                'name': '📈 Reporte de Ventas',
                'icon': '📈',
                'command': self.show_sales_report,
                'desc': 'Ventas por período'
            },
            {
                'name': '🛍️ Productos Vendidos',
                'icon': '🛍️',
                'command': self.show_products_report,
                'desc': 'Top productos vendidos'
            },
            {
                'name': '📦 Estado de Inventario',
                'icon': '📦',
                'command': self.show_inventory_report,
                'desc': 'Stock actual'
            },
            {
                'name': '👥 Reporte por Cajero',
                'icon': '👥',
                'command': self.show_cashier_report,
                'desc': 'Ventas por cajero'
            },
            {
                'name': '📅 Resumen Diario',
                'icon': '📅',
                'command': self.show_daily_summary,
                'desc': 'Cierre del día'
            },
            {
                'name': '🔄 Comparar Períodos',
                'icon': '🔄',
                'command': self.show_period_comparison,
                'desc': 'Comparar ventas'
            }
        ]
        
        for report in reports:
            frame = tk.Frame(parent, bg='white')
            frame.pack(fill='x', padx=10, pady=5)
            
            btn = tk.Button(
                frame,
                text=f"{report['icon']} {report['name'].replace(report['icon'] + ' ', '')}",
                command=report['command'],
                font=('Segoe UI', 11, 'bold'),
                bg='#8e44ad',
                fg='white',
                relief='flat',
                padx=15,
                pady=10,
                cursor='hand2',
                anchor='w'
            )
            btn.pack(fill='x')
            
            # Hover effect
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#9b59b6'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#8e44ad'))
            
            tk.Label(
                frame,
                text=report['desc'],
                font=('Segoe UI', 8),
                bg='white',
                fg='#7f8c8d'
            ).pack(anchor='w', padx=5)
    
    def create_welcome_screen(self):
        """Pantalla de bienvenida"""
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        welcome = tk.Frame(self.right_panel, bg='white')
        welcome.pack(expand=True)
        
        tk.Label(
            welcome,
            text="📊",
            font=('Segoe UI', 72),
            bg='white'
        ).pack(pady=20)
        
        tk.Label(
            welcome,
            text="Módulo de Reportes",
            font=('Segoe UI', 24, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack()
        
        tk.Label(
            welcome,
            text="Selecciona un tipo de reporte del menú lateral",
            font=('Segoe UI', 12),
            bg='white',
            fg='#7f8c8d'
        ).pack(pady=10)
    
    def show_sales_report(self):
        """Mostrar reporte de ventas"""
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        # Header del reporte
        header = tk.Frame(self.right_panel, bg='#3498db', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📈 REPORTE DE VENTAS",
            font=('Segoe UI', 16, 'bold'),
            bg='#3498db',
            fg='white'
        ).pack(side='left', padx=20, pady=15)
        
        # Filtros
        filters = tk.Frame(self.right_panel, bg='white')
        filters.pack(fill='x', padx=20, pady=15)
        
        # Fechas
        date_frame = tk.Frame(filters, bg='white')
        date_frame.pack(fill='x', pady=5)
        
        tk.Label(
            date_frame,
            text="Desde:",
            font=('Segoe UI', 10),
            bg='white'
        ).pack(side='left', padx=5)
        
        self.sales_start_date = DateEntry(
            date_frame,
            width=12,
            background='#3498db',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/mm/yyyy'
        )
        self.sales_start_date.pack(side='left', padx=5)
        
        tk.Label(
            date_frame,
            text="Hasta:",
            font=('Segoe UI', 10),
            bg='white'
        ).pack(side='left', padx=5)
        
        self.sales_end_date = DateEntry(
            date_frame,
            width=12,
            background='#3498db',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/mm/yyyy'
        )
        self.sales_end_date.pack(side='left', padx=5)
        
        # Botón generar
        tk.Button(
            date_frame,
            text="🔍 Generar Reporte",
            command=self.generate_sales_report,
            font=('Segoe UI', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2'
        ).pack(side='left', padx=10)
        
        # Área de resultados
        self.sales_results = tk.Frame(self.right_panel, bg='white')
        self.sales_results.pack(fill='both', expand=True, padx=20, pady=10)
    
    def generate_sales_report(self):
        """Generar reporte de ventas"""
        try:
            start = self.sales_start_date.get_date().strftime('%Y-%m-%d')
            end = self.sales_end_date.get_date().strftime('%Y-%m-%d')
            
            result = self.controller.get_sales_report(start, end)
            
            if not result['success']:
                messagebox.showerror("Error", result['message'])
                return
            
            # Limpiar resultados anteriores
            for widget in self.sales_results.winfo_children():
                widget.destroy()
            
            data = result['data']
            summary = data['summary']
            
            # Resumen en cards
            cards_frame = tk.Frame(self.sales_results, bg='white')
            cards_frame.pack(fill='x', pady=10)
            
            cards = [
                ('Total Ventas', summary['total_sales'], '🛒', '#3498db'),
                ('Monto Total', f"S/ {summary['total_amount']:.2f}", '💰', '#27ae60'),
                ('Ticket Promedio', f"S/ {summary['average_ticket']:.2f}", '🎫', '#f39c12'),
                ('Descuentos', f"S/ {summary['total_discount']:.2f}", '🏷️', '#e74c3c')
            ]
            
            for title, value, icon, color in cards:
                self.create_summary_card(cards_frame, title, value, icon, color)
            
            # Tabla de ventas
            table_frame = tk.Frame(self.sales_results, bg='white')
            table_frame.pack(fill='both', expand=True, pady=10)
            
            tk.Label(
                table_frame,
                text="Detalle de Ventas",
                font=('Segoe UI', 12, 'bold'),
                bg='white',
                fg='#2c3e50'
            ).pack(anchor='w', pady=5)
            
            # Scrollbar
            scroll = tk.Scrollbar(table_frame)
            scroll.pack(side='right', fill='y')
            
            # Treeview
            columns = ('Número', 'Fecha', 'Cajero', 'Cliente', 'Total', 'Método Pago')
            tree = ttk.Treeview(table_frame, columns=columns, show='headings', 
                               height=10, yscrollcommand=scroll.set)
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            
            # Llenar datos
            for sale in data['sales']:
                tree.insert('', 'end', values=(
                    sale['sale_number'],
                    sale['sale_date'].strftime('%d/%m/%Y %H:%M') if isinstance(sale['sale_date'], datetime) else sale['sale_date'],
                    sale['cashier_name'] or 'N/A',
                    sale['customer_name'] or 'Cliente Genérico',
                    f"S/ {sale['total_amount']:.2f}",
                    sale['payment_method'].upper()
                ))
            
            tree.pack(fill='both', expand=True)
            scroll.config(command=tree.yview)
            
            # Botón exportar
            tk.Button(
                self.sales_results,
                text="📄 Exportar a PDF",
                command=lambda: self.export_to_pdf('ventas', data),
                font=('Segoe UI', 10),
                bg='#e74c3c',
                fg='white',
                relief='flat',
                padx=15,
                pady=8,
                cursor='hand2'
            ).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def create_summary_card(self, parent, title, value, icon, color):
        """Crear tarjeta de resumen"""
        card = tk.Frame(parent, bg=color, relief='raised', borderwidth=2)
        card.pack(side='left', fill='both', expand=True, padx=5)
        
        tk.Label(
            card,
            text=icon,
            font=('Segoe UI', 24),
            bg=color,
            fg='white'
        ).pack(pady=5)
        
        tk.Label(
            card,
            text=str(value),
            font=('Segoe UI', 16, 'bold'),
            bg=color,
            fg='white'
        ).pack()
        
        tk.Label(
            card,
            text=title,
            font=('Segoe UI', 9),
            bg=color,
            fg='white'
        ).pack(pady=5)
    
    def show_products_report(self):
        """Mostrar reporte de productos vendidos"""
        messagebox.showinfo("En desarrollo", "Reporte de productos en desarrollo")
    
    def show_inventory_report(self):
        """Mostrar reporte de inventario"""
        messagebox.showinfo("En desarrollo", "Reporte de inventario en desarrollo")
    
    def show_cashier_report(self):
        """Mostrar reporte por cajero"""
        messagebox.showinfo("En desarrollo", "Reporte por cajero en desarrollo")
    
    def show_daily_summary(self):
        """Mostrar resumen diario"""
        messagebox.showinfo("En desarrollo", "Resumen diario en desarrollo")
    
    def show_period_comparison(self):
        """Mostrar comparación de períodos"""
        messagebox.showinfo("En desarrollo", "Comparación de períodos en desarrollo")
    
    def export_to_pdf(self, report_type, data):
        """Exportar reporte a PDF"""
        messagebox.showinfo("Exportar", "Funcionalidad de exportación en desarrollo")
    
    def show(self):
        """Mostrar vista"""
        self.main_frame.pack(fill='both', expand=True)
    
    def hide(self):
        """Ocultar vista"""
        self.main_frame.pack_forget()
    
    def destroy(self):
        """Destruir vista"""
        self.main_frame.destroy()
