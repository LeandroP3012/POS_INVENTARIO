#!/usr/bin/env python3
"""
Script para verificar la estructura de la tabla users
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.connection import get_db_connection

def check_users_table():
    """Verificar estructura de la tabla users"""
    print("=== VERIFICANDO ESTRUCTURA DE TABLA USERS ===")
    
    try:
        db = get_db_connection()
        
        if db.connect():
            print("✅ Conectado a la base de datos")
            
            # Describir tabla users
            result = db.execute_query("DESCRIBE users")
            if result:
                print("\n📋 Estructura de la tabla 'users':")
                print("-" * 60)
                for column in result:
                    print(f"Campo: {column['Field']}")
                    print(f"  Tipo: {column['Type']}")
                    print(f"  Nulo: {column['Null']}")
                    print(f"  Clave: {column['Key']}")
                    print(f"  Default: {column['Default']}")
                    print(f"  Extra: {column['Extra']}")
                    print("-" * 60)
            else:
                print("❌ No se pudo obtener la estructura de la tabla")
                
            # Verificar roles existentes
            roles = db.execute_query("SELECT id, name FROM roles")
            if roles:
                print("\n📋 Roles existentes:")
                for role in roles:
                    print(f"  ID: {role['id']}, Nombre: '{role['name']}'")
            
        else:
            print("❌ No se pudo conectar a la base de datos")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_users_table()
