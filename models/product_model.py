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
        Crear un nuevo producto
        
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
            required_fields = ['name', 'sku', 'category_id', 'price', 'cost']
            for field in required_fields:
                if field not in product_data or product_data[field] is None:
                    self.logger.error(f"Campo requerido faltante: {field}")
                    return None
            
            query = """
                INSERT INTO products (
                    sku, name, description, category_id, unit_id,
                    price, cost, stock_quantity, min_stock, max_stock,
                    barcode, tax_rate, status, created_by
                ) VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
            """
            
            values = (
                product_data['sku'],
                product_data['name'],
                product_data.get('description', ''),
                product_data['category_id'],
                product_data.get('unit_id', 1),
                product_data['price'],
                product_data['cost'],
                product_data.get('stock_quantity', 0),
                product_data.get('min_stock', 0),
                product_data.get('max_stock', 0),
                product_data.get('barcode', ''),
                product_data.get('tax_rate', 0.0),
                product_data.get('status', 'active'),
                product_data.get('created_by', 1)
            )
            
            cursor.execute(query, values)
            connection.commit()
            product_id = cursor.lastrowid
            
            self.logger.info(f"Producto creado exitosamente: {product_data['name']} (ID: {product_id})")
            cursor.close()
            return product_id
            
        except Exception as e:
            self.logger.error(f"Error al crear producto: {e}")
            if connection:
                connection.rollback()
            return None
    
    def get_all_products(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """
        Obtener todos los productos
        
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
            
            query = """
                SELECT 
                    p.*,
                    c.name as category_name,
                    u.name as unit_name,
                    u.symbol as unit_symbol,
                    (SELECT COUNT(*) FROM product_movements pm WHERE pm.product_id = p.id) as movement_count
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
            
            # Calcular margen de ganancia
            for product in products:
                if product['cost'] and product['cost'] > 0:
                    product['profit_margin'] = ((product['price'] - product['cost']) / product['cost']) * 100
                else:
                    product['profit_margin'] = 0
                
                # Estado del stock
                if product['stock_quantity'] <= 0:
                    product['stock_status'] = 'out_of_stock'
                elif product['stock_quantity'] <= product['min_stock']:
                    product['stock_status'] = 'low_stock'
                elif product['stock_quantity'] >= product['max_stock']:
                    product['stock_status'] = 'overstock'
                else:
                    product['stock_status'] = 'normal'
            
            self.logger.info(f"Se obtuvieron {len(products)} productos")
            return products
            
        except Exception as e:
            self.logger.error(f"Error al obtener productos: {e}")
            return []
    
    def get_product_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Obtener producto por ID"""
        try:
            connection = self.get_connection()
            if not connection:
                return None
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    p.*,
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
                if product['cost'] and product['cost'] > 0:
                    product['profit_margin'] = ((product['price'] - product['cost']) / product['cost']) * 100
                else:
                    product['profit_margin'] = 0
            
            return product
            
        except Exception as e:
            self.logger.error(f"Error al obtener producto {product_id}: {e}")
            return None
    
    def update_product(self, product_id: int, product_data: Dict[str, Any]) -> bool:
        """Actualizar producto"""
        try:
            connection = self.get_connection()
            if not connection:
                return False
            
            cursor = connection.cursor()
            
            # Construir query dinámicamente
            fields = []
            values = []
            
            allowed_fields = [
                'sku', 'name', 'description', 'category_id', 'unit_id',
                'price', 'cost', 'stock_quantity', 'min_stock', 'max_stock',
                'barcode', 'tax_rate', 'status'
            ]
            
            for field in allowed_fields:
                if field in product_data:
                    fields.append(f"{field} = %s")
                    values.append(product_data[field])
            
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
            if connection:
                connection.rollback()
            return False
    
    def delete_product(self, product_id: int) -> bool:
        """Eliminar producto (soft delete)"""
        try:
            connection = self.get_connection()
            if not connection:
                return False
            
            cursor = connection.cursor()
            
            # Soft delete - cambiar estado a inactive
            query = """
                UPDATE products
                SET status = 'inactive', updated_at = NOW()
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
        """Buscar productos por nombre, SKU o código de barras"""
        try:
            connection = self.get_connection()
            if not connection:
                return []
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    p.*,
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
    
    def get_low_stock_products(self) -> List[Dict[str, Any]]:
        """Obtener productos con stock bajo"""
        try:
            connection = self.get_connection()
            if not connection:
                return []
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    p.*,
                    c.name as category_name
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.status = 'active'
                AND p.stock_quantity <= p.min_stock
                ORDER BY p.stock_quantity ASC
            """
            
            cursor.execute(query)
            products = cursor.fetchall()
            cursor.close()
            
            return products
            
        except Exception as e:
            self.logger.error(f"Error al obtener productos con stock bajo: {e}")
            return []
    
    def update_stock(self, product_id: int, quantity: int, movement_type: str, 
                     notes: str = '', user_id: int = 1) -> bool:
        """
        Actualizar stock de producto y registrar movimiento
        
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
            
            current_stock = result['stock_quantity']
            new_stock = current_stock + quantity
            
            if new_stock < 0:
                self.logger.error(f"Stock insuficiente. Actual: {current_stock}, Requerido: {abs(quantity)}")
                return False
            
            # Actualizar stock
            cursor.execute(
                "UPDATE products SET stock_quantity = %s, updated_at = NOW() WHERE id = %s",
                (new_stock, product_id)
            )
            
            # Registrar movimiento
            cursor.execute("""
                INSERT INTO product_movements (
                    product_id, movement_type, quantity, 
                    previous_stock, new_stock, notes, created_by
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (product_id, movement_type, quantity, current_stock, new_stock, notes, user_id))
            
            connection.commit()
            cursor.close()
            
            self.logger.info(f"Stock actualizado para producto {product_id}: {current_stock} -> {new_stock}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al actualizar stock: {e}")
            if connection:
                connection.rollback()
            return False
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """Obtener todas las categorías activas"""
        try:
            connection = self.get_connection()
            if not connection:
                return []
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    c.*,
                    COUNT(p.id) as product_count
                FROM categories c
                LEFT JOIN products p ON c.id = p.category_id AND p.status = 'active'
                WHERE c.status = 'active'
                GROUP BY c.id
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
        """Obtener todas las unidades de medida"""
        try:
            connection = self.get_connection()
            if not connection:
                return []
            
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM units WHERE status = 'active' ORDER BY name ASC"
            
            cursor.execute(query)
            units = cursor.fetchall()
            cursor.close()
            
            return units
            
        except Exception as e:
            self.logger.error(f"Error al obtener unidades: {e}")
            return []
