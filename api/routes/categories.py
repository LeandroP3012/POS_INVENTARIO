"""
Ruta: /api/categories
CRUD de categorías de productos
"""

from typing import Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from api.auth_middleware import get_current_user
from controllers.category_controller import CategoryController

router = APIRouter()
category_ctrl = CategoryController()


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    parent_id: Optional[int] = None


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


@router.get("/")
def list_categories(
    include_inactive: bool = False,
    current_user: Dict = Depends(get_current_user),
):
    return category_ctrl.get_all_categories(current_user, include_inactive=include_inactive)


@router.get("/{category_id}")
def get_category(category_id: int, current_user: Dict = Depends(get_current_user)):
    result = category_ctrl.get_category_by_id(category_id, current_user)
    if not result:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, current_user: Dict = Depends(get_current_user)):
    success, message, cat_id = category_ctrl.create_category(category.dict(), current_user)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message, "category_id": cat_id}


@router.put("/{category_id}")
def update_category(category_id: int, category: CategoryUpdate, current_user: Dict = Depends(get_current_user)):
    data = {k: v for k, v in category.dict().items() if v is not None}
    success, message = category_ctrl.update_category(category_id, data, current_user)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message}


@router.delete("/{category_id}")
def delete_category(category_id: int, current_user: Dict = Depends(get_current_user)):
    success, message = category_ctrl.delete_category(category_id, current_user)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message}
