"""
Script de diagnóstico para verificar el estado real del usuario 15 en la DB
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.connection import DatabaseConnection

def check_user_15():
    """Verifica el estado actual del usuario 15"""
    db = DatabaseConnection()
    
    print("\n" + "="*80)
    print("📊 ESTADO ACTUAL DEL USUARIO 15 EN LA BASE DE DATOS")
    print("="*80 + "\n")
    
    query = """
    SELECT 
        u.id,
        u.username,
        u.full_name,
        u.email,
        u.user_type,
        u.role_id,
        u.active,
        u.phone,
        u.avatar_path,
        u.created_at,
        u.updated_at,
        r.name as role_name,
        r.code as role_code
    FROM users u
    LEFT JOIN roles r ON u.role_id = r.id
    WHERE u.id = 15
    """
    
    result = db.execute_query(query)
    
    if result:
        result = result[0]  # Obtener el primer resultado
    
    if result:
        print(f"✅ Usuario encontrado:\n")
        print(f"   ID:           {result['id']}")
        print(f"   Username:     {result['username']}")
        print(f"   Full Name:    {result['full_name']}")
        print(f"   Email:        {result['email']}")
        print(f"   User Type:    {result['user_type']}")
        print(f"   Role ID:      {result['role_id']}")
        print(f"   Role Name:    {result['role_name']}")
        print(f"   Role Code:    {result['role_code']}")
        print(f"   Active:       {result['active']}")
        print(f"   Phone:        {result['phone']}")
        print(f"   Avatar Path:  {result['avatar_path']}")
        print(f"   Created At:   {result['created_at']}")
        print(f"   Updated At:   {result['updated_at']}")
        
        print("\n" + "="*80)
        print("🎯 VALORES ESPERADOS SEGÚN EL ÚLTIMO UPDATE:")
        print("="*80 + "\n")
        print(f"   Full Name:    testv6")
        print(f"   Email:        testv6@gmail.com")
        print(f"   User Type:    supervisor")
        print(f"   Role ID:      12")
        print(f"   Active:       1 (True)")
        print(f"   Phone:        '' (vacío)")
        print(f"   Avatar Path:  '' (vacío)")
        
        print("\n" + "="*80)
        print("🔍 COMPARACIÓN:")
        print("="*80 + "\n")
        
        matches = []
        mismatches = []
        
        if result['full_name'] == 'testv6':
            matches.append("✅ full_name COINCIDE")
        else:
            mismatches.append(f"❌ full_name: DB={result['full_name']} vs Esperado=testv6")
            
        if result['email'] == 'testv6@gmail.com':
            matches.append("✅ email COINCIDE")
        else:
            mismatches.append(f"❌ email: DB={result['email']} vs Esperado=testv6@gmail.com")
            
        if result['user_type'] == 'supervisor':
            matches.append("✅ user_type COINCIDE")
        else:
            mismatches.append(f"❌ user_type: DB={result['user_type']} vs Esperado=supervisor")
            
        if result['role_id'] == 12:
            matches.append("✅ role_id COINCIDE")
        else:
            mismatches.append(f"❌ role_id: DB={result['role_id']} vs Esperado=12")
            
        if result['active'] == 1:
            matches.append("✅ active COINCIDE")
        else:
            mismatches.append(f"❌ active: DB={result['active']} vs Esperado=1")
        
        for match in matches:
            print(f"   {match}")
            
        if mismatches:
            print("\n   ⚠️  VALORES QUE NO COINCIDEN:")
            for mismatch in mismatches:
                print(f"   {mismatch}")
        else:
            print("\n   🎉 TODOS LOS VALORES COINCIDEN - LA BASE DE DATOS ESTÁ ACTUALIZADA CORRECTAMENTE")
            
    else:
        print("❌ Usuario 15 no encontrado en la base de datos")
    
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    check_user_15()
