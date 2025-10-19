"""
Modelo para gestión de clientes
Autor: Sistema POS
Fecha: 2025
"""

from models.base_model import BaseModel

class CustomerModel(BaseModel):
    """Modelo para operaciones de clientes"""
    
    def __init__(self):
        super().__init__()
        self.table_name = "customers"
    
    def get_all_active(self):
        """Obtiene todos los clientes activos"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT * FROM customers
                WHERE status = 'active'
                ORDER BY name
            """
            cursor.execute(query)
            customers = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            return customers
            
        except Exception as e:
            print(f"❌ Error al obtener clientes: {e}")
            return []
    
    def get_generic_customer(self):
        """Obtiene el cliente genérico"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM customers WHERE code = 'GENERIC' LIMIT 1"
            cursor.execute(query)
            customer = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            return customer
            
        except Exception as e:
            print(f"❌ Error al obtener cliente genérico: {e}")
            return None
    
    def search_customers(self, search_text):
        """Busca clientes por nombre o documento"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT * FROM customers
                WHERE status = 'active'
                AND (
                    name LIKE %s 
                    OR document_number LIKE %s
                    OR code LIKE %s
                )
                ORDER BY name
                LIMIT 50
            """
            search_param = f"%{search_text}%"
            cursor.execute(query, (search_param, search_param, search_param))
            customers = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            return customers
            
        except Exception as e:
            print(f"❌ Error al buscar clientes: {e}")
            return []
    
    def create_customer(self, customer_data):
        """Crea un nuevo cliente"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # Generar código automático si no viene
            if 'code' not in customer_data or not customer_data['code']:
                customer_data['code'] = self._generate_customer_code(cursor)
            
            query = """
                INSERT INTO customers (
                    code, name, document_type, document_number,
                    email, phone, address, city, country,
                    tax_id, customer_type, credit_limit,
                    status, created_by
                ) VALUES (
                    %(code)s, %(name)s, %(document_type)s, %(document_number)s,
                    %(email)s, %(phone)s, %(address)s, %(city)s, %(country)s,
                    %(tax_id)s, %(customer_type)s, %(credit_limit)s,
                    %(status)s, %(created_by)s
                )
            """
            cursor.execute(query, customer_data)
            connection.commit()
            
            customer_id = cursor.lastrowid
            
            cursor.close()
            connection.close()
            
            print(f"✅ Cliente creado exitosamente (ID: {customer_id})")
            return customer_id
            
        except Exception as e:
            print(f"❌ Error al crear cliente: {e}")
            return None
    
    def _generate_customer_code(self, cursor):
        """Genera código único de cliente (CLI-00001)"""
        query = """
            SELECT code FROM customers 
            WHERE code LIKE 'CLI-%'
            ORDER BY id DESC 
            LIMIT 1
        """
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            last_number = int(result[0].split('-')[-1])
            new_number = last_number + 1
        else:
            new_number = 1
        
        return f"CLI-{new_number:05d}"
