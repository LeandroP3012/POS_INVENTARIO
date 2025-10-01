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

from controllers.role_controller import RoleController

class RoleManagementView:
    """Vista para gestión de roles y permisos"""
    
    def __init__(self, parent, current_user: Dict[str, Any], embedded: bool = False):
        self.parent = parent
        self.current_user = current_user
        self.embedded = embedded
        self.role_controller = RoleController()
        
        # Variables de la vista
        self.search_var = tk.StringVar()
        self.filter_active_var = tk.StringVar(value="todos")
        self.filter_type_var = tk.StringVar(value="todos")
        
        # Callbacks
        self.callbacks = {}
        
        # Configurar tamaño de ventana si no está embebido
        if not self.embedded and hasattr(parent, 'geometry'):
            parent.geometry("1500x1000")
        
        # Crear interfaz
        self.create_interface()
        
        # Cargar datos iniciales
        self.refresh_roles()
    
    def create_interface(self):
        """Crear la interfaz de usuario"""
        # Marco principal
        if self.embedded:
            self.main_frame = ttk.Frame(self.parent)
            self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        else:
            self.main_frame = self.parent
        
        # Título
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        ttk.Label(title_frame, text="🔐 GESTIÓN DE ROLES Y PERMISOS", 
                 font=('Arial', 26, 'bold')).pack(side=tk.LEFT)
        
        if self.embedded:
            ttk.Button(title_frame, text="← Volver al Dashboard", 
                      command=self._back_to_dashboard).pack(side=tk.RIGHT)
        
        # Marco de estadísticas
        self.create_stats_frame()
        
        # Marco de búsqueda y filtros
        self.create_search_frame()
        
        # Marco de botones de acción
        self.create_action_buttons_frame()
        
        # Marco de tabla de roles
        self.create_roles_table_frame()
    
    def create_stats_frame(self):
        """Crear marco de estadísticas"""
        stats_frame = ttk.LabelFrame(self.main_frame, text="📊 ESTADÍSTICAS", padding=20)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Contenedor de estadísticas
        stats_container = ttk.Frame(stats_frame)
        stats_container.pack(fill=tk.X)
        
        # Estadísticas
        self.stats_labels = {}
        
        stats_data = [
            ("total_roles", "Total de Roles", "#3498db"),
            ("active_roles", "Roles Activos", "#27ae60"),
            ("system_roles", "Roles del Sistema", "#9b59b6"),
            ("custom_roles", "Roles Personalizados", "#e67e22")
        ]
        
        for i, (key, label, color) in enumerate(stats_data):
            stat_frame = ttk.Frame(stats_container)
            stat_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            value_label = ttk.Label(stat_frame, text="0", font=('Arial', 32, 'bold'), 
                                   foreground=color)
            value_label.pack(pady=5)
            
            desc_label = ttk.Label(stat_frame, text=label, font=('Arial', 14, 'bold'))
            desc_label.pack()
            
            self.stats_labels[key] = value_label
    
    def create_search_frame(self):
        """Crear marco de búsqueda y filtros"""
        search_frame = ttk.LabelFrame(self.main_frame, text="🔍 BÚSQUEDA Y FILTROS", padding=15)
        search_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Primera fila: búsqueda
        search_row = ttk.Frame(search_frame)
        search_row.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(search_row, text="Buscar:", font=('Arial', 14, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        
        search_entry = ttk.Entry(search_row, textvariable=self.search_var, width=40, font=('Arial', 14))
        search_entry.pack(side=tk.LEFT, padx=(0, 15))
        search_entry.bind('<KeyRelease>', lambda e: self.search_roles())
        
        ttk.Button(search_row, text="🔍 BUSCAR", 
                  command=self.search_roles).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(search_row, text="🔄 LIMPIAR", 
                  command=self.clear_search).pack(side=tk.LEFT)
        
        # Segunda fila: filtros
        filter_row = ttk.Frame(search_frame)
        filter_row.pack(fill=tk.X)
        
        # Filtro por estado
        ttk.Label(filter_row, text="Estado:", font=('Arial', 14, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        
        active_combo = ttk.Combobox(filter_row, textvariable=self.filter_active_var, 
                                   values=["todos", "activos", "inactivos"], 
                                   state="readonly", width=18, font=('Arial', 14))
        active_combo.pack(side=tk.LEFT, padx=(0, 30))
        active_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        # Filtro por tipo
        ttk.Label(filter_row, text="Tipo:", font=('Arial', 14, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        
        type_combo = ttk.Combobox(filter_row, textvariable=self.filter_type_var, 
                                 values=["todos", "sistema", "personalizados"], 
                                 state="readonly", width=22, font=('Arial', 14))
        type_combo.pack(side=tk.LEFT, padx=(0, 15))
        type_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
    
    def create_action_buttons_frame(self):
        """Crear marco de botones de acción"""
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botones principales
        ttk.Button(buttons_frame, text="➕ Crear Rol", 
                  command=self.create_role, style="Accent.TButton").pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(buttons_frame, text="✏️ Editar Rol", 
                  command=self.edit_role).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(buttons_frame, text="🗑️ Eliminar Rol", 
                  command=self.delete_role).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(buttons_frame, text="🔓 Gestionar Permisos", 
                  command=self.manage_permissions).pack(side=tk.LEFT, padx=(0, 20))
        
        # Botones de estado
        ttk.Button(buttons_frame, text="✅ Activar", 
                  command=self.activate_role).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(buttons_frame, text="❌ Desactivar", 
                  command=self.deactivate_role).pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón de actualizar
        ttk.Button(buttons_frame, text="🔄 Actualizar", 
                  command=self.refresh_roles).pack(side=tk.RIGHT)
    
    def create_roles_table_frame(self):
        """Crear marco de tabla de roles"""
        table_frame = ttk.LabelFrame(self.main_frame, text="📋 Lista de Roles", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear Treeview con scrollbars
        tree_frame = ttk.Frame(table_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Definir columnas
        columns = ('ID', 'Nombre', 'Código', 'Descripción', 'Tipo', 'Estado', 'Usuarios', 'Permisos')
        
        self.roles_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=18)
        
        # Configurar columnas
        column_configs = {
            'ID': (60, tk.CENTER),
            'Nombre': (180, tk.W),
            'Código': (140, tk.W),
            'Descripción': (300, tk.W),
            'Tipo': (120, tk.CENTER),
            'Estado': (100, tk.CENTER),
            'Usuarios': (100, tk.CENTER),
            'Permisos': (100, tk.CENTER)
        }
        
        for col in columns:
            width, anchor = column_configs[col]
            self.roles_tree.heading(col, text=col)
            self.roles_tree.column(col, width=width, anchor=anchor)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.roles_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.roles_tree.xview)
        
        self.roles_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Empaquetar componentes
        self.roles_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind eventos
        self.roles_tree.bind('<Double-1>', lambda e: self.edit_role())
        self.roles_tree.bind('<Button-3>', self.show_context_menu)
    
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
                status = "Activo" if role.get('active', True) else "Inactivo"
                users_count = role.get('users_count', 0)
                permissions_count = len(role.get('permissions', []))
                
                # Insertar en tabla
                item_id = self.roles_tree.insert('', tk.END, values=(
                    role_id, name, code, description, role_type, status, users_count, permissions_count
                ))
                
                # Colorear según estado
                if not role.get('active', True):
                    self.roles_tree.set(item_id, 'Estado', '❌ Inactivo')
                else:
                    self.roles_tree.set(item_id, 'Estado', '✅ Activo')
            
            # Actualizar estadísticas
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
            dialog = RoleDialog(self.main_frame, title="Crear Nuevo Rol", 
                               role_controller=self.role_controller)
            
            # Esperar a que el diálogo termine completamente
            self.main_frame.wait_window(dialog.dialog)
            
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
            dialog = RoleDialog(self.main_frame, title="Editar Rol", 
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
            dialog = PermissionsDialog(self.main_frame, role, self.role_controller)
            
            # Esperar a que el diálogo se cierre
            self.main_frame.wait_window(dialog.dialog)
            
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
                context_menu = tk.Menu(self.main_frame, tearoff=0)
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
        """Crear ventana de diálogo"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.title)
        self.dialog.geometry("600x500")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Centrar ventana
        self.dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 50,
            self.parent.winfo_rooty() + 50
        ))
        
        # Marco principal
        main_frame = ttk.Frame(self.dialog, padding=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campos del formulario
        # Nombre
        ttk.Label(main_frame, text="Nombre del Rol:", font=('Arial', 13)).pack(anchor=tk.W, pady=(0, 8))
        self.name_entry = ttk.Entry(main_frame, textvariable=self.name_var, font=('Arial', 13))
        self.name_entry.pack(fill=tk.X, pady=(0, 20))
        self.name_entry.focus()
        
        print(f"DEBUG ROLE - Name entry creado, var actual: '{self.name_var.get()}'")
        
        # Código
        ttk.Label(main_frame, text="Código del Rol:", font=('Arial', 13)).pack(anchor=tk.W, pady=(0, 8))
        self.code_entry = ttk.Entry(main_frame, textvariable=self.code_var, font=('Arial', 13))
        self.code_entry.pack(fill=tk.X, pady=(0, 20))
        
        print(f"DEBUG ROLE - Code entry creado, var actual: '{self.code_var.get()}'")
        
        # Descripción
        ttk.Label(main_frame, text="Descripción:", font=('Arial', 13)).pack(anchor=tk.W, pady=(0, 8))
        desc_frame = ttk.Frame(main_frame)
        desc_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.desc_text = tk.Text(desc_frame, height=5, font=('Arial', 12), wrap=tk.WORD)
        desc_scrollbar = ttk.Scrollbar(desc_frame, orient=tk.VERTICAL, command=self.desc_text.yview)
        self.desc_text.configure(yscrollcommand=desc_scrollbar.set)
        
        self.desc_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        desc_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insertar descripción existente
        if self.role_data.get('description'):
            self.desc_text.insert('1.0', self.role_data.get('description'))
        
        # Estado
        ttk.Checkbutton(main_frame, text="Rol Activo", 
                       variable=self.active_var).pack(anchor=tk.W, pady=(15, 25))
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame, text="Cancelar", 
                  command=self.cancel).pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Button(button_frame, text="Guardar", 
                  command=self.save, style="Accent.TButton").pack(side=tk.RIGHT)
        
        # Bind Enter y Escape
        self.dialog.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
    
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
        
        # Variables para permisos
        self.permission_vars = {}
        
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
                    
                    # Crear checkbox
                    checkbox = ttk.Checkbutton(
                        category_frame, 
                        text=f"{permission} - {description}",
                        variable=var
                    )
                    checkbox.pack(anchor=tk.W, pady=2)
            
            # Verificar estado final de los checkboxes
            marked_count = sum(1 for var in self.permission_vars.values() if var.get())
            total_count = len(self.permission_vars)
            print(f"DEBUG PERMISOS - Estado final: {marked_count}/{total_count} checkboxes marcados")
            
        except Exception as e:
            print(f"DEBUG PERMISOS - Excepción: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error creando permisos:\n{str(e)}")
    
    def select_all_safe(self):
        """Seleccionar todos los permisos (versión segura)"""
        print("DEBUG PERMISOS - ✅ SELECT_ALL_SAFE llamado manualmente")
        for var in self.permission_vars.values():
            var.set(True)
    
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
        for var in self.permission_vars.values():
            var.set(False)
    
    def reset_permissions(self):
        """Restablecer permisos originales"""
        print("DEBUG PERMISOS - ⚠️ RESET_PERMISSIONS llamado!")
        current_permissions = self.role.get('permissions', [])
        
        for permission, var in self.permission_vars.items():
            if permission in current_permissions or '*' in current_permissions:
                var.set(True)
            else:
                var.set(False)
    
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
