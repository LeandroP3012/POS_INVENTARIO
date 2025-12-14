"""Modelo para gestión de notas de crédito"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any

from models.base_model import BaseModel


class CreditNoteModel(BaseModel):
    """Operaciones sobre notas de crédito"""

    def __init__(self):
        super().__init__()
        self.table_name = "credit_notes"

    # ==========================
    # Creación de notas
    # ==========================
    def create_credit_note(self, sale_id: int, user_id: int, reason: str = "", items: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            connection.start_transaction()

            # 1) Validar venta
            cursor.execute("SELECT * FROM sales WHERE id = %s FOR UPDATE", (sale_id,))
            sale = cursor.fetchone()
            if not sale:
                return {'success': False, 'message': 'La venta no existe.'}

            status = (sale.get('status') or '').lower()
            if status not in {'completed', 'refunded'}:
                return {'success': False, 'message': f"La venta no es elegible para nota de crédito (estado: {sale.get('status')})."}

            if sale.get('credit_note_id'):
                return {'success': False, 'message': 'La venta ya tiene una nota de crédito asociada.'}

            # 2) Obtener items base si no se pasan (nota completa)
            if items is None:
                cursor.execute("SELECT * FROM sale_items WHERE sale_id = %s", (sale_id,))
                items = cursor.fetchall() or []
            if not items:
                return {'success': False, 'message': 'No hay items para generar la nota de crédito.'}

            # 3) Generar número de nota
            credit_note_number = self._generate_credit_note_number(cursor)

            # 4) Calcular totales
            subtotal = Decimal('0')
            tax_amount = Decimal('0')
            total_amount = Decimal('0')
            prepared_items = []
            for item in items:
                qty = Decimal(str(item.get('quantity', 0)))
                unit_price = Decimal(str(item.get('unit_price', 0)))
                disc_percent = Decimal(str(item.get('discount_percent', 0)))
                disc_amount = Decimal(str(item.get('discount_amount', 0)))
                item_subtotal = Decimal(str(item.get('subtotal', qty * unit_price - disc_amount)))
                item_tax = Decimal(str(item.get('tax_amount', 0)))
                item_total = Decimal(str(item.get('total', item_subtotal + item_tax)))

                subtotal += item_subtotal
                tax_amount += item_tax
                total_amount += item_total

                prepared_items.append({
                    'sale_item_id': item.get('id'),
                    'product_id': item['product_id'],
                    'product_sku': item.get('product_sku', ''),
                    'product_name': item.get('product_name', ''),
                    'quantity': qty,
                    'unit_price': unit_price,
                    'discount_percent': disc_percent,
                    'discount_amount': disc_amount,
                    'subtotal': item_subtotal,
                    'tax_rate': Decimal(str(item.get('tax_rate', 18))),
                    'tax_amount': item_tax,
                    'total': item_total
                })

            # 5) Insertar nota
            insert_note = """
                INSERT INTO credit_notes (
                    credit_note_number, sale_id, issued_by, reason,
                    subtotal, tax_amount, total_amount, status,
                    inventory_restored, inventory_restored_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, 'issued', 0, NULL)
            """
            cursor.execute(insert_note, (
                credit_note_number, sale_id, user_id, reason,
                subtotal, tax_amount, total_amount
            ))
            credit_note_id = cursor.lastrowid

            # 6) Insertar items de la nota
            insert_item = """
                INSERT INTO credit_note_items (
                    credit_note_id, sale_item_id, product_id, product_sku, product_name,
                    quantity, unit_price, discount_percent, discount_amount,
                    subtotal, tax_rate, tax_amount, total
                ) VALUES (
                    %(credit_note_id)s, %(sale_item_id)s, %(product_id)s, %(product_sku)s, %(product_name)s,
                    %(quantity)s, %(unit_price)s, %(discount_percent)s, %(discount_amount)s,
                    %(subtotal)s, %(tax_rate)s, %(tax_amount)s, %(total)s
                )
            """
            for item in prepared_items:
                item['credit_note_id'] = credit_note_id
                cursor.execute(insert_item, item)

                # 7) Restaurar stock y movimiento
                self._update_product_stock(cursor, item['product_id'], item['quantity'])
                self._create_inventory_movement(cursor, {
                    'product_id': item['product_id'],
                    'movement_type': 'credit_note',
                    'quantity': item['quantity'],
                    'reference_type': 'manual',
                    'reference_id': credit_note_id,
                    'user_id': user_id,
                    'notes': f"Nota de crédito {credit_note_number} (venta #{sale.get('sale_number', sale_id)})"
                })

            # 8) Actualizar venta
            cursor.execute(
                """
                UPDATE sales
                SET status = 'credited', credit_note_id = %s,
                    cancelled_at = CURRENT_TIMESTAMP,
                    cancelled_by = %s,
                    cancellation_reason = %s
                WHERE id = %s
                """,
                (credit_note_id, user_id, reason or 'Generada nota de crédito', sale_id)
            )

            # 9) Marcar inventario restaurado
            cursor.execute(
                """
                UPDATE credit_notes
                SET inventory_restored = 1, inventory_restored_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (credit_note_id,)
            )

            connection.commit()
            return {
                'success': True,
                'credit_note_id': credit_note_id,
                'credit_note_number': credit_note_number,
                'message': 'Nota de crédito generada y stock restaurado.'
            }

        except Exception as e:
            if connection:
                connection.rollback()
            self.logger.exception("Error creando nota de crédito")
            message = str(e) or repr(e)
            return {'success': False, 'message': message}
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    # ==========================
    # Consultas
    # ==========================
    def list_credit_notes(self, limit: int = 200) -> List[Dict[str, Any]]:
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT cn.*, s.sale_number, u.full_name AS issued_by_name
                FROM credit_notes cn
                LEFT JOIN sales s ON cn.sale_id = s.id
                LEFT JOIN users u ON cn.issued_by = u.id
                ORDER BY cn.created_at DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            return rows
        except Exception as e:
            self.logger.error(f"Error listando notas de crédito: {e}")
            return []

    def _generate_credit_note_number(self, cursor) -> str:
        year = datetime.now().year
        cursor.execute(
            """
            SELECT credit_note_number
            FROM credit_notes
            WHERE credit_note_number LIKE %s
            ORDER BY id DESC
            LIMIT 1
            """,
            (f"NC-{year}-%",)
        )
        result = cursor.fetchone()
        if result:
            if isinstance(result, dict):
                raw_value = result.get('credit_note_number')
            else:
                raw_value = result[0]

            try:
                last_number = int(str(raw_value).split('-')[-1])
            except (ValueError, TypeError):
                last_number = 0
            new_number = last_number + 1
        else:
            new_number = 1
        return f"NC-{year}-{new_number:05d}"

    # ==========================
    # Helpers internos
    # ==========================
    def _update_product_stock(self, cursor, product_id: int, quantity_change: Decimal):
        cursor.execute(
            """
            UPDATE products
            SET stock_quantity = stock_quantity + %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """,
            (quantity_change, product_id)
        )

    def _create_inventory_movement(self, cursor, movement: Dict[str, Any]):
        cursor.execute("SELECT stock_quantity FROM products WHERE id = %s", (movement['product_id'],))
        result = cursor.fetchone()
        if not result:
            current_stock = Decimal('0')
        elif isinstance(result, dict):
            current_stock = Decimal(str(result.get('stock_quantity', 0)))
        else:
            current_stock = Decimal(str(result[0]))
        quantity = Decimal(str(movement['quantity']))
        movement['previous_stock'] = current_stock
        movement['new_stock'] = current_stock + quantity
        cursor.execute(
            """
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
            """,
            movement
        )
