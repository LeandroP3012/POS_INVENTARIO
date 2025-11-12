"""
Generador de Licencias para Sistema POS
Genera licencias únicas y las almacena en archivos
"""

import hashlib
import secrets
import json
import csv
from datetime import datetime, timedelta
from pathlib import Path


class LicenseGenerator:
    """Generador de licencias para el sistema POS"""
    
    def __init__(self, secret_key="POS_SISTEMA_2025_SECRET"):
        self.secret_key = secret_key
        self.licenses = []
    
    def generate_license_key(self, customer_name="", license_type="standard"):
        """
        Genera una clave de licencia única
        Formato: XXXX-XXXX-XXXX-XXXX
        """
        # Generar bytes aleatorios
        random_bytes = secrets.token_bytes(12)
        
        # Agregar información adicional para hacer única cada licencia
        timestamp = datetime.now().isoformat().encode()
        customer_bytes = customer_name.encode() if customer_name else b""
        
        # Combinar todo
        data = random_bytes + timestamp + customer_bytes + self.secret_key.encode()
        
        # Crear hash
        hash_obj = hashlib.sha256(data)
        hash_hex = hash_obj.hexdigest()[:16].upper()
        
        # Formatear como XXXX-XXXX-XXXX-XXXX
        parts = [hash_hex[i:i+4] for i in range(0, 16, 4)]
        license_key = "-".join(parts)
        
        return license_key
    
    def generate_activation_code(self, license_key):
        """
        Genera código de activación basado en la licencia
        Este se usará para validar que la licencia es genuina
        Compatible con el instalador Inno Setup
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
    
    def validate_license(self, license_key, activation_code):
        """Validar que una licencia y su código de activación coincidan"""
        expected_activation = self.generate_activation_code(license_key)
        return activation_code == expected_activation
    
    def generate_batch(self, count=200, license_type="standard", company_prefix=""):
        """
        Generar lote de licencias PERMANENTES (de por vida)
        
        Args:
            count: Número de licencias a generar
            license_type: Tipo de licencia (standard, premium, enterprise)
            company_prefix: Prefijo para el cliente (ej: "Cliente")
        """
        print(f"🔑 Generando {count} licencias PERMANENTES...")
        
        issue_date = datetime.now()
        
        for i in range(count):
            customer_name = f"{company_prefix}{i+1:04d}" if company_prefix else f"License{i+1:04d}"
            
            license_key = self.generate_license_key(customer_name, license_type)
            activation_code = self.generate_activation_code(license_key)
            
            license_info = {
                "license_number": i + 1,
                "license_key": license_key,
                "activation_code": activation_code,
                "customer_name": customer_name,
                "license_type": license_type,
                "issue_date": issue_date.strftime("%Y-%m-%d"),
                "expiry_date": "PERMANENTE",
                "validity": "LIFETIME",
                "status": "active"
            }
            
            self.licenses.append(license_info)
            
            if (i + 1) % 50 == 0:
                print(f"   ✓ {i + 1}/{count} licencias generadas...")
        
        print(f"   ✅ {count} licencias PERMANENTES generadas exitosamente!")
        return self.licenses
    
    def save_to_json(self, filename="licenses.json"):
        """Guardar licencias en formato JSON"""
        filepath = Path(filename)
        
        data = {
            "generated_date": datetime.now().isoformat(),
            "total_licenses": len(self.licenses),
            "secret_key_hash": hashlib.sha256(self.secret_key.encode()).hexdigest()[:16],
            "licenses": self.licenses
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Licencias guardadas en: {filepath.absolute()}")
        return filepath
    
    def save_to_csv(self, filename="licenses.csv"):
        """Guardar licencias en formato CSV (más fácil de distribuir)"""
        filepath = Path(filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if self.licenses:
                writer = csv.DictWriter(f, fieldnames=self.licenses[0].keys())
                writer.writeheader()
                writer.writerows(self.licenses)
        
        print(f"📊 Licencias guardadas en CSV: {filepath.absolute()}")
        return filepath
    
    def save_individual_files(self, output_dir="licenses"):
        """Guardar cada licencia en un archivo individual"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print(f"📁 Creando archivos individuales en: {output_path.absolute()}")
        
        for license_info in self.licenses:
            filename = f"LICENSE_{license_info['customer_name']}.txt"
            filepath = output_path / filename
            
            content = f"""
╔════════════════════════════════════════════════════════════════╗
║                  LICENCIA DE SOFTWARE - SISTEMA POS            ║
╚════════════════════════════════════════════════════════════════╝

INFORMACIÓN DE LA LICENCIA:
──────────────────────────────────────────────────────────────────
Cliente:            {license_info['customer_name']}
Número de Licencia: {license_info['license_number']:04d}
Tipo de Licencia:   {license_info['license_type'].upper()}

CLAVE DE LICENCIA:
──────────────────────────────────────────────────────────────────
{license_info['license_key']}

CÓDIGO DE ACTIVACIÓN:
──────────────────────────────────────────────────────────────────
{license_info['activation_code']}

VALIDEZ:
──────────────────────────────────────────────────────────────────
Fecha de Emisión:   {license_info['issue_date']}
Fecha de Expiración: {license_info['expiry_date']}
Vigencia:           {license_info['validity']}

INSTRUCCIONES DE INSTALACIÓN:
──────────────────────────────────────────────────────────────────
1. Ejecutar el instalador POS_Setup.exe
2. Cuando se solicite, ingresar la CLAVE DE LICENCIA
3. Durante la activación, ingresar el CÓDIGO DE ACTIVACIÓN
4. Completar el proceso de instalación

IMPORTANTE:
──────────────────────────────────────────────────────────────────
• Esta licencia es válida para UNA instalación
• Mantener este archivo en un lugar seguro
• Para soporte técnico: soporte@tuempresa.com

╔════════════════════════════════════════════════════════════════╗
║  © 2025 Tu Empresa. Todos los derechos reservados.             ║
╚════════════════════════════════════════════════════════════════╝
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content.strip())
        
        print(f"   ✅ {len(self.licenses)} archivos creados")
        return output_path
    
    def create_master_list(self, filename="LICENCIAS_MAESTRAS.txt"):
        """Crear lista maestra con todas las licencias (para tu control)"""
        filepath = Path(filename)
        
        content = f"""
