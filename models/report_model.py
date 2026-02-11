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
            
            # ✅ Query optimizada: usar sub-query para contar items en lugar de JOIN
            query = """
                SELECT 
                    s.id,
                    s.sale_number,
                    s.sale_date,
                    s.subtotal,
                    s.total_amount,
                    s.discount_amount,
                    s.tax_rate,
                    s.include_tax,
                    s.tax_amount,
                    s.payment_method,
                    s.status,
                    u.full_name as cashier_name,
                    COALESCE(c.name, 'CLIENTE GENERAL') as customer_name,
                    (SELECT COUNT(*) FROM sale_items WHERE sale_id = s.id) as items_count
                FROM sales s
                LEFT JOIN users u ON s.user_id = u.id
                LEFT JOIN customers c ON s.customer_id = c.id
                WHERE s.sale_date BETWEEN %s AND %s
                AND s.status = 'completed'
            """
            
            params = [start_date, end_date]
            
            if user_id:
                query += " AND s.user_id = %s"
                params.append(user_id)
            
            query += " ORDER BY s.sale_date DESC"
            
            cursor.execute(query, params)
            sales = cursor.fetchall()
            
            # ✅ Calcular total de productos en una sola query optimizada
            total_products = 0
            if sales:
                product_query = """
                    SELECT SUM(si.quantity) as total_products
                    FROM sale_items si
                    INNER JOIN sales s ON si.sale_id = s.id
                    WHERE s.sale_date BETWEEN %s AND %s
                    AND s.status = 'completed'
                """
                product_params = [start_date, end_date]
                
                if user_id:
                    product_query += " AND s.user_id = %s"
                    product_params.append(user_id)
                
                cursor.execute(product_query, product_params)
                product_result = cursor.fetchone()
                total_products = int(product_result['total_products'] or 0)
            
            # Calcular totales
            total_sales = len(sales)
            total_amount = sum(Decimal(str(s['total_amount'])) for s in sales)
            total_discount = sum(Decimal(str(s['discount_amount'] or 0)) for s in sales)
            # ✅ Solo sumar IGV de ventas que lo incluyen
            total_tax = sum(Decimal(str(s['tax_amount'] or 0)) for s in sales if s.get('include_tax', True))
            
            # ✅ Calcular subtotales separados
            total_with_tax = sum(Decimal(str(s['total_amount'])) for s in sales if s.get('include_tax', True))
            total_without_tax = sum(Decimal(str(s['total_amount'])) for s in sales if not s.get('include_tax', True))
            sales_with_tax_count = sum(1 for s in sales if s.get('include_tax', True))
            sales_without_tax_count = sum(1 for s in sales if not s.get('include_tax', True))
            
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
                        'total_products': total_products,
                        'average_ticket': float(total_amount / total_sales) if total_sales > 0 else 0,
                        # ✅ Información adicional de ventas con/sin IGV
                        'sales_with_tax': sales_with_tax_count,
                        'sales_without_tax': sales_without_tax_count,
                        'total_with_tax': float(total_with_tax),
                        'total_without_tax': float(total_without_tax),
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
                    SUM(si.quantity) as total_quantity,
                    SUM(si.subtotal) as total_sales,
                    COUNT(DISTINCT si.sale_id) as times_sold,
                    AVG(si.unit_price) as avg_price
                FROM sale_items si
                INNER JOIN products p ON si.product_id = p.id
                INNER JOIN sales s ON si.sale_id = s.id
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
                    'sales_summary': sales_report['data']['summary'],
                    'sales': sales_report['data']['sales']  # Incluir lista de ventas
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error en resumen diario: {e}")
            return {'success': False, 'message': str(e)}

    # ==========================
    # Reporte de notas de crédito
    # ==========================
    def get_credit_notes_report(self, start_date: datetime, end_date: datetime, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Reporte de notas de crédito emitidas en el rango"""
        try:
            connection = self.get_connection()
            if not connection:
                return {'success': False, 'message': 'No hay conexión'}

            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT 
                    cn.id,
                    cn.credit_note_number,
                    cn.sale_id,
                    s.sale_number,
                    cn.total_amount,
                    cn.subtotal,
                    cn.tax_amount,
                    cn.status,
                    cn.created_at,
                    cn.issued_by,
                    u.full_name AS issued_by_name,
                    cn.reason
                FROM credit_notes cn
                LEFT JOIN sales s ON cn.sale_id = s.id
                LEFT JOIN users u ON cn.issued_by = u.id
                WHERE cn.created_at BETWEEN %s AND %s
            """
            params = [start_date, end_date]
            if user_id:
                query += " AND cn.issued_by = %s"
                params.append(user_id)

            query += " ORDER BY cn.created_at DESC"
            cursor.execute(query, params)
            notes = cursor.fetchall()

            total_amount = sum(Decimal(str(n['total_amount'] or 0)) for n in notes)
            total_count = len(notes)

            cursor.close()
            connection.close()

            return {
                'success': True,
                'data': {
                    'notes': notes,
                    'summary': {
                        'total_notes': total_count,
                        'total_amount': float(total_amount)
                    },
                    'period': {
                        'start': start_date.strftime('%d/%m/%Y'),
                        'end': end_date.strftime('%d/%m/%Y')
                    }
                }
            }
        except Exception as e:
            self.logger.error(f"Error en reporte de notas de crédito: {e}")
            return {'success': False, 'message': str(e)}

    # ==========================================
    # REPORTES AVANZADOS
    # ==========================================

    def get_product_flow_report(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Reporte de flujo de productos: entradas, salidas y stock actual por producto"""
        try:
            connection = self.get_connection()
            if not connection:
                return {'success': False, 'message': 'No hay conexión a la base de datos'}

            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT 
                    p.id,
                    p.sku,
                    p.name,
                    p.stock_quantity,
                    p.cost,
                    p.price,
                    c.name as category_name,
                    COALESCE(SUM(CASE WHEN im.quantity > 0 THEN im.quantity ELSE 0 END), 0) as total_entradas,
                    COALESCE(SUM(CASE WHEN im.quantity < 0 THEN ABS(im.quantity) ELSE 0 END), 0) as total_salidas,
                    COUNT(im.id) as total_movimientos
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                LEFT JOIN inventory_movements im ON p.id = im.product_id
                    AND im.created_at BETWEEN %s AND %s
                WHERE p.status = 'active'
                GROUP BY p.id
                ORDER BY total_movimientos DESC, p.name ASC
            """

            cursor.execute(query, [start_date, end_date])
            products = cursor.fetchall()

            # Totales
            total_entradas = sum(int(p['total_entradas'] or 0) for p in products)
            total_salidas = sum(int(p['total_salidas'] or 0) for p in products)
            productos_con_movimiento = sum(1 for p in products if int(p['total_movimientos'] or 0) > 0)

            cursor.close()

            return {
                'success': True,
                'data': {
                    'products': products,
                    'summary': {
                        'total_products': len(products),
                        'products_with_movement': productos_con_movimiento,
                        'total_entradas': total_entradas,
                        'total_salidas': total_salidas,
                        'balance': total_entradas - total_salidas
                    },
                    'period': {
                        'start': start_date.strftime('%d/%m/%Y'),
                        'end': end_date.strftime('%d/%m/%Y')
                    }
                }
            }

        except Exception as e:
            self.logger.error(f"Error en reporte de flujo de productos: {e}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'message': str(e)}

    def get_monthly_sales_report(self, year: int) -> Dict[str, Any]:
        """Reporte mensual de ventas agrupado por mes para un año dado"""
        try:
            connection = self.get_connection()
            if not connection:
                return {'success': False, 'message': 'No hay conexión a la base de datos'}

            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT 
                    MONTH(s.sale_date) as mes,
                    COUNT(s.id) as total_ventas,
                    COALESCE(SUM(s.total_amount), 0) as monto_total,
                    COALESCE(AVG(s.total_amount), 0) as ticket_promedio,
                    COALESCE(SUM(s.discount_amount), 0) as total_descuentos,
                    COALESCE(SUM(s.tax_amount), 0) as total_impuestos,
                    COALESCE(SUM(
                        (SELECT SUM(si.quantity) FROM sale_items si WHERE si.sale_id = s.id)
                    ), 0) as total_productos
                FROM sales s
                WHERE YEAR(s.sale_date) = %s
                AND s.status = 'completed'
                GROUP BY MONTH(s.sale_date)
                ORDER BY mes ASC
            """

            cursor.execute(query, [year])
            monthly_data = cursor.fetchall()

            # Crear diccionario con los 12 meses
            meses_nombres = [
                'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
            ]

            months = {}
            for i in range(1, 13):
                months[i] = {
                    'mes': i,
                    'nombre': meses_nombres[i - 1],
                    'total_ventas': 0,
                    'monto_total': 0,
                    'ticket_promedio': 0,
                    'total_descuentos': 0,
                    'total_impuestos': 0,
                    'total_productos': 0
                }

            for row in monthly_data:
                m = int(row['mes'])
                months[m] = {
                    'mes': m,
                    'nombre': meses_nombres[m - 1],
                    'total_ventas': int(row['total_ventas']),
                    'monto_total': float(row['monto_total']),
                    'ticket_promedio': float(row['ticket_promedio']),
                    'total_descuentos': float(row['total_descuentos']),
                    'total_impuestos': float(row['total_impuestos']),
                    'total_productos': int(row['total_productos'] or 0)
                }

            months_list = list(months.values())

            # Totales anuales
            total_ventas_anual = sum(m['total_ventas'] for m in months_list)
            monto_total_anual = sum(m['monto_total'] for m in months_list)
            ticket_promedio_anual = monto_total_anual / total_ventas_anual if total_ventas_anual > 0 else 0

            # Mejor y peor mes
            meses_con_ventas = [m for m in months_list if m['total_ventas'] > 0]
            mejor_mes = max(meses_con_ventas, key=lambda x: x['monto_total'])['nombre'] if meses_con_ventas else 'N/A'
            peor_mes = min(meses_con_ventas, key=lambda x: x['monto_total'])['nombre'] if meses_con_ventas else 'N/A'

            cursor.close()

            return {
                'success': True,
                'data': {
                    'months': months_list,
                    'year': year,
                    'summary': {
                        'total_ventas': total_ventas_anual,
                        'monto_total': monto_total_anual,
                        'ticket_promedio': round(ticket_promedio_anual, 2),
                        'mejor_mes': mejor_mes,
                        'peor_mes': peor_mes
                    }
                }
            }

        except Exception as e:
            self.logger.error(f"Error en reporte mensual: {e}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'message': str(e)}

    def get_inventory_investment_report(self) -> Dict[str, Any]:
        """Reporte de inversión en inventario: stock × costo y stock × precio de venta"""
        try:
            connection = self.get_connection()
            if not connection:
                return {'success': False, 'message': 'No hay conexión a la base de datos'}

            cursor = connection.cursor(dictionary=True)

            # Productos con valor de inversión
            query_products = """
                SELECT 
                    p.id,
                    p.sku,
                    p.name,
                    p.stock_quantity,
                    p.cost,
                    p.price,
                    c.name as category_name,
                    (p.stock_quantity * p.cost) as inversion_costo,
                    (p.stock_quantity * p.price) as valor_venta,
                    CASE 
                        WHEN p.cost > 0 THEN ROUND(((p.price - p.cost) / p.cost) * 100, 2)
                        ELSE 0
                    END as margen_pct
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.status = 'active'
                ORDER BY inversion_costo DESC
            """

            cursor.execute(query_products)
            products = cursor.fetchall()

            # Totales por categoría
            query_categories = """
                SELECT 
                    COALESCE(c.name, 'Sin Categoría') as category_name,
                    COUNT(p.id) as total_productos,
                    SUM(p.stock_quantity) as total_unidades,
                    SUM(p.stock_quantity * p.cost) as inversion_costo,
                    SUM(p.stock_quantity * p.price) as valor_venta
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.status = 'active'
                GROUP BY c.id
                ORDER BY inversion_costo DESC
            """

            cursor.execute(query_categories)
            categories = cursor.fetchall()

            # Totales generales
            total_inversion_costo = sum(Decimal(str(p['inversion_costo'] or 0)) for p in products)
            total_valor_venta = sum(Decimal(str(p['valor_venta'] or 0)) for p in products)
            total_unidades = sum(int(p['stock_quantity'] or 0) for p in products)
            ganancia_potencial = total_valor_venta - total_inversion_costo
            margen_global = float((ganancia_potencial / total_inversion_costo) * 100) if total_inversion_costo > 0 else 0

            cursor.close()

            return {
                'success': True,
                'data': {
                    'products': products,
                    'categories': categories,
                    'summary': {
                        'total_products': len(products),
                        'total_unidades': total_unidades,
                        'total_inversion_costo': float(total_inversion_costo),
                        'total_valor_venta': float(total_valor_venta),
                        'ganancia_potencial': float(ganancia_potencial),
                        'margen_global': round(margen_global, 2)
                    }
                }
            }

        except Exception as e:
            self.logger.error(f"Error en reporte de inversión: {e}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'message': str(e)}

    def get_specific_product_report(self, product_id: int, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Reporte de rendimiento de un producto específico en un período"""
        try:
            connection = self.get_connection()
            if not connection:
                return {'success': False, 'message': 'No hay conexión a la base de datos'}

            cursor = connection.cursor(dictionary=True)

            # Info del producto
            cursor.execute("""
                SELECT p.id, p.sku, p.name, p.cost, p.price, p.stock_quantity,
                       c.name as category_name
                FROM products p 
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.id = %s
            """, [product_id])
            product_info = cursor.fetchone()

            if not product_info:
                return {'success': False, 'message': 'Producto no encontrado'}

            # Detalle de ventas del producto
            query_sales = """
                SELECT 
                    s.sale_number,
                    s.sale_date,
                    si.quantity,
                    si.unit_price,
                    si.subtotal,
                    si.discount_amount,
                    u.full_name as cashier_name,
                    COALESCE(cu.name, 'CLIENTE GENERAL') as customer_name
                FROM sale_items si
                INNER JOIN sales s ON si.sale_id = s.id
                LEFT JOIN users u ON s.user_id = u.id
                LEFT JOIN customers cu ON s.customer_id = cu.id
                WHERE si.product_id = %s
                AND s.sale_date BETWEEN %s AND %s
                AND s.status = 'completed'
                ORDER BY s.sale_date DESC
            """

            cursor.execute(query_sales, [product_id, start_date, end_date])
            sales = cursor.fetchall()

            # Totales
            total_unidades = sum(int(s['quantity'] or 0) for s in sales)
            total_ingresos = sum(Decimal(str(s['subtotal'] or 0)) for s in sales)
            total_descuentos = sum(Decimal(str(s['discount_amount'] or 0)) for s in sales)
            veces_vendido = len(sales)
            precio_promedio = float(total_ingresos / total_unidades) if total_unidades > 0 else 0

            # Costo total vendido  
            costo_unitario = Decimal(str(product_info['cost'] or 0))
            costo_total_vendido = costo_unitario * total_unidades
            ganancia = float(total_ingresos - costo_total_vendido)

            # Movimientos de inventario del producto
            query_movements = """
                SELECT 
                    im.movement_type,
                    im.quantity,
                    im.previous_stock,
                    im.new_stock,
                    im.created_at,
                    im.notes
                FROM inventory_movements im
                WHERE im.product_id = %s
                AND im.created_at BETWEEN %s AND %s
                ORDER BY im.created_at DESC
                LIMIT 50
            """

            cursor.execute(query_movements, [product_id, start_date, end_date])
            movements = cursor.fetchall()

            cursor.close()

            return {
                'success': True,
                'data': {
                    'product': product_info,
                    'sales': sales,
                    'movements': movements,
                    'summary': {
                        'total_unidades_vendidas': total_unidades,
                        'total_ingresos': float(total_ingresos),
                        'total_descuentos': float(total_descuentos),
                        'veces_vendido': veces_vendido,
                        'precio_promedio': round(precio_promedio, 2),
                        'costo_total_vendido': float(costo_total_vendido),
                        'ganancia': ganancia,
                        'stock_actual': int(product_info['stock_quantity'] or 0)
                    },
                    'period': {
                        'start': start_date.strftime('%d/%m/%Y'),
                        'end': end_date.strftime('%d/%m/%Y')
                    }
                }
            }

        except Exception as e:
            self.logger.error(f"Error en reporte de producto específico: {e}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'message': str(e)}

    def get_all_products_list(self) -> List[Dict[str, Any]]:
        """Obtener lista simple de productos activos para selectores"""
        try:
            connection = self.get_connection()
            if not connection:
                return []

            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT id, sku, name 
                FROM products 
                WHERE status = 'active' 
                ORDER BY name ASC
            """)
            products = cursor.fetchall()
            cursor.close()
            return products

        except Exception as e:
            self.logger.error(f"Error al obtener lista de productos: {e}")
            return []
