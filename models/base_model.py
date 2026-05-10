"""
Modelo Base para el Sistema POS
Proporciona funcionalidad común para todos los modelos
"""

import os
import sys
import logging
import time
from typing import Dict, Any, Optional, List
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from database.connection import get_db_connection, _get_pool
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    _get_pool = None
    print("⚠️ Base de datos no disponible en base_model")

class _PooledConnectionWrapper:
    """
    Envuelve una PooledMySQLConnection para garantizar que siempre se
    devuelva al pool (vía close()) incluso si el código que la usa
    olvida llamar close() explícitamente.
    """

    def __init__(self, cnx):
        object.__setattr__(self, '_cnx', cnx)

    def __getattr__(self, name):
        cnx = object.__getattribute__(self, '_cnx')
        if cnx is None:
            raise AttributeError(f"Conexión cerrada, no se puede acceder a '{name}'")
        return getattr(cnx, name)

    def close(self):
        cnx = object.__getattribute__(self, '_cnx')
        if cnx is not None:
            try:
                cnx.close()
            except Exception:
                pass
            object.__setattr__(self, '_cnx', None)

    def __del__(self):
        """Garantía de seguridad: devuelve al pool si el caller olvidó close()."""
        self.close()


class BaseModel:
    """Clase base para todos los modelos del sistema"""
    
    def __init__(self):
        self.db = None
        self.table_name = None  # Debe ser definido en clases hijas
        self.primary_key = 'id'  # Llave primaria por defecto
        
        if DB_AVAILABLE:
            self.db = get_db_connection()
        
        # Configurar logging
        self.setup_logging()
    
    def setup_logging(self):
        """Configurar sistema de logging para modelos"""
        self.logger = logging.getLogger(f'model.{self.__class__.__name__}')
    
    def get_connection(self, max_retries: int = 3, retry_delay: float = 0.4):
        """
        Obtener conexión fresca del pool con reintentos.
        Si el pool está agotado, espera un poco y vuelve a intentar hasta
        max_retries veces antes de devolver None.
        """
        if not DB_AVAILABLE or _get_pool is None:
            self.logger.error("DB no disponible")
            return None
        for attempt in range(max_retries):
            try:
                raw = _get_pool().get_connection()
                return _PooledConnectionWrapper(raw)
            except Exception as exc:
                if attempt < max_retries - 1:
                    self.logger.warning(
                        f"Pool ocupado, reintentando ({attempt + 1}/{max_retries}): {exc}"
                    )
                    time.sleep(retry_delay)
                else:
                    self.logger.error(
                        f"Error obteniendo conexión del pool: {exc}"
                    )
        return None
    
    def connect(self) -> bool:
        """Establecer conexión con la base de datos"""
        if not self.db:
            return False
        
        try:
            return self.db.connect()
        except Exception as e:
            self.logger.error(f"Error conectando a BD: {e}")
            return False
    
    def disconnect(self):
        """Cerrar conexión con la base de datos"""
        if self.db:
            self.db.disconnect()
    
    def execute_query(self, query: str, params: tuple = None, fetch: bool = True) -> Optional[List[Dict]]:
        """Ejecutar consulta SQL"""
        if not self.db:
            return None
        
        try:
            return self.db.execute_query(query, params, fetch)
        except Exception as e:
            self.logger.error(f"Error ejecutando query: {e}")
            return None
    
    def find_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
        """Buscar registro por ID"""
        if not self.table_name:
            raise NotImplementedError("table_name debe ser definido en la clase hija")
        
        query = f"SELECT * FROM {self.table_name} WHERE {self.primary_key} = %s"
        result = self.execute_query(query, (record_id,))
        
        return result[0] if result else None
    
    def find_by_field(self, field: str, value: Any) -> Optional[Dict[str, Any]]:
        """Buscar registro por campo específico"""
        if not self.table_name:
            raise NotImplementedError("table_name debe ser definido en la clase hija")
        
        query = f"SELECT * FROM {self.table_name} WHERE {field} = %s"
        result = self.execute_query(query, (value,))
        
        return result[0] if result else None
    
    def find_all(self, conditions: Dict[str, Any] = None, limit: int = None) -> List[Dict[str, Any]]:
        """Buscar todos los registros con condiciones opcionales"""
        if not self.table_name:
            raise NotImplementedError("table_name debe ser definido en la clase hija")
        
        query = f"SELECT * FROM {self.table_name}"
        params = []
        
        if conditions:
            where_clauses = []
            for field, value in conditions.items():
                where_clauses.append(f"{field} = %s")
                params.append(value)
            
            query += " WHERE " + " AND ".join(where_clauses)
        
        if limit:
            query += f" LIMIT {limit}"
        
        result = self.execute_query(query, tuple(params) if params else None)
        return result if result else []
    
    def create(self, data: Dict[str, Any]) -> Optional[int]:
        """Crear nuevo registro"""
        if not self.table_name:
            raise NotImplementedError("table_name debe ser definido en la clase hija")
        
        # Agregar timestamps si no existen
        if 'created_at' not in data and self.has_column('created_at'):
            data['created_at'] = datetime.now()
        
        if 'updated_at' not in data and self.has_column('updated_at'):
            data['updated_at'] = datetime.now()
        
        fields = list(data.keys())
        placeholders = ', '.join(['%s'] * len(fields))
        fields_str = ', '.join(fields)
        
        query = f"INSERT INTO {self.table_name} ({fields_str}) VALUES ({placeholders})"
        
        result = self.execute_query(query, tuple(data.values()), fetch=False)
        
        if result is not None and result > 0:
            # Obtener el ID del registro creado
            last_id_query = "SELECT LAST_INSERT_ID() as last_id"
            last_id_result = self.execute_query(last_id_query)
            return last_id_result[0]['last_id'] if last_id_result else None
        
        return None
    
    def update(self, record_id: int, data: Dict[str, Any]) -> bool:
        """Actualizar registro existente"""
        if not self.table_name:
            raise NotImplementedError("table_name debe ser definido en la clase hija")
        
        # Agregar timestamp de actualización
        if 'updated_at' not in data and self.has_column('updated_at'):
            data['updated_at'] = datetime.now()
        
        set_clauses = []
        params = []
        
        for field, value in data.items():
            set_clauses.append(f"{field} = %s")
            params.append(value)
        
        params.append(record_id)
        
        query = f"UPDATE {self.table_name} SET {', '.join(set_clauses)} WHERE {self.primary_key} = %s"
        
        self.logger.info(f"🔧 BaseModel.update - Table: {self.table_name}, ID: {record_id}")
        self.logger.info(f"🔧 BaseModel.update - Data: {data}")
        print(f"🔧 UPDATE Table: {self.table_name}, ID: {record_id}")
        print(f"🔧 UPDATE Data: {data}")
        
        result = self.execute_query(query, tuple(params), fetch=False)
        
        self.logger.info(f"🔧 BaseModel.update - Rows affected: {result}")
        print(f"🔧 ROWS AFFECTED: {result}")
        
        # Si no hubo filas afectadas, puede ser porque los datos ya eran iguales
        # En ese caso, verificar si el registro existe
        if result == 0:
            self.logger.info(f"⚠️ 0 filas afectadas, verificando si registro existe...")
            print(f"⚠️ 0 filas afectadas, verificando existencia...")
            existing = self.find_by_id(record_id)
            if existing:
                self.logger.info(f"✅ Registro existe, valores ya eran iguales - considerando exitoso")
                print(f"✅ Registro existe - update considerado exitoso")
                return True  # Considerarlo exitoso si el registro existe
            else:
                self.logger.warning(f"❌ Registro {record_id} no existe en {self.table_name}")
                print(f"❌ Registro no existe")
                return False
        
        return result is not None and result > 0
    
    def delete(self, record_id: int) -> bool:
        """Eliminar registro"""
        if not self.table_name:
            raise NotImplementedError("table_name debe ser definido en la clase hija")
        
        query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} = %s"
        result = self.execute_query(query, (record_id,), fetch=False)
        
        return result is not None and result > 0
    
    def soft_delete(self, record_id: int) -> bool:
        """Eliminación suave (marcar como inactivo)"""
        if not self.has_column('active'):
            return self.delete(record_id)
        
        return self.update(record_id, {'active': False})
    
    def count(self, conditions: Dict[str, Any] = None) -> int:
        """Contar registros"""
        if not self.table_name:
            raise NotImplementedError("table_name debe ser definido en la clase hija")
        
        query = f"SELECT COUNT(*) as total FROM {self.table_name}"
        params = []
        
        if conditions:
            where_clauses = []
            for field, value in conditions.items():
                where_clauses.append(f"{field} = %s")
                params.append(value)
            
            query += " WHERE " + " AND ".join(where_clauses)
        
        result = self.execute_query(query, tuple(params) if params else None)
        return result[0]['total'] if result else 0
    
    def exists(self, conditions: Dict[str, Any]) -> bool:
        """Verificar si existe un registro con las condiciones dadas"""
        return self.count(conditions) > 0
    
    def has_column(self, column_name: str) -> bool:
        """Verificar si la tabla tiene una columna específica"""
        if not self.table_name:
            return False
        
        query = """
        SELECT COUNT(*) as count 
        FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() 
        AND TABLE_NAME = %s 
        AND COLUMN_NAME = %s
        """
        
        result = self.execute_query(query, (self.table_name, column_name))
        return result[0]['count'] > 0 if result else False
    
    def get_table_info(self) -> List[Dict[str, Any]]:
        """Obtener información de la estructura de la tabla"""
        if not self.table_name:
            return []
        
        query = f"DESCRIBE {self.table_name}"
        result = self.execute_query(query)
        
        return result if result else []
    
    def validate_data(self, data: Dict[str, Any], is_update: bool = False) -> tuple[bool, List[str]]:
        """Validar datos antes de insertar/actualizar (debe ser implementado por clases hijas)"""
        return True, []
    
    def before_create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Hook que se ejecuta antes de crear (puede ser sobrescrito)"""
        return data
    
    def after_create(self, record_id: int, data: Dict[str, Any]):
        """Hook que se ejecuta después de crear (puede ser sobrescrito)"""
        pass
    
    def before_update(self, record_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Hook que se ejecuta antes de actualizar (puede ser sobrescrito)"""
        return data
    
    def after_update(self, record_id: int, data: Dict[str, Any]):
        """Hook que se ejecuta después de actualizar (puede ser sobrescrito)"""
        pass
    
    def before_delete(self, record_id: int) -> bool:
        """Hook que se ejecuta antes de eliminar (puede ser sobrescrito)"""
        return True
    
    def after_delete(self, record_id: int):
        """Hook que se ejecuta después de eliminar (puede ser sobrescrito)"""
        pass
    
    def to_dict(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Convertir registro de BD a diccionario (puede ser sobrescrito para personalizar)"""
        return dict(record) if record else {}
    
    def sanitize_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitizar datos de entrada"""
        sanitized = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                # Limpiar espacios extra
                sanitized[key] = value.strip()
            else:
                sanitized[key] = value
        
        return sanitized
    
    def log_activity(self, action: str, record_id: int = None, description: str = None, user_id: int = None):
        """Registrar actividad en logs (si existe la tabla activity_logs)"""
        try:
            if not self.has_table('activity_logs'):
                return
            
            log_data = {
                'user_id': user_id,
                'action': action,
                'table_name': self.table_name,
                'record_id': record_id,
                'description': description or f"{action} en {self.table_name}",
                'created_at': datetime.now()
            }
            
            # Crear instancia temporal para logs
            from models.activity_log_model import ActivityLogModel
            activity_log = ActivityLogModel()
            activity_log.create(log_data)
            
        except Exception as e:
            self.logger.warning(f"No se pudo registrar actividad: {e}")
    
    def has_table(self, table_name: str) -> bool:
        """Verificar si existe una tabla en la base de datos"""
        query = """
        SELECT COUNT(*) as count 
        FROM information_schema.TABLES 
        WHERE TABLE_SCHEMA = DATABASE() 
        AND TABLE_NAME = %s
        """
        
        result = self.execute_query(query, (table_name,))
        return result[0]['count'] > 0 if result else False
    
    def __str__(self):
        return f"{self.__class__.__name__}(table={self.table_name})"
    
    def __repr__(self):
        return self.__str__()
