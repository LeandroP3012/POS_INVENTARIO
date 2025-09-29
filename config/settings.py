"""
Configuraciones globales del Sistema POS
"""

import os
import json
from typing import Dict, Any
from datetime import datetime

class SystemSettings:
    """Configuraciones centralizadas del sistema POS"""
    
    # Información de la aplicación
    APP_INFO = {
        'NAME': 'Sistema POS Avanzado',
        'VERSION': '2.0.0',
        'DEVELOPER': 'Tu Empresa',
        'DESCRIPTION': 'Sistema de Punto de Venta con arquitectura MVC',
        'COPYRIGHT': f'© {datetime.now().year} Tu Empresa. Todos los derechos reservados.'
    }
    
    # Configuración de base de datos
    DATABASE = {
        'CONFIG_FILE': 'config/database.json',
        'BACKUP_ENABLED': True,
        'BACKUP_INTERVAL_HOURS': 24,
        'MAX_BACKUPS': 7,
        'AUTO_CREATE_TABLES': True
    }
    
    # Configuración de seguridad
    SECURITY = {
        'PASSWORD_MIN_LENGTH': 6,
        'PASSWORD_MAX_LENGTH': 128,
        'SESSION_TIMEOUT': 3600,  # 1 hora en segundos
        'MAX_LOGIN_ATTEMPTS': 3,
        'LOCKOUT_DURATION': 900,  # 15 minutos en segundos
        'PASSWORD_HASH_ALGORITHM': 'SHA256',
        'REQUIRE_STRONG_PASSWORDS': False,
        'ENABLE_2FA': False
    }
    
    # Configuración de interfaz
    UI = {
        'WINDOW_STATE': 'zoomed',
        'WINDOW_WIDTH': 1200,
        'WINDOW_HEIGHT': 800,
        'MIN_WIDTH': 1024,
        'MIN_HEIGHT': 768,
        'THEME_DEFAULT': 'light',
        'FONT_DEFAULT': ('Segoe UI', 10),
        'FONT_TITLE': ('Segoe UI', 16, 'bold'),
        'FONT_SUBTITLE': ('Segoe UI', 12, 'bold'),
        'FONT_SMALL': ('Segoe UI', 8),
        'ENABLE_ANIMATIONS': True,
        'SHOW_TOOLTIPS': True
    }
    
    # Esquema de colores del sistema
    COLORS = {
        # Colores principales
        'PRIMARY': '#2c3e50',      # Azul oscuro
        'SECONDARY': '#34495e',    # Gris azulado
        'ACCENT': '#3498db',       # Azul brillante
        
        # Colores de estado
        'SUCCESS': '#27ae60',      # Verde
        'WARNING': '#f39c12',      # Naranja
        'DANGER': '#e74c3c',       # Rojo
        'INFO': '#17a2b8',         # Azul claro
        
        # Colores neutros
        'LIGHT': '#ecf0f1',        # Gris muy claro
        'DARK': '#2c3e50',         # Azul muy oscuro
        'WHITE': '#ffffff',        # Blanco
        'BLACK': '#000000',        # Negro
        'MUTED': '#6c757d',        # Gris medio
        
        # Colores de fondo
        'BG_PRIMARY': '#ffffff',   # Fondo principal
        'BG_SECONDARY': '#f8f9fa', # Fondo secundario
        'BG_DARK': '#343a40',      # Fondo oscuro
        'BG_SIDEBAR': '#2c3e50',   # Fondo sidebar
        
        # Colores de texto
        'TEXT_PRIMARY': '#2c3e50',   # Texto principal
        'TEXT_SECONDARY': '#6c757d', # Texto secundario
        'TEXT_LIGHT': '#ffffff',     # Texto claro
        'TEXT_MUTED': '#868e96'      # Texto apagado
    }
    
    # Directorios del sistema
    DIRECTORIES = {
        'CONFIG': 'config',
        'DATABASE': 'database',
        'MODELS': 'models',
        'VIEWS': 'views', 
        'CONTROLLERS': 'controllers',
        'UTILS': 'utils',
        'ASSETS': 'assets',
        'LOGS': 'logs',
        'BACKUPS': 'backups',
        'TEMP': 'temp',
        'REPORTS': 'reportes',
        'IMAGES': 'imagenes',
        'ICONS': 'assets/icons',
        'THEMES': 'assets/themes'
    }
    
    # Configuración de archivos
    FILES = {
        'APP_CONFIG': 'config/app_config.json',
        'USER_PREFERENCES': 'config/user_preferences.json',
        'PERMISSIONS_CONFIG': 'config/permissions.json',
        'THEMES_CONFIG': 'config/themes.json'
    }
    
    # Configuración de negocio
    BUSINESS = {
        'DEFAULT_CURRENCY': 'PEN',
        'DEFAULT_CURRENCY_SYMBOL': 'S/.',
        'DEFAULT_TAX_RATE': 18.0,
        'DECIMAL_PLACES': 2,
        'ROUNDING_METHOD': 'ROUND_HALF_UP',
        'DATE_FORMAT': '%d/%m/%Y',
        'TIME_FORMAT': '%H:%M:%S',
        'DATETIME_FORMAT': '%d/%m/%Y %H:%M:%S'
    }
    
    # Configuración de módulos
    MODULES = {
        'VENTAS': {
            'enabled': True,
            'icon': 'shopping-cart',
            'color': '#27ae60',
            'permissions': ['ventas_ver', 'ventas_crear', 'ventas_editar']
        },
        'INVENTARIO': {
            'enabled': True,
            'icon': 'boxes',
            'color': '#3498db',
            'permissions': ['inventario_ver', 'inventario_crear', 'inventario_editar']
        },
        'CLIENTES': {
            'enabled': True,
            'icon': 'users',
            'color': '#9b59b6',
            'permissions': ['clientes_ver', 'clientes_crear', 'clientes_editar']
        },
        'REPORTES': {
            'enabled': True,
            'icon': 'chart-bar',
            'color': '#e67e22',
            'permissions': ['reportes_ver', 'reportes_generar']
        },
        'USUARIOS': {
            'enabled': True,
            'icon': 'user-cog',
            'color': '#e74c3c',
            'permissions': ['usuarios_ver', 'usuarios_crear', 'usuarios_editar', 'usuarios_eliminar']
        },
        'CONFIGURACION': {
            'enabled': True,
            'icon': 'cogs',
            'color': '#95a5a6',
            'permissions': ['config_ver', 'config_editar']
        }
    }
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Crear todos los directorios necesarios del sistema"""
        created_dirs = []
        
        for dir_name, dir_path in cls.DIRECTORIES.items():
            try:
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path, exist_ok=True)
                    created_dirs.append(dir_path)
                    
            except Exception as e:
                print(f"❌ Error creando directorio {dir_path}: {e}")
        
        if created_dirs:
            print(f"✅ Directorios creados: {', '.join(created_dirs)}")
        else:
            print("✅ Todos los directorios ya existen")
    
    @classmethod
    def load_app_config(cls) -> Dict[str, Any]:
        """Cargar configuración principal de la aplicación"""
        config_file = cls.FILES['APP_CONFIG']
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Crear configuración por defecto
                default_config = cls._get_default_app_config()
                cls.save_app_config(default_config)
                return default_config
                
        except Exception as e:
            print(f"Error cargando configuración de app: {e}")
            return cls._get_default_app_config()
    
    @classmethod
    def _get_default_app_config(cls) -> Dict[str, Any]:
        """Obtener configuración por defecto de la aplicación"""
        return {
            'app_info': cls.APP_INFO,
            'window': {
                'width': cls.UI['WINDOW_WIDTH'],
                'height': cls.UI['WINDOW_HEIGHT'],
                'state': cls.UI['WINDOW_STATE'],
                'center': True,
                'resizable': True,
                'min_width': cls.UI['MIN_WIDTH'],
                'min_height': cls.UI['MIN_HEIGHT']
            },
            'theme': {
                'name': cls.UI['THEME_DEFAULT'],
                'colors': cls.COLORS,
                'fonts': {
                    'default': cls.UI['FONT_DEFAULT'],
                    'title': cls.UI['FONT_TITLE'],
                    'subtitle': cls.UI['FONT_SUBTITLE'],
                    'small': cls.UI['FONT_SMALL']
                },
                'animations': cls.UI['ENABLE_ANIMATIONS'],
                'tooltips': cls.UI['SHOW_TOOLTIPS']
            },
            'business': cls.BUSINESS,
            'security': cls.SECURITY,
            'modules': cls.MODULES,
            'database': cls.DATABASE,
            'created_at': datetime.now().isoformat(),
            'version': cls.APP_INFO['VERSION']
        }
    
    @classmethod
    def save_app_config(cls, config: Dict[str, Any]) -> bool:
        """Guardar configuración de la aplicación"""
        try:
            config_file = cls.FILES['APP_CONFIG']
            os.makedirs(os.path.dirname(config_file), exist_ok=True)
            
            # Actualizar timestamp de modificación
            config.update({
                'updated_at': datetime.now().isoformat(),
                'version': cls.APP_INFO['VERSION']
            })
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error guardando configuración de app: {e}")
            return False
    
    @classmethod
    def get_color(cls, color_name: str) -> str:
        """Obtener color del sistema por nombre"""
        return cls.COLORS.get(color_name.upper(), cls.COLORS['PRIMARY'])
    
    @classmethod
    def get_directory(cls, dir_name: str) -> str:
        """Obtener directorio del sistema por nombre"""
        return cls.DIRECTORIES.get(dir_name.upper(), 'temp')
    
    @classmethod
    def get_module_config(cls, module_name: str) -> Dict[str, Any]:
        """Obtener configuración de un módulo específico"""
        return cls.MODULES.get(module_name.upper(), {})
    
    @classmethod
    def is_module_enabled(cls, module_name: str) -> bool:
        """Verificar si un módulo está habilitado"""
        module_config = cls.get_module_config(module_name)
        return module_config.get('enabled', False)
    
    @classmethod
    def get_enabled_modules(cls) -> Dict[str, Dict[str, Any]]:
        """Obtener todos los módulos habilitados"""
        return {
            name: config for name, config in cls.MODULES.items()
            if config.get('enabled', False)
        }
    
    @classmethod
    def update_module_status(cls, module_name: str, enabled: bool) -> bool:
        """Actualizar estado de un módulo"""
        try:
            if module_name.upper() in cls.MODULES:
                cls.MODULES[module_name.upper()]['enabled'] = enabled
                
                # Guardar cambios en configuración
                config = cls.load_app_config()
                config['modules'] = cls.MODULES
                return cls.save_app_config(config)
            
            return False
            
        except Exception as e:
            print(f"Error actualizando módulo {module_name}: {e}")
            return False
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validar configuración del sistema"""
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'info': []
        }
        
        # Validar directorios
        for dir_name, dir_path in cls.DIRECTORIES.items():
            if not os.path.exists(dir_path):
                validation_result['warnings'].append(f"Directorio faltante: {dir_path}")
        
        # Validar archivos de configuración
        for file_name, file_path in cls.FILES.items():
            if not os.path.exists(file_path):
                validation_result['info'].append(f"Archivo de configuración faltante: {file_path}")
        
        # Validar configuración de negocio
        if cls.BUSINESS['DEFAULT_TAX_RATE'] < 0 or cls.BUSINESS['DEFAULT_TAX_RATE'] > 100:
            validation_result['errors'].append("Tasa de impuestos inválida")
            validation_result['valid'] = False
        
        if cls.BUSINESS['DECIMAL_PLACES'] < 0 or cls.BUSINESS['DECIMAL_PLACES'] > 4:
            validation_result['warnings'].append("Número de decimales inusual")
        
        # Validar seguridad
        if cls.SECURITY['PASSWORD_MIN_LENGTH'] < 4:
            validation_result['warnings'].append("Longitud mínima de contraseña muy baja")
        
        if cls.SECURITY['SESSION_TIMEOUT'] < 300:  # 5 minutos
            validation_result['warnings'].append("Timeout de sesión muy corto")
        
        return validation_result
    
    @classmethod
    def print_system_info(cls) -> None:
        """Imprimir información del sistema"""
        print("🏪 INFORMACIÓN DEL SISTEMA POS")
        print("=" * 50)
        print(f"📱 Nombre: {cls.APP_INFO['NAME']}")
        print(f"🔢 Versión: {cls.APP_INFO['VERSION']}")
        print(f"👨‍💻 Desarrollador: {cls.APP_INFO['DEVELOPER']}")
        print(f"📅 Copyright: {cls.APP_INFO['COPYRIGHT']}")
        print()
        
        # Módulos habilitados
        enabled_modules = cls.get_enabled_modules()
        print(f"🧩 Módulos habilitados ({len(enabled_modules)}):")
        for module_name, module_config in enabled_modules.items():
            icon = module_config.get('icon', '📦')
            color = module_config.get('color', '#000000')
            print(f"   {icon} {module_name.title()}")
        print()
        
        # Validación
        validation = cls.validate_config()
        if validation['valid']:
            print("✅ Configuración del sistema válida")
        else:
            print("❌ Errores en la configuración:")
            for error in validation['errors']:
                print(f"   • {error}")
        
        if validation['warnings']:
            print("⚠️  Advertencias:")
            for warning in validation['warnings']:
                print(f"   • {warning}")

# Función de conveniencia para obtener configuraciones
def get_app_config() -> Dict[str, Any]:
    """Función rápida para obtener configuración de la app"""
    return SystemSettings.load_app_config()

def get_color(color_name: str) -> str:
    """Función rápida para obtener un color"""
    return SystemSettings.get_color(color_name)

def get_directory(dir_name: str) -> str:
    """Función rápida para obtener un directorio"""
    return SystemSettings.get_directory(dir_name)

if __name__ == "__main__":
    # Crear directorios y mostrar información
    SystemSettings.ensure_directories()
    SystemSettings.print_system_info()
