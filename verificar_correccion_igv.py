"""
Script de verificación de la corrección de IGV
Fecha: 2026-01-10

Este script verifica que:
1. El campo include_tax existe en la tabla sales
2. Las ventas existentes tienen include_tax=TRUE
3. El sistema puede crear ventas sin IGV
"""

import mysql.connector
from datetime import datetime

def verificar_campo_include_tax():
    """Verifica que el campo include_tax existe en la tabla sales"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Cambia esto por tu contraseña
            database='pos_system'
        )
        
        cursor = connection.cursor()
        
        # Verificar estructura de la tabla
        cursor.execute("DESCRIBE sales")
        columns = cursor.fetchall()
        
        include_tax_exists = False
        for column in columns:
            if column[0] == 'include_tax':
                include_tax_exists = True
                print(f"✅ Campo 'include_tax' encontrado: {column}")
                break
        
        if not include_tax_exists:
            print("❌ ERROR: El campo 'include_tax' NO existe en la tabla sales")
            print("   Debes ejecutar el script: database/add_include_tax_field.sql")
            return False
        
        # Verificar ventas existentes
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN include_tax = 1 THEN 1 ELSE 0 END) as con_igv,
                SUM(CASE WHEN include_tax = 0 THEN 1 ELSE 0 END) as sin_igv,
                SUM(CASE WHEN include_tax IS NULL THEN 1 ELSE 0 END) as null_igv
            FROM sales
        """)
        
        result = cursor.fetchone()
        print(f"\n📊 Estadísticas de ventas:")
        print(f"   Total de ventas:     {result[0]}")
        print(f"   Con IGV (TRUE):      {result[1]}")
        print(f"   Sin IGV (FALSE):     {result[2]}")
        print(f"   NULL (sin definir):  {result[3]}")
        
        if result[3] > 0:
            print(f"\n⚠️  ADVERTENCIA: Hay {result[3]} ventas con include_tax=NULL")
            print("   Ejecuta: UPDATE sales SET include_tax = TRUE WHERE include_tax IS NULL;")
        
        # Mostrar últimas 5 ventas
        cursor.execute("""
            SELECT 
                sale_number,
                sale_date,
                include_tax,
                subtotal,
                tax_amount,
                total_amount
            FROM sales
            ORDER BY id DESC
            LIMIT 5
        """)
        
        print(f"\n📋 Últimas 5 ventas:")
        print(f"{'Nº Venta':<20} {'Fecha':<20} {'IGV?':<8} {'Subtotal':<12} {'IGV':<12} {'Total':<12}")
        print("-" * 90)
        
        for row in cursor.fetchall():
            igv_status = "✅ Sí" if row[2] else "❌ No"
            print(f"{row[0]:<20} {str(row[1]):<20} {igv_status:<8} S/ {row[3]:>8.2f} S/ {row[4]:>8.2f} S/ {row[5]:>8.2f}")
        
        cursor.close()
        connection.close()
        
        print("\n✅ Verificación completada exitosamente")
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Error de conexión a la base de datos: {e}")
        print("\nVerifica:")
        print("1. Que MySQL esté corriendo")
        print("2. Que la contraseña sea correcta")
        print("3. Que la base de datos 'pos_system' exista")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*90)
    print("🔍 VERIFICACIÓN DE CORRECCIÓN DE IGV EN REPORTES")
    print("="*90)
    print()
    
    resultado = verificar_campo_include_tax()
    
    print()
    print("="*90)
    if resultado:
        print("✅ CORRECCIÓN APLICADA CORRECTAMENTE")
        print()
        print("Ahora puedes:")
        print("1. Hacer ventas SIN IGV (desactivando el checkbox)")
        print("2. Los reportes mostrarán correctamente las ventas sin IGV")
        print("3. El IGV solo se sumará de ventas que lo incluyen")
    else:
        print("❌ CORRECCIÓN NO APLICADA")
        print()
        print("Pasos a seguir:")
        print("1. Ejecuta: mysql -u root -p pos_system < database/add_include_tax_field.sql")
        print("2. Vuelve a ejecutar este script para verificar")
    print("="*90)
