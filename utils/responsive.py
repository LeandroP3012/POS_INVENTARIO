"""
Sistema de Escalado Responsivo para el Sistema POS
Detecta la resolución de pantalla y ajusta automáticamente los tamaños
"""

import tkinter as tk
from typing import Dict, Tuple, Optional, Callable
import logging
import json
import os


class ResponsiveScaler:
    """
    Clase para manejar escalado responsivo basado en resolución de pantalla
    
    Resoluciones de referencia:
    - Base: 1920x1080 (Full HD) - Factor 1.0
    - HD: 1366x768 - Factor 0.71
    - WXGA: 1280x720 - Factor 0.67
    - HD+: 1600x900 - Factor 0.83
    - 2K: 2560x1440 - Factor 1.33
    """
    
    # Resolución base de diseño (Full HD)
    BASE_WIDTH = 1920
    BASE_HEIGHT = 1080
    
    # Tamaños mínimos para evitar elementos muy pequeños
    MIN_FONT_SIZE = 8
    MIN_PADDING = 5
    MIN_BUTTON_HEIGHT = 30
    MIN_WIDGET_HEIGHT = 25
    
    def __init__(self, root_window: tk.Tk = None):
        """
        Inicializar el scaler
        
        Args:
            root_window: Ventana raíz de Tkinter (opcional, si no se pasa crea una temporal)
        """
        self.logger = logging.getLogger('utils.ResponsiveScaler')
        
        # Callbacks para notificar cambios
        self.on_config_change_callbacks = []
        
        # Cargar configuración personalizada si existe
        self.custom_config = self.load_custom_config()
        
        # Obtener resolución de pantalla
        if root_window:
            self.screen_width = root_window.winfo_screenwidth()
            self.screen_height = root_window.winfo_screenheight()
        else:
            # Crear ventana temporal para obtener resolución
            temp_root = tk.Tk()
            temp_root.withdraw()
            self.screen_width = temp_root.winfo_screenwidth()
            self.screen_height = temp_root.winfo_screenheight()
            temp_root.destroy()
        
        # Calcular factores de escala
        self.scale_factor_x = self.screen_width / self.BASE_WIDTH
        self.scale_factor_y = self.screen_height / self.BASE_HEIGHT
        self.scale_factor = min(self.scale_factor_x, self.scale_factor_y)
        
        # Detectar categoría de resolución
        self.resolution_category = self._detect_resolution_category()
        
        self.logger.info(f"Resolución detectada: {self.screen_width}x{self.screen_height}")
        self.logger.info(f"Factor de escala: {self.scale_factor:.2f} ({self.resolution_category})")
    
    def _detect_resolution_category(self) -> str:
        """Detectar categoría de resolución"""
        total_pixels = self.screen_width * self.screen_height
        
        if total_pixels >= 3686400:  # 2560x1440 o superior
            return "2K+"
        elif total_pixels >= 2073600:  # 1920x1080
            return "Full HD"
        elif total_pixels >= 1440000:  # 1600x900
            return "HD+"
        elif total_pixels >= 1049088:  # 1366x768
            return "HD"
        else:
            return "Low Resolution"
    
    def scale(self, value: float) -> int:
        """
        Escalar un valor según la resolución
        
        Args:
            value: Valor base (diseñado para 1920x1080)
            
        Returns:
            Valor escalado redondeado
        """
        scaled = int(value * self.scale_factor)
        return max(scaled, 1)  # Mínimo 1 pixel
    
    def scale_font(self, base_size: int) -> int:
        """
        Escalar tamaño de fuente
        
        Args:
            base_size: Tamaño base de fuente
            
        Returns:
            Tamaño escalado con límite mínimo
        """
        scaled = int(base_size * self.scale_factor)
        return max(scaled, self.MIN_FONT_SIZE)
    
    def scale_padding(self, base_padding: int) -> int:
        """
        Escalar padding/espaciado
        
        Args:
            base_padding: Padding base
            
        Returns:
            Padding escalado con límite mínimo
        """
        scaled = int(base_padding * self.scale_factor)
        return max(scaled, self.MIN_PADDING)
    
    def scale_width(self, base_width: int) -> int:
        """Escalar ancho usando factor X"""
        scaled = int(base_width * self.scale_factor_x)
        return max(scaled, 10)
    
    def scale_height(self, base_height: int) -> int:
        """Escalar altura usando factor Y"""
        scaled = int(base_height * self.scale_factor_y)
        return max(scaled, 10)
    
    def scale_button_padding(self, base_x: int, base_y: int) -> Tuple[int, int]:
        """
        Escalar padding de botón
        
        Args:
            base_x: Padding horizontal base
            base_y: Padding vertical base
            
        Returns:
            Tupla (padding_x, padding_y) escalados
        """
        scaled_x = max(int(base_x * self.scale_factor), self.MIN_PADDING)
        scaled_y = max(int(base_y * self.scale_factor), self.MIN_PADDING)
        return (scaled_x, scaled_y)
    
    def get_window_size(self, base_width: int, base_height: int, 
                       min_width: int = None, min_height: int = None) -> Tuple[int, int]:
        """
        Obtener tamaño de ventana escalado
        
        Args:
            base_width: Ancho base
            base_height: Alto base
            min_width: Ancho mínimo (opcional)
            min_height: Alto mínimo (opcional)
            
        Returns:
            Tupla (width, height) escalados
        """
        width = self.scale_width(base_width)
        height = self.scale_height(base_height)
        
        if min_width:
            width = max(width, min_width)
        if min_height:
            height = max(height, min_height)
        
        # No exceder el tamaño de pantalla (dejar margen del 10%)
        max_width = int(self.screen_width * 0.9)
        max_height = int(self.screen_height * 0.9)
        
        width = min(width, max_width)
        height = min(height, max_height)
        
        return (width, height)
    
    def get_responsive_fonts(self) -> Dict[str, Tuple[str, int, str]]:
        """
        Obtener configuración de fuentes responsivas
        
        Returns:
            Diccionario con configuraciones de fuentes
        """
        return {
            'title': ('Segoe UI', self.scale_font(16), 'bold'),
            'subtitle': ('Segoe UI', self.scale_font(12), 'bold'),
            'heading': ('Segoe UI', self.scale_font(14), 'bold'),
            'default': ('Segoe UI', self.scale_font(10), 'normal'),
            'button': ('Segoe UI', self.scale_font(10), 'normal'),
            'small': ('Segoe UI', self.scale_font(8), 'normal'),
            'large': ('Segoe UI', self.scale_font(14), 'normal'),
            'xlarge': ('Segoe UI', self.scale_font(18), 'bold'),
        }
    
    def get_responsive_sizes(self) -> Dict[str, int]:
        """
        Obtener tamaños responsivos comunes
        
        Returns:
            Diccionario con tamaños escalados
        """
        return {
            # Padding
            'padding_xs': self.scale_padding(5),
            'padding_sm': self.scale_padding(10),
            'padding_md': self.scale_padding(15),
            'padding_lg': self.scale_padding(20),
            'padding_xl': self.scale_padding(30),
            
            # Márgenes
            'margin_xs': self.scale_padding(5),
            'margin_sm': self.scale_padding(10),
            'margin_md': self.scale_padding(15),
            'margin_lg': self.scale_padding(20),
            
            # Widgets
            'entry_height': max(self.scale(35), self.MIN_WIDGET_HEIGHT),
            'button_height': max(self.scale(40), self.MIN_BUTTON_HEIGHT),
            'combobox_height': max(self.scale(35), self.MIN_WIDGET_HEIGHT),
            
            # Iconos
            'icon_sm': self.scale(16),
            'icon_md': self.scale(24),
            'icon_lg': self.scale(32),
            'icon_xl': self.scale(48),
            
            # Bordes
            'border_width': max(self.scale(1), 1),
            'border_radius': self.scale(5),
            
            # Scrollbar
            'scrollbar_width': max(self.scale(15), 10),
        }
    
    def get_button_config(self, size: str = 'default') -> Dict:
        """
        Obtener configuración de botón según tamaño
        
        Args:
            size: 'small', 'default', 'large'
            
        Returns:
            Diccionario con configuración de botón
        """
        configs = {
            'small': {
                'padding': self.scale_button_padding(10, 5),
                'font_size': self.scale_font(9),
            },
            'default': {
                'padding': self.scale_button_padding(20, 10),
                'font_size': self.scale_font(10),
            },
            'large': {
                'padding': self.scale_button_padding(30, 15),
                'font_size': self.scale_font(12),
            }
        }
        return configs.get(size, configs['default'])
    
    def adjust_treeview_columns(self, base_widths: Dict[str, int]) -> Dict[str, int]:
        """
        Ajustar anchos de columnas de Treeview
        
        Args:
            base_widths: Diccionario con anchos base {columna: ancho}
            
        Returns:
            Diccionario con anchos escalados
        """
        return {col: self.scale_width(width) for col, width in base_widths.items()}
    
    def get_listbox_height(self, base_height: int) -> int:
        """
        Calcular altura de Listbox en líneas según resolución
        
        Args:
            base_height: Altura base en líneas (para 1920x1080)
            
        Returns:
            Altura ajustada en líneas
        """
        scaled = int(base_height * self.scale_factor)
        return max(scaled, 5)  # Mínimo 5 líneas
    
    def should_use_compact_layout(self) -> bool:
        """
        Determinar si se debe usar layout compacto
        
        Returns:
            True si la resolución es baja y requiere layout compacto
        """
        return self.resolution_category in ["HD", "Low Resolution"]
    
    def get_info(self) -> Dict:
        """
        Obtener información del scaler
        
        Returns:
            Diccionario con información de configuración
        """
        return {
            'screen_resolution': f"{self.screen_width}x{self.screen_height}",
            'resolution_category': self.resolution_category,
            'scale_factor': round(self.scale_factor, 2),
            'scale_factor_x': round(self.scale_factor_x, 2),
            'scale_factor_y': round(self.scale_factor_y, 2),
            'compact_layout': self.should_use_compact_layout(),
        }
    
    def print_info(self):
        """Imprimir información de configuración"""
        info = self.get_info()
        print("\n" + "="*60)
        print("🖥️  CONFIGURACIÓN DE ESCALADO RESPONSIVO")
        print("="*60)
        print(f"Resolución de pantalla: {info['screen_resolution']}")
        print(f"Categoría: {info['resolution_category']}")
        print(f"Factor de escala: {info['scale_factor']}")
        print(f"Factor X: {info['scale_factor_x']}")
        print(f"Factor Y: {info['scale_factor_y']}")
        print(f"Layout compacto: {'Sí' if info['compact_layout'] else 'No'}")
        print("="*60 + "\n")
    
    def load_custom_config(self) -> Optional[Dict]:
        """
        Cargar configuración personalizada desde archivo JSON
        
        Returns:
            Diccionario con configuración o None si no existe
        """
        config_path = os.path.join('config', 'responsive_config.json')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.logger.info("Configuración personalizada cargada")
                return config
            except Exception as e:
                self.logger.warning(f"Error al cargar configuración personalizada: {e}")
        return None
    
    def reload_config(self):
        """Recargar configuración desde archivo y notificar cambios"""
        self.custom_config = self.load_custom_config()
        self.logger.info("Configuración recargada")
        
        # Notificar a todos los listeners
        for callback in self.on_config_change_callbacks:
            try:
                callback()
            except Exception as e:
                self.logger.error(f"Error en callback de cambio de configuración: {e}")
    
    def register_on_change(self, callback: Callable):
        """
        Registrar callback para notificaciones de cambio de configuración
        
        Args:
            callback: Función a llamar cuando cambie la configuración
        """
        if callback not in self.on_config_change_callbacks:
            self.on_config_change_callbacks.append(callback)
    
    def unregister_on_change(self, callback: Callable):
        """
        Eliminar callback de notificaciones
        
        Args:
            callback: Función a eliminar
        """
        if callback in self.on_config_change_callbacks:
            self.on_config_change_callbacks.remove(callback)
    
    def get_base_size(self, key: str, default: int) -> int:
        """
        Obtener tamaño base desde configuración personalizada o valor por defecto
        
        Args:
            key: Clave del tamaño (ej: 'title_font', 'padding_lg')
            default: Valor por defecto si no hay configuración
            
        Returns:
            Valor del tamaño base
        """
        if self.custom_config and 'base_sizes' in self.custom_config:
            return self.custom_config['base_sizes'].get(key, default)
        return default
    
    def get_min_limit(self, key: str, default: int) -> int:
        """
        Obtener límite mínimo desde configuración personalizada
        
        Args:
            key: Clave del límite (ej: 'font_size', 'padding')
            default: Valor por defecto
            
        Returns:
            Valor del límite mínimo
        """
        if self.custom_config and 'min_limits' in self.custom_config:
            return self.custom_config['min_limits'].get(key, default)
        return default


# Instancia global singleton
_global_scaler = None


def get_scaler(root_window: tk.Tk = None) -> ResponsiveScaler:
    """
    Obtener instancia global del scaler (patrón Singleton)
    
    Args:
        root_window: Ventana raíz (solo necesaria en primera llamada)
        
    Returns:
        Instancia de ResponsiveScaler
    """
    global _global_scaler
    if _global_scaler is None:
        _global_scaler = ResponsiveScaler(root_window)
    return _global_scaler


def reset_scaler():
    """Resetear el scaler global (útil para testing)"""
    global _global_scaler
    _global_scaler = None


def reload_config():
    """Recargar configuración global"""
    global _global_scaler
    if _global_scaler:
        _global_scaler.reload_config()
