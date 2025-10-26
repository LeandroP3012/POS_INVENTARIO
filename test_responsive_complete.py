"""
Script de prueba para verificar el sistema responsivo
Muestra cómo el sistema detecta la pantalla y aplica configuraciones
"""

import tkinter as tk
from tkinter import ttk
from utils.responsive_utils import ResponsiveManager


def test_responsive_system():
    """Probar sistema responsivo completo"""
    
    # Crear ventana de prueba
    root = tk.Tk()
    root.title("Test Sistema Responsivo - POS")
    
    # Inicializar gestor responsivo
    responsive = ResponsiveManager(root)
    
    # Hacer ventana responsiva
    responsive.make_window_responsive(root)
    
    # Crear frame principal con grid responsivo
    main_frame = tk.Frame(root, bg='white')
    main_frame.pack(fill='both', expand=True)
    
    # Aplicar grid weights
    responsive.apply_grid_weights(main_frame, 'header_content_footer')
    
    # === HEADER ===
    header = tk.Frame(main_frame, bg='#2c3e50', height=80)
    header.grid(row=0, column=0, sticky='ew')
    header.grid_propagate(False)
    
    title_font = responsive.get_font('title', bold=True)
    tk.Label(
        header,
        text=f"🖥️ Sistema Responsivo - {responsive.screen_type.upper()}",
        font=title_font,
        bg='#2c3e50',
        fg='white',
        pady=responsive.get_padding('large')
    ).pack()
    
    # === CONTENIDO ===
    content = tk.Frame(main_frame, bg='#ecf0f1')
    content.grid(row=1, column=0, sticky='nsew')
    
    # Configurar grid del contenido
    content.columnconfigure(0, weight=1)
    content.rowconfigure(0, weight=0)
    content.rowconfigure(1, weight=1)
    
    # Panel de información
    info_frame = tk.Frame(content, bg='white', relief='solid', bd=1)
    info_frame.grid(row=0, column=0, sticky='ew', 
                    padx=responsive.get_padding('large'),
                    pady=responsive.get_padding('large'))
    
    header_font = responsive.get_font('header', bold=True)
    body_font = responsive.get_font('body')
    
    tk.Label(
        info_frame,
        text="📊 Información de Pantalla Detectada",
        font=header_font,
        bg='white',
        fg='#2c3e50'
    ).pack(pady=responsive.get_padding('medium'))
    
    # Mostrar información
    info_items = [
        f"Tipo de Pantalla: {responsive.screen_type}",
        f"Resolución: {responsive.screen_width}x{responsive.screen_height}",
        f"Tamaño Ventana: {responsive.config['window_width']}x{responsive.config['window_height']}",
        f"Fuente Base: {responsive.config['font_size_base']}px",
        f"Fuente Título: {responsive.config['font_size_title']}px",
        f"Fuente Header: {responsive.config['font_size_header']}px",
        f"Fuente Body: {responsive.config['font_size_body']}px",
        f"Padding Large: {responsive.config['padding_large']}px",
        f"Padding Medium: {responsive.config['padding_medium']}px",
        f"Altura Botón: {responsive.config['button_height']}px",
        f"Altura Toolbar: {responsive.config['toolbar_height']}px",
        f"Modo Compacto: {'✅ Sí' if responsive.is_compact_mode() else '❌ No'}"
    ]
    
    for item in info_items:
        tk.Label(
            info_frame,
            text=f"• {item}",
            font=body_font,
            bg='white',
            fg='#34495e',
            anchor='w'
        ).pack(fill='x', padx=responsive.get_padding('large'), pady=2)
    
    # Tabla de ejemplo con estilo responsivo
    table_frame = tk.Frame(content, bg='white', relief='solid', bd=1)
    table_frame.grid(row=1, column=0, sticky='nsew',
                     padx=responsive.get_padding('large'),
                     pady=responsive.get_padding('large'))
    
    tk.Label(
        table_frame,
        text="📋 Tabla de Ejemplo",
        font=header_font,
        bg='white',
        fg='#2c3e50'
    ).pack(pady=responsive.get_padding('medium'))
    
    # Configurar estilo de Treeview
    style = ttk.Style()
    responsive.configure_treeview_style(style)
    
    # Crear Treeview
    columns = ('Columna 1', 'Columna 2', 'Columna 3')
    tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    
    # Datos de ejemplo
    for i in range(10):
        tree.insert('', 'end', values=(f'Dato {i+1}', f'Valor {i+1}', f'Info {i+1}'))
    
    tree.pack(fill='both', expand=True, 
              padx=responsive.get_padding('medium'),
              pady=responsive.get_padding('medium'))
    
    # === FOOTER ===
    footer = tk.Frame(main_frame, bg='#34495e', height=60)
    footer.grid(row=2, column=0, sticky='ew')
    footer.grid_propagate(False)
    
    button_font = responsive.get_font('body', bold=True)
    
    tk.Button(
        footer,
        text="✅ Aceptar",
        font=button_font,
        bg='#27ae60',
        fg='white',
        relief='flat',
        cursor='hand2',
        padx=responsive.get_padding('large'),
        command=root.quit
    ).pack(side='right', padx=responsive.get_padding('large'), pady=responsive.get_padding('medium'))
    
    tk.Button(
        footer,
        text="❌ Cancelar",
        font=button_font,
        bg='#e74c3c',
        fg='white',
        relief='flat',
        cursor='hand2',
        padx=responsive.get_padding('large'),
        command=root.quit
    ).pack(side='right', padx=responsive.get_padding('small'), pady=responsive.get_padding('medium'))
    
    # Mostrar información en consola
    print("\n" + "="*60)
    print("🖥️  SISTEMA RESPONSIVO INICIALIZADO")
    print("="*60)
    print(f"Pantalla detectada: {responsive.screen_width}x{responsive.screen_height}")
    print(f"Tipo: {responsive.screen_type.upper()}")
    print(f"Ventana óptima: {responsive.config['window_width']}x{responsive.config['window_height']}")
    print(f"Modo compacto: {'✅ Activado' if responsive.is_compact_mode() else '❌ Desactivado'}")
    print("="*60 + "\n")
    
    # Iniciar aplicación
    root.mainloop()


if __name__ == "__main__":
    test_responsive_system()
