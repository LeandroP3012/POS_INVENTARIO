"""
Validador de Licencias para Sistema POS
Se utiliza durante la instalación y en la aplicación
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path


class LicenseValidator:
    """Validador de licencias del sistema POS"""
    
    def __init__(self, secret_key="POS_SISTEMA_2025_SECRET"):
        self.secret_key = secret_key
    
    def generate_activation_code(self, license_key):
        """
        Genera código de activación basado en la licencia
        (Debe ser idéntico al del generador e instalador)
        """
        data = license_key + self.secret_key
        
        # Función hash simple compatible con Inno Setup
        def simple_hash(s):
            hash_val = 5381
            for c in s:
                hash_val = ((hash_val << 5) + hash_val) + ord(c)
                hash_val = hash_val & 0xFFFFFFFF  # Mantener 32 bits
            return format(hash_val, '08X')
        
        # Generar múltiples hashes
        hash1 = simple_hash(data)
        hash2 = simple_hash(data + '1')
        hash3 = simple_hash(data + '2')
        hash4 = simple_hash(data + '3')
        
        full_hash = (hash1 + hash2 + hash3 + hash4).upper()
        
        # Formatear como XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX
        parts = [full_hash[i:i+4] for i in range(0, 32, 4)]
        return "-".join(parts)
    
    def validate_license_format(self, license_key):
        """Validar formato de la licencia: XXXX-XXXX-XXXX-XXXX"""
        if not license_key:
            return False, "Licencia vacía"
        
        parts = license_key.split('-')
        
        if len(parts) != 4:
            return False, "Formato inválido (debe ser XXXX-XXXX-XXXX-XXXX)"
        
        for part in parts:
            if len(part) != 4:
                return False, "Cada sección debe tener 4 caracteres"
            if not part.isalnum():
                return False, "Solo se permiten letras y números"
        
        return True, "Formato válido"
    
    def validate_activation_format(self, activation_code):
        """Validar formato del código de activación"""
        if not activation_code:
            return False, "Código de activación vacío"
        
        parts = activation_code.split('-')
        
        if len(parts) != 8:
            return False, "Formato inválido (debe tener 8 secciones)"
        
        for part in parts:
            if len(part) != 4:
                return False, "Cada sección debe tener 4 caracteres"
            if not all(c in '0123456789ABCDEF' for c in part.upper()):
                return False, "Código de activación contiene caracteres inválidos"
        
        return True, "Formato válido"
    
    def validate_license(self, license_key, activation_code):
        """
        Validar que una licencia y su código de activación coincidan
        
        Returns:
            (bool, str): (es_válida, mensaje)
        """
        # Validar formatos
        valid, msg = self.validate_license_format(license_key)
        if not valid:
            return False, f"Licencia inválida: {msg}"
        
        valid, msg = self.validate_activation_format(activation_code)
        if not valid:
            return False, f"Código de activación inválido: {msg}"
        
        # Generar código esperado
        expected_activation = self.generate_activation_code(license_key)
        
        # Comparar (case-insensitive)
        if activation_code.upper() != expected_activation.upper():
            return False, "El código de activación no corresponde a esta licencia"
        
        return True, "Licencia válida"
    
    def save_license_info(self, license_key, activation_code, config_file="config/license.json"):
        """Guardar información de licencia activada"""
        filepath = Path(config_file)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        license_data = {
            "license_key": license_key,
            "activation_code": activation_code,
            "activation_date": datetime.now().isoformat(),
            "machine_id": self.get_machine_id(),
            "status": "active"
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(license_data, f, indent=2)
        
        return filepath
    
    def load_license_info(self, config_file="config/license.json"):
        """Cargar información de licencia guardada"""
        filepath = Path(config_file)
        
        if not filepath.exists():
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    
    def is_license_activated(self, config_file="config/license.json"):
        """Verificar si hay una licencia activada"""
        license_info = self.load_license_info(config_file)
        
        if not license_info:
            return False, "No hay licencia activada"
        
        # Validar la licencia guardada
        valid, msg = self.validate_license(
            license_info.get('license_key', ''),
            license_info.get('activation_code', '')
        )
        
        if not valid:
            return False, f"Licencia guardada inválida: {msg}"
        
        return True, "Licencia activa y válida"
    
    def get_machine_id(self):
        """Obtener ID único de la máquina (opcional, para licencias por máquina)"""
        try:
            import uuid
            return str(uuid.getnode())
        except:
            return "unknown"
    
    def check_license_from_database(self, license_key, database_file="licenses_database.json"):
        """
        Verificar licencia contra la base de datos maestra
        (Solo para uso interno, no incluir en distribución)
        """
        filepath = Path(database_file)
        
        if not filepath.exists():
            return None, "Base de datos de licencias no encontrada"
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            licenses = data.get('licenses', [])
            
            for lic in licenses:
                if lic['license_key'] == license_key:
                    # Verificar si está expirada
                    expiry_date = datetime.strptime(lic['expiry_date'], '%Y-%m-%d')
                    if datetime.now() > expiry_date:
                        return lic, "Licencia expirada"
                    
                    if lic['status'] != 'active':
                        return lic, f"Licencia {lic['status']}"
                    
                    return lic, "Licencia válida en base de datos"
            
            return None, "Licencia no encontrada en base de datos"
            
        except Exception as e:
            return None, f"Error al leer base de datos: {e}"


# Función para uso rápido
def validate_quick(license_key, activation_code):
    """Validación rápida de licencia"""
    validator = LicenseValidator()
    return validator.validate_license(license_key, activation_code)


if __name__ == "__main__":
    # Modo de prueba interactivo
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "VALIDADOR DE LICENCIAS - SISTEMA POS" + " " * 17 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    validator = LicenseValidator()
    
    while True:
        print("\n" + "=" * 70)
        license_key = input("Ingrese clave de licencia (o 'salir'): ").strip()
        
        if license_key.lower() == 'salir':
            break
        
        activation_code = input("Ingrese código de activación: ").strip()
        
        print("\n🔍 Validando...")
        valid, message = validator.validate_license(license_key, activation_code)
        
        print("\n" + "-" * 70)
        if valid:
            print(f"✅ {message}")
            print(f"   Licencia: {license_key}")
            print(f"   Código:   {activation_code}")
            
            save = input("\n¿Guardar esta licencia? (S/N): ")
            if save.upper() == 'S':
                filepath = validator.save_license_info(license_key, activation_code)
                print(f"💾 Licencia guardada en: {filepath}")
        else:
            print(f"❌ {message}")
        print("-" * 70)
    
    print("\n👋 ¡Hasta luego!")
