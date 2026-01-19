"""
Módulo de Impresión Térmica para Sistema POS
Soporta impresoras térmicas de 80mm con comandos ESC/POS
Compatible con: TP-300 y otras impresoras térmicas estándar
Autor: Sistema POS
Fecha: 2025
"""

import os
import json
import logging
import win32print
import win32ui
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ThermalPrinter:
    """
    Clase para manejar impresión en impresoras térmicas
    Soporta comandos ESC/POS estándar para impresoras de 80mm
    """
    
    # Comandos ESC/POS
    ESC = chr(27)
    GS = chr(29)
    
    # Comandos de texto
    CMD_INIT = ESC + '@'  # Inicializar impresora
    CMD_ALIGN_LEFT = ESC + 'a' + chr(0)
    CMD_ALIGN_CENTER = ESC + 'a' + chr(1)
    CMD_ALIGN_RIGHT = ESC + 'a' + chr(2)
    
    # Comandos de fuente
    CMD_BOLD_ON = ESC + 'E' + chr(1)
    CMD_BOLD_OFF = ESC + 'E' + chr(0)
    CMD_DOUBLE_ON = GS + '!' + chr(0x11)  # Texto doble altura y ancho
    CMD_DOUBLE_OFF = GS + '!' + chr(0x00)
    
    # Comandos de corte
    CMD_CUT = GS + 'V' + chr(66) + chr(0)  # Corte parcial
    CMD_FULL_CUT = GS + 'V' + chr(65) + chr(0)  # Corte completo
    
    # Comandos de alimentación
    CMD_FEED = ESC + 'd' + chr(1)  # Avanzar 1 línea
    
    # Comandos de código de barras
    CMD_BARCODE_HEIGHT = GS + 'h' + chr(80)  # Altura del código de barras (80 dots)
    CMD_BARCODE_WIDTH = GS + 'w' + chr(3)    # Ancho de barras (3 = medio)
    CMD_BARCODE_TXT_BELOW = GS + 'H' + chr(2)  # Texto debajo del código de barras
    CMD_BARCODE_FONT = GS + 'f' + chr(0)     # Fuente del texto (0 = fuente A)
    CMD_BARCODE_PRINT = GS + 'k'             # Comando para imprimir código de barras
    
    def __init__(self, printer_name: str = None):
        """
        Inicializar impresora térmica
        
        Args:
            printer_name: Nombre de la impresora. Si es None, usa la predeterminada.
        """
        self.printer_name = printer_name or self._get_default_printer()
        self.char_width = 48  # Ancho en caracteres para impresora de 80mm
        self.logger = logging.getLogger(self.__class__.__name__)

        self.logger.info("ThermalPrinter inicializado")
        self.logger.info("Impresora configurada: %s", self.printer_name)
        self.logger.debug("Ancho de caracteres: %s", self.char_width)
    
    def _get_default_printer(self) -> str:
        """Obtener impresora predeterminada del sistema"""
        try:
            return win32print.GetDefaultPrinter()
        except:
            return "Microsoft Print to PDF"
    
    def _center_text(self, text: str) -> str:
        """Centrar texto en el ancho del ticket"""
        return text.center(self.char_width)
    
    def _left_right(self, left: str, right: str) -> str:
        """Alinear texto a izquierda y derecha"""
        spaces = self.char_width - len(left) - len(right)
        return f"{left}{' ' * max(0, spaces)}{right}"
    
    def _separator(self, char: str = '-') -> str:
        """Línea separadora"""
        return char * self.char_width
    
    def _build_ticket_content(self, ticket_data: Dict[str, Any], config: Dict[str, Any]) -> bytes:
        """
        Construir contenido del ticket con comandos ESC/POS
        
        Args:
            ticket_data: Datos de la venta
            config: Configuración del sistema
        
        Returns:
            bytes: Contenido del ticket en formato ESC/POS
        """
        content = b''
        
        # Inicializar impresora
        content += self.CMD_INIT.encode('cp850', errors='ignore')
        
        # ========================================
        # HEADER - Logo y empresa
        # ========================================
        if config.get('print_logo', False) and config.get('logo_text'):
            content += self.CMD_ALIGN_CENTER.encode('cp850', errors='ignore')
            content += self.CMD_BOLD_ON.encode('cp850', errors='ignore')
            content += (config['logo_text'] + '\n').encode('cp850', errors='ignore')
            content += self.CMD_BOLD_OFF.encode('cp850', errors='ignore')
            content += (self._separator('=') + '\n').encode('cp850', errors='ignore')
        
        # Información de la empresa
        content += self.CMD_ALIGN_CENTER.encode('cp850', errors='ignore')
        content += self.CMD_BOLD_ON.encode('cp850', errors='ignore')
        content += (config.get('company_name', 'MI EMPRESA') + '\n').encode('cp850', errors='ignore')
        content += self.CMD_BOLD_OFF.encode('cp850', errors='ignore')
        
        content += (config.get('company_address', '') + '\n').encode('cp850', errors='ignore')
        content += (config.get('company_city', '') + '\n').encode('cp850', errors='ignore')
        content += (f"Tel: {config.get('company_phone', '')}\n").encode('cp850', errors='ignore')
        
        if config.get('company_email'):
            content += (config['company_email'] + '\n').encode('cp850', errors='ignore')
        
        content += (f"RUC: {config.get('company_ruc', '')}\n").encode('cp850', errors='ignore')
        content += (self._separator('=') + '\n').encode('cp850', errors='ignore')
        
        # ========================================
        # Título
        # ========================================
        content += self.CMD_ALIGN_CENTER.encode('cp850', errors='ignore')
        content += self.CMD_DOUBLE_ON.encode('cp850', errors='ignore')
        content += b'BOLETA DE VENTA\n'
        content += self.CMD_DOUBLE_OFF.encode('cp850', errors='ignore')
        content += (self._separator('-') + '\n').encode('cp850', errors='ignore')
        
        # ========================================
        # Información de la venta
        # ========================================
        content += self.CMD_ALIGN_LEFT.encode('cp850', errors='ignore')
        content += f"No Venta: {ticket_data['sale_number']}\n".encode('cp850', errors='ignore')
        content += f"Fecha: {ticket_data['date'].strftime('%d/%m/%Y %H:%M:%S')}\n".encode('cp850', errors='ignore')
        content += f"Cajero: {ticket_data['cashier']}\n".encode('cp850', errors='ignore')
        
        # Cliente (si existe)
        if ticket_data.get('customer'):
            customer = ticket_data['customer']
            content += (self._separator('-') + '\n').encode('cp850', errors='ignore')
            content += f"Cliente: {customer.get('name', 'Cliente Generico')}\n".encode('cp850', errors='ignore')
            if customer.get('document'):
                content += f"Doc: {customer['document']}\n".encode('cp850', errors='ignore')
        
        content += (self._separator('=') + '\n').encode('cp850', errors='ignore')
        
        # ========================================
        # Productos
        # ========================================
        content += self.CMD_BOLD_ON.encode('cp850', errors='ignore')
        content += (self._left_right('PRODUCTO', 'TOTAL') + '\n').encode('cp850', errors='ignore')
        content += self.CMD_BOLD_OFF.encode('cp850', errors='ignore')
        content += (self._separator('-') + '\n').encode('cp850', errors='ignore')
        
        for item in ticket_data['items']:
            # Nombre del producto
            product_name = item['name']
            if len(product_name) > self.char_width:
                product_name = product_name[:self.char_width-3] + '...'
            content += (product_name + '\n').encode('cp850', errors='ignore')
            
            # Cantidad x Precio = Subtotal
            qty = item['quantity']
            price = item.get('price', item.get('unit_price', 0))
            subtotal = item.get('total', item.get('subtotal', 0))
            
            detail = f"  {qty} x S/ {price:.2f}"
            total_str = f"S/ {subtotal:.2f}"
            content += (self._left_right(detail, total_str) + '\n').encode('cp850', errors='ignore')
        
        content += (self._separator('=') + '\n').encode('cp850', errors='ignore')
        
        # ========================================
        # Totales
        # ========================================
        content += (self._left_right('SUBTOTAL:', f"S/ {ticket_data['subtotal']:.2f}") + '\n').encode('cp850', errors='ignore')
        
        if ticket_data.get('discount', 0) > 0:
            content += (self._left_right('DESCUENTO:', f"S/ -{ticket_data['discount']:.2f}") + '\n').encode('cp850', errors='ignore')
        
        content += (self._left_right('IGV (18%):', f"S/ {ticket_data['igv']:.2f}") + '\n').encode('cp850', errors='ignore')
        content += (self._separator('-') + '\n').encode('cp850', errors='ignore')
        
        content += self.CMD_BOLD_ON.encode('cp850', errors='ignore')
        content += (self._left_right('TOTAL:', f"S/ {ticket_data['total']:.2f}") + '\n').encode('cp850', errors='ignore')
        content += self.CMD_BOLD_OFF.encode('cp850', errors='ignore')
        content += (self._separator('=') + '\n').encode('cp850', errors='ignore')
        
        # ========================================
        # Información de pago
        # ========================================
        payment_methods = {
            'cash': 'Efectivo',
            'card': 'Tarjeta',
            'transfer': 'Transferencia'
        }
        payment_text = payment_methods.get(ticket_data['payment_method'], ticket_data['payment_method'])
        content += f"Metodo de Pago: {payment_text}\n".encode('cp850', errors='ignore')
        
        if ticket_data['payment_method'] == 'cash':
            content += (self._left_right('Pagado:', f"S/ {ticket_data['paid_amount']:.2f}") + '\n').encode('cp850', errors='ignore')
            content += (self._left_right('Vuelto:', f"S/ {ticket_data['change_amount']:.2f}") + '\n').encode('cp850', errors='ignore')
        
        content += (self._separator('=') + '\n').encode('cp850', errors='ignore')
        
        # ========================================
        # Footer
        # ========================================
        content += self.CMD_ALIGN_CENTER.encode('cp850', errors='ignore')
        content += '\n'.encode('cp850', errors='ignore')
        content += (config.get('ticket_footer_message', 'Gracias por su compra!') + '\n').encode('cp850', errors='ignore')
        content += (config.get('ticket_footer_message_2', 'Vuelva pronto') + '\n').encode('cp850', errors='ignore')
        content += '\n'.encode('cp850', errors='ignore')
        
        if config.get('print_barcode', False):
            content += (f"*{ticket_data['sale_number']}*\n").encode('cp850', errors='ignore')
        
        content += (self._separator('=') + '\n').encode('cp850', errors='ignore')
        
        # ========================================
        # Finalizar: Alimentar papel y cortar
        # ========================================
        content += self.CMD_FEED.encode('cp850', errors='ignore')
        content += self.CMD_FEED.encode('cp850', errors='ignore')
        content += self.CMD_FEED.encode('cp850', errors='ignore')
        content += self.CMD_CUT.encode('cp850', errors='ignore')
        
        return content
    
    def print_ticket(self, ticket_data: Dict[str, Any], config: Dict[str, Any]) -> bool:
        """
        Imprimir ticket en impresora térmica
        
        Args:
            ticket_data: Datos de la venta
            config: Configuración del sistema
        
        Returns:
            bool: True si la impresión fue exitosa
        """
        try:
            self.logger.info("Iniciando impresión térmica")
            self.logger.info("Impresora configurada: %s", self.printer_name)
            self.logger.debug("Venta asociada: %s", ticket_data.get('sale_number'))
            
            # Verificar si la impresora existe y ajustar el nombre si Windows agrega sufijos
            resolved_printer = self._resolve_printer_name(self.printer_name)
            if not resolved_printer:
                self.logger.warning("Impresora '%s' no encontrada", self.printer_name)
                available = [p[2] for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)]
                self.logger.info("Impresoras disponibles: %s", available)

                default_printer = self._get_default_printer()
                self.logger.warning("Intentando con impresora predeterminada: %s", default_printer)
                resolved_printer = self._resolve_printer_name(default_printer) or default_printer
            elif resolved_printer != self.printer_name:
                self.logger.info("Ajustando nombre de impresora a coincidencia real: %s", resolved_printer)
            
            # Actualizar nombre final a utilizar
            self.printer_name = resolved_printer
            
            # Construir contenido del ticket
            ticket_content = self._build_ticket_content(ticket_data, config)
            
            # Enviar a la impresora
            hPrinter = win32print.OpenPrinter(self.printer_name)
            try:
                hJob = win32print.StartDocPrinter(hPrinter, 1, ("Ticket POS", None, "RAW"))
                try:
                    win32print.StartPagePrinter(hPrinter)
                    win32print.WritePrinter(hPrinter, ticket_content)
                    win32print.EndPagePrinter(hPrinter)
                finally:
                    win32print.EndDocPrinter(hPrinter)
            finally:
                win32print.ClosePrinter(hPrinter)
            
            self.logger.info("Ticket enviado a impresora exitosamente")
            return True

        except Exception:
            self.logger.exception("Error imprimiendo ticket")
            return False
    
    def _resolve_printer_name(self, printer_name: str) -> Optional[str]:
        """Encontrar la coincidencia real de impresora en el sistema."""
        try:
            desired = (printer_name or '').strip()
            if not desired:
                return None

            printers = win32print.EnumPrinters(
                win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
            )
            if not printers:
                return None

            # Coincidencia exacta (ignorando mayúsculas/minúsculas y espacios)
            desired_lower = desired.lower()
            for printer in printers:
                name = printer[2].strip()
                if name.lower() == desired_lower:
                    return name

            # Coincidencia parcial (útil cuando Windows agrega sufijos como "(Copiar 1)")
            for printer in printers:
                name = printer[2].strip()
                if desired_lower in name.lower():
                    return name

            return None
        except Exception as exc:
            self.logger.warning("Error resolviendo impresora '%s': %s", printer_name, exc)
            return None

    def _printer_exists(self, printer_name: str) -> bool:
        """Verificar si una impresora existe en el sistema"""
        return self._resolve_printer_name(printer_name) is not None
    
    def get_available_printers(self) -> List[str]:
        """Obtener lista de impresoras disponibles"""
        try:
            printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
            return sorted({p[2] for p in printers})
        except Exception as e:
            self.logger.error("Error obteniendo impresoras", exc_info=True)
            return []
    
    def print_barcode_image(self, barcode_image, product_name: str, sku: str, barcode: str) -> bool:
        """
        Imprimir imagen de código de barras en impresora térmica
        
        Args:
            barcode_image: Objeto PIL.Image con el código de barras
            product_name: Nombre del producto
            sku: SKU del producto
            barcode: Código de barras EAN-13
            
        Returns:
            bool: True si la impresión fue exitosa
        """
        try:
            from PIL import Image
            import io
            
            self.logger.info("Imprimiendo código de barras en impresora térmica")
            self.logger.debug("Producto: %s | SKU: %s | Código: %s", product_name, sku, barcode)
            
            # Verificar que la impresora exista
            resolved_printer = self._resolve_printer_name(self.printer_name)
            if not resolved_printer:
                self.logger.warning("Impresora '%s' no encontrada", self.printer_name)
                default_printer = self._get_default_printer()
                self.logger.warning("Intentando con impresora predeterminada: %s", default_printer)
                resolved_printer = self._resolve_printer_name(default_printer) or default_printer
            elif resolved_printer != self.printer_name:
                self.logger.info("Ajustando nombre de impresora a coincidencia real: %s", resolved_printer)

            self.printer_name = resolved_printer
            
            # Construir contenido del código de barras para impresora térmica
            content = bytearray()
            
            # Inicializar impresora
            content.extend(self.CMD_INIT.encode('cp437', errors='ignore'))
            
            # Centrar texto
            content.extend(self.CMD_ALIGN_CENTER.encode('cp437', errors='ignore'))
            
            # Imprimir nombre del producto
            content.extend(self.CMD_BOLD_ON.encode('cp437', errors='ignore'))
            product_line = product_name[:32] + '\n'  # Máximo 32 caracteres
            content.extend(product_line.encode('cp437', errors='ignore'))
            content.extend(self.CMD_BOLD_OFF.encode('cp437', errors='ignore'))
            
            # Espacio
            content.extend(b'\n')
            
            # Imprimir SKU
            sku_line = f"SKU: {sku}\n"
            content.extend(sku_line.encode('cp437', errors='ignore'))
            
            # Espacio
            content.extend(b'\n')
            
            # ============================================
            # IMPRIMIR CÓDIGO DE BARRAS GRÁFICO EAN-13
            # ============================================
            self.logger.info("Imprimiendo código de barras gráfico EAN-13: %s", barcode)
            
            # Configurar altura del código de barras (80 dots = ~10mm)
            content.extend(self.CMD_BARCODE_HEIGHT.encode('cp437', errors='ignore'))
            
            # Configurar ancho de barras (2 = delgado, 3 = medio, 4 = grueso)
            content.extend(self.CMD_BARCODE_WIDTH.encode('cp437', errors='ignore'))
            
            # Configurar posición del texto (2 = debajo del código)
            content.extend(self.CMD_BARCODE_TXT_BELOW.encode('cp437', errors='ignore'))
            
            # Configurar fuente del texto
            content.extend(self.CMD_BARCODE_FONT.encode('cp437', errors='ignore'))
            
            # Imprimir código de barras EAN-13
            # Formato: GS k 67 n [datos]
            # 67 = tipo EAN-13 (formato 2)
            # n = cantidad de dígitos (debe ser 12, el último dígito es check)
            barcode_data = barcode[:12]  # Tomar solo los primeros 12 dígitos (el 13° es check digit)
            
            # Comando de impresión de código de barras
            content.extend(self.CMD_BARCODE_PRINT.encode('cp437', errors='ignore'))
            content.extend(chr(67).encode('cp437', errors='ignore'))  # Tipo: EAN-13
            content.extend(chr(12).encode('cp437', errors='ignore'))  # Longitud: 12 dígitos
            content.extend(barcode_data.encode('cp437', errors='ignore'))  # Datos
            
            self.logger.debug("Comando de código de barras enviado (EAN-13, datos=%s)", barcode_data)
            
            # Espacio después del código de barras
            content.extend(b'\n\n')
            
            # Espacios finales antes de cortar
            content.extend(b'\n')
            
            # Cortar papel
            content.extend(self.CMD_CUT.encode('cp437', errors='ignore'))
            
            # Enviar a la impresora
            hPrinter = win32print.OpenPrinter(self.printer_name)
            try:
                hJob = win32print.StartDocPrinter(hPrinter, 1, (f"Barcode-{sku}", None, "RAW"))
                try:
                    win32print.StartPagePrinter(hPrinter)
                    win32print.WritePrinter(hPrinter, bytes(content))
                    win32print.EndPagePrinter(hPrinter)
                finally:
                    win32print.EndDocPrinter(hPrinter)
            finally:
                win32print.ClosePrinter(hPrinter)
            
            self.logger.info("Código de barras enviado exitosamente")
            return True
            
        except Exception:
            self.logger.exception("Error imprimiendo código de barras")
            return False
    
    def test_printer(self) -> bool:
        """Imprimir ticket de prueba"""
        try:
            from datetime import datetime
            
            test_data = {
                'sale_number': 'TEST-001',
                'date': datetime.now(),
                'cashier': 'PRUEBA SISTEMA',
                'customer': {'name': 'Cliente de Prueba'},
                'items': [
                    {
                        'name': 'Producto de Prueba',
                        'quantity': 1,
                        'price': 10.00,
                        'total': 10.00
                    }
                ],
                'subtotal': 8.47,
                'discount': 0,
                'igv': 1.53,
                'total': 10.00,
                'payment_method': 'cash',
                'paid_amount': 20.00,
                'change_amount': 10.00
            }
            
            test_config = {
                'company_name': 'TICKET DE PRUEBA',
                'company_address': 'Sistema POS',
                'company_city': 'Lima, Peru',
                'company_phone': '999-999-999',
                'company_email': 'test@pos.com',
                'company_ruc': '12345678901',
                'print_logo': True,
                'logo_text': '*** TEST ***',
                'ticket_footer_message': 'Ticket de prueba',
                'ticket_footer_message_2': 'Sistema funcionando correctamente',
                'print_barcode': False
            }
            
            return self.print_ticket(test_data, test_config)
        
        except Exception as e:
            self.logger.error("Error en test de impresora: %s", e, exc_info=True)
            return False


