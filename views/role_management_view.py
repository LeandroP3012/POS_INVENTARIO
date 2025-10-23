"""
Vista para gestión de roles y permisos
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, Any, Optional, List, Callable
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from views.base_view import BaseView
from controllers.role_controller import RoleController

class RoleManagementView(BaseView):
    """Vista para gestión de roles y permisos"""
    
    def __init__(self, parent, current_user: Dict[str, Any], embedded: bool = False):
        self.parent = parent
        self.current_user = current_user
        self.embedded = embedded
        super().__init__(parent)
        self.role_controller = RoleController()
        
        # Variables de la vista
        self.search_var = tk.StringVar()
        self.filter_active_var = tk.StringVar(value="todos")
        self.filter_type_var = tk.StringVar(value="todos")
        
        # Callbacks
        self.callbacks = {}
        
        # Crear interfaz
        self.create_interface()
        
        # Cargar datos iniciales
        self.refresh_roles()
    
    def create_interface(self):
        """Crear la interfaz de usuario"""
        # Configurar fondo principal
        if self.embedded:
            self.root.configure(bg='#f8f9fa')
        
        # Header
        self.create_header()
        
        # Navbar
        self.create_navbar()
        
        # Toolbar con búsqueda y botones
        self.create_toolbar()
        
        # Panel principal con tabla
        self.create_main_panel()
        
        # Footer con estadísticas
        self.create_footer()
    
    def create_header(self):
        """Crear header de gestión de roles"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        content_frame = tk.Frame(header_frame, bg='#2c3e50')
        content_frame.pack(expand=True, fill='both', padx=30, pady=15)
        
        # Título (izquierda)
        title_label = tk.Label(
            content_frame,
            text="🔐 Gestión de Roles y Permisos",
            font=('Segoe UI', 24, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(side='left')
        
        # Botón de volver (derecha) - solo en modo embebido
        if self.embedded:
            back_button = tk.Button(
                content_frame,
                text="⬅️ Volver al Dashboard",
                command=self._back_to_dashboard,
                bg='#34495e',
                fg='white',
                font=('Segoe UI', 10, 'bold'),
                relief='flat',
                cursor='hand2',
                padx=15,
                pady=8
            )
            back_button.pack(side='right', padx=10)
        
        # Usuario actual (derecha, antes del botón)
        user_text = f"Usuario: {self.current_user.get('full_name', self.current_user.get('username', 'Admin'))}"
        user_label = tk.Label(
            content_frame,
            text=user_text,
            font=('Segoe UI', 14),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        user_label.pack(side='right')
    
    def create_navbar(self):
        """Crear navbar personalizado - GLOBAL para todos los módulos"""
        navbar_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        navbar_frame.pack(fill='x')
        navbar_frame.pack_propagate(False)
        
        # Estilo de botones
        btn_style = {
            'font': ('Segoe UI', 12, 'bold'),
            'bg': '#2c3e50',
            'fg': 'white',
            'activebackground': '#34495e',
            'activeforeground': 'white',
            'relief': 'flat',
            'bd': 0,
            'padx': 20,
            'pady': 10,
            'cursor': 'hand2'
        }
        
        # Contenedor de botones
        buttons_container = tk.Frame(navbar_frame, bg='#2c3e50')
        buttons_container.pack(side='left', padx=10, pady=5)
        
        # Botón Archivo
        file_btn = tk.Menubutton(buttons_container, text="📁 Archivo", **btn_style)
        file_btn.pack(side='left', padx=2)
        file_menu = tk.Menu(file_btn, tearoff=0, font=('Segoe UI', 11))
        file_btn.config(menu=file_menu)
        file_menu.add_command(label="Nueva Venta", command=self.callbacks.get('new_sale', lambda: None))
        file_menu.add_separator()
        if self.embedded:
            file_menu.add_command(label="Volver al Dashboard", command=self._back_to_dashboard)
        
        # Botón Ventas
        sales_btn = tk.Menubutton(buttons_container, text="💰 Ventas", **btn_style)
        sales_btn.pack(side='left', padx=2)
        sales_menu = tk.Menu(sales_btn, tearoff=0, font=('Segoe UI', 11))
        sales_btn.config(menu=sales_menu)
        sales_menu.add_command(label="Nueva Venta", command=self.callbacks.get('new_sale', lambda: None))
        sales_menu.add_command(label="Historial de Ventas", command=self.callbacks.get('sales_history', lambda: None))
        
        # Botón Inventario
        inv_btn = tk.Menubutton(buttons_container, text="📦 Inventario", **btn_style)
        inv_btn.pack(side='left', padx=2)
        inv_menu = tk.Menu(inv_btn, tearoff=0, font=('Segoe UI', 11))
        inv_btn.config(menu=inv_menu)
        inv_menu.add_command(label="Ver Productos", command=self.callbacks.get('view_products', lambda: None))
        inv_menu.add_command(label="Gestionar Categorías", command=self.callbacks.get('view_categories', lambda: None))
        inv_menu.add_command(label="Control de Stock", command=self.callbacks.get('stock_control', lambda: None))
        
        # Botón Reportes
        rep_btn = tk.Menubutton(buttons_container, text="📊 Reportes", **btn_style)
        rep_btn.pack(side='left', padx=2)
        rep_menu = tk.Menu(rep_btn, tearoff=0, font=('Segoe UI', 11))
        rep_btn.config(menu=rep_menu)
        rep_menu.add_command(label="Ventas del Día", command=self.callbacks.get('daily_report', lambda: None))
        rep_menu.add_command(label="Reporte Completo", command=self.callbacks.get('full_report', lambda: None))
        
        # Botón Administración
        admin_btn = tk.Menubutton(buttons_container, text="⚙️ Administración", **btn_style)
        admin_btn.pack(side='left', padx=2)
        admin_menu = tk.Menu(admin_btn, tearoff=0, font=('Segoe UI', 11))
        admin_btn.config(menu=admin_menu)
        admin_menu.add_command(label="Gestionar Usuarios", command=self.callbacks.get('manage_users', lambda: None))
        admin_menu.add_command(label="Gestionar Roles", command=self.refresh_roles)
        admin_menu.add_separator()
        admin_menu.add_command(label="Configuración", command=self.callbacks.get('system_config', lambda: None))
        
        # Botón Ayuda
        help_btn = tk.Menubutton(buttons_container, text="❓ Ayuda", **btn_style)
        help_btn.pack(side='left', padx=2)
        help_menu = tk.Menu(help_btn, tearoff=0, font=('Segoe UI', 11))
        help_btn.config(menu=help_menu)
        help_menu.add_command(label="Manual de Usuario", command=self.callbacks.get('show_manual', lambda: None))
        help_menu.add_command(label="Acerca de", command=self.callbacks.get('show_about', lambda: None))
    
    def create_toolbar(self):
        """Crear toolbar con búsqueda y botones de acción"""
        toolbar_frame = tk.Frame(self.root, bg='white', height=90)
        toolbar_frame.pack(fill='x', padx=25, pady=(25, 0))
        toolbar_frame.pack_propagate(False)
        
        # Frame interno con padding
        inner_frame = tk.Frame(toolbar_frame, bg='white')
        inner_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Frame izquierdo - Búsqueda
        search_frame = tk.Frame(inner_frame, bg='white')
        search_frame.pack(side='left', fill='y')
        
        tk.Label(
            search_frame,
            text="� Buscar rol:",
            font=('Segoe UI', 13, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left', padx=(0, 10))
        
        self.search_var.trace_add('write', lambda *args: self.search_roles())
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 13),
            width=28,
            relief='solid',
            bd=1
        )
        search_entry.pack(side='left', padx=(0, 15), ipady=8)
        
        # Filtro por estado
        tk.Label(
            search_frame,
            text="Estado:",
            font=('Segoe UI', 13, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left', padx=(25, 8))
        
        status_combo = ttk.Combobox(
            search_frame,
            textvariable=self.filter_active_var,
            values=['todos', 'activos', 'inactivos'],
            state='readonly',
            width=18,
            font=('Segoe UI', 12)
        )
        status_combo.pack(side='left', padx=(0, 15))
        status_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        # Filtro por tipo
        tk.Label(
            search_frame,
            text="Tipo:",
            font=('Segoe UI', 13, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left', padx=(15, 8))
        
        type_combo = ttk.Combobox(
            search_frame,
            textvariable=self.filter_type_var,
            values=['todos', 'sistema', 'personalizados'],
            state='readonly',
            width=18,
            font=('Segoe UI', 12)
        )
        type_combo.pack(side='left', padx=(0, 15))
        type_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        # Frame derecho - Botones de acción
        buttons_frame = tk.Frame(inner_frame, bg='white')
        buttons_frame.pack(side='right', fill='y')
        
        # Botón nuevo rol
        new_role_btn = tk.Button(
            buttons_frame,
            text="➕ Nuevo Rol",
            command=self.create_role,
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', 13, 'bold'),
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=12
        )
        new_role_btn.pack(side='left', padx=(0, 12))
        
        # Botón editar
        self.edit_role_btn = tk.Button(
            buttons_frame,
            text="✏️ Editar",
            command=self.edit_role,
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 13, 'bold'),
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=12,
            state='disabled'
        )
        self.edit_role_btn.pack(side='left', padx=(0, 12))
        
        # Botón eliminar
        self.delete_role_btn = tk.Button(
            buttons_frame,
            text="🗑️ Eliminar",
            command=self.delete_role,
            bg='#e74c3c',
            fg='white',
            font=('Segoe UI', 13, 'bold'),
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=12,
            state='disabled'
        )
        self.delete_role_btn.pack(side='left', padx=(0, 12))
        
        # Botón permisos
        self.permissions_btn = tk.Button(
            buttons_frame,
            text="🔓 Permisos",
            command=self.manage_permissions,
            bg='#9b59b6',
            fg='white',
            font=('Segoe UI', 13, 'bold'),
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=12,
            state='disabled'
        )
        self.permissions_btn.pack(side='left')
    
    def create_main_panel(self):
        """Crear panel principal con tabla de roles"""
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=25, pady=25)
        
        # Frame para la tabla
        table_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=1)
        table_frame.pack(fill='both', expand=True)
        
        # Título de la tabla
        table_header = tk.Frame(table_frame, bg='#34495e', height=50)
        table_header.pack(fill='x')
        table_header.pack_propagate(False)
        
        tk.Label(
            table_header,
            text="📋 Lista de Roles del Sistema",
            font=('Segoe UI', 16, 'bold'),
            fg='white',
            bg='#34495e'
        ).pack(side='left', padx=25, pady=15)
        
        # Contador de roles
        self.role_count_label = tk.Label(
            table_header,
            text="0 roles",
            font=('Segoe UI', 13),
            fg='#bdc3c7',
            bg='#34495e'
        )
        self.role_count_label.pack(side='right', padx=25, pady=15)
        
        # Crear Treeview para la tabla
        self.create_roles_table(table_frame)
    
    def create_roles_table(self, parent):
        """Crear tabla de roles con Treeview"""
        # Frame para tabla y scrollbars
        tree_frame = tk.Frame(parent, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Configurar columnas
        columns = ('id', 'name', 'code', 'description', 'type', 'status', 'users_count', 'permissions_count')
        column_names = {
            'id': 'ID',
            'name': 'Nombre',
            'code': 'Código',
            'description': 'Descripción',
            'type': 'Tipo',
            'status': 'Estado',
            'users_count': 'Usuarios',
            'permissions_count': 'Permisos'
        }
        
        # Crear Treeview
        self.roles_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='tree headings',
            height=18
        )
        
        # Configurar columnas
        self.roles_tree.column('#0', width=0, stretch=False)  # Ocultar primera columna
        self.roles_tree.column('id', width=60, anchor='center')
        self.roles_tree.column('name', width=180, anchor='w')
        self.roles_tree.column('code', width=140, anchor='w')
        self.roles_tree.column('description', width=300, anchor='w')
        self.roles_tree.column('type', width=120, anchor='center')
        self.roles_tree.column('status', width=100, anchor='center')
        self.roles_tree.column('users_count', width=100, anchor='center')
        self.roles_tree.column('permissions_count', width=100, anchor='center')
        
        # Configurar headers
        for col in columns:
            self.roles_tree.heading(col, text=column_names[col], anchor='center')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.roles_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.roles_tree.xview)
        
        self.roles_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars y tree
        self.roles_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind eventos
        self.roles_tree.bind('<<TreeviewSelect>>', self.on_role_select)
        self.roles_tree.bind('<Double-Button-1>', lambda e: self.edit_role())
        
        # Configurar estilo para filas alternadas
        style = ttk.Style()
        style.configure('Treeview', rowheight=30, font=('Segoe UI', 11))
        style.configure('Treeview.Heading', font=('Segoe UI', 12, 'bold'))
    
    def create_footer(self):
        """Crear footer con estadísticas"""
        footer_frame = tk.Frame(self.root, bg='#ecf0f1', height=60)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        # Contenedor interno
        content_frame = tk.Frame(footer_frame, bg='#ecf0f1')
        content_frame.pack(fill='both', expand=True, padx=30, pady=15)
        
        # Estadísticas
        self.stats_labels = {}
        
        stats_data = [
            ('total_roles', 'Total de Roles', '#3498db'),
            ('active_roles', 'Activos', '#27ae60'),
            ('system_roles', 'Sistema', '#9b59b6'),
            ('custom_roles', 'Personalizados', '#e67e22')
        ]
        
        for key, label_text, color in stats_data:
            stat_frame = tk.Frame(content_frame, bg='#ecf0f1')
            stat_frame.pack(side='left', padx=20)
            
            value_label = tk.Label(
                stat_frame,
                text='0',
                font=('Segoe UI', 18, 'bold'),
                fg=color,
                bg='#ecf0f1'
            )
            value_label.pack(side='left', padx=(0, 8))
            
            desc_label = tk.Label(
                stat_frame,
                text=label_text,
                font=('Segoe UI', 13),
                fg='#7f8c8d',
                bg='#ecf0f1'
            )
            desc_label.pack(side='left')
            
            self.stats_labels[key] = value_label
    
    def on_role_select(self, event):
        """Manejar selección de rol"""
        selection = self.roles_tree.selection()
        if selection:
            self.selected_role = selection[0]
            # Habilitar botones de acción
            self.edit_role_btn.config(state='normal')
            self.delete_role_btn.config(state='normal')
            self.permissions_btn.config(state='normal')
        else:
            self.selected_role = None
            # Deshabilitar botones de acción
            self.edit_role_btn.config(state='disabled')
            self.delete_role_btn.config(state='disabled')
            self.permissions_btn.config(state='disabled')
    
    def create_search_frame(self, parent):
        """Este método ya no se usa - la búsqueda está en el toolbar"""
        pass
    
    def create_action_buttons_frame(self, parent):
        """Este método ya no se usa - los botones están en el toolbar"""
        pass
    
    def create_roles_table_frame(self, parent):
        """Este método ya no se usa - la tabla está en create_main_panel"""
        pass
    
    def refresh_roles(self):
        """Actualizar lista de roles"""
        try:
            # Limpiar tabla
            for item in self.roles_tree.get_children():
                self.roles_tree.delete(item)
            
            # Obtener roles
            roles = self.role_controller.get_all_roles(include_inactive=True)
            
            # Llenar tabla
            for role in roles:
                # Preparar valores
                role_id = role.get('id', '')
                name = role.get('name', '')
                code = role.get('code', '')
                description = role.get('description', '')[:50] + '...' if len(role.get('description', '')) > 50 else role.get('description', '')
                role_type = "Sistema" if role.get('system_role', False) else "Personalizado"
                status = "✅ Activo" if role.get('active', True) else "❌ Inactivo"
                users_count = role.get('users_count', 0)
                permissions_count = len(role.get('permissions', []))
                
                # Insertar en tabla
                self.roles_tree.insert('', tk.END, values=(
                    role_id, name, code, description, role_type, status, users_count, permissions_count
                ))
            
            # Actualizar contador de roles
            total_count = len(roles)
            self.role_count_label.config(text=f"{total_count} rol{'es' if total_count != 1 else ''}")
            
            # Actualizar estadísticas del footer
            self.update_stats()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error actualizando roles:\n{str(e)}")
    
    def update_stats(self):
        """Actualizar estadísticas"""
        try:
            stats = self.role_controller.get_roles_stats()
            
            self.stats_labels['total_roles'].config(text=str(stats.get('total_roles', 0)))
            self.stats_labels['active_roles'].config(text=str(stats.get('active_roles', 0)))
            self.stats_labels['system_roles'].config(text=str(stats.get('system_roles', 0)))
            self.stats_labels['custom_roles'].config(text=str(stats.get('custom_roles', 0)))
            
        except Exception as e:
            print(f"Error actualizando estadísticas: {e}")
    
    def search_roles(self):
        """Buscar roles"""
        try:
            query = self.search_var.get().strip()
            filters = self.get_current_filters()
            
            # Limpiar tabla
            for item in self.roles_tree.get_children():
                self.roles_tree.delete(item)
            
            # Buscar roles
            roles = self.role_controller.search_roles(query, filters)
            
            # Llenar tabla con resultados
            for role in roles:
                role_id = role.get('id', '')
                name = role.get('name', '')
                code = role.get('code', '')
                description = role.get('description', '')[:50] + '...' if len(role.get('description', '')) > 50 else role.get('description', '')
                role_type = "Sistema" if role.get('system_role', False) else "Personalizado"
                status = "✅ Activo" if role.get('active', True) else "❌ Inactivo"
                users_count = role.get('users_count', 0)
                permissions_count = len(role.get('permissions', []))
                
                self.roles_tree.insert('', tk.END, values=(
                    role_id, name, code, description, role_type, status, users_count, permissions_count
                ))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en búsqueda:\n{str(e)}")
    
    def get_current_filters(self) -> Dict[str, Any]:
        """Obtener filtros actuales"""
        filters = {}
        
        # Filtro por estado
        active_filter = self.filter_active_var.get()
        if active_filter == "activos":
            filters['active'] = True
        elif active_filter == "inactivos":
            filters['active'] = False
        
        # Filtro por tipo
        type_filter = self.filter_type_var.get()
        if type_filter == "sistema":
            filters['system_role'] = True
        elif type_filter == "personalizados":
            filters['system_role'] = False
        
        return filters
    
    def apply_filters(self):
        """Aplicar filtros"""
        self.search_roles()
    
    def clear_search(self):
        """Limpiar búsqueda"""
        self.search_var.set("")
        self.filter_active_var.set("todos")
        self.filter_type_var.set("todos")
        self.refresh_roles()
    
    def create_role(self):
        """Crear nuevo rol"""
        try:
            print("DEBUG CREATE_ROLE VIEW - Abriendo diálogo...")
            dialog = RoleDialog(self.root, title="Crear Nuevo Rol", 
                               role_controller=self.role_controller)
            
            # Esperar a que el diálogo termine completamente
            self.root.wait_window(dialog.dialog)
            
            print(f"DEBUG CREATE_ROLE VIEW - Diálogo cerrado, result: {dialog.result}")
            
            if dialog.result:
                print("DEBUG CREATE_ROLE VIEW - Llamando al controlador...")
                success, message, role_id = self.role_controller.create_role(
                    dialog.result, self.current_user
                )
                
                print(f"DEBUG CREATE_ROLE VIEW - Resultado: success={success}, message={message}, role_id={role_id}")
                
                if success:
                    messagebox.showinfo("Éxito", message)
                    self.refresh_roles()
                else:
                    messagebox.showerror("Error", message)
            else:
                print("DEBUG CREATE_ROLE VIEW - dialog.result es None/False, no se ejecuta el controlador")
                    
        except Exception as e:
            print(f"DEBUG CREATE_ROLE VIEW - Excepción: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error creando rol:\n{str(e)}")
    
    def edit_role(self):
        """Editar rol seleccionado"""
        try:
            selected = self.roles_tree.selection()
            if not selected:
                messagebox.showwarning("Selección", "Selecciona un rol para editar")
                return
            
            # Obtener datos del rol seleccionado
            item = selected[0]
            role_id = int(self.roles_tree.item(item)['values'][0])
            
            # Obtener rol completo
            role = self.role_controller.get_role_by_id(role_id)
            if not role:
                messagebox.showerror("Error", "Rol no encontrado")
                return
            
            # Verificar si se puede editar
            if not role.get('can_edit', True):
                messagebox.showwarning("Restricción", "Este rol del sistema no se puede editar")
                return
            
            # Mostrar diálogo de edición
            dialog = RoleDialog(self.root, title="Editar Rol", 
                               role_controller=self.role_controller, role_data=role)
            
            if dialog.result:
                success, message = self.role_controller.update_role(
                    role_id, dialog.result, self.current_user
                )
                
                if success:
                    messagebox.showinfo("Éxito", message)
                    self.refresh_roles()
                else:
                    messagebox.showerror("Error", message)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error editando rol:\n{str(e)}")
    
    def delete_role(self):
        """Eliminar rol seleccionado"""
        try:
            selected = self.roles_tree.selection()
            if not selected:
                messagebox.showwarning("Selección", "Selecciona un rol para eliminar")
                return
            
            # Obtener datos del rol seleccionado
            item = selected[0]
            values = self.roles_tree.item(item)['values']
            role_id = int(values[0])
            role_name = values[1]
            
            # Confirmar eliminación
            if not messagebox.askyesno("Confirmar", 
                                      f"¿Estás seguro de eliminar el rol '{role_name}'?\n\n"
                                      "Esta acción no se puede deshacer."):
                return
            
            # Eliminar rol
            success, message = self.role_controller.delete_role(role_id, self.current_user)
            
            if success:
                messagebox.showinfo("Éxito", message)
                self.refresh_roles()
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error eliminando rol:\n{str(e)}")
    
    def activate_role(self):
        """Activar rol seleccionado"""
        try:
            selected = self.roles_tree.selection()
            if not selected:
                messagebox.showwarning("Selección", "Selecciona un rol para activar")
                return
            
            item = selected[0]
            role_id = int(self.roles_tree.item(item)['values'][0])
            
            success, message = self.role_controller.activate_role(role_id, self.current_user)
            
            if success:
                messagebox.showinfo("Éxito", message)
                self.refresh_roles()
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error activando rol:\n{str(e)}")
    
    def deactivate_role(self):
        """Desactivar rol seleccionado"""
        try:
            selected = self.roles_tree.selection()
            if not selected:
                messagebox.showwarning("Selección", "Selecciona un rol para desactivar")
                return
            
            item = selected[0]
            values = self.roles_tree.item(item)['values']
            role_id = int(values[0])
            role_name = values[1]
            
            # Confirmar desactivación
            if not messagebox.askyesno("Confirmar", 
                                      f"¿Desactivar el rol '{role_name}'?\n\n"
                                      "Los usuarios con este rol no podrán acceder al sistema."):
                return
            
            success, message = self.role_controller.deactivate_role(role_id, self.current_user)
            
            if success:
                messagebox.showinfo("Éxito", message)
                self.refresh_roles()
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error desactivando rol:\n{str(e)}")
    
    def manage_permissions(self):
        """Gestionar permisos del rol seleccionado"""
        try:
            print("DEBUG MANAGE_PERMISOS - Iniciando gestión de permisos...")
            
            selected = self.roles_tree.selection()
            if not selected:
                messagebox.showwarning("Selección", "Selecciona un rol para gestionar permisos")
                return
            
            item = selected[0]
            role_id = int(self.roles_tree.item(item)['values'][0])
            print(f"DEBUG MANAGE_PERMISOS - Role ID seleccionado: {role_id}")
            
            # Obtener rol completo
            role = self.role_controller.get_role_by_id(role_id)
            if not role:
                messagebox.showerror("Error", "Rol no encontrado")
                return
            
            print(f"DEBUG MANAGE_PERMISOS - Rol obtenido: {role['name']}")
            
            # Mostrar diálogo de permisos
            print("DEBUG MANAGE_PERMISOS - Abriendo diálogo de permisos...")
            dialog = PermissionsDialog(self.root, role, self.role_controller)
            
            # Esperar a que el diálogo se cierre
            self.root.wait_window(dialog.dialog)
            
            print(f"DEBUG MANAGE_PERMISOS - Diálogo cerrado, result: {dialog.result}")
            
            if dialog.result:
                print(f"DEBUG MANAGE_PERMISOS - Actualizando permisos del rol {role_id} con: {dialog.result}")
                
                # Actualizar permisos del rol
                success, message = self.role_controller.update_role(
                    role_id, {'permissions': dialog.result}, self.current_user
                )
                
                print(f"DEBUG MANAGE_PERMISOS - Resultado update_role: success={success}, message={message}")
                
                if success:
                    messagebox.showinfo("Éxito", "Permisos actualizados exitosamente")
                    self.refresh_roles()
                else:
                    messagebox.showerror("Error", message)
            else:
                print("DEBUG MANAGE_PERMISOS - dialog.result es None/vacío, no se actualiza nada")
                    
        except Exception as e:
            print(f"DEBUG MANAGE_PERMISOS - Excepción: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error gestionando permisos:\n{str(e)}")
    
    def show_context_menu(self, event):
        """Mostrar menú contextual"""
        try:
            # Seleccionar item bajo el cursor
            item = self.roles_tree.identify_row(event.y)
            if item:
                self.roles_tree.selection_set(item)
                
                # Crear menú contextual
                context_menu = tk.Menu(self.root, tearoff=0)
                context_menu.add_command(label="✏️ Editar", command=self.edit_role)
                context_menu.add_command(label="🔓 Permisos", command=self.manage_permissions)
                context_menu.add_separator()
                context_menu.add_command(label="✅ Activar", command=self.activate_role)
                context_menu.add_command(label="❌ Desactivar", command=self.deactivate_role)
                context_menu.add_separator()
                context_menu.add_command(label="🗑️ Eliminar", command=self.delete_role)
                
                # Mostrar menú
                context_menu.tk_popup(event.x_root, event.y_root)
                
        except Exception as e:
            print(f"Error en menú contextual: {e}")
    
    def bind_callback(self, event: str, callback: Callable):
        """Registrar callback"""
        self.callbacks[event] = callback
    
    def _back_to_dashboard(self):
        """Volver al dashboard"""
        if 'back_to_dashboard' in self.callbacks:
            self.callbacks['back_to_dashboard']()
    
    def bind_callback(self, event_name: str, callback: Callable):
        """Registrar un callback para un evento"""
        self.callbacks[event_name] = callback
    
    def on_back_to_dashboard(self):
        """Callback para volver al dashboard"""
        self._back_to_dashboard()


class RoleDialog:
    """Diálogo para crear/editar roles"""
    
    def __init__(self, parent, title: str, role_controller: RoleController, role_data: Dict[str, Any] = None):
        self.parent = parent
        self.title = title
        self.role_controller = role_controller
        self.role_data = role_data or {}
        self.result = None
        
        # Variables
        self.name_var = tk.StringVar(value=self.role_data.get('name', ''))
        self.code_var = tk.StringVar(value=self.role_data.get('code', ''))
        self.description_var = tk.StringVar(value=self.role_data.get('description', ''))
        self.active_var = tk.BooleanVar(value=self.role_data.get('active', True))
        
        # Crear diálogo
        self.create_dialog()
    
    def create_dialog(self):
        """Crear ventana de diálogo con diseño moderno"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.title)
        self.dialog.geometry("650x600")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.dialog.configure(bg='#f5f6fa')
        
        # Centrar ventana
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (650 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (600 // 2)
        self.dialog.geometry(f"650x600+{x}+{y}")
        
        # Header moderno con color
        header_frame = tk.Frame(self.dialog, bg='#3498db', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Icono y título en el header
        title_container = tk.Frame(header_frame, bg='#3498db')
        title_container.pack(expand=True, fill='both', padx=30, pady=20)
        
        icon_label = tk.Label(
            title_container,
            text="🔐",
            font=('Segoe UI', 28),
            bg='#3498db',
            fg='white'
        )
        icon_label.pack(side='left', padx=(0, 15))
        
        title_label = tk.Label(
            title_container,
            text=self.title,
            font=('Segoe UI', 20, 'bold'),
            bg='#3498db',
            fg='white'
        )
        title_label.pack(side='left')
        
        # Contenedor principal con scroll
        main_container = tk.Frame(self.dialog, bg='#f5f6fa')
        main_container.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Canvas para scroll
        canvas = tk.Canvas(main_container, bg='#f5f6fa', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f5f6fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas y scrollbar
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Frame de formulario dentro del scrollable
        form_frame = tk.Frame(scrollable_frame, bg='white', relief='flat', bd=0)
        form_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Padding interno
        inner_frame = tk.Frame(form_frame, bg='white')
        inner_frame.pack(fill='both', expand=True, padx=25, pady=25)
        
        # Campo: Nombre del Rol
        tk.Label(
            inner_frame,
            text="Nombre del Rol",
            font=('Segoe UI', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 8))
        
        name_frame = tk.Frame(inner_frame, bg='white')
        name_frame.pack(fill='x', pady=(0, 20))
        
        self.name_entry = tk.Entry(
            name_frame,
            textvariable=self.name_var,
            font=('Segoe UI', 12),
            relief='solid',
            bd=1,
            bg='#f8f9fa'
        )
        self.name_entry.pack(fill='x', ipady=10)
        
        # Si hay datos existentes, forzar actualización visual
        if self.role_data and self.role_data.get('name'):
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, self.role_data.get('name', ''))
        
        self.name_entry.focus()
        
        # Hint para nombre
        hint_name = tk.Label(
            inner_frame,
            text="Ej: Gerente de Ventas, Cajero, Supervisor",
            font=('Segoe UI', 9, 'italic'),
            bg='white',
            fg='#7f8c8d'
        )
        hint_name.pack(anchor='w', pady=(0, 15))
        
        # Campo: Código del Rol
        tk.Label(
            inner_frame,
            text="Código del Rol",
            font=('Segoe UI', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 8))
        
        code_frame = tk.Frame(inner_frame, bg='white')
        code_frame.pack(fill='x', pady=(0, 20))
        
        self.code_entry = tk.Entry(
            code_frame,
            textvariable=self.code_var,
            font=('Segoe UI', 12),
            relief='solid',
            bd=1,
            bg='#f8f9fa'
        )
        self.code_entry.pack(fill='x', ipady=10)
        
        # Si hay datos existentes, forzar actualización visual
        if self.role_data and self.role_data.get('code'):
            self.code_entry.delete(0, tk.END)
            self.code_entry.insert(0, self.role_data.get('code', ''))
        
        # Hint para código
        hint_code = tk.Label(
            inner_frame,
            text="Código único (sin espacios, minúsculas). Ej: gerente_ventas, cajero",
            font=('Segoe UI', 9, 'italic'),
            bg='white',
            fg='#7f8c8d'
        )
        hint_code.pack(anchor='w', pady=(0, 15))
        
        # Campo: Descripción
        tk.Label(
            inner_frame,
            text="Descripción",
            font=('Segoe UI', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 8))
        
        desc_container = tk.Frame(inner_frame, bg='white', relief='solid', bd=1)
        desc_container.pack(fill='x', pady=(0, 20))
        
        self.desc_text = tk.Text(
            desc_container,
            height=5,
            font=('Segoe UI', 11),
            wrap=tk.WORD,
            relief='flat',
            bg='#f8f9fa',
            padx=10,
            pady=10
        )
        desc_scrollbar = ttk.Scrollbar(desc_container, orient=tk.VERTICAL, command=self.desc_text.yview)
        self.desc_text.configure(yscrollcommand=desc_scrollbar.set)
        
        self.desc_text.pack(side='left', fill='both', expand=True)
        desc_scrollbar.pack(side='right', fill='y')
        
        # Insertar descripción existente
        if self.role_data.get('description'):
            self.desc_text.insert('1.0', self.role_data.get('description'))
        
        # Hint para descripción
        hint_desc = tk.Label(
            inner_frame,
            text="Describe las responsabilidades y alcance de este rol",
            font=('Segoe UI', 9, 'italic'),
            bg='white',
            fg='#7f8c8d'
        )
        hint_desc.pack(anchor='w', pady=(0, 20))
        
        # Separador visual
        separator = tk.Frame(inner_frame, bg='#e0e0e0', height=1)
        separator.pack(fill='x', pady=20)
        
        # Estado con mejor diseño
        status_frame = tk.Frame(inner_frame, bg='white')
        status_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            status_frame,
            text="Estado del Rol",
            font=('Segoe UI', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left', padx=(0, 20))
        
        # Checkbutton personalizado
        self.active_check = tk.Checkbutton(
            status_frame,
            text="✓ Activo",
            variable=self.active_var,
            font=('Segoe UI', 11),
            bg='white',
            fg='#27ae60',
            activebackground='white',
            activeforeground='#27ae60',
            selectcolor='white',
            cursor='hand2'
        )
        self.active_check.pack(side='left')
        
        # Footer con botones
        footer_frame = tk.Frame(self.dialog, bg='#ecf0f1', height=80)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        button_container = tk.Frame(footer_frame, bg='#ecf0f1')
        button_container.pack(expand=True, fill='both', padx=30, pady=20)
        
        # Botón Cancelar
        cancel_btn = tk.Button(
            button_container,
            text="✕ Cancelar",
            command=self.cancel,
            bg='#95a5a6',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief='flat',
            cursor='hand2',
            padx=30,
            pady=12
        )
        cancel_btn.pack(side='right', padx=(10, 0))
        
        # Botón Guardar
        save_btn = tk.Button(
            button_container,
            text="✓ Guardar Rol",
            command=self.save,
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief='flat',
            cursor='hand2',
            padx=30,
            pady=12
        )
        save_btn.pack(side='right')
        
        # Información adicional (si es edición)
        if self.role_data:
            info_label = tk.Label(
                button_container,
                text=f"📝 Editando rol existente",
                font=('Segoe UI', 10),
                bg='#ecf0f1',
                fg='#7f8c8d'
            )
            info_label.pack(side='left')
        
        # Bind Enter y Escape
        self.dialog.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        
        # Efecto hover en botones
        def on_enter_save(e):
            save_btn.config(bg='#229954')
        
        def on_leave_save(e):
            save_btn.config(bg='#27ae60')
        
        def on_enter_cancel(e):
            cancel_btn.config(bg='#7f8c8d')
        
        def on_leave_cancel(e):
            cancel_btn.config(bg='#95a5a6')
        
        save_btn.bind('<Enter>', on_enter_save)
        save_btn.bind('<Leave>', on_leave_save)
        cancel_btn.bind('<Enter>', on_enter_cancel)
        cancel_btn.bind('<Leave>', on_leave_cancel)
        
        print(f"DEBUG ROLE - Diálogo creado con diseño moderno")
    
    def save(self):
        """Guardar rol"""
        try:
            # SISTEMA DE DOBLE CAPTURA - igual que en usuarios
            print("DEBUG ROLE - Capturando datos del formulario...")
            
            # Captura desde StringVar
            name_from_var = self.name_var.get().strip()
            code_from_var = self.code_var.get().strip()
            
            # Captura desde Entry widgets (fallback)
            name_from_entry = self.name_entry.get().strip()
            code_from_entry = self.code_entry.get().strip()
            
            print(f"DEBUG ROLE - Name desde StringVar: '{name_from_var}' (len: {len(name_from_var)})")
            print(f"DEBUG ROLE - Name desde Entry: '{name_from_entry}' (len: {len(name_from_entry)})")
            print(f"DEBUG ROLE - Code desde StringVar: '{code_from_var}' (len: {len(code_from_var)})")
            print(f"DEBUG ROLE - Code desde Entry: '{code_from_entry}' (len: {len(code_from_entry)})")
            
            # Usar Entry como fallback si StringVar está vacío
            name = name_from_entry if not name_from_var and name_from_entry else name_from_var
            code = code_from_entry if not code_from_var and code_from_entry else code_from_var
            
            description = self.desc_text.get('1.0', tk.END).strip()
            active = self.active_var.get()
            
            print(f"VALIDACIÓN FINAL ROLE - Name: '{name}' (len: {len(name)})")
            print(f"VALIDACIÓN FINAL ROLE - Code: '{code}' (len: {len(code)})")
            print(f"VALIDACIÓN FINAL ROLE - Description: '{description}' (len: {len(description)})")
            print(f"VALIDACIÓN FINAL ROLE - Active: {active}")
            
            # Validación básica
            if not name:
                messagebox.showerror("Error", "El nombre del rol es requerido")
                return
            
            if not code:
                messagebox.showerror("Error", "El código del rol es requerido")
                return
            
            # Preparar datos
            self.result = {
                'name': name,
                'code': code.lower().replace(' ', '_'),
                'description': description,
                'active': active
            }
            
            # Si es edición, mantener permisos existentes
            if self.role_data:
                self.result['permissions'] = self.role_data.get('permissions', [])
            else:
                self.result['permissions'] = []
            
            print(f"DEBUG ROLE - Resultado final: {self.result}")
            print("DEBUG ROLE - Cerrando diálogo...")
            
            try:
                self.dialog.destroy()
                print("DEBUG ROLE - Diálogo cerrado exitosamente")
            except Exception as e:
                print(f"DEBUG ROLE - Error cerrando diálogo: {e}")
                import traceback
                traceback.print_exc()
            
        except Exception as e:
            print(f"DEBUG ROLE - Excepción en save(): {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error guardando rol:\n{str(e)}")
    
    def cancel(self):
        """Cancelar"""
        print("DEBUG ROLE - CANCELANDO diálogo")
        self.result = None
        self.dialog.destroy()


class PermissionsDialog:
    """Diálogo para gestionar permisos de un rol"""
    
    def __init__(self, parent, role: Dict[str, Any], role_controller: RoleController):
        self.parent = parent
        self.role = role
        self.role_controller = role_controller
        self.result = None
        
        # Variables para permisos y etiquetas
        self.permission_vars = {}
        self.permission_labels = {}
        
        # Crear diálogo
        self.create_dialog()
    
    def create_dialog(self):
        """Crear ventana de diálogo"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(f"Permisos del Rol: {self.role.get('name')}")
        self.dialog.geometry("800x700")
        self.dialog.resizable(True, True)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Centrar ventana
        self.dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 50,
            self.parent.winfo_rooty() + 50
        ))
        
        # Marco principal
        main_frame = ttk.Frame(self.dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(title_frame, text=f"🔓 Permisos del Rol: {self.role.get('name')}", 
                 font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        
        # Botones de selección rápida
        quick_frame = ttk.Frame(main_frame)
        quick_frame.pack(fill=tk.X, pady=(0, 10))
        
        select_all_btn = ttk.Button(quick_frame, text="✅ Seleccionar Todo", 
                  command=self.select_all_safe)
        select_all_btn.pack(side=tk.LEFT, padx=(0, 5))
        # Prevenir activación automática por focus/binding
        select_all_btn.configure(takefocus=False)
        
        deselect_all_btn = ttk.Button(quick_frame, text="❌ Deseleccionar Todo", 
                  command=self.deselect_all)
        deselect_all_btn.pack(side=tk.LEFT, padx=(0, 5))
        deselect_all_btn.configure(takefocus=False)
        
        reset_btn = ttk.Button(quick_frame, text="🔄 Restablecer", 
                  command=self.reset_permissions)
        reset_btn.pack(side=tk.LEFT)
        reset_btn.configure(takefocus=False)
        
        # Marco con scroll para permisos
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        canvas = tk.Canvas(canvas_frame)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Crear permisos por categoría
        self.create_permissions_checkboxes(scrollable_frame)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Cancelar", 
                  command=self.cancel).pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Button(button_frame, text="Guardar Permisos", 
                  command=self.save, style="Accent.TButton").pack(side=tk.RIGHT)
        
        # Bind Escape
        self.dialog.bind('<Escape>', lambda e: self.cancel())
    
    def create_permissions_checkboxes(self, parent):
        """Crear checkboxes de permisos organizados por categoría"""
        try:
            print(f"DEBUG PERMISOS - Rol completo: {self.role}")
            permissions_by_category = self.role_controller.get_permissions_by_category()
            current_permissions = self.role.get('permissions', [])
            
            print(f"DEBUG PERMISOS - current_permissions tipo: {type(current_permissions)}")
            print(f"DEBUG PERMISOS - current_permissions valor: {current_permissions}")
            
            # Si los permisos están en formato JSON string, convertir a lista
            if isinstance(current_permissions, str):
                try:
                    import json
                    current_permissions = json.loads(current_permissions)
                    print(f"DEBUG PERMISOS - Convertido de JSON: {current_permissions}")
                except:
                    print("DEBUG PERMISOS - Error convirtiendo JSON, usando lista vacía")
                    current_permissions = []
            
            for category, permissions in permissions_by_category.items():
                # Marco para la categoría
                category_frame = ttk.LabelFrame(parent, text=f"📂 {category}", padding=10)
                category_frame.pack(fill=tk.X, pady=(0, 10), padx=5)
                
                # Crear grid para permisos
                for i, permission in enumerate(permissions):
                    var = tk.BooleanVar()
                    
                    # Marcar si el rol ya tiene este permiso
                    has_permission = permission in current_permissions or '*' in current_permissions
                    
                    print(f"DEBUG PERMISOS - Procesando '{permission}': en_lista={permission in current_permissions}, es_admin={'*' in current_permissions}, final={has_permission}")
                    
                    if has_permission:
                        var.set(True)
                        print(f"DEBUG PERMISOS - ✅ MARCANDO '{permission}'")
                    else:
                        print(f"DEBUG PERMISOS - ❌ NO marcando '{permission}'")
                    
                    self.permission_vars[permission] = var
                    
                    # Obtener descripción del permiso
                    description = self.role_controller.get_permission_description(permission)
                    
                    # Crear frame para el permiso (sin checkbox tradicional)
                    checkbox_frame = ttk.Frame(category_frame)
                    checkbox_frame.pack(fill=tk.X, pady=2)
                    
                    # Etiqueta con formato mejorado y clickeable
                    status_icon = "✅" if var.get() else "⬜"
                    label_text = f"{status_icon} {permission} - {description}"
                    
                    label = tk.Label(
                        checkbox_frame,
                        text=label_text,
                        font=('Arial', 10),
                        anchor='w',
                        cursor='hand2',
                        bg='lightgreen' if var.get() else 'lightgray',
                        relief='raised',
                        bd=1,
                        padx=10,
                        pady=5
                    )
                    label.pack(fill=tk.X, expand=True)
                    
                    # Guardar referencia a la etiqueta
                    self.permission_labels[permission] = label
                    
                    # Hacer la etiqueta clickeable
                    def toggle_permission(event, v=var):
                        v.set(not v.get())
                    
                    label.bind('<Button-1>', toggle_permission)
                    
                    # Actualizar etiqueta cuando cambie el checkbox
                    def update_label(perm=permission, lbl=label, v=var):
                        icon = "✅" if v.get() else "⬜"
                        desc = self.role_controller.get_permission_description(perm)
                        lbl.config(
                            text=f"{icon} {perm} - {desc}",
                            bg='lightgreen' if v.get() else 'lightgray'
                        )
                    
                    var.trace('w', lambda *args, ul=update_label: ul())
            
            # Verificar estado final de los checkboxes
            marked_count = sum(1 for var in self.permission_vars.values() if var.get())
            total_count = len(self.permission_vars)
            print(f"DEBUG PERMISOS - Estado final: {marked_count}/{total_count} checkboxes marcados")
            
            # Forzar actualización de la UI después de configurar los valores
            self.dialog.update_idletasks()
            self.dialog.update()
            
            # Verificar nuevamente después de la actualización
            final_marked_count = sum(1 for var in self.permission_vars.values() if var.get())
            print(f"DEBUG PERMISOS - Estado después de update: {final_marked_count}/{total_count} checkboxes marcados")
            
            if final_marked_count != marked_count:
                print(f"DEBUG PERMISOS - ⚠️ CAMBIO DE ESTADO después de update: {marked_count} -> {final_marked_count}")
            
        except Exception as e:
            print(f"DEBUG PERMISOS - Excepción: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error creando permisos:\n{str(e)}")
    
    def select_all_safe(self):
        """Seleccionar todos los permisos (versión segura)"""
        print("DEBUG PERMISOS - ✅ SELECT_ALL_SAFE llamado manualmente")
        for permission, var in self.permission_vars.items():
            var.set(True)
            # Actualizar etiqueta inmediatamente
            if permission in self.permission_labels:
                desc = self.role_controller.get_permission_description(permission)
                self.permission_labels[permission].config(
                    text=f"✅ {permission} - {desc}",
                    bg='lightgreen'
                )
        
        # Forzar actualización de UI
        self.dialog.update_idletasks()
    
    def select_all(self):
        """Seleccionar todos los permisos (método original con debug)"""
        print("DEBUG PERMISOS - ⚠️ SELECT_ALL llamado!")
        import traceback
        traceback.print_stack()
        for var in self.permission_vars.values():
            var.set(True)
    
    def deselect_all(self):
        """Deseleccionar todos los permisos"""
        print("DEBUG PERMISOS - ⚠️ DESELECT_ALL llamado!")
        for permission, var in self.permission_vars.items():
            var.set(False)
            # Actualizar etiqueta inmediatamente
            if permission in self.permission_labels:
                desc = self.role_controller.get_permission_description(permission)
                self.permission_labels[permission].config(
                    text=f"⬜ {permission} - {desc}",
                    bg='lightgray'
                )
        
        # Forzar actualización de UI
        self.dialog.update_idletasks()
    
    def reset_permissions(self):
        """Restablecer permisos originales"""
        print("DEBUG PERMISOS - ⚠️ RESET_PERMISSIONS llamado!")
        current_permissions = self.role.get('permissions', [])
        print(f"DEBUG RESET - Permisos originales del rol: {current_permissions}")
        
        marked_before = sum(1 for var in self.permission_vars.values() if var.get())
        print(f"DEBUG RESET - Estado antes: {marked_before}/{len(self.permission_vars)} marcados")
        
        for permission, var in self.permission_vars.items():
            should_be_checked = permission in current_permissions or '*' in current_permissions
            var.set(should_be_checked)
            
            # Actualizar etiqueta inmediatamente
            if permission in self.permission_labels:
                desc = self.role_controller.get_permission_description(permission)
                icon = "✅" if should_be_checked else "⬜"
                self.permission_labels[permission].config(
                    text=f"{icon} {permission} - {desc}",
                    bg='lightgreen' if should_be_checked else 'lightgray'
                )
            
        # Forzar actualización de UI
        self.dialog.update_idletasks()
        
        marked_after = sum(1 for var in self.permission_vars.values() if var.get())
        print(f"DEBUG RESET - Estado después: {marked_after}/{len(self.permission_vars)} marcados")
        
        if marked_after != len(current_permissions):
            print(f"DEBUG RESET - ⚠️ DISCREPANCIA: esperado {len(current_permissions)}, obtenido {marked_after}")
    
    def save(self):
        """Guardar permisos"""
        try:
            print("DEBUG SAVE_PERMISOS - Iniciando guardado...")
            
            # Obtener permisos seleccionados
            selected_permissions = []
            
            for permission, var in self.permission_vars.items():
                if var.get():
                    selected_permissions.append(permission)
                    print(f"DEBUG SAVE_PERMISOS - Permiso marcado: {permission}")
            
            print(f"DEBUG SAVE_PERMISOS - Total permisos seleccionados: {len(selected_permissions)}")
            print(f"DEBUG SAVE_PERMISOS - Permisos: {selected_permissions}")
            
            self.result = selected_permissions
            print(f"DEBUG SAVE_PERMISOS - Result asignado: {self.result}")
            
            self.dialog.destroy()
            print("DEBUG SAVE_PERMISOS - Diálogo cerrado")
            
        except Exception as e:
            print(f"DEBUG SAVE_PERMISOS - Excepción: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error guardando permisos:\n{str(e)}")
    
    def cancel(self):
        """Cancelar"""
        self.result = None
        self.dialog.destroy()
