#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de resolución de problemas de autenticación
Sistema POS - Diagnóstico y reparación de credenciales
"""

import hashlib
import json
import os
import sys
from datetime import datetime

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user_model import UserModel
from database.connection import DatabaseConnection

class AuthDebugTool:
    """Herramienta de depuración para problemas de autenticación"""
    
    def __init__(self):
        self.user_model = UserModel()
        self.db = DatabaseConnection()
        
    def hash_password(self, password: str) -> str:
        """Crear hash SHA-256 de la contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def test_database_connection(self):
        """Probar conexión a la base de datos"""
        print("=" * 50)
        print("PRUEBA DE CONEXION A BASE DE DATOS")
        print("=" * 50)
        
        if self.db.connect():
            print("OK - Conexion a base de datos: EXITOSA")
            print(f"   Host: {self.db.host}")
            print(f"   Base de datos: {self.db.database}")
            print(f"   Usuario: {self.db.user}")
            return True
        else:
            print("ERROR - Conexion a base de datos: FALLO")
            print("   Usando usuarios por defecto")
            return False
    
    def check_users_table(self):
        """Verificar tabla de usuarios"""
        print("\n" + "=" * 50)
        print("VERIFICATION DE TABLA USERS")
        print("=" * 50)
        
        if not self.db.connect():
            print("ERROR - No se puede conectar a la base de datos")
            return False
        
        try:
            # Verificar si existe la tabla users
            query = "SHOW TABLES LIKE 'users'"
            result = self.db.execute_query(query)
            
            if not result:
                print("ERROR - Tabla 'users' no existe")
                return False
            
            print("OK - Tabla 'users' existe")
            
            # Obtener estructura de la tabla
            query = "DESCRIBE users"
            columns = self.db.execute_query(query)
            
            print("\nEstructura de la tabla:")
            for col in columns:
                print(f"   - {col['Field']}: {col['Type']}")
            
            # Contar usuarios
            query = "SELECT COUNT(*) as count FROM users"
            result = self.db.execute_query(query)
            user_count = result[0]['count'] if result else 0
            
            print(f"\nTotal de usuarios: {user_count}")
            return True
            
        except Exception as e:
            print(f"ERROR - Error verificando tabla users: {e}")
            return False
    
    def list_all_users(self):
        """Listar todos los usuarios en la base de datos"""
        print("\n" + "=" * 50)
        print("LISTADO DE USUARIOS")
        print("=" * 50)
        
        if not self.db.connect():
            print("ERROR - No se puede conectar a la base de datos")
            print("\nUsuarios por defecto:")
            default_users = self.user_model.default_users
            for username, user_data in default_users.items():
                print(f"   Usuario: {username} ({user_data.get('full_name', 'N/A')})")
                print(f"      - Tipo: {user_data.get('user_type', 'N/A')}")
                print(f"      - Activo: {user_data.get('active', 'N/A')}")
                print(f"      - Hash: {user_data.get('password_hash', 'N/A')[:20]}...")
            return
        
        try:
            query = """
            SELECT id, username, full_name, user_type, active, 
                   password_hash, created_at, last_login
            FROM users 
            ORDER BY id
            """
            
            users = self.db.execute_query(query)
            
            if not users:
                print("ERROR - No se encontraron usuarios en la base de datos")
                return
            
            for user in users:
                status = "ACTIVO" if user.get('active') else "INACTIVO"
                print(f"{status} - ID: {user.get('id', 'N/A')}")
                print(f"   Usuario: {user.get('username', 'N/A')}")
                print(f"   Nombre: {user.get('full_name', 'N/A')}")
                print(f"   Tipo: {user.get('user_type', 'N/A')}")
                print(f"   Hash: {user.get('password_hash', 'N/A')[:20]}...")
                print(f"   Creado: {user.get('created_at', 'N/A')}")
                print(f"   Ultimo acceso: {user.get('last_login', 'Nunca')}")
                print()
                
        except Exception as e:
            print(f"ERROR - Error listando usuarios: {e}")
    
    def test_admin_credentials(self):
        """Probar credenciales del administrador"""
        print("\n" + "=" * 50)
        print("PRUEBA DE CREDENCIALES ADMIN")
        print("=" * 50)
        
        username = "admin"
        password = "123456"
        expected_hash = self.hash_password(password)
        
        print(f"Probando: {username} / {password}")
        print(f"Hash esperado: {expected_hash}")
        
        # Buscar usuario admin
        user_data = self.user_model.find_by_username(username)
        
        if not user_data:
            print("ERROR - Usuario 'admin' no encontrado")
            return False
        
        print(f"OK - Usuario encontrado: {user_data.get('full_name', 'N/A')}")
        
        stored_hash = user_data.get('password_hash', '')
        print(f"Hash almacenado: {stored_hash}")
        
        # Verificar contraseña
        if self.user_model.verify_password(password, stored_hash):
            print("OK - Contraseña CORRECTA")
            
            # Verificar si el usuario está activo
            if user_data.get('active', True):
                print("OK - Usuario ACTIVO")
            else:
                print("ERROR - Usuario INACTIVO")
                return False
            
            # Verificar si está bloqueado
            if self.user_model.is_user_locked(user_data):
                print("ERROR - Usuario BLOQUEADO")
                return False
            else:
                print("OK - Usuario NO bloqueado")
            
            return True
        else:
            print("ERROR - Contraseña INCORRECTA")
            print(f"   Hash esperado: {expected_hash}")
            print(f"   Hash almacenado: {stored_hash}")
            print(f"   Coinciden: {expected_hash == stored_hash}")
            return False
    
    def test_authentication_flow(self):
        """Probar todo el flujo de autenticación"""
        print("\n" + "=" * 50)
        print("PRUEBA COMPLETA DE AUTENTICACION")
        print("=" * 50)
        
        username = "admin"
        password = "123456"
        
        print(f"Iniciando autenticacion para: {username}")
        
        # Intentar autenticación
        user_data = self.user_model.authenticate(username, password)
        
        if user_data:
            print("OK - AUTENTICACION EXITOSA")
            print(f"   ID: {user_data.get('id', 'N/A')}")
            print(f"   Usuario: {user_data.get('username', 'N/A')}")
            print(f"   Nombre: {user_data.get('full_name', 'N/A')}")
            print(f"   Tipo: {user_data.get('user_type', 'N/A')}")
            print(f"   Permisos: {len(user_data.get('permissions', {}))}")
            return True
        else:
            print("ERROR - AUTENTICACION FALLO")
            return False
    
    def fix_admin_password(self):
        """Reparar contraseña del administrador"""
        print("\n" + "=" * 50)
        print("REPARACION DE CONTRASEÑA ADMIN")
        print("=" * 50)
        
        if not self.db.connect():
            print("ERROR - No se puede conectar a la base de datos para reparar")
            return False
        
        username = "admin"
        password = "123456"
        correct_hash = self.hash_password(password)
        
        try:
            # Actualizar contraseña del admin
            query = """
            UPDATE users 
            SET password_hash = %s, 
                failed_attempts = 0, 
                locked_until = NULL,
                active = TRUE,
                updated_at = %s
            WHERE username = %s
            """
            
            params = (correct_hash, datetime.now(), username)
            
            if self.db.execute_query(query, params, fetch=False):
                print(f"OK - Contraseña del usuario '{username}' actualizada correctamente")
                print(f"   Nueva contraseña: {password}")
                print(f"   Hash: {correct_hash}")
                return True
            else:
                print("ERROR - Error actualizando contraseña")
                return False
                
        except Exception as e:
            print(f"ERROR - Error reparando contraseña: {e}")
            return False
    
    def create_admin_if_missing(self):
        """Crear usuario admin si no existe"""
        print("\n" + "=" * 50)
        print("CREACION DE USUARIO ADMIN")
        print("=" * 50)
        
        if not self.db.connect():
            print("ERROR - No se puede conectar a la base de datos")
            return False
        
        # Verificar si admin existe
        user_data = self.user_model.find_by_username("admin")
        if user_data:
            print("OK - Usuario admin ya existe")
            return True
        
        try:
            admin_data = {
                'username': 'admin',
                'password_hash': self.hash_password('123456'),
                'email': 'admin@sistema-pos.com',
                'full_name': 'Administrador del Sistema',
                'user_type': 'admin',
                'active': True,
                'permissions': json.dumps({'all_modules': True, 'super_admin': True}),
                'created_at': datetime.now()
            }
            
            admin_id = self.user_model.create(admin_data)
            
            if admin_id:
                print(f"OK - Usuario admin creado con ID: {admin_id}")
                print("   Usuario: admin")
                print("   Contraseña: 123456")
                return True
            else:
                print("ERROR - Error creando usuario admin")
                return False
                
        except Exception as e:
            print(f"ERROR - Error creando admin: {e}")
            return False
    
    def run_full_diagnosis(self):
        """Ejecutar diagnóstico completo"""
        print("DIAGNOSTICO COMPLETO DEL SISTEMA DE AUTENTICACION")
        print("=" * 70)
        
        # 1. Probar conexión
        db_connected = self.test_database_connection()
        
        # 2. Verificar tabla users
        if db_connected:
            self.check_users_table()
        
        # 3. Listar usuarios
        self.list_all_users()
        
        # 4. Probar credenciales admin
        admin_works = self.test_admin_credentials()
        
        # 5. Probar flujo completo
        auth_works = self.test_authentication_flow()
        
        # 6. Resumen
        print("\n" + "=" * 50)
        print("RESUMEN DEL DIAGNOSTICO")
        print("=" * 50)
        
        print(f"Conexion BD: {'OK' if db_connected else 'ERROR'}")
        print(f"Credenciales Admin: {'OK' if admin_works else 'ERROR'}")
        print(f"Flujo Autenticacion: {'OK' if auth_works else 'ERROR'}")
        
        if not admin_works or not auth_works:
            print("\nSE DETECTARON PROBLEMAS")
            print("TIP: Ejecuta con --fix para intentar repararlos")
        else:
            print("\nSISTEMA DE AUTENTICACION FUNCIONANDO CORRECTAMENTE")

def main():
    """Función principal"""
    tool = AuthDebugTool()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--fix":
        print("MODO REPARACION ACTIVADO")
        print("=" * 50)
        
        # Intentar reparar
        if tool.create_admin_if_missing():
            tool.fix_admin_password()
        
        print("\nVerificando reparacion...")
        tool.test_admin_credentials()
        tool.test_authentication_flow()
    else:
        # Solo diagnóstico
        tool.run_full_diagnosis()

if __name__ == "__main__":
    main()
