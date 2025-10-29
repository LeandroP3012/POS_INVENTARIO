"""
Modelo para gestión de roles del sistema
"""

import os
import sys
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.base_model import BaseModel

class RoleModel(BaseModel):
    """Modelo para gestión de roles"""
    
    def __init__(self):
        super().__init__()
        self.table_name = 'roles'
        
        # Roles por defecto del sistema
        self.default_roles = [
            {
                'id': 1,
                'name': 'Super Admin',
                'code': 'super_admin',
                'description': 'Acceso completo al sistema, puede gestionar todo',
                'system_role': True,
                'active': True,
                'permissions': ['*'],  # Todos los permisos
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'id': 2,
                'name': 'Administrador',
                'code': 'admin',
                'description': 'Administrador del sistema con acceso a la mayoría de funciones',
                'system_role': True,
                'active': True,
                'permissions': [
                    'users.view', 'users.create', 'users.edit', 'users.delete',
                    'roles.view', 'roles.create', 'roles.edit',
                    'system.config', 'system.backup', 'system.reports',
                    'inventory.view', 'inventory.edit', 'inventory.reports',
                    'sales.view', 'sales.create', 'sales.reports',
                    'dashboard.view'
                ],
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'id': 3,
                'name': 'Gerente',
                'code': 'manager',
                'description': 'Gerente de tienda con acceso a reportes y supervisión',
                'system_role': True,
                'active': True,
                'permissions': [
                    'users.view',
                    'inventory.view', 'inventory.reports',
                    'sales.view', 'sales.create', 'sales.reports',
                    'dashboard.view', 'dashboard.stats'
                ],
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'id': 4,
                'name': 'Empleado',
                'code': 'employee',
                'description': 'Empleado con acceso básico para ventas',
                'system_role': True,
                'active': True,
                'permissions': [
                    'sales.view', 'sales.create',
                    'inventory.view',
                    'dashboard.view'
                ],
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'id': 5,
                'name': 'Cajero',
                'code': 'cashier',
                'description': 'Cajero con acceso solo a ventas y caja',
                'system_role': True,
                'active': True,
                'permissions': [
                    'sales.create', 'sales.view_own',
                    'cash.register'
                ],
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        ]
    
    def get_all_roles(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Obtener todos los roles"""
        try:
            if self.db and self.connect():
                conditions = {} if include_inactive else {'active': True}
                roles = self.find_all(conditions)
                
                # Procesar permisos (convertir de JSON string a lista si es necesario)
                for role in roles:
                    if isinstance(role.get('permissions'), str):
                        import json
                        try:
                            role['permissions'] = json.loads(role['permissions'])
                        except:
                            role['permissions'] = []
                
                return roles
            else:
                # Fallback a roles por defecto
                if include_inactive:
                    return self.default_roles
                else:
                    return [role for role in self.default_roles if role.get('active', True)]
                    
        except Exception as e:
            self.logger.error(f"Error obteniendo roles: {e}")
            return [role for role in self.default_roles if include_inactive or role.get('active', True)]
    
    def get_role_by_id(self, role_id: int) -> Optional[Dict[str, Any]]:
        """Obtener rol por ID"""
        try:
            if self.db and self.connect():
                role = self.find_by_id(role_id)
                
                if role:
                    if isinstance(role.get('permissions'), str):
                        import json
                        try:
                            role['permissions'] = json.loads(role['permissions'])
                        except:
                            role['permissions'] = []
                    
                    return role
                
            # Buscar en roles por defecto
            for default_role in self.default_roles:
                if default_role['id'] == role_id:
                    return default_role.copy()
            
            return None
                
        except Exception as e:
            self.logger.error(f"Error obteniendo rol {role_id}: {e}")
            # Buscar en roles por defecto
            for role in self.default_roles:
                if role['id'] == role_id:
                    return role.copy()
            return None
    
    def get_role_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """Obtener rol por código"""
        try:
            if self.db and self.connect():
                role = self.find_by_field('code', code)
                
                if role and isinstance(role.get('permissions'), str):
                    import json
                    try:
                        role['permissions'] = json.loads(role['permissions'])
                    except:
                        role['permissions'] = []
                
                return role
            else:
                # Buscar en roles por defecto
                for role in self.default_roles:
                    if role['code'] == code:
                        return role.copy()
                return None
                
        except Exception as e:
            self.logger.error(f"Error obteniendo rol por código {code}: {e}")
            # Buscar en roles por defecto
            for role in self.default_roles:
                if role['code'] == code:
                    return role.copy()
            return None
    
    def create_role(self, role_data: Dict[str, Any]) -> Optional[int]:
        """Crear nuevo rol"""
        try:
            print(f"DEBUG ROLE_MODEL - create_role llamado con: {role_data}")
            
            # Validar datos
            print("DEBUG ROLE_MODEL - Validando datos...")
            is_valid, errors = self.validate_role_data(role_data)
            print(f"DEBUG ROLE_MODEL - Validación: válido={is_valid}, errores={errors}")
            
            if not is_valid:
                print(f"DEBUG ROLE_MODEL - Datos inválidos, errores: {errors}")
                self.logger.error(f"Datos de rol inválidos: {errors}")
                return None
            
            # Preparar datos
            print("DEBUG ROLE_MODEL - Preparando datos...")
            role_data = self.sanitize_input(role_data)
            
            # Convertir permisos a JSON si es necesario
            if isinstance(role_data.get('permissions'), list):
                import json
                role_data['permissions'] = json.dumps(role_data['permissions'])
            
            # Establecer valores por defecto
            role_data.setdefault('active', True)
            role_data.setdefault('system_role', False)
            role_data.setdefault('created_at', datetime.now())
            role_data.setdefault('updated_at', datetime.now())
            
            print(f"DEBUG ROLE_MODEL - Datos preparados: {role_data}")
            
            if self.db and self.connect():
                print("DEBUG ROLE_MODEL - Conectado a BD, llamando a self.create()")
                role_id = self.create(role_data)
                print(f"DEBUG ROLE_MODEL - self.create() devolvió: {role_id}")
                
                if role_id:
                    self.logger.info(f"Rol creado exitosamente: {role_data.get('name')} (ID: {role_id})")
                    print(f"DEBUG ROLE_MODEL - Rol creado exitosamente con ID: {role_id}")
                    return role_id
                else:
                    print("DEBUG ROLE_MODEL - self.create() devolvió None/False")
            else:
                print("DEBUG ROLE_MODEL - No se pudo conectar a la BD")
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error creando rol: {e}")
            return None
    
    def update_role(self, role_id: int, role_data: Dict[str, Any]) -> bool:
        """Actualizar rol existente"""
        try:
            print(f"\n{'='*80}")
            print(f"🔄 ROLE_MODEL.UPDATE_ROLE - INICIADO")
            print(f"{'='*80}")
            print(f"📌 Role ID: {role_id}")
            print(f"📦 Datos recibidos: {role_data}")
            print(f"📊 Tipo de 'permissions': {type(role_data.get('permissions'))}")
            
            # Verificar que el rol existe
            existing_role = self.get_role_by_id(role_id)
            if not existing_role:
                print(f"❌ Rol {role_id} no encontrado")
                self.logger.error(f"Rol {role_id} no encontrado")
                return False
            
            print(f"✅ Rol encontrado: {existing_role['name']}")
            print(f"📋 Permisos actuales: {existing_role.get('permissions', [])[:5]}... (primeros 5)")
            
            # No permitir editar roles del sistema protegidos
            if existing_role.get('system_role') and existing_role.get('code') in ['super_admin']:
                print(f"❌ No se puede editar Super Admin")
                self.logger.error(f"No se puede editar el rol del sistema: {existing_role.get('code')}")
                return False
            
            print(f"✅ Rol puede ser editado")
            
            # Validar datos
            print(f"🔍 Validando datos...")
            is_valid, errors = self.validate_role_data(role_data, is_update=True)
            print(f"📊 Validación: válido={is_valid}, errores={errors}")
            
            if not is_valid:
                print(f"❌ Datos inválidos: {errors}")
                self.logger.error(f"Datos de rol inválidos: {errors}")
                return False
            
            print(f"✅ Datos válidos")
            
            # Preparar datos
            print(f"🔧 Sanitizando datos...")
            role_data = self.sanitize_input(role_data)
            print(f"✅ Datos sanitizados: {role_data}")
            
            # Convertir permisos a JSON si es necesario
            if isinstance(role_data.get('permissions'), list):
                import json
                perms_list = role_data['permissions']
                print(f"🔄 Convirtiendo {len(perms_list)} permisos a JSON...")
                print(f"📝 Permisos: {perms_list[:5]}... (primeros 5)")
                role_data['permissions'] = json.dumps(perms_list)
                print(f"✅ JSON generado: {role_data['permissions'][:100]}... (primeros 100 chars)")
            
            role_data['updated_at'] = datetime.now()
            print(f"📅 updated_at establecido: {role_data['updated_at']}")
            
            print(f"🔌 Verificando conexión a BD...")
            if self.db and self.connect():
                print(f"✅ Conectado a BD")
                print(f"💾 Ejecutando UPDATE en tabla 'roles' con ID={role_id}...")
                print(f"📦 Datos a actualizar: {role_data}")
                
                success = self.update(role_id, role_data)
                
                print(f"📊 Resultado del UPDATE: {success}")
                
                if success:
                    print(f"✅ ROL ACTUALIZADO EXITOSAMENTE")
                    self.logger.info(f"Rol actualizado exitosamente: ID {role_id}")
                    
                    # Limpiar caché de permisos para todos los usuarios con este rol
                    print(f"🧹 Limpiando caché de permisos para usuarios con role_id={role_id}...")
                    self._clear_permissions_cache_for_role(role_id)
                else:
                    print(f"❌ UPDATE retornó False")
                
                print(f"{'='*80}\n")
                return success
            else:
                print(f"❌ No se pudo conectar a la BD")
                print(f"   self.db: {self.db}")
                print(f"{'='*80}\n")
                return False
            
        except Exception as e:
            print(f"❌ EXCEPCIÓN en update_role: {e}")
            import traceback
            traceback.print_exc()
            self.logger.error(f"Error actualizando rol {role_id}: {e}")
            print(f"{'='*80}\n")
            return False
    
    def delete_role(self, role_id: int) -> bool:
        """Eliminar rol (solo roles personalizados)"""
        try:
            # Verificar que el rol existe
            existing_role = self.get_role_by_id(role_id)
            if not existing_role:
                self.logger.error(f"Rol {role_id} no encontrado")
                return False
            
            # No permitir eliminar roles del sistema
            if existing_role.get('system_role'):
                self.logger.error(f"No se puede eliminar el rol del sistema: {existing_role.get('name')}")
                return False
            
            # Verificar que no hay usuarios usando este rol
            if self._role_has_users(role_id):
                self.logger.error(f"No se puede eliminar el rol {role_id}, tiene usuarios asignados")
                return False
            
            if self.db and self.connect():
                success = self.delete(role_id)
                if success:
                    self.logger.info(f"Rol eliminado exitosamente: ID {role_id}")
                return success
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error eliminando rol {role_id}: {e}")
            return False
    
    def activate_role(self, role_id: int) -> bool:
        """Activar rol"""
        return self.update_role(role_id, {'active': True})
    
    def deactivate_role(self, role_id: int) -> bool:
        """Desactivar rol"""
        try:
            # Verificar que el rol existe
            existing_role = self.get_role_by_id(role_id)
            if not existing_role:
                return False
            
            # No permitir desactivar roles críticos del sistema
            if existing_role.get('code') in ['super_admin', 'admin']:
                self.logger.error(f"No se puede desactivar el rol crítico: {existing_role.get('code')}")
                return False
            
            return self.update_role(role_id, {'active': False})
            
        except Exception as e:
            self.logger.error(f"Error desactivando rol {role_id}: {e}")
            return False
    
    def get_role_permissions(self, role_id: int) -> List[str]:
        """Obtener permisos de un rol"""
        role = self.get_role_by_id(role_id)
        if role:
            permissions = role.get('permissions', [])
            if permissions == ['*']:
                return self.get_all_available_permissions()
            return permissions
        return []
    
    def role_has_permission(self, role_id: int, permission: str) -> bool:
        """Verificar si un rol tiene un permiso específico"""
        permissions = self.get_role_permissions(role_id)
        
        # Super admin tiene todos los permisos
        if '*' in permissions:
            return True
        
        # Verificar permiso exacto
        if permission in permissions:
            return True
        
        # Verificar permisos con comodín (ej: users.* incluye users.view)
        for perm in permissions:
            if perm.endswith('.*'):
                module = perm[:-2]
                if permission.startswith(f"{module}."):
                    return True
        
        return False
    
    def get_all_available_permissions(self) -> List[str]:
        """Obtener todos los permisos disponibles en el sistema"""
        # ⭐ USAR get_permissions_by_category() COMO FUENTE ÚNICA DE VERDAD
        all_permissions = []
        permissions_by_category = self.get_permissions_by_category()
        
        for category, perms in permissions_by_category.items():
            all_permissions.extend(perms)
        
        return all_permissions
    
    def get_permissions_by_category(self) -> Dict[str, List[str]]:
        """Obtener permisos organizados por categoría"""
        return {
            'Usuarios': [
                'users.view', 'users.create', 'users.edit', 'users.delete',
                'users.activate', 'users.deactivate', 'users.export'
            ],
            'Roles y Permisos': [
                'roles.view', 'roles.create', 'roles.edit', 'roles.delete',
                'roles.assign', 'roles.permissions'
            ],
            'Sistema': [
                'system.config', 'system.backup', 'system.restore',
                'system.logs', 'system.maintenance', 'system.reports'
            ],
            'Dashboard': [
                'dashboard.view', 'dashboard.stats', 'dashboard.analytics'
            ],
            'Inventario': [
                'inventory.view', 'inventory.create', 'inventory.edit', 'inventory.delete',
                'inventory.stock', 'inventory.reports', 'inventory.export'
            ],
            'Ventas': [
                'sales.view', 'sales.create', 'sales.edit', 'sales.delete',
                'sales.view_own', 'sales.reports', 'sales.export'
            ],
            'Caja': [
                'cash.register', 'cash.open', 'cash.close', 'cash.reports'
            ],
            'Productos': [
                'products.view', 'products.create', 'products.edit', 'products.delete',
                'products.prices', 'products.categories'
            ],
            'Clientes': [
                'customers.view', 'customers.create', 'customers.edit', 'customers.delete',
                'customers.export'
            ],
            'Proveedores': [
                'suppliers.view', 'suppliers.create', 'suppliers.edit', 'suppliers.delete'
            ],
            'Reportes': [
                'reports.sales', 'reports.inventory', 'reports.users',
                'reports.financial', 'reports.export'
            ]
        }
    
    def validate_role_data(self, data: Dict[str, Any], is_update: bool = False) -> tuple[bool, List[str]]:
        """Validar datos del rol"""
        errors = []
        
        # Validar nombre
        if not is_update or 'name' in data:
            name = data.get('name', '').strip()
            if not name:
                errors.append("El nombre del rol es requerido")
            elif len(name) < 2:
                errors.append("El nombre del rol debe tener al menos 2 caracteres")
            elif len(name) > 100:
                errors.append("El nombre del rol no puede exceder 100 caracteres")
        
        # Validar código
        if not is_update or 'code' in data:
            code = data.get('code', '').strip()
            if not code:
                errors.append("El código del rol es requerido")
            elif not code.replace('_', '').isalnum():
                errors.append("El código del rol solo puede contener letras, números y guiones bajos")
            elif len(code) < 2:
                errors.append("El código del rol debe tener al menos 2 caracteres")
            elif len(code) > 50:
                errors.append("El código del rol no puede exceder 50 caracteres")
            else:
                # Verificar que el código sea único
                if not is_update and self._code_exists(code):
                    errors.append(f"Ya existe un rol con el código '{code}'")
        
        # Validar descripción
        if 'description' in data:
            description = data.get('description', '').strip()
            if description and len(description) > 500:
                errors.append("La descripción no puede exceder 500 caracteres")
        
        # Validar permisos
        if 'permissions' in data:
            permissions = data.get('permissions')
            print(f"\n🔍 VALIDANDO PERMISOS...")
            print(f"📦 Tipo de permissions: {type(permissions)}")
            print(f"📊 Cantidad de permisos: {len(permissions) if isinstance(permissions, list) else 'N/A'}")
            
            if not isinstance(permissions, list):
                print(f"❌ Los permisos NO son una lista")
                errors.append("Los permisos deben ser una lista")
            else:
                print(f"✅ Los permisos son una lista")
                available_permissions = self.get_all_available_permissions() + ['*']
                print(f"📋 Permisos disponibles en sistema: {len(available_permissions)}")
                print(f"📝 Primeros 10 disponibles: {available_permissions[:10]}")
                
                invalid_perms = []
                for perm in permissions:
                    if perm not in available_permissions:
                        invalid_perms.append(perm)
                
                if invalid_perms:
                    print(f"❌ PERMISOS INVÁLIDOS DETECTADOS: {len(invalid_perms)}")
                    print(f"📝 Permisos inválidos: {invalid_perms[:10]}... (primeros 10)")
                    for perm in invalid_perms[:10]:
                        errors.append(f"Permiso inválido: {perm}")
                else:
                    print(f"✅ Todos los {len(permissions)} permisos son válidos")
        
        print(f"\n📊 RESULTADO DE VALIDACIÓN:")
        print(f"   Errores encontrados: {len(errors)}")
        if errors:
            print(f"   Lista de errores: {errors}")
        
        return len(errors) == 0, errors
    
    def _code_exists(self, code: str) -> bool:
        """Verificar si existe un rol con el código dado"""
        return self.get_role_by_code(code) is not None
    
    def _role_has_users(self, role_id: int) -> bool:
        """Verificar si el rol tiene usuarios asignados"""
        try:
            # Importar aquí para evitar circular imports
            from models.user_model import UserModel
            user_model = UserModel()
            
            # Buscar usuarios con este rol
            users = user_model.find_all({'role_id': role_id})
            return len(users) > 0
            
        except Exception as e:
            self.logger.error(f"Error verificando usuarios del rol {role_id}: {e}")
            return True  # Por seguridad, asumir que tiene usuarios
    
    def get_roles_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de roles"""
        try:
            all_roles = self.get_all_roles(include_inactive=True)
            
            stats = {
                'total_roles': len(all_roles),
                'active_roles': len([r for r in all_roles if r.get('active', True)]),
                'inactive_roles': len([r for r in all_roles if not r.get('active', True)]),
                'system_roles': len([r for r in all_roles if r.get('system_role', False)]),
                'custom_roles': len([r for r in all_roles if not r.get('system_role', False)])
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error obteniendo estadísticas de roles: {e}")
            return {
                'total_roles': 0,
                'active_roles': 0,
                'inactive_roles': 0,
                'system_roles': 0,
                'custom_roles': 0
            }
    
    def _clear_permissions_cache_for_role(self, role_id: int):
        """Limpiar caché de permisos para todos los usuarios con este rol"""
        try:
            # Importar aquí para evitar circular imports
            from services.permission_service import PermissionService
            from models.user_model import UserModel
            
            permission_service = PermissionService()
            user_model = UserModel()
            
            # Obtener todos los usuarios con este rol
            users = user_model.find_all({'role_id': role_id})
            
            if users:
                print(f"   📋 Encontrados {len(users)} usuarios con este rol")
                for user in users:
                    user_id = user.get('id')
                    if user_id:
                        permission_service.clear_user_cache(user_id)
                        print(f"   🧹 Caché limpiado para usuario ID={user_id}")
            else:
                print(f"   ℹ️ No hay usuarios con este rol")
            
            # También limpiar todo el caché por seguridad
            permission_service.clear_all_cache()
            print(f"   ✅ Caché de permisos completamente limpiado")
            
        except Exception as e:
            self.logger.error(f"Error limpiando caché de permisos: {e}")
            print(f"   ⚠️ Error limpiando caché: {e}")