def load_printer_from_config() -> ThermalPrinter:
    """
    Cargar configuración de impresora desde system_config.json
    
    Returns:
        ThermalPrinter: Instancia configurada de la impresora
    """
    printer_name = None
    
    try:
        # Usar PathManager para obtener la configuración
        from utils.path_manager import load_config
        system_config = load_config('system_config.json')
        
        if system_config:
            printer_name = system_config.get('printer')

            logger.info("Configuración de impresora cargada")
            logger.info("Impresora configurada: %s", printer_name)
            logger.info("Auto-impresión habilitada: %s", system_config.get('auto_print', False))
    except Exception as e:
        logger.error("Error cargando configuración de impresora: %s", e, exc_info=True)
    
    return ThermalPrinter(printer_name)


# Ejemplo de uso
if __name__ == '__main__':
    print("🖨️ Módulo de Impresión Térmica - Sistema POS")
    print("=" * 50)
    
    # Cargar impresora desde configuración
    printer = load_printer_from_config()
    
    # Mostrar impresoras disponibles
    print("\n📋 Impresoras disponibles en el sistema:")
    for p in printer.get_available_printers():
        print(f"   - {p}")
    
    # Preguntar si hacer prueba
    print(f"\n¿Desea imprimir un ticket de prueba en '{printer.printer_name}'? (s/n): ", end='')
    response = input().strip().lower()
    
    if response == 's':
        print("\n🖨️ Imprimiendo ticket de prueba...")
        if printer.test_printer():
            print("✅ Ticket de prueba impreso exitosamente")
        else:
            print("❌ Error imprimiendo ticket de prueba")
