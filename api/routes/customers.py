"""
Ruta: /api/customers
Gestión de clientes
"""

from typing import Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel

from api.auth_middleware import get_current_user
from models.customer_model import CustomerModel

router = APIRouter()
customer_model = CustomerModel()


class CustomerCreate(BaseModel):
    name: str
    code: Optional[str] = None
    document_number: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


@router.get("/")
def list_customers(
    search: Optional[str] = Query(default=None),
    current_user: Dict = Depends(get_current_user),
):
    if search:
        return customer_model.search_customers(search)
    return customer_model.get_all_active()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate, current_user: Dict = Depends(get_current_user)):
    result = customer_model.create_customer(customer.dict())
    if not result:
        raise HTTPException(status_code=400, detail="Error al crear cliente")
    return {"success": True, "customer_id": result}
