"""
Script de prueba para verificar que los íconos se muestran correctamente
"""
import tkinter as tk
from PIL import Image, ImageTk
import os

def test_icons():
    """Probar que los íconos se muestran correctamente"""
    root = tk.Tk()
    root.title("Prueba de Íconos del Dashboard")
    root.geometry("800x600")
    root.configure(bg='#f1f5f9')
    
    # Lista de íconos
    icons = [
        ('cart.png', 'Nueva Venta', '#ea580c'),
        ('history.png', 'Historial', '#be123c'),
        ('box.png', 'Productos', '#2563eb'),
        ('folder.png', 'Categorías', '#dc2626'),
        ('chart.png', 'Stock', '#f59e0b'),
        ('users.png', 'Usuarios', '#8b5cf6'),
        ('lock.png', 'Roles', '#6366f1'),
        ('trending.png', 'Reportes', '#0ea5e9'),
    ]
    
    # Crear contenedor para las tarjetas
    container = tk.Frame(root, bg='#f1f5f9')
    container.pack(expand=True, fill='both', padx=20, pady=20)
    
    # Referencias de imágenes (importante para evitar garbage collection)
    icon_images = []
    
    # Crear una tarjeta de prueba para cada ícono
    for idx, (icon_file, title, color) in enumerate(icons):
        row = idx // 4
        col = idx % 4
        
        # Frame de la tarjeta
        card = tk.Frame(container, bg='#ffffff', width=150, height=120)
        card.grid(row=row, column=col, padx=10, pady=10)
        card.grid_propagate(False)
        
        # Canvas para dibujar
        canvas = tk.Canvas(card, bg=color, highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        
        # Círculo blanco de fondo
        canvas.create_oval(55, 20, 95, 60, fill='white', outline='')
        
        # Cargar y mostrar imagen
        icon_path = os.path.join('assets', 'images', icon_file)
        if os.path.exists(icon_path):
            try:
                img = Image.open(icon_path)
                img = img.resize((35, 35), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                icon_images.append(photo)  # Guardar referencia
                canvas.create_image(75, 40, image=photo, anchor='center')
                print(f"✓ Ícono cargado: {icon_file}")
            except Exception as e:
                print(f"✗ Error cargando {icon_file}: {e}")
                canvas.create_text(75, 40, text="❌", font=('Arial', 20), fill=color)
        else:
            print(f"✗ No existe: {icon_path}")
            canvas.create_text(75, 40, text="❌", font=('Arial', 20), fill=color)
        
        # Título
        canvas.create_text(75, 90, text=title, font=('Segoe UI', 10, 'bold'), 
                          fill='white', anchor='center')
    
    print(f"\n✓ Se cargaron {len(icon_images)} imágenes correctamente")
    print("Si ves los íconos en la ventana, entonces las imágenes están bien.")
    print("Si solo ves círculos blancos, hay un problema con las imágenes o las referencias.\n")
    
    root.mainloop()

if __name__ == '__main__':
    test_icons()
