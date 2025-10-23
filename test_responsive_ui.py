"""
Script de Prueba - Sistema de Escalado Responsivo
Muestra cómo funciona el escalado en diferentes resoluciones
"""

import tkinter as tk
from tkinter import ttk
from utils.responsive import get_scaler, ResponsiveScaler


def test_responsive_system():
    """Probar sistema de escalado responsivo"""
    
    # Crear ventana principal
    root = tk.Tk()
    root.title("Prueba de Sistema Responsivo")
    root.configure(bg='#f0f0f0')
    
    # Obtener scaler
    scaler = get_scaler(root)
    
    # Imprimir información
    scaler.print_info()
    
    # Obtener tamaños responsivos
    sizes = scaler.get_responsive_sizes()
    fonts = scaler.get_responsive_fonts()
    
    # Configurar tamaño de ventana responsivo
    window_width, window_height = scaler.get_window_size(1200, 800, min_width=800, min_height=600)
    root.geometry(f"{window_width}x{window_height}")
    
    # Centrar ventana
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Frame principal con padding responsivo
    main_frame = tk.Frame(root, bg='white')
    main_frame.pack(fill='both', expand=True, 
                   padx=sizes['padding_lg'], 
                   pady=sizes['padding_lg'])
    
    # Título con fuente responsiva
    title_font = fonts['xlarge']
    title = tk.Label(
        main_frame,
        text="🖥️ Sistema de Escalado Responsivo",
        font=title_font,
        bg='white',
        fg='#2c3e50'
    )
    title.pack(pady=sizes['padding_md'])
    
    # Información de pantalla
    info_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='solid', borderwidth=sizes['border_width'])
    info_frame.pack(fill='x', pady=sizes['padding_md'])
    
    info_data = scaler.get_info()
    
    subtitle_font = fonts['subtitle']
    default_font = fonts['default']
    
    tk.Label(
        info_frame,
        text="Información de Pantalla",
        font=subtitle_font,
        bg='#ecf0f1',
        fg='#2c3e50'
    ).pack(pady=sizes['padding_sm'])
    
    info_items = [
        f"Resolución: {info_data['screen_resolution']}",
        f"Categoría: {info_data['resolution_category']}",
        f"Factor de escala: {info_data['scale_factor']}",
        f"Factor X: {info_data['scale_factor_x']}",
        f"Factor Y: {info_data['scale_factor_y']}",
        f"Modo compacto: {'Sí' if info_data['compact_layout'] else 'No'}"
    ]
    
    for item in info_items:
        tk.Label(
            info_frame,
            text=item,
            font=default_font,
            bg='#ecf0f1',
            fg='#34495e',
            anchor='w'
        ).pack(padx=sizes['padding_md'], pady=2, fill='x')
    
    tk.Label(info_frame, text="", bg='#ecf0f1').pack(pady=sizes['padding_xs'])
    
    # Frame de demostración de tamaños
    demo_frame = tk.Frame(main_frame, bg='white')
    demo_frame.pack(fill='both', expand=True, pady=sizes['padding_md'])
    
    # Columna izquierda - Fuentes
    left_frame = tk.Frame(demo_frame, bg='white')
    left_frame.pack(side='left', fill='both', expand=True, padx=sizes['padding_sm'])
    
    tk.Label(
        left_frame,
        text="Tamaños de Fuente Responsivos",
        font=subtitle_font,
        bg='white',
        fg='#2c3e50'
    ).pack(pady=sizes['padding_sm'])
    
    font_demos = [
        ('small', 'Texto pequeño'),
        ('default', 'Texto por defecto'),
        ('heading', 'Encabezado'),
        ('subtitle', 'Subtítulo'),
        ('title', 'Título'),
        ('xlarge', 'Extra grande')
    ]
    
    for font_name, text in font_demos:
        f = fonts[font_name]
        tk.Label(
            left_frame,
            text=f"{text} ({f[1]}pt)",
            font=f,
            bg='white',
            fg='#2c3e50',
            anchor='w'
        ).pack(padx=sizes['padding_md'], pady=2, fill='x')
    
    # Columna derecha - Botones
    right_frame = tk.Frame(demo_frame, bg='white')
    right_frame.pack(side='right', fill='both', expand=True, padx=sizes['padding_sm'])
    
    tk.Label(
        right_frame,
        text="Botones Responsivos",
        font=subtitle_font,
        bg='white',
        fg='#2c3e50'
    ).pack(pady=sizes['padding_sm'])
    
    # Botones de diferentes tamaños
    button_styles = [
        ('small', '#95a5a6', 'Botón Pequeño'),
        ('default', '#3498db', 'Botón Normal'),
        ('large', '#2ecc71', 'Botón Grande')
    ]
    
    for size, color, text in button_styles:
        config = scaler.get_button_config(size)
        btn_frame = tk.Frame(right_frame, bg='white')
        btn_frame.pack(pady=sizes['padding_xs'])
        
        btn = tk.Button(
            btn_frame,
            text=text,
            bg=color,
            fg='white',
            font=('Segoe UI', config['font_size']),
            relief='flat',
            cursor='hand2',
            padx=config['padding'][0],
            pady=config['padding'][1]
        )
        btn.pack()
    
    # Frame de tamaños
    sizes_frame = tk.Frame(main_frame, bg='#e8f4f8', relief='solid', borderwidth=sizes['border_width'])
    sizes_frame.pack(fill='x', pady=sizes['padding_md'])
    
    tk.Label(
        sizes_frame,
        text="Valores de Padding Responsivos",
        font=subtitle_font,
        bg='#e8f4f8',
        fg='#2c3e50'
    ).pack(pady=sizes['padding_sm'])
    
    size_items = [
        f"XS: {sizes['padding_xs']}px",
        f"SM: {sizes['padding_sm']}px",
        f"MD: {sizes['padding_md']}px",
        f"LG: {sizes['padding_lg']}px",
        f"XL: {sizes['padding_xl']}px",
        f"Altura de Entry: {sizes['entry_height']}px",
        f"Altura de Botón: {sizes['button_height']}px"
    ]
    
    for item in size_items:
        tk.Label(
            sizes_frame,
            text=item,
            font=default_font,
            bg='#e8f4f8',
            fg='#34495e',
            anchor='w'
        ).pack(padx=sizes['padding_md'], pady=2, fill='x')
    
    tk.Label(sizes_frame, text="", bg='#e8f4f8').pack(pady=sizes['padding_xs'])
    
    # Mensaje final
    message_frame = tk.Frame(main_frame, bg='#d5f4e6', relief='solid', borderwidth=sizes['border_width'])
    message_frame.pack(fill='x', pady=sizes['padding_md'])
    
    message = (
        "✅ El sistema de escalado responsivo ajusta automáticamente:\n"
        "   • Tamaños de fuente\n"
        "   • Padding y márgenes\n"
        "   • Dimensiones de widgets\n"
        "   • Tamaño de ventanas\n"
        "   • Anchos de columnas en tablas"
    )
    
    tk.Label(
        message_frame,
        text=message,
        font=default_font,
        bg='#d5f4e6',
        fg='#27ae60',
        justify='left',
        anchor='w'
    ).pack(padx=sizes['padding_md'], pady=sizes['padding_md'], fill='x')
    
    # Botón de cerrar
    close_btn = tk.Button(
        main_frame,
        text="Cerrar",
        command=root.destroy,
        bg='#e74c3c',
        fg='white',
        font=('Segoe UI', fonts['button'][1]),
        relief='flat',
        cursor='hand2',
        padx=scaler.get_button_config('default')['padding'][0],
        pady=scaler.get_button_config('default')['padding'][1]
    )
    close_btn.pack(pady=sizes['padding_md'])
    
    root.mainloop()


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Iniciando Prueba de Sistema Responsivo")
    print("="*60)
    test_responsive_system()
