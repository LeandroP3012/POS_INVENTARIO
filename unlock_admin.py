#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Herramienta de Desbloqueo de Administrador
Sistema POS - Corrige problemas de autenticación del usuario admin
"""

import sys
import os
import hashlib
from datetime import datetime

# Agregar directorio actual al path
sys.path.append(os.getcwd())

try:
    from models.user_model import UserModel
    from database.connection import DatabaseConnection
    from models.auth_model import AuthModel
except ImportError as e:
    print(f"ERROR: No se pudieron importar los módulos necesarios: {e}")
    print("Asegúrate de ejecutar este script desde el directorio raíz del proyecto POS")
    sys.exit(1)
class AdminUnlocker:
    """Herramienta para desbloquear y corregir el usuario administrador"""
    
    def __init__(self):
        self.user_model = UserModel()
        self.db = DatabaseConnection()
        self.auth_model = AuthModel()
        
    def hash_password(self, password: str) -> str:
        """Crear hash SHA-256 de la contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def test_current_status(self):
        """Probar el estado actual del sistema de autenticación"""
        print("=" * 60)
        print("DIAGNÓSTICO DEL SISTEMA DE AUTENTICACIÓN")
        print("=" * 60)
        
        # 1. Probar conexión a BD
        print("\n1. Conexión a base de datos:")
        db_connected = self.db.connect()
        print(f"   Estado: {'OK - CONECTADA' if db_connected else 'ERROR - SIN CONEXIÓN (usando fallback)'}")
        
        if db_connected:
            print(f"   Host: {self.db.host}")
            print(f"   Database: {self.db.database}")
        
        # 2. Buscar usuario admin
        print("\n2. Usuario administrador:")
        admin_user = self.user_model.find_by_username("admin")
        
        if admin_user:
            print("   Estado: OK - ENCONTRADO")
            print(f"   Nombre: {admin_user.get('full_name', 'N/A')}")
            print(f"   Activo: {'OK - SÍ' if admin_user.get('active', True) else 'ERROR - NO'}")
            print(f"   Tipo: {admin_user.get('user_type', 'N/A')}")
            
            # 3. Verificar contraseña
            print("\n3. Contraseña '123456':")
            expected_hash = self.hash_password("123456")
            stored_hash = admin_user.get('password_hash', '')
            
            password_ok = (expected_hash == stored_hash)
            print(f"   Estado: {'OK - CORRECTA' if password_ok else 'ERROR - INCORRECTA'}")
            
            if not password_ok:
                print(f"   Hash esperado:   {expected_hash}")
                print(f"   Hash almacenado: {stored_hash}")
            
            # 4. Verificar bloqueos
            print("\n4. Estado de bloqueo:")
            is_locked = self.user_model.is_user_locked(admin_user)
            failed_attempts = admin_user.get('failed_attempts', 0)
            
            print(f"   Bloqueado: {'ERROR - SÍ' if is_locked else 'OK - NO'}")
            print(f"   Intentos fallidos: {failed_attempts}")
            
            # 5. Probar autenticación completa
            print("\n5. Autenticación completa:")
            auth_result = self.user_model.authenticate("admin", "123456")
            
            if auth_result:
                print("   Estado: OK - FUNCIONANDO")
                print(f"   ID autenticado: {auth_result.get('id')}")
            else:
                print("   Estado: ERROR - FALLANDO")
            
            return {
                'db_connected': db_connected,
                'admin_found': True,
                'admin_active': admin_user.get('active', True),
                'password_correct': password_ok,
                'is_locked': is_locked,
                'auth_working': bool(auth_result),
                'admin_data': admin_user
            }
        else:
            print("   Estado: ERROR - NO ENCONTRADO")
            return {
                'db_connected': db_connected,
                'admin_found': False,
                'admin_active': False,
                'password_correct': False,
                'is_locked': False,
                'auth_working': False,
                'admin_data': None
            }
    
    def fix_default_users(self):
        """Corregir usuarios por defecto en memoria"""
        print("\n" + "=" * 60)
        print("CORRIGIENDO USUARIOS POR DEFECTO")
        print("=" * 60)
        
        try:
            # Forzar recarga del modelo con contraseña correcta
            correct_hash = self.hash_password("123456")
            
            # Verificar si el hash actual es correcto
            current_admin = self.user_model.default_users.get('admin', {})
            current_hash = current_admin.get('password_hash', '')
            
            if current_hash == correct_hash:
                print("OK - Los usuarios por defecto ya tienen la contraseña correcta")
                return True
            
            # Actualizar hash en memoria
            if 'admin' in self.user_model.default_users:
                self.user_model.default_users['admin']['password_hash'] = correct_hash
                self.user_model.default_users['admin']['active'] = True
                self.user_model.default_users['admin']['failed_attempts'] = 0
                self.user_model.default_users['admin']['locked_until'] = None
                
                print("OK - Contraseña del admin corregida en memoria")
                print("   Nueva contraseña: 123456")
                return True
            else:
                print("ERROR - Usuario admin no encontrado en usuarios por defecto")
                return False
                
        except Exception as e:
            print(f"ERROR - Error corrigiendo usuarios por defecto: {e}")
            return False
    
    def run_unlock_process(self):
        """Ejecutar proceso completo de desbloqueo"""
        print("INICIANDO PROCESO DE DESBLOQUEO DEL ADMINISTRADOR")
        print("=" * 80)
        
        # 1. Diagnóstico inicial
        status = self.test_current_status()
        
        # 2. Determinar qué necesita arreglo
        needs_fix = (
            not status['admin_found'] or
            not status['admin_active'] or
            not status['password_correct'] or
            status['is_locked'] or
            not status['auth_working']
        )
        
        if not needs_fix:
            print("\n" + "=" * 60)
            print("OK - SISTEMA FUNCIONANDO CORRECTAMENTE")
            print("=" * 60)
            print("No se necesitan correcciones.")
            print("Credenciales: admin / 123456")
            return True
        
        print("\n" + "=" * 60)
        print("APLICANDO CORRECCIONES")
        print("=" * 60)
        
        # 3. Corregir usuarios por defecto
        self.fix_default_users()
        
        # 4. Verificación final
        print("\n" + "=" * 60)
        print("VERIFICACIÓN FINAL")
        print("=" * 60)
        
        final_status = self.test_current_status()
        
        if final_status['auth_working']:
            print("\n" + "=" * 60)
            print("OK - DESBLOQUEO EXITOSO")
            print("=" * 60)
            print("El usuario administrador ha sido reparado correctamente.")
            print()
            print("CREDENCIALES DE ACCESO:")
            print("   Usuario: admin")
            print("   Contraseña: 123456")
            print()
            print("Ahora puedes iniciar sesión normalmente.")
            return True
        else:
            print("\n" + "=" * 60)
            print("ERROR - DESBLOQUEO PARCIAL")
            print("=" * 60)
            print("Se aplicaron algunas correcciones pero el problema persiste.")
            return False

def main():
    """Función principal"""
    print("HERRAMIENTA DE DESBLOQUEO DEL ADMINISTRADOR")
    print("Sistema POS - Versión 2.0")
    print("=" * 80)
    
    try:
        unlocker = AdminUnlocker()
        
        if len(sys.argv) > 1 and sys.argv[1] == "--test":
            # Solo diagnóstico
            print("MODO DIAGNÓSTICO (solo pruebas)")
            unlocker.test_current_status()
        else:
            # Proceso completo de desbloqueo
            success = unlocker.run_unlock_process()
            sys.exit(0 if success else 1)
            
    except KeyboardInterrupt:
        print("\n\nProceso interrumpido por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError inesperado: {e}")
        print("Verifica que estés ejecutando el script desde el directorio correcto.")
        sys.exit(1)

if __name__ == "__main__":
    main()
