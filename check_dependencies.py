"""
Script para verificar e instalar dependencias necesarias para el sistema de permisos
"""

import subprocess
import sys

def check_and_install_dependencies():
    """Verificar e instalar dependencias necesarias"""
    
    print("\n" + "="*70)
    print("🔍 VERIFICACIÓN DE DEPENDENCIAS")
    print("="*70 + "\n")
    
    dependencies = [
        ('openpyxl', 'openpyxl>=3.1.0', 'Exportación a Excel')
    ]
    
    missing_dependencies = []
    
    for package_name, pip_name, description in dependencies:
        try:
            __import__(package_name)
            print(f"✅ {package_name:20} - Instalado correctamente ({description})")
        except ImportError:
            print(f"❌ {package_name:20} - NO instalado ({description})")
            missing_dependencies.append(pip_name)
    
    if missing_dependencies:
        print("\n" + "="*70)
        print("📦 INSTALANDO DEPENDENCIAS FALTANTES")
        print("="*70 + "\n")
        
        for dep in missing_dependencies:
            print(f"Instalando {dep}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                print(f"   ✅ {dep} instalado exitosamente\n")
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Error instalando {dep}: {e}\n")
                return False
        
        print("\n" + "="*70)
        print("✅ TODAS LAS DEPENDENCIAS INSTALADAS")
        print("="*70 + "\n")
        return True
    else:
        print("\n" + "="*70)
        print("✅ TODAS LAS DEPENDENCIAS YA ESTÁN INSTALADAS")
        print("="*70 + "\n")
        return True

if __name__ == "__main__":
    success = check_and_install_dependencies()
    
    if success:
        print("💡 El sistema está listo para usar la función de exportación a Excel\n")
        sys.exit(0)
    else:
        print("⚠️ Algunas dependencias no se pudieron instalar")
        print("   Ejecuta manualmente: pip install -r requirements.txt\n")
        sys.exit(1)
