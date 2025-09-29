"""
Script simple para probar conectividad Python <-> MySQL
Usa el archivo connection.py existente
"""

import sys
import os
from datetime import datetime

# Agregar directorio actual al path para importar connection.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_mysql_connection():
    """Prueba simple de conectividad con MySQL"""
    
    print("=" * 60)
    print("🔧 PRUEBA DE CONECTIVIDAD PYTHON <-> MYSQL")
    print("=" * 60)
    
    try:
        # Importar la conexión
        from database.connection import get_db_connection
        
        # Obtener instancia de conexión
        db = get_db_connection()
        
        # Mostrar configuración que se va a usar
        print("📋 CONFIGURACIÓN:")
        print(f"   Host: {db.config.get('host')}")
        print(f"   Puerto: {db.config.get('port')}")
        print(f"   Usuario: {db.config.get('username')}")
        print(f"   Base de datos: {db.config.get('database')}")
        print(f"   Charset: {db.config.get('charset')}")
        
        print("\n🔌 PROBANDO CONEXIÓN...")
        
        # Intentar conectar
        if db.connect():
            print("✅ ¡CONEXIÓN EXITOSA!")
            
            # Realizar consultas de prueba
            print("\n🧪 EJECUTANDO CONSULTAS DE PRUEBA:")
            
            # 1. Consulta básica - obtener versión de MySQL
            print("\n1️⃣ Versión de MySQL:")
            version_result = db.execute_query("SELECT VERSION() as version")
            if version_result:
                print(f"   📊 MySQL Versión: {version_result[0]['version']}")
            
            # 2. Consulta de fecha y hora del servidor
            print("\n2️⃣ Fecha y hora del servidor:")
            datetime_result = db.execute_query("SELECT NOW() as fecha_hora, CURDATE() as fecha, CURTIME() as hora")
            if datetime_result:
                row = datetime_result[0]
                print(f"   📅 Fecha y hora: {row['fecha_hora']}")
                print(f"   📅 Solo fecha: {row['fecha']}")
                print(f"   🕐 Solo hora: {row['hora']}")
            
            # 3. Verificar base de datos actual
            print("\n3️⃣ Base de datos actual:")
            db_result = db.execute_query("SELECT DATABASE() as base_datos")
            if db_result:
                current_db = db_result[0]['base_datos']
                if current_db:
                    print(f"   🗄️ Base de datos activa: {current_db}")
                else:
                    print("   ⚠️ No hay base de datos seleccionada")
            
            # 4. Listar bases de datos disponibles
            print("\n4️⃣ Bases de datos disponibles:")
            databases_result = db.execute_query("SHOW DATABASES")
            if databases_result:
                print("   📁 Bases de datos encontradas:")
                for i, db_row in enumerate(databases_result, 1):
                    db_name = list(db_row.values())[0]
                    print(f"      {i}. {db_name}")
            
            # 5. Si existe pos_system, mostrar tablas
            pos_system_exists = any(
                'pos_system' in list(db_row.values())[0] 
                for db_row in databases_result
            ) if databases_result else False
            
            if pos_system_exists:
                print("\n5️⃣ Verificando tablas en pos_system:")
                tables_result = db.execute_query("SHOW TABLES FROM pos_system")
                if tables_result and len(tables_result) > 0:
                    print(f"   📊 Tablas encontradas ({len(tables_result)}):")
                    for i, table_row in enumerate(tables_result, 1):
                        table_name = list(table_row.values())[0]
                        print(f"      {i}. {table_name}")
                else:
                    print("   📭 No hay tablas en pos_system")
            else:
                print("\n5️⃣ Base de datos 'pos_system' no encontrada")
                print("   💡 Ejecuta el script SQL para crearla")
            
            # 6. Información del servidor
            print("\n6️⃣ Información del servidor:")
            server_info = db.connection.get_server_info()
            print(f"   🖥️ Información del servidor: {server_info}")
            
            # 7. Variables importantes del sistema
            print("\n7️⃣ Variables del sistema:")
            variables_query = """
            SELECT 
                @@version as mysql_version,
                @@character_set_server as charset_server,
                @@collation_server as collation_server,
                @@max_connections as max_connections,
                @@port as puerto
            """
            vars_result = db.execute_query(variables_query)
            if vars_result:
                vars_info = vars_result[0]
                print(f"   🐬 Versión MySQL: {vars_info['mysql_version']}")
                print(f"   🔤 Charset servidor: {vars_info['charset_server']}")
                print(f"   📝 Collation: {vars_info['collation_server']}")
                print(f"   🔗 Max conexiones: {vars_info['max_connections']}")
                print(f"   🚪 Puerto: {vars_info['puerto']}")
            
            # Cerrar conexión
            db.disconnect()
            print("\n✅ Conexión cerrada correctamente")
            
            # Resumen final
            print("\n" + "=" * 60)
            print("🎉 ¡PRUEBA COMPLETADA EXITOSAMENTE!")
            print("✅ Python puede conectarse a MySQL")
            print("✅ Las consultas funcionan correctamente")
            print("✅ La configuración es válida")
            print("=" * 60)
            
            return True
            
        else:
            print("❌ NO SE PUDO CONECTAR A MYSQL")
            print("\n🛠️ POSIBLES SOLUCIONES:")
            print("1. Verificar que MySQL esté ejecutándose")
            print("2. Revisar credenciales en config/database.json")
            print("3. Verificar que el puerto 3306 esté disponible")
            print("4. Comprobar permisos del usuario MySQL")
            return False
            
    except ImportError as e:
        print(f"❌ ERROR DE IMPORTACIÓN: {e}")
        print("\n🛠️ SOLUCIONES:")
        print("1. Verificar que connection.py existe en database/")
        print("2. Instalar mysql-connector-python:")
        print("   pip install mysql-connector-python")
        return False
        
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")
        print(f"\n📝 Tipo de error: {type(e).__name__}")
        return False

def main():
    """Función principal"""
    try:
        # Mostrar información del entorno
        print(f"🐍 Python: {sys.version}")
        print(f"📁 Directorio: {os.getcwd()}")
        print(f"⏰ Hora local: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Ejecutar prueba
        success = test_mysql_connection()
        
        if success:
            print("\n💡 PRÓXIMOS PASOS:")
            print("1. Si pos_system no existe, ejecuta el script SQL")
            print("2. Si existe pero sin tablas, ejecuta setup_database_clean.sql")
            print("3. Prueba tu aplicación POS con: python main.py")
        else:
            print("\n🚨 REVISAR CONFIGURACIÓN:")
            print("- Verificar MySQL instalado y ejecutándose")
            print("- Revisar config/database.json")
            print("- Probar credenciales manualmente en MySQL Workbench")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error en main: {e}")

if __name__ == "__main__":
    main()
