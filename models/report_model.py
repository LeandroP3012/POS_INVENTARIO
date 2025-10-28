"""
Modelo de Reportes
Autor: Sistema POS
Fecha: 2025-10-27
"""

from models.base_model import BaseModel
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from decimal import Decimal

class ReportModel(BaseModel):
    """Modelo para generar reportes del sistema"""
    
    def __init__(self):
        super().__init__()
        self.table_name = 'sales'  # Tabla principal
    
    # ==========================================
    # REPORTES DE VENTAS
    # ==========================================
    
    def get_sales_report(self, start_date: datetime, end_date: datetime, 
                        user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Reporte de ventas por rango de fechas
        
        Args:
            start_date: Fecha inicial
            end_date: Fecha final
            user_id: ID del usuario (opcional, para filtrar por cajero)
        
        Returns:
            Dict con datos del reporte
        """
        try:
            connection = self.get_connection()
            if not connection:
                return {'success': False, 'message': 'No hay conexión a la base de datos'}
            
            cursor = connection.cursor(dictionary=True)
            
            # Query base
            query = """
                SELECT 
                    s.id,
                    s.sale_number,
                    s.sale_date,
                    s.total_amount,
                    s.discount_amount,
                    s.tax_amount,
                    s.payment_method,
                    s.status,
                    u.full_name as cashier_name,
                    c.name as customer_name,
                    COUNT(sd.id) as items_count
                FROM sales s
                LEFT JOIN users u ON s.user_id = u.id
                LEFT JOIN customers c ON s.customer_id = c.id
                LEFT JOIN sale_details sd ON s.id = sd.sale_id
                WHERE s.sale_date BETWEEN %s AND %s
            """
            
            params = [start_date, end_date]
            
            if user_id:
                query += " AND s.user_id = %s"
                params.append(user_id)
            
            query += " GROUP BY s.id ORDER BY s.sale_date DESC"
            
            cursor.execute(query, params)
            sales = cursor.fetchall()
            
            # Calcular totales
            total_sales = len(sales)
            total_amount = sum(Decimal(str(s['total_amount'])) for s in sales)
            total_discount = sum(Decimal(str(s['discount_amount'] or 0)) for s in sales)
            total_tax = sum(Decimal(str(s['tax_amount'] or 0)) for s in sales)
            
            # Ventas por método de pago
            payment_methods = {}
            for sale in sales:
                method = sale['payment_method']
                if method not in payment_methods:
                    payment_methods[method] = {'count': 0, 'amount': Decimal('0')}
                payment_methods[method]['count'] += 1
                payment_methods[method]['amount'] += Decimal(str(sale['total_amount']))
            
            cursor.close()
            
            return {
                'success': True,
                'data': {
                    'sales': sales,
                    'summary': {
                        'total_sales': total_sales,
                        'total_amount': float(total_amount),
                        'total_discount': float(total_discount),
                        'total_tax': float(total_tax),
                        'average_ticket': float(total_amount / total_sales) if total_sales > 0 else 0,
                        'payment_methods': {
                            k: {'count': v['count'], 'amount': float(v['amount'])}
                            for k, v in payment_methods.items()
                        }
                    },
                    'period': {
                        'start': start_date.strftime('%d/%m/%Y'),
                        'end': end_date.strftime('%d/%m/%Y')
                    }
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error en reporte de ventas: {e}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'message': str(e)}
    
    def get_products_sold_report(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Reporte de productos vendidos"""
        try:
            connection = self.get_connection()
            if not connection:
                return {'success': False, 'message': 'No hay conexión'}
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    p.id,
                    p.sku,
                    p.name,
                    p.price,
                    SUM(sd.quantity) as total_quantity,
                    SUM(sd.subtotal) as total_sales,
                    COUNT(DISTINCT sd.sale_id) as times_sold,
                    AVG(sd.unit_price) as avg_price
                FROM sale_details sd
                INNER JOIN products p ON sd.product_id = p.id
                INNER JOIN sales s ON sd.sale_id = s.id
                WHERE s.sale_date BETWEEN %s AND %s
                AND s.status = 'completed'
                GROUP BY p.id
                ORDER BY total_sales DESC
            """
            
            cursor.execute(query, [start_date, end_date])
            products = cursor.fetchall()
            
            total_quantity = sum(int(p['total_quantity']) for p in products)
            total_sales = sum(Decimal(str(p['total_sales'])) for p in products)
            
            cursor.close()
            
            return {
                'success': True,
                'data': {
                    'products': products,
                    'summary': {
                        'total_products': len(products),
                        'total_quantity': total_quantity,
                        'total_sales': float(total_sales)
                    }
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error en reporte de productos: {e}")
            return {'success': False, 'message': str(e)}
    
    def get_inventory_report(self) -> Dict[str, Any]:
        """Reporte de inventario actual"""
        try:
            connection = self.get_connection()
            if not connection:
                return {'success': False, 'message': 'No hay conexión'}
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    p.id,
                    p.sku,
                    p.name,
                    p.stock_quantity,
                    p.min_stock,
                    p.max_stock,
                    p.cost,
                    p.price,
                    c.name as category_name,
                    p.status,
                    (p.stock_quantity * p.cost) as stock_value,
                    CASE 
                        WHEN p.stock_quantity <= 0 THEN 'Sin Stock'
                        WHEN p.stock_quantity <= p.min_stock THEN 'Stock Bajo'
                        WHEN p.stock_quantity >= p.max_stock THEN 'Sobrestock'
                        ELSE 'Normal'
                    END as stock_status
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.status = 'active'
                ORDER BY stock_status DESC, p.name ASC
            """
            
            cursor.execute(query)
            products = cursor.fetchall()
            
            # Calcular totales
            total_value = sum(Decimal(str(p['stock_value'] or 0)) for p in products)
            low_stock = sum(1 for p in products if p['stock_status'] == 'Stock Bajo')
            out_stock = sum(1 for p in products if p['stock_status'] == 'Sin Stock')
            overstock = sum(1 for p in products if p['stock_status'] == 'Sobrestock')
            
            cursor.close()
            
            return {
                'success': True,
                'data': {
                    'products': products,
                    'summary': {
                        'total_products': len(products),
                        'total_value': float(total_value),
                        'low_stock': low_stock,
                        'out_stock': out_stock,
                        'overstock': overstock
                    }
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error en reporte de inventario: {e}")
            return {'success': False, 'message': str(e)}
    
    def get_cashier_report(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Reporte por cajero"""
        try:
            connection = self.get_connection()
            if not connection:
                return {'success': False, 'message': 'No hay conexión'}
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    u.id as user_id,
                    u.full_name as cashier_name,
                    COUNT(s.id) as total_sales,
                    SUM(s.total_amount) as total_amount,
                    AVG(s.total_amount) as avg_ticket,
                    MIN(s.sale_date) as first_sale,
                    MAX(s.sale_date) as last_sale
                FROM users u
                LEFT JOIN sales s ON u.id = s.user_id 
                    AND s.sale_date BETWEEN %s AND %s
                    AND s.status = 'completed'
                GROUP BY u.id
                HAVING total_sales > 0
                ORDER BY total_amount DESC
            """
            
            cursor.execute(query, [start_date, end_date])
            cashiers = cursor.fetchall()
            
            cursor.close()
            
            return {
                'success': True,
                'data': {
                    'cashiers': cashiers,
                    'summary': {
                        'total_cashiers': len(cashiers),
                        'total_sales': sum(int(c['total_sales']) for c in cashiers),
                        'total_amount': sum(float(c['total_amount'] or 0) for c in cashiers)
                    }
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error en reporte de cajeros: {e}")
            return {'success': False, 'message': str(e)}
    
    def get_daily_summary(self, date: datetime) -> Dict[str, Any]:
        """Resumen del día"""
        try:
            start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = date.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            # Obtener reporte de ventas del día
            sales_report = self.get_sales_report(start_date, end_date)
            
            if not sales_report['success']:
                return sales_report
            
            return {
                'success': True,
                'data': {
                    'date': date.strftime('%d/%m/%Y'),
                    'sales_summary': sales_report['data']['summary']
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error en resumen diario: {e}")
            return {'success': False, 'message': str(e)}
