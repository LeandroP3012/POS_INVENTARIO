"""
Script para crear rol de prueba "Gerente de Personal" y usuario de prueba
Este script facilita la validación del sistema de permisos
"""

import mysql.connector
import json
import os
import hashlib

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

def hash_password(password: str) -> str:
    """Generar hash SHA256 de la contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_test_role_and_user():
    """Crear rol de prueba y usuario de prueba"""
    
    print("\n" + "="*70)
    print("🧪 CREACIÓN DE ROL Y USUARIO DE PRUEBA")
    print("="*70 + "\n")
    
    try:
        # Conectar a la base de datos
        db_config = get_db_config()
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        
        print("📡 Conectado a la base de datos\n")
        
        # 1. Verificar si el rol ya existe
        print("1️⃣ Verificando si el rol 'Gerente de Personal' existe...")
        cursor.execute("SELECT * FROM roles WHERE code = 'gerente_personal'")
        existing_role = cursor.fetchone()
        
        if existing_role:
            print(f"   ⚠️ El rol ya existe con ID: {existing_role['id']}")
            role_id = existing_role['id']
        else:
            # Crear nuevo rol
            print("   ✅ Creando nuevo rol 'Gerente de Personal'...")
            
            # Permisos para el rol de prueba (solo algunos permisos de usuarios)
            test_permissions = [
                'dashboard.view',      # Ver dashboard
                'users.view',          # Ver lista de usuarios
                'users.edit',          # Editar usuarios
                'users.activate',      # Activar usuarios
                'users.deactivate'     # Desactivar usuarios
            ]
            
            permissions_json = json.dumps(test_permissions)
            
            cursor.execute("""
                INSERT INTO roles (name, code, description, permissions, created_at)
                VALUES (%s, %s, %s, %s, NOW())
            """, (
                'Gerente de Personal',
                'gerente_personal',
                'Rol de prueba para validar permisos - Puede ver y editar usuarios, cambiar estados',
                permissions_json
            ))
            
            role_id = cursor.lastrowid
            connection.commit()
            print(f"   ✅ Rol creado exitosamente con ID: {role_id}")
        
        print()
        
        # 2. Verificar si el usuario ya existe
        print("2️⃣ Verificando si el usuario 'prueba_permisos' existe...")
        cursor.execute("SELECT * FROM users WHERE username = 'prueba_permisos'")
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"   ⚠️ El usuario ya existe con ID: {existing_user['id']}")
            print(f"   📝 Actualizando usuario existente...")
            
            # Actualizar usuario existente con el nuevo rol
            password_hash = hash_password('1234')
            cursor.execute("""
                UPDATE users 
                SET password_hash = %s, 
                    role_id = %s
                WHERE username = 'prueba_permisos'
            """, (password_hash, role_id))
            
            connection.commit()
            print("   ✅ Usuario actualizado exitosamente")
            user_id = existing_user['id']
        else:
            # Crear nuevo usuario
            print("   ✅ Creando nuevo usuario 'prueba_permisos'...")
            
            password_hash = hash_password('1234')
            
            cursor.execute("""
                INSERT INTO users (
                    username, password_hash, full_name, email, 
                    user_type, role_id, created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, NOW())
            """, (
                'prueba_permisos',
                password_hash,
                'Prueba Permisos',
                'prueba@pos.com',
                'employee',  # Usar tipo estándar
                role_id
            ))
            
            user_id = cursor.lastrowid
            connection.commit()
            print(f"   ✅ Usuario creado exitosamente con ID: {user_id}")
        
        print()
        
        # 3. Mostrar resumen
        print("="*70)
        print("✅ CONFIGURACIÓN COMPLETADA")
        print("="*70 + "\n")
        
        print("📋 RESUMEN DE CREACIÓN:\n")
        
        print("🔐 ROL CREADO:")
        print(f"   • Nombre: Gerente de Personal")
        print(f"   • Código: gerente_personal")
        print(f"   • ID: {role_id}")
        print(f"   • Permisos asignados:")
        print(f"     ✅ users.view - Ver lista de usuarios")
        print(f"     ✅ users.edit - Editar usuarios")
        print(f"     ✅ users.activate - Activar usuarios")
        print(f"     ✅ users.deactivate - Desactivar usuarios")
        print(f"   • Permisos NO asignados:")
        print(f"     ❌ users.create - Crear usuarios")
        print(f"     ❌ users.delete - Eliminar usuarios")
        print(f"     ❌ users.export - Exportar a Excel")
        
        print()
        
        print("👤 USUARIO CREADO:")
        print(f"   • Usuario: prueba_permisos")
        print(f"   • Contraseña: 1234")
        print(f"   • Nombre: Prueba Permisos")
        print(f"   • Email: prueba@pos.com")
        print(f"   • Rol: Gerente de Personal")
        print(f"   • ID: {user_id}")
        
        print()
        print("="*70)
        print("🧪 PASOS PARA VALIDAR")
        print("="*70 + "\n")
        
        print("1. Iniciar la aplicación POS:")
        print("   python main.py\n")
        
        print("2. Cerrar sesión del usuario actual\n")
        
        print("3. Iniciar sesión con:")
        print("   👤 Usuario: prueba_permisos")
        print("   🔑 Contraseña: 1234\n")
        
        print("4. Ir al módulo: Gestión de Usuarios\n")
        
        print("5. Verificar que VE estos botones:")
        print("   ✅ ✏️ Editar")
        print("   ✅ ✓ Activar / ⊗ Desactivar\n")
        
        print("6. Verificar que NO VE estos botones:")
        print("   ❌ ➕ Nuevo Usuario")
        print("   ❌ 🗑️ Eliminar")
        print("   ❌ 📄 Exportar Excel\n")
        
        print("7. Probar funcionalidad:")
        print("   • Seleccionar un usuario")
        print("   • Clic en 'Editar' → Debe permitir editar ✓")
        print("   • Clic en 'Activar/Desactivar' → Debe permitir cambiar estado ✓")
        
        print()
        print("="*70)
        print("✅ ¡TODO LISTO PARA VALIDAR!")
        print("="*70 + "\n")
        
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
    success = create_test_role_and_user()
    
    if success:
        print("\n💡 Ahora puedes iniciar la aplicación y validar los permisos\n")
    else:
        print("\n⚠️ No se pudo completar la creación del rol y usuario de prueba\n")
