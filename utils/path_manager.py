"""
Gestor de rutas para la aplicación
Maneja rutas correctamente tanto en desarrollo como en ejecutable compilado
"""

import os
import sys
import json
import shutil
from pathlib import Path
from typing import Optional

class PathManager:
    """Gestiona rutas de archivos y directorios de la aplicación"""
    
    def __init__(self):
        self._base_path = None
        self._is_frozen = getattr(sys, 'frozen', False)
        self._user_data_path = None
        
    @property
    def is_frozen(self) -> bool:
        """Verifica si la aplicación está ejecutándose como ejecutable compilado"""
        return self._is_frozen
    
    @property
    def base_path(self) -> Path:
        """Obtiene la ruta base de la aplicación"""
        if self._base_path is None:
            if self.is_frozen:
                # Ejecutable compilado con PyInstaller
                self._base_path = Path(sys.executable).parent
            else:
                # Ejecutándose como script Python
                self._base_path = Path(__file__).parent.parent
        
        return self._base_path
    
    @property
    def user_data_path(self) -> Path:
        """Obtiene la ruta de datos del usuario (para archivos editables)"""
        if self._user_data_path is None:
            if self.is_frozen:
                # En ejecutable: usar carpeta en AppData o junto al ejecutable
                # Opción 1: AppData (recomendado para instalaciones en Program Files)
                app_data = os.getenv('APPDATA') or os.getenv('LOCALAPPDATA')
                if app_data:
                    self._user_data_path = Path(app_data) / 'SistemaPOS'
                else:
                    # Fallback: junto al ejecutable
                    self._user_data_path = self.base_path / 'data'
            else:
                # En desarrollo: usar la carpeta del proyecto
                self._user_data_path = self.base_path
        
        # Crear directorio si no existe
        self._user_data_path.mkdir(parents=True, exist_ok=True)
        return self._user_data_path
    
    def get_resource_path(self, relative_path: str) -> Path:
        """
        Obtiene la ruta a un recurso empaquetado (solo lectura)
        Úsalo para: imágenes, iconos, plantillas, etc.
        """
        if self.is_frozen:
            # PyInstaller crea una carpeta temporal _MEIPASS
            base = getattr(sys, '_MEIPASS', self.base_path)
            return Path(base) / relative_path
        else:
            return self.base_path / relative_path
    
    def get_config_path(self, config_file: str) -> Path:
        """
        Obtiene la ruta a un archivo de configuración (editable)
        Úsalo para: database.json, system_config.json, etc.
        
        NOTA: Esta función solo retorna la ruta, NO crea ni copia archivos.
        Para crear archivos de configuración usar ensure_config_files()
        """
        config_path = self.user_data_path / 'config' / config_file
        
        # Crear directorio si no existe
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # NO copiar desde recursos - dejar que ensure_config_files() maneje la creación
        # Esto evita sobrescribir configuraciones editadas por el usuario
        
        return config_path
    
    def get_data_path(self, relative_path: str) -> Path:
        """
        Obtiene la ruta a un archivo de datos (editable)
        Úsalo para: logs, backups, reportes, etc.
        """
        data_path = self.user_data_path / relative_path
        data_path.parent.mkdir(parents=True, exist_ok=True)
        return data_path
    
    def ensure_config_files(self):
        """Asegura que existan todos los archivos de configuración necesarios"""
        config_files = [
            'database.json',
            'system_config.json',
            'ticket_config.json'
        ]
        
        for config_file in config_files:
            config_path = self.get_config_path(config_file)

            if not config_path.exists():
                # Priorizar plantilla personalizada si existe
                template_config = self._load_template_config(config_file)
                if template_config is not None:
                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump(template_config, f, indent=4, ensure_ascii=False)
                    print(f"✅ Configuración creada desde plantilla: {config_file}")
                    continue

                # Fallback: configuración por defecto embebida
                default_config = self._get_default_config(config_file)
                if default_config:
                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump(default_config, f, indent=4, ensure_ascii=False)
                    print(f"✅ Configuración creada: {config_file}")
    
    def _load_template_config(self, config_file: str) -> Optional[dict]:
        """Intenta cargar una plantilla de configuración desde config_templates"""
        try:
            template_path = self.get_resource_path(f'config_templates/{config_file}')
            if template_path.exists():
                with open(template_path, 'r', encoding='utf-8-sig') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️  Error cargando plantilla {config_file}: {e}")
        return None

    def _get_default_config(self, config_file: str) -> Optional[dict]:
        """Obtiene la configuración por defecto para un archivo"""
        defaults = {
            'database.json': {
                "host": "localhost",
                "port": "3306",
                "name": "pos_system",
                "user": "root",
                "password": "D3v3l0p3r@@$",
                "max_connections": "10",
                "timeout": "30"
            },
            'system_config.json': {
                "company_name": "Sistema POS",
                "company_rut": "",
                "company_address": "",
                "company_phone": "",
                "company_email": "",
                "company_website": "",
                "logo_path": "",
                "currency": "PEN",
                "currency_symbol": "S/.",
                "tax_rate": "18",
                "language": "Español",
                "theme": "Claro",
                "auto_print": True,
                "printer": "",
                "printer_mode": "auto",
                "force_thermal_print": False,
                "thermal_printer_keywords": [],
                "barcode_font_path": "",
                "copies": "1",
                "paper_size": "A4",
                "print_logo": True,
                "print_company_info": True,
                "print_customer_info": False,
                "print_barcode": False,
                "print_quality": "Normal",
                "save_pdf_copy": False,
                "session_timeout": "480",
                "auto_logout": True,
                "auto_backup": True,
                "backup_frequency": "Diario",
                "backup_path": "./backups",
                "auto_save": True,
                "include_tax": True,
                "tax_id": "",
                "min_password_length": "6",
                "require_special_chars": False,
                "show_animations": True,
                "sound_notifications": True
            },
            'ticket_config.json': {
                "printer_name": "",
                "paper_width": 80,
                "print_logo": False,
                "logo_path": "",
                "header_text": "TICKET DE VENTA",
                "footer_text": "¡Gracias por su compra!",
                "show_barcode": False
            }
        }
        
        return defaults.get(config_file)
    
    def load_json_config(self, config_file: str) -> dict:
        """Carga un archivo de configuración JSON"""
        try:
            config_path = self.get_config_path(config_file)
            
            if config_path.exists():
                # Soportar archivos creados con BOM (por ejemplo, desde Notepad o Set-Content)
                with open(config_path, 'r', encoding='utf-8-sig') as f:
                    return json.load(f)
            else:
                # Intentar crear desde plantilla
                template_config = self._load_template_config(config_file)
                if template_config is not None:
                    self.save_json_config(config_file, template_config)
                    return template_config

                # Fallback: retornar configuración por defecto interna
                default = self._get_default_config(config_file)
                if default:
                    self.save_json_config(config_file, default)
                return default or {}
                
        except Exception as e:
            print(f"❌ Error cargando configuración {config_file}: {e}")
            return self._get_default_config(config_file) or {}
    
    def save_json_config(self, config_file: str, data: dict) -> bool:
        """Guarda un archivo de configuración JSON"""
        try:
            config_path = self.get_config_path(config_file)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"❌ Error guardando configuración {config_file}: {e}")
            return False
    
    def get_log_path(self, log_file: str = 'app.log') -> Path:
        """Obtiene la ruta para archivos de log"""
        return self.get_data_path(f'logs/{log_file}')
    
    def get_backup_path(self, backup_file: str) -> Path:
        """Obtiene la ruta para archivos de backup"""
        return self.get_data_path(f'backups/{backup_file}')
    
    def get_report_path(self, report_file: str) -> Path:
        """Obtiene la ruta para archivos de reportes"""
        return self.get_data_path(f'reports/{report_file}')
    
    def get_ticket_path(self, ticket_file: str) -> Path:
        """Obtiene la ruta para archivos de tickets"""
        return self.get_data_path(f'tickets/{ticket_file}')
    
    def print_paths_info(self):
        """Imprime información sobre las rutas configuradas"""
        print("\n" + "=" * 60)
        print("INFORMACIÓN DE RUTAS DEL SISTEMA")
        print("=" * 60)
        print(f"Modo de ejecución: {'EJECUTABLE' if self.is_frozen else 'DESARROLLO'}")
        print(f"Ruta base: {self.base_path}")
        print(f"Ruta de datos del usuario: {self.user_data_path}")
        print(f"Configuraciones: {self.user_data_path / 'config'}")
        print(f"Logs: {self.user_data_path / 'logs'}")
        print(f"Backups: {self.user_data_path / 'backups'}")
        print(f"Reportes: {self.user_data_path / 'reports'}")
        print("=" * 60 + "\n")


