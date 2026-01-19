"""
Controlador para módulo de ventas (POS)
Autor: Sistema POS
Fecha: 2025
"""

from models.sale_model import SaleModel
from models.customer_model import CustomerModel
from models.product_model import ProductModel
from decimal import Decimal
from datetime import datetime

class SaleController:
    """Controlador para operaciones de ventas"""
    
    def __init__(self):
        self.sale_model = SaleModel()
        self.customer_model = CustomerModel()
        self.product_model = ProductModel()
        self.default_sales_limit = 500
        self.default_product_limit = 500
    
    # ==========================================
    # OPERACIONES DE VENTA
    # ==========================================
    
    def process_sale(self, cart_items, customer_id, user_id, payment_info, notes=""):
        """
        Procesa una venta completa
        
        Args:
            cart_items: lista de productos en el carrito
            customer_id: ID del cliente (None para genérico)
            user_id: ID del cajero
            payment_info: dict con información de pago (debe incluir 'include_tax': bool)
            notes: notas adicionales
        
        Returns:
            dict con resultado de la operación
        """
        try:
            # Validar carrito
            if not cart_items:
                return {'success': False, 'message': 'El carrito está vacío'}
            
            # Si no hay cliente, usar el genérico
            if not customer_id:
                generic_customer = self.customer_model.get_generic_customer()
                if generic_customer:
                    customer_id = generic_customer['id']
            
            # Obtener si la venta incluye IGV (por defecto True para compatibilidad)
            include_tax = payment_info.get('include_tax', True)
            
            # Calcular totales
            totals = self._calculate_totals(cart_items, payment_info.get('discount_amount', 0), include_tax)
            
            # Preparar datos de venta
            sale_data = {
                'user_id': user_id,
                'customer_id': customer_id,
                'subtotal': totals['subtotal'],
                'tax_rate': totals['tax_rate'],
                'include_tax': include_tax,
                'tax_amount': totals['tax_amount'],
                'discount_amount': totals['discount_amount'],
                'total_amount': totals['total'],
                'payment_method': payment_info.get('method', 'cash'),
                'paid_amount': payment_info.get('paid_amount', totals['total']),
                'change_amount': payment_info.get('change_amount', 0),
                'status': 'completed',
                'notes': notes
            }
            
            # Preparar items
            items = []
            for item in cart_items:
                items.append({
                    'product_id': item['id'],
                    'product_sku': item['sku'],
                    'product_name': item['name'],
                    'quantity': item['quantity'],
                    'unit_price': item['price'],
                    'discount_percent': item.get('discount_percent', 0),
                    'discount_amount': item.get('discount_amount', 0),
                    'subtotal': item['subtotal'],
                    'tax_rate': totals['tax_rate'],
                    'tax_amount': item['tax_amount'],
                    'total': item['total']
                })
            
            # Preparar pagos múltiples (si aplica)
            payments = None
            if payment_info.get('method') == 'multiple' and payment_info.get('payments'):
                payments = payment_info['payments']
            
            # Crear venta
            sale_id = self.sale_model.create_sale(sale_data, items, payments)
            
            if sale_id:
                # Obtener datos completos de la venta
                sale = self.sale_model.get_sale_by_id(sale_id)
                return {
                    'success': True,
                    'message': f'Venta {sale["sale_number"]} procesada exitosamente',
                    'sale_id': sale_id,
                    'sale_number': sale['sale_number'],
                    'sale': sale
                }
            else:
                return {'success': False, 'message': 'Error al procesar la venta'}
        
        except Exception as e:
            print(f"❌ Error en process_sale: {e}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def _calculate_totals(self, cart_items, discount_amount=0, include_tax=True):
        """Calcula los totales de la venta
        
        Args:
            cart_items: lista de productos en el carrito
            discount_amount: monto de descuento a aplicar
            include_tax: si True, calcula IGV; si False, no calcula IGV
        """
        tax_rate = Decimal('18.00') if include_tax else Decimal('0.00')  # IGV 18% solo si está activado
        subtotal = Decimal('0')
        
        # Calcular subtotal de cada item
        for item in cart_items:
            item_subtotal = Decimal(str(item['price'])) * Decimal(str(item['quantity']))
            item_discount = item.get('discount_amount', 0)
            item_subtotal_after_discount = item_subtotal - Decimal(str(item_discount))
            
            # Calcular impuesto del item (solo si include_tax es True)
            if include_tax:
                item_tax = (item_subtotal_after_discount * tax_rate / Decimal('100')).quantize(Decimal('0.01'))
            else:
                item_tax = Decimal('0.00')
            
            item_total = item_subtotal_after_discount + item_tax
            
            # Actualizar item con cálculos
            item['subtotal'] = float(item_subtotal_after_discount)
            item['tax_amount'] = float(item_tax)
            item['total'] = float(item_total)
            
            subtotal += item_subtotal_after_discount
        
        # Aplicar descuento general
        discount = Decimal(str(discount_amount))
        subtotal_after_discount = subtotal - discount
        
        # Calcular impuesto total (solo si include_tax es True)
        if include_tax:
            tax_amount = (subtotal_after_discount * tax_rate / Decimal('100')).quantize(Decimal('0.01'))
        else:
            tax_amount = Decimal('0.00')
        
        # Total final
        total = subtotal_after_discount + tax_amount
        
        return {
            'subtotal': float(subtotal),
            'discount_amount': float(discount),
            'tax_rate': float(tax_rate),
            'tax_amount': float(tax_amount),
            'total': float(total)
        }
    
    def cancel_sale(self, sale_id, user_id, reason):
        """Cancela una venta"""
        try:
            result = self.sale_model.cancel_sale(sale_id, user_id, reason)

            if isinstance(result, dict):
                return result

            return {
                'success': bool(result),
                'message': 'Venta cancelada exitosamente' if result else 'No se pudo cancelar la venta'
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }

    def create_credit_note(self, sale_id: int, user_id: int, reason: str = "", items=None):
        """Generar una nota de crédito para una venta"""
        try:
            return self.sale_model.create_credit_note(sale_id, user_id, reason, items)
        except Exception as e:
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    # ==========================================
    # CONSULTAS
    # ==========================================
    
    def get_sales_list(self, filters=None):
        """Obtiene lista de ventas con filtros"""
        try:
            normalized_filters = filters.copy() if filters else {}
            if normalized_filters.get('limit') is None:
                normalized_filters['limit'] = self.default_sales_limit

            sales = self.sale_model.get_all_sales(normalized_filters)
            return {'success': True, 'sales': sales}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_sale_detail(self, sale_id):
        """Obtiene detalle completo de una venta"""
        try:
            sale = self.sale_model.get_sale_by_id(sale_id)
            if sale:
                return {'success': True, 'sale': sale}
            else:
                return {'success': False, 'message': 'Venta no encontrada'}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}

    def get_recent_sales_for_credit_notes(self, sale_code: str | None = None, limit: int = 100):
        """Obtiene ventas elegibles para notas de crédito filtrando por número"""
        try:
            print(f"🔍 [DEBUG] get_recent_sales_for_credit_notes - Recibido: '{sale_code}' (tipo: {type(sale_code).__name__})")
            
            base_filters = {'status': 'completed', 'limit': limit, 'exclude_credit_notes': True}
            filters = dict(base_filters)

            sale_code_clean = None
            sale_digits = None
            sale_sanitized = None

            if sale_code:
                sale_code_clean = sale_code.strip().lower()
                print(f"🔍 [DEBUG] sale_code_clean: '{sale_code_clean}'")
                if sale_code_clean:
                    filters['sale_number'] = sale_code_clean

                    sale_digits = ''.join(ch for ch in sale_code_clean if ch.isdigit())
                    if sale_digits:
                        filters['sale_number_digits'] = sale_digits

                    sale_sanitized = ''.join(ch for ch in sale_code_clean if ch.isalnum())
                    if sale_sanitized:
                        filters['sale_number_sanitized'] = sale_sanitized
            else:
                print(f"⚠️ [DEBUG] sale_code es None o vacío, no se aplicará filtro")

            print(f"🔍 [DEBUG] Filtros: {filters}")
            
            result = self.get_sales_list(filters)
            if not result.get('success'):
                print(f"❌ [DEBUG] get_sales_list falló: {result.get('message')}")
                return result

            sales = result.get('sales', [])
            print(f"🔍 [DEBUG] Primera consulta devolvió {len(sales)} ventas")

            # Si la consulta SQL no devolvió filas, reintentar sin filtro y luego filtrar en memoria
            if sale_code_clean and not sales:
                print(f"🔄 [DEBUG] Reintentando sin filtro...")
                fallback_result = self.get_sales_list(base_filters)
                if fallback_result.get('success'):
                    sales = fallback_result.get('sales', [])
                    print(f"🔍 [DEBUG] Fallback devolvió {len(sales)} ventas")

            if sale_code_clean:
                print(f"🔍 [DEBUG] Aplicando filtro en memoria con:")
                print(f"  - term_lower: '{sale_code_clean}'")
                print(f"  - term_digits: '{sale_digits}'")
                print(f"  - term_sanitized: '{sale_sanitized}'")
                print(f"🔍 [DEBUG] Antes del filtro: {len(sales)} ventas")
                
                filtered = []
                for sale in sales:
                    matches = self._matches_sale_code(sale, sale_code_clean, sale_digits, sale_sanitized)
                    if matches:
                        print(f"  ✅ Coincide: ID={sale.get('id')}, sale_number={sale.get('sale_number')}")
                        filtered.append(sale)
                    else:
                        print(f"  ❌ No coincide: ID={sale.get('id')}, sale_number={sale.get('sale_number')}")
                
                sales = filtered
                print(f"🔍 [DEBUG] Tras filtro en memoria: {len(sales)} ventas coinciden")

            print(f"🔍 [DEBUG] Retornando {len(sales)} ventas")
            return {'success': True, 'sales': sales}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}

    @staticmethod
    def _matches_sale_code(sale: dict, term_lower: str, term_digits: str | None, term_sanitized: str | None) -> bool:
        """Asegura que la lógica de coincidencia sea consistente entre backend y vista"""
        sale_id = sale.get('id')
        sale_number_raw = sale.get('sale_number') or (f"Venta #{sale_id}" if sale_id else '')
        sale_text = str(sale_number_raw)
        sale_lower = sale_text.lower()
        sale_digits = ''.join(ch for ch in sale_text if ch.isdigit())
        sale_sanitized = ''.join(ch for ch in sale_lower if ch.isalnum())
        sale_id_str = str(sale_id) if sale_id is not None else ''

        # Debug para cada comparación
        print(f"      [MATCH] Comparando: sale_number='{sale_number_raw}'")
        print(f"      [MATCH] sale_lower='{sale_lower}', term_lower='{term_lower}'")
        print(f"      [MATCH] sale_sanitized='{sale_sanitized}', term_sanitized='{term_sanitized}'")
        print(f"      [MATCH] sale_digits='{sale_digits}', term_digits='{term_digits}'")
        print(f"      [MATCH] sale_id_str='{sale_id_str}'")

        if term_lower in sale_lower:
            print(f"      [MATCH] ✅ Coincide por term_lower in sale_lower")
            return True

        if term_sanitized and term_sanitized in sale_sanitized:
            print(f"      [MATCH] ✅ Coincide por term_sanitized in sale_sanitized")
            return True

        if term_digits and term_digits in sale_digits:
            print(f"      [MATCH] ✅ Coincide por term_digits in sale_digits")
            return True

        if term_digits and sale_id_str and term_digits == sale_id_str:
            print(f"      [MATCH] ✅ Coincide por term_digits == sale_id_str")
            return True

        if sale_id_str and term_lower == sale_id_str:
            print(f"      [MATCH] ✅ Coincide por term_lower == sale_id_str")
            return True

        print(f"      [MATCH] ❌ No coincide")
        return False
    
    def get_daily_summary(self, date=None):
        """Obtiene resumen de ventas del día"""
        try:
            summary = self.sale_model.get_daily_sales_summary(date)
            if summary:
                return {'success': True, 'summary': summary}
            else:
                return {'success': False, 'message': 'No se pudo obtener el resumen'}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    # ==========================================
    # BÚSQUEDA DE PRODUCTOS
    # ==========================================
    
    def search_products_for_sale(self, search_text):
        """Busca productos disponibles para venta"""
        try:
            # Si no hay texto de búsqueda, devolver todos los productos activos (con o sin stock)
            if not search_text or search_text.strip() == "":
                # Obtener todos los productos activos
                products = self.product_model.get_all_products(include_inactive=False, limit=self.default_product_limit)
                
                # ✅ Mostrar TODOS los productos activos (incluso sin stock para ver catálogo completo)
                available_products = [
                    p for p in products 
                    if p.get('status') == 'active'
                ]
            else:
                # Buscar en base de datos por SKU y NOMBRE
                products = self.product_model.search_products(search_text)
                
                # ✅ Mostrar productos activos encontrados (incluso sin stock)
                available_products = [
                    p for p in products 
                    if p.get('status') == 'active'
                ]
            
            return {
                'success': True,
                'products': available_products
            }
        
        except Exception as e:
            print(f"❌ Error en search_products_for_sale: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    def get_product_by_barcode(self, barcode):
        """Busca producto por código de barras"""
        try:
            product = self.product_model.get_by_barcode(barcode)
            
            if product and product.get('status') == 'active' and product.get('stock_quantity', 0) > 0:
                return {'success': True, 'product': product}
            else:
                return {'success': False, 'message': 'Producto no encontrado o sin stock'}
        
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    # ==========================================
    # CLIENTES
    # ==========================================
    
    def search_customers(self, search_text):
        """Busca clientes"""
        try:
            customers = self.customer_model.search_customers(search_text)
            return {'success': True, 'customers': customers}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_generic_customer(self):
        """Obtiene cliente genérico"""
        try:
            customer = self.customer_model.get_generic_customer()
            if customer:
                return {'success': True, 'customer': customer}
            else:
                return {'success': False, 'message': 'Cliente genérico no encontrado'}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
