"""
Ruta: /api/roles
Gestión de roles y permisos del sistema
"""

from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from api.auth_middleware import get_current_user
from controllers.role_controller import RoleController
from config.permissions_catalog import PERMISSIONS_CATALOG

router = APIRouter()
role_ctrl = RoleController()


class RoleCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = ""
    permissions: Optional[List[str]] = []


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[List[str]] = None


@router.get("/")
def list_roles(current_user: Dict = Depends(get_current_user)):
    """Listar todos los roles"""
    roles = role_ctrl.get_all_roles()
    return {"success": True, "data": roles}


@router.get("/permissions-catalog")
def get_permissions_catalog(current_user: Dict = Depends(get_current_user)):
    """Obtener catálogo completo de permisos disponibles"""
    return {"success": True, "data": PERMISSIONS_CATALOG}


@router.get("/{role_id}")
def get_role(role_id: int, current_user: Dict = Depends(get_current_user)):
    """Obtener rol por ID con sus permisos"""
    role = role_ctrl.get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {"success": True, "data": role}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_role(role: RoleCreate, current_user: Dict = Depends(get_current_user)):
    """Crear nuevo rol"""
    success, message, role_id = role_ctrl.create_role(role.dict(), current_user)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message, "role_id": role_id}


@router.put("/{role_id}")
def update_role(
    role_id: int, role: RoleUpdate, current_user: Dict = Depends(get_current_user)
):
    """Actualizar rol (nombre, descripción o permisos)"""
    data = {k: v for k, v in role.dict().items() if v is not None}
    success, message = role_ctrl.update_role(role_id, data, current_user)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message}


@router.delete("/{role_id}")
def delete_role(role_id: int, current_user: Dict = Depends(get_current_user)):
    """Eliminar rol (solo si no es de sistema y no tiene usuarios)"""
    success, message = role_ctrl.delete_role(role_id, current_user)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message}
