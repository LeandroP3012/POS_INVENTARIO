"""
Ruta: /api/credit-notes
Gestión de notas de crédito / devoluciones
"""

from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from api.auth_middleware import get_current_user
from controllers.credit_note_controller import CreditNoteController

router = APIRouter()
cn_ctrl = CreditNoteController()


class CreditNoteItem(BaseModel):
    sale_item_id: int
    quantity: float
    reason: Optional[str] = ""


class CreditNoteCreate(BaseModel):
    sale_id: int
    reason: str
    items: Optional[List[CreditNoteItem]] = None


@router.get("/")
def list_credit_notes(
    limit: int = 50,
    current_user: Dict = Depends(get_current_user),
):
    return cn_ctrl.list_credit_notes(limit=limit)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_credit_note(cn: CreditNoteCreate, current_user: Dict = Depends(get_current_user)):
    user_id = int(current_user.get("sub", 0))
    items = [i.dict() for i in cn.items] if cn.items else None
    result = cn_ctrl.create_credit_note(cn.sale_id, user_id, cn.reason, items)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "Error"))
    return result
