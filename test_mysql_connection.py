"""
Script de prueba para verificar la conexión a MySQL
Solución para error: Authentication plugin 'caching_sha2_password' reported error
"""

import mysql.connector
from mysql.connector import Error

def test_connection():
    """Probar conexión a MySQL con diferentes configuraciones"""
    
    print("=" * 70)
    print("PRUEBA DE CONEXIÓN A MYSQL - Sistema POS")
    print("=" * 70)
    print()
    
    # Configuración
    config = {
        'host': 'localhost',
        'port': 3306,
        'database': 'pos_system',
        'user': 'root',
        'password': 'D3v3l0p3r@@$',
        'charset': 'utf8mb4',
        'autocommit': True,
        'connection_timeout': 10,
    }
    
    # Test 1: Conexión con SSL deshabilitado
    print("📋 Test 1: Conexión con SSL deshabilitado")
    print("-" * 70)
    try:
        test_config = config.copy()
        test_config['ssl_disabled'] = True
        
        conn = mysql.connector.connect(**test_config)
        
        if conn.is_connected():
            db_info = conn.get_server_info()
            print(f"✅ ÉXITO - Conectado a MySQL Server versión {db_info}")
            
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"✅ Base de datos actual: {record[0]}")
            
            cursor.close()
            conn.close()
            print("✅ Conexión cerrada correctamente")
            return True
            
    except Error as e:
        print(f"❌ ERROR: {e}")
        print(f"   Código de error: {e.errno}")
    
    print()
    
    # Test 2: Conexión con get_server_public_key
    print("📋 Test 2: Conexión con get_server_public_key=True")
    print("-" * 70)
    try:
        test_config = config.copy()
        test_config['ssl_disabled'] = True
        test_config['get_server_public_key'] = True
        
        conn = mysql.connector.connect(**test_config)
        
        if conn.is_connected():
            db_info = conn.get_server_info()
            print(f"✅ ÉXITO - Conectado a MySQL Server versión {db_info}")
            
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"✅ Base de datos actual: {record[0]}")
            
            # Test de consulta a roles
            cursor.execute("SELECT COUNT(*) as total FROM roles;")
            result = cursor.fetchone()
            print(f"✅ Total de roles en la BD: {result[0]}")
            
            cursor.close()
            conn.close()
            print("✅ Conexión cerrada correctamente")
            return True
            
    except Error as e:
        print(f"❌ ERROR: {e}")
        print(f"   Código de error: {e.errno}")
    
    print()
    
    # Test 3: Conexión con todas las opciones
    print("📋 Test 3: Conexión con todas las opciones (Recomendado)")
    print("-" * 70)
    try:
        test_config = config.copy()
        test_config['ssl_disabled'] = True
        test_config['get_server_public_key'] = True
        test_config['allow_local_infile'] = True
        
        conn = mysql.connector.connect(**test_config)
        
        if conn.is_connected():
            db_info = conn.get_server_info()
            print(f"✅ ÉXITO - Conectado a MySQL Server versión {db_info}")
            
            cursor = conn.cursor(dictionary=True)
            
            # Verificar base de datos
            cursor.execute("SELECT DATABASE() as db;")
            record = cursor.fetchone()
            print(f"✅ Base de datos actual: {record['db']}")
            
            # Verificar tablas
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print(f"✅ Tablas encontradas: {len(tables)}")
            
            # Test de consulta compleja
            cursor.execute("""
                SELECT id, name, code, active, system_role 
                FROM roles 
                LIMIT 3
            """)
            roles = cursor.fetchall()
            print(f"✅ Roles de ejemplo:")
            for role in roles:
                status = "Activo" if role['active'] else "Inactivo"
                tipo = "Sistema" if role['system_role'] else "Custom"
                print(f"   - [{role['id']}] {role['name']} ({role['code']}) - {status} - {tipo}")
            
            cursor.close()
            conn.close()
            print("✅ Conexión cerrada correctamente")
            print()
            print("=" * 70)
            print("🎉 TODAS LAS PRUEBAS EXITOSAS")
            print("=" * 70)
            return True
            
    except Error as e:
        print(f"❌ ERROR: {e}")
        print(f"   Código de error: {e.errno}")
        return False
    
    return False

if __name__ == "__main__":
    test_connection()
    print()
    input("Presiona Enter para cerrar...")
