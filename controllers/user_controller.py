"""
Controlador de Usuarios
Maneja la lógica de negocio para la gestión de usuarios
"""

import hashlib
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from models.user_model import UserModel


class UserController:
    """Controlador para gestión de usuarios"""
    
    def __init__(self):
        self.user_model = UserModel()
        self.logger = logging.getLogger(__name__)
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Obtener todos los usuarios"""
        try:
            users = self.user_model.get_all_users()
            
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
            self.logger.error(f"Error obteniendo usuarios: {str(e)}")
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
            # Validar datos requeridos
            required_fields = ['username', 'full_name', 'email', 'user_type', 'password']
            for field in required_fields:
                if field not in user_data or not user_data[field]:
                    self.logger.error(f"Campo requerido faltante: {field}")
                    return False
            
            # Verificar si el usuario ya existe
            existing_user = self.user_model.get_user_by_username(user_data['username'])
            if existing_user:
                self.logger.error(f"Usuario ya existe: {user_data['username']}")
                return False
            
            # Verificar si el email ya existe
            existing_email = self.user_model.get_user_by_email(user_data['email'])
            if existing_email:
                self.logger.error(f"Email ya existe: {user_data['email']}")
                return False
            
            # Preparar datos para crear usuario
            create_data = {
                'username': user_data['username'],
                'password_hash': self.hash_password(user_data['password']),
                'full_name': user_data['full_name'],
                'email': user_data['email'],
                'user_type': user_data['user_type'],
                'status': 1,  # Activo por defecto
                'phone': user_data.get('phone', ''),
                'avatar_path': user_data.get('avatar_path', ''),
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Crear usuario
            user_id = self.user_model.create_user(create_data)
            
            if user_id:
                self.logger.info(f"Usuario creado exitosamente: {user_data['username']} (ID: {user_id})")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error creando usuario: {str(e)}")
            return False
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> bool:
        """Actualizar usuario existente"""
        try:
            # Verificar que el usuario existe
            existing_user = self.user_model.get_user_by_id(user_id)
            if not existing_user:
                self.logger.error(f"Usuario no encontrado: {user_id}")
                return False
            
            # Preparar datos para actualizar
            update_data = {
                'full_name': user_data.get('full_name', existing_user.get('full_name')),
                'email': user_data.get('email', existing_user.get('email')),
                'user_type': user_data.get('user_type', existing_user.get('user_type')),
                'status': 1 if user_data.get('status', 'active') == 'active' else 0,
                'phone': user_data.get('phone', existing_user.get('phone', '')),
                'avatar_path': user_data.get('avatar_path', existing_user.get('avatar_path', ''))
            }
            
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
            
            if success:
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
            
            # Convertir status a formato de base de datos
            status_value = 1 if status == 'active' else 0
            
            # No permitir desactivar el último administrador
            if status == 'inactive' and existing_user.get('user_type') == 'admin':
                active_admin_count = self.count_active_users_by_type('admin')
                if active_admin_count <= 1:
                    self.logger.error("No se puede desactivar el último administrador activo")
                    return False
            
            # Actualizar estado
            success = self.user_model.update_user(user_id, {'status': status_value})
            
            if success:
                self.logger.info(f"Estado de usuario actualizado: ID {user_id} -> {status}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error cambiando estado de usuario {user_id}: {str(e)}")
            return False
    
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
                'admin': ['all_modules', 'users_manage', 'system_config', 'reports_full', 'super_admin'],
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