# Instancia global del PathManager
_path_manager = PathManager()


# Funciones de conveniencia
def get_resource_path(relative_path: str) -> Path:
    """Obtiene la ruta a un recurso empaquetado"""
    return _path_manager.get_resource_path(relative_path)


def get_config_path(config_file: str) -> Path:
    """Obtiene la ruta a un archivo de configuración"""
    return _path_manager.get_config_path(config_file)


def get_data_path(relative_path: str) -> Path:
    """Obtiene la ruta a un archivo de datos"""
    return _path_manager.get_data_path(relative_path)


def load_config(config_file: str) -> dict:
    """Carga un archivo de configuración"""
    return _path_manager.load_json_config(config_file)


def save_config(config_file: str, data: dict) -> bool:
    """Guarda un archivo de configuración"""
    return _path_manager.save_json_config(config_file, data)


def ensure_config_files():
    """Asegura que existan todos los archivos de configuración"""
    _path_manager.ensure_config_files()


def is_frozen() -> bool:
    """Verifica si la aplicación está ejecutándose como ejecutable"""
    return _path_manager.is_frozen


if __name__ == "__main__":
    # Prueba del módulo
    _path_manager.print_paths_info()
    _path_manager.ensure_config_files()
    
    # Probar carga de configuración
    db_config = load_config('database.json')
    print(f"Configuración de base de datos: {db_config}")
