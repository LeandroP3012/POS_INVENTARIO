"""
Vista de Configuración de Boletas/Tickets
Permite configurar la información que aparecerá en las boletas
Autor: Sistema POS
Fecha: 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from utils.ticket_generator import TicketGenerator

class TicketConfigView:
    """Vista para configurar las boletas"""
    
    def __init__(self, parent, on_back=None):
        self.parent = parent
        self.on_back = on_back
        self.config_path = os.path.join('config', 'system_config.json')
        
        # Diccionario para almacenar widgets
        self.entries = {}
        
        # Cargar configuración ANTES de crear la UI
        self.config_data = self.load_config_data()
        
        # Frame principal
        self.main_frame = tk.Frame(parent, bg='#ecf0f1')
        self.main_frame.pack(fill='both', expand=True)
        
        self.setup_ui()
        
        # Forzar actualización de valores después de crear UI
        self.parent.after(100, self.force_update_fields)
    
    def setup_ui(self):
        """Configurar interfaz"""
        # Header
        self.create_header()
        
        # Contenedor con scroll
        container = tk.Frame(self.main_frame, bg='#ecf0f1')
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Canvas con scrollbar
        canvas = tk.Canvas(container, bg='#ecf0f1', highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        
        self.scrollable_frame = tk.Frame(canvas, bg='white')
        self.scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Formulario
        self.create_form()
    
    def create_header(self):
        """Crear header"""
        header = tk.Frame(self.main_frame, bg='#2c3e50', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Botón volver
        if self.on_back:
            back_btn = tk.Button(
                header,
                text='← Volver',
                command=self.on_back,
                bg='#34495e',
                fg='white',
                font=('Segoe UI', 10),
                cursor='hand2',
                relief='flat',
                padx=20,
                pady=10
            )
            back_btn.pack(side='left', padx=20, pady=20)
        
        # Título
        title = tk.Label(
            header,
            text='🎫 CONFIGURACIÓN DE BOLETAS',
            font=('Segoe UI', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title.pack(side='left', padx=20)
    
    def create_form(self):
        """Crear formulario de configuración"""
        form_frame = tk.Frame(self.scrollable_frame, bg='white', padx=30, pady=30)
        form_frame.pack(fill='both', expand=True)
        
        # Variables
        self.vars = {}
        
        # ========================================
        # SECCIÓN: Información de la Empresa
        # ========================================
        self.create_section_title(form_frame, '🏢 INFORMACIÓN DE LA EMPRESA')
        
        self.create_field(form_frame, 'company_name', 'Nombre de la Empresa:')
        self.create_field(form_frame, 'company_rut', 'RUC:')
        self.create_field(form_frame, 'company_address', 'Dirección:')
        self.create_field(form_frame, 'company_city', 'Ciudad:')
        self.create_field(form_frame, 'company_phone', 'Teléfono:')
        self.create_field(form_frame, 'company_email', 'Email:')
        
        # ========================================
        # SECCIÓN: Personalización
        # ========================================
        self.create_section_title(form_frame, '🎨 PERSONALIZACIÓN')
        
        self.create_field(form_frame, 'ticket_logo_text', 'Texto del Logo:')
        
        # Checkbox: Mostrar logo
        checkbox_frame = tk.Frame(form_frame, bg='white')
        checkbox_frame.pack(fill='x', pady=10)
        
        self.vars['print_logo'] = tk.BooleanVar(value=self.config_data.get('print_logo', False))
        tk.Checkbutton(
            checkbox_frame,
            text='Mostrar Logo en Boleta',
            variable=self.vars['print_logo'],
            bg='white',
            font=('Segoe UI', 10),
            activebackground='white'
        ).pack(anchor='w')
        
        self.vars['print_barcode'] = tk.BooleanVar(value=self.config_data.get('print_barcode', False))
        tk.Checkbutton(
            checkbox_frame,
            text='Mostrar Código de Barras',
            variable=self.vars['print_barcode'],
            bg='white',
            font=('Segoe UI', 10),
            activebackground='white'
        ).pack(anchor='w', pady=5)
        
        self.vars['auto_print'] = tk.BooleanVar(value=self.config_data.get('auto_print', True))
        tk.Checkbutton(
            checkbox_frame,
            text='Imprimir Automáticamente',
            variable=self.vars['auto_print'],
            bg='white',
            font=('Segoe UI', 10),
            activebackground='white'
        ).pack(anchor='w')
        
        # ========================================
        # SECCIÓN: Mensajes
        # ========================================
        self.create_section_title(form_frame, '💬 MENSAJES DE PIE DE PÁGINA')
        
        self.create_field(form_frame, 'ticket_footer_message', 'Mensaje 1:')
        self.create_field(form_frame, 'ticket_footer_message_2', 'Mensaje 2:')
        
        # ========================================
        # Botones de acción
        # ========================================
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.pack(fill='x', pady=30)
        
        tk.Button(
            button_frame,
            text='💾 Guardar Configuración',
            command=self.save_config,
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            cursor='hand2',
            relief='flat',
            padx=30,
            pady=15
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text='👁️ Vista Previa',
            command=self.show_preview,
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            cursor='hand2',
            relief='flat',
            padx=30,
            pady=15
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text='🔄 Restaurar por Defecto',
            command=self.restore_defaults,
            bg='#e67e22',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            cursor='hand2',
            relief='flat',
            padx=30,
            pady=15
        ).pack(side='left', padx=5)
    
    def create_section_title(self, parent, title):
        """Crear título de sección"""
        frame = tk.Frame(parent, bg='#ecf0f1')
        frame.pack(fill='x', pady=(20, 10))
        
        tk.Label(
            frame,
            text=title,
            font=('Segoe UI', 14, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50',
            anchor='w'
        ).pack(fill='x', padx=10, pady=10)
    
    def create_field(self, parent, key, label):
        """Crear campo de entrada"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='x', pady=5)
        
        tk.Label(
            frame,
            text=label,
            font=('Segoe UI', 10),
            bg='white',
            fg='#2c3e50',
            anchor='w',
            width=20
        ).pack(side='left', padx=5)
        
        # Obtener valor de la configuración cargada
        value = self.config_data.get(key, '')
        print(f"   🔧 create_field({key}) = '{value}'")
        
        self.vars[key] = tk.StringVar(value=value)
        entry = tk.Entry(
            frame,
            textvariable=self.vars[key],
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1
        )
        entry.pack(side='left', fill='x', expand=True, padx=5, ipady=5)
        
        # Guardar referencia al Entry
        self.entries[key] = entry
    
    def force_update_fields(self):
        """Forzar actualización visual de los campos"""
        print("\n🔄 DEBUG: Forzando actualización de campos...")
        for key, entry in self.entries.items():
            value = self.config_data.get(key, '')
            if value:
                entry.delete(0, tk.END)
                entry.insert(0, value)
                print(f"   ✏️ Actualizado {key} = '{value}'")
    
    def load_config_data(self):
        """Cargar datos de configuración desde system_config.json"""
        try:
            print(f"\n📂 DEBUG: Pre-cargando configuración de ticket")
            print(f"   Ruta: {self.config_path}")
            
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    print(f"   ✅ Configuración leída correctamente")
                    print(f"   📊 Claves encontradas: {list(config.keys())}")
                    print(f"   🏢 company_name = '{config.get('company_name', 'NO ENCONTRADO')}'")
                    print(f"   📧 company_email = '{config.get('company_email', 'NO ENCONTRADO')}'")
                    return config
            else:
                print(f"   ⚠️ Archivo no existe, usando valores por defecto")
                return {}
        except Exception as e:
            print(f"❌ Error cargando configuración: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def load_config(self):
        """Cargar configuración existente desde system_config.json"""
        try:
            print(f"\n📂 DEBUG: Cargando configuración de ticket")
            print(f"   Ruta: {self.config_path}")
            print(f"   ¿Existe? {os.path.exists(self.config_path)}")
            
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                    print(f"   Variables del formulario disponibles:")
                    for var_key in self.vars.keys():
                        print(f"      - {var_key}")
                    
                    print(f"\n   Cargando valores desde JSON:")
                    # Cargar valores en los campos
                    for key, value in config.items():
                        if key in self.vars:
                            print(f"      ✅ {key}: {value}")
                            if isinstance(self.vars[key], tk.BooleanVar):
                                self.vars[key].set(bool(value))
                            else:
                                self.vars[key].set(str(value))
                        else:
                            # Este campo no existe en el formulario
                            pass
                    
                    print(f"   ✅ Configuración cargada correctamente")
            else:
                print(f"   ⚠️ Archivo no existe")
        except Exception as e:
            print(f"❌ Error cargando configuración: {e}")
            import traceback
            traceback.print_exc()
    
    def save_config(self):
        """Guardar configuración en system_config.json"""
        try:
            print(f"\n💾 DEBUG: Guardando configuración de ticket en system_config.json")
            print(f"   Ruta: {self.config_path}")
            
            # Leer configuración existente
            existing_config = {}
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    existing_config = json.load(f)
            
            # Actualizar solo los campos de ticket
            for key, var in self.vars.items():
                value = var.get()
                existing_config[key] = value
                print(f"      {key}: {value}")
            
            # Crear directorio si no existe
            os.makedirs('config', exist_ok=True)
            
            # Guardar archivo JSON completo
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(existing_config, f, indent=2, ensure_ascii=False)
            
            print(f"   ✅ Configuración guardada en: {os.path.abspath(self.config_path)}")
            
            messagebox.showinfo(
                'Éxito',
                '✅ Configuración guardada correctamente.\n\n'
                'Los cambios se aplicarán en las próximas boletas.'
            )
        
        except Exception as e:
            print(f"❌ Error guardando configuración: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror('Error', f'No se pudo guardar la configuración:\n{str(e)}')
    
    def show_preview(self):
        """Mostrar vista previa de boleta con logo en HTML"""
        try:
            from datetime import datetime
            
            # Crear datos de venta de ejemplo
            sample_sale = {
                'sale_number': 'DEMO-001',
                'date': datetime.now(),
                'cashier': 'Usuario Demo',
                'customer': {
                    'name': 'Cliente Ejemplo',
                    'document': '12345678'
                },
                'items': [
                    {
                        'name': 'Producto Demo 1',
                        'quantity': 2,
                        'price': 15.50,
                        'total': 31.00
                    },
                    {
                        'name': 'Producto Demo 2',
                        'quantity': 1,
                        'price': 25.00,
                        'total': 25.00
                    }
                ],
                'subtotal': 56.00,
                'discount': 0.00,
                'igv': 10.08,
                'total': 66.08,
                'payment_method': 'Efectivo',
                'paid_amount': 70.00,
                'change_amount': 3.92
            }
            
            # Guardar configuración actual primero
            self.save_config()
            
            # Generar ticket HTML con configuración actual
            generator = TicketGenerator()
            ticket_html = generator.generate_ticket_html(sample_sale)
            
            # Guardar temporal y abrir en navegador
            import tempfile
            import webbrowser
            import os
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(ticket_html)
                temp_path = f.name
            
            # Abrir en navegador
            webbrowser.open('file://' + os.path.abspath(temp_path))
            
            messagebox.showinfo('Vista Previa', 'Vista previa abierta en tu navegador con el logo')
        
        except Exception as e:
            messagebox.showerror('Error', f'Error generando vista previa:\n{str(e)}')
            import traceback
            traceback.print_exc()
    
    def show_preview_window(self, ticket_content):
        """Mostrar ventana con vista previa"""
        preview_window = tk.Toplevel(self.parent)
        preview_window.title('Vista Previa de Boleta')
        preview_window.geometry('600x700')
        preview_window.configure(bg='white')
        
        # Header
        header = tk.Frame(preview_window, bg='#2c3e50')
        header.pack(fill='x')
        
        tk.Label(
            header,
            text='👁️ VISTA PREVIA DE BOLETA',
            font=('Segoe UI', 16, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=15)
        
        # Texto del ticket
        text_frame = tk.Frame(preview_window, bg='white')
        text_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        text_widget = tk.Text(
            text_frame,
            font=('Courier New', 10),
            bg='#f8f9fa',
            relief='solid',
            borderwidth=1,
            padx=10,
            pady=10
        )
        text_widget.pack(fill='both', expand=True)
        text_widget.insert('1.0', ticket_content)
        text_widget.config(state='disabled')
        
        # Botón cerrar
        tk.Button(
            preview_window,
            text='Cerrar',
            command=preview_window.destroy,
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            cursor='hand2',
            relief='flat',
            padx=30,
            pady=10
        ).pack(pady=10)
    
    def restore_defaults(self):
        """Restaurar valores por defecto"""
        if messagebox.askyesno(
            'Confirmar',
            '¿Restaurar configuración por defecto?\n\nSe perderán los cambios actuales.'
        ):
            defaults = {
                'company_name': 'MI EMPRESA',
                'company_address': 'Av. Principal 123',
                'company_city': 'Lima, Perú',
                'company_phone': '(01) 234-5678',
                'company_email': 'ventas@miempresa.com',
                'company_rut': '20123456789',
                'print_logo': False,
                'ticket_logo_text': '*** POS SYSTEM ***',
                'ticket_footer_message': '¡Gracias por su compra!',
                'ticket_footer_message_2': 'Vuelva pronto',
                'print_barcode': False,
                'auto_print': True
            }
            
            for key, value in defaults.items():
                if key in self.vars:
                    self.vars[key].set(value)
            
            messagebox.showinfo('Éxito', '✅ Configuración restaurada a valores por defecto.')
    
    def show(self):
        """Mostrar vista"""
        self.main_frame.pack(fill='both', expand=True)
    
    def hide(self):
        """Ocultar vista"""
        self.main_frame.pack_forget()
