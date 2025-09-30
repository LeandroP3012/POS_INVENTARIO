#!/usr/bin/env python3
"""
Script de prueba para verificar la implementación de gestión de usuarios
"""

def test_imports():
    """Probar las importaciones"""
    try:
        print("🔄 Probando importaciones...")
        
        # Probar importar el controlador
        from controllers.user_controller import UserController
        print("   ✅ UserController importado correctamente")
        
        # Probar importar la vista
        from views.user_management_view import UserManagementView
        print("   ✅ UserManagementView importado correctamente")
        
        # Probar importar el modelo mejorado
        from models.user_model import UserModel
        print("   ✅ UserModel importado correctamente")
        
        # Probar importar sistema de roles
        from models.role_model import RoleModel
        print("   ✅ RoleModel importado correctamente")
        
        from controllers.role_controller import RoleController
        print("   ✅ RoleController importado correctamente")
        
        from views.role_management_view import RoleManagementView
        print("   ✅ RoleManagementView importado correctamente")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en importaciones: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_user_controller():
    """Probar la funcionalidad básica del controlador"""
    try:
        print("\n🔄 Probando UserController...")
        
        from controllers.user_controller import UserController
        
        # Crear instancia del controlador
        controller = UserController()
        print("   ✅ UserController instanciado correctamente")
        
        # Probar obtener usuarios
        users = controller.get_all_users()
        print(f"   ✅ get_all_users() ejecutado, {len(users)} usuarios encontrados")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en UserController: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_user_model():
    """Probar las nuevas funciones del modelo"""
    try:
        print("\n🔄 Probando UserModel...")
        
        from models.user_model import UserModel
        
        # Crear instancia del modelo
        model = UserModel()
        print("   ✅ UserModel instanciado correctamente")
        
        # Probar obtener usuarios
        users = model.get_all_users()
        print(f"   ✅ get_all_users() ejecutado, {len(users)} usuarios encontrados")
        
        if users:
            print(f"      Primer usuario: {users[0]}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en UserModel: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_role_controller():
    """Probar el controlador de roles"""
    try:
        print("\n🔄 Probando RoleController...")
        
        from controllers.role_controller import RoleController
        
        # Crear instancia del controlador
        controller = RoleController()
        print("   ✅ RoleController instanciado correctamente")
        
        # Probar obtener roles
        roles = controller.get_all_roles()
        print(f"   ✅ get_all_roles() ejecutado, {len(roles)} roles encontrados")
        
        if roles:
            print(f"      Primer rol: {roles[0]['name']}")
        
        # Probar obtener permisos
        permissions = controller.get_all_permissions()
        print(f"   ✅ get_all_permissions() ejecutado, {len(permissions)} permisos disponibles")
        
        # Probar permisos por categoría
        permissions_by_cat = controller.get_permissions_by_category()
        print(f"   ✅ get_permissions_by_category() ejecutado, {len(permissions_by_cat)} categorías")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en RoleController: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_role_model():
    """Probar el modelo de roles"""
    try:
        print("\n🔄 Probando RoleModel...")
        
        from models.role_model import RoleModel
        
        # Crear instancia del modelo
        model = RoleModel()
        print("   ✅ RoleModel instanciado correctamente")
        
        # Probar obtener roles
        roles = model.get_all_roles()
        print(f"   ✅ get_all_roles() ejecutado, {len(roles)} roles encontrados")
        
        if roles:
            print(f"      Primer rol: {roles[0]}")
        
        # Probar estadísticas
        stats = model.get_roles_stats()
        print(f"   ✅ get_roles_stats() ejecutado: {stats}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en RoleModel: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 PRUEBAS DE GESTIÓN DE USUARIOS")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Ejecutar pruebas
    all_tests_passed &= test_imports()
    all_tests_passed &= test_user_controller()
    all_tests_passed &= test_user_model()
    all_tests_passed &= test_role_model()
    all_tests_passed &= test_role_controller()
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("✅ TODAS LAS PRUEBAS PASARON")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
    print("=" * 50)
