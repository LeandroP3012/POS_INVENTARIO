"""
Ruta: /api/print
Envío de tickets ESC/POS a impresoras térmicas en red (por IP:Puerto TCP)
"""

import socket
import struct
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter()

# ── Comandos ESC/POS básicos ────────────────────────────────────────────────

ESC  = b'\x1b'
GS   = b'\x1d'
INIT = ESC + b'@'                        # Inicializar impresora
CUT  = GS  + b'V\x41\x03'               # Corte parcial
LF   = b'\n'
BOLD_ON  = ESC + b'E\x01'
BOLD_OFF = ESC + b'E\x00'
CENTER   = ESC + b'a\x01'
LEFT     = ESC + b'a\x00'
RIGHT    = ESC + b'a\x02'
LARGE    = GS  + b'!\x11'               # 2x ancho + 2x alto
NORMAL   = GS  + b'!\x00'
LINE_SIMPLE = b'-' * 42 + LF


def _encode(text: str) -> bytes:
    """Codifica texto para impresoras ESC/POS (Latin-1 con fallback)."""
    return text.encode('latin-1', errors='replace')


def _line(text: str, width: int = 42) -> bytes:
    return _encode(text[:width].ljust(width)) + LF


def _two_col(left: str, right: str, width: int = 42) -> bytes:
    right = right[-20:] if len(right) > 20 else right
    left = left[: width - len(right) - 1]
    return _encode(f"{left:<{width - len(right) - 1}} {right}") + LF


# ── Generación del ticket ───────────────────────────────────────────────────

def _build_ticket(sale: Dict[str, Any]) -> bytes:
    """Construye los bytes del ticket a partir del dict de venta."""
    buf = bytearray()

    buf += INIT
    buf += CENTER

    # Encabezado
    buf += BOLD_ON + LARGE
    buf += _encode("T-GESTIONA POS") + LF
    buf += NORMAL + BOLD_OFF
    buf += _encode("Sistema de Punto de Venta") + LF
    buf += LINE_SIMPLE

    # Datos de la venta
    buf += LEFT
    sale_id = sale.get('sale_id') or sale.get('id', '')
    sale_date = sale.get('sale_date') or sale.get('created_at', '')
    cashier = sale.get('cashier_name') or sale.get('user', '')

    buf += _encode(f"Venta N°: {sale_id}") + LF
    buf += _encode(f"Fecha:    {str(sale_date)[:19]}") + LF
    if cashier:
        buf += _encode(f"Cajero:   {cashier}") + LF
    buf += LINE_SIMPLE

    # Items del carrito
    items: List[Dict] = sale.get('items') or sale.get('cart_items') or []
    for item in items:
        name  = str(item.get('product_name') or item.get('name', 'Producto'))
        qty   = item.get('quantity', 1)
        price = float(item.get('unit_price') or item.get('price', 0))
        sub   = float(item.get('subtotal', qty * price))
        buf += _encode(f"  {name[:30]}") + LF
        buf += _two_col(f"  {qty} x S/ {price:.2f}", f"S/ {sub:.2f}")

    buf += LINE_SIMPLE

    # Totales
    payment = sale.get('payment_info') or {}
    total       = float(sale.get('total_amount') or payment.get('total', 0))
    paid        = float(payment.get('paid_amount') or sale.get('paid_amount', total))
    change      = float(payment.get('change_amount') or sale.get('change_amount', 0))
    method      = str(payment.get('method') or sale.get('payment_method', 'Efectivo'))
    include_tax = payment.get('include_tax', True)

    if include_tax and total > 0:
        base_imp = total / 1.18
        igv      = total - base_imp
        buf += _two_col("  OP. GRAVADA:", f"S/ {base_imp:.2f}")
        buf += _two_col("  IGV (18%):",   f"S/ {igv:.2f}")

    buf += BOLD_ON
    buf += _two_col("  TOTAL:", f"S/ {total:.2f}")
    buf += BOLD_OFF
    buf += _two_col(f"  {method.upper()}:", f"S/ {paid:.2f}")
    if change > 0:
        buf += _two_col("  VUELTO:", f"S/ {change:.2f}")

    # Pie
    buf += LINE_SIMPLE
    buf += CENTER
    buf += _encode("Gracias por su compra") + LF
    buf += _encode("Conserve su ticket") + LF
    buf += LF + LF + LF
    buf += CUT

    return bytes(buf)


# ── Helper TCP ──────────────────────────────────────────────────────────────

def _send_to_printer(ip: str, port: int, data: bytes, timeout: int = 5) -> None:
    """Abre conexión TCP con la impresora y envía los bytes."""
    try:
        with socket.create_connection((ip, port), timeout=timeout) as sock:
            sock.sendall(data)
    except socket.timeout:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Tiempo de espera agotado al conectar con {ip}:{port}",
        )
    except ConnectionRefusedError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Conexión rechazada por {ip}:{port}. Verifique que la impresora esté encendida.",
        )
    except OSError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error de red: {e}",
        )


# ── Schemas ─────────────────────────────────────────────────────────────────

class PrintTicketRequest(BaseModel):
    printer_ip: str   = Field(..., description="IP de la impresora")
    printer_port: int = Field(9100, description="Puerto TCP (default 9100)")
    sale: Dict[str, Any] = Field(..., description="Datos de la venta")


class PrintTestRequest(BaseModel):
    printer_ip: str   = Field(..., description="IP de la impresora")
    printer_port: int = Field(9100, description="Puerto TCP (default 9100)")


# ── Rutas ────────────────────────────────────────────────────────────────────

@router.post("/ticket", summary="Imprime ticket de venta en impresora térmica")
def print_ticket(req: PrintTicketRequest):
    """
    Genera un ticket ESC/POS a partir de los datos de la venta
    y lo envía por TCP a la impresora con la IP/puerto indicados.
    """
    data = _build_ticket(req.sale)
    _send_to_printer(req.printer_ip, req.printer_port, data)
    return {"status": "printed", "printer": f"{req.printer_ip}:{req.printer_port}"}


@router.post("/test", summary="Prueba de conexión con impresora")
def test_printer(req: PrintTestRequest):
    """Envía una línea de prueba a la impresora para verificar la conexión."""
    buf  = INIT + CENTER
    buf += BOLD_ON + _encode("-- PRUEBA DE IMPRESION --") + LF + BOLD_OFF
    buf += _encode("T-Gestiona POS") + LF
    buf += LINE_SIMPLE
    buf += _encode("Impresora configurada OK") + LF
    buf += LF + LF + CUT
    _send_to_printer(req.printer_ip, req.printer_port, buf)
    return {"status": "ok", "printer": f"{req.printer_ip}:{req.printer_port}"}
