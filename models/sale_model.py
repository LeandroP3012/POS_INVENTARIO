"""
Modelo para gestión de ventas (POS)
Autor: Sistema POS
Fecha: 2025
"""

from models.base_model import BaseModel
from datetime import datetime
from decimal import Decimal

class SaleModel(BaseModel):
    """Modelo para operaciones de ventas"""
    
    def __init__(self):
        super().__init__()
        self.table_name = "sales"
    
    # ==========================================
    # OPERACIONES DE VENTA
    # ==========================================
    
    def create_sale(self, sale_data, items, payments=None):
        """
        Crea una nueva venta con sus items y pagos
        
        Args:
            sale_data: dict con datos de la venta principal
            items: list de dict con los productos vendidos
            payments: list de dict con métodos de pago (opcional)
        
        Returns:
            int: ID de la venta creada o None si falla
        """
        connection = None
        cursor = None
        
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # Iniciar transacción
            connection.start_transaction()
            
            # 1. Generar número de venta
            sale_number = self._generate_sale_number(cursor)
            sale_data['sale_number'] = sale_number
            
            # 2. Insertar venta principal
            sale_query = """
                INSERT INTO sales (
                    sale_number, user_id, customer_id, 
                    subtotal, tax_rate, tax_amount, 
                    discount_amount, total_amount,
                    payment_method, paid_amount, change_amount,
                    status, notes
                ) VALUES (
                    %(sale_number)s, %(user_id)s, %(customer_id)s,
                    %(subtotal)s, %(tax_rate)s, %(tax_amount)s,
                    %(discount_amount)s, %(total_amount)s,
                    %(payment_method)s, %(paid_amount)s, %(change_amount)s,
                    %(status)s, %(notes)s
                )
            """
            cursor.execute(sale_query, sale_data)
            sale_id = cursor.lastrowid
            
            # 3. Insertar items de venta
            for item in items:
                item['sale_id'] = sale_id
                self._insert_sale_item(cursor, item)
                
                # 4. Actualizar stock del producto
                self._update_product_stock(cursor, item['product_id'], -item['quantity'])
                
                # 5. Registrar movimiento de inventario
                self._create_inventory_movement(cursor, {
                    'product_id': item['product_id'],
                    'movement_type': 'sale',
                    'quantity': -item['quantity'],
                    'reference_type': 'sale',
                    'reference_id': sale_id,
                    'user_id': sale_data['user_id'],
                    'notes': f"Venta {sale_number}"
                })
            
            # 6. Insertar pagos (si hay múltiples métodos)
            if payments:
                for payment in payments:
                    payment['sale_id'] = sale_id
                    self._insert_sale_payment(cursor, payment)
            
            # Confirmar transacción
            connection.commit()
            
            print(f"✅ Venta {sale_number} creada exitosamente (ID: {sale_id})")
            return sale_id
            
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error al crear venta: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def _generate_sale_number(self, cursor):
        """Genera número único de venta (VTA-2025-00001)"""
        year = datetime.now().year
        
        query = """
            SELECT sale_number 
            FROM sales 
            WHERE sale_number LIKE %s 
            ORDER BY id DESC 
            LIMIT 1
        """
        cursor.execute(query, (f"VTA-{year}-%",))
        result = cursor.fetchone()
        
        if result:
            last_number = int(result[0].split('-')[-1])
            new_number = last_number + 1
        else:
            new_number = 1
        
        return f"VTA-{year}-{new_number:05d}"
    
    def _insert_sale_item(self, cursor, item):
        """Inserta un item de venta"""
        query = """
            INSERT INTO sale_items (
                sale_id, product_id, product_sku, product_name,
                quantity, unit_price, discount_percent, discount_amount,
                subtotal, tax_rate, tax_amount, total
            ) VALUES (
                %(sale_id)s, %(product_id)s, %(product_sku)s, %(product_name)s,
                %(quantity)s, %(unit_price)s, %(discount_percent)s, %(discount_amount)s,
                %(subtotal)s, %(tax_rate)s, %(tax_amount)s, %(total)s
            )
        """
        cursor.execute(query, item)
    
    def _insert_sale_payment(self, cursor, payment):
        """Inserta un pago de venta"""
        query = """
            INSERT INTO sale_payments (
                sale_id, payment_method, amount,
                card_type, card_last_digits, transaction_reference, bank_name
            ) VALUES (
                %(sale_id)s, %(payment_method)s, %(amount)s,
                %(card_type)s, %(card_last_digits)s, %(transaction_reference)s, %(bank_name)s
            )
        """
        cursor.execute(query, payment)
    
    def _update_product_stock(self, cursor, product_id, quantity_change):
        """Actualiza el stock de un producto"""
        query = """
            UPDATE products 
            SET stock_quantity = stock_quantity + %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        cursor.execute(query, (quantity_change, product_id))
    
    def _create_inventory_movement(self, cursor, movement):
        """Registra un movimiento de inventario"""
        from decimal import Decimal
        
        # Obtener stock actual
        cursor.execute("SELECT stock_quantity FROM products WHERE id = %s", (movement['product_id'],))
        result = cursor.fetchone()
        current_stock = result[0] if result else Decimal('0')
        
        # Convertir quantity a Decimal para evitar errores de tipo
        quantity = Decimal(str(movement['quantity']))
        
        movement['previous_stock'] = current_stock
        movement['new_stock'] = current_stock + quantity
        
        query = """
            INSERT INTO inventory_movements (
                product_id, movement_type, quantity,
                previous_stock, new_stock,
                reference_type, reference_id,
                user_id, notes
            ) VALUES (
                %(product_id)s, %(movement_type)s, %(quantity)s,
                %(previous_stock)s, %(new_stock)s,
                %(reference_type)s, %(reference_id)s,
                %(user_id)s, %(notes)s
            )
        """
        cursor.execute(query, movement)
    
    # ==========================================
    # CONSULTAS DE VENTAS
    # ==========================================
    
    def get_all_sales(self, filters=None):
        """Obtiene todas las ventas con filtros opcionales"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    s.*,
                    u.username as cashier_username,
                    u.full_name as cashier_name,
                    COALESCE(c.name, 'Cliente Genérico') as customer_name,
                    COALESCE(c.document_number, '00000000') as customer_document
                FROM sales s
                INNER JOIN users u ON s.user_id = u.id
                LEFT JOIN customers c ON s.customer_id = c.id
                WHERE 1=1
            """
            params = []
            
            if filters:
                if filters.get('status'):
                    query += " AND s.status = %s"
                    params.append(filters['status'])
                
                if filters.get('date_from'):
                    query += " AND DATE(s.sale_date) >= %s"
                    params.append(filters['date_from'])
                
                if filters.get('date_to'):
                    query += " AND DATE(s.sale_date) <= %s"
                    params.append(filters['date_to'])
                
                if filters.get('cashier_id'):
                    query += " AND s.user_id = %s"
                    params.append(filters['cashier_id'])
            
            query += " ORDER BY s.sale_date DESC"
            
            cursor.execute(query, params)
            sales = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            return sales
            
        except Exception as e:
            print(f"❌ Error al obtener ventas: {e}")
            return []
    
    def get_sale_by_id(self, sale_id):
        """Obtiene una venta específica con todos sus detalles"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            # Obtener venta principal
            query = """
                SELECT 
                    s.*,
                    u.username as cashier_username,
                    u.full_name as cashier_name,
                    COALESCE(c.name, 'Cliente Genérico') as customer_name,
                    COALESCE(c.document_number, '00000000') as customer_document,
                    COALESCE(c.address, '') as customer_address
                FROM sales s
                INNER JOIN users u ON s.user_id = u.id
                LEFT JOIN customers c ON s.customer_id = c.id
                WHERE s.id = %s
            """
            cursor.execute(query, (sale_id,))
            sale = cursor.fetchone()
            
            if sale:
                # Obtener items
                query_items = """
                    SELECT * FROM sale_items 
                    WHERE sale_id = %s
                    ORDER BY id
                """
                cursor.execute(query_items, (sale_id,))
                sale['items'] = cursor.fetchall()
                
                # Obtener pagos
                query_payments = """
                    SELECT * FROM sale_payments
                    WHERE sale_id = %s
                """
                cursor.execute(query_payments, (sale_id,))
                sale['payments'] = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            return sale
            
        except Exception as e:
            print(f"❌ Error al obtener venta {sale_id}: {e}")
            return None
    
    def cancel_sale(self, sale_id, user_id, reason):
        """Cancela una venta y revierte el inventario"""
        connection = None
        cursor = None
        
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            connection.start_transaction()
            
            # Verificar que la venta existe y está completada
            cursor.execute(
                "SELECT * FROM sales WHERE id = %s AND status = 'completed'",
                (sale_id,)
            )
            sale = cursor.fetchone()
            
            if not sale:
                print("❌ Venta no encontrada o ya está cancelada")
                return False
            
            # Obtener items de la venta
            cursor.execute("SELECT * FROM sale_items WHERE sale_id = %s", (sale_id,))
            items = cursor.fetchall()
            
            # Revertir stock de cada producto
            for item in items:
                self._update_product_stock(cursor, item['product_id'], item['quantity'])
                
                # Registrar movimiento de devolución
                self._create_inventory_movement(cursor, {
                    'product_id': item['product_id'],
                    'movement_type': 'return',
                    'quantity': item['quantity'],
                    'reference_type': 'sale',
                    'reference_id': sale_id,
                    'user_id': user_id,
                    'notes': f"Cancelación de venta {sale['sale_number']}"
                })
            
            # Actualizar estado de la venta
            update_query = """
                UPDATE sales 
                SET status = 'cancelled',
                    cancelled_at = CURRENT_TIMESTAMP,
                    cancelled_by = %s,
                    cancellation_reason = %s
                WHERE id = %s
            """
            cursor.execute(update_query, (user_id, reason, sale_id))
            
            connection.commit()
            
            print(f"✅ Venta {sale['sale_number']} cancelada exitosamente")
            return True
            
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"❌ Error al cancelar venta: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    # ==========================================
    # REPORTES Y ESTADÍSTICAS
    # ==========================================
    
    def get_daily_sales_summary(self, date=None):
        """Obtiene resumen de ventas del día"""
        if not date:
            date = datetime.now().date()
        
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    COUNT(*) as total_sales,
                    SUM(total_amount) as total_amount,
                    SUM(CASE WHEN payment_method = 'cash' THEN total_amount ELSE 0 END) as cash_amount,
                    SUM(CASE WHEN payment_method = 'card' THEN total_amount ELSE 0 END) as card_amount,
                    SUM(CASE WHEN payment_method = 'transfer' THEN total_amount ELSE 0 END) as transfer_amount
                FROM sales
                WHERE DATE(sale_date) = %s
                AND status = 'completed'
            """
            cursor.execute(query, (date,))
            summary = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            return summary
            
        except Exception as e:
            print(f"❌ Error al obtener resumen de ventas: {e}")
            return None