╔════════════════════════════════════════════════════════════════════════╗
║               LISTA MAESTRA DE LICENCIAS - SISTEMA POS                 ║
║                   ⚠️  DOCUMENTO CONFIDENCIAL ⚠️                        ║
╚════════════════════════════════════════════════════════════════════════╝

Fecha de Generación: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Total de Licencias: {len(self.licenses)}

╔════════════════════════════════════════════════════════════════════════╗
"""
        
        for lic in self.licenses:
            content += f"""
┌────────────────────────────────────────────────────────────────────────┐
│ #{lic['license_number']:04d} - {lic['customer_name']:<20} │ {lic['license_type'].upper():<10}
├────────────────────────────────────────────────────────────────────────┤
│ Licencia:   {lic['license_key']}
│ Activación: {lic['activation_code']}
│ Vigencia:   {lic['issue_date']} → {lic['expiry_date']}
└────────────────────────────────────────────────────────────────────────┘
"""
        
        content += """
╚════════════════════════════════════════════════════════════════════════╝

INSTRUCCIONES DE USO:
─────────────────────────────────────────────────────────────────────────
1. Cada licencia debe entregarse por separado a cada cliente
2. Mantener este archivo maestro en lugar seguro
3. No compartir los códigos de activación públicamente
4. Registrar a qué cliente se entregó cada licencia

NOTAS DE SEGURIDAD:
─────────────────────────────────────────────────────────────────────────
• Este archivo contiene información sensible
• Guardar en ubicación segura con respaldo
• No enviar por correo electrónico sin cifrar
• Considerar usar un gestor de contraseñas o base de datos

═══════════════════════════════════════════════════════════════════════════
  © 2025 Tu Empresa - Documento Confidencial
═══════════════════════════════════════════════════════════════════════════
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"📋 Lista maestra creada: {filepath.absolute()}")
        return filepath


def main():
    """Función principal"""
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "GENERADOR DE LICENCIAS - SISTEMA POS" + " " * 17 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # Configuración
    print("⚙️  CONFIGURACIÓN:")
    print("-" * 70)
    
    count = int(input("Cantidad de licencias a generar [200]: ") or "200")
    
    license_types = {
        "1": "standard",
        "2": "premium", 
        "3": "enterprise"
    }
    
    print("\nTipos de licencia:")
    print("  1. Standard   - Licencia básica")
    print("  2. Premium    - Licencia con características adicionales")
    print("  3. Enterprise - Licencia corporativa completa")
    
    type_choice = input("Seleccione tipo [1]: ") or "1"
    license_type = license_types.get(type_choice, "standard")
    
    company_prefix = input("Prefijo para clientes [Cliente]: ") or "Cliente"
    
    print("\n" + "=" * 70)
    print(f"📝 Resumen:")
    print(f"   • Cantidad: {count} licencias")
    print(f"   • Tipo: {license_type}")
    print(f"   • Validez: PERMANENTE (de por vida)")
    print(f"   • Prefijo: {company_prefix}")
    print("=" * 70)
    
    confirm = input("\n¿Generar licencias? (S/N): ")
    if confirm.upper() != 'S':
        print("❌ Operación cancelada")
        return
    
    print("\n" + "=" * 70)
    
    # Generar licencias
    generator = LicenseGenerator()
    generator.generate_batch(
        count=count,
        license_type=license_type,
        company_prefix=company_prefix
    )
    
    print("\n📦 GUARDANDO ARCHIVOS:")
    print("-" * 70)
    
    # Guardar en diferentes formatos
    generator.save_to_json("licenses_database.json")
    generator.save_to_csv("licenses_list.csv")
    generator.save_individual_files("licenses_individual")
    generator.create_master_list("LICENCIAS_MAESTRAS.txt")
    
    print("\n" + "=" * 70)
    print("✅ PROCESO COMPLETADO")
    print("=" * 70)
    print("\n📁 Archivos generados:")
    print("   • licenses_database.json     - Base de datos JSON")
    print("   • licenses_list.csv          - Lista en Excel")
    print("   • licenses_individual/       - Archivos individuales para clientes")
    print("   • LICENCIAS_MAESTRAS.txt     - Lista maestra (⚠️ CONFIDENCIAL)")
    print("\n💡 Distribución:")
    print("   • Entregar archivos de licenses_individual/ a cada cliente")
    print("   • Guardar LICENCIAS_MAESTRAS.txt en lugar seguro")
    print("   • Usar licenses_list.csv para control y seguimiento")
    
    print("\n" + "=" * 70)
    input("\nPresione ENTER para salir...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresione ENTER para salir...")
