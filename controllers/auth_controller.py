"""
Controlador de Autenticación para el Sistema POS
Maneja la lógica entre la vista de login y los modelos de usuario/auth
"""

import json
import os
from typing import Dict, Any, Optional, Callable
import logging
from models.user_model import UserModel
from models.auth_model import AuthModel
from views.login_view import LoginView

class AuthController:
    """Controlador para gestión de autenticación"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Modelos
        self.user_model = UserModel()
        self.auth_model = AuthModel()
        
        # Vista de login (se inicializa cuando se necesita)
        self.login_view = None
        
        # Callbacks para eventos
        self.on_login_success_callback = None
        self.on_login_failure_callback = None
        self.on_logout_callback = None
        
        # Configuración
        self.remember_file = "config/remembered_users.json"
        self.max_login_attempts = 3
        
        # Estado
        self.current_user = None
        self.login_attempts = 0
    
    def show_login(self, on_success: Callable = None, on_failure: Callable = None):
        """Mostrar ventana de login"""
        try:
            # Configurar callbacks
            if on_success:
                self.on_login_success_callback = on_success
            if on_failure:
                self.on_login_failure_callback = on_failure
            
            # Crear vista si no existe
            if not self.login_view:
                self.login_view = LoginView()
                self._setup_login_callbacks()
            
            # Resetear formulario para limpiar estado previo
            self.login_view.reset_form()
            
            # Cargar usuario recordado si existe
            self._load_remembered_user()
            
            # Mostrar ventana
            self.login_view.show()
            self.login_view.run()
            
        except Exception as e:
            self.logger.error(f"Error mostrando login: {e}")
            if self.on_login_failure_callback:
                self.on_login_failure_callback(f"Error al inicializar login: {str(e)}")
    
    def _setup_login_callbacks(self):
        """Configurar callbacks de la vista de login"""
        self.login_view.bind_login_callback(self._handle_login_attempt)
        self.login_view.bind_success_callback(self._handle_login_success)
        self.login_view.bind_error_callback(self._handle_login_error)
        self.login_view.bind_callback('before_close', self._handle_login_close)
    
    def _handle_login_attempt(self, form_data: Dict[str, Any]):
        """Manejar intento de login"""
        try:
            username = form_data.get('username', '').strip()
            password = form_data.get('password', '').strip()
            remember = form_data.get('remember', False)
            
            self.logger.info(f"Intento de login para usuario: {username}")
            
            # Verificar límite de intentos
            if self.login_attempts >= self.max_login_attempts:
                self.login_view.on_login_error("Demasiados intentos fallidos. Reinicia la aplicación.")
                return
            
            # Autenticar usuario
            user_data = self.user_model.authenticate(username, password)
            
            if user_data:
                # Login exitoso
                self.login_attempts = 0  # Resetear intentos
                
                # Crear sesión
                session_id = self.auth_model.create_session(user_data, 'manual')
                
                if session_id:
                    self.current_user = user_data
                    
                    # Guardar usuario si se marcó recordar
                    if remember:
                        self._save_remembered_user(username)
                    else:
                        self._clear_remembered_user()
                    
                    # Notificar éxito a la vista
                    self.login_view.on_login_success(user_data)
                    
                    # Ocultar login después de un breve delay
                    self.login_view.root.after(1500, self._complete_login_success)
                    
                else:
                    self.login_view.on_login_error("Error al crear sesión")
            else:
                # Login fallido
                self.login_attempts += 1
                remaining = self.max_login_attempts - self.login_attempts
                
                if remaining > 0:
                    error_msg = f"Credenciales incorrectas. Te quedan {remaining} intentos."
                else:
                    error_msg = "Credenciales incorrectas. Has agotado tus intentos."
                
                self.login_view.on_login_error(error_msg)
                
        except Exception as e:
            self.logger.error(f"Error en intento de login: {e}")
            self.login_view.on_login_error("Error interno del sistema")
    
    def _complete_login_success(self):
        """Completar proceso de login exitoso"""
        try:
            # Ocultar ventana de login
            self.login_view.hide()
            
            # Ejecutar callback de éxito
            if self.on_login_success_callback:
                self.on_login_success_callback(self.current_user)
            
            self.logger.info(f"Login completado para: {self.current_user.get('username')}")
            
        except Exception as e:
            self.logger.error(f"Error completando login: {e}")
    
    def _handle_login_success(self, user_data: Dict[str, Any]):
        """Manejar evento de login exitoso desde la vista"""
        # Este método se llama desde la vista, la lógica principal está en _handle_login_attempt
        pass
    
    def _handle_login_error(self, error_message: str):
        """Manejar evento de error desde la vista"""
        # Log del error
        self.logger.warning(f"Error de login: {error_message}")
        
        # Ejecutar callback de fallo si existe
        if self.on_login_failure_callback:
            self.on_login_failure_callback(error_message)
    
    def _handle_login_close(self) -> bool:
        """Manejar cierre de ventana de login"""
        # Retornar False para permitir el cierre normal
        return False
    
    def logout(self, reason: str = 'manual') -> bool:
        """Cerrar sesión del usuario actual"""
        try:
            if not self.auth_model.current_session:
                self.logger.warning("Intento de logout sin sesión activa")
                return True
            
            username = self.auth_model.current_session.get('username', 'desconocido')
            
            # Cerrar sesión en el modelo
            success = self.auth_model.close_session(reason)
            
            if success:
                # Limpiar datos locales
                self.current_user = None
                self.login_attempts = 0
                
                # Ejecutar callback de logout
                if self.on_logout_callback:
                    self.on_logout_callback(username, reason)
                
                self.logger.info(f"Logout exitoso para: {username}")
                return True
            else:
                self.logger.error("Error cerrando sesión")
                return False
                
        except Exception as e:
            self.logger.error(f"Error en logout: {e}")
            return False
    
    def is_authenticated(self) -> bool:
        """Verificar si hay un usuario autenticado"""
        session = self.auth_model.get_current_session()
        return session is not None
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Obtener datos del usuario actual"""
        return self.auth_model.get_current_user()
    
    def has_permission(self, permission: str) -> bool:
        """Verificar si el usuario actual tiene un permiso"""
        return self.auth_model.has_permission(permission)
    
    def require_authentication(self) -> bool:
        """Requerir autenticación válida"""
        if not self.is_authenticated():
            raise PermissionError("Se requiere autenticación")
        return True
    
    def require_permission(self, permission: str) -> bool:
        """Requerir permiso específico"""
        self.require_authentication()
        return self.auth_model.require_permission(permission)
    
    def extend_session(self, hours: int = 2) -> bool:
        """Extender sesión actual"""
        return self.auth_model.extend_session(hours)
    
    def get_session_info(self) -> Dict[str, Any]:
        """Obtener información de la sesión actual"""
        return self.auth_model.get_session_info()
    
    def change_password(self, current_password: str, new_password: str) -> tuple[bool, str]:
        """Cambiar contraseña del usuario actual"""
        try:
            user = self.get_current_user()
            if not user:
                return False, "No hay usuario autenticado"
            
            # Verificar contraseña actual
            user_data = self.user_model.find_by_username(user['username'])
            if not user_data:
                return False, "Usuario no encontrado"
            
            if not self.user_model.verify_password(current_password, user_data.get('password_hash', '')):
                return False, "Contraseña actual incorrecta"
            
            # Cambiar contraseña
            success = self.user_model.change_password(user['id'], new_password, user['id'])
            
            if success:
                self.logger.info(f"Contraseña cambiada para usuario: {user['username']}")
                return True, "Contraseña cambiada exitosamente"
            else:
                return False, "Error al cambiar contraseña"
                
        except Exception as e:
            self.logger.error(f"Error cambiando contraseña: {e}")
            return False, f"Error interno: {str(e)}"
    
    def _save_remembered_user(self, username: str):
        """Guardar usuario para recordar"""
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(self.remember_file), exist_ok=True)
            
            data = {'username': username, 'remember': True}
            
            with open(self.remember_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
            self.logger.info(f"Usuario recordado guardado: {username}")
            
        except Exception as e:
            self.logger.error(f"Error guardando usuario recordado: {e}")
    
    def _load_remembered_user(self):
        """Cargar usuario recordado"""
        try:
            if os.path.exists(self.remember_file):
                with open(self.remember_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                username = data.get('username', '')
                if username and data.get('remember', False):
                    self.login_view.load_remembered_user(username)
                    self.logger.info(f"Usuario recordado cargado: {username}")
                    
        except Exception as e:
            self.logger.error(f"Error cargando usuario recordado: {e}")
    
    def _clear_remembered_user(self):
        """Limpiar usuario recordado"""
        try:
            if os.path.exists(self.remember_file):
                os.remove(self.remember_file)
                self.logger.info("Usuario recordado eliminado")
                
        except Exception as e:
            self.logger.error(f"Error eliminando usuario recordado: {e}")
    
    def get_login_attempts_info(self, username: str) -> Dict[str, Any]:
        """Obtener información de intentos de login"""
        try:
            attempts = self.auth_model.get_login_attempts(username, hours=1)
            
            return {
                'total_attempts': len(attempts),
                'recent_attempts': attempts[:5],  # Últimos 5 intentos
                'max_attempts': self.max_login_attempts,
                'current_attempts': self.login_attempts
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo intentos de login: {e}")
            return {}
    
    def reset_login_attempts(self):
        """Resetear contador de intentos de login"""
        self.login_attempts = 0
        self.logger.info("Intentos de login reseteados")
    
    def set_login_success_callback(self, callback: Callable):
        """Establecer callback de login exitoso"""
        self.on_login_success_callback = callback
    
    def set_login_failure_callback(self, callback: Callable):
        """Establecer callback de login fallido"""
        self.on_login_failure_callback = callback
    
    def set_logout_callback(self, callback: Callable):
        """Establecer callback de logout"""
        self.on_logout_callback = callback
    
    def cleanup(self):
        """Limpiar recursos del controlador"""
        try:
            # Cerrar sesión si existe
            if self.is_authenticated():
                self.logout('cleanup')
            
            # Limpiar vista
            if self.login_view:
                self.login_view.on_destroy()
                self.login_view = None
            
            # Limpiar modelos
            self.user_model = None
            self.auth_model = None
            
            self.logger.info("Controlador de autenticación limpiado")
            
        except Exception as e:
            self.logger.error(f"Error limpiando controlador: {e}")
    
    def __del__(self):
        """Destructor del controlador"""
        self.cleanup()
