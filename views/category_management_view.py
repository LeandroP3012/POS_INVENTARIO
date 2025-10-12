"""
Vista de Gestión de Categorías
Interfaz para administrar categorías de productos
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, List, Callable, Optional


class CategoryManagementView:
    """Vista principal de gestión de categorías"""
    
    def __init__(self, parent, current_user: Dict[str, Any]):
        self.parent = parent
        self.current_user = current_user
        self.root = tk.Frame(parent, bg='#ecf0f1')
        self.root.pack(fill='both', expand=True)
        
        # Callbacks
        self.on_refresh_callback = None
        self.on_search_callback = None
        self.on_create_callback = None
        self.on_edit_callback = None
        self.on_delete_callback = None
        
        # Variables
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search_changed)
        
        # Crear interfaz
        self.create_widgets()
    
    def create_widgets(self):
        """Crear widgets de la interfaz"""
        # Header
        header = tk.Frame(self.root, bg='#2c3e50', height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg='#2c3e50')
        header_content.pack(fill='both', expand=True, padx=30)
        
        tk.Label(
            header_content,
            text="🏷️  Gestión de Categorías",
            font=('Segoe UI', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(side='left', pady=15)
        
        # Botón volver
        tk.Button(
            header_content,
            text="← Volver",
            command=self._on_back,
            font=('Segoe UI', 11),
            bg='#34495e',
            fg='white',
            activebackground='#2c3e50',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8
        ).pack(side='right', pady=15)
        
        # Toolbar
        toolbar = tk.Frame(self.root, bg='white', height=70)
        toolbar.pack(fill='x')
        toolbar.pack_propagate(False)
        
        toolbar_content = tk.Frame(toolbar, bg='white')
        toolbar_content.pack(fill='both', expand=True, padx=30, pady=15)
        
        # Búsqueda
        search_frame = tk.Frame(toolbar_content, bg='white')
        search_frame.pack(side='left', fill='x', expand=True)
        
        tk.Label(
            search_frame,
            text="🔍",
            font=('Segoe UI', 14),
            bg='white'
        ).pack(side='left', padx=(0, 10))
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 11),
            relief='solid',
            bd=1,
            width=40
        )
        search_entry.pack(side='left', fill='x', expand=True)
        search_entry.insert(0, "Buscar categoría...")
        search_entry.config(fg='#95a5a6')
        
        def on_focus_in(e):
            if search_entry.get() == "Buscar categoría...":
                search_entry.delete(0, tk.END)
                search_entry.config(fg='#2c3e50')
        
        def on_focus_out(e):
            if not search_entry.get():
                search_entry.insert(0, "Buscar categoría...")
                search_entry.config(fg='#95a5a6')
        
        search_entry.bind('<FocusIn>', on_focus_in)
        search_entry.bind('<FocusOut>', on_focus_out)
        
        # Botón Nueva Categoría
        tk.Button(
            toolbar_content,
            text="➕ Nueva Categoría",
            command=self._on_create_click,
            font=('Segoe UI', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=10
        ).pack(side='right', padx=(10, 0))
        
        # Contenido principal
        main_content = tk.Frame(self.root, bg='#ecf0f1')
        main_content.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Tabla de categorías
        self.create_table(main_content)
        
        # Footer con estadísticas
        self.create_footer()
    
    def create_table(self, parent):
        """Crear tabla de categorías"""
        # Frame de la tabla
        table_frame = tk.Frame(parent, bg='white', relief='solid', bd=1)
        table_frame.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview
        columns = ('ID', 'Nombre', 'Productos', 'Estado', 'Categoría Padre')
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set,
            selectmode='browse',
            height=15
        )
        
        # Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre de Categoría')
        self.tree.heading('Productos', text='Productos')
        self.tree.heading('Estado', text='Estado')
        self.tree.heading('Categoría Padre', text='Categoría Padre')
        
        self.tree.column('ID', width=60, anchor='center')
        self.tree.column('Nombre', width=300, anchor='w')
        self.tree.column('Productos', width=100, anchor='center')
        self.tree.column('Estado', width=100, anchor='center')
        self.tree.column('Categoría Padre', width=200, anchor='w')
        
        # Estilo para filas
        self.tree.tag_configure('active', background='#ffffff')
        self.tree.tag_configure('inactive', background='#ffebee')
        
        # Eventos
        self.tree.bind('<Double-Button-1>', lambda e: self._on_edit_click())
        self.tree.bind('<<TreeviewSelect>>', self._on_select)
        
        scrollbar.config(command=self.tree.yview)
        self.tree.pack(fill='both', expand=True)
        
        # Panel de acciones (derecha)
        actions_frame = tk.Frame(parent, bg='white', width=200, relief='solid', bd=1)
        actions_frame.pack(side='right', fill='y', padx=(20, 0))
        actions_frame.pack_propagate(False)
        
        tk.Label(
            actions_frame,
            text="⚙️ Acciones",
            font=('Segoe UI', 12, 'bold'),
            bg='#f8f9fa',
            fg='#2c3e50',
            pady=15
        ).pack(fill='x')
        
        self.edit_btn = tk.Button(
            actions_frame,
            text="✏️ Editar",
            command=self._on_edit_click,
            font=('Segoe UI', 10),
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            relief='flat',
            cursor='hand2',
            state='disabled',
            pady=10
        )
        self.edit_btn.pack(fill='x', padx=15, pady=5)
        
        self.delete_btn = tk.Button(
            actions_frame,
            text="🗑️ Eliminar",
            command=self._on_delete_click,
            font=('Segoe UI', 10),
            bg='#e74c3c',
            fg='white',
            activebackground='#c0392b',
            relief='flat',
            cursor='hand2',
            state='disabled',
            pady=10
        )
        self.delete_btn.pack(fill='x', padx=15, pady=5)
    
    def create_footer(self):
        """Crear footer con estadísticas"""
        footer = tk.Frame(self.root, bg='#34495e', height=50)
        footer.pack(fill='x', side='bottom')
        footer.pack_propagate(False)
        
        footer_content = tk.Frame(footer, bg='#34495e')
        footer_content.pack(fill='both', expand=True, padx=30)
        
        self.stats_label = tk.Label(
            footer_content,
            text="Total: 0 categorías",
            font=('Segoe UI', 10),
            bg='#34495e',
            fg='white'
        )
        self.stats_label.pack(side='left', pady=12)
    
    def load_categories(self, categories: List[Dict[str, Any]]):
        """Cargar categorías en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Cargar datos
        for category in categories:
            status_text = "✅ Activo" if category.get('status') == 'active' else "❌ Inactivo"
            parent_name = category.get('parent_name', '-')
            
            tag = 'active' if category.get('status') == 'active' else 'inactive'
            
            self.tree.insert('', 'end', values=(
                category.get('id', ''),
                category.get('name', ''),
                category.get('product_count', 0),
                status_text,
                parent_name
            ), tags=(tag,))
        
        # Actualizar estadísticas
        self.stats_label.config(text=f"Total: {len(categories)} categorías")
    
    def get_selected_category(self) -> Optional[Dict[str, Any]]:
        """Obtener categoría seleccionada"""
        selection = self.tree.selection()
        if not selection:
            return None
        
        item = self.tree.item(selection[0])
        values = item['values']
        
        return {
            'id': values[0],
            'name': values[1],
            'product_count': values[2]
        }
    
    def _on_select(self, event):
        """Manejar selección de categoría"""
        if self.tree.selection():
            self.edit_btn.config(state='normal')
            self.delete_btn.config(state='normal')
        else:
            self.edit_btn.config(state='disabled')
            self.delete_btn.config(state='disabled')
    
    def _on_search_changed(self, *args):
        """Manejar cambio en búsqueda"""
        search_text = self.search_var.get()
        if search_text and search_text != "Buscar categoría..." and self.on_search_callback:
            self.on_search_callback(search_text)
        elif self.on_refresh_callback:
            self.on_refresh_callback()
    
    def _on_create_click(self):
        """Manejar clic en crear"""
        if self.on_create_callback:
            self.on_create_callback()
    
    def _on_edit_click(self):
        """Manejar clic en editar"""
        if self.on_edit_callback:
            category = self.get_selected_category()
            if category:
                self.on_edit_callback(category['id'])
    
    def _on_delete_click(self):
        """Manejar clic en eliminar"""
        if self.on_delete_callback:
            category = self.get_selected_category()
            if category:
                if messagebox.askyesno(
                    "Confirmar eliminación",
                    f"¿Estás seguro de que deseas eliminar la categoría '{category['name']}'?",
                    parent=self.root
                ):
                    self.on_delete_callback(category['id'])
    
    def _on_back(self):
        """Volver al dashboard"""
        if hasattr(self, 'on_back_callback') and self.on_back_callback:
            self.on_back_callback()
        else:
            # Limpiar la vista actual
            for widget in self.root.winfo_children():
                widget.destroy()
    
    def register_callbacks(self, refresh, search, create, edit, delete, back=None):
        """Registrar callbacks"""
        self.on_refresh_callback = refresh
        self.on_search_callback = search
        self.on_create_callback = create
        self.on_edit_callback = edit
        self.on_delete_callback = delete
        self.on_back_callback = back
