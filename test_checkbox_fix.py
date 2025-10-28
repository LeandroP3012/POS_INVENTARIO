"""
Script de prueba para verificar el problema de los checkboxes
Este script crea un diálogo simple con checkboxes para identificar el problema
"""
import tkinter as tk
from tkinter import messagebox

def test_checkboxes():
    """Prueba simple de checkboxes con BooleanVar"""
    
    root = tk.Tk()
    root.title("Test de Checkboxes")
    root.geometry("600x400")
    
    # Diccionario para almacenar variables
    vars_dict = {}
    
    # Crear diálogo
    dialog = tk.Toplevel(root)
    dialog.title("Test Checkboxes")
    dialog.geometry("500x300")
    
    print("\n" + "="*60)
    print("CREANDO CHECKBOXES...")
    print("="*60)
    
    # Crear 10 checkboxes
    for i in range(10):
        perm_name = f"permiso_{i+1}"
        
        # OPCIÓN 1: SIN master (puede fallar)
        # var = tk.BooleanVar()
        
        # OPCIÓN 2: CON master (debería funcionar)
        var = tk.BooleanVar(master=dialog)
        
        var.set(False)
        vars_dict[perm_name] = var
        
        print(f"✓ Variable creada: {perm_name} = {var.get()}")
        
        # Crear checkbox
        checkbox = tk.Checkbutton(
            dialog,
            text=f"Permiso {i+1}",
            variable=var,
            onvalue=True,
            offvalue=False,
            selectcolor='#4CAF50',
            command=lambda p=perm_name: print(f"🔔 CLICK: {p} = {vars_dict[p].get()}")
        )
        checkbox.pack(pady=5, anchor='w', padx=20)
    
    # Botón para mostrar seleccionados
    def show_selected():
        print("\n" + "="*60)
        print("VERIFICANDO ESTADO DE VARIABLES:")
        print("="*60)
        
        selected = []
        for perm_name, var in vars_dict.items():
            state = var.get()
            print(f"   {perm_name}: {state}")
            if state:
                selected.append(perm_name)
        
        print(f"\n📊 TOTAL SELECCIONADOS: {len(selected)}/{len(vars_dict)}")
        
        if selected:
            print("✅ Permisos seleccionados:")
            for p in selected:
                print(f"   - {p}")
            messagebox.showinfo("Resultado", f"Seleccionados: {len(selected)}\n\n" + "\n".join(selected))
        else:
            print("❌ NO HAY PERMISOS SELECCIONADOS")
            messagebox.showwarning("Resultado", "No hay permisos seleccionados")
    
    tk.Button(
        dialog,
        text="💾 Verificar Seleccionados",
        command=show_selected,
        bg='#27ae60',
        fg='white',
        font=('Arial', 12, 'bold'),
        padx=20,
        pady=10
    ).pack(pady=20)
    
    print("\n✅ Test iniciado")
    print("📌 Marca algunos checkboxes y haz clic en 'Verificar Seleccionados'")
    print("="*60 + "\n")
    
    root.mainloop()

if __name__ == '__main__':
    test_checkboxes()
