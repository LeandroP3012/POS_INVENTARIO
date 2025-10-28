"""
Script para actualizar el rol de prueba 'Gerente de Personal' con el permiso dashboard.view
"""

import mysql.connector
import json
import os

def get_db_config():
    """Obtener configuración de base de datos"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'database.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    return {
        'host': config.get('host', 'localhost'),
        'port': int(config.get('port', 3306)),
        'user': config.get('user', 'root'),
        'password': config.get('password', ''),
        'database': config.get('name', 'pos_system')
    }

def update_test_role():
    """Actualizar rol de prueba con permiso dashboard.view"""
    
    print("\n" + "="*70)
    print("🔄 ACTUALIZACIÓN DE ROL DE PRUEBA")
    print("="*70 + "\n")
    
    try:
        # Conectar a la base de datos
        db_config = get_db_config()
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        
        print("📡 Conectado a la base de datos\n")
        
        # Buscar rol 'Gerente de Personal'
        cursor.execute("SELECT * FROM roles WHERE code = 'gerente_personal'")
        role = cursor.fetchone()
        
        if not role:
            print("❌ No se encontró el rol 'Gerente de Personal'")
            print("   Ejecuta primero: python create_test_role_user.py\n")
            return False
        
        print(f"✅ Rol encontrado: {role['name']} (ID: {role['id']})\n")
        
        # Permisos actualizados
        updated_permissions = [
            'dashboard.view',      # Ver dashboard
            'users.view',          # Ver lista de usuarios
            'users.edit',          # Editar usuarios
            'users.activate',      # Activar usuarios
            'users.deactivate'     # Desactivar usuarios
        ]
        
        permissions_json = json.dumps(updated_permissions)
        
        # Actualizar permisos
        cursor.execute("""
            UPDATE roles 
            SET permissions = %s
            WHERE code = 'gerente_personal'
        """, (permissions_json,))
        
        connection.commit()
        
        print("="*70)
        print("✅ ROL ACTUALIZADO EXITOSAMENTE")
        print("="*70 + "\n")
        
        print("📋 PERMISOS ACTUALIZADOS:\n")
        print("   ✅ dashboard.view      - Ver dashboard principal")
        print("   ✅ users.view          - Ver lista de usuarios")
        print("   ✅ users.edit          - Editar usuarios")
        print("   ✅ users.activate      - Activar usuarios")
        print("   ✅ users.deactivate    - Desactivar usuarios")
        
        print("\n   ❌ users.create        - NO puede crear usuarios")
        print("   ❌ users.delete        - NO puede eliminar usuarios")
        print("   ❌ users.export        - NO puede exportar a Excel")
        
        print("\n" + "="*70)
        print("🧪 AHORA PUEDES VALIDAR")
        print("="*70 + "\n")
        
        print("1. Iniciar la aplicación:")
        print("   python main.py\n")
        
        print("2. Iniciar sesión con:")
        print("   👤 Usuario: prueba_permisos")
        print("   🔑 Contraseña: 1234\n")
        
        print("3. Verificar que AHORA VES:")
        print("   ✅ Dashboard con módulos")
        print("   ✅ Tarjeta 'Gestión de Usuarios' en el dashboard")
        print("   ✅ Menú 'Administración' en la navbar")
        print("   ✅ Opción 'Gestionar Usuarios' en el menú\n")
        
        print("4. Ir a Gestión de Usuarios y verificar:")
        print("   ✅ Botón 'Editar'")
        print("   ✅ Botón 'Activar/Desactivar'")
        print("   ❌ NO ve botón 'Nuevo Usuario'")
        print("   ❌ NO ve botón 'Eliminar'")
        print("   ❌ NO ve botón 'Exportar Excel'\n")
        
        cursor.close()
        connection.close()
        
        return True
        
    except mysql.connector.Error as e:
        print(f"\n❌ Error de base de datos: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = update_test_role()
    
    if success:
        print("="*70)
        print("✅ ¡ACTUALIZACIÓN COMPLETA!")
        print("="*70 + "\n")
    else:
        print("\n⚠️ No se pudo completar la actualización\n")
