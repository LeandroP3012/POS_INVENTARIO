"""
Vista Base para el Sistema POS
Clase base para todas las vistas con funciones comunes
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
from typing import Dict, Any, Callable, Optional
import logging
from config.settings import SystemSettings

class BaseView:
    """Clase base para todas las vistas del sistema"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.root = parent if parent else tk.Tk()
        self.settings = SystemSettings()
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Variables de configuración
        self.colors = self.settings.get_colors()
        self.fonts = self._setup_fonts()
        
        # Variables de control
        self.is_initialized = False
        self.callbacks = {}
        
        # Configurar estilo
        self.setup_style()
    
    def _setup_fonts(self) -> Dict[str, font.Font]:
        """Configurar fuentes del sistema"""
        return {
            'default': font.Font(family="Segoe UI", size=10),
            'title': font.Font(family="Segoe UI", size=16, weight="bold"),
            'subtitle': font.Font(family="Segoe UI", size=12, weight="bold"),
            'button': font.Font(family="Segoe UI", size=10, weight="normal"),
            'small': font.Font(family="Segoe UI", size=8),
            'large': font.Font(family="Segoe UI", size=14)
        }
    
    def setup_style(self):
        """Configurar estilos TTK"""
        self.style = ttk.Style()
        
        # Configurar tema
        available_themes = self.style.theme_names()
        if 'clam' in available_themes:
            self.style.theme_use('clam')
        elif 'alt' in available_themes:
            self.style.theme_use('alt')
        
        # Colores personalizados
        colors = self.colors
        
        # Configurar estilos de botones
        self.style.configure(
            'Primary.TButton',
            background=colors['primary'],
            foreground='white',
            borderwidth=0,
            focuscolor='none',
            padding=(20, 10)
        )
        
        self.style.map(
            'Primary.TButton',
            background=[('active', colors['primary_dark']),
                       ('pressed', colors['primary_dark'])]
        )
        
        self.style.configure(
            'Secondary.TButton',
            background=colors['secondary'],
            foreground='white',
            borderwidth=0,
            focuscolor='none',
            padding=(15, 8)
        )
        
        self.style.configure(
            'Success.TButton',
            background=colors['success'],
            foreground='white',
            borderwidth=0,
            focuscolor='none',
            padding=(15, 8)
        )
        
        self.style.configure(
            'Warning.TButton',
            background=colors['warning'],
            foreground='white',
            borderwidth=0,
            focuscolor='none',
            padding=(15, 8)
        )
        
        self.style.configure(
            'Danger.TButton',
            background=colors['danger'],
            foreground='white',
            borderwidth=0,
            focuscolor='none',
            padding=(15, 8)
        )
        
        # Configurar estilos de frames
        self.style.configure(
            'Card.TFrame',
            background=colors['surface'],
            relief='solid',
            borderwidth=1
        )
        
        # Configurar estilos de labels
        self.style.configure(
            'Title.TLabel',
            background=colors['background'],
            foreground=colors['on_background'],
            font=self.fonts['title']
        )
        
        self.style.configure(
            'Subtitle.TLabel',
            background=colors['background'],
            foreground=colors['on_background'],
            font=self.fonts['subtitle']
        )
        
        # Configurar entrada de texto
        self.style.configure(
            'Custom.TEntry',
            borderwidth=1,
            relief='solid',
            padding=10
        )
    
    def create_window(self, title: str, width: int = 800, height: int = 600, 
                     resizable: bool = True, center: bool = True) -> tk.Toplevel:
        """Crear ventana secundaria"""
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry(f"{width}x{height}")
        
        if not resizable:
            window.resizable(False, False)
        
        if center:
            self.center_window(window, width, height)
        
        # Configurar colores
        window.configure(bg=self.colors['background'])
        
        return window
    
    def center_window(self, window, width: int, height: int):
        """Centrar ventana en la pantalla"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_card_frame(self, parent, padding: int = 20) -> ttk.Frame:
        """Crear frame con estilo de tarjeta"""
        frame = ttk.Frame(parent, style='Card.TFrame')
        frame.pack(fill='both', expand=True, padx=padding, pady=padding)
        return frame
    
    def create_title_label(self, parent, text: str, pack_options: Dict = None) -> ttk.Label:
        """Crear label de título"""
        label = ttk.Label(parent, text=text, style='Title.TLabel')
        
        if pack_options:
            label.pack(**pack_options)
        else:
            label.pack(pady=(0, 20))
        
        return label
    
    def create_subtitle_label(self, parent, text: str, pack_options: Dict = None) -> ttk.Label:
        """Crear label de subtítulo"""
        label = ttk.Label(parent, text=text, style='Subtitle.TLabel')
        
        if pack_options:
            label.pack(**pack_options)
        else:
            label.pack(pady=(0, 10))
        
        return label
    
    def create_button(self, parent, text: str, command: Callable, 
                     style: str = 'Primary.TButton', pack_options: Dict = None) -> ttk.Button:
        """Crear botón con estilo"""
        button = ttk.Button(parent, text=text, command=command, style=style)
        
        if pack_options:
            button.pack(**pack_options)
        else:
            button.pack(pady=10)
        
        return button
    
    def create_entry(self, parent, textvariable=None, placeholder: str = None, 
                    show: str = None, pack_options: Dict = None) -> ttk.Entry:
        """Crear campo de entrada"""
        entry = ttk.Entry(parent, textvariable=textvariable, style='Custom.TEntry')
        
        if show:  # Para contraseñas
            entry.configure(show=show)
        
        if placeholder:
            self.add_placeholder(entry, placeholder)
        
        if pack_options:
            entry.pack(**pack_options)
        else:
            entry.pack(pady=5, padx=10, fill='x')
        
        return entry
    
    def add_placeholder(self, entry: ttk.Entry, placeholder: str):
        """Agregar placeholder a un Entry"""
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.configure(foreground=self.colors['on_background'])
        
        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.configure(foreground=self.colors['on_surface_variant'])
        
        # Establecer placeholder inicial
        entry.insert(0, placeholder)
        entry.configure(foreground=self.colors['on_surface_variant'])
        
        # Bind eventos
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
    
    def create_labeled_entry(self, parent, label_text: str, textvariable=None,
                           show: str = None, placeholder: str = None) -> tuple[ttk.Label, ttk.Entry]:
        """Crear entrada con etiqueta"""
        frame = ttk.Frame(parent)
        frame.pack(fill='x', padx=10, pady=5)
        
        label = ttk.Label(frame, text=label_text)
        label.pack(anchor='w')
        
        entry = ttk.Entry(frame, textvariable=textvariable, style='Custom.TEntry')
        
        if show:
            entry.configure(show=show)
        
        if placeholder:
            self.add_placeholder(entry, placeholder)
        
        entry.pack(fill='x', pady=(5, 0))
        
        return label, entry
    
    def create_button_frame(self, parent, pack_options: Dict = None) -> ttk.Frame:
        """Crear frame para botones"""
        frame = ttk.Frame(parent)
        
        if pack_options:
            frame.pack(**pack_options)
        else:
            frame.pack(fill='x', padx=10, pady=20)
        
        return frame
    
    def show_success(self, title: str, message: str):
        """Mostrar mensaje de éxito"""
        messagebox.showinfo(title, message)
    
    def show_error(self, title: str, message: str):
        """Mostrar mensaje de error"""
        messagebox.showerror(title, message)
    
    def show_warning(self, title: str, message: str):
        """Mostrar mensaje de advertencia"""
        messagebox.showwarning(title, message)
    
    def ask_confirmation(self, title: str, message: str) -> bool:
        """Pedir confirmación al usuario"""
        return messagebox.askyesno(title, message)
    
    def show_loading(self, message: str = "Cargando..."):
        """Mostrar ventana de carga"""
        self.loading_window = tk.Toplevel(self.root)
        self.loading_window.title("Por favor espere")
        self.loading_window.geometry("300x100")
        self.loading_window.resizable(False, False)
        self.loading_window.configure(bg=self.colors['background'])
        
        # Centrar ventana
        self.center_window(self.loading_window, 300, 100)
        
        # Contenido
        frame = ttk.Frame(self.loading_window)
        frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        label = ttk.Label(frame, text=message, font=self.fonts['default'])
        label.pack()
        
        # Barra de progreso
        progress = ttk.Progressbar(frame, mode='indeterminate')
        progress.pack(fill='x', pady=(10, 0))
        progress.start(10)
        
        # Hacer modal
        self.loading_window.transient(self.root)
        self.loading_window.grab_set()
        
        # Actualizar interfaz
        self.root.update()
    
    def hide_loading(self):
        """Ocultar ventana de carga"""
        if hasattr(self, 'loading_window'):
            self.loading_window.destroy()
            delattr(self, 'loading_window')
    
    def bind_callback(self, event_name: str, callback: Callable):
        """Registrar callback para evento"""
        self.callbacks[event_name] = callback
    
    def trigger_callback(self, event_name: str, *args, **kwargs):
        """Ejecutar callback si existe"""
        if event_name in self.callbacks:
            try:
                return self.callbacks[event_name](*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Error en callback {event_name}: {e}")
                return None
        return None
    
    def validate_form(self, validations: Dict[str, Any]) -> tuple[bool, str]:
        """Validar formulario con reglas"""
        for field_name, rules in validations.items():
            value = rules.get('value', '')
            required = rules.get('required', False)
            min_length = rules.get('min_length')
            max_length = rules.get('max_length')
            pattern = rules.get('pattern')
            custom_validator = rules.get('validator')
            
            # Campo requerido
            if required and not value.strip():
                return False, f"El campo {field_name} es requerido"
            
            # Longitud mínima
            if min_length and len(value) < min_length:
                return False, f"El campo {field_name} debe tener al menos {min_length} caracteres"
            
            # Longitud máxima
            if max_length and len(value) > max_length:
                return False, f"El campo {field_name} no puede tener más de {max_length} caracteres"
            
            # Patrón regex
            if pattern and not pattern.match(value):
                return False, f"El campo {field_name} no tiene un formato válido"
            
            # Validador personalizado
            if custom_validator:
                is_valid, error_msg = custom_validator(value)
                if not is_valid:
                    return False, error_msg
        
        return True, ""
    
    def clear_frame(self, frame):
        """Limpiar todos los widgets de un frame"""
        for widget in frame.winfo_children():
            widget.destroy()
    
    def set_window_icon(self, window, icon_path: str = None):
        """Establecer icono de ventana"""
        if icon_path:
            try:
                window.iconbitmap(icon_path)
            except:
                self.logger.warning(f"No se pudo cargar el icono: {icon_path}")
    
    def make_modal(self, window):
        """Hacer ventana modal"""
        window.transient(self.root)
        window.grab_set()
        window.focus_set()
    
    def setup_window_close_protocol(self, window, callback: Callable = None):
        """Configurar protocolo de cierre de ventana"""
        def on_close():
            if callback:
                if callback():  # Si el callback retorna True, cerrar
                    window.destroy()
            else:
                window.destroy()
        
        window.protocol("WM_DELETE_WINDOW", on_close)
    
    def bind_enter_key(self, widget, callback: Callable):
        """Bind tecla Enter a un widget"""
        widget.bind('<Return>', lambda event: callback())
    
    def create_separator(self, parent, pack_options: Dict = None) -> ttk.Separator:
        """Crear separador"""
        separator = ttk.Separator(parent, orient='horizontal')
        
        if pack_options:
            separator.pack(**pack_options)
        else:
            separator.pack(fill='x', padx=10, pady=10)
        
        return separator
    
    def create_scrollable_frame(self, parent) -> tuple[tk.Canvas, ttk.Frame]:
        """Crear frame con scroll"""
        canvas = tk.Canvas(parent, bg=self.colors['background'])
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return canvas, scrollable_frame
    
    def on_destroy(self):
        """Método llamado al destruir la vista"""
        pass
