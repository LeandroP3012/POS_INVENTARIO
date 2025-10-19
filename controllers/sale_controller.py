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
            payment_info: dict con información de pago
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
            
            # Calcular totales
            totals = self._calculate_totals(cart_items, payment_info.get('discount_amount', 0))
            
            # Preparar datos de venta
            sale_data = {
                'user_id': user_id,
                'customer_id': customer_id,
                'subtotal': totals['subtotal'],
                'tax_rate': totals['tax_rate'],
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
    
    def _calculate_totals(self, cart_items, discount_amount=0):
        """Calcula los totales de la venta"""
        tax_rate = Decimal('18.00')  # IGV 18%
        subtotal = Decimal('0')
        
        # Calcular subtotal de cada item
        for item in cart_items:
            item_subtotal = Decimal(str(item['price'])) * Decimal(str(item['quantity']))
            item_discount = item.get('discount_amount', 0)
            item_subtotal_after_discount = item_subtotal - Decimal(str(item_discount))
            
            # Calcular impuesto del item
            item_tax = (item_subtotal_after_discount * tax_rate / Decimal('100')).quantize(Decimal('0.01'))
            item_total = item_subtotal_after_discount + item_tax
            
            # Actualizar item con cálculos
            item['subtotal'] = float(item_subtotal_after_discount)
            item['tax_amount'] = float(item_tax)
            item['total'] = float(item_total)
            
            subtotal += item_subtotal_after_discount
        
        # Aplicar descuento general
        discount = Decimal(str(discount_amount))
        subtotal_after_discount = subtotal - discount
        
        # Calcular impuesto total
        tax_amount = (subtotal_after_discount * tax_rate / Decimal('100')).quantize(Decimal('0.01'))
        
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
            success = self.sale_model.cancel_sale(sale_id, user_id, reason)
            
            if success:
                return {
                    'success': True,
                    'message': 'Venta cancelada exitosamente'
                }
            else:
                return {
                    'success': False,
                    'message': 'No se pudo cancelar la venta'
                }
        
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
            sales = self.sale_model.get_all_sales(filters)
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
            # Si no hay texto de búsqueda, devolver todos los productos activos con stock
            if not search_text or search_text.strip() == "":
                # Obtener todos los productos activos
                products = self.product_model.get_all_products(include_inactive=False)
                
                # Filtrar solo activos con stock
                available_products = [
                    p for p in products 
                    if p.get('status') == 'active' and p.get('stock_quantity', 0) > 0
                ]
            else:
                # Buscar en base de datos
                products = self.product_model.search_products(search_text)
                
                # Filtrar solo productos activos con stock
                available_products = [
                    p for p in products 
                    if p.get('status') == 'active' and p.get('stock_quantity', 0) > 0
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
