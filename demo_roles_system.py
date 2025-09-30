"""
Demostración del Sistema de Gestión de Roles y Permisos
Este script muestra las capacidades del nuevo sistema de roles personalizable
"""

import os
import sys

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.role_controller import RoleController
from models.role_model import RoleModel

def mostrar_roles_disponibles():
    """Mostrar todos los roles disponibles en el sistema"""
    print("\n" + "="*60)
    print("🔐 ROLES DISPONIBLES EN EL SISTEMA")
    print("="*60)
    
    role_controller = RoleController()
    roles = role_controller.get_all_roles(include_inactive=True)
    
    for i, role in enumerate(roles, 1):
        status_icon = "✅" if role.get('active', True) else "❌"
        type_icon = "🏛️" if role.get('system_role', False) else "🔧"
        
        print(f"\n{i}. {status_icon} {type_icon} {role.get('name')}")
        print(f"   📋 Código: {role.get('code')}")
        print(f"   📝 Descripción: {role.get('description', 'Sin descripción')}")
        print(f"   👥 Usuarios: {role.get('users_count', 0)}")
        print(f"   🔓 Permisos: {len(role.get('permissions', []))} permisos")
        
        # Mostrar algunos permisos si no son demasiados
        permissions = role.get('permissions', [])
        if permissions == ['*']:
            print(f"   🌟 SUPER ADMIN: Todos los permisos")
        elif len(permissions) <= 5:
            print(f"   🔑 Permisos: {', '.join(permissions)}")
        else:
            print(f"   🔑 Permisos: {', '.join(permissions[:3])}... (+{len(permissions)-3} más)")

def mostrar_permisos_por_categoria():
    """Mostrar todos los permisos organizados por categoría"""
    print("\n" + "="*60)
    print("🔑 PERMISOS DISPONIBLES POR CATEGORÍA")
    print("="*60)
    
    role_controller = RoleController()
    permissions_by_category = role_controller.get_permissions_by_category()
    
    for category, permissions in permissions_by_category.items():
        print(f"\n📂 {category} ({len(permissions)} permisos)")
        print("-" * (len(category) + 15))
        
        for permission in permissions:
            description = role_controller.get_permission_description(permission)
            print(f"   🔸 {permission}")
            print(f"     💬 {description}")

def mostrar_estadisticas():
    """Mostrar estadísticas del sistema de roles"""
    print("\n" + "="*60)
    print("📊 ESTADÍSTICAS DEL SISTEMA DE ROLES")
    print("="*60)
    
    role_controller = RoleController()
    stats = role_controller.get_roles_stats()
    
    print(f"📈 Total de Roles: {stats.get('total_roles', 0)}")
    print(f"✅ Roles Activos: {stats.get('active_roles', 0)}")
    print(f"❌ Roles Inactivos: {stats.get('inactive_roles', 0)}")
    print(f"🏛️ Roles del Sistema: {stats.get('system_roles', 0)}")
    print(f"🔧 Roles Personalizados: {stats.get('custom_roles', 0)}")

def demostrar_verificacion_permisos():
    """Demostrar cómo funciona la verificación de permisos"""
    print("\n" + "="*60)
    print("🔍 DEMOSTRACIÓN DE VERIFICACIÓN DE PERMISOS")
    print("="*60)
    
    role_controller = RoleController()
    
    # Obtener algunos roles para probar
    roles = role_controller.get_all_roles()[:3]  # Primeros 3 roles
    
    permisos_prueba = [
        'users.view',
        'users.create', 
        'roles.manage',
        'system.config',
        'sales.create'
    ]
    
    print(f"\n🧪 Probando permisos: {', '.join(permisos_prueba)}")
    print("\n" + "-"*80)
    
    for role in roles:
        print(f"\n🔐 Rol: {role.get('name')} ({role.get('code')})")
        
        for permiso in permisos_prueba:
            tiene_permiso = role_controller.check_role_permission(role.get('id'), permiso)
            icono = "✅" if tiene_permiso else "❌"
            print(f"   {icono} {permiso}")

def mostrar_capacidades_personalizacion():
    """Mostrar las capacidades de personalización del sistema"""
    print("\n" + "="*60)
    print("🎨 CAPACIDADES DE PERSONALIZACIÓN")
    print("="*60)
    
    print("🔧 CARACTERÍSTICAS DEL SISTEMA:")
    print("   ✅ Crear roles personalizados con cualquier nombre")
    print("   ✅ Asignar permisos granulares por módulo y acción")
    print("   ✅ Activar/desactivar roles sin eliminarlos")
    print("   ✅ Protección de roles críticos del sistema")
    print("   ✅ Validación automática de permisos")
    print("   ✅ Interfaz gráfica completa para gestión")
    print("   ✅ Búsqueda y filtrado de roles")
    print("   ✅ Estadísticas en tiempo real")
    print("   ✅ Sistema de callbacks y hooks")
    print("   ✅ Logging detallado de actividades")
    
    print("\n🎯 CASOS DE USO TÍPICOS:")
    print("   📋 Crear rol 'Supervisor de Turno' con permisos específicos")
    print("   📋 Crear rol 'Vendedor Senior' con acceso ampliado")
    print("   📋 Crear rol 'Contador' solo con acceso a reportes")
    print("   📋 Crear rol 'Almacenista' solo para inventario")
    print("   📋 Definir permisos por horarios o días")
    print("   📋 Roles temporales para empleados en prueba")

def main():
    """Función principal de demostración"""
    print("🎉 DEMOSTRACIÓN DEL SISTEMA DE GESTIÓN DE ROLES")
    print("="*80)
    
    try:
        # Mostrar capacidades de personalización
        mostrar_capacidades_personalizacion()
        
        # Mostrar roles disponibles
        mostrar_roles_disponibles()
        
        # Mostrar permisos por categoría
        mostrar_permisos_por_categoria()
        
        # Mostrar estadísticas
        mostrar_estadisticas()
        
        # Demostrar verificación de permisos
        demostrar_verificacion_permisos()
        
        print("\n" + "="*80)
        print("✨ SISTEMA DE ROLES COMPLETAMENTE FUNCIONAL")
        print("   🚀 Listo para personalización completa")
        print("   🔐 60+ permisos granulares disponibles")
        print("   📊 11 categorías de funcionalidades")
        print("   🎨 Interfaz gráfica amigable")
        print("="*80)
        
    except Exception as e:
        print(f"❌ Error en demostración: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
