#!/usr/bin/env python3
"""
Script para probar la conexión a la base de datos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.connection import get_db_connection

def test_database():
    """Probar conexión a la base de datos"""
    print("=== PRUEBA DE CONEXIÓN A LA BASE DE DATOS ===")
    
    try:
        # Obtener instancia de la base de datos
        db = get_db_connection()
        print(f"✅ Instancia de DB creada")
        
        # Probar conexión
        print("\n🔄 Probando conexión...")
        connection_info = db.test_connection()
        
        if connection_info["connected"]:
            print(f"✅ Conexión exitosa!")
            print(f"   📊 Servidor: {connection_info['server_info']}")
            print(f"   📊 Base de datos: {connection_info['database']}")
            print(f"   📊 Versión MySQL: {connection_info['mysql_version']}")
            
            # Probar una consulta simple
            print("\n🔄 Probando consulta simple...")
            result = db.execute_query("SELECT COUNT(*) as total_roles FROM roles")
            if result:
                print(f"✅ Consulta exitosa! Total roles: {result[0]['total_roles']}")
            else:
                print("❌ Error en consulta de prueba")
                
        else:
            print(f"❌ Error de conexión: {connection_info['error']}")
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cerrar conexión
        try:
            db.disconnect()
            print("\n🔌 Conexión cerrada")
        except:
            pass

if __name__ == "__main__":
    test_database()
