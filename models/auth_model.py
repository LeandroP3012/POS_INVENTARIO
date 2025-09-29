"""
Modelo de Autenticación para el Sistema POS
Maneja sesiones, permisos y logs de actividad
"""

import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from models.base_model import BaseModel

class AuthModel(BaseModel):
    """Modelo para gestión de autenticación y sesiones"""
    
    def __init__(self):
        super().__init__()
        self.table_name = 'user_sessions'
        self.primary_key = 'id'
        
        # Sesión actual (singleton)
        self.current_session = None
    
    def create_session(self, user_data: Dict[str, Any], login_method: str = 'manual') -> Optional[str]:
        """Crear nueva sesión de usuario"""
        try:
            session_data = {
                'user_id': user_data.get('id', 0),
                'username': user_data.get('username', ''),
                'user_type': user_data.get('user_type', 'user'),
                'login_time': datetime.now(),
                'login_method': login_method,
                'is_active': True,
                'permissions': json.dumps(user_data.get('permissions', {})),
                'expires_at': datetime.now() + timedelta(hours=8)  # Sesión de 8 horas
            }
            
            # Si hay conexión a BD, guardar sesión
            if self.connect():
                try:
                    session_id = self.create(session_data)
                    if session_id:
                        session_data['session_id'] = session_id
                    else:
                        # Si falla la inserción, usar ID local
                        session_data['session_id'] = f"local_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                except Exception as db_error:
                    self.logger.warning(f"Error guardando sesión en BD: {db_error}")
                    session_data['session_id'] = f"local_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            else:
                # Generar ID local
                session_data['session_id'] = f"local_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Establecer como sesión actual
            self.current_session = session_data
            
            # Log de actividad (opcional si falla)
            try:
                self.log_activity(
                    'LOGIN', 
                    user_data.get('id', 0), 
                    f"Usuario {user_data.get('username')} inició sesión", 
                    user_data.get('id', 0)
                )
            except Exception as log_error:
                self.logger.warning(f"No se pudo registrar actividad: {log_error}")
            
            self.logger.info(f"Sesión creada para usuario: {user_data.get('username')}")
            return session_data.get('session_id')
            
        except Exception as e:
            self.logger.error(f"Error creando sesión: {e}")
            return None
    
    def get_current_session(self) -> Optional[Dict[str, Any]]:
        """Obtener sesión actual"""
        if not self.current_session:
            return None
        
        # Verificar si la sesión ha expirado
        if self.is_session_expired(self.current_session):
            self.close_session()
            return None
        
        return self.current_session
    
    def is_session_expired(self, session: Dict[str, Any]) -> bool:
        """Verificar si una sesión ha expirado"""
        expires_at = session.get('expires_at')
        
        if not expires_at:
            return True
        
        if isinstance(expires_at, str):
            try:
                expires_at = datetime.fromisoformat(expires_at)
            except:
                return True
        
        return datetime.now() > expires_at
    
    def extend_session(self, hours: int = 2) -> bool:
        """Extender sesión actual"""
        if not self.current_session:
            return False
        
        try:
            new_expiry = datetime.now() + timedelta(hours=hours)
            self.current_session['expires_at'] = new_expiry
            
            # Actualizar en BD si existe
            if self.connect() and self.current_session.get('session_id'):
                session_id = self.current_session['session_id']
                if isinstance(session_id, int):  # Solo si es ID de BD
                    self.update(session_id, {'expires_at': new_expiry})
            
            self.logger.info(f"Sesión extendida por {hours} horas")
            return True
            
        except Exception as e:
            self.logger.error(f"Error extendiendo sesión: {e}")
            return False
    
    def close_session(self, logout_reason: str = 'manual') -> bool:
        """Cerrar sesión actual"""
        if not self.current_session:
            return True
        
        try:
            # Marcar sesión como inactiva en BD
            if self.connect() and self.current_session.get('session_id'):
                session_id = self.current_session['session_id']
                if isinstance(session_id, int):  # Solo si es ID de BD
                    self.update(session_id, {
                        'is_active': False,
                        'logout_time': datetime.now(),
                        'logout_reason': logout_reason
                    })
            
            # Log de actividad
            self.log_activity(
                'LOGOUT', 
                self.current_session.get('user_id', 0), 
                f"Usuario {self.current_session.get('username')} cerró sesión", 
                self.current_session.get('user_id', 0)
            )
            
            username = self.current_session.get('username', 'desconocido')
            self.current_session = None
            
            self.logger.info(f"Sesión cerrada para usuario: {username}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error cerrando sesión: {e}")
            return False
    
    def has_permission(self, permission: str) -> bool:
        """Verificar si el usuario actual tiene un permiso específico"""
        if not self.current_session:
            return False
        
        try:
            permissions = self.current_session.get('permissions', {})
            
            # Si permissions es string JSON, convertir
            if isinstance(permissions, str):
                permissions = json.loads(permissions)
            
            # Super admin tiene todos los permisos
            if permissions.get('super_admin', False) or permissions.get('all_modules', False):
                return True
            
            # Verificar permiso específico
            return permissions.get(permission, False)
            
        except Exception as e:
            self.logger.error(f"Error verificando permiso {permission}: {e}")
            return False
    
    def get_user_permissions(self) -> Dict[str, bool]:
        """Obtener todos los permisos del usuario actual"""
        if not self.current_session:
            return {}
        
        try:
            permissions = self.current_session.get('permissions', {})
            
            # Si permissions es string JSON, convertir
            if isinstance(permissions, str):
                permissions = json.loads(permissions)
            
            return permissions
            
        except Exception as e:
            self.logger.error(f"Error obteniendo permisos: {e}")
            return {}
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Obtener datos del usuario actual"""
        if not self.current_session:
            return None
        
        return {
            'id': self.current_session.get('user_id', 0),
            'username': self.current_session.get('username', ''),
            'user_type': self.current_session.get('user_type', 'user'),
            'permissions': self.get_user_permissions(),
            'login_time': self.current_session.get('login_time'),
            'expires_at': self.current_session.get('expires_at')
        }
    
    def is_admin(self) -> bool:
        """Verificar si el usuario actual es admin"""
        return (self.current_session and 
                self.current_session.get('user_type') == 'admin')
    
    def is_supervisor(self) -> bool:
        """Verificar si el usuario actual es supervisor"""
        return (self.current_session and 
                self.current_session.get('user_type') in ['admin', 'supervisor'])
    
    def is_cashier(self) -> bool:
        """Verificar si el usuario actual es cajero"""
        return (self.current_session and 
                self.current_session.get('user_type') in ['admin', 'supervisor', 'cashier'])
    
    def get_active_sessions(self) -> List[Dict[str, Any]]:
        """Obtener todas las sesiones activas"""
        if not self.connect():
            # Retornar sesión actual si existe
            return [self.current_session] if self.current_session else []
        
        try:
            query = """
            SELECT s.*, u.full_name, u.email
            FROM user_sessions s
            LEFT JOIN users u ON s.user_id = u.id
            WHERE s.is_active = TRUE AND s.expires_at > %s
            ORDER BY s.login_time DESC
            """
            
            result = self.execute_query(query, (datetime.now(),))
            return result if result else []
            
        except Exception as e:
            self.logger.error(f"Error obteniendo sesiones activas: {e}")
            return []
    
    def close_all_user_sessions(self, user_id: int, except_current: bool = True) -> bool:
        """Cerrar todas las sesiones de un usuario"""
        if not self.connect():
            return True  # No hay sesiones que cerrar
        
        try:
            conditions = {'user_id': user_id, 'is_active': True}
            
            # Si se debe mantener la sesión actual
            if except_current and self.current_session:
                current_session_id = self.current_session.get('session_id')
                if current_session_id and isinstance(current_session_id, int):
                    query = """
                    UPDATE user_sessions 
                    SET is_active = FALSE, logout_time = %s, logout_reason = 'force_logout'
                    WHERE user_id = %s AND is_active = TRUE AND id != %s
                    """
                    self.execute_query(query, (datetime.now(), user_id, current_session_id), fetch=False)
                else:
                    # Cerrar todas las sesiones
                    query = """
                    UPDATE user_sessions 
                    SET is_active = FALSE, logout_time = %s, logout_reason = 'force_logout'
                    WHERE user_id = %s AND is_active = TRUE
                    """
                    self.execute_query(query, (datetime.now(), user_id), fetch=False)
            else:
                # Cerrar todas las sesiones
                query = """
                UPDATE user_sessions 
                SET is_active = FALSE, logout_time = %s, logout_reason = 'force_logout'
                WHERE user_id = %s AND is_active = TRUE
                """
                self.execute_query(query, (datetime.now(), user_id), fetch=False)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error cerrando sesiones del usuario {user_id}: {e}")
            return False
    
    def get_session_history(self, user_id: int = None, days: int = 30) -> List[Dict[str, Any]]:
        """Obtener historial de sesiones"""
        if not self.connect():
            return []
        
        try:
            since_date = datetime.now() - timedelta(days=days)
            
            if user_id:
                query = """
                SELECT s.*, u.full_name, u.email
                FROM user_sessions s
                LEFT JOIN users u ON s.user_id = u.id
                WHERE s.user_id = %s AND s.login_time >= %s
                ORDER BY s.login_time DESC
                """
                params = (user_id, since_date)
            else:
                query = """
                SELECT s.*, u.full_name, u.email
                FROM user_sessions s
                LEFT JOIN users u ON s.user_id = u.id
                WHERE s.login_time >= %s
                ORDER BY s.login_time DESC
                """
                params = (since_date,)
            
            result = self.execute_query(query, params)
            return result if result else []
            
        except Exception as e:
            self.logger.error(f"Error obteniendo historial de sesiones: {e}")
            return []
    
    def clean_expired_sessions(self) -> int:
        """Limpiar sesiones expiradas"""
        if not self.connect():
            return 0
        
        try:
            query = """
            UPDATE user_sessions 
            SET is_active = FALSE, logout_time = %s, logout_reason = 'expired'
            WHERE is_active = TRUE AND expires_at < %s
            """
            
            result = self.execute_query(query, (datetime.now(), datetime.now()), fetch=False)
            
            # Obtener número de filas afectadas
            if self.cursor:
                affected_rows = self.cursor.rowcount
                self.logger.info(f"Se limpiaron {affected_rows} sesiones expiradas")
                return affected_rows
            
            return 0
            
        except Exception as e:
            self.logger.error(f"Error limpiando sesiones expiradas: {e}")
            return 0
    
    def get_login_attempts(self, username: str, hours: int = 1) -> List[Dict[str, Any]]:
        """Obtener intentos de login recientes para un usuario"""
        if not self.connect():
            return []
        
        try:
            since_time = datetime.now() - timedelta(hours=hours)
            
            query = """
            SELECT created_at, description, ip_address
            FROM activity_logs
            WHERE activity_type = 'LOGIN_ATTEMPT' 
            AND description LIKE %s 
            AND created_at >= %s
            ORDER BY created_at DESC
            """
            
            search_pattern = f"%{username}%"
            result = self.execute_query(query, (search_pattern, since_time))
            return result if result else []
            
        except Exception as e:
            self.logger.error(f"Error obteniendo intentos de login: {e}")
            return []
    
    def require_permission(self, permission: str) -> bool:
        """Verificar permiso y lanzar excepción si no lo tiene"""
        if not self.has_permission(permission):
            username = self.current_session.get('username', 'desconocido') if self.current_session else 'sin sesión'
            raise PermissionError(f"Usuario {username} no tiene permiso: {permission}")
        return True
    
    def get_session_info(self) -> Dict[str, Any]:
        """Obtener información completa de la sesión actual"""
        if not self.current_session:
            return {
                'authenticated': False,
                'message': 'No hay sesión activa'
            }
        
        # Verificar expiración
        if self.is_session_expired(self.current_session):
            self.close_session('expired')
            return {
                'authenticated': False,
                'message': 'Sesión expirada'
            }
        
        # Calcular tiempo restante
        expires_at = self.current_session.get('expires_at')
        time_remaining = None
        
        if expires_at:
            if isinstance(expires_at, str):
                try:
                    expires_at = datetime.fromisoformat(expires_at)
                except:
                    expires_at = None
            
            if expires_at:
                remaining = expires_at - datetime.now()
                time_remaining = {
                    'total_seconds': int(remaining.total_seconds()),
                    'hours': int(remaining.total_seconds() // 3600),
                    'minutes': int((remaining.total_seconds() % 3600) // 60)
                }
        
        return {
            'authenticated': True,
            'user': self.get_current_user(),
            'session_id': self.current_session.get('session_id'),
            'login_time': self.current_session.get('login_time'),
            'expires_at': expires_at,
            'time_remaining': time_remaining,
            'permissions': self.get_user_permissions()
        }
