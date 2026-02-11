"""
Script de Diagnóstico y Optimización de Base de Datos
Verifica el estado de la conexión, analiza el performance y optimiza tablas
"""

import sys
import os
import logging
from datetime import datetime
import time

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_db_connection

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('DatabaseDiagnostic')

def print_header(title):
    """Imprimir encabezado formateado"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_connection_speed():
    """Probar velocidad de conexión"""
    print_header("PRUEBA DE VELOCIDAD DE CONEXIÓN")
    
    db = get_db_connection()
    
    # Probar 5 conexiones
    times = []
    for i in range(5):
        start = time.time()
        db.connect()
        end = time.time()
        elapsed = (end - start) * 1000  # en milisegundos
        times.append(elapsed)
        print(f"  Intento {i+1}: {elapsed:.2f} ms")
    
    avg_time = sum(times) / len(times)
    print(f"\n  ⏱️  Tiempo promedio: {avg_time:.2f} ms")
    
    if avg_time > 500:
        print("  ⚠️  ADVERTENCIA: Conexión lenta (>500ms)")
        print("     Considera revisar la configuración de red o MySQL")
    elif avg_time > 100:
        print("  ⚠️  Conexión moderada (>100ms)")
    else:
        print("  ✅ Conexión rápida")

def test_query_performance():
    """Probar performance de consultas comunes"""
    print_header("PRUEBA DE PERFORMANCE DE CONSULTAS")
    
    db = get_db_connection()
    
    queries = [
        ("Contar ventas totales", "SELECT COUNT(*) as total FROM sales"),
        ("Contar productos", "SELECT COUNT(*) as total FROM products"),
        ("Ventas del día (última semana)", """
            SELECT COUNT(*) as total 
            FROM sales 
            WHERE sale_date >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        """),
        ("Productos más vendidos", """
            SELECT p.name, SUM(sd.quantity) as total
            FROM sale_details sd
            JOIN products p ON sd.product_id = p.id
            JOIN sales s ON sd.sale_id = s.id
            WHERE s.sale_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            GROUP BY p.id
            ORDER BY total DESC
            LIMIT 10
        """)
    ]
    
    for name, query in queries:
        try:
            start = time.time()
            result = db.execute_query(query)
            end = time.time()
            elapsed = (end - start) * 1000
            
            print(f"\n  {name}")
            print(f"    Tiempo: {elapsed:.2f} ms")
            
            if elapsed > 1000:
                print(f"    ⚠️  LENTA (>1s)")
            elif elapsed > 500:
                print(f"    ⚠️  Moderada (>500ms)")
            else:
                print(f"    ✅ Rápida")
                
        except Exception as e:
            print(f"  ❌ Error en {name}: {e}")

def check_indexes():
    """Verificar índices en las tablas principales"""
    print_header("VERIFICACIÓN DE ÍNDICES")
    
    db = get_db_connection()
    
    query = """
        SELECT 
            TABLE_NAME as tabla,
            INDEX_NAME as indice,
            GROUP_CONCAT(COLUMN_NAME ORDER BY SEQ_IN_INDEX) as columnas,
            INDEX_TYPE as tipo
        FROM information_schema.STATISTICS
        WHERE TABLE_SCHEMA = 'pos_system'
        AND TABLE_NAME IN ('sales', 'sale_details', 'products', 'users', 'credit_notes')
        GROUP BY TABLE_NAME, INDEX_NAME, INDEX_TYPE
        ORDER BY TABLE_NAME, INDEX_NAME
    """
    
    try:
        indexes = db.execute_query(query)
        
        if indexes:
            current_table = None
            for idx in indexes:
                if current_table != idx['tabla']:
                    current_table = idx['tabla']
                    print(f"\n  📊 Tabla: {current_table}")
                
                print(f"     • {idx['indice']}: {idx['columnas']} ({idx['tipo']})")
        else:
            print("  ⚠️  No se encontraron índices")
            
    except Exception as e:
        print(f"  ❌ Error verificando índices: {e}")

def check_table_sizes():
    """Verificar tamaño de las tablas"""
    print_header("TAMAÑO DE TABLAS")
    
    db = get_db_connection()
    
    query = """
        SELECT 
            table_name AS tabla,
            table_rows AS registros,
            ROUND(((data_length + index_length) / 1024 / 1024), 2) AS tamaño_mb,
            ROUND((data_length / 1024 / 1024), 2) AS datos_mb,
            ROUND((index_length / 1024 / 1024), 2) AS indices_mb
        FROM information_schema.TABLES
        WHERE table_schema = 'pos_system'
        AND table_name IN ('sales', 'sale_details', 'products', 'users', 'credit_notes', 'categories')
        ORDER BY (data_length + index_length) DESC
    """
    
    try:
        tables = db.execute_query(query)
        
        if tables:
            print(f"\n  {'Tabla':<20} {'Registros':<12} {'Tamaño':<10} {'Datos':<10} {'Índices':<10}")
            print("  " + "-" * 65)
            
            for table in tables:
                print(f"  {table['tabla']:<20} {table['registros']:<12} "
                      f"{table['tamaño_mb']:<10} {table['datos_mb']:<10} {table['indices_mb']:<10}")
                      
    except Exception as e:
        print(f"  ❌ Error verificando tamaños: {e}")

def check_mysql_variables():
    """Verificar variables importantes de MySQL"""
    print_header("VARIABLES DE CONFIGURACIÓN MYSQL")
    
    db = get_db_connection()
    
    important_vars = [
        'max_connections',
        'max_execution_time',
        'wait_timeout',
        'interactive_timeout',
        'innodb_buffer_pool_size',
        'query_cache_size',
        'query_cache_type'
    ]
    
    try:
        for var in important_vars:
            query = f"SHOW VARIABLES LIKE '{var}'"
            result = db.execute_query(query)
            
            if result:
                value = result[0]['Value']
                print(f"  {var:<30} = {value}")
                
    except Exception as e:
        print(f"  ❌ Error verificando variables: {e}")

def optimize_tables():
    """Optimizar tablas de la base de datos"""
    print_header("OPTIMIZACIÓN DE TABLAS")
    
    response = input("\n  ¿Deseas optimizar las tablas? (s/n): ")
    
    if response.lower() != 's':
        print("  ⏭️  Optimización cancelada")
        return
    
    db = get_db_connection()
    tables = ['sales', 'sale_details', 'products', 'users', 'credit_notes', 'categories']
    
    print("\n  Optimizando tablas...")
    
    for table in tables:
        try:
            print(f"    • Optimizando {table}...", end=" ")
            db.execute_query(f"OPTIMIZE TABLE {table}", fetch=False)
            print("✅")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n  Analizando tablas...")
    
    for table in tables:
        try:
            print(f"    • Analizando {table}...", end=" ")
            db.execute_query(f"ANALYZE TABLE {table}", fetch=False)
            print("✅")
        except Exception as e:
            print(f"❌ Error: {e}")

def check_process_list():
    """Verificar procesos activos en MySQL"""
    print_header("PROCESOS ACTIVOS EN MYSQL")
    
    db = get_db_connection()
    
    query = """
        SELECT 
            ID as id,
            USER as usuario,
            DB as base_datos,
            COMMAND as comando,
            TIME as tiempo,
            STATE as estado,
            LEFT(INFO, 50) as consulta
        FROM information_schema.PROCESSLIST
        WHERE DB = 'pos_system' OR COMMAND != 'Sleep'
        ORDER BY TIME DESC
    """
    
    try:
        processes = db.execute_query(query)
        
        if processes:
            print(f"\n  Total de procesos: {len(processes)}")
            
            for proc in processes[:10]:  # Mostrar máximo 10
                print(f"\n  ID: {proc['id']}")
                print(f"    Usuario: {proc['usuario']}")
                print(f"    BD: {proc['base_datos']}")
                print(f"    Comando: {proc['comando']}")
                print(f"    Tiempo: {proc['tiempo']}s")
                print(f"    Estado: {proc['estado']}")
                if proc['consulta']:
                    print(f"    Consulta: {proc['consulta']}...")
        else:
            print("  ✅ No hay procesos activos")
            
    except Exception as e:
        print(f"  ❌ Error verificando procesos: {e}")

def run_diagnostics():
    """Ejecutar todos los diagnósticos"""
    print("\n" + "=" * 70)
    print("  DIAGNÓSTICO DE BASE DE DATOS - SISTEMA POS")
    print("  " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 70)
    
    try:
        # 1. Prueba de conexión
        test_connection_speed()
        
        # 2. Verificar índices
        check_indexes()
        
        # 3. Tamaño de tablas
        check_table_sizes()
        
        # 4. Performance de consultas
        test_query_performance()
        
        # 5. Variables de MySQL
        check_mysql_variables()
        
        # 6. Procesos activos
        check_process_list()
        
        # 7. Optimización (opcional)
        optimize_tables()
        
        print_header("DIAGNÓSTICO COMPLETADO")
        print("\n  ✅ Todas las pruebas completadas\n")
        
    except Exception as e:
        print(f"\n  ❌ Error durante el diagnóstico: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_diagnostics()
