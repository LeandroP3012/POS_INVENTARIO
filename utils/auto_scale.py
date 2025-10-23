"""
Sistema de Auto-Ajuste Automático para el Sistema POS
Se ajusta automáticamente a cualquier resolución de pantalla sin configuración manual
"""

import tkinter as tk
from typing import Dict, Tuple
import logging


class AutoScaler:
    """
    Sistema de escalado automático que se ajusta a cualquier resolución
    """
    
    # Resolución base de diseño (Full HD)
    BASE_WIDTH = 1920
    BASE_HEIGHT = 1080
    
    # Tamaños mínimos y máximos
    MIN_FONT_SIZE = 8
    MAX_FONT_SIZE = 32
    MIN_PADDING = 5
    MAX_PADDING = 50
    
    def __init__(self, root_window: tk.Tk = None):
        """Inicializar el auto-scaler"""
        self.logger = logging.getLogger('utils.AutoScaler')
        
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
        self.scale_x = self.screen_width / self.BASE_WIDTH
        self.scale_y = self.screen_height / self.BASE_HEIGHT
        self.scale = min(self.scale_x, self.scale_y)  # Usar el menor para mantener proporciones
        
        self.logger.info(f"🖥️  Resolución: {self.screen_width}x{self.screen_height}")
        self.logger.info(f"📊 Factor de escala: {self.scale:.2f}")
    
    def scale_value(self, value: int) -> int:
        """Escalar cualquier valor (ancho, alto, padding, etc.)"""
        scaled = int(value * self.scale)
        return max(scaled, 1)
    
    def scale_font(self, base_size: int) -> int:
        """Escalar tamaño de fuente"""
        scaled = int(base_size * self.scale)
        return max(self.MIN_FONT_SIZE, min(scaled, self.MAX_FONT_SIZE))
    
    def scale_padding(self, base_padding: int) -> int:
        """Escalar padding"""
        scaled = int(base_padding * self.scale)
        return max(self.MIN_PADDING, min(scaled, self.MAX_PADDING))
    
    def scale_width(self, base_width: int) -> int:
        """Escalar ancho"""
        return int(base_width * self.scale_x)
    
    def scale_height(self, base_height: int) -> int:
        """Escalar alto"""
        return int(base_height * self.scale_y)
    
    def get_window_geometry(self, base_width: int, base_height: int) -> str:
        """Obtener geometría de ventana escalada"""
        width = self.scale_width(base_width)
        height = self.scale_height(base_height)
        
        # Centrar en pantalla
        x = (self.screen_width - width) // 2
        y = (self.screen_height - height) // 2
        
        return f"{width}x{height}+{x}+{y}"
    
    def get_fonts(self) -> Dict[str, Tuple[str, int, str]]:
        """Obtener fuentes escaladas"""
        return {
            # Fuentes principales
            'title': ('Segoe UI', self.scale_font(28), 'bold'),
            'subtitle': ('Segoe UI', self.scale_font(20), 'bold'),
            'heading': ('Segoe UI', self.scale_font(16), 'bold'),
            'body': ('Segoe UI', self.scale_font(12), 'normal'),
            'body_bold': ('Segoe UI', self.scale_font(12), 'bold'),
            'small': ('Segoe UI', self.scale_font(10), 'normal'),
            'tiny': ('Segoe UI', self.scale_font(9), 'normal'),
            
            # Fuentes específicas
            'button': ('Segoe UI', self.scale_font(13), 'bold'),
            'button_small': ('Segoe UI', self.scale_font(11), 'bold'),
            'label': ('Segoe UI', self.scale_font(12), 'bold'),
            'entry': ('Segoe UI', self.scale_font(11), 'normal'),
            'table_header': ('Segoe UI', self.scale_font(12), 'bold'),
            'table_body': ('Segoe UI', self.scale_font(11), 'normal'),
        }
    
    def get_sizes(self) -> Dict[str, int]:
        """Obtener tamaños comunes escalados"""
        return {
            # Padding
            'padding_xs': self.scale_padding(5),
            'padding_sm': self.scale_padding(10),
            'padding_md': self.scale_padding(15),
            'padding_lg': self.scale_padding(20),
            'padding_xl': self.scale_padding(30),
            
            # Margins
            'margin_sm': self.scale_padding(10),
            'margin_md': self.scale_padding(20),
            'margin_lg': self.scale_padding(30),
            
            # Alturas de componentes
            'button_height': self.scale_value(40),
            'input_height': self.scale_value(35),
            'header_height': self.scale_value(100),
            'navbar_height': self.scale_value(50),
            'footer_height': self.scale_value(60),
            
            # Anchos
            'sidebar_width': self.scale_value(250),
            'icon_size': self.scale_value(24),
            
            # Bordes
            'border_width': max(1, int(1 * self.scale)),
            'border_radius': self.scale_value(5),
        }


# Instancia global
_global_scaler = None


def get_auto_scaler(root_window: tk.Tk = None) -> AutoScaler:
    """
    Obtener instancia global del auto-scaler
    
    Args:
        root_window: Ventana raíz (opcional, solo necesaria en primera llamada)
    
    Returns:
        Instancia de AutoScaler
    """
    global _global_scaler
    if _global_scaler is None:
        _global_scaler = AutoScaler(root_window)
    return _global_scaler


def reset_auto_scaler():
    """Resetear el auto-scaler (útil para testing)"""
    global _global_scaler
    _global_scaler = None
