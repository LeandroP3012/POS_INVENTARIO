"""
Ruta: /api/sales
Procesar ventas y consultar historial
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from api.auth_middleware import get_current_user
from controllers.sale_controller import SaleController

router = APIRouter()
sale_ctrl = SaleController()


# ── Schemas ──────────────────────────────────────────────────────────────────

class CartItem(BaseModel):
    product_id: int
    product_name: str
    quantity: float
    unit_price: float
    subtotal: float


class PaymentInfo(BaseModel):
    method: str = "cash"              # cash | card | transfer
    paid_amount: float
    change_amount: float = 0.0
    discount_amount: float = 0.0
    include_tax: bool = True


class SaleRequest(BaseModel):
    cart_items: List[CartItem]
    customer_id: Optional[int] = None
    payment_info: PaymentInfo
    notes: Optional[str] = ""


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/", status_code=status.HTTP_201_CREATED)
def process_sale(sale: SaleRequest, current_user: Dict = Depends(get_current_user)):
    """Procesar una venta completa"""
    user_id = int(current_user.get("sub", 0))

    cart = [item.dict() for item in sale.cart_items]
    payment = sale.payment_info.dict()

    result = sale_ctrl.process_sale(
        cart_items=cart,
        customer_id=sale.customer_id,
        user_id=user_id,
        payment_info=payment,
        notes=sale.notes or "",
    )

    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "Error al procesar venta"))

    return result


@router.get("/")
def list_sales(
    limit: int = 50,
    current_user: Dict = Depends(get_current_user),
):
    """Listar ventas recientes"""
    result = sale_ctrl.get_sales_list(filters={'limit': limit})
    return result


@router.get("/{sale_id}")
def get_sale(sale_id: int, current_user: Dict = Depends(get_current_user)):
    """Obtener detalle de una venta"""
    result = sale_ctrl.get_sale_detail(sale_id)
    if not result:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return result


@router.post("/{sale_id}/cancel")
def cancel_sale(sale_id: int, current_user: Dict = Depends(get_current_user)):
    """Cancelar una venta"""
    result = sale_ctrl.cancel_sale(sale_id, int(current_user.get("sub", 0)), reason="Cancelado desde app móvil")
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "Error al cancelar"))
    return result
