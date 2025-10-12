"""
Controlador de Categorías
Maneja la lógica de negocio de categorías
"""

from typing import Dict, Any, List, Optional, Tuple
from models.category_model import CategoryModel
from services.permission_service import PermissionService
import logging


class CategoryController:
    """Controlador para gestión de categorías"""
    
    def __init__(self):
        self.category_model = CategoryModel()
        self.permission_service = PermissionService()
        self.logger = logging.getLogger('controller.CategoryController')
    
    def create_category(self, category_data: Dict[str, Any], user_data: Dict[str, Any]) -> Tuple[bool, str, Optional[int]]:
        """
        Crear nueva categoría
        
        Returns:
            (success, message, category_id)
        """
        try:
            # Verificar permisos
            if not self.permission_service.check_permission(user_data, 'inventory.create'):
                self.logger.warning(f"Usuario {user_data.get('username')} sin permiso inventory.create")
                return False, "No tienes permiso para crear categorías", None
            
            # Validar datos
            if not category_data.get('name') or not category_data['name'].strip():
                return False, "El nombre de la categoría es requerido", None
            
            # Crear categoría
            category_id = self.category_model.create_category(category_data)
            
            if category_id:
                self.logger.info(f"Categoría creada por {user_data.get('username')}: {category_data['name']}")
                return True, "Categoría creada exitosamente", category_id
            else:
                return False, "Error al crear la categoría", None
                
        except Exception as e:
            self.logger.error(f"Error en create_category: {e}")
            return False, f"Error interno: {str(e)}", None
    
    def get_all_categories(self, user_data: Dict[str, Any], include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Obtener todas las categorías"""
        try:
            # Verificar permisos
            if not self.permission_service.check_permission(user_data, 'inventory.view'):
                self.logger.warning(f"Usuario {user_data.get('username')} sin permiso inventory.view")
                return []
            
            return self.category_model.get_all_categories(include_inactive)
            
        except Exception as e:
            self.logger.error(f"Error en get_all_categories: {e}")
            return []
    
    def get_category_by_id(self, category_id: int, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Obtener categoría por ID"""
        try:
            # Verificar permisos
            if not self.permission_service.check_permission(user_data, 'inventory.view'):
                return None
            
            return self.category_model.get_category_by_id(category_id)
            
        except Exception as e:
            self.logger.error(f"Error en get_category_by_id: {e}")
            return None
    
    def update_category(self, category_id: int, category_data: Dict[str, Any], 
                       user_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Actualizar categoría"""
        try:
            # Verificar permisos
            if not self.permission_service.check_permission(user_data, 'inventory.edit'):
                self.logger.warning(f"Usuario {user_data.get('username')} sin permiso inventory.edit")
                return False, "No tienes permiso para editar categorías"
            
            # Validar si hay nombre
            if 'name' in category_data and not category_data['name'].strip():
                return False, "El nombre no puede estar vacío"
            
            # Actualizar
            success = self.category_model.update_category(category_id, category_data)
            
            if success:
                self.logger.info(f"Categoría {category_id} actualizada por {user_data.get('username')}")
                return True, "Categoría actualizada exitosamente"
            else:
                return False, "Error al actualizar la categoría"
                
        except Exception as e:
            self.logger.error(f"Error en update_category: {e}")
            return False, f"Error interno: {str(e)}"
    
    def delete_category(self, category_id: int, user_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Eliminar categoría"""
        try:
            # Verificar permisos
            if not self.permission_service.check_permission(user_data, 'inventory.delete'):
                self.logger.warning(f"Usuario {user_data.get('username')} sin permiso inventory.delete")
                return False, "No tienes permiso para eliminar categorías"
            
            # Verificar si tiene productos
            category = self.category_model.get_category_by_id(category_id)
            if category and category.get('product_count', 0) > 0:
                return False, f"No se puede eliminar: la categoría tiene {category['product_count']} productos asociados"
            
            # Eliminar
            success = self.category_model.delete_category(category_id)
            
            if success:
                self.logger.info(f"Categoría {category_id} eliminada por {user_data.get('username')}")
                return True, "Categoría eliminada exitosamente"
            else:
                return False, "Error al eliminar la categoría"
                
        except Exception as e:
            self.logger.error(f"Error en delete_category: {e}")
            return False, f"Error interno: {str(e)}"
    
    def search_categories(self, search_term: str, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Buscar categorías"""
        try:
            # Verificar permisos
            if not self.permission_service.check_permission(user_data, 'inventory.view'):
                return []
            
            return self.category_model.search_categories(search_term)
            
        except Exception as e:
            self.logger.error(f"Error en search_categories: {e}")
            return []
