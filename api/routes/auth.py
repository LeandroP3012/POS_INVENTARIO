"""
Ruta: /api/auth
Autenticación de usuarios - login y refresh de token
"""

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
    token = create_access_token(token_data)

    return LoginResponse(
        access_token=token,
        user_id=user["id"],
        username=user["username"],
        full_name=user.get("full_name", user["username"]),
        user_type=user.get("user_type", "user"),
        role_id=user.get("role_id"),
    )
