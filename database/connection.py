"""
Módulo de Conexión a la Base de Datos
Maneja la conexión y configuración de MySQL mediante pool de conexiones
"""

import mysql.connector
from mysql.connector import Error, pooling
import logging
import os
import sys
from typing import Optional, List, Dict, Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.path_manager import load_config, get_config_path


# Pool global — thread-safe por diseño
_connection_pool: Optional[pooling.MySQLConnectionPool] = None


def _load_config() -> dict:
    """Carga config desde env vars (Railway) o database.json (local)."""
    if os.environ.get("DB_HOST"):
        return {
            "host":            os.environ.get("DB_HOST", "localhost"),
            "port":            os.environ.get("DB_PORT", "3306"),
            "name":            os.environ.get("DB_NAME", "pos_system"),
            "user":            os.environ.get("DB_USER", "root"),
            "password":        os.environ.get("DB_PASSWORD", ""),
            "max_connections": os.environ.get("DB_MAX_CONNECTIONS", "10"),
            "timeout":         os.environ.get("DB_TIMEOUT", "30"),
        }
    try:
        cfg = load_config("database.json")
        return cfg or _default_config()
    except Exception:
        return _default_config()


def _default_config() -> dict:
    return {
        "host": "localhost", "port": "3306", "name": "pos_system",
        "user": "root", "password": "", "max_connections": "10", "timeout": "30",
    }


def _get_pool() -> pooling.MySQLConnectionPool:
    """Inicializar el pool una sola vez (thread-safe por GIL + check doble)."""
    global _connection_pool
    if _connection_pool is not None:
        return _connection_pool

    config = _load_config()

    _connection_pool = pooling.MySQLConnectionPool(
        pool_name="pos_pool",
        pool_size=int(config.get("max_connections", 10)),
        pool_reset_session=True,
        host=config["host"],
        port=int(config["port"]),
        user=config["user"],
        password=config["password"],
        database=config["name"],
        charset="utf8mb4",
        collation="utf8mb4_unicode_ci",
        autocommit=True,
        connect_timeout=10,
        use_pure=True,
    )

    logging.getLogger("DatabasePool").info(
        f"✅ Pool MySQL creado ({config['user']}@{config['host']}:{config['port']}/{config['name']}, "
        f"size={config.get('max_connections', 10)})"
    )
    return _connection_pool


class DatabaseConnection:
    """
    Wrapper que toma/devuelve conexiones del pool.
    Cada instancia obtiene su propia conexión → no hay estado compartido entre threads.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._cnx = None  # conexión tomada del pool

    # ------------------------------------------------------------------
    # Gestión de conexión
    # ------------------------------------------------------------------

    def connect(self) -> bool:
        try:
            if self._cnx and self._cnx.is_connected():
                return True
            self._cnx = _get_pool().get_connection()
            self.logger.info("✅ Conexión obtenida del pool")
            return True
        except Error as e:
            self.logger.error(f"❌ Error al conectar a MySQL: {e}")
            return False

    def disconnect(self):
        """Devuelve la conexión al pool."""
        try:
            if self._cnx:
                self._cnx.close()   # Con pool, esto la devuelve; no la destruye
                self._cnx = None
        except Error as e:
            self.logger.error(f"❌ Error al cerrar conexión: {e}")

    def ensure_connection(self):
        """Garantiza una conexión activa desde el pool."""
        try:
            if self._cnx and self._cnx.is_connected():
                return self._cnx
            self._cnx = _get_pool().get_connection()
            return self._cnx
        except Error as e:
            self.logger.error(f"❌ No se pudo obtener conexión del pool: {e}")
            return None

    # ------------------------------------------------------------------
    # Ejecución de queries
    # ------------------------------------------------------------------

    def execute_query(
        self,
        query: str,
        params: tuple = None,
        fetch: bool = True,
        timeout: int = 30,
    ) -> Optional[List[Dict] | int]:
        for attempt in range(2):
            cursor = None
            try:
                cnx = self.ensure_connection()
                if not cnx:
                    return None

                cursor = cnx.cursor(dictionary=True)
                if timeout:
                    cursor.execute(f"SET SESSION max_execution_time={timeout * 1000}")
                cursor.execute(query, params)

                if fetch:
                    result = cursor.fetchall()
                else:
                    result = cursor.rowcount
                    cnx.commit()

                cursor.close()
                return result

            except Error as e:
                if cursor:
                    try: cursor.close()
                    except Exception: pass

                self.logger.error(f"❌ Error ejecutando query (intento {attempt+1}): {e}")

                if e.errno in (2006, 2013, 2055):   # conexión muerta
                    self._cnx = None
                    continue
                break

            except Exception as e:
                if cursor:
                    try: cursor.close()
                    except Exception: pass
                self.logger.error(f"❌ Error inesperado: {e}")
                break

        return None



    def execute_many(self, query: str, data_list: List[tuple]) -> bool:
        for attempt in range(2):
            cursor = None
            try:
                cnx = self.ensure_connection()
                if not cnx:
                    return False

                cursor = cnx.cursor()
                cursor.executemany(query, data_list)
                cnx.commit()
                cursor.close()
                return True

            except Error as e:
                if cursor:
                    try: cursor.close()
                    except Exception: pass
                self.logger.error(f"❌ Error en execute_many: {e}")
                if e.errno in (2006, 2013, 2055):
                    self._cnx = None
                    continue
                break

            except Exception as e:
                if cursor:
                    try: cursor.close()
                    except Exception: pass
                self.logger.error(f"❌ Error inesperado en execute_many: {e}")
                break

        return False

    def test_connection(self) -> tuple[bool, str]:
        try:
            if self.connect():
                result = self.execute_query("SELECT 1 as test")
                if result and result[0]["test"] == 1:
                    return True, "✅ Conexión exitosa"
                return False, "❌ Error en query de prueba"
            return False, "❌ No se pudo conectar"
        except Exception as e:
            return False, f"❌ Error: {e}"

    def get_tables(self) -> List[str]:
        result = self.execute_query("SHOW TABLES")
        if result:
            key = list(result[0].keys())[0]
            return [row[key] for row in result]
        return []

    def table_exists(self, table_name: str) -> bool:
        return table_name in self.get_tables()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def __del__(self):
        self.disconnect()


# ------------------------------------------------------------------
# API pública — compatible con el código existente
# ------------------------------------------------------------------

def get_db_connection() -> DatabaseConnection:
    """
    Retorna una NUEVA instancia por llamada.
    Cada request/thread obtiene su propia conexión del pool.
    """
    return DatabaseConnection()


def test_database_connection() -> tuple[bool, str]:
    with DatabaseConnection() as db:
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
