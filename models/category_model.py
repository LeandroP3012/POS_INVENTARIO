"""
Modelo de Categoría
Gestión de categorías de productos
"""

from typing import Dict, Any, List, Optional
from models.base_model import BaseModel
import logging


class CategoryModel(BaseModel):
    """Modelo para gestión de categorías"""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('model.CategoryModel')
        self.table_name = 'categories'

    def _table_has_column(self, table: str, column: str) -> bool:
        """Verificar columnas sin alterar estado base"""
        original = self.table_name
        self.table_name = table
        try:
            return self.has_column(column)
        finally:
            self.table_name = original

    def _product_status_clause(self) -> str:
        """Construir filtro seguro para productos activos"""
        if self._table_has_column('products', 'status'):
            return "p.status = 'active'"
        if self._table_has_column('products', 'active'):
            return 'p.active = 1'
        return '1=1'
    
    def get_connection(self):
        """Obtener conexión a la base de datos"""
        connection = super().get_connection()
        if not connection:
            self.logger.error("No se pudo obtener conexión a la base de datos")
        return connection
    
    def create_category(self, category_data: Dict[str, Any]) -> Optional[int]:
        """
        Crear una nueva categoría
        
        Args:
            category_data: Diccionario con datos de la categoría
            
        Returns:
            ID de la categoría creada o None si hay error
        """
        try:
            connection = self.get_connection()
            if not connection:
                self.logger.error("No hay conexión a la base de datos")
                return None
            
            cursor = connection.cursor()

            status_value = category_data.get('status', 'active') or 'active'
            has_status = self.has_column('status')
            has_active = self.has_column('active')

            columns: List[str] = ['name', 'description', 'parent_id']
            placeholders: List[str] = ['%s', '%s', '%s']
            values: List[Any] = [
                category_data['name'],
                category_data.get('description', ''),
                category_data.get('parent_id', None)
            ]

            if has_status:
                columns.append('status')
                placeholders.append('%s')
                values.append(status_value)
            elif has_active:
                columns.append('active')
                placeholders.append('%s')
                values.append(1 if status_value == 'active' else 0)

            query = f"""
                INSERT INTO categories (
                    {', '.join(columns)}
                ) VALUES (
                    {', '.join(placeholders)}
                )
            """

            cursor.execute(query, tuple(values))
            connection.commit()
            category_id = cursor.lastrowid
            
            self.logger.info(f"Categoría creada exitosamente: {category_data['name']} (ID: {category_id})")
            cursor.close()
            return category_id
            
        except Exception as e:
            self.logger.error(f"Error al crear categoría: {e}")
            if connection:
                connection.rollback()
            return None
    
    def get_all_categories(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """
        Obtener todas las categorías
        
        Args:
            include_inactive: Incluir categorías inactivas
            
        Returns:
            Lista de categorías
        """
        try:
            connection = self.get_connection()
            if not connection:
                self.logger.error("No hay conexión a la base de datos")
                return []
            
            cursor = connection.cursor(dictionary=True)
            
            has_status = self.has_column('status')
            has_active = self.has_column('active')

            product_status_clause = self._product_status_clause()

            status_select = "c.status" if has_status else (
                "CASE WHEN c.active = 1 THEN 'active' ELSE 'inactive' END"
                if has_active else "'active'"
            )

            query = f"""
                SELECT 
                    c.id,
                    c.name,
                    c.description,
                    c.parent_id,
                    {status_select} AS status,
                    c.created_at,
                    c.updated_at,
                    COUNT(p.id) as product_count,
                    pc.name as parent_name
                FROM categories c
                LEFT JOIN products p ON c.id = p.category_id AND {product_status_clause}
                LEFT JOIN categories pc ON c.parent_id = pc.id
            """

            conditions: List[str] = []
            if not include_inactive:
                if has_status:
                    conditions.append("c.status = 'active'")
                elif has_active:
                    conditions.append("c.active = 1")

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += """
                GROUP BY c.id, c.name, c.description, c.parent_id, status, c.created_at, c.updated_at, pc.name
                ORDER BY c.name ASC
            """

            cursor.execute(query)
            categories = cursor.fetchall()
            cursor.close()
            
            return categories
            
        except Exception as e:
            self.logger.error(f"Error al obtener categorías: {e}")
            return []
    
    def get_category_by_id(self, category_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtener categoría por ID
        
        Args:
            category_id: ID de la categoría
            
        Returns:
            Datos de la categoría o None
        """
        try:
            connection = self.get_connection()
            if not connection:
                return None
            
            cursor = connection.cursor(dictionary=True)
            
            has_status = self.has_column('status')
            has_active = self.has_column('active')

            status_select = "c.status" if has_status else (
                "CASE WHEN c.active = 1 THEN 'active' ELSE 'inactive' END"
                if has_active else "'active'"
            )

            product_status_clause = self._product_status_clause()

            query = f"""
                SELECT 
                    c.id,
                    c.name,
                    c.description,
                    c.parent_id,
                    {status_select} AS status,
                    c.created_at,
                    c.updated_at,
                    COUNT(p.id) as product_count,
                    pc.name as parent_name
                FROM categories c
                LEFT JOIN products p ON c.id = p.category_id AND {product_status_clause}
                LEFT JOIN categories pc ON c.parent_id = pc.id
                WHERE c.id = %s
                GROUP BY c.id, c.name, c.description, c.parent_id, status, c.created_at, c.updated_at, pc.name
            """

            cursor.execute(query, (category_id,))
            category = cursor.fetchone()
            cursor.close()
            
            return category
            
        except Exception as e:
            self.logger.error(f"Error al obtener categoría {category_id}: {e}")
            return None
    
    def update_category(self, category_id: int, category_data: Dict[str, Any]) -> bool:
        """
        Actualizar categoría
        
        Args:
            category_id: ID de la categoría
            category_data: Datos a actualizar
            
        Returns:
            True si se actualizó, False si no
        """
        try:
            connection = self.get_connection()
            if not connection:
                return False
            
            cursor = connection.cursor()
            
            # Construir query dinámicamente
            update_fields = []
            values = []
            
            if 'name' in category_data:
                update_fields.append("name = %s")
                values.append(category_data['name'])
            
            if 'description' in category_data:
                update_fields.append("description = %s")
                values.append(category_data['description'])
            
            if 'parent_id' in category_data:
                update_fields.append("parent_id = %s")
                values.append(category_data['parent_id'])
            
            has_status = self.has_column('status')
            has_active = self.has_column('active')

            if 'status' in category_data:
                status_value = category_data['status']
                if has_status:
                    update_fields.append("status = %s")
                    values.append(status_value)
                elif has_active:
                    update_fields.append("active = %s")
                    values.append(1 if status_value == 'active' else 0)
            elif 'active' in category_data and has_active:
                update_fields.append("active = %s")
                values.append(category_data['active'])
            
            if not update_fields:
                return False
            
            values.append(category_id)
            
            query = f"""
                UPDATE categories 
                SET {', '.join(update_fields)}
                WHERE id = %s
            """
            
            cursor.execute(query, values)
            connection.commit()
            
            affected_rows = cursor.rowcount
            cursor.close()
            
            if affected_rows > 0:
                self.logger.info(f"Categoría {category_id} actualizada exitosamente")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error al actualizar categoría {category_id}: {e}")
            if connection:
                connection.rollback()
            return False
    
    def delete_category(self, category_id: int) -> bool:
        """
        Eliminar categoría (soft delete)
        
        Args:
            category_id: ID de la categoría
            
        Returns:
            True si se eliminó, False si no
        """
        try:
            # No eliminar si tiene productos
            category = self.get_category_by_id(category_id)
            if category and category.get('product_count', 0) > 0:
                self.logger.warning(f"No se puede eliminar categoría {category_id}: tiene {category['product_count']} productos")
                return False

            if self.has_column('status'):
                return self.update_category(category_id, {'status': 'inactive'})
            elif self.has_column('active'):
                return self.update_category(category_id, {'active': 0})
            else:
                # Sin campos de estado, eliminar registro
                connection = self.get_connection()
                if not connection:
                    return False
                cursor = connection.cursor()
                cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
                connection.commit()
                return cursor.rowcount > 0
            
        except Exception as e:
            self.logger.error(f"Error al eliminar categoría {category_id}: {e}")
            return False
    
    def search_categories(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Buscar categorías por nombre o descripción
        
        Args:
            search_term: Término de búsqueda
            
        Returns:
            Lista de categorías encontradas
        """
        try:
            connection = self.get_connection()
            if not connection:
                return []
            
            cursor = connection.cursor(dictionary=True)
            
            has_status = self.has_column('status')
            has_active = self.has_column('active')

            product_status_clause = self._product_status_clause()

            status_filter = "c.status = 'active'" if has_status else (
                "c.active = 1" if has_active else '1=1'
            )

            status_select = "c.status" if has_status else (
                "CASE WHEN c.active = 1 THEN 'active' ELSE 'inactive' END"
                if has_active else "'active'"
            )

            query = f"""
                SELECT 
                    c.id,
                    c.name,
                    c.description,
                    c.parent_id,
                    {status_select} AS status,
                    c.created_at,
                    c.updated_at,
                    COUNT(p.id) as product_count,
                    pc.name as parent_name
                FROM categories c
                LEFT JOIN products p ON c.id = p.category_id AND {product_status_clause}
                LEFT JOIN categories pc ON c.parent_id = pc.id
                WHERE {status_filter}
                AND (
                    c.name LIKE %s 
                    OR c.description LIKE %s
                )
                GROUP BY c.id, c.name, c.description, c.parent_id, status, c.created_at, c.updated_at, pc.name
                ORDER BY c.name ASC
            """

            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern))
            categories = cursor.fetchall()
            cursor.close()
            
            return categories
            
        except Exception as e:
            self.logger.error(f"Error al buscar categorías: {e}")
            return []
