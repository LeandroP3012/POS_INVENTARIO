"""
Ruta: /api/auth
Autenticación de usuarios - login y refresh de token
"""

import json
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from api.auth_middleware import create_access_token
from models.user_model import UserModel

router = APIRouter()
user_model = UserModel()


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    full_name: str
    user_type: str
    role_id: int | None = None


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    """Autenticar usuario y retornar token JWT"""
    user = user_model.find_by_username(request.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )

    if not user_model.verify_password(request.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )

    if not user.get("active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )

    token_data = {
        "sub": str(user["id"]),
        "username": user["username"],
        "user_type": user.get("user_type", "user"),
        "role_id": user.get("role_id"),
    }

    # Incluir custom_permissions en el token para que el PermissionService
    # pueda verificar permisos sin consultar la BD en cada request
    raw_perms = user.get("custom_permissions") or user.get("permissions")
    if raw_perms:
        if isinstance(raw_perms, str):
            try:
                raw_perms = json.loads(raw_perms)
            except (json.JSONDecodeError, ValueError):
                raw_perms = None
        if raw_perms:
            token_data["permissions"] = raw_perms

    token = create_access_token(token_data)

    return LoginResponse(
        access_token=token,
        user_id=user["id"],
        username=user["username"],
        full_name=user.get("full_name", user["username"]),
        user_type=user.get("user_type", "user"),
        role_id=user.get("role_id"),
    )
