"""
Ruta: /api/users
Gestión de usuarios del sistema
"""

from typing import Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from api.auth_middleware import get_current_user
from controllers.user_controller import UserController

router = APIRouter()
user_ctrl = UserController()


class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    email: Optional[str] = None
    user_type: str = "cashier"
    role_id: Optional[int] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    user_type: Optional[str] = None
    role_id: Optional[int] = None
    active: Optional[bool] = None


@router.get("/")
def list_users(current_user: Dict = Depends(get_current_user)):
    return user_ctrl.get_all_users_with_roles()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, current_user: Dict = Depends(get_current_user)):
    success, message, user_id = user_ctrl.create_user(user.dict(), current_user)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message, "user_id": user_id}


@router.put("/{user_id}")
def update_user(user_id: int, user: UserUpdate, current_user: Dict = Depends(get_current_user)):
    data = {k: v for k, v in user.dict().items() if v is not None}
    data["id"] = user_id
    success, message = user_ctrl.update_user(data, current_user)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message}


@router.delete("/{user_id}")
def delete_user(user_id: int, current_user: Dict = Depends(get_current_user)):
    success, message = user_ctrl.delete_user(user_id, current_user)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message}
