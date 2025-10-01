#!/usr/bin/env python3
"""
Script de prueba simple para conexión
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Agregar debug de importación
print("=== INICIANDO PRUEBA DE CONEXIÓN ===")

try:
    print("🔄 Importando database.connection...")
    from database.connection import get_db_connection
    print("✅ database.connection importado")
    
    print("🔄 Obteniendo instancia de conexión...")
    db = get_db_connection()
    print("✅ Instancia obtenida")
    
    print("🔄 Intentando conectar...")
    result = db.connect()
    print(f"📊 Resultado de conexión: {result}")
    
    if result:
        print("✅ Conexión exitosa!")
    else:
        print("❌ Falló la conexión")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
