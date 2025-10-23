"""
Configurador Visual de Escalado Responsivo
Panel de control GUI para ajustar tamaños y resoluciones
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, List
import json
import os
from utils.responsive import get_scaler, ResponsiveScaler


class ResponsiveConfigurator:
    """Configurador visual para ajustar el sistema responsivo"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("⚙️ Configurador de Escalado Responsivo")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f8f9fa')
        
        # Variables de configuración
        self.current_resolution = tk.StringVar(value="1366x768")
        self.scale_factor = tk.DoubleVar(value=0.71)
        self.custom_scale = tk.BooleanVar(value=False)
        
        # Configuración actual
        self.config = self.load_default_config()
        
        # Scaler actual
        self.scaler = get_scaler(self.root)
        
        # Preview variables
        self.preview_widgets = []
        
        # Estado de cambios
        self.has_unsaved_changes = False
        self.notification_label = None
        
        self.create_ui()
        self.update_preview()
    
    def load_default_config(self) -> Dict:
        """Cargar configuración por defecto"""
        return {
            'resolutions': {
                '3840x2160': {'name': '4K/UHD', 'factor': 2.0},
                '2560x1440': {'name': '2K/QHD', 'factor': 1.33},
                '1920x1080': {'name': 'Full HD', 'factor': 1.0},
                '1600x900': {'name': 'HD+', 'factor': 0.83},
                '1366x768': {'name': 'HD', 'factor': 0.71},
                '1280x720': {'name': 'HD Ready', 'factor': 0.67},
            },
            'base_sizes': {
                'title_font': 16,
                'subtitle_font': 12,
                'default_font': 10,
                'small_font': 8,
                'padding_lg': 20,
                'padding_md': 15,
                'padding_sm': 10,
                'padding_xs': 5,
                'button_padding_x': 20,
                'button_padding_y': 10,
                'card_width': 220,
                'card_height': 140,
            },
            'min_limits': {
                'font_size': 8,
                'padding': 5,
                'button_height': 30,
                'widget_height': 25,
            }
        }
    
    def create_ui(self):
        """Crear interfaz principal"""
        # Header
        self.create_header()
        
        # Contenedor principal
        main_container = tk.Frame(self.root, bg='#f8f9fa')
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Panel izquierdo - Controles
        left_panel = tk.Frame(main_container, bg='white', relief='solid', borderwidth=1)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.create_controls_panel(left_panel)
        
        # Panel derecho - Preview
        right_panel = tk.Frame(main_container, bg='white', relief='solid', borderwidth=1)
        right_panel.pack(side='right', fill='both', expand=True)
        
        self.create_preview_panel(right_panel)
        
        # Footer con botones de acción
        self.create_footer()
    
    def create_header(self):
        """Crear header"""
        header = tk.Frame(self.root, bg='#2c3e50', height=100)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="⚙️ Configurador de Escalado Responsivo",
            font=('Segoe UI', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title.pack(pady=15)
        
        subtitle = tk.Label(
            header,
            text="Ajusta tamaños y resoluciones para tu aplicación",
            font=('Segoe UI', 10),
            bg='#2c3e50',
            fg='#bdc3c7'
        )
        subtitle.pack()
        
        # Área de notificaciones (oculta por defecto)
        self.notification_frame = tk.Frame(header, bg='#f39c12', height=0)
        self.notification_frame.pack(fill='x', side='bottom')
        self.notification_frame.pack_propagate(False)
        
        self.notification_label = tk.Label(
            self.notification_frame,
            text="",
            font=('Segoe UI', 10, 'bold'),
            bg='#f39c12',
            fg='white'
        )
        self.notification_label.pack(pady=8)
    
    def create_controls_panel(self, parent):
        """Crear panel de controles"""
        # Título del panel
        title_frame = tk.Frame(parent, bg='#3498db', height=50)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="🎛️ Controles de Configuración",
            font=('Segoe UI', 14, 'bold'),
            bg='#3498db',
            fg='white'
        ).pack(pady=12)
        
        # Contenedor scrollable
        canvas = tk.Canvas(parent, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Sección 1: Resolución
        self.create_resolution_section(scrollable_frame)
        
        # Sección 2: Tamaños base
        self.create_sizes_section(scrollable_frame)
        
        # Sección 3: Límites mínimos
        self.create_limits_section(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Scroll con rueda
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def create_resolution_section(self, parent):
        """Crear sección de resolución"""
        section = self.create_section(parent, "📐 Resolución de Pantalla")
        
        # Información actual
        info_frame = tk.Frame(section, bg='#e8f4f8', relief='solid', borderwidth=1)
        info_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(
            info_frame,
            text=f"Resolución actual: {self.scaler.screen_width}x{self.scaler.screen_height}",
            font=('Segoe UI', 10, 'bold'),
            bg='#e8f4f8',
            fg='#2c3e50'
        ).pack(pady=8)
        
        tk.Label(
            info_frame,
            text=f"Categoría: {self.scaler.resolution_category}",
            font=('Segoe UI', 9),
            bg='#e8f4f8',
            fg='#34495e'
        ).pack(pady=(0, 8))
        
        # Selector de resolución de prueba
        tk.Label(
            section,
            text="Simular resolución:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', padx=15, pady=(10, 5))
        
        resolutions = list(self.config['resolutions'].keys())
        res_combo = ttk.Combobox(
            section,
            textvariable=self.current_resolution,
            values=resolutions,
            state='readonly',
            font=('Segoe UI', 10),
            width=20
        )
        res_combo.pack(padx=15, pady=5)
        res_combo.bind('<<ComboboxSelected>>', self.on_resolution_change)
        
        # Factor de escala
        tk.Label(
            section,
            text="Factor de escala:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', padx=15, pady=(15, 5))
        
        scale_frame = tk.Frame(section, bg='white')
        scale_frame.pack(fill='x', padx=15, pady=5)
        
        self.scale_label = tk.Label(
            scale_frame,
            text=f"{self.scale_factor.get():.2f}x",
            font=('Segoe UI', 12, 'bold'),
            bg='white',
            fg='#3498db'
        )
        self.scale_label.pack(side='left', padx=(0, 10))
        
        scale_slider = ttk.Scale(
            scale_frame,
            from_=0.5,
            to=2.0,
            variable=self.scale_factor,
            orient='horizontal',
            command=lambda v: self.on_scale_change()
        )
        scale_slider.pack(side='left', fill='x', expand=True)
        
        # Checkbox para escala personalizada
        ttk.Checkbutton(
            section,
            text="Usar factor personalizado",
            variable=self.custom_scale,
            command=self.on_custom_scale_toggle
        ).pack(anchor='w', padx=15, pady=5)
    
    def create_sizes_section(self, parent):
        """Crear sección de tamaños base"""
        section = self.create_section(parent, "📏 Tamaños Base (1920x1080)")
        
        self.size_sliders = {}
        
        sizes_config = [
            ('Fuente Título', 'title_font', 12, 24, 'pt'),
            ('Fuente Subtítulo', 'subtitle_font', 10, 18, 'pt'),
            ('Fuente Por Defecto', 'default_font', 8, 14, 'pt'),
            ('Fuente Pequeña', 'small_font', 6, 12, 'pt'),
            ('Padding Grande', 'padding_lg', 10, 40, 'px'),
            ('Padding Mediano', 'padding_md', 8, 30, 'px'),
            ('Padding Pequeño', 'padding_sm', 5, 20, 'px'),
            ('Padding Extra Pequeño', 'padding_xs', 2, 10, 'px'),
            ('Ancho de Tarjeta', 'card_width', 150, 300, 'px'),
            ('Alto de Tarjeta', 'card_height', 100, 200, 'px'),
        ]
        
        for label, key, min_val, max_val, unit in sizes_config:
            self.create_slider_control(section, label, key, min_val, max_val, unit)
    
    def create_limits_section(self, parent):
        """Crear sección de límites mínimos"""
        section = self.create_section(parent, "⚠️ Límites Mínimos")
        
        limits_config = [
            ('Tamaño mínimo de fuente', 'font_size', 6, 12, 'pt'),
            ('Padding mínimo', 'padding', 3, 10, 'px'),
            ('Altura mínima de botón', 'button_height', 25, 50, 'px'),
            ('Altura mínima de widget', 'widget_height', 20, 40, 'px'),
        ]
        
        for label, key, min_val, max_val, unit in limits_config:
            self.create_slider_control(
                section, 
                label, 
                key, 
                min_val, 
                max_val, 
                unit,
                config_key='min_limits'
            )
    
    def create_section(self, parent, title):
        """Crear sección con título"""
        section = tk.Frame(parent, bg='white')
        section.pack(fill='x', pady=10)
        
        # Separador superior
        tk.Frame(section, bg='#e0e0e0', height=2).pack(fill='x', padx=15, pady=(10, 0))
        
        # Título
        tk.Label(
            section,
            text=title,
            font=('Segoe UI', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', padx=15, pady=10)
        
        return section
    
    def create_slider_control(self, parent, label, key, min_val, max_val, unit, config_key='base_sizes'):
        """Crear control deslizante"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='x', padx=15, pady=5)
        
        # Label y valor
        top_frame = tk.Frame(frame, bg='white')
        top_frame.pack(fill='x')
        
        tk.Label(
            top_frame,
            text=label,
            font=('Segoe UI', 9),
            bg='white',
            fg='#34495e'
        ).pack(side='left')
        
        current_val = self.config[config_key][key]
        value_label = tk.Label(
            top_frame,
            text=f"{current_val}{unit}",
            font=('Segoe UI', 9, 'bold'),
            bg='white',
            fg='#3498db'
        )
        value_label.pack(side='right')
        
        # Slider
        var = tk.DoubleVar(value=current_val)
        slider = ttk.Scale(
            frame,
            from_=min_val,
            to=max_val,
            variable=var,
            orient='horizontal',
            command=lambda v: self.on_slider_change(key, var, value_label, unit, config_key)
        )
        slider.pack(fill='x', pady=(2, 0))
        
        self.size_sliders[key] = {
            'var': var,
            'label': value_label,
            'unit': unit,
            'config_key': config_key
        }
    
    def create_preview_panel(self, parent):
        """Crear panel de preview"""
        # Título del panel
        title_frame = tk.Frame(parent, bg='#2ecc71', height=50)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="👁️ Vista Previa",
            font=('Segoe UI', 14, 'bold'),
            bg='#2ecc71',
            fg='white'
        ).pack(pady=12)
        
        # Contenedor scrollable
        canvas = tk.Canvas(parent, bg='#f8f9fa', highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        self.preview_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        self.preview_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.preview_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_footer(self):
        """Crear footer con botones"""
        footer = tk.Frame(self.root, bg='#ecf0f1', height=70)
        footer.pack(fill='x', side='bottom')
        footer.pack_propagate(False)
        
        button_frame = tk.Frame(footer, bg='#ecf0f1')
        button_frame.pack(expand=True)
        
        # Botón aplicar
        tk.Button(
            button_frame,
            text="✅ Guardar Configuración",
            command=self.apply_changes,
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            cursor='hand2',
            padx=25,
            pady=12
        ).pack(side='left', padx=5)
        
        # Botón exportar
        tk.Button(
            button_frame,
            text="💾 Exportar",
            command=self.export_config,
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=12
        ).pack(side='left', padx=5)
        
        # Botón resetear
        tk.Button(
            button_frame,
            text="🔄 Restaurar",
            command=self.reset_values,
            bg='#95a5a6',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=12
        ).pack(side='left', padx=5)
        
        # Botón cerrar
        tk.Button(
            button_frame,
            text="❌ Cerrar",
            command=self.root.quit,
            bg='#e74c3c',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=12
        ).pack(side='left', padx=5)
    
    def update_preview(self):
        """Actualizar vista previa"""
        # Limpiar preview anterior
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
        
        # Calcular tamaños escalados
        scale = self.scale_factor.get() if self.custom_scale.get() else self.get_current_scale_factor()
        
        # Preview de fuentes
        self.create_font_preview(scale)
        
        # Preview de tarjetas
        self.create_card_preview(scale)
        
        # Preview de botones
        self.create_button_preview(scale)
        
        # Preview de información
        self.create_info_preview(scale)
    
    def create_font_preview(self, scale):
        """Preview de fuentes"""
        section = tk.Frame(self.preview_frame, bg='white', relief='solid', borderwidth=1)
        section.pack(fill='x', padx=15, pady=10)
        
        tk.Label(
            section,
            text="Fuentes",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', padx=15, pady=10)
        
        fonts = [
            ('title_font', 'Título Principal'),
            ('subtitle_font', 'Subtítulo'),
            ('default_font', 'Texto por defecto'),
            ('small_font', 'Texto pequeño'),
        ]
        
        for key, label in fonts:
            base_size = self.config['base_sizes'][key]
            scaled_size = max(int(base_size * scale), self.config['min_limits']['font_size'])
            
            tk.Label(
                section,
                text=f"{label} ({scaled_size}pt)",
                font=('Segoe UI', scaled_size),
                bg='white',
                fg='#34495e'
            ).pack(anchor='w', padx=15, pady=2)
        
        tk.Frame(section, height=10, bg='white').pack()
    
    def create_card_preview(self, scale):
        """Preview de tarjeta"""
        section = tk.Frame(self.preview_frame, bg='white', relief='solid', borderwidth=1)
        section.pack(fill='x', padx=15, pady=10)
        
        tk.Label(
            section,
            text="Tarjeta de Módulo",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', padx=15, pady=10)
        
        # Calcular tamaño escalado
        base_width = self.config['base_sizes']['card_width']
        base_height = self.config['base_sizes']['card_height']
        card_width = int(base_width * scale)
        card_height = int(base_height * scale)
        
        # Crear tarjeta de ejemplo
        card = tk.Frame(section, bg='#3498db', width=card_width, height=card_height)
        card.pack(padx=15, pady=10)
        card.pack_propagate(False)
        
        title_size = max(int(11 * scale), self.config['min_limits']['font_size'])
        
        tk.Label(
            card,
            text="📦",
            font=('Segoe UI Emoji', int(36 * scale)),
            bg='#3498db',
            fg='white'
        ).pack(expand=True)
        
        tk.Label(
            card,
            text=f"Módulo ({card_width}x{card_height}px)",
            font=('Segoe UI', title_size, 'bold'),
            bg='#3498db',
            fg='white'
        ).pack(pady=(0, 10))
        
        tk.Frame(section, height=10, bg='white').pack()
    
    def create_button_preview(self, scale):
        """Preview de botones"""
        section = tk.Frame(self.preview_frame, bg='white', relief='solid', borderwidth=1)
        section.pack(fill='x', padx=15, pady=10)
        
        tk.Label(
            section,
            text="Botones",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', padx=15, pady=10)
        
        btn_frame = tk.Frame(section, bg='white')
        btn_frame.pack(padx=15, pady=10)
        
        padx = max(int(self.config['base_sizes']['button_padding_x'] * scale), self.config['min_limits']['padding'])
        pady = max(int(self.config['base_sizes']['button_padding_y'] * scale), self.config['min_limits']['padding'])
        font_size = max(int(10 * scale), self.config['min_limits']['font_size'])
        
        tk.Button(
            btn_frame,
            text="Botón de Ejemplo",
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', font_size),
            relief='flat',
            padx=padx,
            pady=pady
        ).pack()
        
        tk.Label(
            section,
            text=f"Padding: {padx}x{pady}px, Fuente: {font_size}pt",
            font=('Segoe UI', 8),
            bg='white',
            fg='#7f8c8d'
        ).pack(pady=(5, 10))
        
        tk.Frame(section, height=10, bg='white').pack()
    
    def create_info_preview(self, scale):
        """Preview de información"""
        section = tk.Frame(self.preview_frame, bg='#e8f4f8', relief='solid', borderwidth=1)
        section.pack(fill='x', padx=15, pady=10)
        
        tk.Label(
            section,
            text="📊 Resumen de Escala",
            font=('Segoe UI', 11, 'bold'),
            bg='#e8f4f8',
            fg='#2c3e50'
        ).pack(anchor='w', padx=15, pady=10)
        
        info = [
            f"Factor de escala: {scale:.2f}x",
            f"Resolución simulada: {self.current_resolution.get()}",
            f"Fuente título: {self.config['base_sizes']['title_font']}pt → {int(self.config['base_sizes']['title_font'] * scale)}pt",
            f"Padding grande: {self.config['base_sizes']['padding_lg']}px → {int(self.config['base_sizes']['padding_lg'] * scale)}px",
            f"Tarjeta: {self.config['base_sizes']['card_width']}x{self.config['base_sizes']['card_height']}px → {int(self.config['base_sizes']['card_width'] * scale)}x{int(self.config['base_sizes']['card_height'] * scale)}px",
        ]
        
        for line in info:
            tk.Label(
                section,
                text=line,
                font=('Segoe UI', 9),
                bg='#e8f4f8',
                fg='#34495e',
                anchor='w'
            ).pack(fill='x', padx=20, pady=2)
        
        tk.Frame(section, height=10, bg='#e8f4f8').pack()
    
    def on_resolution_change(self, event=None):
        """Manejar cambio de resolución"""
        resolution = self.current_resolution.get()
        if not self.custom_scale.get():
            factor = self.config['resolutions'][resolution]['factor']
            self.scale_factor.set(factor)
            self.scale_label.config(text=f"{factor:.2f}x")
        self.update_preview()
        self.mark_as_changed()
    
    def on_scale_change(self):
        """Manejar cambio de escala"""
        factor = self.scale_factor.get()
        self.scale_label.config(text=f"{factor:.2f}x")
        if self.custom_scale.get():
            self.update_preview()
            self.mark_as_changed()
    
    def on_custom_scale_toggle(self):
        """Toggle de escala personalizada"""
        if not self.custom_scale.get():
            self.on_resolution_change()
        else:
            self.update_preview()
        self.mark_as_changed()
    
    def on_slider_change(self, key, var, label, unit, config_key):
        """Manejar cambio de slider"""
        value = int(var.get())
        label.config(text=f"{value}{unit}")
        self.config[config_key][key] = value
        self.update_preview()
        self.mark_as_changed()
    
    def get_current_scale_factor(self):
        """Obtener factor de escala actual"""
        resolution = self.current_resolution.get()
        return self.config['resolutions'][resolution]['factor']
    
    def mark_as_changed(self):
        """Marcar que hay cambios sin guardar"""
        if not self.has_unsaved_changes:
            self.has_unsaved_changes = True
            self.show_notification(
                "⚠️ Cambios sin guardar - Haz clic en 'Guardar Configuración' y reinicia la aplicación para ver los cambios",
                "#f39c12"
            )
    
    def show_notification(self, message, bg_color):
        """Mostrar notificación en el header"""
        self.notification_label.config(text=message)
        self.notification_frame.config(bg=bg_color, height=40)
        self.notification_label.config(bg=bg_color)
    
    def hide_notification(self):
        """Ocultar notificación"""
        self.notification_frame.config(height=0)
    
    def apply_changes(self):
        """Aplicar cambios a la configuración"""
        try:
            # Guardar configuración
            config_path = os.path.join('config', 'responsive_config.json')
            os.makedirs('config', exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            
            # Marcar como guardado
            self.has_unsaved_changes = False
            
            # Mostrar notificación de éxito
            self.show_notification(
                "✅ Configuración guardada - REINICIA LA APLICACIÓN (python main.py) para ver los cambios",
                "#27ae60"
            )
            
            # Mostrar diálogo
            messagebox.showinfo(
                "✅ Configuración Guardada",
                "Configuración guardada correctamente.\n\n"
                "⚠️ IMPORTANTE:\n"
                "Para ver los cambios aplicados, debes:\n\n"
                "1️⃣ Cerrar tu aplicación si está abierta\n"
                "2️⃣ Ejecutar nuevamente: python main.py\n\n"
                "Los cambios NO se aplican automáticamente.\n\n"
                "Archivo: config/responsive_config.json"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar configuración:\n{str(e)}")
    
    def export_config(self):
        """Exportar configuración"""
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile="responsive_config.json"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, indent=4)
                messagebox.showinfo("Éxito", f"✅ Configuración exportada a:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar:\n{str(e)}")
    
    def reset_values(self):
        """Resetear valores por defecto"""
        if messagebox.askyesno("Confirmar", "¿Restaurar valores por defecto?"):
            self.config = self.load_default_config()
            
            # Actualizar sliders
            for key, slider_data in self.size_sliders.items():
                config_key = slider_data['config_key']
                value = self.config[config_key][key]
                slider_data['var'].set(value)
                slider_data['label'].config(text=f"{value}{slider_data['unit']}")
            
            self.update_preview()
            self.mark_as_changed()
            messagebox.showinfo(
                "✅ Valores Restaurados", 
                "Valores restaurados a los predeterminados.\n\n"
                "⚠️ No olvides hacer clic en 'Guardar Configuración'\n"
                "y reiniciar la aplicación para aplicar los cambios."
            )
    
    def run(self):
        """Ejecutar aplicación"""
        self.root.mainloop()


if __name__ == '__main__':
    app = ResponsiveConfigurator()
    app.run()
