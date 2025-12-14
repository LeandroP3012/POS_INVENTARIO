"""
Controlador de Productos
Lógica de negocio para gestión de productos
"""

from typing import Dict, Any, List, Optional, Tuple
import time
from models.product_model import ProductModel
from services.permission_service import PermissionService
import logging


class ProductController:
    """Controlador para gestión de productos"""
    
    def __init__(self):
        self.product_model = ProductModel()
        self.permission_service = PermissionService()
        self.logger = logging.getLogger('controller.ProductController')
        self._cache_ttl = 60  # segundos
        self._categories_cache: Optional[Tuple[float, List[Dict[str, Any]]]] = None
        self._units_cache: Optional[Tuple[float, List[Dict[str, Any]]]] = None
    
    def create_product(self, product_data: Dict[str, Any], user_data: Dict[str, Any]) -> Tuple[bool, str, Optional[int]]:
        """
        Crear nuevo producto
        
        Returns:
            (success, message, product_id)
        """
        try:
            # Verificar permisos
            if not self.permission_service.check_permission(user_data, 'inventory.create'):
                self.logger.warning(f"Usuario {user_data.get('username')} sin permiso inventory.create")
                return False, "No tienes permiso para crear productos", None
            
            # Validar datos
            is_valid, validation_errors = self._validate_product_data(product_data)
            if not is_valid:
                return False, f"Datos inválidos: {', '.join(validation_errors)}", None
            
            # Verificar SKU único
            if self._sku_exists(product_data['sku']):
                return False, f"El SKU '{product_data['sku']}' ya existe", None
            
            # Agregar usuario creador
            product_data['created_by'] = user_data.get('id', 1)
            
            # Crear producto
            product_id = self.product_model.create_product(product_data)
            
            if product_id:
                self.logger.info(f"Producto creado por {user_data.get('username')}: {product_data['name']}")
                return True, "Producto creado exitosamente", product_id
            else:
                return False, "Error al crear el producto", None
                
        except Exception as e:
            self.logger.error(f"Error en create_product: {e}")
            return False, f"Error interno: {str(e)}", None

    def generate_next_sku(self) -> Optional[str]:
        """Obtener el siguiente SKU disponible"""
        try:
            return self.product_model.generate_next_code()
        except Exception as exc:
            self.logger.error(f"Error generando próximo SKU: {exc}")
            return None
    
    def get_all_products(self, user_data: Dict[str, Any], include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Obtener todos los productos"""
        try:
            # Verificar permisos
            if not self.permission_service.check_permission(user_data, 'inventory.view'):
                self.logger.warning(f"Usuario {user_data.get('username')} sin permiso inventory.view")
                return []
            
            self.logger.info(f"Obteniendo productos (incluir inactivos: {include_inactive})")
            return self.product_model.get_all_products(include_inactive)
            
        except Exception as e:
            self.logger.error(f"Error en get_all_products: {e}")
            return []
    
    def get_product_by_id(self, product_id: int, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Obtener producto por ID"""
        try:
            # Verificar permisos
            if not self.permission_service.check_permission(user_data, 'inventory.view'):
                self.logger.warning(f"Usuario {user_data.get('username')} sin permiso inventory.view")
                return None
            
            return self.product_model.get_product_by_id(product_id)
            
        except Exception as e:
            self.logger.error(f"Error en get_product_by_id: {e}")
            return None
    
    def update_product(self, product_id: int, product_data: Dict[str, Any], 
                      user_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Actualizar producto"""
        try:
            # Verificar permisos
            if not self.permission_service.check_permission(user_data, 'inventory.edit'):
                self.logger.warning(f"Usuario {user_data.get('username')} sin permiso inventory.edit")
                return False, "No tienes permiso para editar productos"
            
            # Validar datos
            is_valid, validation_errors = self._validate_product_data(product_data, is_update=True)
            if not is_valid:
                return False, f"Datos inválidos: {', '.join(validation_errors)}"
            
            # Verificar SKU único (si se está cambiando)
            if 'sku' in product_data:
                current_product = self.product_model.get_product_by_id(product_id)
                if current_product and current_product['sku'] != product_data['sku']:
                    if self._sku_exists(product_data['sku'], exclude_id=product_id):
                        return False, f"El SKU '{product_data['sku']}' ya existe"
            
            # Actualizar producto
            success = self.product_model.update_product(product_id, product_data)
            
            if success:
                self.logger.info(f"Producto {product_id} actualizado por {user_data.get('username')}")
                return True, "Producto actualizado exitosamente"
            else:
                return False, "Error al actualizar el producto"
                
        except Exception as e:
            self.logger.error(f"Error en update_product: {e}")
            return False, f"Error interno: {str(e)}"
    
    def delete_product(self, product_id: int, user_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Eliminar producto (soft delete)"""
        try:
            # Verificar permisos
            if not self.permission_service.check_permission(user_data, 'inventory.delete'):
                self.logger.warning(f"Usuario {user_data.get('username')} sin permiso inventory.delete")
                return False, "No tienes permiso para eliminar productos"
            
            success = self.product_model.delete_product(product_id)
            
            if success:
                self.logger.info(f"Producto {product_id} eliminado por {user_data.get('username')}")
                return True, "Producto eliminado exitosamente"
            else:
                return False, "Error al eliminar el producto"
                
        except Exception as e:
            self.logger.error(f"Error en delete_product: {e}")
            return False, f"Error interno: {str(e)}"
    
    def search_products(self, search_term: str, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Buscar productos"""
        try:
            # Verificar permisos
            if not self.permission_service.check_permission(user_data, 'inventory.view'):
                return []
            
            return self.product_model.search_products(search_term)
            
        except Exception as e:
            self.logger.error(f"Error en search_products: {e}")
            return []
    
    def update_stock(self, product_id: int, quantity: int, movement_type: str,
                    notes: str, user_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Actualizar stock de producto"""
        try:
            # Verificar permisos
            if not self.permission_service.check_permission(user_data, 'inventory.stock'):
                self.logger.warning(f"Usuario {user_data.get('username')} sin permiso inventory.stock")
                return False, "No tienes permiso para gestionar stock"
            
            success = self.product_model.update_stock(
                product_id, quantity, movement_type, notes, user_data.get('id', 1)
            )
            
            if success:
                action = "incrementado" if quantity > 0 else "decrementado"
                self.logger.info(f"Stock {action} para producto {product_id} por {user_data.get('username')}")
                return True, f"Stock actualizado exitosamente"
            else:
                return False, "Error al actualizar el stock"
                
        except Exception as e:
            self.logger.error(f"Error en update_stock: {e}")
            return False, f"Error interno: {str(e)}"
    
    def update_product_stock(self, sku: str, movement_type: str, quantity: float,
                           user: Dict[str, Any], reason: str = "", 
                           min_stock: float = 0, max_stock: float = 0) -> Tuple[bool, str]:
        """Actualizar stock de producto por SKU con diferentes tipos de movimiento"""
        try:
            # Verificar permisos
            if not self.permission_service.check_permission(user, 'inventory.edit'):
                self.logger.warning(f"Usuario {user.get('username')} sin permiso inventory.edit")
                return False, "No tienes permiso para actualizar stock"
            
            # Mapear tipos de movimiento del español al inglés (base de datos)
            movement_type_map = {
                'entrada': 'purchase',      # Entrada → Purchase
                'salida': 'sale',           # Salida → Sale
                'ajuste': 'adjustment'      # Ajuste → Adjustment
            }
            
            db_movement_type = movement_type_map.get(movement_type, movement_type)
            
            # Obtener producto por SKU
            products = self.product_model.search_products(sku)
            if not products:
                return False, f"Producto con SKU '{sku}' no encontrado"
            
            product = products[0]
            product_id = product['id']
            # Convertir Decimal a float para evitar errores de tipo
            current_stock = float(product['stock_quantity'])
            
            # Calcular nuevo stock según tipo de movimiento
            if movement_type == 'entrada':
                new_stock = current_stock + quantity
                notes = f"Entrada de stock: +{quantity}"
            elif movement_type == 'salida':
                if current_stock < quantity:
                    return False, f"Stock insuficiente. Actual: {current_stock}, Solicitado: {quantity}"
                new_stock = current_stock - quantity
                notes = f"Salida de stock: -{quantity}"
            elif movement_type == 'ajuste':
                new_stock = quantity
                notes = f"Ajuste manual: {current_stock} → {quantity}"
            else:
                return False, f"Tipo de movimiento inválido: {movement_type}"
            
            # Agregar razón si existe
            if reason:
                notes += f" | Motivo: {reason}"
            
            # Actualizar stock en la base de datos (usando tipo mapeado para BD)
            success = self.product_model.update_stock_direct(
                product_id=product_id,
                new_stock=new_stock,
                movement_type=db_movement_type,  # Usar tipo mapeado
                notes=notes,
                user_id=user.get('id', 1),
                min_stock=min_stock,
                max_stock=max_stock
            )
            
            if success:
                self.logger.info(
                    f"Stock actualizado para {sku}: {current_stock} → {new_stock} "
                    f"({movement_type}) por {user.get('username')}"
                )
                return True, f"Stock actualizado: {current_stock} → {new_stock}"
            else:
                return False, "Error al actualizar el stock"
                
        except Exception as e:
            self.logger.error(f"Error en update_product_stock: {e}")
            return False, f"Error interno: {str(e)}"
    
    def save_product_limits(self, sku: str, min_stock: float, max_stock: float,
                          user: Dict[str, Any]) -> Tuple[bool, str]:
        """Guardar límites de stock (mín/máx) sin afectar el stock actual"""
        try:
            print(f"\n🔍 ProductController.save_product_limits llamado")
            print(f"   SKU: {sku}")
            print(f"   Min: {min_stock}, Max: {max_stock}")
            
            # Verificar permisos
            if not self.permission_service.check_permission(user, 'inventory.edit'):
                self.logger.warning(f"Usuario {user.get('username')} sin permiso inventory.edit")
                return False, "No tienes permiso para actualizar límites de stock"
            
            print(f"   ✅ Permisos verificados")
            
            # Obtener producto por SKU
            products = self.product_model.search_products(sku)
            if not products:
                print(f"   ❌ Producto no encontrado")
                return False, f"Producto con SKU '{sku}' no encontrado"
            
            product = products[0]
            product_id = product['id']
            
            print(f"   ✅ Producto encontrado: ID={product_id}")
            
            # Actualizar límites
            success = self.product_model.update_product_limits(
                product_id=product_id,
                min_stock=min_stock,
                max_stock=max_stock
            )
            
            if success:
                self.logger.info(
                    f"Límites actualizados para {sku}: min={min_stock}, max={max_stock} "
                    f"por {user.get('username')}"
                )
                print(f"   ✅ Límites actualizados en BD")
                return True, f"Límites de stock actualizados correctamente"
            else:
                print(f"   ❌ Error al actualizar en BD")
                return False, "Error al actualizar los límites de stock"
                
        except Exception as e:
            self.logger.error(f"Error en save_product_limits: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error interno: {str(e)}"
    
    def get_low_stock_products(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Obtener productos con stock bajo"""
        try:
            # Verificar permisos
            if not self.permission_service.check_permission(user_data, 'inventory.view'):
                return []
            
            return self.product_model.get_low_stock_products()
            
        except Exception as e:
            self.logger.error(f"Error en get_low_stock_products: {e}")
            return []
    
    def get_categories(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Obtener categorías"""
        try:
            if not self.permission_service.check_permission(user_data, 'inventory.view'):
                return []
            cached = self._categories_cache
            if cached and time.time() - cached[0] < self._cache_ttl:
                return cached[1]

            categories = self.product_model.get_categories()
            self._categories_cache = (time.time(), categories)
            return categories

        except Exception as e:
            self.logger.error(f"Error en get_categories: {e}")
            return []
    
    def get_units(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Obtener unidades de medida"""
        try:
            if not self.permission_service.check_permission(user_data, 'inventory.view'):
                return []
            cached = self._units_cache
            if cached and time.time() - cached[0] < self._cache_ttl:
                return cached[1]

            units = self.product_model.get_units()
            self._units_cache = (time.time(), units)
            return units

        except Exception as e:
            self.logger.error(f"Error en get_units: {e}")
            return []

    def invalidate_category_cache(self):
        self._categories_cache = None

    def invalidate_units_cache(self):
        self._units_cache = None
    
    def _validate_product_data(self, data: Dict[str, Any], is_update: bool = False) -> Tuple[bool, List[str]]:
        """Validar datos del producto"""
        errors = []
        
        if not is_update:
            # Campos requeridos para creación
            if not data.get('name') or not data['name'].strip():
                errors.append("El nombre es requerido")
            
            if not data.get('sku') or not data['sku'].strip():
                errors.append("El SKU es requerido")
            
            if not data.get('category_id'):
                errors.append("La categoría es requerida")
            
            if not data.get('price') or float(data['price']) < 0:
                errors.append("El precio debe ser mayor o igual a 0")
            
            if not data.get('cost') or float(data['cost']) < 0:
                errors.append("El costo debe ser mayor o igual a 0")
        else:
            # Validaciones para actualización (solo si el campo está presente)
            if 'name' in data and (not data['name'] or not data['name'].strip()):
                errors.append("El nombre no puede estar vacío")
            
            if 'sku' in data and (not data['sku'] or not data['sku'].strip()):
                errors.append("El SKU no puede estar vacío")
            
            if 'price' in data and float(data['price']) < 0:
                errors.append("El precio debe ser mayor o igual a 0")
            
            if 'cost' in data and float(data['cost']) < 0:
                errors.append("El costo debe ser mayor o igual a 0")
        
        # Validaciones comunes
        if 'stock_quantity' in data and float(data['stock_quantity']) < 0:
            errors.append("El stock no puede ser negativo")
        
        if 'min_stock' in data and float(data['min_stock']) < 0:
            errors.append("El stock mínimo no puede ser negativo")
        
        if 'max_stock' in data and float(data['max_stock']) < 0:
            errors.append("El stock máximo no puede ser negativo")
        
        if 'tax_rate' in data and (float(data['tax_rate']) < 0 or float(data['tax_rate']) > 100):
            errors.append("La tasa de impuesto debe estar entre 0 y 100")
        
        return len(errors) == 0, errors
    
    def _sku_exists(self, sku: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar si un SKU ya existe"""
        try:
            return self.product_model.sku_exists(sku, exclude_id)
        except Exception as exc:
            self.logger.error(f"Error verificando SKU '{sku}': {exc}")
            return False
