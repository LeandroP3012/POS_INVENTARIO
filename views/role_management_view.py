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
from services.permission_service import PermissionService
from utils.responsive_utils import ResponsiveManager

class RoleManagementView(BaseView):
    """Vista para gestión de roles y permisos"""
    
    def __init__(self, parent, current_user: Dict[str, Any], embedded: bool = False):
        self.parent = parent
        self.current_user = current_user
        self.embedded = embedded
        super().__init__(parent)
        self.role_controller = RoleController()
        self.permission_service = PermissionService()
        
        # Inicializar gestor responsivo
        self.responsive = ResponsiveManager(self.root)
        
        # Variables de la vista
        self.search_var = tk.StringVar()
        self.filter_active_var = tk.StringVar(value="todos")
        self.filter_type_var = tk.StringVar(value="todos")
        
        # Callbacks
        self.callbacks = {}
        self.navbar_built = False
        
        # Crear interfaz
        self.create_interface()
        
        # Cargar datos iniciales
        self.refresh_roles()
    
    def has_permission(self, permission: str) -> bool:
        """Verificar si el usuario actual tiene un permiso específico"""
        try:
            return self.permission_service.check_permission(self.current_user, permission)
        except Exception as e:
            print(f"Error verificando permiso {permission}: {e}")
            return False
    
    def create_interface(self):
        """Crear la interfaz de usuario"""
        # Configurar fondo principal
        if self.embedded:
            self.root.configure(bg='#f8f9fa')
        
        # Header
        self.create_header()
        
        # El navbar se creará después de registrar callbacks
        # en build_navbar()
        
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
    
    def create_navbar(self, after_widget=None):
        """Crear navbar personalizado - GLOBAL para todos los módulos"""
        navbar_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        if after_widget:
            navbar_frame.pack(fill='x', after=after_widget)
        else:
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
        
        # Helper para ejecutar callbacks de forma segura
        def safe_call(callback_name):
            def wrapper():
                print(f"🔄 Navbar (roles): Intentando ejecutar '{callback_name}'")
                callback = self.callbacks.get(callback_name)
                if callback:
                    print(f"   ✓ Callback encontrado, ejecutando...")
                    callback()
                else:
                    print(f"   ✗ Callback no encontrado o es None")
            return wrapper
        
        # Botón Archivo
        file_btn = tk.Menubutton(buttons_container, text="📁 Archivo", **btn_style)
        file_btn.pack(side='left', padx=2)
        file_menu = tk.Menu(file_btn, tearoff=0, font=('Segoe UI', 11))
        file_btn.config(menu=file_menu)
        file_menu.add_command(label="Nueva Venta", command=safe_call('new_sale'))
        file_menu.add_separator()
        file_menu.add_command(label="Volver al Dashboard", command=safe_call('back_to_dashboard'))
        
        # Botón Ventas
        sales_btn = tk.Menubutton(buttons_container, text="💰 Ventas", **btn_style)
        sales_btn.pack(side='left', padx=2)
        sales_menu = tk.Menu(sales_btn, tearoff=0, font=('Segoe UI', 11))
        sales_btn.config(menu=sales_menu)
        sales_menu.add_command(label="Nueva Venta", command=safe_call('new_sale'))
        sales_menu.add_command(label="Historial de Ventas", command=safe_call('sales_history'))
        
        # Botón Inventario
        inv_btn = tk.Menubutton(buttons_container, text="📦 Inventario", **btn_style)
        inv_btn.pack(side='left', padx=2)
        inv_menu = tk.Menu(inv_btn, tearoff=0, font=('Segoe UI', 11))
        inv_btn.config(menu=inv_menu)
        inv_menu.add_command(label="Ver Productos", command=safe_call('view_products'))
        inv_menu.add_command(label="Gestionar Categorías", command=safe_call('view_categories'))
        inv_menu.add_command(label="Control de Stock", command=safe_call('stock_control'))
        
        # Botón Reportes
        rep_btn = tk.Menubutton(buttons_container, text="📊 Reportes", **btn_style)
        rep_btn.pack(side='left', padx=2)
        rep_menu = tk.Menu(rep_btn, tearoff=0, font=('Segoe UI', 11))
        rep_btn.config(menu=rep_menu)
        rep_menu.add_command(label="Ventas del Día", command=safe_call('daily_report'))
        rep_menu.add_command(label="Reporte Completo", command=safe_call('full_report'))
        
        # Botón Administración (ACTIVO)
        admin_btn = tk.Menubutton(buttons_container, text="⚙️ Administración", **btn_style)
        admin_btn.config(bg='#34495e')  # Resaltar activo
        admin_btn.pack(side='left', padx=2)
        admin_menu = tk.Menu(admin_btn, tearoff=0, font=('Segoe UI', 11))
        admin_btn.config(menu=admin_menu)
        admin_menu.add_command(label="Gestionar Usuarios", command=safe_call('manage_users'))
        admin_menu.add_command(label="Gestionar Roles ✓", command=lambda: None)  # Actual
        admin_menu.add_separator()
        admin_menu.add_command(label="Configuración", command=safe_call('system_config'))
        
        # Botón Ayuda
        help_btn = tk.Menubutton(buttons_container, text="❓ Ayuda", **btn_style)
        help_btn.pack(side='left', padx=2)
        help_menu = tk.Menu(help_btn, tearoff=0, font=('Segoe UI', 11))
        help_btn.config(menu=help_menu)
        help_menu.add_command(label="Manual de Usuario", command=safe_call('show_manual'))
        help_menu.add_command(label="Acerca de", command=safe_call('show_about'))
    
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
        
        # Botón nuevo rol - Solo si tiene permiso roles.create
        if self.has_permission('roles.create'):
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
        
        # Botón editar - Solo si tiene permiso roles.edit
        if self.has_permission('roles.edit'):
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
        else:
            self.edit_role_btn = None
        
        # Botón eliminar - Solo si tiene permiso roles.delete
        if self.has_permission('roles.delete'):
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
        else:
            self.delete_role_btn = None
        
        # Botón permisos - Solo si tiene permiso roles.permissions
        if self.has_permission('roles.permissions'):
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
        else:
            self.permissions_btn = None
    
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
            # Habilitar botones de acción solo si existen (depende de permisos)
            if self.edit_role_btn is not None:
                self.edit_role_btn.config(state='normal')
            if self.delete_role_btn is not None:
                self.delete_role_btn.config(state='normal')
            if self.permissions_btn is not None:
                self.permissions_btn.config(state='normal')
        else:
            self.selected_role = None
            # Deshabilitar botones de acción solo si existen
            if self.edit_role_btn is not None:
                self.edit_role_btn.config(state='disabled')
            if self.delete_role_btn is not None:
                self.delete_role_btn.config(state='disabled')
            if self.permissions_btn is not None:
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
        # Validar permiso primero
        if not self.has_permission('roles.create'):
            messagebox.showerror(
                "Acceso Denegado", 
                "❌ No tienes permisos para crear roles.\n\n"
                "Contacta al administrador del sistema."
            )
            return
            
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
        # Validar permiso primero
        if not self.has_permission('roles.edit'):
            messagebox.showerror(
                "Acceso Denegado", 
                "❌ No tienes permisos para editar roles.\n\n"
                "Contacta al administrador del sistema."
            )
            return
            
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
        # Validar permiso primero
        if not self.has_permission('roles.delete'):
            messagebox.showerror(
                "Acceso Denegado", 
                "❌ No tienes permisos para eliminar roles.\n\n"
                "Contacta al administrador del sistema."
            )
            return
            
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
        # Validar permiso primero
        if not self.has_permission('roles.permissions'):
            messagebox.showerror(
                "Acceso Denegado", 
                "❌ No tienes permisos para gestionar permisos de roles.\n\n"
                "Contacta al administrador del sistema."
            )
            return
            
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
            
            print(f"\n{'='*80}")
            print(f"📥 DIÁLOGO CERRADO - PROCESANDO RESULTADO")
            print(f"{'='*80}")
            print(f"🔍 Tipo de dialog.result: {type(dialog.result)}")
            print(f"📊 Valor de dialog.result: {dialog.result}")
            
            if dialog.result is not None:
                print(f"✅ dialog.result NO es None")
                print(f"📏 Longitud: {len(dialog.result) if isinstance(dialog.result, list) else 'N/A'}")
            else:
                print(f"❌ dialog.result ES None")
            
            if dialog.result:
                print(f"\n✅ ENTRANDO AL BLOQUE DE ACTUALIZACIÓN")
                print(f"📝 Permisos a guardar: {dialog.result[:5]}... (primeros 5)")
                print(f"📌 Actualizando permisos del rol {role_id}")
                
                # Actualizar permisos del rol
                success, message = self.role_controller.update_role(
                    role_id, {'permissions': dialog.result}, self.current_user
                )
                
                print(f"\n📊 RESULTADO DE UPDATE_ROLE:")
                print(f"   Success: {success}")
                print(f"   Message: {message}")
                print(f"{'='*80}\n")
                
                if success:
                    messagebox.showinfo("Éxito", "Permisos actualizados exitosamente")
                    self.refresh_roles()
                else:
                    messagebox.showerror("Error", message)
            else:
                print(f"\n⚠️ NO ENTRA AL BLOQUE DE ACTUALIZACIÓN")
                print(f"   Razón: dialog.result es {dialog.result}")
                print(f"   Tipo: {type(dialog.result)}")
                if dialog.result is not None and isinstance(dialog.result, list):
                    print(f"   Lista vacía: {len(dialog.result) == 0}")
                print(f"{'='*80}\n")
                    
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
    
    def bind_callback(self, event_name: str, callback: Callable):
        """Registrar un callback para un evento"""
        self.callbacks[event_name] = callback
        print(f"📋 Role: Callback '{event_name}' registrado")
        
        # Crear navbar cuando se registre el primer callback de navegación
        if not self.navbar_built and event_name in ['back_to_dashboard', 'new_sale', 'view_products']:
            print(f"   📋 Primer callback de navegación detectado")
            # Esperar un poco para que se registren todos los callbacks
            self.root.after(100, self._try_build_navbar)
    
    def _try_build_navbar(self):
        """Intentar construir navbar después de un delay"""
        if not self.navbar_built:
            print(f"📋 Callbacks totales registrados en roles: {len(self.callbacks)}")
            for key in self.callbacks:
                print(f"   - {key}")
            self.build_navbar()
            self.navbar_built = True
    
    def build_navbar(self):
        """Construir navbar DESPUÉS de registrar callbacks"""
        print("🔨 Construyendo navbar en role_management_view...")
        # Encontrar el widget header para insertar el navbar después
        header_widget = None
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                try:
                    if widget.cget('bg') == '#2c3e50' and widget.cget('height') != 50:
                        header_widget = widget
                        break
                except:
                    pass
        
        if header_widget:
            self.create_navbar(header_widget)
            print("   ✅ Navbar construido")
        else:
            print("   ✗ No se encontró el header, creando navbar sin after")
            self.create_navbar()
    
    def _back_to_dashboard(self):
        """Volver al dashboard"""
        if 'back_to_dashboard' in self.callbacks:
            self.callbacks['back_to_dashboard']()
    
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
    """Diálogo mejorado para gestionar permisos de un rol"""
    
    def __init__(self, parent, role: Dict[str, Any], role_controller: RoleController):
        self.parent = parent
        self.role = role
        self.role_controller = role_controller
        self.result = None
        
        # Variables para permisos
        self.permission_vars = {}
        self.permission_frames = {}
        self.category_vars = {}  # Para checkboxes de categorías
        
        # Crear diálogo
        self.create_dialog()
    
    def create_dialog(self):
        """Crear ventana de diálogo moderna"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(f"🔐 Gestión de Permisos - {self.role.get('name')}")
        
        # Obtener dimensiones de la pantalla
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        
        # Calcular tamaño de ventana (80% del ancho, 85% del alto)
        window_width = int(screen_width * 0.80)
        window_height = int(screen_height * 0.85)
        
        # Calcular posición centrada
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.dialog.resizable(True, True)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.dialog.configure(bg='#f8f9fa')
        
        # Header moderno
        self.create_header()
        
        # Toolbar con acciones rápidas
        self.create_toolbar()
        
        # Contenedor principal con scroll
        self.create_permissions_area()
        
        # Footer con botones
        self.create_footer()
        
        # Bind Escape
        self.dialog.bind('<Escape>', lambda e: self.cancel())
    
    def create_header(self):
        """Crear header moderno"""
        header_frame = tk.Frame(self.dialog, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        content_frame = tk.Frame(header_frame, bg='#2c3e50')
        content_frame.pack(expand=True, fill='both', padx=25, pady=15)
        
        # Icono y título
        title_frame = tk.Frame(content_frame, bg='#2c3e50')
        title_frame.pack(side='left')
        
        tk.Label(
            title_frame,
            text="🔐",
            font=('Segoe UI', 32),
            bg='#2c3e50',
            fg='white'
        ).pack(side='left', padx=(0, 15))
        
        info_frame = tk.Frame(title_frame, bg='#2c3e50')
        info_frame.pack(side='left')
        
        tk.Label(
            info_frame,
            text="Gestión de Permisos",
            font=('Segoe UI', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        ).pack(anchor='w')
        
        tk.Label(
            info_frame,
            text=f"Rol: {self.role.get('name')} ({self.role.get('code')})",
            font=('Segoe UI', 11),
            fg='#bdc3c7',
            bg='#2c3e50'
        ).pack(anchor='w')
        
        # Contador de permisos
        self.counter_label = tk.Label(
            content_frame,
            text="0 / 0",
            font=('Segoe UI', 16, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        self.counter_label.pack(side='right')
    
    def create_toolbar(self):
        """Crear toolbar con acciones rápidas"""
        toolbar_frame = tk.Frame(self.dialog, bg='white', height=60)
        toolbar_frame.pack(fill='x', pady=(0, 1))
        toolbar_frame.pack_propagate(False)
        
        inner_toolbar = tk.Frame(toolbar_frame, bg='white')
        inner_toolbar.pack(expand=True, fill='both', padx=25, pady=10)
        
        # Título
        tk.Label(
            inner_toolbar,
            text="Acciones Rápidas:",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left', padx=(0, 15))
        
        # Botones de acción
        btn_style = {
            'font': ('Segoe UI', 10, 'bold'),
            'cursor': 'hand2',
            'relief': 'flat',
            'padx': 15,
            'pady': 8,
            'bd': 0
        }
        
        tk.Button(
            inner_toolbar,
            text="✅ Seleccionar Todo",
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            activeforeground='white',
            command=self.select_all_permissions,
            **btn_style
        ).pack(side='left', padx=3)
        
        tk.Button(
            inner_toolbar,
            text="❌ Deseleccionar Todo",
            bg='#e74c3c',
            fg='white',
            activebackground='#c0392b',
            activeforeground='white',
            command=self.deselect_all_permissions,
            **btn_style
        ).pack(side='left', padx=3)
        
        tk.Button(
            inner_toolbar,
            text="🔄 Restablecer",
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            activeforeground='white',
            command=self.reset_permissions,
            **btn_style
        ).pack(side='left', padx=3)
        
        # Buscador
        tk.Label(
            inner_toolbar,
            text="🔍",
            font=('Segoe UI', 14),
            bg='white'
        ).pack(side='right', padx=(15, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_permissions)
        
        search_entry = tk.Entry(
            inner_toolbar,
            textvariable=self.search_var,
            font=('Segoe UI', 10),
            width=25,
            relief='solid',
            bd=1
        )
        search_entry.pack(side='right')
    
    def create_permissions_area(self):
        """Crear área de permisos con scroll"""
        # Frame contenedor
        container = tk.Frame(self.dialog, bg='#f8f9fa')
        container.pack(fill='both', expand=True, padx=25, pady=10)
        
        # Canvas con scrollbar
        canvas = tk.Canvas(container, bg='#f8f9fa', highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        # Función mejorada para actualizar región de scroll y ancho
        def _configure_scroll(event):
            # Actualizar región de scroll
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Hacer que el frame interno ocupe todo el ancho del canvas
            canvas_width = canvas.winfo_width()
            canvas.itemconfig(window_id, width=canvas_width)
        
        self.scrollable_frame.bind("<Configure>", _configure_scroll)
        
        # Crear ventana en canvas y guardar ID
        window_id = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind para actualizar ancho cuando el canvas cambie de tamaño
        def _on_canvas_configure(event):
            canvas.itemconfig(window_id, width=event.width)
        
        canvas.bind("<Configure>", _on_canvas_configure)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Crear permisos por categoría
        self.create_permissions_by_category()
    
    def create_permissions_by_category(self):
        """Crear permisos organizados por categoría con diseño moderno"""
        try:
            print("\n" + "="*100)
            print("🔐 INICIANDO CREACIÓN DE INTERFAZ DE PERMISOS")
            print("="*100)
            
            permissions_by_category = self.role_controller.get_permissions_by_category()
            current_permissions = self.role.get('permissions', [])
            
            print(f"\n📋 ROL: {self.role.get('name')} (ID: {self.role.get('id')})")
            print(f"   Código: {self.role.get('code')}")
            print(f"\n📊 PERMISOS ACTUALES DEL ROL:")
            print(f"   Tipo: {type(current_permissions)}")
            print(f"   Valor: {current_permissions}")
            
            # Convertir si es JSON string
            if isinstance(current_permissions, str):
                import json
                try:
                    current_permissions = json.loads(current_permissions)
                    print(f"   ✓ Convertido desde JSON a lista")
                except:
                    current_permissions = []
                    print(f"   ⚠️ Error convirtiendo JSON, usando lista vacía")
            
            print(f"\n📂 CATEGORÍAS DISPONIBLES: {len(permissions_by_category)}")
            for cat_name, perms in permissions_by_category.items():
                print(f"   - {cat_name}: {len(perms)} permisos")
            
            # VALIDACIÓN ESPECIAL PARA MÓDULO DE USUARIOS
            print("\n" + "="*100)
            print("🔍 VALIDACIÓN DE PERMISOS DEL MÓDULO DE USUARIOS")
            print("="*100)
            
            users_permissions = permissions_by_category.get('Usuarios', [])
            print(f"\n📌 Permisos de Usuarios registrados en el sistema: {len(users_permissions)}")
            for perm in users_permissions:
                description = self.role_controller.get_permission_description(perm)
                has_it = perm in current_permissions or '*' in current_permissions
                status = "✅ TIENE" if has_it else "❌ NO TIENE"
                print(f"   {status} | {perm:<30} | {description}")
            
            print("\n" + "="*100)
            
            total_permissions = 0
            selected_permissions = 0
            
            for category_name, permissions in permissions_by_category.items():
                print(f"\n{'─'*100}")
                print(f"📂 PROCESANDO CATEGORÍA: {category_name}")
                print(f"   Total de permisos: {len(permissions)}")
                
                # Frame de categoría con diseño moderno
                category_container = tk.Frame(self.scrollable_frame, bg='#f8f9fa')
                category_container.pack(fill='x', pady=(0, 15))
                
                # Header de categoría
                category_header = tk.Frame(category_container, bg='white', relief='flat', bd=0)
                category_header.pack(fill='x', pady=(0, 5))
                
                # Variable para checkbox de categoría
                category_var = tk.BooleanVar()
                self.category_vars[category_name] = category_var
                
                print(f"   ✓ Variable de categoría creada: {type(category_var)}")
                
                # Checkbox de categoría (seleccionar toda la categoría)
                category_check_frame = tk.Frame(category_header, bg='#34495e', padx=15, pady=12)
                category_check_frame.pack(fill='x')
                
                def on_category_click(cat=category_name):
                    """Callback para checkbox de categoría"""
                    state = self.category_vars[cat].get()
                    print(f"\n🔘 CLICK EN CATEGORÍA: {cat}")
                    print(f"   Nuevo estado: {state}")
                    print(f"   Aplicando a {len(permissions_by_category[cat])} permisos...")
                    self.toggle_category(cat)
                
                category_checkbox = tk.Checkbutton(
                    category_check_frame,
                    variable=category_var,
                    command=on_category_click,
                    bg='#34495e',
                    activebackground='#34495e',
                    selectcolor='#2c3e50',
                    font=('Segoe UI', 11, 'bold'),
                    fg='white',
                    activeforeground='white',
                    cursor='hand2',
                    text=f"📂 {category_name}",
                    anchor='w',
                    indicatoron=1
                )
                category_checkbox.pack(side='left', fill='x', expand=True)
                
                # Contador de permisos de categoría
                category_count_label = tk.Label(
                    category_check_frame,
                    text=f"0/{len(permissions)}",
                    font=('Segoe UI', 10, 'bold'),
                    bg='#34495e',
                    fg='#bdc3c7'
                )
                category_count_label.pack(side='right')
                
                # Grid de permisos
                permissions_grid = tk.Frame(category_container, bg='white', relief='solid', bd=1)
                permissions_grid.pack(fill='x')
                
                for idx, permission in enumerate(permissions):
                    total_permissions += 1
                    
                    # 1️⃣ Crear variable CON MASTER EXPLÍCITO (esto es crítico para que funcione)
                    var = tk.BooleanVar(master=self.dialog)
                    
                    # 2️⃣ Guardar en diccionario PRIMERO
                    self.permission_vars[permission] = var
                    
                    # 3️⃣ Verificar si tiene el permiso
                    has_permission = permission in current_permissions or '*' in current_permissions
                    
                    if has_permission:
                        selected_permissions += 1
                    
                    # Frame del permiso (tarjeta)
                    perm_frame = tk.Frame(
                        permissions_grid,
                        bg='#f8f9fa' if idx % 2 == 0 else 'white',
                        relief='flat',
                        bd=0
                    )
                    perm_frame.pack(fill='both', expand=True, padx=10, pady=3)
                    self.permission_frames[permission] = perm_frame
                    
                    # Contenedor interno que ocupa todo el ancho
                    inner_frame = tk.Frame(perm_frame, bg=perm_frame['bg'], padx=10, pady=8)
                    inner_frame.pack(fill='both', expand=True)
                    
                    # Obtener descripción del permiso
                    description = self.role_controller.get_permission_description(permission)
                    
                    # 4️⃣ Configurar el valor inicial ANTES de agregar trace
                    var.set(has_permission)
                    
                    # 5️⃣ Crear función de callback que se ejecutará DESPUÉS del click
                    def make_update_callback(cat_name, cat_label, perm_name):
                        """Factory para crear callback con closure correcto"""
                        def callback():
                            # Verificar el estado actual
                            current_state = self.permission_vars[perm_name].get()
                            print(f"🔔 CLICK en {perm_name}: estado ahora es {current_state}")
                            # Usar after para ejecutar DESPUÉS de que Tkinter actualice la variable
                            self.dialog.after(1, lambda: self.update_counters(cat_name, cat_label))
                        return callback
                    
                    # Checkbox del permiso con texto incluido
                    perm_checkbox = tk.Checkbutton(
                        inner_frame,
                        text=f"{permission} - {description}",
                        variable=var,
                        command=make_update_callback(category_name, category_count_label, permission),  # ✅ Con callback
                        bg=perm_frame['bg'],
                        activebackground=perm_frame['bg'],
                        selectcolor='#4CAF50',  # ✅ VERDE cuando está marcado
                        cursor='hand2',
                        font=('Segoe UI', 10),
                        fg='#2c3e50',
                        activeforeground='#2c3e50',
                        indicatoron=1,  # ✅ MOSTRAR CHECKBOX (cuadrito con checkmark)
                        onvalue=True,   # ✅ Valor cuando está marcado
                        offvalue=False, # ✅ Valor cuando NO está marcado
                        anchor='w',
                        wraplength=700,
                        justify='left',
                        relief='flat',  # Sin relieve
                        borderwidth=0   # Sin borde
                    )
                    perm_checkbox.pack(fill='x', expand=True)
                    
                    # Log de creación
                    print(f"✓ Checkbox creado: {permission} | Estado inicial: {var.get()} | ID: {id(perm_checkbox)}")
                
                # Actualizar estado inicial de checkbox de categoría
                self.update_category_checkbox(category_name, update_count=False)
            
            # Actualizar contador global
            self.update_global_counter()
            
            # RESUMEN FINAL
            print("\n" + "="*100)
            print("✅ INTERFAZ DE PERMISOS CREADA EXITOSAMENTE")
            print("="*100)
            print(f"\n📊 RESUMEN:")
            print(f"   Total de categorías: {len(permissions_by_category)}")
            print(f"   Total de permisos: {len(self.permission_vars)}")
            print(f"   Permisos seleccionados: {sum(1 for var in self.permission_vars.values() if var.get())}")
            print(f"\n🎯 ESTADO DE CHECKBOXES:")
            print(f"   Variables creadas: {len(self.permission_vars)}")
            print(f"   Frames creados: {len(self.permission_frames)}")
            print(f"   Categorías: {len(self.category_vars)}")
            
            print(f"\n🔍 VALIDACIÓN DE WIDGETS:")
            sample_count = 0
            for perm, var in list(self.permission_vars.items())[:5]:
                print(f"   - {perm}")
                print(f"     Tipo variable: {type(var)}")
                print(f"     Estado: {var.get()}")
                sample_count += 1
            
            if len(self.permission_vars) > 5:
                print(f"   ... y {len(self.permission_vars) - 5} permisos más")
            
            print("\n" + "="*100)
            print("🚀 INTERFAZ LISTA PARA USO")
            print("="*100 + "\n")
            
        except Exception as e:
            print(f"\n❌ ERROR CREANDO INTERFAZ:")
            print(f"   {str(e)}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error creando interfaz de permisos:\n{str(e)}")
    
    def toggle_category(self, category_name):
        """Activar/desactivar todos los permisos de una categoría"""
        print(f"\n🔄 TOGGLE_CATEGORY: {category_name}")
        
        permissions_by_category = self.role_controller.get_permissions_by_category()
        permissions = permissions_by_category.get(category_name, [])
        
        # Obtener estado del checkbox de categoría
        category_state = self.category_vars[category_name].get()
        
        print(f"   Estado de categoría: {category_state}")
        print(f"   Permisos a modificar: {len(permissions)}")
        
        # Aplicar a todos los permisos de la categoría
        for permission in permissions:
            if permission in self.permission_vars:
                old_state = self.permission_vars[permission].get()
                self.permission_vars[permission].set(category_state)
                print(f"   - {permission}: {old_state} → {category_state}")
        
        print(f"   ✓ Todos los permisos actualizados")
    
    def update_category_checkbox(self, category_name, update_count=True):
        """Actualizar estado del checkbox de categoría basado en sus permisos"""
        permissions_by_category = self.role_controller.get_permissions_by_category()
        permissions = permissions_by_category.get(category_name, [])
        
        # Contar permisos seleccionados
        selected_count = sum(1 for p in permissions 
                           if p in self.permission_vars and self.permission_vars[p].get())
        
        print(f"\n📊 UPDATE_CATEGORY_CHECKBOX: {category_name}")
        print(f"   Permisos seleccionados: {selected_count}/{len(permissions)}")
        
        # Actualizar checkbox de categoría
        if category_name in self.category_vars:
            if selected_count == 0:
                self.category_vars[category_name].set(False)
                print(f"   → Categoría desmarcada (0 permisos)")
            elif selected_count == len(permissions):
                self.category_vars[category_name].set(True)
                print(f"   → Categoría marcada (todos los permisos)")
            else:
                print(f"   → Categoría parcial ({selected_count}/{len(permissions)})")
        
        if update_count:
            self.update_global_counter()
    
    def update_counters(self, category_name, label):
        """Actualizar contador de permisos de una categoría"""
        permissions_by_category = self.role_controller.get_permissions_by_category()
        permissions = permissions_by_category.get(category_name, [])
        
        selected_count = sum(1 for p in permissions 
                           if p in self.permission_vars and self.permission_vars[p].get())
        
        print(f"\n📈 UPDATE_COUNTERS: {category_name}")
        print(f"   Contador actualizado: {selected_count}/{len(permissions)}")
        
        label.config(text=f"{selected_count}/{len(permissions)}")
        self.update_global_counter()
    
    def update_global_counter(self):
        """Actualizar contador global de permisos"""
        total = len(self.permission_vars)
        selected = sum(1 for var in self.permission_vars.values() if var.get())
        
        print(f"\n🌐 CONTADOR GLOBAL: {selected}/{total} permisos seleccionados")
        
        self.counter_label.config(
            text=f"{selected} / {total} permisos",
            fg='#27ae60' if selected > 0 else 'white'
        )
    
    def filter_permissions(self, *args):
        """Filtrar permisos por búsqueda"""
        search_text = self.search_var.get().lower()
        
        for permission, frame in self.permission_frames.items():
            description = self.role_controller.get_permission_description(permission).lower()
            
            if search_text in permission.lower() or search_text in description:
                frame.pack(fill='x', padx=10, pady=3)
            else:
                frame.pack_forget()
    
    def select_all_permissions(self):
        """Seleccionar todos los permisos"""
        print("\n" + "🟢"*50)
        print("✅ SELECCIONAR TODO - INICIADO")
        print("🟢"*50)
        
        count = 0
        for permission, var in self.permission_vars.items():
            old_state = var.get()
            var.set(True)
            if not old_state:
                count += 1
                print(f"   ✓ {permission}: False → True")
        
        print(f"\n   Total modificados: {count}/{len(self.permission_vars)}")
        
        # Actualizar checkboxes de categorías
        for category_name, category_var in self.category_vars.items():
            category_var.set(True)
            print(f"   ✓ Categoría '{category_name}': marcada")
        
        self.update_global_counter()
        print("🟢"*50 + "\n")
    
    def deselect_all_permissions(self):
        """Deseleccionar todos los permisos"""
        print("\n" + "🔴"*50)
        print("❌ DESELECCIONAR TODO - INICIADO")
        print("🔴"*50)
        
        count = 0
        for permission, var in self.permission_vars.items():
            old_state = var.get()
            var.set(False)
            if old_state:
                count += 1
                print(f"   ✓ {permission}: True → False")
        
        print(f"\n   Total modificados: {count}/{len(self.permission_vars)}")
        
        # Actualizar checkboxes de categorías
        for category_name, category_var in self.category_vars.items():
            category_var.set(False)
            print(f"   ✓ Categoría '{category_name}': desmarcada")
        
        self.update_global_counter()
        print("🔴"*50 + "\n")
    
    def reset_permissions(self):
        """Restablecer permisos originales"""
        print("\n" + "🔵"*50)
        print("🔄 RESTABLECER - INICIADO")
        print("🔵"*50)
        
        current_permissions = self.role.get('permissions', [])
        
        # Convertir si es JSON string
        if isinstance(current_permissions, str):
            import json
            try:
                current_permissions = json.loads(current_permissions)
            except:
                current_permissions = []
        
        print(f"\n   Permisos originales: {len(current_permissions)}")
        print(f"   Permisos a restaurar: {current_permissions}\n")
        
        modified = 0
        for permission, var in self.permission_vars.items():
            should_be_checked = permission in current_permissions or '*' in current_permissions
            old_state = var.get()
            var.set(should_be_checked)
            
            if old_state != should_be_checked:
                modified += 1
                print(f"   ✓ {permission}: {old_state} → {should_be_checked}")
        
        print(f"\n   Total modificados: {modified}/{len(self.permission_vars)}")
        
        # Actualizar checkboxes de categorías
        permissions_by_category = self.role_controller.get_permissions_by_category()
        for category_name in permissions_by_category.keys():
            self.update_category_checkbox(category_name)
        
        self.update_global_counter()
        print("🔵"*50 + "\n")
    
    def create_footer(self):
        """Crear footer con botones de acción"""
        footer_frame = tk.Frame(self.dialog, bg='white', height=70)
        footer_frame.pack(fill='x', side='bottom', pady=(10, 0))
        footer_frame.pack_propagate(False)
        
        button_container = tk.Frame(footer_frame, bg='white')
        button_container.pack(expand=True, pady=15)
        
        btn_style = {
            'font': ('Segoe UI', 12, 'bold'),
            'cursor': 'hand2',
            'relief': 'flat',
            'padx': 30,
            'pady': 12,
            'bd': 0
        }
        
        # Botón Cancelar
        tk.Button(
            button_container,
            text="❌ Cancelar",
            bg='#95a5a6',
            fg='white',
            activebackground='#7f8c8d',
            activeforeground='white',
            command=self.cancel,
            **btn_style
        ).pack(side='right', padx=5)
        
        # Botón Guardar
        tk.Button(
            button_container,
            text="💾 Guardar Permisos",
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            activeforeground='white',
            command=self.save,
            **btn_style
        ).pack(side='right', padx=5)
    
    def save(self):
        """Guardar permisos"""
        print("\n🚨🚨🚨 MÉTODO save() LLAMADO 🚨🚨🚨\n")
        try:
            print("\n" + "="*80)
            print("💾 GUARDAR PERMISOS - INICIADO")
            print("="*80)
            
            print(f"\n🔍 DIAGNÓSTICO DE VARIABLES:")
            print(f"   Total de permission_vars: {len(self.permission_vars)}")
            print(f"   Tipo de permission_vars: {type(self.permission_vars)}")
            
            # 🔍 LOGS DETALLADOS: Mostrar TODOS los estados
            print(f"\n📋 ESTADO COMPLETO DE TODAS LAS VARIABLES:")
            true_count = 0
            false_count = 0
            for perm, var in self.permission_vars.items():
                state = var.get()
                if state:
                    true_count += 1
                    print(f"   ✅ TRUE:  {perm}")
                else:
                    false_count += 1
            
            print(f"\n📊 RESUMEN DE ESTADOS:")
            print(f"   Variables con TRUE:  {true_count}")
            print(f"   Variables con FALSE: {false_count}")
            print(f"   Total: {true_count + false_count}")
            
            # Obtener permisos seleccionados
            selected_permissions = [
                permission for permission, var in self.permission_vars.items()
                if var.get()
            ]
            
            print(f"\n📊 PERMISOS SELECCIONADOS: {len(selected_permissions)}/60")
            
            # Mostrar estado de cada variable (primeros 10)
            print(f"\n� ESTADO DE VARIABLES (primeros 10):")
            count = 0
            for permission, var in self.permission_vars.items():
                if count < 10:
                    print(f"   {permission}: {var.get()} (tipo: {type(var)})")
                    count += 1
            
            print(f"\n�📝 LISTA DE PERMISOS SELECCIONADOS:")
            for perm in sorted(selected_permissions)[:10]:
                print(f"   ✓ {perm}")
            if len(selected_permissions) > 10:
                print(f"   ... y {len(selected_permissions) - 10} más")
            
            # Guardar resultado
            print(f"\n🔧 GUARDANDO EN self.result...")
            self.result = selected_permissions
            
            print(f"✅ self.result establecido")
            print(f"   Tipo: {type(self.result)}")
            print(f"   Longitud: {len(self.result)}")
            print(f"   Contenido (primeros 5): {self.result[:5] if len(self.result) > 0 else '[]'}")
            print(f"   self.result is None: {self.result is None}")
            print(f"   bool(self.result): {bool(self.result)}")
            print("="*80 + "\n")
            
            # Cerrar diálogo
            print("🔒 Cerrando diálogo...")
            self.dialog.destroy()
            print("✅ Diálogo cerrado")
            
        except Exception as e:
            print(f"\n❌ ERROR en save(): {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error guardando permisos:\n{str(e)}")
    
    def cancel(self):
        """Cancelar"""
        self.result = None
        self.dialog.destroy()
