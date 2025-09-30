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


class UserManagementView(BaseView):
    """Vista completa de gestión de usuarios"""
    
    def __init__(self, root: tk.Tk, user_data: Dict[str, Any] = None, embedded: bool = True):
        super().__init__(root)
        self.user_data = user_data or {}
        self.embedded = embedded
        self.users_data = []
        self.filtered_users = []
        self.selected_user = None
        
        # Inicializar controlador
        self.user_controller = UserController()
        
        # Configurar ventana
        self.setup_user_management_window()
        
        # Cargar datos iniciales
        self.load_users_data()
    
    def setup_user_management_window(self):
        """Configurar ventana de gestión de usuarios"""
        if not self.embedded:
            self.root.title("Sistema POS - Gestión de Usuarios")
            self.root.geometry("1200x800") 
            self.root.configure(bg='#f8f9fa')
            self.center_window(1200, 800)
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        else:
            self.root.configure(bg='#f8f9fa')
        
        self.create_user_management_interface()
    
    def create_user_management_interface(self):
        """Crear interfaz de gestión de usuarios"""
        # Header
        self.create_header()
        
        # Toolbar con búsqueda y botones
        self.create_toolbar()
        
        # Panel principal con tabla y detalles
        self.create_main_panel()
        
        # Footer con estadísticas
        self.create_footer()
    
    def create_header(self):
        """Crear header de gestión de usuarios"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        content_frame = tk.Frame(header_frame, bg='#2c3e50')
        content_frame.pack(expand=True, fill='both', padx=30, pady=15)
        
        # Frame izquierdo para botón de volver y título
        left_frame = tk.Frame(content_frame, bg='#2c3e50')
        left_frame.pack(side='left', fill='y')
        
        # Botón de volver (solo en modo embebido)
        if self.embedded:
            back_button = tk.Button(
                left_frame,
                text="← Volver al Dashboard",
                command=self.go_back_to_dashboard,
                bg='#34495e',
                fg='white',
                font=('Segoe UI', 10, 'bold'),
                relief='flat',
                cursor='hand2',
                padx=15,
                pady=5
            )
            back_button.pack(side='left', padx=(0, 20))
        
        # Título
        title_label = tk.Label(
            left_frame,
            text="👥 Gestión de Usuarios",
            font=('Segoe UI', 20, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(side='left')
        
        # Usuario actual (derecha)
        user_text = f"Usuario: {self.user_data.get('full_name', self.user_data.get('username', 'Admin'))}"
        user_label = tk.Label(
            content_frame,
            text=user_text,
            font=('Segoe UI', 12),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        user_label.pack(side='right')
    
    def create_toolbar(self):
        """Crear toolbar con búsqueda y botones de acción"""
        toolbar_frame = tk.Frame(self.root, bg='white', height=70)
        toolbar_frame.pack(fill='x', padx=20, pady=(20, 0))
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
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left', padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self.on_search_change)
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 11),
            width=25,
            relief='solid',
            bd=1
        )
        search_entry.pack(side='left', padx=(0, 10), ipady=5)
        
        # Filtro por rol
        tk.Label(
            search_frame,
            text="Rol:",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left', padx=(20, 5))
        
        self.role_filter_var = tk.StringVar(value='Todos')
        role_combo = ttk.Combobox(
            search_frame,
            textvariable=self.role_filter_var,
            values=['Todos', 'admin', 'supervisor', 'cajero'],
            state='readonly',
            width=12,
            font=('Segoe UI', 10)
        )
        role_combo.pack(side='left', padx=(0, 10))
        role_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # Frame derecho - Botones de acción
        buttons_frame = tk.Frame(inner_frame, bg='white')
        buttons_frame.pack(side='right', fill='y')
        
        # Botón nuevo usuario
        new_user_btn = tk.Button(
            buttons_frame,
            text="➕ Nuevo Usuario",
            command=self.create_new_user,
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8
        )
        new_user_btn.pack(side='left', padx=(0, 10))
        
        # Botón editar
        self.edit_user_btn = tk.Button(
            buttons_frame,
            text="✏️ Editar",
            command=self.edit_selected_user,
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8,
            state='disabled'
        )
        self.edit_user_btn.pack(side='left', padx=(0, 10))
        
        # Botón eliminar
        self.delete_user_btn = tk.Button(
            buttons_frame,
            text="🗑️ Eliminar",
            command=self.delete_selected_user,
            bg='#e74c3c',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8,
            state='disabled'
        )
        self.delete_user_btn.pack(side='left')
    
    def create_main_panel(self):
        """Crear panel principal con tabla de usuarios"""
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Frame para la tabla
        table_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=1)
        table_frame.pack(fill='both', expand=True)
        
        # Título de la tabla
        table_header = tk.Frame(table_frame, bg='#34495e', height=40)
        table_header.pack(fill='x')
        table_header.pack_propagate(False)
        
        tk.Label(
            table_header,
            text="📋 Lista de Usuarios del Sistema",
            font=('Segoe UI', 14, 'bold'),
            fg='white',
            bg='#34495e'
        ).pack(side='left', padx=20, pady=10)
        
        # Contador de usuarios
        self.user_count_label = tk.Label(
            table_header,
            text="0 usuarios",
            font=('Segoe UI', 11),
            fg='#bdc3c7',
            bg='#34495e'
        )
        self.user_count_label.pack(side='right', padx=20, pady=10)
        
        # Crear Treeview para la tabla
        self.create_users_table(table_frame)
    
    def create_users_table(self, parent):
        """Crear tabla de usuarios con Treeview"""
        # Frame para tabla y scrollbars
        tree_frame = tk.Frame(parent, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
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
            height=15
        )
        
        # Configurar columnas
        self.users_tree.column('#0', width=0, stretch=False)  # Ocultar primera columna
        self.users_tree.column('id', width=50, anchor='center')
        self.users_tree.column('username', width=120, anchor='w')
        self.users_tree.column('full_name', width=200, anchor='w')
        self.users_tree.column('user_type', width=120, anchor='center')
        self.users_tree.column('email', width=200, anchor='w')
        self.users_tree.column('status', width=80, anchor='center')
        self.users_tree.column('last_login', width=150, anchor='center')
        self.users_tree.column('created_at', width=150, anchor='center')
        
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
        style.configure('Treeview', rowheight=25)
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))
    
    def create_footer(self):
        """Crear footer con estadísticas"""
        footer_frame = tk.Frame(self.root, bg='#ecf0f1', height=50)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        inner_frame = tk.Frame(footer_frame, bg='#ecf0f1')
        inner_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Estadísticas
        self.stats_label = tk.Label(
            inner_frame,
            text="👥 Total: 0 | ✅ Activos: 0 | ❌ Inactivos: 0 | 👑 Admins: 0",
            font=('Segoe UI', 10, 'bold'),
            fg='#2c3e50',
            bg='#ecf0f1'
        )
        self.stats_label.pack(side='left')
        
        # Información de la sesión actual
        session_info = f"Sesión actual: {self.user_data.get('username', 'admin')} ({self.user_data.get('user_type', 'admin')})"
        tk.Label(
            inner_frame,
            text=session_info,
            font=('Segoe UI', 10),
            fg='#7f8c8d',
            bg='#ecf0f1'
        ).pack(side='right')
    
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
            
            # Filtro de rol
            role_match = role_filter == 'Todos' or user.get('user_type', '') == role_filter
            
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
            
            # Habilitar botones
            self.edit_user_btn.configure(state='normal')
            # Solo permitir eliminar si no es el usuario actual
            if self.selected_user and self.selected_user.get('username') != self.user_data.get('username', ''):
                self.delete_user_btn.configure(state='normal')
            else:
                self.delete_user_btn.configure(state='disabled')
        else:
            self.selected_user = None
            self.edit_user_btn.configure(state='disabled')
            self.delete_user_btn.configure(state='disabled')
    
    def on_user_double_click(self, event):
        """Manejar doble clic en usuario"""
        if self.selected_user:
            self.edit_selected_user()
    
    def create_new_user(self):
        """Crear nuevo usuario"""
        dialog = UserDialog(self.root, "Crear Nuevo Usuario")
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
        
        dialog = UserDialog(self.root, "Editar Usuario", self.selected_user)
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
                    self.edit_user_btn.configure(state='disabled')
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
    
    def __init__(self, parent, title: str, user_data: Dict = None):
        self.parent = parent
        self.user_data = user_data or {}
        self.result = None
        self.is_edit = bool(user_data)
        
        # Crear ventana de diálogo
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x650")
        self.dialog.configure(bg='white')
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar diálogo
        self.center_dialog()
        
        # Crear interfaz
        self.create_dialog_interface()
        
        # Enfocar primer campo
        self.username_entry.focus_set()
    
    def create_dialog_interface(self):
        """Crear interfaz del diálogo"""
        # Header
        header_frame = tk.Frame(self.dialog, bg='#3498db', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        icon = "✏️" if self.is_edit else "➕"
        title_text = "Editar Usuario" if self.is_edit else "Crear Nuevo Usuario"
        
        tk.Label(
            header_frame,
            text=f"{icon} {title_text}",
            font=('Segoe UI', 16, 'bold'),
            fg='white',
            bg='#3498db'
        ).pack(expand=True)
        
        # Contenido
        content_frame = tk.Frame(self.dialog, bg='white')
        content_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Variables
        self.username_var = tk.StringVar(value=self.user_data.get('username', ''))
        self.full_name_var = tk.StringVar(value=self.user_data.get('full_name', ''))
        self.email_var = tk.StringVar(value=self.user_data.get('email', ''))
        self.user_type_var = tk.StringVar(value=self.user_data.get('user_type', 'cajero'))
        self.status_var = tk.StringVar(value='active' if self.user_data.get('status', 'active') == 'active' else 'inactive')
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()
        
        # Campos del formulario
        y_pos = 0
        
        # Username
        self.create_field(content_frame, "👤 Nombre de Usuario:", self.username_var, y_pos)
        self.username_entry = self.last_entry
        y_pos += 70
        
        # Full name
        self.create_field(content_frame, "📝 Nombre Completo:", self.full_name_var, y_pos)
        y_pos += 70
        
        # Email
        self.create_field(content_frame, "📧 Email:", self.email_var, y_pos)
        y_pos += 70
        
        # User Type (Role)
        tk.Label(
            content_frame,
            text="🎭 Rol:",
            font=('Segoe UI', 12, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).place(x=0, y=y_pos)
        
        user_type_combo = ttk.Combobox(
            content_frame,
            textvariable=self.user_type_var,
            values=['admin', 'supervisor', 'cajero'],
            state='readonly',
            font=('Segoe UI', 11),
            width=35
        )
        user_type_combo.place(x=0, y=y_pos + 25)
        y_pos += 70
        
        # Status (solo en edición)
        if self.is_edit:
            tk.Label(
                content_frame,
                text="📊 Estado:",
                font=('Segoe UI', 12, 'bold'),
                fg='#2c3e50',
                bg='white'
            ).place(x=0, y=y_pos)
            
            status_combo = ttk.Combobox(
                content_frame,
                textvariable=self.status_var,
                values=['active', 'inactive'],
                state='readonly',
                font=('Segoe UI', 11),
                width=35
            )
            status_combo.place(x=0, y=y_pos + 25)
            y_pos += 70
        
        # Contraseña
        password_label = "🔒 Nueva Contraseña:" if self.is_edit else "🔒 Contraseña:"
        required = "" if self.is_edit else " *"
        
        tk.Label(
            content_frame,
            text=password_label + required,
            font=('Segoe UI', 12, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).place(x=0, y=y_pos)
        
        password_entry = tk.Entry(
            content_frame,
            textvariable=self.password_var,
            font=('Segoe UI', 11),
            show='*',
            width=38,
            relief='solid',
            bd=1
        )
        password_entry.place(x=0, y=y_pos + 25)
        y_pos += 70
        
        # Confirmar contraseña
        confirm_label = "🔒 Confirmar Nueva Contraseña:" if self.is_edit else "🔒 Confirmar Contraseña:"
        
        tk.Label(
            content_frame,
            text=confirm_label + required,
            font=('Segoe UI', 12, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).place(x=0, y=y_pos)
        
        confirm_entry = tk.Entry(
            content_frame,
            textvariable=self.confirm_password_var,
            font=('Segoe UI', 11),
            show='*',
            width=38,
            relief='solid',
            bd=1
        )
        confirm_entry.place(x=0, y=y_pos + 25)
        y_pos += 80
        
        # Nota para edición
        if self.is_edit:
            tk.Label(
                content_frame,
                text="💡 Deje las contraseñas vacías si no desea cambiarla",
                font=('Segoe UI', 10),
                fg='#7f8c8d',
                bg='white'
            ).place(x=0, y=y_pos)
            y_pos += 30
        
        # Botones
        buttons_frame = tk.Frame(content_frame, bg='white')
        buttons_frame.place(x=0, y=y_pos, width=440, height=50)
        
        cancel_btn = tk.Button(
            buttons_frame,
            text="❌ Cancelar",
            command=self.cancel,
            bg='#95a5a6',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            cursor='hand2',
            width=12
        )
        cancel_btn.pack(side='left')
        
        save_text = "💾 Guardar" if self.is_edit else "➕ Crear Usuario"
        save_btn = tk.Button(
            buttons_frame,
            text=save_text,
            command=self.save,
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            cursor='hand2',
            width=15
        )
        save_btn.pack(side='right')
        
        # Bind Enter key
        self.dialog.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
    
    def create_field(self, parent, label_text, variable, y_pos):
        """Crear campo de entrada"""
        tk.Label(
            parent,
            text=label_text,
            font=('Segoe UI', 12, 'bold'),
            fg='#2c3e50',
            bg='white'
        ).place(x=0, y=y_pos)
        
        entry = tk.Entry(
            parent,
            textvariable=variable,
            font=('Segoe UI', 11),
            width=38,
            relief='solid',
            bd=1
        )
        entry.place(x=0, y=y_pos + 25)
        self.last_entry = entry
    
    def validate_form(self) -> tuple[bool, str]:
        """Validar formulario"""
        # Campos requeridos
        if not self.username_var.get().strip():
            return False, "El nombre de usuario es requerido"
        
        if not self.full_name_var.get().strip():
            return False, "El nombre completo es requerido"
        
        if not self.email_var.get().strip():
            return False, "El email es requerido"
        
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
        
        # Crear resultado
        self.result = {
            'username': self.username_var.get().strip(),
            'full_name': self.full_name_var.get().strip(),
            'email': self.email_var.get().strip(),
            'user_type': self.user_type_var.get(),
            'status': self.status_var.get() if self.is_edit else 'active'
        }
        
        # Agregar contraseña si se proporcionó
        if self.password_var.get():
            self.result['password'] = self.password_var.get()
        
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
