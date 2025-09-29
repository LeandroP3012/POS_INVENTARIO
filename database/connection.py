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
                    return json.load(file)
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
                    "ssl_disabled": True
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
            self.connection = mysql.connector.connect(
                host=self.config['host'],
                port=self.config['port'],
                database=self.config['database'],
                user=self.config['username'],
                password=self.config['password'],
                charset=self.config['charset'],
                autocommit=self.config.get('autocommit', True),
                connection_timeout=self.config.get('connection_timeout', 10),
                ssl_disabled=self.config.get('ssl_disabled', True)
            )
            
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
            cursor.execute(query, params or ())
            
            if fetch and query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                affected_rows = cursor.rowcount
                cursor.close()
                return affected_rows
                
        except Error as e:
            self.logger.error(f"Error ejecutando query: {e}")
            self.logger.error(f"Query: {query}")
            self.logger.error(f"Params: {params}")
            return None
        except Exception as e:
            self.logger.error(f"Error inesperado en query: {e}")
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
