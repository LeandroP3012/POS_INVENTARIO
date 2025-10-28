"""
Script para verificar y actualizar permisos en la base de datos
Ejecutar este script para aplicar los nuevos permisos al sistema
"""

import mysql.connector
import json
import sys
import os

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def get_db_config():
    """Obtener configuración de base de datos"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'database.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Convertir formato del archivo a formato de mysql.connector
    return {
        'host': config.get('host', 'localhost'),
        'port': int(config.get('port', 3306)),
        'user': config.get('user', 'root'),
        'password': config.get('password', ''),
        'database': config.get('name', 'pos_system')
    }

def update_permissions():
    """Actualizar permisos en la base de datos"""
    print("\n" + "="*70)
    print("🔐 ACTUALIZACIÓN DE SISTEMA DE PERMISOS")
    print("="*70 + "\n")
    
    try:
        # Conectar a la base de datos
        db_config = get_db_config()
        
        print(f"📡 Conectando a la base de datos: {db_config['database']}...")
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        print("   ✅ Conexión exitosa\n")
        
        # 1. Verificar permisos actuales
        print("1️⃣ Verificando permisos actuales...")
        cursor.execute("SELECT id, name, code, permissions FROM roles ORDER BY id")
        roles = cursor.fetchall()
        
        print(f"\n   Roles encontrados: {len(roles)}\n")
        for role in roles:
            perms = json.loads(role['permissions']) if role['permissions'] else []
            print(f"   • {role['name']} ({role['code']})")
            print(f"     Permisos: {len(perms)} - {perms[:3]}{'...' if len(perms) > 3 else ''}")
        
        # 2. Actualizar permisos de roles
        print("\n2️⃣ Actualizando permisos de roles...\n")
        
        updates = [
            {
                'code': 'super_admin',
                'permissions': ['*'],
                'description': 'Acceso total al sistema'
            },
            {
                'code': 'admin',
                'permissions': [
                    'users.view', 'users.create', 'users.edit', 'users.delete',
                    'users.activate', 'users.deactivate', 'users.export',
                    'roles.view', 'roles.create', 'roles.edit', 'roles.delete',
                    'system.config', 'system.backup', 'system.reports',
                    'inventory.view', 'inventory.create', 'inventory.edit', 'inventory.delete',
                    'inventory.reports', 'inventory.export',
                    'sales.view', 'sales.create', 'sales.edit', 'sales.reports', 'sales.export',
                    'dashboard.view', 'dashboard.stats',
                    'reports.sales', 'reports.inventory', 'reports.users'
                ],
                'description': 'Administrador con acceso completo'
            },
            {
                'code': 'manager',
                'permissions': [
                    'users.view',
                    'inventory.view', 'inventory.reports', 'inventory.export',
                    'sales.view', 'sales.create', 'sales.reports', 'sales.export',
                    'dashboard.view', 'dashboard.stats',
                    'reports.sales', 'reports.inventory'
                ],
                'description': 'Gerente con acceso a reportes'
            },
            {
                'code': 'employee',
                'permissions': [
                    'sales.view', 'sales.create',
                    'inventory.view',
                    'dashboard.view'
                ],
                'description': 'Empleado con acceso básico'
            },
            {
                'code': 'cashier',
                'permissions': [
                    'sales.create', 'sales.view_own',
                    'cash.register',
                    'dashboard.view'
                ],
                'description': 'Cajero solo ventas'
            }
        ]
        
        for update in updates:
            perms_json = json.dumps(update['permissions'])
            cursor.execute(
                "UPDATE roles SET permissions = %s WHERE code = %s",
                (perms_json, update['code'])
            )
            print(f"   ✅ Actualizado: {update['code']} ({len(update['permissions'])} permisos)")
        
        connection.commit()
        print(f"\n   💾 Cambios guardados en la base de datos")
        
        # 3. Verificar permisos actualizados
        print("\n3️⃣ Verificando permisos actualizados...\n")
        cursor.execute("SELECT id, name, code, permissions FROM roles ORDER BY id")
        roles = cursor.fetchall()
        
        for role in roles:
            perms = json.loads(role['permissions']) if role['permissions'] else []
            print(f"   • {role['name']}")
            if '*' in perms:
                print(f"     ⭐ Super Admin - Todos los permisos")
            else:
                print(f"     📋 {len(perms)} permisos asignados")
                if 'users.view' in perms:
                    print(f"        ✓ Módulo Usuarios: ", end='')
                    user_perms = [p for p in perms if p.startswith('users.')]
                    print(', '.join([p.split('.')[1] for p in user_perms]))
        
        print("\n" + "="*70)
        print("✅ ACTUALIZACIÓN COMPLETADA EXITOSAMENTE")
        print("="*70)
        print("\n💡 Recomendaciones:")
        print("   1. Los usuarios deben cerrar sesión y volver a iniciarla")
        print("   2. Los cambios en permisos se aplican inmediatamente")
        print("   3. Verifica que cada rol tenga los permisos correctos\n")
        
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
    success = update_permissions()
    sys.exit(0 if success else 1)
