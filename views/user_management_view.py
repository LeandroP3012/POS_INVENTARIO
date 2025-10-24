"""
Vista de Gestión de Usuarios
Panel completo para administrar usuarios del sistema
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, List, Callable, Optional
import hashlib
from datetime import datetime
from views.base_view import BaseView
from controllers.user_controller import UserController
from controllers.role_controller import RoleController
from services.permission_service import PermissionService


class UserManagementView(BaseView):
    """Vista completa de gestión de usuarios"""
    
    def __init__(self, root: tk.Tk, user_data: Dict[str, Any] = None, embedded: bool = True):
        super().__init__(root)
        self.user_data = user_data or {}
        self.embedded = embedded
        self.users_data = []
        self.filtered_users = []
        self.selected_user = None
        self.roles_data = []
        
        # Inicializar controladores y servicios
        self.user_controller = UserController()
        self.role_controller = RoleController()
        self.permission_service = PermissionService()
        
        # Configurar ventana
        self.setup_user_management_window()
        
        # Cargar datos iniciales
        self.load_roles_data()
        self.load_users_data()
    
    def has_permission(self, permission: str) -> bool:
        """Verificar si el usuario actual tiene un permiso específico"""
        try:
            return self.permission_service.check_permission(self.user_data, permission)
        except Exception as e:
            print(f"Error verificando permiso {permission}: {e}")
            return False
    
    def setup_user_management_window(self):
        """Configurar ventana de gestión de usuarios"""
        if not self.embedded:
            self.root.title("Sistema POS - Gestión de Usuarios")
            self.root.geometry("1400x900") 
            self.root.configure(bg='#f8f9fa')
            self.center_window(1400, 900)
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        else:
            self.root.configure(bg='#f8f9fa')
        
        self.create_user_management_interface()
    
    def create_user_management_interface(self):
        """Crear interfaz de gestión de usuarios"""
        # Header
        self.create_header()
        
        # Navbar
        self.create_navbar()
        
        # Toolbar con búsqueda y botones
        self.create_toolbar()
        
        # Panel principal con tabla y detalles
        self.create_main_panel()
        
        # Footer con estadísticas
        self.create_footer()
    
    def create_header(self):
        """Crear header de gestión de usuarios"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        content_frame = tk.Frame(header_frame, bg='#2c3e50')
        content_frame.pack(expand=True, fill='both', padx=30, pady=15)
        
        # Título (izquierda)
        title_label = tk.Label(
            content_frame,
            text="👥 Gestión de Usuarios",
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
                command=self.go_back_to_dashboard,
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
        user_text = f"Usuario: {self.user_data.get('full_name', self.user_data.get('username', 'Admin'))}"
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
            file_menu.add_command(label="Volver al Dashboard", command=self.go_back_to_dashboard)
        
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
        admin_menu.add_command(label="Gestionar Usuarios", command=self.callbacks.get('refresh', lambda: None))
        if hasattr(self, 'manage_roles_callback') and self.manage_roles_callback:
            admin_menu.add_command(label="Gestionar Roles", command=self.manage_roles_callback)
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
            text="🔍 Buscar usuario:",
            font=('Segoe UI', 13, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left', padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self.on_search_change)
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 13),
            width=28,
            relief='solid',
            bd=1
        )
        search_entry.pack(side='left', padx=(0, 15), ipady=8)
        
        # Filtro por rol
        tk.Label(
            search_frame,
            text="Rol:",
            font=('Segoe UI', 13, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left', padx=(25, 8))
        
        self.role_filter_var = tk.StringVar(value='Todos')
        # Obtener valores de roles dinámicamente
        role_values = ['Todos'] + [role.get('name', '') for role in self.roles_data if role.get('active', True)]
        role_combo = ttk.Combobox(
            search_frame,
            textvariable=self.role_filter_var,
            values=role_values,
            state='readonly',
            width=18,
            font=('Segoe UI', 12)
        )
        role_combo.pack(side='left', padx=(0, 15))
        role_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # Frame derecho - Botones de acción
        buttons_frame = tk.Frame(inner_frame, bg='white')
        buttons_frame.pack(side='right', fill='y')
        
        # Botón nuevo usuario - Solo si tiene permiso users.create
        if self.has_permission('users.create'):
            new_user_btn = tk.Button(
                buttons_frame,
                text="➕ Nuevo Usuario",
                command=self.create_new_user,
                bg='#27ae60',
                fg='white',
                font=('Segoe UI', 13, 'bold'),
                relief='flat',
                cursor='hand2',
                padx=20,
                pady=12
            )
            new_user_btn.pack(side='left', padx=(0, 12))
        
        # Botón editar - Solo si tiene permiso users.edit
        if self.has_permission('users.edit'):
            self.edit_user_btn = tk.Button(
                buttons_frame,
                text="✏️ Editar",
                command=self.edit_selected_user,
                bg='#3498db',
                fg='white',
                font=('Segoe UI', 13, 'bold'),
                relief='flat',
                cursor='hand2',
                padx=20,
                pady=12,
                state='disabled'
            )
            self.edit_user_btn.pack(side='left', padx=(0, 12))
        else:
            self.edit_user_btn = None
        
        # Botón eliminar - Solo si tiene permiso users.delete
        if self.has_permission('users.delete'):
            self.delete_user_btn = tk.Button(
                buttons_frame,
                text="🗑️ Eliminar",
                command=self.delete_selected_user,
                bg='#e74c3c',
                fg='white',
                font=('Segoe UI', 13, 'bold'),
                relief='flat',
                cursor='hand2',
                padx=20,
                pady=12,
                state='disabled'
            )
            self.delete_user_btn.pack(side='left')
        else:
            self.delete_user_btn = None
    
    def create_main_panel(self):
        """Crear panel principal con tabla de usuarios"""
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
            text="📋 Lista de Usuarios del Sistema",
            font=('Segoe UI', 16, 'bold'),
            fg='white',
            bg='#34495e'
        ).pack(side='left', padx=25, pady=15)
        
        # Contador de usuarios
        self.user_count_label = tk.Label(
            table_header,
            text="0 usuarios",
            font=('Segoe UI', 13),
            fg='#bdc3c7',
            bg='#34495e'
        )
        self.user_count_label.pack(side='right', padx=25, pady=15)
        
        # Crear Treeview para la tabla
        self.create_users_table(table_frame)
    
    def create_users_table(self, parent):
        """Crear tabla de usuarios con Treeview"""
        # Frame para tabla y scrollbars
        tree_frame = tk.Frame(parent, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Configurar columnas
        columns = ('id', 'username', 'full_name', 'user_type', 'email', 'status', 'last_login', 'created_at')
        column_names = {
            'id': 'ID',
            'username': 'Usuario',
            'full_name': 'Nombre Completo',
            'user_type': 'Rol',
            'email': 'Email',
            'status': 'Estado',
            'last_login': 'Último Acceso',
            'created_at': 'Creado'
        }
        
        # Crear Treeview
        self.users_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='tree headings',
            height=18
        )
        
        # Configurar columnas
        self.users_tree.column('#0', width=0, stretch=False)  # Ocultar primera columna
        self.users_tree.column('id', width=60, anchor='center')
        self.users_tree.column('username', width=140, anchor='w')
        self.users_tree.column('full_name', width=250, anchor='w')
        self.users_tree.column('user_type', width=140, anchor='center')
        self.users_tree.column('email', width=250, anchor='w')
        self.users_tree.column('status', width=100, anchor='center')
        self.users_tree.column('last_login', width=180, anchor='center')
        self.users_tree.column('created_at', width=180, anchor='center')
        
        # Configurar headers
        for col in columns:
            self.users_tree.heading(col, text=column_names[col], anchor='center')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.users_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.users_tree.xview)
        
        self.users_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars y tree
        self.users_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind eventos
        self.users_tree.bind('<<TreeviewSelect>>', self.on_user_select)
        self.users_tree.bind('<Double-Button-1>', self.on_user_double_click)
        
        # Configurar estilo para filas alternadas
        style = ttk.Style()
        style.configure('Treeview', rowheight=30, font=('Segoe UI', 11))
        style.configure('Treeview.Heading', font=('Segoe UI', 12, 'bold'))
    
    def create_footer(self):
        """Crear footer con estadísticas"""
        footer_frame = tk.Frame(self.root, bg='#ecf0f1', height=60)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        inner_frame = tk.Frame(footer_frame, bg='#ecf0f1')
        inner_frame.pack(expand=True, fill='both', padx=25, pady=15)
        
        # Estadísticas
        self.stats_label = tk.Label(
            inner_frame,
            text="👥 Total: 0 | ✅ Activos: 0 | ❌ Inactivos: 0 | 👑 Admins: 0",
            font=('Segoe UI', 12, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        )
        self.stats_label.pack(side='left')
        
        # Información de la sesión actual
        session_info = f"Sesión actual: {self.user_data.get('username', 'admin')} ({self.user_data.get('user_type', 'admin')})"
        tk.Label(
            inner_frame,
            text=session_info,
            font=('Segoe UI', 12),
            fg='#7f8c8d',
            bg='#ecf0f1'
        ).pack(side='right')
    
    def load_roles_data(self):
        """Cargar datos de roles desde el controlador"""
        try:
            self.roles_data = self.role_controller.get_all_roles()
        except Exception as e:
            print(f"Error cargando roles: {str(e)}")
            # Roles por defecto como fallback
            self.roles_data = [
                {'id': 1, 'name': 'Super Admin', 'active': True},
                {'id': 2, 'name': 'Admin', 'active': True},
                {'id': 3, 'name': 'Manager', 'active': True},
                {'id': 4, 'name': 'Employee', 'active': True},
                {'id': 5, 'name': 'Cashier', 'active': True}
            ]
    
    def load_users_data(self):
        """Cargar datos de usuarios desde el controlador"""
        try:
            self.users_data = self.user_controller.get_all_users()
            self.filtered_users = self.users_data.copy()
            self.update_users_table()
            self.update_statistics()
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando usuarios: {str(e)}")
            # Datos de fallback en caso de error
            self.users_data = []
            self.filtered_users = []
    
    def update_users_table(self):
        """Actualizar tabla de usuarios"""
        # Limpiar tabla
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Llenar tabla con datos filtrados
        for user in self.filtered_users:
            # Formatear fechas
            last_login = self.format_datetime(user.get('last_login', ''))
            created_at = self.format_datetime(user.get('created_at', ''))
            
            # Formatear estado
            status_display = '✅ Activo' if user.get('status', 'active') == 'active' else '❌ Inactivo'
            
            # Insertar fila
            item = self.users_tree.insert('', 'end', values=(
                user.get('id', ''),
                user.get('username', ''),
                user.get('full_name', ''),
                user.get('user_type', ''),
                user.get('email', ''),
                status_display,
                last_login,
                created_at
            ))
        
        # Actualizar contador
        self.user_count_label.configure(text=f"{len(self.filtered_users)} usuarios")
    
    def update_statistics(self):
        """Actualizar estadísticas del footer"""
        total = len(self.users_data)
        active = len([u for u in self.users_data if u.get('status', 'active') == 'active'])
        inactive = total - active
        admins = len([u for u in self.users_data if u.get('user_type', '') == 'admin'])
        
        stats_text = f"👥 Total: {total} | ✅ Activos: {active} | ❌ Inactivos: {inactive} | 👑 Admins: {admins}"
        self.stats_label.configure(text=stats_text)
    
    def on_search_change(self, *args):
        """Manejar cambio en búsqueda"""
        self.apply_filters()
    
    def on_filter_change(self, event=None):
        """Manejar cambio en filtros"""
        self.apply_filters()
    
    def apply_filters(self):
        """Aplicar filtros de búsqueda y rol"""
        search_term = self.search_var.get().lower()
        role_filter = self.role_filter_var.get()
        
        self.filtered_users = []
        
        for user in self.users_data:
            # Filtro de búsqueda
            search_match = (
                search_term in user.get('username', '').lower() or
                search_term in user.get('full_name', '').lower() or
                search_term in user.get('email', '').lower()
            )
            
            # Filtro de rol - buscar tanto en user_type como en el nombre del rol
            user_role = user.get('user_type', '')
            # Intentar encontrar el rol en el sistema de roles
            role_name = user_role
            for role in self.roles_data:
                if role.get('name', '').lower() == user_role.lower():
                    role_name = role.get('name', '')
                    break
            
            role_match = role_filter == 'Todos' or user_role == role_filter or role_name == role_filter
            
            if search_match and role_match:
                self.filtered_users.append(user)
        
        self.update_users_table()
    
    def on_user_select(self, event):
        """Manejar selección de usuario en la tabla"""
        selection = self.users_tree.selection()
        if selection:
            item = selection[0]
            values = self.users_tree.item(item, 'values')
            user_id = int(values[0]) if values[0] else 0
            
            # Buscar usuario seleccionado
            self.selected_user = next((u for u in self.users_data if u.get('id') == user_id), None)
            
            # Habilitar botón editar solo si tiene permiso users.edit
            if self.edit_user_btn:
                self.edit_user_btn.configure(state='normal')
            
            # Habilitar botón eliminar solo si:
            # 1. Tiene permiso users.delete
            # 2. No es el usuario actual
            if self.delete_user_btn:
                if self.selected_user and self.selected_user.get('username') != self.user_data.get('username', ''):
                    self.delete_user_btn.configure(state='normal')
                else:
                    self.delete_user_btn.configure(state='disabled')
        else:
            self.selected_user = None
            if self.edit_user_btn:
                self.edit_user_btn.configure(state='disabled')
            if self.delete_user_btn:
                self.delete_user_btn.configure(state='disabled')
    
    def on_user_double_click(self, event):
        """Manejar doble clic en usuario"""
        if self.selected_user:
            self.edit_selected_user()
    
    def create_new_user(self):
        """Crear nuevo usuario"""
        # Verificar permiso
        if not self.has_permission('users.create'):
            messagebox.showerror("Acceso Denegado", "❌ No tienes permisos para crear usuarios")
            return
        
        dialog = UserDialog(self.root, "Crear Nuevo Usuario", None, self.roles_data)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            try:
                # Crear usuario a través del controlador
                success = self.user_controller.create_user(dialog.result)
                if success:
                    self.load_users_data()  # Recargar datos
                    messagebox.showinfo("Usuario Creado", f"✅ Usuario '{dialog.result['username']}' creado exitosamente")
                else:
                    messagebox.showerror("Error", "❌ Error creando el usuario")
            except Exception as e:
                messagebox.showerror("Error", f"❌ Error creando usuario: {str(e)}")
    
    def edit_selected_user(self):
        """Editar usuario seleccionado"""
        if not self.selected_user:
            return
        
        # Verificar permiso
        if not self.has_permission('users.edit'):
            messagebox.showerror("Acceso Denegado", "❌ No tienes permisos para editar usuarios")
            return
        
        dialog = UserDialog(self.root, "Editar Usuario", self.selected_user, self.roles_data)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            try:
                # Actualizar usuario a través del controlador
                success = self.user_controller.update_user(self.selected_user['id'], dialog.result)
                if success:
                    self.load_users_data()  # Recargar datos
                    messagebox.showinfo("Usuario Actualizado", f"✅ Usuario '{dialog.result['username']}' actualizado exitosamente")
                else:
                    messagebox.showerror("Error", "❌ Error actualizando el usuario")
            except Exception as e:
                messagebox.showerror("Error", f"❌ Error actualizando usuario: {str(e)}")
    
    def delete_selected_user(self):
        """Eliminar usuario seleccionado"""
        if not self.selected_user:
            return
        
        # Verificar permiso
        if not self.has_permission('users.delete'):
            messagebox.showerror("Acceso Denegado", "❌ No tienes permisos para eliminar usuarios")
            return
        
        # Confirmar eliminación
        if messagebox.askyesno("Confirmar Eliminación", 
                             f"⚠️ ¿Está seguro de que desea eliminar al usuario '{self.selected_user.get('full_name', '')}'?\n\n"
                             f"Esta acción no se puede deshacer."):
            
            try:
                # Eliminar usuario a través del controlador
                success = self.user_controller.delete_user(self.selected_user['id'])
                if success:
                    self.selected_user = None
                    self.load_users_data()  # Recargar datos
                    if self.edit_user_btn:
                        self.edit_user_btn.configure(state='disabled')
                    if self.delete_user_btn:
                        self.delete_user_btn.configure(state='disabled')
                    messagebox.showinfo("Usuario Eliminado", "✅ Usuario eliminado exitosamente")
                else:
                    messagebox.showerror("Error", "❌ Error eliminando el usuario")
            except Exception as e:
                messagebox.showerror("Error", f"❌ Error eliminando usuario: {str(e)}")
    
    def format_datetime(self, datetime_str: str) -> str:
        """Formatear fecha y hora"""
        if not datetime_str or datetime_str == 'Nunca' or datetime_str is None:
            return 'Nunca'
        
        try:
            # Intentar varios formatos de fecha
            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y %H:%M:%S', '%d/%m/%Y']:
                try:
                    dt = datetime.strptime(str(datetime_str), fmt)
                    return dt.strftime('%d/%m/%Y %H:%M')
                except:
                    continue
            return str(datetime_str)
        except:
            return str(datetime_str)
    
    def go_back_to_dashboard(self):
        """Volver al dashboard"""
        self.trigger_callback('back_to_dashboard')
    
    def on_close(self):
        """Manejar cierre de ventana"""
        if self.embedded:
            self.go_back_to_dashboard()
        else:
            self.root.destroy()
    
    def center_window(self, width, height):
        """Centrar ventana en la pantalla"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")


class UserDialog:
    """Diálogo para crear/editar usuarios"""
    
    def __init__(self, parent, title: str, user_data: Dict = None, roles_data: List = None):
        self.parent = parent
        self.user_data = user_data or {}
        self.result = None
        self.is_edit = bool(user_data)
        self.roles_data = roles_data or []
        
        # Inicializar variables PRIMERO
        self.username_var = tk.StringVar(value=self.user_data.get('username', '') if self.user_data else '')
        self.full_name_var = tk.StringVar(value=self.user_data.get('full_name', '') if self.user_data else '')
        self.email_var = tk.StringVar(value=self.user_data.get('email', '') if self.user_data else '')
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()
        
        # Para el rol, usar el rol del usuario o el primer rol disponible como default
        default_role = self.user_data.get('user_type', '') if self.user_data else ''
        if not default_role and self.roles_data:
            # Si no hay rol seleccionado, usar el último rol (generalmente Cajero)
            default_role = self.roles_data[-1].get('name', 'Cajero')
        
        self.user_type_var = tk.StringVar(value=default_role)
        self.status_var = tk.StringVar(value='active' if self.user_data and self.user_data.get('status', 'active') == 'active' else 'active')
        
        # Crear ventana de diálogo
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("600x750")
        self.dialog.configure(bg='white')
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar diálogo
        self.center_dialog()
        
        # Crear interfaz
        self.create_dialog_interface()
        
        # Enfocar primer campo y forzar actualización
        self.dialog.after(100, lambda: self.username_entry.focus_set())
    
    def create_dialog_interface(self):
        """Crear interfaz del diálogo"""
        # Header
        header_frame = tk.Frame(self.dialog, bg='#3498db', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        icon = "✏️" if self.is_edit else "➕"
        title_text = "Editar Usuario" if self.is_edit else "Crear Nuevo Usuario"
        
        tk.Label(
            header_frame,
            text=f"{icon} {title_text}",
            font=('Segoe UI', 20, 'bold'),
            fg='white',
            bg='#3498db'
        ).pack(expand=True)
        
        # Contenedor principal con Canvas para scroll
        main_container = tk.Frame(self.dialog, bg='white')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Canvas con scrollbar
        canvas = tk.Canvas(main_container, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient='vertical', command=canvas.yview)
        
        # Frame que contendrá todo el contenido scrolleable
        content_frame = tk.Frame(canvas, bg='white')
        
        # Configurar el canvas
        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content_frame, anchor='nw', width=560)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar canvas y scrollbar
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Habilitar scroll con rueda del ratón
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Padding interno para el contenido
        inner_frame = tk.Frame(content_frame, bg='white')
        inner_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Campos del formulario usando pack para simplicidad
        # Username
        tk.Label(inner_frame, text="👤 Nombre de Usuario:", bg='white', 
                font=('Segoe UI', 12, 'bold'), fg='#2c3e50').pack(anchor='w', pady=(0, 5))
        self.username_entry = tk.Entry(inner_frame, textvariable=self.username_var, 
                                      font=('Segoe UI', 11), relief='solid', bd=1)
        self.username_entry.pack(fill='x', pady=(0, 15))
        
        # Si hay datos existentes, forzar actualización visual
        if self.user_data and self.user_data.get('username'):
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, self.user_data.get('username', ''))
        
        # Full name
        tk.Label(inner_frame, text="📝 Nombre Completo:", bg='white',
                font=('Segoe UI', 12, 'bold'), fg='#2c3e50').pack(anchor='w', pady=(0, 5))
        self.fullname_entry = tk.Entry(inner_frame, textvariable=self.full_name_var, 
                font=('Segoe UI', 11), relief='solid', bd=1)
        self.fullname_entry.pack(fill='x', pady=(0, 15))
        
        # Si hay datos existentes, forzar actualización visual
        if self.user_data and self.user_data.get('full_name'):
            self.fullname_entry.delete(0, tk.END)
            self.fullname_entry.insert(0, self.user_data.get('full_name', ''))
        
        # Email
        tk.Label(inner_frame, text="📧 Email:", bg='white',
                font=('Segoe UI', 12, 'bold'), fg='#2c3e50').pack(anchor='w', pady=(0, 5))
        self.email_entry = tk.Entry(inner_frame, textvariable=self.email_var, 
                font=('Segoe UI', 11), relief='solid', bd=1)
        self.email_entry.pack(fill='x', pady=(0, 15))
        
        # Si hay datos existentes, forzar actualización visual
        if self.user_data and self.user_data.get('email'):
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, self.user_data.get('email', ''))
        
        # User Type (Role)
        tk.Label(inner_frame, text="🎭 Rol:", bg='white',
                font=('Segoe UI', 12, 'bold'), fg='#2c3e50').pack(anchor='w', pady=(0, 5))
        
        # Obtener valores de roles dinámicamente
        role_values = [role.get('name', '') for role in self.roles_data if role.get('active', True)]
        if not role_values:  # Fallback si no hay roles
            role_values = ['Admin', 'Manager', 'Employee', 'Cashier']
        
        user_type_combo = ttk.Combobox(inner_frame, textvariable=self.user_type_var,
                                      values=role_values, state='readonly', font=('Segoe UI', 11))
        user_type_combo.pack(fill='x', pady=(0, 15))
        
        # Si hay datos existentes, forzar actualización visual del rol
        if self.user_data and self.user_data.get('user_type'):
            user_type = self.user_data.get('user_type', '')
            # Buscar el nombre del rol correspondiente
            for role in self.roles_data:
                if role.get('name', '').lower() == user_type.lower() or role.get('code', '').lower() == user_type.lower():
                    user_type_combo.set(role.get('name', ''))
                    break
            else:
                # Si no se encuentra, usar el valor directo
                user_type_combo.set(user_type)
        
        # Status (solo en edición)
        if self.is_edit:
            tk.Label(inner_frame, text="📊 Estado:", bg='white',
                    font=('Segoe UI', 12, 'bold'), fg='#2c3e50').pack(anchor='w', pady=(0, 5))
            
            status_combo = ttk.Combobox(inner_frame, textvariable=self.status_var,
                                       values=['activo', 'inactivo'], state='readonly', font=('Segoe UI', 11))
            status_combo.pack(fill='x', pady=(0, 15))
            
            # Si hay datos existentes, forzar actualización visual del estado
            if self.user_data:
                current_status = self.user_data.get('status', 'activo')
                # Normalizar el valor del estado
                status_value = 'activo' if current_status in ['active', 'activo', 'Active', 'ACTIVE'] else 'inactivo'
                status_combo.set(status_value)
        
        # Contraseña
        password_label = "🔒 Nueva Contraseña:" if self.is_edit else "🔒 Contraseña:"
        required = "" if self.is_edit else " *"
        
        tk.Label(inner_frame, text=password_label + required, bg='white',
                font=('Segoe UI', 12, 'bold'), fg='#2c3e50').pack(anchor='w', pady=(0, 5))
        
        self.password_entry = tk.Entry(inner_frame, textvariable=self.password_var, font=('Segoe UI', 11), 
                show='*', relief='solid', bd=1)
        self.password_entry.pack(fill='x', pady=(0, 15))
        
        # Confirmar contraseña
        confirm_label = "🔒 Confirmar Nueva Contraseña:" if self.is_edit else "🔒 Confirmar Contraseña:"
        
        tk.Label(inner_frame, text=confirm_label + required, bg='white',
                font=('Segoe UI', 12, 'bold'), fg='#2c3e50').pack(anchor='w', pady=(0, 5))
        
        self.confirm_password_entry = tk.Entry(inner_frame, textvariable=self.confirm_password_var, font=('Segoe UI', 11), 
                show='*', relief='solid', bd=1)
        self.confirm_password_entry.pack(fill='x', pady=(0, 15))
        
        # Nota para edición
        if self.is_edit:
            tk.Label(inner_frame, text="💡 Deje las contraseñas vacías si no desea cambiarla",
                    font=('Segoe UI', 10), fg='#7f8c8d', bg='white').pack(anchor='w', pady=(10, 0))
        
        # Botones
        buttons_frame = tk.Frame(inner_frame, bg='white')
        buttons_frame.pack(fill='x', pady=(30, 0))
        
        cancel_btn = tk.Button(buttons_frame, text="❌ Cancelar", command=self.cancel,
                              bg='#95a5a6', fg='white', font=('Segoe UI', 11, 'bold'),
                              relief='flat', cursor='hand2', width=12, padx=20, pady=10)
        cancel_btn.pack(side='left')
        
        save_text = "💾 Guardar" if self.is_edit else "➕ Crear Usuario"
        save_btn = tk.Button(buttons_frame, text=save_text, command=self.save,
                            bg='#27ae60', fg='white', font=('Segoe UI', 11, 'bold'),
                            relief='flat', cursor='hand2', width=15, padx=20, pady=10)
        save_btn.pack(side='right')
        
        # Bind Enter key
        self.dialog.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
    

    
    def validate_form(self) -> tuple[bool, str]:
        """Validar formulario"""
        try:
            # Intentar obtener valores de StringVar primero
            username = self.username_var.get().strip()
            full_name = self.full_name_var.get().strip()
            email = self.email_var.get().strip()
            password = self.password_var.get()
            confirm_password = self.confirm_password_var.get()
            
            # Si las StringVar están vacías, leer directamente de los Entry widgets
            if not username and hasattr(self, 'username_entry'):
                username = self.username_entry.get().strip()
                print(f"DEBUG - Username desde Entry: '{username}'")
                
            if not full_name and hasattr(self, 'fullname_entry'):
                full_name = self.fullname_entry.get().strip()
                print(f"DEBUG - Full name desde Entry: '{full_name}'")
                
            if not email and hasattr(self, 'email_entry'):
                email = self.email_entry.get().strip()
                print(f"DEBUG - Email desde Entry: '{email}'")
                
            if not password and hasattr(self, 'password_entry'):
                password = self.password_entry.get()
                print(f"DEBUG - Password desde Entry: '{'*' * len(password)}'")
                
            if not confirm_password and hasattr(self, 'confirm_password_entry'):
                confirm_password = self.confirm_password_entry.get()
                print(f"DEBUG - Confirm password desde Entry: '{'*' * len(confirm_password)}'")
            
            # Debug temporal
            print(f"VALIDACIÓN FINAL - Username: '{username}' (len: {len(username)})")
            print(f"VALIDACIÓN FINAL - Full name: '{full_name}' (len: {len(full_name)})")
            print(f"VALIDACIÓN FINAL - Email: '{email}' (len: {len(email)})")
            print(f"VALIDACIÓN FINAL - Password: '{'*' * len(password)}' (len: {len(password)})")
            print(f"VALIDACIÓN FINAL - Confirm password: '{'*' * len(confirm_password)}' (len: {len(confirm_password)})")
            
            # Campos requeridos
            if not username:
                print("VALIDACIÓN FALLÓ - Username vacío")
                return False, "El nombre de usuario es requerido"
            
            if not full_name:
                print("VALIDACIÓN FALLÓ - Full name vacío")
                return False, "El nombre completo es requerido"
            
            if not email:
                print("VALIDACIÓN FALLÓ - Email vacío")
                return False, "El email es requerido"
            
            # Validar formato de email
            if '@' not in email or '.' not in email:
                return False, "El email no tiene un formato válido"
            
            # Validar contraseña
            if not self.is_edit:
                # Para nuevo usuario, contraseña es requerida
                if not password:
                    return False, "La contraseña es requerida"
                
                if len(password) < 4:
                    return False, "La contraseña debe tener al menos 4 caracteres"
                
                if password != confirm_password:
                    return False, "Las contraseñas no coinciden"
            else:
                # Para edición, solo validar si se proporcionó contraseña
                if password or confirm_password:
                    if len(password) < 4:
                        return False, "La contraseña debe tener al menos 4 caracteres"
                    
                    if password != confirm_password:
                        return False, "Las contraseñas no coinciden"
            
            return True, ""
                
        except Exception as e:
            return False, f"Error en validación: {str(e)}"
        
        # Validar email
        email = self.email_var.get().strip()
        if '@' not in email or '.' not in email:
            return False, "El email no tiene un formato válido"
        
        # Validar contraseña
        password = self.password_var.get()
        confirm = self.confirm_password_var.get()
        
        if not self.is_edit:
            # Para nuevo usuario, contraseña es requerida
            if not password:
                return False, "La contraseña es requerida"
            
            if len(password) < 4:
                return False, "La contraseña debe tener al menos 4 caracteres"
            
            if password != confirm:
                return False, "Las contraseñas no coinciden"
        else:
            # Para edición, solo validar si se proporcionó contraseña
            if password or confirm:
                if len(password) < 4:
                    return False, "La contraseña debe tener al menos 4 caracteres"
                
                if password != confirm:
                    return False, "Las contraseñas no coinciden"
        
        return True, ""
    
    def save(self):
        """Guardar usuario"""
        is_valid, error_message = self.validate_form()
        
        if not is_valid:
            messagebox.showerror("Error de Validación", error_message)
            return
        
        # Obtener valores de manera robusta (igual que en validate_form)
        username = self.username_var.get().strip()
        if not username and hasattr(self, 'username_entry'):
            username = self.username_entry.get().strip()
            
        full_name = self.full_name_var.get().strip()
        if not full_name and hasattr(self, 'fullname_entry'):
            full_name = self.fullname_entry.get().strip()
            
        email = self.email_var.get().strip()
        if not email and hasattr(self, 'email_entry'):
            email = self.email_entry.get().strip()
        
        password = self.password_var.get()
        if not password and hasattr(self, 'password_entry'):
            password = self.password_entry.get()
            
        user_type = self.user_type_var.get()
        status = self.status_var.get() if self.is_edit else 'active'
        
        # Crear resultado
        self.result = {
            'username': username,
            'full_name': full_name,
            'email': email,
            'user_type': user_type,
            'status': status
        }
        
        # Agregar contraseña si se proporcionó
        if password:
            self.result['password'] = password
        
        print(f"DEBUG - Resultado final: {self.result}")
        self.dialog.destroy()
    
    def cancel(self):
        """Cancelar diálogo"""
        self.result = None
        self.dialog.destroy()
    
    def center_dialog(self):
        """Centrar diálogo"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (650 // 2)
        self.dialog.geometry(f"500x650+{x}+{y}")
