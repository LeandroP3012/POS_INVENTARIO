#!/usr/bin/env python3
"""
Debug para encontrar el problema con el logo
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import tkinter as tk
from views.login_view import LoginView

def debug_widgets(parent, level=0):
    """Mostrar todos los widgets recursivamente"""
    indent = "  " * level
    try:
        widget_info = f"{parent.__class__.__name__}"
        if isinstance(parent, tk.Label) and hasattr(parent, 'cget'):
            try:
                text = parent.cget('text')
                if text:
                    widget_info += f" (text='{text[:20]}...')"
            except:
                pass
        print(f"{indent}{widget_info}")
        
        for child in parent.winfo_children():
            debug_widgets(child, level + 1)
    except Exception as e:
        print(f"{indent}Error: {e}")

def test_debug():
    """Debug de widgets"""
    print("🔍 Debug de widgets...")
    
    # Crear login view
    login_view = LoginView()
    
    def delayed_debug():
        print("\n🌳 Estructura de widgets:")
        debug_widgets(login_view.root)
        
        print("\n🔍 Buscando labels con emoji...")
        def find_emoji_labels(parent):
            try:
                for child in parent.winfo_children():
                    if isinstance(child, tk.Label) and hasattr(child, 'cget'):
                        try:
                            text = child.cget('text')
                            if "🏪" in text or "IPV" in text:
                                print(f"  ✅ Encontrado: {child} - text='{text}'")
                        except:
                            pass
                    find_emoji_labels(child)
            except:
                pass
        
        find_emoji_labels(login_view.root)
        
        # Cerrar después de 2 segundos
        login_view.root.after(2000, login_view.root.quit)
    
    # Programar debug después de que la interfaz esté lista
    login_view.root.after(500, delayed_debug)
    
    print("👀 Mostrando login para debug...")
    login_view.run()

if __name__ == "__main__":
    test_debug()
