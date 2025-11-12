"""
Generador de Tickets/Boletas para el Sistema POS
Genera tickets de venta en formato texto para impresión
Autor: Sistema POS
Fecha: 2025
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any

class TicketGenerator:
    """Generador de tickets de venta"""
    
    def __init__(self):
        self.config = self._load_config()
        self.ticket_width = 40  # Ancho del ticket en caracteres
    
    def _load_config(self) -> Dict[str, Any]:
        """Cargar configuración de la boleta desde system_config.json"""
        # Configuración por defecto para campos de ticket
        default_ticket_config = {
            'ticket_footer_message': '¡Gracias por su compra!',
            'ticket_footer_message_2': 'Vuelva pronto',
            'ticket_logo_text': '*** POS SYSTEM ***',
        }
        
        try:
            print(f"\n🎫 DEBUG: Cargando configuración de ticket desde system_config.json")
            
            # Usar PathManager para cargar configuración
            from utils.path_manager import load_config
            system_config = load_config('system_config.json')
            
            if system_config:
                print(f"   ✅ Configuración cargada desde system_config.json")
                print(f"   Empresa: {system_config.get('company_name', 'N/A')}")
                print(f"   RUC: {system_config.get('company_rut', 'N/A')}")
                
                # Mapear campos de system_config a formato de ticket
                config = {
                    'company_name': system_config.get('company_name', 'MI EMPRESA'),
                    'company_address': system_config.get('company_address', 'Dirección no configurada'),
                    'company_city': system_config.get('company_city', 'Lima, Perú'),
                    'company_phone': system_config.get('company_phone', ''),
                    'company_email': system_config.get('company_email', ''),
                    'company_ruc': system_config.get('company_rut', ''),
                    'show_logo': system_config.get('print_logo', False),
                    'logo_text': system_config.get('ticket_logo_text', default_ticket_config['ticket_logo_text']),
                    'footer_message': system_config.get('ticket_footer_message', default_ticket_config['ticket_footer_message']),
                    'footer_message_2': system_config.get('ticket_footer_message_2', default_ticket_config['ticket_footer_message_2']),
                    'show_barcode': system_config.get('print_barcode', False),
                    'print_copy': system_config.get('auto_print', True)
                }
                
                return config
            else:
                print(f"   ⚠️ Archivo system_config.json no existe")
                return {
                    'company_name': 'MI EMPRESA',
                    'company_address': 'Dirección no configurada',
                    'company_city': 'Lima, Perú',
                    'company_phone': '',
                    'company_email': '',
                    'company_ruc': '',
                    'show_logo': False,
                    'logo_text': default_ticket_config['ticket_logo_text'],
                    'footer_message': default_ticket_config['ticket_footer_message'],
                    'footer_message_2': default_ticket_config['ticket_footer_message_2'],
                    'show_barcode': False,
                    'print_copy': True
                }
        except Exception as e:
            print(f"❌ Error cargando configuración de ticket: {e}")
            import traceback
            traceback.print_exc()
            return {
                'company_name': 'MI EMPRESA',
                'company_address': 'Error al cargar config',
                'company_city': '',
                'company_phone': '',
                'company_email': '',
                'company_ruc': '',
                'show_logo': False,
                'logo_text': default_ticket_config['ticket_logo_text'],
                'footer_message': default_ticket_config['ticket_footer_message'],
                'footer_message_2': default_ticket_config['ticket_footer_message_2'],
                'show_barcode': False,
                'print_copy': True
            }
    
    def _center_text(self, text: str) -> str:
        """Centrar texto en el ancho del ticket"""
        return text.center(self.ticket_width)
    
    def _left_right(self, left: str, right: str) -> str:
        """Alinear texto a izquierda y derecha"""
        spaces = self.ticket_width - len(left) - len(right)
        return f"{left}{' ' * spaces}{right}"
    
    def _separator(self, char: str = '-') -> str:
        """Línea separadora"""
        return char * self.ticket_width
    
    def generate_ticket(self, sale_data: Dict[str, Any]) -> str:
        """
        Generar ticket de venta
        
        Args:
            sale_data: Diccionario con información de la venta
                - sale_number: Número de venta
                - date: Fecha y hora de la venta
                - items: Lista de productos vendidos
                - subtotal: Subtotal sin IGV
                - igv: Monto del IGV
                - discount: Descuento aplicado
                - total: Total de la venta
                - payment_method: Método de pago
                - paid_amount: Monto pagado
                - change_amount: Vuelto
                - customer: Datos del cliente (opcional)
                - cashier: Nombre del cajero
        """
        ticket = []
        
        # ========================================
        # HEADER - Información de la empresa
        # ========================================
        if self.config.get('show_logo'):
            ticket.append(self._center_text(self.config['logo_text']))
            ticket.append(self._separator('='))
        
        ticket.append(self._center_text(self.config['company_name']))
        ticket.append(self._center_text(self.config['company_address']))
        ticket.append(self._center_text(self.config['company_city']))
        ticket.append(self._center_text(f"Tel: {self.config['company_phone']}"))
        
        if self.config.get('company_email'):
            ticket.append(self._center_text(self.config['company_email']))
        
        ticket.append(self._center_text(f"RUC: {self.config['company_ruc']}"))
        ticket.append(self._separator('='))
        
        # ========================================
        # Información de la venta
        # ========================================
        ticket.append(self._center_text('BOLETA DE VENTA'))
        ticket.append(self._separator('-'))
        
        ticket.append(f"N° Venta: {sale_data['sale_number']}")
        ticket.append(f"Fecha: {sale_data['date'].strftime('%d/%m/%Y %H:%M:%S')}")
        ticket.append(f"Cajero: {sale_data['cashier']}")
        
        # Cliente (si existe)
        if sale_data.get('customer'):
            customer = sale_data['customer']
            ticket.append(self._separator('-'))
            ticket.append(f"Cliente: {customer.get('name', 'Cliente Genérico')}")
            if customer.get('document'):
                ticket.append(f"Doc: {customer['document']}")
        
        ticket.append(self._separator('='))
        
        # ========================================
        # Productos
        # ========================================
        ticket.append(self._left_right('PRODUCTO', 'TOTAL'))
        ticket.append(self._separator('-'))
        
        for item in sale_data['items']:
            # Línea 1: Nombre del producto
            product_name = item['name']
            if len(product_name) > self.ticket_width:
                product_name = product_name[:self.ticket_width-3] + '...'
            ticket.append(product_name)
            
            # Línea 2: Cantidad x Precio = Subtotal
            qty = item['quantity']
            price = item.get('price', item.get('unit_price', 0))  # Soportar ambos nombres
            subtotal = item.get('total', item.get('subtotal', 0))  # Soportar ambos nombres
            
            detail = f"  {qty} x S/ {price:.2f}"
            total_str = f"S/ {subtotal:.2f}"
            ticket.append(self._left_right(detail, total_str))
        
        ticket.append(self._separator('='))
        
        # ========================================
        # Totales
        # ========================================
        ticket.append(self._left_right('SUBTOTAL:', f"S/ {sale_data['subtotal']:.2f}"))
        
        if sale_data.get('discount', 0) > 0:
            ticket.append(self._left_right('DESCUENTO:', f"S/ -{sale_data['discount']:.2f}"))
        
        # ✅ Solo mostrar IGV si es mayor a 0 (cuando está activado)
        if sale_data.get('igv', 0) > 0:
            ticket.append(self._left_right('IGV (18%):', f"S/ {sale_data['igv']:.2f}"))
        
        ticket.append(self._separator('-'))
        ticket.append(self._left_right('TOTAL:', f"S/ {sale_data['total']:.2f}"))
        ticket.append(self._separator('='))
        
        # ========================================
        # Información de pago
        # ========================================
        payment_methods = {
            'cash': '💵 Efectivo',
            'card': '💳 Tarjeta',
            'transfer': '🏦 Transferencia'
        }
        payment_text = payment_methods.get(sale_data['payment_method'], sale_data['payment_method'])
        ticket.append(f"Método de Pago: {payment_text}")
        
        if sale_data['payment_method'] == 'cash':
            ticket.append(self._left_right('Pagado:', f"S/ {sale_data['paid_amount']:.2f}"))
            ticket.append(self._left_right('Vuelto:', f"S/ {sale_data['change_amount']:.2f}"))
        
        ticket.append(self._separator('='))
        
        # ========================================
        # Footer
        # ========================================
        ticket.append('')
        ticket.append(self._center_text(self.config['footer_message']))
        ticket.append(self._center_text(self.config['footer_message_2']))
        ticket.append('')
        
        if self.config.get('show_barcode'):
            ticket.append(self._center_text(f"*{sale_data['sale_number']}*"))
        
        ticket.append(self._separator('='))
        
        # Unir todas las líneas
        return '\n'.join(ticket)
    
    def save_ticket(self, ticket_content: str, sale_number: str) -> str:
        """
        Guardar ticket en archivo
        
        Returns:
            str: Ruta del archivo guardado
        """
        try:
            # Crear directorio de tickets si no existe
            tickets_dir = os.path.join('tickets')
            os.makedirs(tickets_dir, exist_ok=True)
            
            # Nombre del archivo con fecha y número de venta
            date_str = datetime.now().strftime('%Y%m%d')
            filename = f"ticket_{sale_number}_{date_str}.txt"
            filepath = os.path.join(tickets_dir, filename)
            
            # Guardar archivo
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(ticket_content)
            
            return filepath
        
        except Exception as e:
            print(f"Error guardando ticket: {e}")
            return None
    
    def print_ticket(self, ticket_content: str):
        """
        Enviar ticket a impresora (Windows)
        Usa la impresora predeterminada del sistema
        """
        try:
            import tempfile
            import subprocess
            
            # Crear archivo temporal
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(ticket_content)
                temp_path = f.name
            
            # Imprimir usando notepad en Windows
            subprocess.run(['notepad', '/p', temp_path], check=True)
            
            # Eliminar archivo temporal después de un delay
            import time
            time.sleep(2)
            os.unlink(temp_path)
            
            return True
        
        except Exception as e:
            print(f"Error imprimiendo ticket: {e}")
            return False
    
    def generate_ticket_html(self, sale_data: Dict[str, Any]) -> str:
        """
        Generar ticket en formato HTML con imagen de logo
        Ideal para impresión moderna y vista previa
        """
        # Cargar configuración actualizada para obtener logo_path usando PathManager
        from utils.path_manager import load_config
        logo_path = ""
        logo_base64 = ""
        
        try:
            system_config = load_config('system_config.json')
            if system_config:
                logo_path = system_config.get('logo_path', '')
                
                # Convertir imagen a base64 para incrustar en HTML
                if logo_path and os.path.exists(logo_path):
                    import base64
                    with open(logo_path, 'rb') as img_file:
                        logo_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                        # Detectar extensión
                        ext = os.path.splitext(logo_path)[1].lower()
                        mime_type = 'image/png' if ext == '.png' else 'image/jpeg'
                        logo_base64 = f"data:{mime_type};base64,{logo_base64}"
        except Exception as e:
            print(f"⚠️ No se pudo cargar logo: {e}")
        
        # Generar HTML
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Boleta de Venta #{sale_data['sale_number']}</title>
    <style>
        @page {{
            size: 80mm auto;
            margin: 5mm;
        }}
        body {{
            font-family: 'Courier New', monospace;
            font-size: 12px;
            width: 70mm;
            margin: 0 auto;
            padding: 10px;
        }}
        .center {{ text-align: center; }}
        .logo {{ 
            text-align: center; 
            margin: 10px 0;
        }}
        .logo img {{
            max-width: 120px;
            max-height: 80px;
            margin: 10px auto;
        }}
        .company-name {{ 
            font-weight: bold; 
            font-size: 14px; 
            margin: 5px 0;
        }}
        .separator {{ 
            border-top: 2px dashed #000; 
            margin: 10px 0; 
        }}
        .section-title {{
            font-weight: bold;
            text-align: center;
            margin: 10px 0;
            font-size: 13px;
        }}
        .info-row {{ 
            margin: 3px 0; 
        }}
        .items-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }}
        .items-table th {{
            border-bottom: 1px solid #000;
            padding: 5px 2px;
            text-align: left;
            font-size: 11px;
        }}
        .items-table td {{
            padding: 3px 2px;
            font-size: 11px;
        }}
        .text-right {{ text-align: right; }}
        .totals {{
            margin-top: 10px;
            border-top: 2px solid #000;
            padding-top: 10px;
        }}
        .total-row {{
            display: flex;
            justify-content: space-between;
            margin: 3px 0;
        }}
        .total-final {{
            font-weight: bold;
            font-size: 14px;
            border-top: 1px solid #000;
            padding-top: 5px;
            margin-top: 5px;
        }}
        .footer {{
            text-align: center;
            margin-top: 15px;
            font-size: 11px;
        }}
    </style>
</head>
<body>
    <!-- LOGO -->
    {"<div class='logo'><img src='" + logo_base64 + "' alt='Logo'></div>" if logo_base64 and self.config.get('show_logo') else ""}
    {"<div class='center logo-text'><strong>" + self.config['logo_text'] + "</strong></div>" if self.config.get('show_logo') and not logo_base64 else ""}
    
    <!-- INFORMACIÓN DE LA EMPRESA -->
    <div class='center company-name'>{self.config['company_name']}</div>
    <div class='center'>{self.config['company_address']}</div>
    <div class='center'>{self.config['company_city']}</div>
    <div class='center'>Tel: {self.config['company_phone']}</div>
    {"<div class='center'>" + self.config['company_email'] + "</div>" if self.config.get('company_email') else ""}
    <div class='center'>RUC: {self.config['company_ruc']}</div>
    
    <div class='separator'></div>
    
    <!-- TÍTULO -->
    <div class='section-title'>BOLETA DE VENTA</div>
    
    <!-- INFORMACIÓN DE VENTA -->
    <div class='info-row'>N° Venta: <strong>{sale_data['sale_number']}</strong></div>
    <div class='info-row'>Fecha: {sale_data['date'].strftime('%d/%m/%Y %H:%M:%S')}</div>
    <div class='info-row'>Cajero: {sale_data['cashier']}</div>
    
    <div class='separator'></div>
    
    <!-- PRODUCTOS -->
    <table class='items-table'>
        <thead>
            <tr>
                <th>PRODUCTO</th>
                <th class='text-right'>CANT</th>
                <th class='text-right'>P.U.</th>
                <th class='text-right'>TOTAL</th>
            </tr>
        </thead>
        <tbody>
"""
        
        # Agregar items
        for item in sale_data['items']:
            item_name = item['name'][:25]  # Limitar longitud
            html += f"""
            <tr>
                <td>{item_name}</td>
                <td class='text-right'>{item['quantity']}</td>
                <td class='text-right'>S/ {item['price']:.2f}</td>
                <td class='text-right'>S/ {item['total']:.2f}</td>
            </tr>
"""
        
        html += """
        </tbody>
    </table>
    
    <!-- TOTALES -->
    <div class='totals'>
"""
        
        # Agregar totales
        html += f"""
        <div class='total-row'>
            <span>Subtotal:</span>
            <span>S/ {sale_data['subtotal']:.2f}</span>
        </div>
"""
        
        if sale_data.get('discount', 0) > 0:
            html += f"""
        <div class='total-row'>
            <span>Descuento:</span>
            <span>-S/ {sale_data['discount']:.2f}</span>
        </div>
"""
        
        # ✅ Solo agregar IGV si es mayor a 0 (cuando está activado)
        if sale_data.get('igv', 0) > 0:
            html += f"""
        <div class='total-row'>
            <span>IGV (18%):</span>
            <span>S/ {sale_data['igv']:.2f}</span>
        </div>
"""
        
        html += f"""
        <div class='total-row total-final'>
            <span>TOTAL:</span>
            <span>S/ {sale_data['total']:.2f}</span>
        </div>
    </div>
    
    <div class='separator'></div>
    
    <!-- INFORMACIÓN DE PAGO -->
    <div class='info-row'>Método de Pago: <strong>{sale_data['payment_method']}</strong></div>
    <div class='info-row'>Pagó: S/ {sale_data.get('paid_amount', sale_data['total']):.2f}</div>
"""
        
        if sale_data.get('change_amount', 0) > 0:
            html += f"""
    <div class='info-row'>Vuelto: S/ {sale_data['change_amount']:.2f}</div>
"""
        
        html += f"""
    
    <div class='separator'></div>
    
    <!-- MENSAJES DE PIE -->
    <div class='footer'>
        <div>{self.config['footer_message']}</div>
        <div>{self.config['footer_message_2']}</div>
    </div>
</body>
</html>
"""
        
        return html
    
    def save_ticket_html(self, ticket_html: str, sale_number: str) -> str:
        """Guardar ticket HTML en archivo"""
        try:
            # Crear directorio si no existe
            tickets_dir = os.path.join('tickets')
            if not os.path.exists(tickets_dir):
                os.makedirs(tickets_dir)
            
            # Crear nombre de archivo
            date_str = datetime.now().strftime('%Y%m%d')
            filename = f"ticket_{sale_number}_{date_str}.html"
            filepath = os.path.join(tickets_dir, filename)
            
            # Guardar archivo
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(ticket_html)
            
            return filepath
        
        except Exception as e:
            print(f"Error guardando ticket HTML: {e}")
            return None
    
    def print_ticket_html(self, ticket_html: str, ticket_html_path: str = None, ticket_data: Dict[str, Any] = None):
        """
        Imprimir ticket usando impresora configurada
        
        Args:
            ticket_html: Contenido HTML del ticket (para PDF o navegador)
            ticket_html_path: Ruta al archivo HTML guardado (opcional)
            ticket_data: Datos de la venta (necesario para impresoras térmicas)
        """
        try:
            # ============================================
            # RECARGAR CONFIGURACIÓN ACTUALIZADA
            # Esto permite cambiar la impresora en system_config.json
            # y que se aplique inmediatamente sin reiniciar el sistema
            # ============================================
            from utils.path_manager import load_config
            printer_name = "Microsoft Print to PDF"  # Default
            is_thermal = False
            current_config = {}  # Configuración actualizada para esta impresión
            
            try:
                system_config = load_config('system_config.json')
                if system_config:
                    printer_name = system_config.get('printer', 'Microsoft Print to PDF')

                    print(f"\n🔄 Recargando configuración de impresora desde system_config.json...")
                    print(f"🖨️  Impresora configurada: {printer_name}")

                    # Crear configuración actualizada para el ticket
                    current_config = {
                        'company_name': system_config.get('company_name', 'MI EMPRESA'),
                        'company_address': system_config.get('company_address', 'Dirección no configurada'),
                        'company_city': system_config.get('company_city', 'Lima, Perú'),
                        'company_phone': system_config.get('company_phone', ''),
                        'company_email': system_config.get('company_email', ''),
                        'company_ruc': system_config.get('company_rut', ''),
                        'print_logo': system_config.get('print_logo', False),
                        'logo_text': system_config.get('ticket_logo_text', '*** POS SYSTEM ***'),
                        'ticket_footer_message': system_config.get('ticket_footer_message', '¡Gracias por su compra!'),
                        'ticket_footer_message_2': system_config.get('ticket_footer_message_2', 'Vuelva pronto'),
                        'print_barcode': system_config.get('print_barcode', False),
                        'auto_print': system_config.get('auto_print', True)
                    }

                    # Detectar si es impresora térmica
                    printer_mode = str(system_config.get('printer_mode', 'auto')).strip().lower()
                    force_thermal = bool(system_config.get('force_thermal_print', False))

                    thermal_keywords = ['TP-', 'TM-', 'THERMAL', 'TERMICA', 'POS', '80MM', 'TICKET']
                    extra_keywords = system_config.get('thermal_printer_keywords', [])

                    if isinstance(extra_keywords, str):
                        extra_keywords = [k.strip() for k in extra_keywords.split(',') if k.strip()]
                    if isinstance(extra_keywords, list):
                        thermal_keywords.extend([str(k).upper() for k in extra_keywords if isinstance(k, (str, bytes))])

                    thermal_keywords = [str(k).upper() for k in thermal_keywords]

                    normalized_name = printer_name.upper()

                    if force_thermal or printer_mode == 'thermal':
                        is_thermal = True
                        print("   ✓ Modo térmico forzado desde la configuración")
                    elif printer_mode == 'standard':
                        is_thermal = False
                        print("   → Modo estándar forzado desde la configuración")
                    else:
                        is_thermal = any(keyword in normalized_name for keyword in thermal_keywords)
                        if is_thermal:
                            print("   ✓ Detectada como impresora térmica (auto)")
                        else:
                            print("   → Impresora estándar/PDF (auto)")
            except Exception as e:
                print(f"   ⚠️ Error cargando configuración: {e}")
                current_config = self.config  # Usar configuración por defecto si falla
            
            # ============================================
            # IMPRESORAS TÉRMICAS (TP-300, TM-T20, etc.)
            # ============================================
            if is_thermal:
                print(f"🖨️  Usando módulo de impresión térmica...")
                
                if not ticket_data:
                    print(f"   ⚠️  Error: No se proporcionaron datos de venta para impresora térmica")
                    print(f"   🔄 Cambiando a impresión HTML...")
                    is_thermal = False  # Fallback a HTML
                else:
                    try:
                        from utils.thermal_printer import ThermalPrinter
                        
                        # Crear instancia de impresora térmica con nombre actualizado
                        thermal = ThermalPrinter(printer_name)
                        
                        # Imprimir usando ESC/POS con configuración actualizada
                        success = thermal.print_ticket(ticket_data, current_config)
                        
                        if success:
                            print(f"   ✅ Ticket enviado a impresora térmica exitosamente")
                            return True
                        else:
                            print(f"   ❌ Error en impresión térmica, cambiando a HTML...")
                            is_thermal = False  # Fallback a HTML
                    
                    except ImportError as ie:
                        print(f"   ⚠️ Módulo thermal_printer no disponible: {ie}")
                        print(f"   🔄 Cambiando a impresión HTML...")
                        is_thermal = False  # Fallback a HTML
                    
                    except Exception as e:
                        print(f"   ❌ Error en impresión térmica: {e}")
                        import traceback
                        traceback.print_exc()
                        print(f"   🔄 Cambiando a impresión HTML...")
                        is_thermal = False  # Fallback a HTML
            
            # ============================================
            # IMPRESORAS ESTÁNDAR / PDF
            # ============================================
            if not is_thermal:
                import tempfile
                
                # Crear archivo HTML temporal si no se proporciona
                if not ticket_html_path:
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                        f.write(ticket_html)
                        ticket_html_path = f.name
                
                # Si la impresora es "Microsoft Print to PDF", generar PDF directamente
                if "Print to PDF" in printer_name or "PDF" in printer_name:
                    return self._print_html_to_pdf(ticket_html_path, ticket_html)
                else:
                    # Para otras impresoras estándar, abrir en navegador
                    import webbrowser
                    webbrowser.open('file://' + os.path.abspath(ticket_html_path))
                    return True
        
        except Exception as e:
            print(f"❌ Error imprimiendo ticket: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _print_html_to_pdf(self, html_path: str, html_content: str):
        """Convertir HTML a PDF y guardarlo directamente SIN abrir navegador"""
        try:
            # Método 1: Usar WeasyPrint (recomendado - no requiere navegador)
            try:
                from weasyprint import HTML, CSS
                
                # Crear directorio para PDFs
                pdf_dir = os.path.join('tickets', 'pdf')
                if not os.path.exists(pdf_dir):
                    os.makedirs(pdf_dir)
                
                from datetime import datetime
                pdf_filename = f"ticket_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                pdf_path = os.path.join(pdf_dir, pdf_filename)
                
                print(f"📄 Generando PDF directamente (sin navegador)...")
                
                # Leer el HTML
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_string = f.read()
                
                # Convertir HTML a PDF directamente
                HTML(string=html_string, base_url=os.path.dirname(os.path.abspath(html_path))).write_pdf(pdf_path)
                
                print(f"✅ PDF generado exitosamente: {pdf_path}")
                
                # Abrir el PDF con el visor predeterminado
                import subprocess
                import platform
                
                if platform.system() == 'Windows':
                    os.startfile(pdf_path)
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.run(['open', pdf_path])
                else:  # Linux
                    subprocess.run(['xdg-open', pdf_path])
                
                return True
            
            except ImportError as ie:
                print(f"⚠️ WeasyPrint no disponible: {ie}")
                print("   Intentando método alternativo...")
                # Método 2: Abrir en navegador con diálogo de impresión
                return self._print_html_browser(html_path)
        
        except Exception as e:
            print(f"❌ Error en _print_html_to_pdf: {e}")
            import traceback
            traceback.print_exc()
            # Fallback: abrir en navegador
            return self._print_html_browser(html_path)
    
    def _print_html_browser(self, html_path: str):
        """Abrir HTML en navegador con script de auto-impresión"""
        try:
            import webbrowser
            
            # Leer el HTML original
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Agregar script de auto-impresión
            auto_print_script = """
    <script>
        window.onload = function() {
            // Esperar un momento para que el contenido se cargue completamente
            setTimeout(function() {
                window.print();
            }, 500);
        };
    </script>
"""
            
            # Insertar el script antes de </body>
            if '</body>' in html_content:
                html_content = html_content.replace('</body>', auto_print_script + '</body>')
            else:
                html_content += auto_print_script
            
            # Guardar HTML modificado
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html_content)
                temp_path = f.name
            
            print(f"🌐 Abriendo en navegador con diálogo de impresión automático...")
            webbrowser.open('file://' + os.path.abspath(temp_path))
            
            return True
        
        except Exception as e:
            print(f"❌ Error en _print_html_browser: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def preview_ticket(self, ticket_content: str):
        """Mostrar vista previa del ticket en consola"""
        print("\n" + "="*50)
        print("VISTA PREVIA DEL TICKET")
        print("="*50)
        print(ticket_content)
        print("="*50 + "\n")
