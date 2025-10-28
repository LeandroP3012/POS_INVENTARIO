"""
Test simple para verificar trace_add en Checkbuttons
"""
import tkinter as tk
from tkinter import messagebox

def test_trace():
    """Probar trace_add con checkboxes"""
    root = tk.Tk()
    root.title("Test Trace en Checkboxes")
    root.geometry("500x300")
    
    # Diccionario para guardar variables
    vars_dict = {}
    
    # Crear 5 checkboxes de prueba
    for i in range(5):
        perm_name = f"permiso_{i+1}"
        
        # Variable
        var = tk.BooleanVar()
        var.set(False)
        vars_dict[perm_name] = var
        
        # Callback con trace
        def on_change(*args, name=perm_name):
            state = vars_dict[name].get()
            print(f"🔔 {name} cambió a: {state}")
        
        # Vincular trace
        var.trace_add('write', on_change)
        
        # Checkbox
        checkbox = tk.Checkbutton(
            root,
            text=f"Permiso {i+1}",
            variable=var,
            onvalue=True,
            offvalue=False,
            selectcolor='#4CAF50'
        )
        checkbox.pack(pady=5)
    
    # Botón para mostrar seleccionados
    def mostrar_seleccionados():
        selected = [name for name, var in vars_dict.items() if var.get()]
        print(f"\n📊 PERMISOS SELECCIONADOS: {len(selected)}/{len(vars_dict)}")
        for perm in selected:
            print(f"   ✓ {perm}")
        
        messagebox.showinfo("Resultado", f"Seleccionados: {len(selected)}/{len(vars_dict)}\n\n{', '.join(selected)}")
    
    tk.Button(
        root,
        text="💾 Mostrar Seleccionados",
        command=mostrar_seleccionados,
        bg='#27ae60',
        fg='white',
        font=('Arial', 12, 'bold'),
        padx=20,
        pady=10
    ).pack(pady=20)
    
    print("✅ Test iniciado - Marca algunos checkboxes y haz click en el botón")
    root.mainloop()

if __name__ == '__main__':
    test_trace()
