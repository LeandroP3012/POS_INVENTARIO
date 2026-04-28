"""
Módulo de Conexión a la Base de Datos
Maneja la conexión y configuración de MySQL
"""

import mysql.connector
from mysql.connector import Error, errorcode
import json
import logging
from typing import Optional, List, Dict, Any
import sys
import os

# Agregar utils al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.path_manager import load_config, get_config_path

class DatabaseConnection:
    """Gestiona la conexión a la base de datos MySQL"""
    
    def __init__(self, config_file: str = 'database.json'):
        self.connection = None
        self.cursor = None
        self.config_file = config_file
        self.config = None
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Cargar configuración usando PathManager
        self.load_config()
    
    def load_config(self):
        """Cargar configuración de la base de datos.
        Prioridad: variables de entorno (Railway/producción) > database.json (local)
        """
        # 1. Variables de entorno tienen prioridad (Railway las inyecta automáticamente)
        if os.environ.get("DB_HOST"):
            self.config = {
                "host":            os.environ.get("DB_HOST", "localhost"),
                "port":            os.environ.get("DB_PORT", "3306"),
                "name":            os.environ.get("DB_NAME", "pos_system"),
                "user":            os.environ.get("DB_USER", "root"),
                "password":        os.environ.get("DB_PASSWORD", ""),
                "max_connections": os.environ.get("DB_MAX_CONNECTIONS", "10"),
                "timeout":         os.environ.get("DB_TIMEOUT", "30"),
            }
            self.logger.info("✅ Configuración DB cargada desde variables de entorno")
            return

        # 2. Fallback: leer database.json (entorno local)
        try:
            config_path = get_config_path(self.config_file)
            self.logger.info(f"🔍 DEBUG - Intentando leer: {config_path}")
            self.logger.info(f"🔍 DEBUG - ¿Archivo existe?: {config_path.exists()}")

            self.config = load_config(self.config_file)

            if not self.config:
                self.logger.error("No se pudo cargar la configuración de la base de datos")
                self.config = self._get_default_config()
            else:
                self.logger.info(f"✅ Configuración cargada desde: {config_path}")
                self.logger.info(f"🔍 DEBUG - Contenido leído: {self.config}")

        except Exception as e:
            self.logger.error(f"Error cargando configuración: {e}")
            self.config = self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """Obtener configuración por defecto"""
        return {
            "host": "localhost",
            "port": "3306",
            "name": "pos_system",
            "user": "root",
            "password": "",
            "max_connections": "10",
            "timeout": "30"
        }
    
    def connect(self) -> bool:
        """Establecer conexión con la base de datos"""
        try:
            if self._is_connection_alive():
                # ✅ Reducir logging: Solo log en DEBUG mode
                return True
            
            # DEBUG: Ver qué contiene self.config (solo en modo debug)
            # self.logger.debug(f"🔍 DEBUG - Config completa: {self.config}")
            
            # Parámetros de conexión — sin pool nombrado para evitar problemas
            # con el fork de procesos de uvicorn --reload
            connection_params = {
                'host': self.config.get('host', 'localhost'),
                'port': int(self.config.get('port', 3306)),
                'user': self.config.get('user', 'root'),
                'password': self.config.get('password', ''),
                'database': self.config.get('name', 'pos_system'),
                'charset': 'utf8mb4',
                'collation': 'utf8mb4_unicode_ci',
                'autocommit': True,
                'connect_timeout': 10,
                'use_pure': True,
            }
            
            # ✅ Solo log al reconectar, no en cada verificación
            self.logger.info(f"🔌 Conectando a MySQL: {connection_params['user']}@{connection_params['host']}:{connection_params['port']}/{connection_params['database']}")
            
            self.connection = mysql.connector.connect(**connection_params)
            
            if self._is_connection_alive():
                db_info = self.connection.get_server_info()
                self.logger.info(f"✅ Conectado a MySQL Server version {db_info}")
                return True
            
            return False
            
        except Error as e:
            self.logger.error(f"❌ Error al conectar a MySQL: {e}")
            return False
        except Exception as e:
            self.logger.error(f"❌ Error inesperado: {e}")
            return False
    
    def disconnect(self):
        """Cerrar conexión con la base de datos"""
        try:
            if self.cursor:
                self.cursor.close()
                self.cursor = None
            
            if self._is_connection_alive():
                self.connection.close()
                self.logger.info("✅ Conexión a MySQL cerrada")
                
        except Error as e:
            self.logger.error(f"❌ Error al cerrar conexión: {e}")
    
    def execute_query(self, query: str, params: tuple = None, fetch: bool = True, timeout: int = 30) -> Optional[List[Dict] | int]:
        """
        Ejecutar consulta SQL
        
        Args:
            query: Consulta SQL
            params: Parámetros para la consulta
            fetch: Si es True, retorna resultados. Si es False, retorna filas afectadas.
            timeout: Timeout en segundos para la consulta (default: 30)
        
        Returns:
            Lista de diccionarios (si fetch=True) o número de filas afectadas (si fetch=False)
        """
        attempts = 0

        while attempts < 2:
            cursor = None
            try:
                connection = self.ensure_connection()
                if not connection:
                    return None

                cursor = connection.cursor(dictionary=True)
                
                # ✅ Establecer timeout para la query
                if timeout:
                    cursor.execute(f"SET SESSION max_execution_time={timeout * 1000}")
                
                cursor.execute(query, params)

                if fetch:
                    result = cursor.fetchall()
                else:
                    result = cursor.rowcount
                    connection.commit()

                cursor.close()
                return result

            except Error as e:
                if cursor:
                    cursor.close()

                self.logger.error(f"❌ Error ejecutando query: {e}")
                self.logger.error(f"Query: {query}")
                self.logger.error(f"Params: {params}")

                if self.connection:
                    try:
                        self.connection.rollback()
                    except Exception:
                        pass

                if e.errno in (
                    errorcode.CR_SERVER_GONE_ERROR,
                    errorcode.CR_SERVER_LOST,
                    errorcode.CR_CONN_HOST_ERROR,
                    errorcode.ER_SERVER_SHUTDOWN,
                    2006,
                    2013,
                ):
                    self.logger.warning("🔄 Conexión MySQL perdida, intentando reconectar...")
                    self.connection = None
                    attempts += 1
                    continue

                break

            except Exception as e:
                if cursor:
                    cursor.close()
                self.logger.error(f"❌ Error inesperado: {e}")
                break

        return None
    
    def execute_many(self, query: str, data_list: List[tuple]) -> bool:
        """Ejecutar múltiples inserts/updates"""
        attempts = 0

        while attempts < 2:
            cursor = None
            try:
                connection = self.ensure_connection()
                if not connection:
                    return False

                cursor = connection.cursor()
                cursor.executemany(query, data_list)
                connection.commit()
                cursor.close()
                return True

            except Error as e:
                if cursor:
                    cursor.close()

                self.logger.error(f"❌ Error en execute_many: {e}")
                if self.connection:
                    try:
                        self.connection.rollback()
                    except Exception:
                        pass

                if e.errno in (
                    errorcode.CR_SERVER_GONE_ERROR,
                    errorcode.CR_SERVER_LOST,
                    errorcode.CR_CONN_HOST_ERROR,
                    errorcode.ER_SERVER_SHUTDOWN,
                    2006,
                    2013,
                ):
                    self.logger.warning("🔄 Conexión MySQL perdida durante execute_many, reintentando...")
                    self.connection = None
                    attempts += 1
                    continue

                break

            except Exception as e:
                if cursor:
                    cursor.close()
                self.logger.error(f"❌ Error inesperado en execute_many: {e}")
                break

        return False
    
    def test_connection(self) -> tuple[bool, str]:
        """Probar conexión a la base de datos"""
        try:
            if self.connect():
                # Ejecutar query simple
                result = self.execute_query("SELECT 1 as test")
                
                if result and result[0]['test'] == 1:
                    return True, "✅ Conexión exitosa"
                else:
                    return False, "❌ Error en query de prueba"
            else:
                return False, "❌ No se pudo conectar"
                
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
    
    def get_tables(self) -> List[str]:
        """Obtener lista de tablas en la base de datos"""
        try:
            result = self.execute_query("SHOW TABLES")
            if result:
                # El nombre de la columna varía según la BD
                key = list(result[0].keys())[0]
                return [row[key] for row in result]
            return []
        except Exception as e:
            self.logger.error(f"Error obteniendo tablas: {e}")
            return []
    
    def table_exists(self, table_name: str) -> bool:
        """Verificar si una tabla existe"""
        tables = self.get_tables()
        return table_name in tables

    def _is_connection_alive(self) -> bool:
        """Verificar si la conexión actual sigue activa."""
        if not self.connection:
            return False
        try:
            # ✅ Verificación rápida sin overhead
            return bool(self.connection.is_connected())
        except AttributeError:
            self.logger.warning("⚠️  Conexión inválida detectada (AttributeError), restableciendo handle.")
            self.connection = None
            return False
        except Exception as exc:
            # ✅ Solo log en caso de error real, no en verificaciones rutinarias
            self.logger.debug(f"Conexión perdida: {exc}")
            try:
                self.connection.close()
            except Exception:
                pass
            self.connection = None
            return False

    def ensure_connection(self):
        """Obtener una conexión activa, reconectando si es necesario."""
        if not self._is_connection_alive():
            self.logger.info("🔄 Reconectando a la base de datos...")
            if not self.connect():
                return None
        # Ping real al socket para detectar conexiones silenciosamente muertas
        try:
            self.connection.ping(reconnect=True, attempts=3, delay=1)
        except Exception:
            self.connection = None
            if not self.connect():
                return None
        return self.connection
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
    
    def __del__(self):
        """Destructor"""
        self.disconnect()


# Instancia global
_db_connection = None


def get_db_connection() -> DatabaseConnection:
    """Obtener instancia global de la conexión a la base de datos"""
    global _db_connection
    
    if _db_connection is None:
        _db_connection = DatabaseConnection()
    
    return _db_connection


def test_database_connection() -> tuple[bool, str]:
    """Probar conexión a la base de datos"""
    db = get_db_connection()
    return db.test_connection()


if __name__ == "__main__":
    # Prueba de conexión
    logging.basicConfig(level=logging.INFO)
    
    print("\n" + "=" * 60)
    print("PRUEBA DE CONEXIÓN A LA BASE DE DATOS")
    print("=" * 60 + "\n")
    
    # Mostrar ruta de configuración
    from utils.path_manager import get_config_path
    print(f"📁 Archivo de configuración: {get_config_path('database.json')}\n")
    
    # Probar conexión
    success, message = test_database_connection()
    print(f"\n{message}\n")
    
    if success:
        # Mostrar tablas
        db = get_db_connection()
        tables = db.get_tables()
        print(f"📊 Tablas encontradas ({len(tables)}):")
        for table in tables:
            print(f"   • {table}")
    
    print("\n" + "=" * 60 + "\n")
