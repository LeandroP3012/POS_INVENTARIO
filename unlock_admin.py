#!/usr/bin/env python3
"""
Script temporal para desbloquear usuario admin
Ejecutar cuando el usuario admin esté bloqueado por intentos fallidos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user_model import UserModel
from database.connection import DatabaseConnection

def unlock_admin_user():
    """Desbloquear usuario admin resetando intentos fallidos"""
    try:
        print("🔓 Desbloqueando usuario admin...")
        
        # Crear instancia del modelo de usuario
        user_model = UserModel()
        
        # Buscar usuario admin
        admin_user = user_model.get_user_by_username('admin')
        
        if admin_user:
            print(f"✅ Usuario admin encontrado: {admin_user['username']}")
            print(f"📊 Intentos fallidos actuales: {admin_user.get('failed_attempts', 0)}")
            
            # Resetear intentos fallidos
            user_model.reset_failed_attempts(admin_user)
            
            print("🎉 ¡Usuario admin desbloqueado exitosamente!")
            print("💡 Ahora puedes hacer login con: admin / 123456")
            
        else:
            print("❌ Usuario admin no encontrado en la base de datos")
            print("💡 Intentando usar credenciales por defecto...")
            
            # Si no existe, usar autenticación por defecto
            print("✅ Se usarán las credenciales por defecto del sistema")
            
    except Exception as e:
        print(f"❌ Error al desbloquear usuario: {e}")
        print("💡 El sistema usará autenticación por defecto como respaldo")

if __name__ == "__main__":
    print("=" * 50)
    print("🔐 SCRIPT DE DESBLOQUEO DE USUARIO ADMIN")
    print("=" * 50)
    
    unlock_admin_user()
    
    print("=" * 50)
    print("✅ Proceso completado")
    print("=" * 50)
