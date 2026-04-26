"""
Ruta: /api/products
CRUD de productos e inventario
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from api.auth_middleware import get_current_user
from controllers.product_controller import ProductController

router = APIRouter()
product_ctrl = ProductController()


# ── Schemas ──────────────────────────────────────────────────────────────────

class ProductCreate(BaseModel):
    name: str
    sku: Optional[str] = None
    description: Optional[str] = ""
    category_id: Optional[int] = None
    unit_id: Optional[int] = None
    price: float
    cost: Optional[float] = 0.0
    stock_quantity: Optional[float] = 0
    min_stock: Optional[float] = 0
    max_stock: Optional[float] = 0
    status: Optional[str] = "active"


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    unit_id: Optional[int] = None
    price: Optional[float] = None
    cost: Optional[float] = None
    stock_quantity: Optional[float] = None
    min_stock: Optional[float] = None
    max_stock: Optional[float] = None
    status: Optional[str] = None


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.get("/")
def list_products(current_user: Dict = Depends(get_current_user)):
    """Listar todos los productos"""
    result = product_ctrl.get_all_products(current_user)
    if isinstance(result, dict) and not result.get("success", True):
        raise HTTPException(status_code=500, detail=result.get("message", "Error"))
    return result


@router.get("/{product_id}")
def get_product(product_id: int, current_user: Dict = Depends(get_current_user)):
    """Obtener un producto por ID"""
    result = product_ctrl.get_product_by_id(product_id, current_user)
    if not result:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, current_user: Dict = Depends(get_current_user)):
    """Crear nuevo producto"""
    success, message, product_id = product_ctrl.create_product(product.dict(), current_user)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message, "product_id": product_id}


@router.put("/{product_id}")
def update_product(product_id: int, product: ProductUpdate, current_user: Dict = Depends(get_current_user)):
    """Actualizar producto"""
    data = {k: v for k, v in product.dict().items() if v is not None}
    success, message = product_ctrl.update_product(product_id, data, current_user)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message}


@router.delete("/{product_id}")
def delete_product(product_id: int, current_user: Dict = Depends(get_current_user)):
    """Eliminar producto"""
    success, message = product_ctrl.delete_product(product_id, current_user)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message}


@router.get("/low-stock/alerts")
def low_stock(current_user: Dict = Depends(get_current_user)):
    """Productos con stock bajo"""
    return product_ctrl.get_low_stock_products(current_user)
