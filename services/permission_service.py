"""
Servicio centralizado para gestión de permisos
Este servicio maneja toda la lógica de verificación de permisos en tiempo real
"""

import os
import sys
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user_model import UserModel
from models.role_model import RoleModel

class PermissionService:
    """Servicio para gestión centralizada de permisos"""
    
    def __init__(self):
        self.user_model = UserModel()
        self.role_model = RoleModel()
        self.logger = logging.getLogger(f'service.{self.__class__.__name__}')
        
        # Cache para permisos (mejora performance)
        self._permissions_cache = {}
        self._cache_timeout = 300  # 5 minutos
    
    def check_permission(self, user: Dict[str, Any], permission: str) -> bool:
        """
        Verificar si un usuario tiene un permiso específico
        
        Args:
            user: Diccionario con datos del usuario
            permission: Permiso a verificar (ej: 'users.create')
            
        Returns:
            True si tiene el permiso, False si no
        """
        try:
            if not user:
                return False
            
            user_id = user.get('id')
            if not user_id:
                return False
            
            # Verificar caché primero
            cache_key = f"{user_id}_{permission}"
            if self._is_cache_valid(cache_key):
                return self._permissions_cache[cache_key]['result']
            
            # Verificar permisos del usuario
            has_permission = self._check_user_permission_detailed(user, permission)
            
            # Guardar en caché
            self._cache_permission(cache_key, has_permission)
            
            return has_permission
            
        except Exception as e:
            self.logger.error(f"Error verificando permiso {permission}: {e}")
            return False
    
    def _check_user_permission_detailed(self, user: Dict[str, Any], permission: str) -> bool:
        """Verificación detallada de permisos - SOLO permisos explícitamente asignados"""
        try:
            # 1. Verificar permisos específicos del usuario (tienen prioridad)
            user_permissions = user.get('permissions', {})
            if isinstance(user_permissions, dict):
                # Convertir formato anterior a nuevo formato
                permission_key = permission.replace('.', '_')
                if user_permissions.get(permission_key):
                    return True
                
                # Super admin o all_modules
                if user_permissions.get('super_admin') or user_permissions.get('all_modules'):
                    return True
            
            # 2. Verificar permisos por rol (PRIORIDAD PRINCIPAL)
            role_id = user.get('role_id')
            if role_id:
                has_role_permission = self.role_model.role_has_permission(role_id, permission)
                if has_role_permission:
                    return True
                # Si tiene role_id, NO continuar con fallback legacy
                # Los roles personalizados solo deben tener permisos explícitamente asignados
                return False
            
            # 3. Fallback: verificar por user_type (solo para roles del sistema sin role_id)
            user_type = user.get('user_type', 'user')
            
            # Si user_type es 'user' pero no tiene role_id, NO dar permisos por defecto
            if user_type == 'user':
                return False
            
            return self._check_legacy_permission(user_type, permission)
            
        except Exception as e:
            self.logger.error(f"Error en verificación detallada de permiso {permission}: {e}")
            return False
    
    def _check_legacy_permission(self, user_type: str, permission: str) -> bool:
        """Verificación de permisos por user_type legacy - SOLO roles del sistema"""
        # SOLO asignar permisos por defecto a roles específicos del sistema
        # Los roles personalizados (user_type='user') NO deben tener permisos automáticos
        legacy_permissions = {
            'admin': [
                'users.view', 'users.create', 'users.edit', 'users.delete',
                'roles.view', 'roles.create', 'roles.edit', 'roles.delete',
                'system.config', 'system.backup', 'system.reports',
                'inventory.view', 'inventory.edit', 'inventory.reports',
                'sales.view', 'sales.create', 'sales.reports',
                'dashboard.view', 'dashboard.stats'
            ],
            'supervisor': [
                'users.view',
                'inventory.view', 'inventory.reports',
                'sales.view', 'sales.create', 'sales.reports',
                'dashboard.view', 'dashboard.stats'
            ],
            'manager': [
                'users.view',
                'inventory.view', 'inventory.reports',
                'sales.view', 'sales.create', 'sales.reports',
                'dashboard.view', 'dashboard.stats'
            ],
            'employee': [
                'sales.create', 'sales.view_own',
                'inventory.view',
                'dashboard.view'
            ],
            'cashier': [
                'sales.create', 'sales.view_own',
                'cash.register',
                'dashboard.view'
            ]
            # NOTA: 'user' NO está incluido intencionalmente
            # Los usuarios con user_type='user' solo deben tener permisos
            # que estén explícitamente asignados a través de role_id
        }
        
        # Super admin legacy
        if user_type == 'admin':
            return True
        
        # Para todos los otros tipos, verificar permisos específicos
        allowed_permissions = legacy_permissions.get(user_type, [])
        return permission in allowed_permissions
    
    def get_user_permissions(self, user: Dict[str, Any]) -> List[str]:
        """Obtener todos los permisos de un usuario"""
        try:
            if not user:
                return []
            
            permissions = set()
            
            # 1. Permisos específicos del usuario
            user_permissions = user.get('permissions', {})
            if isinstance(user_permissions, dict):
                if user_permissions.get('super_admin') or user_permissions.get('all_modules'):
                    return ['*']  # Todos los permisos
                
                # Agregar permisos específicos
                for perm, granted in user_permissions.items():
                    if granted:
                        # Convertir formato anterior a nuevo
                        if '_' in perm:
                            perm = perm.replace('_', '.')
                        permissions.add(perm)
            
            # 2. Permisos del rol
            role_id = user.get('role_id')
            if role_id:
                role_permissions = self.role_model.get_role_permissions(role_id)
                permissions.update(role_permissions)
            
            # 3. Fallback: permisos por user_type (solo para roles del sistema)
            if not permissions:
                user_type = user.get('user_type', 'user')
                
                # Si user_type es 'user' y no tiene role_id, NO asignar permisos por defecto
                if user_type == 'user' and not role_id:
                    # Los roles personalizados solo deben tener permisos explícitamente asignados
                    return []
                
                legacy_permissions = self._get_legacy_permissions(user_type)
                permissions.update(legacy_permissions)
            
            return list(permissions)
            
        except Exception as e:
            self.logger.error(f"Error obteniendo permisos del usuario: {e}")
            return []
    
    def _get_legacy_permissions(self, user_type: str) -> List[str]:
        """Obtener permisos legacy por user_type - SOLO roles del sistema"""
        # SOLO asignar permisos por defecto a roles específicos del sistema
        legacy_permissions = {
            'admin': ['*'],
            'supervisor': [
                'users.view', 'inventory.view', 'inventory.reports',
                'sales.view', 'sales.create', 'sales.reports',
                'dashboard.view', 'dashboard.stats'
            ],
            'manager': [
                'users.view', 'inventory.view', 'inventory.reports',
                'sales.view', 'sales.create', 'sales.reports',
                'dashboard.view', 'dashboard.stats'
            ],
            'employee': [
                'sales.create', 'sales.view_own', 'inventory.view', 'dashboard.view'
            ],
            'cashier': [
                'sales.create', 'sales.view_own', 'cash.register', 'dashboard.view'
            ]
            # NOTA: 'user' NO está incluido intencionalmente
            # Los usuarios con user_type='user' (roles personalizados) solo deben
            # tener permisos que estén explícitamente asignados a través de role_id
        }
        
        return legacy_permissions.get(user_type, [])
    
    def check_multiple_permissions(self, user: Dict[str, Any], permissions: List[str], require_all: bool = False) -> bool:
        """
        Verificar múltiples permisos
        
        Args:
            user: Usuario a verificar
            permissions: Lista de permisos
            require_all: Si True, requiere todos los permisos. Si False, requiere al menos uno
            
        Returns:
            True si cumple la condición, False si no
        """
        try:
            if not permissions:
                return True
            
            results = [self.check_permission(user, perm) for perm in permissions]
            
            if require_all:
                return all(results)
            else:
                return any(results)
                
        except Exception as e:
            self.logger.error(f"Error verificando múltiples permisos: {e}")
            return False
    
    def can_access_module(self, user: Dict[str, Any], module: str) -> bool:
        """Verificar si el usuario puede acceder a un módulo completo"""
        module_permissions = {
            'users': ['users.view', 'users.create', 'users.edit', 'users.delete'],
            'roles': ['roles.view', 'roles.create', 'roles.edit', 'roles.delete'],
            'system': ['system.config', 'system.backup', 'system.reports'],
            'inventory': ['inventory.view', 'inventory.create', 'inventory.edit'],
            'sales': ['sales.view', 'sales.create', 'sales.edit'],
            'dashboard': ['dashboard.view', 'dashboard.stats'],
            'reports': ['reports.sales', 'reports.inventory', 'reports.users']
        }
        
        permissions = module_permissions.get(module, [])
        return self.check_multiple_permissions(user, permissions, require_all=False)
    
    def get_accessible_modules(self, user: Dict[str, Any]) -> List[str]:
        """Obtener lista de módulos accesibles para el usuario"""
        modules = ['users', 'roles', 'system', 'inventory', 'sales', 'dashboard', 'reports']
        accessible = []
        
        for module in modules:
            if self.can_access_module(user, module):
                accessible.append(module)
        
        return accessible
    
    def clear_user_cache(self, user_id: int):
        """Limpiar caché de permisos para un usuario específico"""
        try:
            keys_to_remove = [key for key in self._permissions_cache.keys() 
                            if key.startswith(f"{user_id}_")]
            
            for key in keys_to_remove:
                del self._permissions_cache[key]
            
            self.logger.info(f"Caché de permisos limpiado para usuario {user_id}")
            
        except Exception as e:
            self.logger.error(f"Error limpiando caché de usuario {user_id}: {e}")
    
    def clear_all_cache(self):
        """Limpiar todo el caché de permisos"""
        self._permissions_cache.clear()
        self.logger.info("Caché de permisos completamente limpiado")
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Verificar si el caché es válido"""
        if cache_key not in self._permissions_cache:
            return False
        
        cache_time = self._permissions_cache[cache_key]['timestamp']
        return (datetime.now() - cache_time).seconds < self._cache_timeout
    
    def _cache_permission(self, cache_key: str, result: bool):
        """Guardar resultado en caché"""
        self._permissions_cache[cache_key] = {
            'result': result,
            'timestamp': datetime.now()
        }
    
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
            
            # Roles
            'roles.view': 'Ver lista de roles',
            'roles.create': 'Crear nuevos roles',
            'roles.edit': 'Editar roles existentes',
            'roles.delete': 'Eliminar roles',
            'roles.assign': 'Asignar roles a usuarios',
            
            # Sistema
            'system.config': 'Configurar sistema',
            'system.backup': 'Crear respaldos',
            'system.reports': 'Reportes del sistema',
            
            # Dashboard
            'dashboard.view': 'Ver dashboard principal',
            'dashboard.stats': 'Ver estadísticas',
            
            # Inventario
            'inventory.view': 'Ver inventario',
            'inventory.create': 'Agregar productos',
            'inventory.edit': 'Editar productos',
            'inventory.reports': 'Reportes de inventario',
            
            # Ventas
            'sales.view': 'Ver todas las ventas',
            'sales.create': 'Realizar ventas',
            'sales.edit': 'Editar ventas',
            'sales.view_own': 'Ver solo sus propias ventas',
            'sales.reports': 'Reportes de ventas',
            
            # Caja
            'cash.register': 'Operar caja registradora',
            'cash.open': 'Abrir caja',
            'cash.close': 'Cerrar caja'
        }
        
        return descriptions.get(permission, permission)
    
    def validate_permission_format(self, permission: str) -> bool:
        """Validar que un permiso tenga el formato correcto"""
        if not permission or not isinstance(permission, str):
            return False
        
        # Super admin
        if permission == '*':
            return True
        
        # Formato module.action
        parts = permission.split('.')
        if len(parts) != 2:
            return False
        
        module, action = parts
        if not module or not action:
            return False
        
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del servicio de permisos"""
        return {
            'cache_size': len(self._permissions_cache),
            'cache_timeout': self._cache_timeout,
            'total_permissions': len(self.role_model.get_all_available_permissions()),
            'service_status': 'active'
        }
