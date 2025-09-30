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

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 PRUEBAS DE GESTIÓN DE USUARIOS")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Ejecutar pruebas
    all_tests_passed &= test_imports()
    all_tests_passed &= test_user_controller()
    all_tests_passed &= test_user_model()
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("✅ TODAS LAS PRUEBAS PASARON")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
    print("=" * 50)
