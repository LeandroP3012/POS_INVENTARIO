"""
Script de prueba del módulo de reportes
Ejecuta este script para verificar que todo funcione correctamente
"""

print("\n" + "="*60)
print("🧪 TEST DEL MÓDULO DE REPORTES")
print("="*60 + "\n")

# Test 1: Imports
print("1️⃣ Verificando imports...")
try:
    from models.report_model import ReportModel
    from controllers.report_controller import ReportController
    from views.reports_view import ReportsView
    from tkcalendar import DateEntry
    import matplotlib.pyplot as plt
    print("   ✅ Todos los imports exitosos\n")
except ImportError as e:
    print(f"   ❌ Error en imports: {e}\n")
    exit(1)

# Test 2: Crear instancias
print("2️⃣ Creando instancias...")
try:
    model = ReportModel()
    controller = ReportController()
    print("   ✅ Modelo y controlador creados\n")
except Exception as e:
    print(f"   ❌ Error creando instancias: {e}\n")
    exit(1)

# Test 3: Probar conexión a BD
print("3️⃣ Probando conexión a base de datos...")
try:
    result = controller.get_inventory_report()
    if result['success']:
        print(f"   ✅ Conexión exitosa")
        print(f"   📦 Productos en inventario: {result['data']['summary']['total_products']}\n")
    else:
        print(f"   ⚠️ Sin datos: {result.get('message')}\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")

# Test 4: Probar reporte de ventas
print("4️⃣ Probando reporte de ventas...")
try:
    from datetime import datetime, timedelta
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    result = controller.get_sales_report(start_date, end_date)
    
    if result['success']:
        summary = result['data']['summary']
        print(f"   ✅ Reporte generado exitosamente")
        print(f"   📊 Período: {start_date} a {end_date}")
        print(f"   🛒 Total ventas: {summary['total_sales']}")
        print(f"   💰 Monto total: S/ {summary['total_amount']:.2f}")
        print(f"   🎫 Ticket promedio: S/ {summary['average_ticket']:.2f}\n")
    else:
        print(f"   ⚠️ Sin ventas en el período: {result.get('message')}\n")
        
except Exception as e:
    print(f"   ❌ Error: {e}\n")
    import traceback
    traceback.print_exc()

print("="*60)
print("✅ PRUEBAS COMPLETADAS")
print("="*60)
print("\n💡 Si todo salió bien, puedes ejecutar main.py y probar el módulo\n")
