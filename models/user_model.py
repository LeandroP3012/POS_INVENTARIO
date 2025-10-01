"""
Modelo de Usuario para el Sistema POS
Maneja todas las operaciones relacionadas con usuarios
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from models.base_model import BaseModel

class UserModel(BaseModel):
    """Modelo para gestión de usuarios"""
    
    def __init__(self):
        super().__init__()
        self.table_name = 'users'
        self.primary_key = 'id'
        
        # Definir tipos de usuario válidos (mantener por compatibilidad)
        self.valid_user_types = ['admin', 'supervisor', 'cashier', 'user']
        
        # Usuarios por defecto (fallback) - ahora con role_id
        self.default_users = {
            'admin': {
                'id': 1,
                'username': 'admin',
                'password_hash': self.hash_password('123456'),
                'email': 'admin@sistema-pos.com',
                'full_name': 'Administrador del Sistema',
                'user_type': 'admin',  # Mantener por compatibilidad
                'role_id': 2,  # Rol Administrador
                'active': True,
                'permissions': {
                    'all_modules': True,
                    'super_admin': True,
                    'users_manage': True,
                    'roles_manage': True,
                    'system_config': True,
                    'reports_full': True
                }
            },
            'manager': {
                'id': 2,
                'username': 'manager',
                'password_hash': self.hash_password('123456'),
                'email': 'manager@sistema-pos.com',
                'full_name': 'Gerente Principal',
                'user_type': 'supervisor',  # Mantener por compatibilidad
                'role_id': 3,  # Rol Gerente
                'active': True,
                'permissions': {
                    'users_view': True,
                    'inventory_view': True,
                    'sales_manage': True,
                    'reports_basic': True
                }
            }
        }
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Crear hash SHA-256 de la contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verificar contraseña contra hash"""
        return self.hash_password(password) == password_hash
    
    def find_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Buscar usuario por nombre de usuario"""
        if not self.connect():
            # Fallback a usuarios por defecto
            return self.default_users.get(username)
        
        try:
            result = self.find_by_field('username', username)
            return result
        except Exception as e:
            self.logger.error(f"Error buscando usuario {username}: {e}")
            return self.default_users.get(username)
    
    def find_active_users(self) -> List[Dict[str, Any]]:
        """Obtener todos los usuarios activos"""
        if not self.connect():
            return [user for user in self.default_users.values() if user.get('active', True)]
        
        try:
            return self.find_all({'active': True})
        except Exception as e:
            self.logger.error(f"Error obteniendo usuarios activos: {e}")
            return [user for user in self.default_users.values() if user.get('active', True)]
    
    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Autenticar usuario con username y password"""
        user = self.find_by_username(username)
        
        if not user:
            self.logger.warning(f"Usuario no encontrado: {username}")
            return None
        
        # Verificar si el usuario está activo
        if not user.get('active', True):
            self.logger.warning(f"Usuario inactivo: {username}")
            return None
        
        # Verificar si el usuario está bloqueado
        if self.is_user_locked(user):
            self.logger.warning(f"Usuario bloqueado: {username}")
            return None
        
        # Verificar contraseña
        if not self.verify_password(password, user.get('password_hash', '')):
            self.increment_failed_attempts(user)
            self.logger.warning(f"Contraseña incorrecta para: {username}")
            return None
        
        # Resetear intentos fallidos y actualizar último login
        self.reset_failed_attempts(user)
        
        # Preparar datos del usuario para retornar
        user_data = self.prepare_user_data(user)
        
        self.logger.info(f"Usuario autenticado exitosamente: {username}")
        return user_data
    
    def is_user_locked(self, user: Dict[str, Any]) -> bool:
        """Verificar si el usuario está bloqueado"""
        locked_until = user.get('locked_until')
        
        if not locked_until:
            return False
        
        # Si locked_until es string, convertir a datetime
        if isinstance(locked_until, str):
            try:
                locked_until = datetime.fromisoformat(locked_until)
            except:
                return False
        
        return datetime.now() < locked_until
    
    def increment_failed_attempts(self, user: Dict[str, Any]):
        """Incrementar intentos fallidos de login"""
        if not self.connect() or not user.get('id'):
            return  # No podemos actualizar usuarios por defecto
        
        try:
            user_id = user['id']
            current_attempts = user.get('failed_attempts', 0) + 1
            
            update_data = {'failed_attempts': current_attempts}
            
            # Si excede el límite, bloquear usuario
            if current_attempts >= 3:
                locked_until = datetime.now() + timedelta(minutes=15)
                update_data['locked_until'] = locked_until
                self.logger.warning(f"Usuario bloqueado por exceso de intentos: {user['username']}")
            
            self.update(user_id, update_data)
            
        except Exception as e:
            self.logger.error(f"Error incrementando intentos fallidos: {e}")
    
    def reset_failed_attempts(self, user: Dict[str, Any]):
        """Resetear intentos fallidos y actualizar último login"""
        if not self.connect() or not user.get('id'):
            return  # No podemos actualizar usuarios por defecto
        
        try:
            user_id = user['id']
            update_data = {
                'failed_attempts': 0,
                'locked_until': None,
                'last_login': datetime.now()
            }
            
            self.update(user_id, update_data)
            
        except Exception as e:
            self.logger.error(f"Error reseteando intentos fallidos: {e}")
    
    def prepare_user_data(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Preparar datos del usuario para uso en la aplicación"""
        permissions = user.get('permissions', {})
        
        # Si permissions es string JSON, convertir
        if isinstance(permissions, str):
            try:
                permissions = json.loads(permissions)
            except:
                permissions = {}
        
        return {
            'id': user.get('id', 0),
            'username': user.get('username', ''),
            'full_name': user.get('full_name', ''),
            'email': user.get('email', ''),
            'user_type': user.get('user_type', 'user'),
            'permissions': permissions,
            'last_login': user.get('last_login'),
            'phone': user.get('phone'),
            'avatar_path': user.get('avatar_path'),
            'created_at': user.get('created_at'),
            'source': 'database' if user.get('id') else 'local'
        }
    
    def create_user(self, user_data: Dict[str, Any], created_by_id: int = None) -> Optional[int]:
        """Crear nuevo usuario"""
        print(f"DEBUG USER_MODEL - create_user llamado con: {user_data}")
        
        # Validar datos
        print("DEBUG USER_MODEL - Validando datos de usuario...")
        is_valid, errors = self.validate_user_data(user_data)
        print(f"DEBUG USER_MODEL - Validación: válido={is_valid}, errores={errors}")
        
        if not is_valid:
            print(f"DEBUG USER_MODEL - Datos inválidos, errores: {errors}")
            self.logger.error(f"Datos de usuario inválidos: {errors}")
            return None
        
        # Hashear contraseña si viene en texto plano
        if 'password' in user_data:
            user_data['password_hash'] = self.hash_password(user_data['password'])
            del user_data['password']
        
        # Agregar creador
        if created_by_id:
            user_data['created_by'] = created_by_id
        
        # Convertir permisos a JSON si es necesario
        if 'permissions' in user_data and isinstance(user_data['permissions'], dict):
            user_data['permissions'] = json.dumps(user_data['permissions'])
        
        try:
            print("DEBUG USER_MODEL - Llamando a self.create()")
            user_id = self.create(user_data)
            print(f"DEBUG USER_MODEL - self.create() devolvió: {user_id}")
            
            if user_id:
                print(f"DEBUG USER_MODEL - Usuario creado exitosamente con ID: {user_id}")
                self.log_activity('CREATE_USER', user_id, f"Usuario creado: {user_data.get('username')}", created_by_id)
            else:
                print("DEBUG USER_MODEL - self.create() devolvió None/False")
                
            return user_id
        except Exception as e:
            print(f"DEBUG USER_MODEL - Excepción en create_user: {e}")
            import traceback
            traceback.print_exc()
            self.logger.error(f"Error creando usuario: {e}")
            return None
    
    def update_user(self, user_id: int, user_data: Dict[str, Any], updated_by_id: int = None) -> bool:
        """Actualizar usuario existente"""
        # Validar datos
        is_valid, errors = self.validate_user_data(user_data, is_update=True)
        if not is_valid:
            self.logger.error(f"Datos de usuario inválidos: {errors}")
            return False
        
        # Hashear contraseña si viene en texto plano
        if 'password' in user_data:
            user_data['password_hash'] = self.hash_password(user_data['password'])
            del user_data['password']
        
        # Convertir permisos a JSON si es necesario
        if 'permissions' in user_data and isinstance(user_data['permissions'], dict):
            user_data['permissions'] = json.dumps(user_data['permissions'])
        
        try:
            success = self.update(user_id, user_data)
            if success:
                self.log_activity('UPDATE_USER', user_id, f"Usuario actualizado", updated_by_id)
            return success
        except Exception as e:
            self.logger.error(f"Error actualizando usuario: {e}")
            return False
    
    def change_password(self, user_id: int, new_password: str, changed_by_id: int = None) -> bool:
        """Cambiar contraseña de usuario"""
        try:
            password_hash = self.hash_password(new_password)
            success = self.update(user_id, {'password_hash': password_hash})
            
            if success:
                self.log_activity('CHANGE_PASSWORD', user_id, "Contraseña cambiada", changed_by_id)
            
            return success
        except Exception as e:
            self.logger.error(f"Error cambiando contraseña: {e}")
            return False
    
    def toggle_user_status(self, user_id: int, active: bool, updated_by_id: int = None) -> bool:
        """Activar/desactivar usuario"""
        try:
            success = self.update(user_id, {'active': active})
            
            if success:
                status = "activado" if active else "desactivado"
                self.log_activity('TOGGLE_STATUS', user_id, f"Usuario {status}", updated_by_id)
            
            return success
        except Exception as e:
            self.logger.error(f"Error cambiando estado de usuario: {e}")
            return False
    
    def unlock_user(self, user_id: int, unlocked_by_id: int = None) -> bool:
        """Desbloquear usuario"""
        try:
            update_data = {
                'failed_attempts': 0,
                'locked_until': None
            }
            
            success = self.update(user_id, update_data)
            
            if success:
                self.log_activity('UNLOCK_USER', user_id, "Usuario desbloqueado", unlocked_by_id)
            
            return success
        except Exception as e:
            self.logger.error(f"Error desbloqueando usuario: {e}")
            return False
    
    def get_users_by_type(self, user_type: str) -> List[Dict[str, Any]]:
        """Obtener usuarios por tipo"""
        if not self.connect():
            return [user for user in self.default_users.values() if user.get('user_type') == user_type]
        
        try:
            return self.find_all({'user_type': user_type, 'active': True})
        except Exception as e:
            self.logger.error(f"Error obteniendo usuarios por tipo: {e}")
            return []
    
    def get_user_statistics(self) -> Dict[str, int]:
        """Obtener estadísticas de usuarios"""
        if not self.connect():
            users = list(self.default_users.values())
            return {
                'total': len(users),
                'active': len([u for u in users if u.get('active', True)]),
                'inactive': len([u for u in users if not u.get('active', True)]),
                'admin': len([u for u in users if u.get('user_type') == 'admin']),
                'cashier': len([u for u in users if u.get('user_type') == 'cashier']),
                'supervisor': len([u for u in users if u.get('user_type') == 'supervisor']),
                'user': len([u for u in users if u.get('user_type') == 'user'])
            }
        
        try:
            stats = {}
            stats['total'] = self.count()
            stats['active'] = self.count({'active': True})
            stats['inactive'] = self.count({'active': False})
            
            for user_type in self.valid_user_types:
                stats[user_type] = self.count({'user_type': user_type, 'active': True})
            
            return stats
        except Exception as e:
            self.logger.error(f"Error obteniendo estadísticas: {e}")
            return {}
    
    def validate_user_data(self, data: Dict[str, Any], is_update: bool = False) -> tuple[bool, List[str]]:
        """Validar datos de usuario"""
        errors = []
        
        # Validar username (requerido para crear, opcional para actualizar)
        if not is_update or 'username' in data:
            username = data.get('username', '').strip()
            if not username:
                errors.append("El nombre de usuario es requerido")
            elif len(username) < 3:
                errors.append("El nombre de usuario debe tener al menos 3 caracteres")
            elif len(username) > 50:
                errors.append("El nombre de usuario no puede tener más de 50 caracteres")
            elif not username.replace('_', '').replace('-', '').isalnum():
                errors.append("El nombre de usuario solo puede contener letras, números, guiones y guiones bajos")
        
        # Validar email
        if 'email' in data and data['email']:
            email = data['email'].strip()
            if '@' not in email or '.' not in email:
                errors.append("El email no tiene un formato válido")
        
        # Validar full_name
        if not is_update or 'full_name' in data:
            full_name = data.get('full_name', '').strip()
            if not full_name:
                errors.append("El nombre completo es requerido")
            elif len(full_name) > 100:
                errors.append("El nombre completo no puede tener más de 100 caracteres")
        
        # Validar user_type - permite tanto tipos antiguos como nombres de roles nuevos
        if not is_update or 'user_type' in data:
            user_type = data.get('user_type', '').strip()
            if not user_type:
                errors.append("El tipo de usuario es requerido")
            elif user_type not in self.valid_user_types:
                # Si no es un tipo válido antiguo, verificar si es un nombre de rol válido
                try:
                    from models.role_model import RoleModel
                    role_model = RoleModel()
                    roles = role_model.get_all_roles()
                    valid_role_names = [role.get('name', '') for role in roles if role.get('active', True)]
                    
                    if user_type not in valid_role_names:
                        # Si tampoco es un rol válido, mostrar error
                        all_valid = self.valid_user_types + valid_role_names
                        errors.append(f"Tipo de usuario/rol inválido. Debe ser uno de: {', '.join(all_valid)}")
                except Exception as e:
                    # Si hay error obteniendo roles, usar solo validación antigua
                    print(f"DEBUG - Error validando rol: {e}")
                    if user_type not in self.valid_user_types:
                        errors.append(f"Tipo de usuario inválido. Debe ser uno de: {', '.join(self.valid_user_types)}")
        
        # Validar contraseña (solo si se proporciona)
        if 'password' in data:
            password = data['password']
            if len(password) < 6:
                errors.append("La contraseña debe tener al menos 6 caracteres")
            elif len(password) > 128:
                errors.append("La contraseña no puede tener más de 128 caracteres")
        
        # Validar que username sea único (solo para crear o si se cambió)
        if not is_update or 'username' in data:
            username = data.get('username', '').strip()
            existing_user = self.find_by_username(username)
            if existing_user and (not is_update or existing_user.get('id') != data.get('id')):
                errors.append("El nombre de usuario ya está en uso")
        
        return len(errors) == 0, errors
    
    def search_users(self, search_term: str) -> List[Dict[str, Any]]:
        """Buscar usuarios por término de búsqueda"""
        if not self.connect():
            # Búsqueda en usuarios por defecto
            results = []
            search_term = search_term.lower()
            for user in self.default_users.values():
                if (search_term in user.get('username', '').lower() or 
                    search_term in user.get('full_name', '').lower() or
                    search_term in user.get('email', '').lower()):
                    results.append(user)
            return results
        
        try:
            query = """
            SELECT * FROM users 
            WHERE (username LIKE %s OR full_name LIKE %s OR email LIKE %s) 
            AND active = TRUE
            ORDER BY full_name
            """
            search_pattern = f"%{search_term}%"
            
            result = self.execute_query(query, (search_pattern, search_pattern, search_pattern))
            return result if result else []
            
        except Exception as e:
            self.logger.error(f"Error buscando usuarios: {e}")
            return []
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Obtener todos los usuarios"""
        if not self.connect():
            return list(self.default_users.values())
        
        try:
            return self.find_all(order_by='full_name')
        except Exception as e:
            self.logger.error(f"Error obteniendo todos los usuarios: {e}")
            return list(self.default_users.values())
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Obtener usuario por ID"""
        if not self.connect():
            # En usuarios por defecto, usar el username como "id"
            for user in self.default_users.values():
                if str(user.get('username')) == str(user_id):
                    return user
            return None
        
        try:
            return self.find_by_id(user_id)
        except Exception as e:
            self.logger.error(f"Error obteniendo usuario por ID {user_id}: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Obtener usuario por nombre de usuario (alias para find_by_username)"""
        return self.find_by_username(username)
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Obtener usuario por email"""
        if not self.connect():
            for user in self.default_users.values():
                if user.get('email', '').lower() == email.lower():
                    return user
            return None
        
        try:
            return self.find_by_field('email', email)
        except Exception as e:
            self.logger.error(f"Error obteniendo usuario por email {email}: {e}")
            return None
    
    def get_active_users_by_type(self, user_type: str) -> List[Dict[str, Any]]:
        """Obtener usuarios activos por tipo"""
        if not self.connect():
            return [user for user in self.default_users.values() 
                   if user.get('user_type') == user_type and user.get('active', True)]
        
        try:
            return self.find_all({'user_type': user_type, 'active': True})
        except Exception as e:
            self.logger.error(f"Error obteniendo usuarios activos por tipo: {e}")
            return []
    
    def delete_user(self, user_id: int) -> bool:
        """Eliminar usuario (eliminar físicamente)"""
        if not self.connect():
            self.logger.warning("No se pueden eliminar usuarios por defecto")
            return False
        
        try:
            # Log de la acción antes de eliminar
            user = self.get_user_by_id(user_id)
            if user:
                self.log_activity('DELETE_USER', user_id, f"Usuario eliminado: {user.get('username')}")
            
            return self.delete(user_id)
        except Exception as e:
            self.logger.error(f"Error eliminando usuario: {e}")
            return False
    
    # =============================================================================
    # MÉTODOS PARA TRABAJAR CON ROLES
    # =============================================================================
    
    def get_user_with_role(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Obtener usuario con información de su rol"""
        try:
            if not self.connect():
                # Fallback para usuarios por defecto
                for user in self.default_users.values():
                    if user.get('id') == user_id:
                        return self._enrich_user_with_role_info(user)
                return None
            
            # Consulta con JOIN para obtener información del rol
            query = """
            SELECT u.*, r.name as role_name, r.code as role_code, 
                   r.permissions as role_permissions, r.system_role
            FROM users u
            LEFT JOIN roles r ON u.role_id = r.id
            WHERE u.id = %s
            """
            
            result = self.execute_query(query, (user_id,))
            
            if result:
                user_data = result[0]
                return self._process_user_with_role(user_data)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error obteniendo usuario con rol {user_id}: {e}")
            return None
    
    def get_all_users_with_roles(self) -> List[Dict[str, Any]]:
        """Obtener todos los usuarios con información de sus roles"""
        try:
            if not self.connect():
                # Fallback para usuarios por defecto
                users = []
                for user in self.default_users.values():
                    users.append(self._enrich_user_with_role_info(user))
                return users
            
            # Consulta con JOIN para obtener información del rol
            query = """
            SELECT u.*, r.name as role_name, r.code as role_code, 
                   r.permissions as role_permissions, r.system_role
            FROM users u
            LEFT JOIN roles r ON u.role_id = r.id
            ORDER BY u.username
            """
            
            result = self.execute_query(query)
            
            if result:
                users = []
                for user_data in result:
                    users.append(self._process_user_with_role(user_data))
                return users
            
            return []
            
        except Exception as e:
            self.logger.error(f"Error obteniendo usuarios con roles: {e}")
            # Fallback para usuarios por defecto
            users = []
            for user in self.default_users.values():
                users.append(self._enrich_user_with_role_info(user))
            return users
    
    def get_user_permissions(self, user_id: int) -> List[str]:
        """Obtener todos los permisos de un usuario (combinando rol y permisos específicos)"""
        try:
            user = self.get_user_with_role(user_id)
            if not user:
                return []
            
            # Combinar permisos del rol y permisos específicos del usuario
            permissions = []
            
            # Permisos del rol
            role_permissions = user.get('role_permissions', [])
            if isinstance(role_permissions, str):
                import json
                try:
                    role_permissions = json.loads(role_permissions)
                except:
                    role_permissions = []
            
            if role_permissions:
                permissions.extend(role_permissions)
            
            # Permisos específicos del usuario
            user_permissions = user.get('permissions', {})
            if isinstance(user_permissions, dict):
                for perm, granted in user_permissions.items():
                    if granted and perm not in permissions:
                        permissions.append(perm)
            
            return permissions
            
        except Exception as e:
            self.logger.error(f"Error obteniendo permisos del usuario {user_id}: {e}")
            return []
    
    def user_has_permission(self, user_id: int, permission: str) -> bool:
        """Verificar si un usuario tiene un permiso específico"""
        try:
            permissions = self.get_user_permissions(user_id)
            
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
            
        except Exception as e:
            self.logger.error(f"Error verificando permiso {permission} para usuario {user_id}: {e}")
            return False
    
    def assign_role_to_user(self, user_id: int, role_id: int) -> bool:
        """Asignar rol a usuario"""
        try:
            success = self.update(user_id, {'role_id': role_id, 'updated_at': datetime.now()})
            
            if success:
                self.log_activity('ASSIGN_ROLE', user_id, f"Rol {role_id} asignado al usuario")
                self.logger.info(f"Rol {role_id} asignado al usuario {user_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error asignando rol {role_id} al usuario {user_id}: {e}")
            return False
    
    def get_users_by_role(self, role_id: int) -> List[Dict[str, Any]]:
        """Obtener usuarios que tienen un rol específico"""
        try:
            if not self.connect():
                # Fallback para usuarios por defecto
                users = []
                for user in self.default_users.values():
                    if user.get('role_id') == role_id:
                        users.append(self._enrich_user_with_role_info(user))
                return users
            
            conditions = {'role_id': role_id, 'active': True}
            users_data = self.find_all(conditions)
            
            # Enriquecer con información del rol
            users = []
            for user_data in users_data:
                user_with_role = self.get_user_with_role(user_data['id'])
                if user_with_role:
                    users.append(user_with_role)
            
            return users
            
        except Exception as e:
            self.logger.error(f"Error obteniendo usuarios por rol {role_id}: {e}")
            return []
    
    def _process_user_with_role(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Procesar datos de usuario con información del rol"""
        # Convertir permisos del rol de JSON string a lista si es necesario
        if isinstance(user_data.get('role_permissions'), str):
            import json
            try:
                user_data['role_permissions'] = json.loads(user_data['role_permissions'])
            except:
                user_data['role_permissions'] = []
        
        # Convertir permisos del usuario de JSON string a dict si es necesario
        if isinstance(user_data.get('permissions'), str):
            import json
            try:
                user_data['permissions'] = json.loads(user_data['permissions'])
            except:
                user_data['permissions'] = {}
        
        return user_data
    
    def _enrich_user_with_role_info(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Enriquecer usuario por defecto con información del rol"""
        user_copy = user.copy()
        
        # Agregar información del rol basada en role_id
        role_id = user.get('role_id')
        if role_id:
            # Mapeo de roles por defecto
            role_info = {
                1: {'name': 'Super Admin', 'code': 'super_admin', 'permissions': ['*']},
                2: {'name': 'Administrador', 'code': 'admin', 'permissions': ['users.view', 'users.create', 'users.edit']},
                3: {'name': 'Gerente', 'code': 'manager', 'permissions': ['users.view', 'sales.create']},
                4: {'name': 'Empleado', 'code': 'employee', 'permissions': ['sales.create']},
                5: {'name': 'Cajero', 'code': 'cashier', 'permissions': ['sales.create']}
            }
            
            role = role_info.get(role_id, {})
            user_copy['role_name'] = role.get('name', 'Sin Rol')
            user_copy['role_code'] = role.get('code', 'no_role')
            user_copy['role_permissions'] = role.get('permissions', [])
            user_copy['system_role'] = True
        
        return user_copy
