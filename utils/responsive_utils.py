"""
Utilidades para diseño responsivo en Tkinter
Adapta la interfaz según el tamaño de pantalla del dispositivo
"""

import tkinter as tk
from typing import Dict, Tuple


class ResponsiveManager:
    """Gestor de diseño responsivo para aplicaciones Tkinter"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        
        # Detectar tipo de pantalla
        self.screen_type = self._detect_screen_type()
        
        # Configuraciones por tipo de pantalla
        self.config = self._get_responsive_config()
        
        print(f"📱 Pantalla detectada: {self.screen_width}x{self.screen_height} ({self.screen_type})")
    
    def _detect_screen_type(self) -> str:
        """Detectar tipo de pantalla según resolución"""
        if self.screen_width <= 1366:
            return 'small'      # Laptops pequeñas, tablets
        elif self.screen_width <= 1920:
            return 'medium'     # Full HD estándar
        elif self.screen_width <= 2560:
            return 'large'      # 2K
        else:
            return 'xlarge'     # 4K o superior
    
    def _get_responsive_config(self) -> Dict:
        """Obtener configuración responsiva según tipo de pantalla"""
        configs = {
            'small': {
                # Pantallas 1366x768 o menores
                'window_width': 1320,
                'window_height': 760,
                'font_size_base': 10,
                'font_size_title': 15,
                'font_size_header': 13,
                'font_size_body': 10,
                'font_size_small': 9,
                'padding_large': 18,
                'padding_medium': 12,
                'padding_small': 6,
                'button_height': 38,
                'toolbar_height': 54,
                'sidebar_width': 215,
                'table_row_height': 26,
                'icon_size': 18,
                'use_compact_mode': True
            },
            'medium': {
                # Pantallas 1920x1080 (Full HD)
                'window_width': 1600,
                'window_height': 900,
                'font_size_base': 10,
                'font_size_title': 16,
                'font_size_header': 13,
                'font_size_body': 10,
                'font_size_small': 9,
                'padding_large': 20,
                'padding_medium': 12,
                'padding_small': 6,
                'button_height': 40,
                'toolbar_height': 60,
                'sidebar_width': 250,
                'table_row_height': 28,
                'icon_size': 20,
                'use_compact_mode': False
            },
            'large': {
                # Pantallas 2560x1440 (2K)
                'window_width': 2000,
                'window_height': 1200,
                'font_size_base': 11,
                'font_size_title': 18,
                'font_size_header': 14,
                'font_size_body': 11,
                'font_size_small': 10,
                'padding_large': 25,
                'padding_medium': 15,
                'padding_small': 8,
                'button_height': 45,
                'toolbar_height': 70,
                'sidebar_width': 300,
                'table_row_height': 30,
                'icon_size': 24,
                'use_compact_mode': False
            },
            'xlarge': {
                # Pantallas 3840x2160 (4K) o superiores
                'window_width': 2400,
                'window_height': 1400,
                'font_size_base': 12,
                'font_size_title': 20,
                'font_size_header': 16,
                'font_size_body': 12,
                'font_size_small': 11,
                'padding_large': 30,
                'padding_medium': 18,
                'padding_small': 10,
                'button_height': 50,
                'toolbar_height': 80,
                'sidebar_width': 350,
                'table_row_height': 35,
                'icon_size': 28,
                'use_compact_mode': False
            }
        }
        
        return configs.get(self.screen_type, configs['medium'])
    
    def get_window_size(self) -> Tuple[int, int]:
        """Obtener tamaño óptimo de ventana"""
        return (self.config['window_width'], self.config['window_height'])
    
    def center_window(self, window: tk.Tk | tk.Toplevel, width: int = None, height: int = None):
        """Centrar ventana en la pantalla"""
        if width is None:
            width = self.config['window_width']
        if height is None:
            height = self.config['window_height']
        
        # Calcular posición para centrar
        x = (self.screen_width - width) // 2
        y = (self.screen_height - height) // 2
        
        # Aplicar geometría
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def get_font(self, font_type: str = 'body', bold: bool = False) -> Tuple[str, int, str]:
        """Obtener configuración de fuente responsiva"""
        size_map = {
            'title': self.config['font_size_title'],
            'header': self.config['font_size_header'],
            'body': self.config['font_size_body'],
            'small': self.config['font_size_small'],
            'base': self.config['font_size_base']
        }
        
        size = size_map.get(font_type, self.config['font_size_body'])
        weight = 'bold' if bold else 'normal'
        
        return ('Segoe UI', size, weight)
    
    def get_padding(self, size: str = 'medium') -> int:
        """Obtener padding responsivo"""
        padding_map = {
            'large': self.config['padding_large'],
            'medium': self.config['padding_medium'],
            'small': self.config['padding_small']
        }
        return padding_map.get(size, self.config['padding_medium'])
    
    def get_button_height(self) -> int:
        """Obtener altura de botones"""
        return self.config['button_height']
    
    def get_toolbar_height(self) -> int:
        """Obtener altura de toolbar"""
        return self.config['toolbar_height']
    
    def get_sidebar_width(self) -> int:
        """Obtener ancho de sidebar"""
        return self.config['sidebar_width']
    
    def get_table_row_height(self) -> int:
        """Obtener altura de filas de tabla"""
        return self.config['table_row_height']
    
    def is_compact_mode(self) -> bool:
        """Verificar si debe usar modo compacto"""
        return self.config.get('use_compact_mode', False)
    
    def configure_treeview_style(self, style: tk.ttk.Style):
        """Configurar estilo de Treeview responsivo"""
        row_height = self.get_table_row_height()
        font_size = self.config['font_size_body']
        
        style.configure(
            "Treeview",
            rowheight=row_height,
            font=('Segoe UI', font_size)
        )
        style.configure(
            "Treeview.Heading",
            font=('Segoe UI', font_size, 'bold')
        )
    
    def make_window_responsive(self, window: tk.Tk | tk.Toplevel):
        """Hacer ventana completamente responsiva"""
        # Permitir redimensionamiento
        window.resizable(True, True)
        
        # Configurar peso para que los widgets se expandan
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        
        # Tamaño mínimo
        min_width = int(self.config['window_width'] * 0.7)
        min_height = int(self.config['window_height'] * 0.7)
        window.minsize(min_width, min_height)
        
        # Centrar ventana
        self.center_window(window)
    
    def get_grid_weights(self, layout_type: str = 'default') -> Dict:
        """Obtener configuración de weights para grid layout"""
        layouts = {
            'default': {
                'columns': [1],  # Una columna con weight 1
                'rows': [1]      # Una fila con weight 1
            },
            'sidebar_main': {
                'columns': [0, 3],  # Sidebar fijo, main expandible
                'rows': [1]
            },
            'header_content_footer': {
                'columns': [1],
                'rows': [0, 1, 0]  # Header fijo, content expandible, footer fijo
            },
            'two_columns': {
                'columns': [1, 1],  # Dos columnas iguales
                'rows': [1]
            },
            'three_columns': {
                'columns': [1, 2, 1],  # Columna central más grande
                'rows': [1]
            }
        }
        
        return layouts.get(layout_type, layouts['default'])
    
    def apply_grid_weights(self, widget: tk.Widget, layout_type: str = 'default'):
        """Aplicar weights a grid layout"""
        weights = self.get_grid_weights(layout_type)
        
        for col, weight in enumerate(weights['columns']):
            widget.columnconfigure(col, weight=weight)
        
        for row, weight in enumerate(weights['rows']):
            widget.rowconfigure(row, weight=weight)
    
    def scale_value(self, base_value: int | float, scale_factor: float = 1.0) -> int:
        """Escalar valor según tamaño de pantalla"""
        screen_scale = {
            'small': 0.8,
            'medium': 1.0,
            'large': 1.2,
            'xlarge': 1.4
        }
        
        total_scale = screen_scale.get(self.screen_type, 1.0) * scale_factor
        return int(base_value * total_scale)
    
    def get_responsive_size(self, base_width: int, base_height: int) -> Tuple[int, int]:
        """Obtener tamaño responsivo para un widget"""
        return (
            self.scale_value(base_width),
            self.scale_value(base_height)
        )


# Instancia global (se inicializa en main.py)
_responsive_manager = None


def init_responsive(root: tk.Tk) -> ResponsiveManager:
    """Inicializar gestor responsivo global"""
    global _responsive_manager
    _responsive_manager = ResponsiveManager(root)
    return _responsive_manager


def get_responsive() -> ResponsiveManager:
    """Obtener gestor responsivo global"""
    if _responsive_manager is None:
        raise RuntimeError("ResponsiveManager no ha sido inicializado. Llama a init_responsive() primero.")
    return _responsive_manager
