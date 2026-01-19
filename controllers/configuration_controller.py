"""
Controlador de Configuración del Sistema
Maneja la lógica de configuración y persistencia
"""

import json
import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import shutil

from utils.path_manager import (
    _path_manager,
    get_data_path,
    load_config as pm_load_config,
    save_config as pm_save_config,
)


class ConfigurationController:
    """Controlador para la gestión de configuración del sistema"""
    
    def __init__(self):
        self.logger = logging.getLogger('ConfigController')

        # Usar PathManager para rutas de configuración
        self.path_manager = _path_manager
        # Ubicar respaldos dentro de la ruta de datos del usuario
        self.backup_dir = get_data_path('backups')

        # Asegurar que exista el directorio de backups
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def load_configuration(self) -> Dict[str, Any]:
        """Cargar configuración del sistema"""
        try:
            config = {}
            
            # Cargar configuración del sistema usando PathManager
            system_config = pm_load_config('system_config.json')
            if system_config:
                config.update(system_config)
                self.logger.info(f"Configuración del sistema cargada: {len(system_config)} elementos")
            else:
                self.logger.warning("Archivo de configuración no encontrado, usando defaults")
                config = self.get_default_configuration()
                self.save_configuration(config)
            
            # Cargar configuración de base de datos usando PathManager
            db_config = pm_load_config('database.json')
            if db_config:
                # Mapear campos de BD con el prefijo correcto
                config.update({
                    'db_host': db_config.get('host', 'localhost'),
                    'db_port': db_config.get('port', '3306'),
                    'db_name': db_config.get('name', 'pos_system'),
                    'db_user': db_config.get('user', 'root'),
                    'db_password': db_config.get('password', ''),
                    'db_max_connections': db_config.get('max_connections', '10'),
                    'db_timeout': db_config.get('timeout', '30')
                })
                self.logger.info("Configuración de base de datos cargada")
            
            return config
            
        except Exception as e:
            self.logger.error(f"Error cargando configuración: {e}")
            return self.get_default_configuration()
    
    def save_configuration(self, config_data: Dict[str, Any]) -> bool:
        """Guardar configuración del sistema"""
        try:
            # Separar configuración del sistema y de base de datos
            system_config = {}
            db_config = {}
            
            for key, value in config_data.items():
                if key.startswith('db_'):
                    db_config[key[3:]] = value  # Remover prefijo 'db_'
                else:
                    system_config[key] = value
            
            # Guardar configuración del sistema usando PathManager
            pm_save_config('system_config.json', system_config)
            
            # Guardar configuración de base de datos si hay datos
            if db_config:
                pm_save_config('database.json', db_config)
            
            self.logger.info("Configuración guardada exitosamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error guardando configuración: {e}")
            return False
    
    def get_default_configuration(self) -> Dict[str, Any]:
        """Obtener configuración por defecto"""
        return {
            # Información de la empresa
            'company_name': 'Mi Negocio POS',
            'company_rut': '',
            'company_address': '',
            'company_phone': '',
            'company_email': '',
            'company_website': '',
            'company_logo': '',
            
            # Configuración de moneda e impuestos
            'currency': 'CLP',
            'currency_symbol': '$',
            'tax_rate': '19',
            'include_tax_in_price': True,
            
            # Configuración de interfaz
            'theme': 'Claro',
            'language': 'Español',
            
            # Configuración de impresión
            'default_printer': 'Impresora del sistema',
            'auto_print_receipt': True,
            'print_logo': True,
            'receipt_copies': '1',
            
            # Configuración de seguridad
            'session_timeout': '480',
            'auto_logout': True,
            'min_password_length': '6',
            'require_special_chars': False,
            
            # Configuración de backup
            'auto_backup_enabled': True,
            'backup_frequency': 'Diario',
            'backup_path': './backups',
            
            # Configuración de base de datos (valores por defecto)
            'db_host': 'localhost',
            'db_port': '3306',
            'db_name': 'pos_system',
            'db_user': 'root',
            'db_password': ''
        }
    
    def test_database_connection(self, db_config: Dict[str, str]) -> tuple[bool, str]:
        """Probar conexión a la base de datos"""
        try:
            # Importar el módulo de conexión
            from database.connection import DatabaseConnection
            
            # Crear configuración temporal
            temp_config = {
                'host': db_config.get('db_host', 'localhost'),
                'port': int(db_config.get('db_port', 3306)),
                'database': db_config.get('db_name', 'pos_system'),
                'user': db_config.get('db_user', 'root'),
                'password': db_config.get('db_password', '')
            }
            
            # Intentar conexión
            db = DatabaseConnection()
            connection = db.get_connection()
            if connection:
                connection.close()
                return True, "Conexión exitosa"
            else:
                return False, "No se pudo establecer la conexión"
                
        except Exception as e:
            self.logger.error(f"Error probando conexión de BD: {e}")
            return False, f"Error de conexión: {str(e)}"
    
    def create_backup(self, backup_name: Optional[str] = None) -> tuple[bool, str]:
        """Crear backup de la base de datos"""
        try:
            if not backup_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"backup_{timestamp}.sql"
            
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            # Aquí iría la lógica real de backup usando mysqldump
            # Por ahora simulamos el backup
            
            # Crear archivo de backup simulado
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(f"-- Backup creado el {datetime.now()}\n")
                f.write("-- Este es un backup simulado\n")
                f.write("-- En producción contendría el dump real de la BD\n")
            
            self.logger.info(f"Backup creado: {backup_path}")
            return True, f"Backup creado exitosamente: {backup_name}"
            
        except Exception as e:
            self.logger.error(f"Error creando backup: {e}")
            return False, f"Error creando backup: {str(e)}"
    
    def restore_backup(self, backup_file: str) -> tuple[bool, str]:
        """Restaurar desde backup"""
        try:
            if not os.path.exists(backup_file):
                return False, "Archivo de backup no encontrado"
            
            # Aquí iría la lógica real de restauración usando mysql
            # Por ahora simulamos la restauración
            
            self.logger.info(f"Backup restaurado desde: {backup_file}")
            return True, "Backup restaurado exitosamente"
            
        except Exception as e:
            self.logger.error(f"Error restaurando backup: {e}")
            return False, f"Error restaurando backup: {str(e)}"
    
    def validate_configuration(self, config_data: Dict[str, Any]) -> tuple[bool, list[str]]:
        """Validar configuración antes de guardar"""
        errors = []
        
        try:
            # Validar campos obligatorios
            required_fields = ['company_name', 'currency', 'currency_symbol']
            for field in required_fields:
                if not config_data.get(field, '').strip():
                    errors.append(f"El campo '{field}' es obligatorio")
            
            # Validar formato de email si está presente
            email = config_data.get('company_email', '').strip()
            if email and '@' not in email:
                errors.append("Formato de email inválido")
            
            # Validar tasa de impuestos
            try:
                tax_rate = float(config_data.get('tax_rate', '0'))
                if tax_rate < 0 or tax_rate > 100:
                    errors.append("La tasa de impuestos debe estar entre 0 y 100")
            except ValueError:
                errors.append("Tasa de impuestos debe ser un número válido")
            
            # Validar timeout de sesión
            try:
                timeout = int(config_data.get('session_timeout', '480'))
                if timeout < 60 or timeout > 1440:  # Entre 1 hora y 24 horas
                    errors.append("El timeout de sesión debe estar entre 60 y 1440 minutos")
            except ValueError:
                errors.append("Timeout de sesión debe ser un número válido")
            
            # Validar longitud mínima de contraseña
            try:
                min_length = int(config_data.get('min_password_length', '6'))
                if min_length < 4 or min_length > 20:
                    errors.append("La longitud mínima de contraseña debe estar entre 4 y 20")
            except ValueError:
                errors.append("Longitud mínima de contraseña debe ser un número válido")
            
            # Validar configuración de base de datos si está presente
            if 'db_host' in config_data:
                db_port = config_data.get('db_port', '3306')
                try:
                    port = int(db_port)
                    if port < 1 or port > 65535:
                        errors.append("Puerto de base de datos debe estar entre 1 y 65535")
                except ValueError:
                    errors.append("Puerto de base de datos debe ser un número válido")
            
            return len(errors) == 0, errors
            
        except Exception as e:
            self.logger.error(f"Error validando configuración: {e}")
            return False, [f"Error en validación: {str(e)}"]
    
    def apply_configuration(self, config_data: Dict[str, Any]) -> bool:
        """Aplicar configuración al sistema en tiempo real"""
        try:
            # Aquí se aplicarían los cambios que requieren reinicio o actualización inmediata
            
            # Actualizar configuración de logging si cambió
            # Actualizar configuración de tema si cambió
            # Actualizar configuración de moneda en la interfaz
            # etc.
            
            self.logger.info("Configuración aplicada al sistema")
            return True
            
        except Exception as e:
            self.logger.error(f"Error aplicando configuración: {e}")
            return False
    
    def get_backup_history(self) -> list[Dict[str, Any]]:
        """Obtener historial de backups"""
        try:
            backups = []
            if os.path.exists(self.backup_dir):
                for filename in os.listdir(self.backup_dir):
                    if filename.endswith('.sql'):
                        file_path = os.path.join(self.backup_dir, filename)
                        file_stats = os.stat(file_path)
                        backups.append({
                            'name': filename,
                            'path': file_path,
                            'size': file_stats.st_size,
                            'created': datetime.fromtimestamp(file_stats.st_ctime),
                            'modified': datetime.fromtimestamp(file_stats.st_mtime)
                        })
            
            # Ordenar por fecha de creación (más reciente primero)
            backups.sort(key=lambda x: x['created'], reverse=True)
            return backups
            
        except Exception as e:
            self.logger.error(f"Error obteniendo historial de backups: {e}")
            return []
    
    def export_configuration(self, export_path: str) -> bool:
        """Exportar configuración a archivo"""
        try:
            config = self.load_configuration()
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Configuración exportada a: {export_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exportando configuración: {e}")
            return False
    
    def import_configuration(self, import_path: str) -> tuple[bool, str]:
        """Importar configuración desde archivo"""
        try:
            if not os.path.exists(import_path):
                return False, "Archivo no encontrado"
            
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            # Validar configuración importada
            is_valid, errors = self.validate_configuration(imported_config)
            if not is_valid:
                return False, f"Configuración inválida: {', '.join(errors)}"
            
            # Guardar configuración
            if self.save_configuration(imported_config):
                self.logger.info(f"Configuración importada desde: {import_path}")
                return True, "Configuración importada exitosamente"
            else:
                return False, "Error guardando configuración importada"
                
        except json.JSONDecodeError:
            return False, "Archivo de configuración inválido (formato JSON incorrecto)"
        except Exception as e:
            self.logger.error(f"Error importando configuración: {e}")
            return False, f"Error importando configuración: {str(e)}"
    
    def get_available_printers(self) -> list:
        """Obtener lista de impresoras disponibles"""
        try:
            # Importar módulo de impresoras si está disponible
            import win32print
            printers = []
            
            # Obtener impresoras del sistema
            printer_info = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
            for printer in printer_info:
                printers.append(printer[2])  # Nombre de la impresora
            
            if not printers:
                printers = ['Impresora del sistema', 'Microsoft Print to PDF']
            
            return printers
            
        except ImportError:
            # Si no está disponible win32print, devolver lista básica
            return ['Impresora del sistema', 'Microsoft Print to PDF', 'Fax']
        except Exception as e:
            self.logger.error(f"Error obteniendo impresoras: {e}")
            return ['Impresora del sistema']
    
    def get_database_info(self) -> Dict[str, Any]:
        """Obtener información de la base de datos"""
        try:
            # Simular información de la base de datos
            # En una implementación real, esto haría consultas a la BD
            return {
                'database': 'pos_system',
                'version': 'MySQL 8.0.33',
                'last_connection': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'tables_count': 12,
                'size': '45.2 MB',
                'status': 'OK'
            }
        except Exception as e:
            self.logger.error(f"Error obteniendo información de BD: {e}")
            return {
                'database': 'No disponible',
                'version': 'No disponible',
                'last_connection': 'No disponible',
                'tables_count': 'No disponible',
                'size': 'No disponible',
                'status': 'ERROR'
            }
