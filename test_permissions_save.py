"""
Script de prueba para validar guardado de permisos
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.role_model import RoleModel

def test_permissions_save():
    """Probar guardado de permisos"""
    
    print("\n" + "="*80)
    print("🧪 TEST DE GUARDADO DE PERMISOS")
    print("="*80 + "\n")
    
    # Crear modelo
    role_model = RoleModel()
    
    # 1. Obtener permisos disponibles
    print("1️⃣ Obteniendo permisos disponibles...")
    available_perms = role_model.get_all_available_permissions()
    print(f"   ✅ Total de permisos disponibles: {len(available_perms)}")
    print(f"   📝 Primeros 10: {available_perms[:10]}")
    
    # 2. Obtener permisos por categoría
    print("\n2️⃣ Obteniendo permisos por categoría...")
    perms_by_cat = role_model.get_permissions_by_category()
    print(f"   ✅ Total de categorías: {len(perms_by_cat)}")
    for cat, perms in perms_by_cat.items():
        print(f"   📂 {cat}: {len(perms)} permisos")
    
    # 3. Obtener un rol para probar
    print("\n3️⃣ Obteniendo rol de prueba...")
    test_role = role_model.get_role_by_id(3)  # Gerente
    if test_role:
        print(f"   ✅ Rol encontrado: {test_role['name']}")
        print(f"   📋 Permisos actuales: {test_role.get('permissions', [])}")
    else:
        print("   ❌ No se encontró el rol con ID 3")
        return
    
    # 4. Preparar datos de prueba
    print("\n4️⃣ Preparando datos de prueba...")
    test_permissions = [
        'users.view',
        'users.create',
        'users.edit',
        'roles.view',
        'dashboard.view'
    ]
    print(f"   📦 Permisos de prueba: {test_permissions}")
    
    # 5. Validar datos
    print("\n5️⃣ Validando datos...")
    is_valid, errors = role_model.validate_role_data(
        {'permissions': test_permissions},
        is_update=True
    )
    print(f"   📊 Validación: válido={is_valid}")
    if errors:
        print(f"   ❌ Errores: {errors}")
    else:
        print(f"   ✅ Sin errores")
    
    # 6. Intentar actualizar
    print("\n6️⃣ Intentando actualizar rol...")
    success = role_model.update_role(3, {'permissions': test_permissions})
    print(f"   📊 Resultado: {success}")
    
    # 7. Verificar cambios
    print("\n7️⃣ Verificando cambios...")
    updated_role = role_model.get_role_by_id(3)
    if updated_role:
        print(f"   ✅ Rol recuperado: {updated_role['name']}")
        print(f"   📋 Permisos después de actualizar: {updated_role.get('permissions', [])}")
        
        if updated_role.get('permissions') == test_permissions:
            print(f"   ✅ ¡PERMISOS GUARDADOS CORRECTAMENTE!")
        else:
            print(f"   ❌ Los permisos NO coinciden")
            print(f"      Esperado: {test_permissions}")
            print(f"      Obtenido: {updated_role.get('permissions', [])}")
    
    print("\n" + "="*80)
    print("🏁 TEST COMPLETADO")
    print("="*80 + "\n")

if __name__ == "__main__":
    test_permissions_save()
