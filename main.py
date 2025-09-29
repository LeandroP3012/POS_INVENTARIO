"""
Archivo Principal del Sistema POS
Punto de entrada de la aplicación
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import logging

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup_logging():
    """Configurar sistema de logging"""
    try:
        # Crear directorio de logs
        os.makedirs('logs', exist_ok=True)
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/pos_system.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        return logging.getLogger('POS_SYSTEM')
        
    except Exception as e:
        print(f"Error configurando logging: {e}")
        return None

def check_dependencies():
    """Verificar dependencias del sistema"""
    try:
        # Verificar módulos necesarios
        required_modules = [
            ('tkinter', 'Interfaz gráfica'),
            ('mysql.connector', 'Conexión a MySQL'),
            ('hashlib', 'Encriptación'),
            ('json', 'Manejo de JSON'),
            ('datetime', 'Manejo de fechas'),
            ('logging', 'Sistema de logs')
        ]
        
        missing_modules = []
        
        for module_name, description in required_modules:
            try:
                if module_name == 'mysql.connector':
                    import mysql.connector
                else:
                    __import__(module_name)
            except ImportError:
                missing_modules.append(f"- {module_name} ({description})")
        
        if missing_modules:
            error_msg = "Faltan las siguientes dependencias:\n\n"
            error_msg += "\n".join(missing_modules)
            error_msg += "\n\nPor favor instala las dependencias faltantes."
            
            # Mostrar error sin tkinter si no está disponible
            if 'tkinter' in [m.split(' ')[1] for m in missing_modules]:
                print(f"ERROR: {error_msg}")
            else:
                root = tk.Tk()
                root.withdraw()  # Ocultar ventana principal
                messagebox.showerror("Dependencias Faltantes", error_msg)
                root.destroy()
            
            return False
        
        return True
        
    except Exception as e:
        print(f"Error verificando dependencias: {e}")
        return False

def check_directory_structure():
    """Verificar y crear estructura de directorios"""
    try:
        required_dirs = [
            'config',
            'controllers',
            'database',
            'logs',
            'models',
            'views',
            'assets'
        ]
        
        for directory in required_dirs:
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
        
        return True
        
    except Exception as e:
        print(f"Error creando estructura de directorios: {e}")
        return False

def main():
    """Función principal de la aplicación"""
    try:
        print("=" * 50)
        print("🏪 SISTEMA POS v1.0")
        print("Iniciando aplicación...")
        print("=" * 50)
        
        # Verificar dependencias
        print("Verificando dependencias...")
        if not check_dependencies():
            print("❌ Error: Dependencias faltantes")
            input("Presiona Enter para salir...")
            sys.exit(1)
        print("✅ Dependencias verificadas")
        
        # Configurar logging
        print("Configurando sistema de logs...")
        logger = setup_logging()
        if not logger:
            print("⚠️  Advertencia: No se pudo configurar el logging")
        else:
            print("✅ Sistema de logs configurado")
            logger.info("Sistema POS iniciado")
        
        # Verificar estructura de directorios
        print("Verificando estructura de directorios...")
        if not check_directory_structure():
            print("❌ Error: No se pudo crear la estructura de directorios")
            if logger:
                logger.error("Error creando estructura de directorios")
            sys.exit(1)
        print("✅ Estructura de directorios verificada")
        
        # Importar y iniciar controlador principal
        print("Iniciando controlador principal...")
        try:
            from controllers.main_controller import MainController
            
            # Crear y ejecutar aplicación
            app = MainController()
            app.start()
            
        except ImportError as e:
            error_msg = f"Error importando controladores: {e}"
            print(f"❌ {error_msg}")
            if logger:
                logger.error(error_msg)
            
            # Mostrar error con GUI si está disponible
            try:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("Error de Importación", 
                                   f"No se pudieron cargar los módulos del sistema:\n\n{e}\n\nVerifica que todos los archivos estén presentes.")
                root.destroy()
            except:
                input("Presiona Enter para salir...")
            
            sys.exit(1)
        
        except Exception as e:
            error_msg = f"Error iniciando aplicación: {e}"
            print(f"❌ {error_msg}")
            if logger:
                logger.error(error_msg)
            
            try:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("Error Fatal", 
                                   f"No se pudo iniciar la aplicación:\n\n{e}")
                root.destroy()
            except:
                input("Presiona Enter para salir...")
            
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n⚠️  Aplicación interrumpida por el usuario")
        if logger:
            logger.info("Aplicación interrumpida por el usuario")
        sys.exit(0)
    
    except Exception as e:
        error_msg = f"Error fatal no manejado: {e}"
        print(f"💥 {error_msg}")
        try:
            if logger:
                logger.critical(error_msg)
        except:
            pass
        
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error Fatal", 
                               f"Error crítico del sistema:\n\n{e}\n\nLa aplicación se cerrará.")
            root.destroy()
        except:
            input("Presiona Enter para salir...")
        
        sys.exit(1)

if __name__ == "__main__":
    main()
