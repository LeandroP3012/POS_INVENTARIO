import mysql.connector
from mysql.connector import Error
import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any

class DatabaseConnection:
    """Gestor de conexión a la base de datos MySQL"""
    
    def __init__(self, config_file: str = "config/database.json"):
        self.config_file = config_file
        self.connection = None
        self.config = self.load_config()
        self.setup_logging()
    
    def load_config(self) -> Dict[str, Any]:
        """Cargar configuración de la base de datos"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as file:
                    config = json.load(file)
                    
                    # Normalizar formato antiguo al nuevo
                    if 'name' in config and 'database' not in config:
                        config['database'] = config['name']
                    if 'user' in config and 'username' not in config:
                        config['username'] = config['user']
                    
                    # Asegurar que port sea int
                    if 'port' in config and isinstance(config['port'], str):
                        config['port'] = int(config['port'])
                    
                    # Agregar valores por defecto si no existen
                    config.setdefault('charset', 'utf8mb4')
                    config.setdefault('autocommit', True)
                    config.setdefault('connection_timeout', 10)
                    config.setdefault('reconnection_attempts', 3)
                    config.setdefault('ssl_disabled', True)
                    config.setdefault('get_server_public_key', True)
                    config.setdefault('allow_local_infile', True)
                    
                    return config
            else:
                # Configuración por defecto
                default_config = {
                    "host": "localhost",
                    "port": 3306,
                    "database": "pos_system",
                    "username": "root",
                    "password": "D3v3l0p3r@@$",
                    "charset": "utf8mb4",
                    "autocommit": True,
                    "pool_name": "pos_pool",
                    "pool_size": 5,
                    "pool_reset_session": True,
                    "connection_timeout": 10,
                    "reconnection_attempts": 3,
                    "ssl_disabled": True,
                    "get_server_public_key": True,
                    "allow_local_infile": True
                }
                self.save_config(default_config)
                return default_config
        except Exception as e:
            print(f"Error cargando configuración: {e}")
            return self.get_fallback_config()
    
    def save_config(self, config: Dict[str, Any]) -> None:
        """Guardar configuración de la base de datos"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as file:
                json.dump(config, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando configuración: {e}")
    
    def get_fallback_config(self) -> Dict[str, Any]:
        """Configuración de emergencia"""
        return {
            "host": "localhost",
            "port": 3306,
            "database": "pos_system",
            "username": "root",
            "password": "D3v3l0p3r@@$",
            "charset": "utf8mb4",
            "autocommit": True
        }
    
    def setup_logging(self) -> None:
        """Configurar logging para la base de datos"""
        os.makedirs("logs", exist_ok=True)
        log_filename = f"logs/database_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Logger específico para base de datos
        self.logger = logging.getLogger('database')
    
    def connect(self) -> bool:
        """Establecer conexión con la base de datos"""
        try:
            # Configuración de conexión para MySQL 8.0+ y 9.x
            connection_params = {
                'host': self.config['host'],
                'port': self.config['port'],
                'database': self.config['database'],
                'user': self.config['username'],
                'password': self.config['password'],
                'charset': self.config['charset'],
                'autocommit': self.config.get('autocommit', True),
                'connection_timeout': self.config.get('connection_timeout', 10),
            }
            
            # Intentar con mysql_native_password como plugin de autenticación
            # Esto resuelve el error de caching_sha2_password
            try:
                connection_params['auth_plugin'] = 'mysql_native_password'
                self.connection = mysql.connector.connect(**connection_params)
            except Exception:
                # Si falla, intentar sin auth_plugin especificado
                del connection_params['auth_plugin']
                self.connection = mysql.connector.connect(**connection_params)
            
            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                self.logger.info(f"Conectado exitosamente a MySQL Server versión {db_info}")
                return True
                
        except Error as e:
            self.logger.error(f"Error conectando a MySQL: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error inesperado: {e}")
            return False
    
    def disconnect(self) -> None:
        """Cerrar conexión con la base de datos"""
        try:
            if self.connection and self.connection.is_connected():
                self.connection.close()
                self.logger.info("Conexión a MySQL cerrada")
        except Exception as e:
            self.logger.error(f"Error cerrando conexión: {e}")
    
    def is_connected(self) -> bool:
        """Verificar si la conexión está activa"""
        try:
            return self.connection and self.connection.is_connected()
        except:
            return False
    
    def reconnect(self) -> bool:
        """Reconectar a la base de datos"""
        self.logger.info("Intentando reconectar a la base de datos...")
        self.disconnect()
        return self.connect()
    
    def execute_query(self, query: str, params: tuple = None, fetch: bool = True) -> Optional[list]:
        """Ejecutar una consulta SQL"""
        try:
            if not self.is_connected():
                if not self.reconnect():
                    return None
            
            cursor = self.connection.cursor(dictionary=True)
            
            # Log detallado de la query antes de ejecutar
            self.logger.info(f"📝 EJECUTANDO SQL: {query}")
            self.logger.info(f"📦 PARÁMETROS: {params}")
            print(f"📝 SQL: {query}")
            print(f"📦 PARAMS: {params}")
            
            cursor.execute(query, params or ())
            
            if fetch and query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
                self.logger.info(f"✅ SELECT retornó {len(result) if result else 0} filas")
                print(f"✅ SELECT: {len(result) if result else 0} filas")
                cursor.close()
                return result
            else:
                self.connection.commit()
                affected_rows = cursor.rowcount
                self.logger.info(f"✅ UPDATE/INSERT afectó {affected_rows} filas")
                print(f"✅ AFFECTED ROWS: {affected_rows}")
                cursor.close()
                return affected_rows
                
        except Error as e:
            self.logger.error(f"❌ Error ejecutando query: {e}")
            self.logger.error(f"Query: {query}")
            self.logger.error(f"Params: {params}")
            print(f"❌ ERROR SQL: {e}")
            return None
        except Exception as e:
            self.logger.error(f"❌ Error inesperado en query: {e}")
            print(f"ERROR QUERY DB: {e}")  # Debug adicional
            import traceback
            print(f"QUERY TRACEBACK: {traceback.format_exc()}")
            return None
    
    def execute_many(self, query: str, data: list) -> bool:
        """Ejecutar múltiples inserciones/actualizaciones"""
        try:
            if not self.is_connected():
                if not self.reconnect():
                    return False
            
            cursor = self.connection.cursor()
            cursor.executemany(query, data)
            self.connection.commit()
            cursor.close()
            return True
            
        except Error as e:
            self.logger.error(f"Error ejecutando executemany: {e}")
            return False
    
    def get_cursor(self, dictionary: bool = True):
        """Obtener cursor para operaciones manuales"""
        try:
            if not self.is_connected():
                if not self.reconnect():
                    return None
            return self.connection.cursor(dictionary=dictionary)
        except Exception as e:
            self.logger.error(f"Error obteniendo cursor: {e}")
            return None
    
    def test_connection(self) -> Dict[str, Any]:
        """Probar conexión y obtener información"""
        result = {
            "connected": False,
            "server_info": None,
            "database": None,
            "error": None
        }
        
        try:
            if self.connect():
                result["connected"] = True
                result["server_info"] = self.connection.get_server_info()
                result["database"] = self.config['database']
                
                # Probar una consulta simple
                cursor = self.connection.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                cursor.close()
                result["mysql_version"] = version[0] if version else "Unknown"
                
        except Exception as e:
            result["error"] = str(e)
            
        return result

# Singleton para conexión global
_db_instance = None

def get_db_connection() -> DatabaseConnection:
    """Obtener instancia singleton de la conexión"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseConnection()
    return _db_instance

def init_database() -> bool:
    """Inicializar base de datos"""
    db = get_db_connection()
    return db.connect()

def close_database() -> None:
    """Cerrar conexión global"""
    global _db_instance
    if _db_instance:
        _db_instance.disconnect()
        _db_instance = None
