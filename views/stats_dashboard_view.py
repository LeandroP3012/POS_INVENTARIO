"""
Vista del Dashboard con Estadísticas - Métricas en Tiempo Real
Panel de control con KPIs y gráficos del negocio
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, List
from datetime import datetime, timedelta
import random


class StatsDashboardView:
    """Dashboard con estadísticas y métricas del negocio"""
    
    def __init__(self, parent_frame: tk.Frame, user_data: Dict[str, Any] = None):
        self.parent_frame = parent_frame
        self.user_data = user_data or {}
        self.setup_dashboard()
    
    def setup_dashboard(self):
        """Configurar dashboard de estadísticas"""
        self.create_header()
        self.create_kpi_cards()
        self.create_charts_section()
        self.create_recent_activity()
    
    def create_header(self):
        """Crear header con resumen del día"""
        header_frame = tk.Frame(self.parent_frame, bg='#f8f9fa')
        header_frame.pack(fill='x', padx=20, pady=(20, 0))
        
        # Título principal
        title_label = tk.Label(
            header_frame,
            text="📊 Dashboard de Ventas",
            font=('Segoe UI', 24, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        )
        title_label.pack(pady=(0, 10))
        
        # Fecha actual
        today = datetime.now().strftime("%d de %B de %Y")
        date_label = tk.Label(
            header_frame,
            text=f"Resumen del día: {today}",
            font=('Segoe UI', 14),
            fg='#7f8c8d',
            bg='#f8f9fa'
        )
        date_label.pack()
    
    def create_kpi_cards(self):
        """Crear tarjetas de KPIs principales"""
        kpis_frame = tk.Frame(self.parent_frame, bg='#f8f9fa')
        kpis_frame.pack(fill='x', padx=20, pady=20)
        
        # Datos de ejemplo (en una implementación real vendrían de la BD)
        kpis = [
            {
                'title': 'Ventas de Hoy',
                'value': '$1,247.50',
                'change': '+12.5%',
                'change_positive': True,
                'icon': '💰',
                'color': '#27ae60'
            },
            {
                'title': 'Productos Vendidos',
                'value': '48',
                'change': '+8 productos',
                'change_positive': True,
                'icon': '📦',
                'color': '#3498db'
            },
            {
                'title': 'Transacciones',
                'value': '23',
                'change': '+5 vs ayer',
                'change_positive': True,
                'icon': '🧾',
                'color': '#9b59b6'
            },
            {
                'title': 'Ticket Promedio',
                'value': '$54.24',
                'change': '-2.1%',
                'change_positive': False,
                'icon': '💳',
                'color': '#e74c3c'
            }
        ]
        
        # Crear grid de KPIs
        for i, kpi in enumerate(kpis):
            self.create_kpi_card(kpis_frame, kpi, i)
    
    def create_kpi_card(self, parent, kpi_data, index):
        """Crear una tarjeta KPI individual"""
        card_frame = tk.Frame(
            parent,
            bg='white',
            relief='solid',
            bd=1,
            padx=20,
            pady=15
        )
        card_frame.grid(row=0, column=index, padx=10, sticky='ew')
        
        # Configurar weight para distribución equitativa
        parent.grid_columnconfigure(index, weight=1)
        
        # Icono y título
        header_frame = tk.Frame(card_frame, bg='white')
        header_frame.pack(fill='x')
        
        icon_label = tk.Label(
            header_frame,
            text=kpi_data['icon'],
            font=('Segoe UI', 20),
            bg='white'
        )
        icon_label.pack(side='left')
        
        title_label = tk.Label(
            header_frame,
            text=kpi_data['title'],
            font=('Segoe UI', 12),
            fg='#7f8c8d',
            bg='white'
        )
        title_label.pack(side='right')
        
        # Valor principal
        value_label = tk.Label(
            card_frame,
            text=kpi_data['value'],
            font=('Segoe UI', 24, 'bold'),
            fg=kpi_data['color'],
            bg='white'
        )
        value_label.pack(pady=(10, 5))
        
        # Cambio/tendencia
        change_color = '#27ae60' if kpi_data['change_positive'] else '#e74c3c'
        change_icon = '↗️' if kpi_data['change_positive'] else '↘️'
        
        change_label = tk.Label(
            card_frame,
            text=f"{change_icon} {kpi_data['change']}",
            font=('Segoe UI', 11),
            fg=change_color,
            bg='white'
        )
        change_label.pack()
        
        # Efecto hover
        self.setup_kpi_hover(card_frame)
    
    def setup_kpi_hover(self, card_frame):
        """Configurar efectos hover para KPIs"""
        def on_enter(event):
            card_frame.configure(bg='#f8f9fa', relief='solid', bd=2)
        
        def on_leave(event):
            card_frame.configure(bg='white', relief='solid', bd=1)
        
        card_frame.bind('<Enter>', on_enter)
        card_frame.bind('<Leave>', on_leave)
    
    def create_charts_section(self):
        """Crear sección de gráficos"""
        charts_frame = tk.Frame(self.parent_frame, bg='#f8f9fa')
        charts_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Dividir en dos columnas
        left_chart = tk.Frame(charts_frame, bg='white', relief='solid', bd=1)
        left_chart.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        right_chart = tk.Frame(charts_frame, bg='white', relief='solid', bd=1)
        right_chart.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Gráfico de ventas por hora (izquierda)
        self.create_sales_by_hour_chart(left_chart)
        
        # Top productos (derecha)
        self.create_top_products_chart(right_chart)
    
    def create_sales_by_hour_chart(self, parent):
        """Crear gráfico de ventas por hora (simulado)"""
        # Título
        title_label = tk.Label(
            parent,
            text="📈 Ventas por Hora",
            font=('Segoe UI', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        title_label.pack(pady=20)
        
        # Canvas para el gráfico (simulado con barras ASCII)
        chart_frame = tk.Frame(parent, bg='white')
        chart_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Datos simulados de ventas por hora
        hours_data = [
            ('09:00', 45), ('10:00', 78), ('11:00', 123), ('12:00', 189),
            ('13:00', 156), ('14:00', 134), ('15:00', 167), ('16:00', 198),
            ('17:00', 145), ('18:00', 89), ('19:00', 67), ('20:00', 34)
        ]
        
        max_value = max(data[1] for data in hours_data)
        
        for hour, value in hours_data:
            row_frame = tk.Frame(chart_frame, bg='white')
            row_frame.pack(fill='x', pady=2)
            
            # Hora
            hour_label = tk.Label(
                row_frame,
                text=hour,
                font=('Segoe UI', 10),
                fg='#7f8c8d',
                bg='white',
                width=6
            )
            hour_label.pack(side='left')
            
            # Barra de progreso simulada
            bar_width = int((value / max_value) * 200)
            bar_color = '#3498db' if value > max_value * 0.7 else '#95a5a6'
            
            bar_frame = tk.Frame(row_frame, bg=bar_color, height=20, width=bar_width)
            bar_frame.pack(side='left', padx=5)
            bar_frame.pack_propagate(False)
            
            # Valor
            value_label = tk.Label(
                row_frame,
                text=f"${value}",
                font=('Segoe UI', 10, 'bold'),
                fg='#2c3e50',
                bg='white'
            )
            value_label.pack(side='left', padx=10)
    
    def create_top_products_chart(self, parent):
        """Crear lista de productos más vendidos"""
        # Título
        title_label = tk.Label(
            parent,
            text="🏆 Top Productos Hoy",
            font=('Segoe UI', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        title_label.pack(pady=20)
        
        # Lista de productos
        products_frame = tk.Frame(parent, bg='white')
        products_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Datos simulados
        top_products = [
            {'name': 'Café Americano', 'qty': 12, 'revenue': 148.50, 'color': '#f39c12'},
            {'name': 'Sandwich Mixto', 'qty': 8, 'revenue': 124.00, 'color': '#e74c3c'},
            {'name': 'Jugo Natural', 'qty': 15, 'revenue': 97.50, 'color': '#27ae60'},
            {'name': 'Empanada', 'qty': 6, 'revenue': 78.00, 'color': '#9b59b6'},
            {'name': 'Té Helado', 'qty': 9, 'revenue': 63.75, 'color': '#3498db'}
        ]
        
        for i, product in enumerate(top_products):
            product_frame = tk.Frame(products_frame, bg='white')
            product_frame.pack(fill='x', pady=5)
            
            # Posición
            pos_label = tk.Label(
                product_frame,
                text=f"#{i+1}",
                font=('Segoe UI', 12, 'bold'),
                fg=product['color'],
                bg='white',
                width=3
            )
            pos_label.pack(side='left')
            
            # Nombre del producto
            name_label = tk.Label(
                product_frame,
                text=product['name'],
                font=('Segoe UI', 11),
                fg='#2c3e50',
                bg='white'
            )
            name_label.pack(side='left', padx=10)
            
            # Información a la derecha
            info_frame = tk.Frame(product_frame, bg='white')
            info_frame.pack(side='right')
            
            qty_label = tk.Label(
                info_frame,
                text=f"{product['qty']} uds",
                font=('Segoe UI', 10),
                fg='#7f8c8d',
                bg='white'
            )
            qty_label.pack(side='top', anchor='e')
            
            revenue_label = tk.Label(
                info_frame,
                text=f"${product['revenue']:.2f}",
                font=('Segoe UI', 11, 'bold'),
                fg=product['color'],
                bg='white'
            )
            revenue_label.pack(side='top', anchor='e')
    
    def create_recent_activity(self):
        """Crear sección de actividad reciente"""
        activity_frame = tk.Frame(self.parent_frame, bg='white', relief='solid', bd=1)
        activity_frame.pack(fill='x', padx=20, pady=(10, 20))
        
        # Título
        title_label = tk.Label(
            activity_frame,
            text="🔔 Actividad Reciente",
            font=('Segoe UI', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        title_label.pack(pady=15)
        
        # Lista de actividades
        activities_frame = tk.Frame(activity_frame, bg='white')
        activities_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        # Actividades simuladas
        activities = [
            {'time': '14:32', 'action': 'Venta completada', 'detail': 'Factura #1234 - $67.50', 'icon': '✅'},
            {'time': '14:28', 'action': 'Producto agregado', 'detail': 'Café Espresso - Stock: 25', 'icon': '📦'},
            {'time': '14:15', 'action': 'Usuario conectado', 'detail': 'Cajero María González', 'icon': '👤'},
            {'time': '13:45', 'action': 'Backup realizado', 'detail': 'Base de datos respaldada', 'icon': '💾'}
        ]
        
        for activity in activities:
            activity_row = tk.Frame(activities_frame, bg='white')
            activity_row.pack(fill='x', pady=3)
            
            # Hora
            time_label = tk.Label(
                activity_row,
                text=activity['time'],
                font=('Segoe UI', 10),
                fg='#7f8c8d',
                bg='white',
                width=6
            )
            time_label.pack(side='left')
            
            # Icono
            icon_label = tk.Label(
                activity_row,
                text=activity['icon'],
                font=('Segoe UI', 12),
                bg='white'
            )
            icon_label.pack(side='left', padx=5)
            
            # Acción y detalle
            text_frame = tk.Frame(activity_row, bg='white')
            text_frame.pack(side='left', fill='x', expand=True, padx=10)
            
            action_label = tk.Label(
                text_frame,
                text=activity['action'],
                font=('Segoe UI', 11, 'bold'),
                fg='#2c3e50',
                bg='white'
            )
            action_label.pack(anchor='w')
            
            detail_label = tk.Label(
                text_frame,
                text=activity['detail'],
                font=('Segoe UI', 10),
                fg='#7f8c8d',
                bg='white'
            )
            detail_label.pack(anchor='w')
    
    def update_dashboard_data(self):
        """Actualizar datos del dashboard (llamar periódicamente)"""
        # TODO: Conectar con base de datos real
        pass
    
    def refresh_kpis(self):
        """Refrescar KPIs con datos actuales"""
        # TODO: Obtener datos actuales de ventas
        pass
