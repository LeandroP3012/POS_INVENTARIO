#!/usr/bin/env python3
"""
Script de prueba para crear usuarios y debuggear el problema
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.user_controller import UserController
from controllers.role_controller import RoleController

def test_user_creation():
    """Probar la creación de usuarios"""
    try:
        print("=== PRUEBA DE CREACIÓN DE USUARIOS ===")
        
        # Inicializar controladores
        user_controller = UserController()
        role_controller = RoleController()
        
        # Obtener roles disponibles
        print("\n1. Obteniendo roles disponibles...")
        roles = role_controller.get_all_roles()
        print(f"Roles encontrados: {len(roles)}")
        for role in roles:
            print(f"  - {role.get('name', 'Sin nombre')} (ID: {role.get('id', 'N/A')})")
        
        if not roles:
            print("❌ No se encontraron roles. Esto puede ser el problema.")
            return False
        
        # Datos de prueba para crear usuario
        user_data = {
            'username': 'test_user',
            'full_name': 'Usuario de Prueba',
            'email': 'test@example.com',
            'password': 'test123',
            'user_type': roles[0].get('name', 'Cajero'),  # Usar el primer rol disponible
            'status': 'active'
        }
        
        print(f"\n2. Intentando crear usuario con datos:")
        for key, value in user_data.items():
            if key != 'password':
                print(f"  - {key}: {value}")
            else:
                print(f"  - {key}: ****")
        
        # Intentar crear usuario
        print("\n3. Creando usuario...")
        success = user_controller.create_user(user_data)
        
        if success:
            print("✅ Usuario creado exitosamente!")
            
            # Verificar que se creó
            print("\n4. Verificando creación...")
            users = user_controller.get_all_users()
            test_user = next((u for u in users if u.get('username') == 'test_user'), None)
            
            if test_user:
                print("✅ Usuario encontrado en la base de datos:")
                print(f"  - ID: {test_user.get('id')}")
                print(f"  - Username: {test_user.get('username')}")
                print(f"  - Nombre: {test_user.get('full_name')}")
                print(f"  - Email: {test_user.get('email')}")
                print(f"  - Rol: {test_user.get('user_type')}")
                print(f"  - Estado: {test_user.get('status')}")
            else:
                print("❌ Usuario no encontrado después de la creación")
                return False
            
            return True
        else:
            print("❌ Error creando usuario")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_database_connection():
    """Probar conexión a la base de datos"""
    try:
        print("=== PRUEBA DE CONEXIÓN A BASE DE DATOS ===")
        
        from database.connection import get_connection
        
        print("1. Intentando conectar a la base de datos...")
        connection = get_connection()
        
        if connection:
            print("✅ Conexión exitosa!")
            
            # Probar una consulta simple
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM users")
            result = cursor.fetchone()
            
            print(f"✅ Consulta exitosa. Usuarios en BD: {result['count'] if result else 'N/A'}")
            
            cursor.close()
            connection.close()
            return True
        else:
            print("❌ No se pudo establecer conexión")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

if __name__ == "__main__":
    print("INICIANDO DIAGNÓSTICO DEL SISTEMA DE USUARIOS\n")
    
    # Probar conexión
    db_ok = test_database_connection()
    print()
    
    if db_ok:
        # Probar creación de usuarios
        creation_ok = test_user_creation()
        
        if creation_ok:
            print("\n🎉 TODAS LAS PRUEBAS PASARON!")
            print("El problema parece estar en la interfaz gráfica, no en la lógica de negocio.")
        else:
            print("\n❌ PROBLEMA EN LA LÓGICA DE CREACIÓN")
    else:
        print("\n❌ PROBLEMA DE CONEXIÓN A BASE DE DATOS")
        print("Verifique que MySQL esté ejecutándose y la configuración sea correcta.")
