#!/usr/bin/env python3
"""
Script de diagnóstico simple para MySQL
"""

try:
    import mysql.connector
    print("✅ mysql.connector importado correctamente")
    
    # Probar conexión directa
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            database='pos_system',
            user='root',
            password='D3v3l0p3r@@$',
            charset='utf8mb4',
            autocommit=True,
            ssl_disabled=True
        )
        
        if connection.is_connected():
            print("✅ Conexión MySQL exitosa!")
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ Versión MySQL: {version[0]}")
            
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"✅ Tablas encontradas: {len(tables)}")
            for table in tables:
                print(f"   📋 {table[0]}")
            
            cursor.close()
            connection.close()
            print("✅ Conexión cerrada exitosamente")
        else:
            print("❌ No se pudo conectar")
            
    except mysql.connector.Error as e:
        print(f"❌ Error MySQL: {e}")
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()
        
except ImportError as e:
    print(f"❌ Error importando mysql.connector: {e}")
    print("💡 Instala: pip install mysql-connector-python")
