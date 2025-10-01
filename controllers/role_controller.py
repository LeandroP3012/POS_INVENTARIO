"""
Controlador para gestión de roles y permisos
"""

import os
import sys
import logging
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.role_model import RoleModel

class RoleController:
    """Controlador para gestión de roles y permisos"""
    
    def __init__(self):
        self.role_model = RoleModel()
        self.logger = logging.getLogger(f'controller.{self.__class__.__name__}')
    
    def get_all_roles(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Obtener todos los roles"""
        try:
            self.logger.info(f"Obteniendo todos los roles (incluir inactivos: {include_inactive})")
            roles = self.role_model.get_all_roles(include_inactive)
            
            # Enriquecer con información adicional
            for role in roles:
                role['users_count'] = self._get_role_users_count(role['id'])
                role['can_edit'] = not (role.get('system_role', False) and role.get('code') == 'super_admin')
                role['can_delete'] = not role.get('system_role', False)
            
            self.logger.info(f"Se obtuvieron {len(roles)} roles")
            return roles
            
        except Exception as e:
            self.logger.error(f"Error obteniendo roles: {e}")
            return []
    
    def get_role_by_id(self, role_id: int) -> Optional[Dict[str, Any]]:
        """Obtener rol por ID"""
        try:
            self.logger.info(f"Obteniendo rol por ID: {role_id}")
            role = self.role_model.get_role_by_id(role_id)
            
            if role:
                role['users_count'] = self._get_role_users_count(role['id'])
                role['can_edit'] = not (role.get('system_role', False) and role.get('code') == 'super_admin')
                role['can_delete'] = not role.get('system_role', False)
            
            return role
            
        except Exception as e:
            self.logger.error(f"Error obteniendo rol {role_id}: {e}")
            return None
    
    def create_role(self, role_data: Dict[str, Any], current_user: Dict[str, Any] = None) -> Tuple[bool, str, Optional[int]]:
        """Crear nuevo rol"""
        try:
            print(f"DEBUG CREATE_ROLE - Datos recibidos: {role_data}")
            self.logger.info(f"Creando nuevo rol: {role_data.get('name')}")
            
            # Verificar permisos del usuario
            print(f"DEBUG CREATE_ROLE - Verificando permisos...")
            if not self._check_permission(current_user, 'roles.create'):
                print("DEBUG CREATE_ROLE - Sin permisos para crear roles")
                return False, "No tienes permisos para crear roles", None
            
            print("DEBUG CREATE_ROLE - Permisos verificados")
            
            # Validar datos
            print("DEBUG CREATE_ROLE - Validando datos...")
            is_valid, errors = self.role_model.validate_role_data(role_data)
            print(f"DEBUG CREATE_ROLE - Validación: válido={is_valid}, errores={errors}")
            
            if not is_valid:
                error_msg = "Errores de validación: " + ", ".join(errors)
                self.logger.warning(f"Validación fallida para crear rol: {error_msg}")
                return False, error_msg, None
            
            # Crear rol
            print("DEBUG CREATE_ROLE - Llamando a role_model.create_role()")
            role_id = self.role_model.create_role(role_data)
            print(f"DEBUG CREATE_ROLE - Resultado de create_role: {role_id}")
            
            if role_id:
                success_msg = f"Rol '{role_data.get('name')}' creado exitosamente"
                self.logger.info(success_msg)
                print(f"DEBUG CREATE_ROLE - Éxito: {success_msg}")
                return True, success_msg, role_id
            else:
                error_msg = "Error interno al crear el rol"
                self.logger.error(error_msg)
                print(f"DEBUG CREATE_ROLE - Error: {error_msg}")
                return False, error_msg, None
                
        except Exception as e:
            error_msg = f"Error creando rol: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg, None
    
    def update_role(self, role_id: int, role_data: Dict[str, Any], current_user: Dict[str, Any] = None) -> Tuple[bool, str]:
        """Actualizar rol existente"""
        try:
            self.logger.info(f"Actualizando rol ID: {role_id}")
            
            # Verificar permisos del usuario
            if not self._check_permission(current_user, 'roles.edit'):
                return False, "No tienes permisos para editar roles"
            
            # Verificar que el rol existe
            existing_role = self.role_model.get_role_by_id(role_id)
            if not existing_role:
                return False, f"El rol con ID {role_id} no existe"
            
            # Verificar si se puede editar
            if existing_role.get('system_role', False) and existing_role.get('code') == 'super_admin':
                return False, "No se puede editar el rol Super Admin"
            
            # Validar datos
            is_valid, errors = self.role_model.validate_role_data(role_data, is_update=True)
            if not is_valid:
                error_msg = "Errores de validación: " + ", ".join(errors)
                self.logger.warning(f"Validación fallida para actualizar rol: {error_msg}")
                return False, error_msg
            
            # Actualizar rol
            success = self.role_model.update_role(role_id, role_data)
            
            if success:
                success_msg = f"Rol actualizado exitosamente"
                self.logger.info(success_msg)
                return True, success_msg
            else:
                error_msg = "Error interno al actualizar el rol"
                self.logger.error(error_msg)
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Error actualizando rol: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def delete_role(self, role_id: int, current_user: Dict[str, Any] = None) -> Tuple[bool, str]:
        """Eliminar rol"""
        try:
            self.logger.info(f"Eliminando rol ID: {role_id}")
            
            # Verificar permisos del usuario
            if not self._check_permission(current_user, 'roles.delete'):
                return False, "No tienes permisos para eliminar roles"
            
            # Verificar que el rol existe
            existing_role = self.role_model.get_role_by_id(role_id)
            if not existing_role:
                return False, f"El rol con ID {role_id} no existe"
            
            # Verificar si se puede eliminar
            if existing_role.get('system_role', False):
                return False, f"No se puede eliminar el rol del sistema: {existing_role.get('name')}"
            
            # Verificar que no tenga usuarios asignados
            users_count = self._get_role_users_count(role_id)
            if users_count > 0:
                return False, f"No se puede eliminar el rol porque tiene {users_count} usuario(s) asignado(s)"
            
            # Eliminar rol
            success = self.role_model.delete_role(role_id)
            
            if success:
                success_msg = f"Rol '{existing_role.get('name')}' eliminado exitosamente"
                self.logger.info(success_msg)
                return True, success_msg
            else:
                error_msg = "Error interno al eliminar el rol"
                self.logger.error(error_msg)
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Error eliminando rol: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def activate_role(self, role_id: int, current_user: Dict[str, Any] = None) -> Tuple[bool, str]:
        """Activar rol"""
        try:
            self.logger.info(f"Activando rol ID: {role_id}")
            
            if not self._check_permission(current_user, 'roles.edit'):
                return False, "No tienes permisos para activar roles"
            
            success = self.role_model.activate_role(role_id)
            
            if success:
                return True, "Rol activado exitosamente"
            else:
                return False, "Error activando el rol"
                
        except Exception as e:
            self.logger.error(f"Error activando rol {role_id}: {e}")
            return False, f"Error activando rol: {str(e)}"
    
    def deactivate_role(self, role_id: int, current_user: Dict[str, Any] = None) -> Tuple[bool, str]:
        """Desactivar rol"""
        try:
            self.logger.info(f"Desactivando rol ID: {role_id}")
            
            if not self._check_permission(current_user, 'roles.edit'):
                return False, "No tienes permisos para desactivar roles"
            
            # Verificar que no sea un rol crítico
            role = self.role_model.get_role_by_id(role_id)
            if role and role.get('code') in ['super_admin', 'admin']:
                return False, f"No se puede desactivar el rol crítico: {role.get('name')}"
            
            success = self.role_model.deactivate_role(role_id)
            
            if success:
                return True, "Rol desactivado exitosamente"
            else:
                return False, "Error desactivando el rol"
                
        except Exception as e:
            self.logger.error(f"Error desactivando rol {role_id}: {e}")
            return False, f"Error desactivando rol: {str(e)}"
    
    def get_all_permissions(self) -> List[str]:
        """Obtener todos los permisos disponibles"""
        try:
            return self.role_model.get_all_available_permissions()
        except Exception as e:
            self.logger.error(f"Error obteniendo permisos: {e}")
            return []
    
    def get_permissions_by_category(self) -> Dict[str, List[str]]:
        """Obtener permisos organizados por categoría"""
        try:
            return self.role_model.get_permissions_by_category()
        except Exception as e:
            self.logger.error(f"Error obteniendo permisos por categoría: {e}")
            return {}
    
    def check_role_permission(self, role_id: int, permission: str) -> bool:
        """Verificar si un rol tiene un permiso específico"""
        try:
            return self.role_model.role_has_permission(role_id, permission)
        except Exception as e:
            self.logger.error(f"Error verificando permiso {permission} para rol {role_id}: {e}")
            return False
    
    def get_role_permissions(self, role_id: int) -> List[str]:
        """Obtener todos los permisos de un rol"""
        try:
            return self.role_model.get_role_permissions(role_id)
        except Exception as e:
            self.logger.error(f"Error obteniendo permisos del rol {role_id}: {e}")
            return []
    
    def get_roles_for_assignment(self) -> List[Dict[str, Any]]:
        """Obtener roles disponibles para asignar a usuarios"""
        try:
            roles = self.get_all_roles(include_inactive=False)
            
            # Filtrar roles que se pueden asignar
            assignable_roles = []
            for role in roles:
                if role.get('active', True):
                    assignable_roles.append({
                        'id': role['id'],
                        'name': role['name'],
                        'code': role['code'],
                        'description': role.get('description', ''),
                        'system_role': role.get('system_role', False)
                    })
            
            return assignable_roles
            
        except Exception as e:
            self.logger.error(f"Error obteniendo roles para asignación: {e}")
            return []
    
    def get_roles_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de roles"""
        try:
            return self.role_model.get_roles_stats()
        except Exception as e:
            self.logger.error(f"Error obteniendo estadísticas de roles: {e}")
            return {
                'total_roles': 0,
                'active_roles': 0,
                'inactive_roles': 0,
                'system_roles': 0,
                'custom_roles': 0
            }
    
    def search_roles(self, query: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Buscar roles por query y filtros"""
        try:
            all_roles = self.get_all_roles(include_inactive=True)
            
            # Aplicar búsqueda por texto
            if query:
                query = query.lower().strip()
                filtered_roles = []
                
                for role in all_roles:
                    if (query in role.get('name', '').lower() or 
                        query in role.get('code', '').lower() or 
                        query in role.get('description', '').lower()):
                        filtered_roles.append(role)
                
                all_roles = filtered_roles
            
            # Aplicar filtros
            if filters:
                # Filtro por estado
                if 'active' in filters and filters['active'] is not None:
                    all_roles = [r for r in all_roles if r.get('active', True) == filters['active']]
                
                # Filtro por tipo de rol
                if 'system_role' in filters and filters['system_role'] is not None:
                    all_roles = [r for r in all_roles if r.get('system_role', False) == filters['system_role']]
            
            return all_roles
            
        except Exception as e:
            self.logger .error(f"Error buscando roles: {e}")
            return []
    
    def validate_permissions(self, permissions: List[str]) -> Tuple[bool, List[str]]:
        """Validar que una lista de permisos sea válida"""
        try:
            available_permissions = self.get_all_permissions() + ['*']
            invalid_permissions = []
            
            for perm in permissions:
                if perm not in available_permissions:
                    invalid_permissions.append(perm)
            
            if invalid_permissions:
                return False, invalid_permissions
            
            return True, []
            
        except Exception as e:
            self.logger.error(f"Error validando permisos: {e}")
            return False, ["Error interno validando permisos"]
    
    def _check_permission(self, user: Dict[str, Any], permission: str) -> bool:
        """Verificar si el usuario tiene un permiso específico"""
        try:
            if not user:
                return False
            
            # Super admin tiene todos los permisos
            user_permissions = user.get('permissions', {})
            if user_permissions.get('super_admin') or user_permissions.get('all_modules'):
                return True
            
            # Verificar permiso específico
            if user_permissions.get(permission.replace('.', '_')):
                return True
            
            # Verificar por rol si existe
            role_id = user.get('role_id')
            if role_id:
                return self.check_role_permission(role_id, permission)
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error verificando permiso {permission}: {e}")
            return False
    
    def _get_role_users_count(self, role_id: int) -> int:
        """Obtener cantidad de usuarios que tienen este rol"""
        try:
            # Importar aquí para evitar circular imports
            from models.user_model import UserModel
            user_model = UserModel()
            
            # Contar usuarios con este rol
            return user_model.count({'role_id': role_id})
            
        except Exception as e:
            self.logger.error(f"Error contando usuarios del rol {role_id}: {e}")
            return 0
    
    def export_roles_data(self) -> List[Dict[str, Any]]:
        """Exportar datos de roles para backup o migración"""
        try:
            roles = self.get_all_roles(include_inactive=True)
            
            # Limpiar datos para exportación
            export_data = []
            for role in roles:
                export_role = {
                    'name': role.get('name'),
                    'code': role.get('code'),
                    'description': role.get('description'),
                    'permissions': role.get('permissions', []),
                    'active': role.get('active', True),
                    'system_role': role.get('system_role', False)
                }
                export_data.append(export_role)
            
            return export_data
            
        except Exception as e:
            self.logger.error(f"Error exportando datos de roles: {e}")
            return []
    
    def get_permission_description(self, permission: str) -> str:
        """Obtener descripción amigable de un permiso"""
        descriptions = {
            # Usuarios
            'users.view': 'Ver lista de usuarios',
            'users.create': 'Crear nuevos usuarios',
            'users.edit': 'Editar usuarios existentes',
            'users.delete': 'Eliminar usuarios',
            'users.activate': 'Activar usuarios',
            'users.deactivate': 'Desactivar usuarios',
            'users.export': 'Exportar datos de usuarios',
            
            # Roles
            'roles.view': 'Ver lista de roles',
            'roles.create': 'Crear nuevos roles',
            'roles.edit': 'Editar roles existentes',
            'roles.delete': 'Eliminar roles',
            'roles.assign': 'Asignar roles a usuarios',
            'roles.permissions': 'Gestionar permisos de roles',
            
            # Sistema
            'system.config': 'Configurar sistema',
            'system.backup': 'Crear respaldos',
            'system.restore': 'Restaurar sistema',
            'system.logs': 'Ver logs del sistema',
            'system.maintenance': 'Modo mantenimiento',
            'system.reports': 'Reportes del sistema',
            
            # Dashboard
            'dashboard.view': 'Ver dashboard principal',
            'dashboard.stats': 'Ver estadísticas',
            'dashboard.analytics': 'Ver análisis avanzados',
            
            # Inventario
            'inventory.view': 'Ver inventario',
            'inventory.create': 'Agregar productos al inventario',
            'inventory.edit': 'Editar productos del inventario',
            'inventory.delete': 'Eliminar productos del inventario',
            'inventory.stock': 'Gestionar stock',
            'inventory.reports': 'Reportes de inventario',
            'inventory.export': 'Exportar inventario',
            
            # Ventas
            'sales.view': 'Ver todas las ventas',
            'sales.create': 'Realizar ventas',
            'sales.edit': 'Editar ventas',
            'sales.delete': 'Eliminar ventas',
            'sales.view_own': 'Ver solo sus propias ventas',
            'sales.reports': 'Reportes de ventas',
            'sales.export': 'Exportar datos de ventas',
            
            # Caja
            'cash.register': 'Operar caja registradora',
            'cash.open': 'Abrir caja',
            'cash.close': 'Cerrar caja',
            'cash.reports': 'Reportes de caja',
            
            # Productos
            'products.view': 'Ver catálogo de productos',
            'products.create': 'Crear nuevos productos',
            'products.edit': 'Editar productos',
            'products.delete': 'Eliminar productos',
            'products.prices': 'Gestionar precios',
            'products.categories': 'Gestionar categorías',
            
            # Clientes
            'customers.view': 'Ver lista de clientes',
            'customers.create': 'Crear nuevos clientes',
            'customers.edit': 'Editar clientes',
            'customers.delete': 'Eliminar clientes',
            'customers.export': 'Exportar datos de clientes',
            
            # Proveedores
            'suppliers.view': 'Ver lista de proveedores',
            'suppliers.create': 'Crear nuevos proveedores',
            'suppliers.edit': 'Editar proveedores',
            'suppliers.delete': 'Eliminar proveedores',
            
            # Reportes
            'reports.sales': 'Reportes de ventas',
            'reports.inventory': 'Reportes de inventario',
            'reports.users': 'Reportes de usuarios',
            'reports.financial': 'Reportes financieros',
            'reports.export': 'Exportar reportes'
        }
        
        return descriptions.get(permission, permission)
