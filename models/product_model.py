"""
Modelo de Producto
Gestión de productos e inventario
"""

from typing import Dict, Any, List, Optional
from models.base_model import BaseModel
from datetime import datetime
import logging


class ProductModel(BaseModel):
    """Modelo para gestión de productos"""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('model.ProductModel')
        self.table_name = 'products'
    
    def generate_next_code(self) -> str:
        """
        Generar el siguiente código de producto disponible
        Formato: PROD-XXXXXX (ej: PROD-000001, PROD-000002, etc.)
        Soporta hasta 999,999 productos
        
        Returns:
            Siguiente código disponible (ej: "PROD-000045")
        """
        try:
            connection = self.get_connection()
            if not connection:
                return "PROD-000001"
            
            cursor = connection.cursor()
            
            # Obtener el último código que sigue el patrón PROD-XXXXXX
            # Buscar códigos que empiecen con PROD- y tengan números después
            # PROD- tiene 5 caracteres, entonces SUBSTRING desde posición 6 toma todo después del guión
            query = """
                SELECT sku 
                FROM products 
                WHERE sku LIKE 'PROD-%'
                  AND LENGTH(sku) = 11
                  AND SUBSTRING(sku, 6) REGEXP '^[0-9]+$'
                ORDER BY CAST(SUBSTRING(sku, 6) AS UNSIGNED) DESC 
                LIMIT 1
            """
            
            self.logger.info(f"🔍 Buscando último código PROD-XXXXXX en base de datos...")
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            
            if result and result[0]:
                # Extraer el número después de "PROD-"
                last_code = result[0]
                # Separar por guión y tomar la parte numérica
                parts = last_code.split('-')
                if len(parts) == 2 and parts[1].isdigit():
                    last_number = int(parts[1])
                    next_number = last_number + 1
                    self.logger.info(f"   Último código encontrado: {last_code}")
                    self.logger.info(f"   Último número: {last_number}")
                    self.logger.info(f"   ✅ Siguiente número: {next_number}")
                else:
                    next_number = 1
                    self.logger.warning(f"   ⚠️ Código encontrado con formato incorrecto: {last_code}")
            else:
                # No hay códigos previos, empezar desde 1
                next_number = 1
                self.logger.info(f"   No se encontraron códigos previos, iniciando desde 1")
            
            # Formatear con 6 dígitos (padding con ceros)
            next_code = f"PROD-{next_number:06d}"
            self.logger.info(f"   📦 Código generado: {next_code}")
            return next_code
            
        except Exception as e:
            self.logger.error(f"Error al generar código: {e}")
            return "PROD-000001"
    
    def generate_barcode_from_code(self, code: str) -> str:
        """
        Generar código de barras EAN-13 basado en el código del producto
        
        Para códigos PROD-XXXXXX:
        - Solo usa la parte numérica después del guión
        - Ej: "PROD-000123" → usa "123" para generar el código de barras
        - Formato final: 775 (país Perú) + número + padding + dígito verificador
        
        Args:
            code: Código del producto (ej: "PROD-000045")
            
        Returns:
            Código de barras EAN-13 de 13 dígitos (ej: "7750000000451")
        """
        try:
            self.logger.info(f"📊 Generando código de barras EAN-13 para SKU: {code}")
            
            # Extraer solo el número del código
            if code.startswith('PROD-'):
                # Separar por guión y tomar la parte numérica
                parts = code.split('-')
                if len(parts) == 2 and parts[1].isdigit():
                    # Mantener el número como string para preservar los ceros
                    # Ej: "PROD-000002" → "000002"
                    number_str = parts[1]
                    # Convertir a entero para usar en el código de barras
                    number = int(number_str)
                    self.logger.info(f"   ✓ Formato PROD-XXXXXX detectado")
                    self.logger.info(f"   ✓ Número extraído: {number_str} (valor numérico: {number})")
                else:
                    # Si no tiene el formato esperado, usar hash
                    number = abs(hash(code)) % 1000000000
                    self.logger.warning(f"   ⚠️ Formato incorrecto, usando hash: {number}")
            elif code.startswith('P') and code[1:].isdigit():
                # Compatibilidad con formato antiguo P###
                number = int(code[1:])
                self.logger.info(f"   ✓ Formato antiguo P### detectado, número: {number}")
            else:
                # Si no tiene formato reconocido, usar hash del código
                number = abs(hash(code)) % 1000000000
                self.logger.warning(f"   ⚠️ Formato no reconocido, usando hash: {number}")
            
            # Completar con prefix para EAN-13 (775 = código de país Perú)
            # Formato: 775 + número del código + padding hasta 12 dígitos
            barcode_base = f"775{number:09d}"  # 775 + 9 dígitos = 12 dígitos total
            
            self.logger.info(f"   Base del código (12 dígitos): {barcode_base}")
            
            # Calcular dígito verificador EAN-13
            check_digit = self._calculate_ean13_check_digit(barcode_base)
            
            final_barcode = f"{barcode_base}{check_digit}"
            
            self.logger.info(f"   Dígito verificador calculado: {check_digit}")
            self.logger.info(f"   ✅ Código de barras EAN-13 final: {final_barcode}")
            
            return final_barcode
            
        except Exception as e:
            self.logger.error(f"❌ Error al generar código de barras: {e}", exc_info=True)
            # Fallback: generar código basado en timestamp
            import time
            fallback = f"775{int(time.time()) % 1000000000:09d}0"
            self.logger.warning(f"   Usando código de barras fallback: {fallback}")
            return fallback
    
    def _calculate_ean13_check_digit(self, barcode_12: str) -> int:
        """
        Calcular dígito verificador para código EAN-13
        
        Args:
            barcode_12: Primeros 12 dígitos del código
            
        Returns:
            Dígito verificador (0-9)
        """
        try:
            # Sumar dígitos en posiciones impares (multiplicar por 1)
            odd_sum = sum(int(barcode_12[i]) for i in range(0, 12, 2))
            
            # Sumar dígitos en posiciones pares (multiplicar por 3)
            even_sum = sum(int(barcode_12[i]) * 3 for i in range(1, 12, 2))
            
            # Calcular total
            total = odd_sum + even_sum
            
            # Dígito verificador
            check_digit = (10 - (total % 10)) % 10
            
            return check_digit
            
        except Exception as e:
            self.logger.error(f"Error al calcular dígito verificador: {e}")
            return 0
    
    def get_connection(self):
        """Obtener conexión a la base de datos"""
        if not self.db:
            self.logger.error("DB no disponible")
            return None
        
        if not self.db.connection or not self.db.connection.is_connected():
            if not self.db.connect():
                self.logger.error("No se pudo conectar a la base de datos")
                return None
        
        return self.db.connection
    
    def create_product(self, product_data: Dict[str, Any]) -> Optional[int]:
        """
        Crear un nuevo producto - COMPATIBLE con estructura real de la tabla
        
        Args:
            product_data: Diccionario con datos del producto
            
        Returns:
            ID del producto creado o None si hay error
        """
        try:
            connection = self.get_connection()
            if not connection:
                self.logger.error("No hay conexión a la base de datos")
                return None
            
            cursor = connection.cursor()
            
            # Validar datos requeridos
            name = product_data.get('name')
            sku = product_data.get('sku') or product_data.get('code')
            category_id = product_data.get('category_id')
            unit_id = product_data.get('unit_id', 1)  # Default: Unidad
            price = product_data.get('price', 0)
            cost = product_data.get('cost', 0)
            
            if not name or not name.strip():
                self.logger.error("Campo requerido faltante: name")
                return None
            
            if not sku or not sku.strip():
                self.logger.error("Campo requerido faltante: sku")
                return None
            
            query = """
                INSERT INTO products (
                    sku, name, description, category_id, unit_id,
                    barcode, price, cost,
                    stock_quantity, min_stock, max_stock, tax_rate,
                    status, image_path, created_by
                ) VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s
                )
            """
            
            values = (
                sku,
                name,
                product_data.get('description', ''),
                category_id,
                unit_id,
                product_data.get('barcode', ''),
                price,
                cost,
                product_data.get('stock_quantity', 0),
                product_data.get('min_stock', 0),
                product_data.get('max_stock', 0),
                product_data.get('tax_rate', 18.0),
                product_data.get('status', 'active'),
                product_data.get('image_path'),
                product_data.get('created_by', 1)
            )
            
            cursor.execute(query, values)
            connection.commit()
            product_id = cursor.lastrowid
            
            self.logger.info(f"Producto creado exitosamente: {name} (ID: {product_id})")
            cursor.close()
            return product_id
            
        except Exception as e:
            self.logger.error(f"Error al crear producto: {e}")
            import traceback
            traceback.print_exc()
            if connection:
                connection.rollback()
            return None
    
    def get_all_products(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """
        Obtener todos los productos
        COMPATIBLE con scriptDB.txt: usa 'code', 'active', 'current_stock', 'sale_price', 'cost_price'
        
        Args:
            include_inactive: Incluir productos inactivos
            
        Returns:
            Lista de productos
        """
        try:
            connection = self.get_connection()
            if not connection:
                return []
            
            cursor = connection.cursor(dictionary=True)
            
            # Query compatible con estructura real de la tabla
            query = """
                SELECT 
                    p.id,
                    p.sku,
                    p.barcode,
                    p.name,
                    p.description,
                    p.category_id,
                    p.cost,
                    p.price,
                    p.stock_quantity,
                    p.min_stock,
                    p.max_stock,
                    p.tax_rate,
                    p.image_path,
                    p.status,
                    p.created_at,
                    p.updated_at,
                    p.created_by,
                    p.unit_id,
                    c.name as category_name,
                    u.name as unit_name,
                    u.symbol as unit_symbol
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                LEFT JOIN units u ON p.unit_id = u.id
            """
            
            if not include_inactive:
                query += " WHERE p.status = 'active'"
            
            query += " ORDER BY p.name ASC"
            
            cursor.execute(query)
            products = cursor.fetchall()
            cursor.close()
            
            # Calcular margen de ganancia y estado del stock
            for product in products:
                # Calcular margen
                cost = product.get('cost', 0) or 0
                price = product.get('price', 0) or 0
                
                if cost and cost > 0:
                    product['profit_margin'] = ((price - cost) / cost) * 100
                else:
                    product['profit_margin'] = 0
                
                # Estado del stock
                stock_qty = product.get('stock_quantity', 0) or 0
                min_stock = product.get('min_stock', 0) or 0
                max_stock = product.get('max_stock', 0) or 0
                
                if stock_qty <= 0:
                    product['stock_status'] = 'out_of_stock'
                elif stock_qty <= min_stock:
                    product['stock_status'] = 'low_stock'
                elif max_stock > 0 and stock_qty >= max_stock:
                    product['stock_status'] = 'overstock'
                else:
                    product['stock_status'] = 'normal'
                
                # Agregar campos para compatibilidad
                product['unit_name'] = product.get('unit', 'Unidad')
                product['unit_symbol'] = product.get('unit', 'un')
            
            self.logger.info(f"Se obtuvieron {len(products)} productos")
            return products
            
        except Exception as e:
            self.logger.error(f"Error al obtener productos: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_product_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Obtener producto por ID - COMPATIBLE con scriptDB.txt"""
        try:
            connection = self.get_connection()
            if not connection:
                return None
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    p.id,
                    p.sku,
                    p.barcode,
                    p.name,
                    p.description,
                    p.category_id,
                    p.cost,
                    p.price,
                    p.stock_quantity,
                    p.min_stock,
                    p.max_stock,
                    p.unit_id,
                    p.tax_rate,
                    p.status,
                    p.created_at,
                    p.updated_at,
                    c.name as category_name,
                    u.name as unit_name,
                    u.symbol as unit_symbol
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                LEFT JOIN units u ON p.unit_id = u.id
                WHERE p.id = %s
            """
            
            cursor.execute(query, (product_id,))
            product = cursor.fetchone()
            cursor.close()
            
            if product:
                # Calcular margen
                cost = product.get('cost', 0) or 0
                price = product.get('price', 0) or 0
                
                if cost and cost > 0:
                    product['profit_margin'] = ((price - cost) / cost) * 100
                else:
                    product['profit_margin'] = 0
                
                # Alias para compatibilidad
                product['sku'] = product['code']
                product['unit_name'] = product.get('unit', 'Unidad')
                product['unit_symbol'] = product.get('unit', 'un')
            
            return product
            
        except Exception as e:
            self.logger.error(f"Error al obtener producto {product_id}: {e}")
            return None
    
    def update_product(self, product_id: int, product_data: Dict[str, Any]) -> bool:
        """Actualizar producto - COMPATIBLE con scriptDB.txt"""
        try:
            connection = self.get_connection()
            if not connection:
                return False
            
            cursor = connection.cursor()
            
            # Construir query dinámicamente
            fields = []
            values = []
            
            # Mapeo de campos para compatibilidad con estructura real
            field_mapping = {
                'sku': 'sku',
                'code': 'sku',
                'name': 'name',
                'description': 'description',
                'category_id': 'category_id',
                'unit_id': 'unit_id',
                'price': 'price',
                'cost': 'cost',
                'stock_quantity': 'stock_quantity',
                'min_stock': 'min_stock',
                'max_stock': 'max_stock',
                'barcode': 'barcode',
                'tax_rate': 'tax_rate',
                'status': 'status',
                'image_path': 'image_path'
            }
            
            for key, value in product_data.items():
                if key in field_mapping:
                    db_field = field_mapping[key]
                    fields.append(f"{db_field} = %s")
                    values.append(value)
            
            if not fields:
                self.logger.warning("No hay campos para actualizar")
                return False
            
            fields.append("updated_at = NOW()")
            values.append(product_id)
            
            query = f"""
                UPDATE products
                SET {', '.join(fields)}
                WHERE id = %s
            """
            
            cursor.execute(query, values)
            connection.commit()
            
            affected_rows = cursor.rowcount
            cursor.close()
            
            if affected_rows > 0:
                self.logger.info(f"Producto {product_id} actualizado exitosamente")
                return True
            else:
                self.logger.warning(f"No se encontró el producto {product_id}")
                return False
            
        except Exception as e:
            self.logger.error(f"Error al actualizar producto {product_id}: {e}")
            import traceback
            traceback.print_exc()
            if connection:
                connection.rollback()
            return False
    
    def delete_product(self, product_id: int) -> bool:
        """Eliminar producto (soft delete) - COMPATIBLE con scriptDB.txt"""
        try:
            connection = self.get_connection()
            if not connection:
                return False
            
            cursor = connection.cursor()
            
            # Soft delete - cambiar active a 0
            query = """
                UPDATE products
                SET active = 0, updated_at = NOW()
                WHERE id = %s
            """
            
            cursor.execute(query, (product_id,))
            connection.commit()
            
            affected_rows = cursor.rowcount
            cursor.close()
            
            if affected_rows > 0:
                self.logger.info(f"Producto {product_id} eliminado exitosamente")
                return True
            else:
                self.logger.warning(f"No se encontró el producto {product_id}")
                return False
            
        except Exception as e:
            self.logger.error(f"Error al eliminar producto {product_id}: {e}")
            if connection:
                connection.rollback()
            return False
    
    def search_products(self, search_term: str) -> List[Dict[str, Any]]:
        """Buscar productos por nombre, código o código de barras - COMPATIBLE"""
        try:
            connection = self.get_connection()
            if not connection:
                return []
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    p.id,
                    p.sku,
                    p.barcode,
                    p.name,
                    p.description,
                    p.category_id,
                    p.cost,
                    p.price,
                    p.stock_quantity,
                    p.min_stock,
                    p.max_stock,
                    p.unit_id,
                    p.tax_rate,
                    p.status,
                    c.name as category_name,
                    u.name as unit_name,
                    u.symbol as unit_symbol
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                LEFT JOIN units u ON p.unit_id = u.id
                WHERE p.status = 'active'
                AND (
                    p.name LIKE %s 
                    OR p.sku LIKE %s 
                    OR p.barcode LIKE %s
                )
                ORDER BY p.name ASC
            """
            
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            products = cursor.fetchall()
            cursor.close()
            
            return products
            
        except Exception as e:
            self.logger.error(f"Error al buscar productos: {e}")
            return []
    
    def get_by_barcode(self, barcode: str) -> Optional[Dict[str, Any]]:
        """Buscar producto por código de barras exacto - COMPATIBLE"""
        try:
            connection = self.get_connection()
            if not connection:
                return None
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    p.id,
                    p.sku,
                    p.barcode,
                    p.name,
                    p.cost,
                    p.price,
                    p.stock_quantity,
                    p.unit_id,
                    p.status,
                    c.name as category_name,
                    u.name as unit_name,
                    u.symbol as unit_symbol
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                LEFT JOIN units u ON p.unit_id = u.id
                WHERE p.barcode = %s
                AND p.status = 'active'
                LIMIT 1
            """
            
            cursor.execute(query, (barcode,))
            product = cursor.fetchone()
            cursor.close()
            
            return product
            
        except Exception as e:
            self.logger.error(f"Error al buscar producto por código de barras: {e}")
            return None
    
    def get_low_stock_products(self) -> List[Dict[str, Any]]:
        """Obtener productos con stock bajo - COMPATIBLE"""
        try:
            connection = self.get_connection()
            if not connection:
                return []
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    p.id,
                    p.code,
                    p.name,
                    p.current_stock as stock_quantity,
                    p.min_stock,
                    p.max_stock,
                    p.active,
                    c.name as category_name,
                    CASE WHEN p.active = 1 THEN 'active' ELSE 'inactive' END as status
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.active = 1
                AND p.current_stock <= p.min_stock
                ORDER BY p.current_stock ASC
            """
            
            cursor.execute(query)
            products = cursor.fetchall()
            cursor.close()
            
            for product in products:
                product['sku'] = product['code']
            
            return products
            
        except Exception as e:
            self.logger.error(f"Error al obtener productos con stock bajo: {e}")
            return []
    
    def update_stock(self, product_id: int, quantity: int, movement_type: str, 
                     notes: str = '', user_id: int = 1) -> bool:
        """
        Actualizar stock de producto y registrar movimiento - COMPATIBLE con scriptDB.txt
        Usa 'stock_movements' y 'current_stock'
        
        Args:
            product_id: ID del producto
            quantity: Cantidad (positivo para entrada, negativo para salida)
            movement_type: Tipo de movimiento (purchase, sale, adjustment, return)
            notes: Notas adicionales
            user_id: ID del usuario que realiza el movimiento
        """
        try:
            connection = self.get_connection()
            if not connection:
                return False
            
            cursor = connection.cursor(dictionary=True)
            
            # Obtener stock actual
            cursor.execute("SELECT stock_quantity FROM products WHERE id = %s", (product_id,))
            result = cursor.fetchone()
            
            if not result:
                self.logger.error(f"Producto {product_id} no encontrado")
                return False
            
            current_stock = result['stock_quantity'] or 0
            new_stock = current_stock + quantity
            
            if new_stock < 0:
                self.logger.error(f"Stock insuficiente. Actual: {current_stock}, Requerido: {abs(quantity)}")
                return False
            
            # Actualizar stock
            cursor.execute(
                "UPDATE products SET stock_quantity = %s, updated_at = NOW() WHERE id = %s",
                (new_stock, product_id)
            )
            
            # Registrar movimiento en stock_movements
            # Mapear tipos de movimiento a los que espera la BD
            movement_type_map = {
                'purchase': 'in',
                'sale': 'out',
                'adjustment': 'adjustment',
                'return': 'in'
            }
            
            movement_direction = movement_type_map.get(movement_type, 'adjustment')
            
            cursor.execute("""
                INSERT INTO stock_movements (
                    product_id, movement_type, movement_reason, reference_type,
                    quantity, previous_stock, new_stock, unit_cost, user_id, notes
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (product_id, movement_direction, movement_type, 'manual',
                  quantity, current_stock, new_stock, 0, user_id, notes))
            
            connection.commit()
            cursor.close()
            
            self.logger.info(f"Stock actualizado para producto {product_id}: {current_stock} -> {new_stock}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al actualizar stock: {e}")
            import traceback
            traceback.print_exc()
            if connection:
                connection.rollback()
            return False
    
    def update_stock_direct(self, product_id: int, new_stock: float, movement_type: str,
                          notes: str = '', user_id: int = 1, 
                          min_stock: float = 0, max_stock: float = 0) -> bool:
        """
        Actualizar stock directamente a un valor específico y registrar movimiento
        COMPATIBLE con scriptDB.txt: usa 'current_stock' y 'stock_movements'
        
        Args:
            product_id: ID del producto
            new_stock: Nuevo valor de stock
            movement_type: Tipo de movimiento (entrada, salida, ajuste)
            notes: Notas adicionales
            user_id: ID del usuario que realiza el movimiento
            min_stock: Stock mínimo
            max_stock: Stock máximo
        """
        try:
            connection = self.get_connection()
            if not connection:
                return False
            
            cursor = connection.cursor(dictionary=True)
            
            # Obtener stock actual
            cursor.execute("SELECT stock_quantity FROM products WHERE id = %s", (product_id,))
            result = cursor.fetchone()
            
            if not result:
                self.logger.error(f"Producto {product_id} no encontrado")
                return False
            
            # Convertir Decimal a float para evitar errores de tipo
            current_stock = float(result['stock_quantity'] or 0)
            quantity = new_stock - current_stock  # Diferencia para el movimiento
            
            # Actualizar stock, min_stock y max_stock
            cursor.execute("""
                UPDATE products 
                SET stock_quantity = %s, 
                    min_stock = %s,
                    max_stock = %s,
                    updated_at = NOW() 
                WHERE id = %s
            """, (new_stock, min_stock, max_stock, product_id))
            
            # Registrar movimiento en stock_movements
            movement_type_map = {
                'purchase': 'in',
                'sale': 'out',
                'adjustment': 'adjustment',
                'entrada': 'in',
                'salida': 'out',
                'ajuste': 'adjustment'
            }
            
            movement_direction = movement_type_map.get(movement_type, 'adjustment')
            
            cursor.execute("""
                INSERT INTO stock_movements (
                    product_id, movement_type, movement_reason, reference_type,
                    quantity, previous_stock, new_stock, unit_cost, user_id, notes
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (product_id, movement_direction, movement_type, 'manual',
                  quantity, current_stock, new_stock, 0, user_id, notes))
            
            connection.commit()
            cursor.close()
            
            self.logger.info(f"Stock actualizado directamente para producto {product_id}: {current_stock} → {new_stock} (min: {min_stock}, max: {max_stock})")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al actualizar stock directamente: {e}")
            import traceback
            traceback.print_exc()
            if connection:
                connection.rollback()
            return False
    
    def update_product_limits(self, product_id: int, min_stock: float, max_stock: float) -> bool:
        """
        Actualizar solo los límites de stock (min/max) sin afectar el stock actual
        
        Args:
            product_id: ID del producto
            min_stock: Stock mínimo
            max_stock: Stock máximo
        """
        try:
            print(f"\n🔍 ProductModel.update_product_limits llamado")
            print(f"   Product ID: {product_id}")
            print(f"   Min: {min_stock}, Max: {max_stock}")
            
            connection = self.get_connection()
            if not connection:
                print(f"   ❌ No hay conexión a BD")
                return False
            
            cursor = connection.cursor()
            
            # Actualizar solo min_stock y max_stock
            cursor.execute("""
                UPDATE products 
                SET min_stock = %s,
                    max_stock = %s,
                    updated_at = NOW() 
                WHERE id = %s
            """, (min_stock, max_stock, product_id))
            
            connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            
            print(f"   ✅ Filas afectadas: {affected_rows}")
            
            self.logger.info(f"Límites actualizados para producto {product_id}: min={min_stock}, max={max_stock}")
            return affected_rows > 0
            
        except Exception as e:
            self.logger.error(f"Error al actualizar límites: {e}")
            import traceback
            traceback.print_exc()
            if connection:
                connection.rollback()
            return False
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """Obtener todas las categorías activas - COMPATIBLE con estructura real"""
        try:
            connection = self.get_connection()
            if not connection:
                return []
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    c.id,
                    c.name,
                    c.description,
                    c.parent_id,
                    c.status,
                    c.created_at,
                    c.updated_at,
                    COUNT(p.id) as product_count
                FROM categories c
                LEFT JOIN products p ON c.id = p.category_id AND p.status = 'active'
                WHERE c.status = 'active'
                GROUP BY c.id, c.name, c.description, c.parent_id, c.status, c.created_at, c.updated_at
                ORDER BY c.name ASC
            """
            
            cursor.execute(query)
            categories = cursor.fetchall()
            cursor.close()
            
            return categories
            
        except Exception as e:
            self.logger.error(f"Error al obtener categorías: {e}")
            return []
    
    def get_units(self) -> List[Dict[str, Any]]:
        """
        Obtener unidades de medida simuladas
        NOTA: La tabla 'units' NO existe en scriptDB.txt
        Retorna lista predefinida de unidades comunes
        """
        # Lista predefinida de unidades ya que la tabla no existe
        predefined_units = [
            {'id': 1, 'name': 'Unidad', 'symbol': 'un', 'type': 'unit', 'status': 'active'},
            {'id': 2, 'name': 'Kilogramo', 'symbol': 'kg', 'type': 'weight', 'status': 'active'},
            {'id': 3, 'name': 'Gramo', 'symbol': 'g', 'type': 'weight', 'status': 'active'},
            {'id': 4, 'name': 'Litro', 'symbol': 'L', 'type': 'volume', 'status': 'active'},
            {'id': 5, 'name': 'Mililitro', 'symbol': 'ml', 'type': 'volume', 'status': 'active'},
            {'id': 6, 'name': 'Metro', 'symbol': 'm', 'type': 'length', 'status': 'active'},
            {'id': 7, 'name': 'Paquete', 'symbol': 'paq', 'type': 'unit', 'status': 'active'},
            {'id': 8, 'name': 'Caja', 'symbol': 'cja', 'type': 'unit', 'status': 'active'},
            {'id': 9, 'name': 'Docena', 'symbol': 'doc', 'type': 'unit', 'status': 'active'}
        ]
        
        try:
            # Intentar obtener de la BD si existe la tabla
            connection = self.get_connection()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SHOW TABLES LIKE 'units'")
                if cursor.fetchone():
                    # La tabla existe, obtener datos
                    query = "SELECT * FROM units WHERE status = 'active' ORDER BY name ASC"
                    cursor.execute(query)
                    units = cursor.fetchall()
                    cursor.close()
                    return units if units else predefined_units
                cursor.close()
        except:
            pass
        
        # Si la tabla no existe o hay error, retornar lista predefinida
        return predefined_units
