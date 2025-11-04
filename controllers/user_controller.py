"""
Controlador de Usuarios
Maneja la lógica de negocio para la gestión de usuarios
"""

import hashlib
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from models.user_model import UserModel
from models.role_model import RoleModel


class UserController:
    """Controlador para gestión de usuarios"""
    
    def __init__(self):
        self.user_model = UserModel()
        self.role_model = RoleModel()
        self.logger = logging.getLogger(__name__)
    
    @staticmethod
    def _simplify_user_type(primary: Optional[str], secondary: Optional[str] = None) -> str:
        """Reducir nombre/código de rol a los tipos técnicos admitidos por la BD."""
        candidates = []
        if primary:
            candidates.append(str(primary).strip().lower())
        if secondary:
            candidates.append(str(secondary).strip().lower())
        candidates.append('')  # Garantizar al menos un elemento para fallback

        for value in candidates:
            if not value:
                continue
            if any(keyword in value for keyword in ('admin', 'super_admin', 'sistema', 'root')):
                return 'admin'
            if any(keyword in value for keyword in ('supervis', 'gerente', 'manager', 'jefe')):
                return 'supervisor'
            if any(keyword in value for keyword in ('cajer', 'cashier', 'vend', 'seller')):
                return 'cashier'

        return 'user'

    def get_all_users(self) -> List[Dict[str, Any]]:
        """Obtener todos los usuarios con sus roles"""
        try:
            # Intentar obtener usuarios con roles integrados
            users = self.user_model.get_all_users_with_roles()
            
            # Convertir a formato compatible con la vista
            formatted_users = []
            for user in users:
                # Determinar el rol a mostrar
                role_name = user.get('role_name', user.get('user_type', ''))
                
                formatted_user = {
                    'id': user.get('id'),
                    'username': user.get('username'),
                    'full_name': user.get('full_name'),
                    'email': user.get('email'),
                    'user_type': role_name,  # Usar el nombre del rol
                    'role_id': user.get('role_id'),
                    'role_code': user.get('role_code'),
                    'status': 'active' if user.get('active') else 'inactive',
                    'last_login': user.get('last_login'),
                    'created_at': user.get('created_at'),
                    'phone': user.get('phone'),
                    'avatar_path': user.get('avatar_path')
                }
                formatted_users.append(formatted_user)
            
            return formatted_users
            
        except Exception as e:
            self.logger.error(f"Error obteniendo usuarios con roles: {str(e)}")
            # Fallback al método original
            try:
                users = self.user_model.get_all_users()
                formatted_users = []
                for user in users:
                    formatted_user = {
                        'id': user.get('id'),
                        'username': user.get('username'),
                        'full_name': user.get('full_name'),
                        'email': user.get('email'),
                        'user_type': user.get('user_type'),
                        'status': 'active' if user.get('active') else 'inactive',
                        'last_login': user.get('last_login'),
                        'created_at': user.get('created_at'),
                        'phone': user.get('phone'),
                        'avatar_path': user.get('avatar_path')
                    }
                    formatted_users.append(formatted_user)
                return formatted_users
            except Exception as fallback_error:
                self.logger.error(f"Error en fallback: {str(fallback_error)}")
                return []
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Obtener usuario por ID"""
        try:
            user = self.user_model.get_user_by_id(user_id)
            if user:
                return {
                    'id': user.get('id'),
                    'username': user.get('username'),
                    'full_name': user.get('full_name'),
                    'email': user.get('email'),
                    'user_type': user.get('user_type'),
                    'status': 'active' if user.get('status') == 1 else 'inactive',
                    'last_login': user.get('last_login'),
                    'created_at': user.get('created_at'),
                    'phone': user.get('phone'),
                    'avatar_path': user.get('avatar_path')
                }
            return None
            
        except Exception as e:
            self.logger.error(f"Error obteniendo usuario {user_id}: {str(e)}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Obtener usuario por nombre de usuario"""
        try:
            user = self.user_model.get_user_by_username(username)
            if user:
                return {
                    'id': user.get('id'),
                    'username': user.get('username'),
                    'full_name': user.get('full_name'),
                    'email': user.get('email'),
                    'user_type': user.get('user_type'),
                    'status': 'active' if user.get('status') == 1 else 'inactive',
                    'last_login': user.get('last_login'),
                    'created_at': user.get('created_at'),
                    'phone': user.get('phone'),
                    'avatar_path': user.get('avatar_path')
                }
            return None
            
        except Exception as e:
            self.logger.error(f"Error obteniendo usuario por username {username}: {str(e)}")
            return None
    
    def create_user(self, user_data: Dict[str, Any]) -> bool:
        """Crear nuevo usuario"""
        try:
            print(f"DEBUG CREATE_USER - Datos recibidos: {user_data}")
            
            # Validar datos requeridos
            required_fields = ['username', 'full_name', 'email', 'user_type', 'password']
            for field in required_fields:
                if field not in user_data or not user_data[field]:
                    print(f"DEBUG CREATE_USER - Campo requerido faltante: {field}")
                    self.logger.error(f"Campo requerido faltante: {field}")
                    return False
            
            print("DEBUG CREATE_USER - Todos los campos requeridos están presentes")
            
            # Verificar si el usuario ya existe
            print(f"DEBUG CREATE_USER - Verificando si usuario existe: {user_data['username']}")
            existing_user = self.user_model.get_user_by_username(user_data['username'])
            if existing_user:
                print(f"DEBUG CREATE_USER - Usuario ya existe: {user_data['username']}")
                self.logger.error(f"Usuario ya existe: {user_data['username']}")
                return False
            
            # Verificar si el email ya existe
            print(f"DEBUG CREATE_USER - Verificando si email existe: {user_data['email']}")
            existing_email = self.user_model.get_user_by_email(user_data['email'])
            if existing_email:
                print(f"DEBUG CREATE_USER - Email ya existe: {user_data['email']}")
                self.logger.error(f"Email ya existe: {user_data['email']}")
                return False
            
            print("DEBUG CREATE_USER - Usuario y email únicos, continuando...")
            
            # Resolver rol seleccionado desde la vista (id / código / nombre)
            input_role_name = user_data.get('user_type', '')
            role_id = user_data.get('role_id')
            role_code = user_data.get('role_code')
            print(f"DEBUG CREATE_USER - Intentando resolver rol: nombre='{input_role_name}', id='{role_id}', código='{role_code}'")

            if role_id is not None:
                try:
                    role_id = int(role_id)
                except (TypeError, ValueError):
                    print(f"DEBUG CREATE_USER - role_id '{role_id}' no es numérico, descartando")
                    role_id = None

            resolved_role_name = input_role_name

            try:
                roles = self.role_model.get_all_roles()
                print(f"DEBUG CREATE_USER - Roles encontrados: {len(roles)}")
                for role in roles:
                    role_name_db = role.get('name', '')
                    role_code_db = role.get('code', '')
                    role_id_db = role.get('id')

                    if role_id is not None and role_id_db == role_id:
                        resolved_role_name = role_name_db or resolved_role_name
                        role_code = role_code or role_code_db
                        print(f"DEBUG CREATE_USER - Rol resuelto por ID: {role_id_db}")
                        break

                    if input_role_name and role_name_db.lower() == input_role_name.lower():
                        role_id = role_id_db
                        resolved_role_name = role_name_db
                        role_code = role_code or role_code_db
                        print(f"DEBUG CREATE_USER - Rol resuelto por nombre: {resolved_role_name} (ID: {role_id})")
                        break

                    if role_code and role_code_db and role_code_db.lower() == str(role_code).lower():
                        role_id = role_id_db
                        resolved_role_name = role_name_db or resolved_role_name
                        print(f"DEBUG CREATE_USER - Rol resuelto por código: {role_code_db} (ID: {role_id})")
                        break

                if role_id is None:
                    print(f"DEBUG CREATE_USER - No se pudo determinar el role_id para '{input_role_name}'")

            except Exception as role_error:
                print(f"DEBUG CREATE_USER - Error obteniendo roles: {role_error}")
                self.logger.warning(f"Error obteniendo roles: {role_error}")

            db_user_type = self._simplify_user_type(role_code, resolved_role_name)
            print(f"DEBUG CREATE_USER - Mapeo simplificado: rol='{resolved_role_name}' código='{role_code}' -> user_type='{db_user_type}' (role_id: {role_id})")
            
            create_data = {
                'username': user_data['username'],
                'password_hash': self.hash_password(user_data['password']),
                'full_name': user_data['full_name'],
                'email': user_data['email'],
                'user_type': db_user_type,  # Usar valor mapeado compatible con BD
                'role_id': role_id,  # Asignar role_id si se encontró
                'active': True,  # Activo por defecto
                'phone': user_data.get('phone', ''),
                'avatar_path': user_data.get('avatar_path', ''),
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"DEBUG CREATE_USER - Datos preparados para crear usuario: {create_data}")
            
            # Crear usuario
            print("DEBUG CREATE_USER - Llamando a user_model.create_user()")
            user_id = self.user_model.create_user(create_data)
            print(f"DEBUG CREATE_USER - Resultado de create_user: {user_id}")
            
            if user_id:
                print(f"DEBUG CREATE_USER - Usuario creado exitosamente con ID: {user_id}")
                self.logger.info(f"Usuario creado exitosamente: {user_data['username']} (ID: {user_id})")
                return True
            else:
                print("DEBUG CREATE_USER - create_user devolvió None/False")
            
            return False
            
        except Exception as e:
            print(f"DEBUG CREATE_USER - Excepción capturada: {str(e)}")
            import traceback
            traceback.print_exc()
            self.logger.error(f"Error creando usuario: {str(e)}")
            return False
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> bool:
        """Actualizar usuario existente"""
        try:
            safe_payload = {k: ('***' if 'password' in k else v) for k, v in user_data.items()}
            self.logger.info("Actualizando usuario %s con datos recibidos: %s", user_id, safe_payload)
            print(f"DEBUG UPDATE_USER - Payload recibido: {safe_payload}")

            # Verificar que el usuario existe
            existing_user = self.user_model.get_user_by_id(user_id)
            if not existing_user:
                self.logger.error(f"Usuario no encontrado: {user_id}")
                return False
            
            # Resolver rol seleccionado desde la vista
            existing_role_id = existing_user.get('role_id')
            incoming_role_id = user_data.get('role_id')
            resolved_role_id = existing_role_id
            resolved_role_code = user_data.get('role_code')
            resolved_role_name = user_data.get('user_type') or ''

            if incoming_role_id is not None:
                try:
                    resolved_role_id = int(incoming_role_id)
                except (TypeError, ValueError):
                    self.logger.warning(f"ID de rol inválido recibido: {incoming_role_id}")
                    resolved_role_id = existing_role_id

            try:
                roles = self.role_model.get_all_roles()
                self.logger.debug(f"Roles disponibles para actualización: {len(roles)}")
                for role in roles:
                    role_name_db = role.get('name', '')
                    role_code_db = role.get('code', '')
                    role_id_db = role.get('id')

                    if resolved_role_id is not None and role_id_db == resolved_role_id:
                        resolved_role_name = resolved_role_name or role_name_db
                        resolved_role_code = resolved_role_code or role_code_db
                        break

                    if resolved_role_name and role_name_db.lower() == resolved_role_name.lower():
                        resolved_role_id = role_id_db
                        resolved_role_code = resolved_role_code or role_code_db
                        resolved_role_name = role_name_db
                        break

                    if resolved_role_code and role_code_db and role_code_db.lower() == str(resolved_role_code).lower():
                        resolved_role_id = role_id_db
                        resolved_role_name = role_name_db or resolved_role_name
                        break

            except Exception as role_error:
                self.logger.warning(f"Error obteniendo roles: {role_error}")

            # Simplificar user_type con la información resuelta
            db_user_type = existing_user.get('user_type')  # Mantener el actual por defecto
            role_reference_name = resolved_role_name or existing_user.get('user_type', '')
            if resolved_role_code or role_reference_name or resolved_role_id != existing_role_id:
                db_user_type = self._simplify_user_type(resolved_role_code, role_reference_name)
                print(f"DEBUG UPDATE_USER - Mapeo: '{role_reference_name}' (código: '{resolved_role_code}') -> '{db_user_type}' (role_id: {resolved_role_id})")
            self.logger.info(
                "Usuario %s -> rol resuelto id=%s código=%s nombre='%s' user_type='%s'",
                user_id,
                resolved_role_id,
                resolved_role_code,
                role_reference_name,
                db_user_type,
            )
            
            # Normalizar estado proporcionado por la vista (puede venir en español)
            status_raw = str(user_data.get('status', 'active')).strip().lower()
            is_active = status_raw not in {'inactive', 'inactivo', '0', 'false', 'no'}

            # Preparar datos para actualizar
            update_data = {
                'full_name': user_data.get('full_name', existing_user.get('full_name')),
                'email': user_data.get('email', existing_user.get('email')),
                'user_type': db_user_type,  # ✅ Usar valor mapeado
                'role_id': resolved_role_id,
                'active': is_active,
                'phone': user_data.get('phone', existing_user.get('phone', '')),
                'avatar_path': user_data.get('avatar_path', existing_user.get('avatar_path', ''))
            }
            self.logger.info("Payload final para update_user %s: %s", user_id, update_data)
            print(f"DEBUG UPDATE_USER - Payload final para modelo: {update_data}")
            
            # Actualizar contraseña si se proporcionó
            if 'password' in user_data and user_data['password']:
                update_data['password_hash'] = self.hash_password(user_data['password'])
            
            # Verificar cambio de username
            if 'username' in user_data and user_data['username'] != existing_user.get('username'):
                # Verificar que el nuevo username no existe
                existing_username = self.user_model.get_user_by_username(user_data['username'])
                if existing_username and existing_username.get('id') != user_id:
                    self.logger.error(f"Username ya existe: {user_data['username']}")
                    return False
                update_data['username'] = user_data['username']
            
            # Verificar cambio de email
            if user_data.get('email') != existing_user.get('email'):
                existing_email = self.user_model.get_user_by_email(user_data['email'])
                if existing_email and existing_email.get('id') != user_id:
                    self.logger.error(f"Email ya existe: {user_data['email']}")
                    return False
            
            # Actualizar usuario
            success = self.user_model.update_user(user_id, update_data)
            self.logger.info("Resultado de update_user %s: %s", user_id, success)
            
            if success:
                updated = self.user_model.get_user_by_id(user_id)
                self.logger.info(
                    "Usuario %s actualizado. role_id=%s, user_type=%s, active=%s",
                    user_id,
                    updated.get('role_id') if updated else None,
                    updated.get('user_type') if updated else None,
                    updated.get('active') if updated else None,
                )
                self.logger.info(f"Usuario actualizado exitosamente: ID {user_id}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error actualizando usuario {user_id}: {str(e)}")
            return False
    
    def delete_user(self, user_id: int) -> bool:
        """Eliminar usuario"""
        try:
            # Verificar que el usuario existe
            existing_user = self.user_model.get_user_by_id(user_id)
            if not existing_user:
                self.logger.error(f"Usuario no encontrado: {user_id}")
                return False
            
            # No permitir eliminar el último administrador
            if existing_user.get('user_type') == 'admin':
                admin_count = self.count_users_by_type('admin')
                if admin_count <= 1:
                    self.logger.error("No se puede eliminar el último administrador")
                    return False
            
            # Eliminar usuario
            success = self.user_model.delete_user(user_id)
            
            if success:
                self.logger.info(f"Usuario eliminado exitosamente: ID {user_id}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error eliminando usuario {user_id}: {str(e)}")
            return False
    
    def change_user_status(self, user_id: int, status: str) -> bool:
        """Cambiar estado de usuario (activo/inactivo)"""
        try:
            # Verificar que el usuario existe
            existing_user = self.user_model.get_user_by_id(user_id)
            if not existing_user:
                self.logger.error(f"Usuario no encontrado: {user_id}")
                return False
            
            # Convertir status a booleano para la columna 'active'
            active_value = True if status == 'active' else False
            
            # No permitir desactivar el último administrador
            if status == 'inactive' and existing_user.get('user_type') == 'admin':
                active_admin_count = self.count_active_users_by_type('admin')
                if active_admin_count <= 1:
                    self.logger.error("No se puede desactivar el último administrador activo")
                    return False
            
            # Actualizar estado usando la columna 'active' (no 'status')
            success = self.user_model.update_user(user_id, {'active': active_value})
            
            if success:
                self.logger.info(f"Estado de usuario actualizado: ID {user_id} -> active={active_value}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error cambiando estado de usuario {user_id}: {str(e)}")
            return False
    
    def update_user_status(self, user_id: int, status: str) -> bool:
        """Actualizar estado de usuario (activo/inactivo) - Alias para change_user_status"""
        return self.change_user_status(user_id, status)
    
    def change_password(self, user_id: int, new_password: str) -> bool:
        """Cambiar contraseña de usuario"""
        try:
            # Verificar que el usuario existe
            existing_user = self.user_model.get_user_by_id(user_id)
            if not existing_user:
                self.logger.error(f"Usuario no encontrado: {user_id}")
                return False
            
            # Validar contraseña
            if len(new_password) < 4:
                self.logger.error("La contraseña debe tener al menos 4 caracteres")
                return False
            
            # Actualizar contraseña
            password_hash = self.hash_password(new_password)
            success = self.user_model.update_user(user_id, {'password_hash': password_hash})
            
            if success:
                self.logger.info(f"Contraseña actualizada para usuario ID {user_id}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error cambiando contraseña de usuario {user_id}: {str(e)}")
            return False
    
    def count_users_by_type(self, user_type: str) -> int:
        """Contar usuarios por tipo"""
        try:
            users = self.user_model.get_users_by_type(user_type)
            return len(users) if users else 0
        except Exception as e:
            self.logger.error(f"Error contando usuarios por tipo {user_type}: {str(e)}")
            return 0
    
    def count_active_users_by_type(self, user_type: str) -> int:
        """Contar usuarios activos por tipo"""
        try:
            users = self.user_model.get_active_users_by_type(user_type)
            return len(users) if users else 0
        except Exception as e:
            self.logger.error(f"Error contando usuarios activos por tipo {user_type}: {str(e)}")
            return 0
    
    def get_users_by_type(self, user_type: str) -> List[Dict[str, Any]]:
        """Obtener usuarios por tipo"""
        try:
            users = self.user_model.get_users_by_type(user_type)
            
            # Convertir a formato compatible con la vista
            formatted_users = []
            for user in users:
                formatted_user = {
                    'id': user.get('id'),
                    'username': user.get('username'),
                    'full_name': user.get('full_name'),
                    'email': user.get('email'),
                    'user_type': user.get('user_type'),
                    'status': 'active' if user.get('status') == 1 else 'inactive',
                    'last_login': user.get('last_login'),
                    'created_at': user.get('created_at'),
                    'phone': user.get('phone'),
                    'avatar_path': user.get('avatar_path')
                }
                formatted_users.append(formatted_user)
            
            return formatted_users
            
        except Exception as e:
            self.logger.error(f"Error obteniendo usuarios por tipo {user_type}: {str(e)}")
            return []
    
    def search_users(self, search_term: str) -> List[Dict[str, Any]]:
        """Buscar usuarios por término de búsqueda"""
        try:
            users = self.user_model.search_users(search_term)
            
            # Convertir a formato compatible con la vista
            formatted_users = []
            for user in users:
                formatted_user = {
                    'id': user.get('id'),
                    'username': user.get('username'),
                    'full_name': user.get('full_name'),
                    'email': user.get('email'),
                    'user_type': user.get('user_type'),
                    'status': 'active' if user.get('status') == 1 else 'inactive',
                    'last_login': user.get('last_login'),
                    'created_at': user.get('created_at'),
                    'phone': user.get('phone'),
                    'avatar_path': user.get('avatar_path')
                }
                formatted_users.append(formatted_user)
            
            return formatted_users
            
        except Exception as e:
            self.logger.error(f"Error buscando usuarios con término '{search_term}': {str(e)}")
            return []
    
    def validate_user_permissions(self, user_id: int, required_permission: str) -> bool:
        """Validar permisos de usuario"""
        try:
            user = self.user_model.get_user_by_id(user_id)
            if not user:
                return False
            
            user_type = user.get('user_type', '')
            
            # Definir permisos por tipo de usuario
            permissions = {
                'admin': ['all_modules', 'users_manage', 'system_config', 'reports.full', 'super_admin'],
                'supervisor': ['sales', 'inventory', 'reports_limited', 'users_view'],
                'cajero': ['sales', 'basic_reports']
            }
            
            user_permissions = permissions.get(user_type, [])
            
            # Admin tiene todos los permisos
            if user_type == 'admin':
                return True
            
            return required_permission in user_permissions
            
        except Exception as e:
            self.logger.error(f"Error validando permisos de usuario {user_id}: {str(e)}")
            return False
    
    def hash_password(self, password: str) -> str:
        """Hash de contraseña usando SHA-256"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verificar contraseña contra hash"""
        return self.hash_password(password) == password_hash
    
    def get_user_statistics(self) -> Dict[str, int]:
        """Obtener estadísticas de usuarios"""
        try:
            all_users = self.get_all_users()
            
            stats = {
                'total': len(all_users),
                'active': len([u for u in all_users if u['status'] == 'active']),
                'inactive': len([u for u in all_users if u['status'] == 'inactive']),
                'admins': len([u for u in all_users if u['user_type'] == 'admin']),
                'supervisors': len([u for u in all_users if u['user_type'] == 'supervisor']),
                'cajeros': len([u for u in all_users if u['user_type'] == 'cajero'])
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error obteniendo estadísticas de usuarios: {str(e)}")
            return {
                'total': 0,
                'active': 0,
                'inactive': 0,
                'admins': 0,
                'supervisors': 0,
                'cajeros': 0
            }
