"""
Script para cambiar la autenticación de MySQL 9.x a mysql_native_password
Esto resuelve el error: "Authentication plugin 'caching_sha2_password' reported error"
"""

import mysql.connector
from mysql.connector import Error

def fix_mysql_authentication():
    """
    Cambia la autenticación del usuario root de caching_sha2_password a mysql_native_password
    """
    print("=" * 70)
    print("FIX PARA AUTENTICACIÓN MYSQL 9.x")
    print("=" * 70)
    print()
    
    # Configuración de conexión
    password = "D3v3l0p3r@@$"
    
    print("⚠️  IMPORTANTE:")
    print("   Este script cambiará la autenticación del usuario 'root'")
    print("   de 'caching_sha2_password' a 'mysql_native_password'")
    print()
    print("   Esto es necesario para que mysql-connector-python")
    print("   pueda conectarse sin requerir conexión SSL.")
    print()
    
    respuesta = input("¿Desea continuar? (s/n): ")
    if respuesta.lower() != 's':
        print("❌ Operación cancelada")
        return
    
    print()
    print("-" * 70)
    print("Paso 1: Conectando a MySQL...")
    print("-" * 70)
    
    try:
        # Intentar conexión inicial (puede fallar si no hay privilegios)
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=password,
            ssl_disabled=True
        )
        
        if conn.is_connected():
            print("✅ Conexión establecida")
            cursor = conn.cursor()
            
            print()
            print("-" * 70)
            print("Paso 2: Verificando usuario actual...")
            print("-" * 70)
            
            # Verificar autenticación actual
            cursor.execute("""
                SELECT user, host, plugin 
                FROM mysql.user 
                WHERE user = 'root' AND host = 'localhost'
            """)
            
            resultado = cursor.fetchone()
            if resultado:
                user, host, plugin = resultado
                print(f"📋 Usuario: {user}@{host}")
                print(f"📋 Plugin actual: {plugin}")
            
            print()
            print("-" * 70)
            print("Paso 3: Cambiando método de autenticación...")
            print("-" * 70)
            
            # Cambiar a mysql_native_password
            sql_alter = f"""
                ALTER USER 'root'@'localhost' 
                IDENTIFIED WITH mysql_native_password BY '{password}'
            """
            
            cursor.execute(sql_alter)
            print("✅ Método de autenticación cambiado")
            
            # Aplicar privilegios
            cursor.execute("FLUSH PRIVILEGES")
            print("✅ Privilegios actualizados")
            
            print()
            print("-" * 70)
            print("Paso 4: Verificando cambio...")
            print("-" * 70)
            
            # Verificar el cambio
            cursor.execute("""
                SELECT user, host, plugin 
                FROM mysql.user 
                WHERE user = 'root' AND host = 'localhost'
            """)
            
            resultado = cursor.fetchone()
            if resultado:
                user, host, plugin = resultado
                print(f"📋 Usuario: {user}@{host}")
                print(f"📋 Plugin nuevo: {plugin}")
                
                if plugin == 'mysql_native_password':
                    print()
                    print("=" * 70)
                    print("✅ ¡AUTENTICACIÓN CORREGIDA EXITOSAMENTE!")
                    print("=" * 70)
                    print()
                    print("Ahora puedes usar la aplicación sin errores de conexión.")
                    print("El sistema ya no requerirá conexión SSL.")
                else:
                    print("⚠️  El plugin no cambió correctamente")
            
            cursor.close()
            conn.close()
            
    except Error as e:
        print(f"❌ Error de MySQL: {e}")
        print()
        print("SOLUCIÓN ALTERNATIVA:")
        print("Ejecuta este comando en el MySQL Command Line Client:")
        print()
        print(f"ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '{password}';")
        print("FLUSH PRIVILEGES;")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        print()
        print("SOLUCIÓN ALTERNATIVA:")
        print("Ejecuta estos comandos en el MySQL Command Line Client:")
        print()
        print(f"ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '{password}';")
        print("FLUSH PRIVILEGES;")

if __name__ == "__main__":
    fix_mysql_authentication()
