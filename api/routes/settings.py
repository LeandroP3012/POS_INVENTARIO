"""
Ruta: /api/settings
Configuración del sistema: ticket, empresa, etc.
"""

import json
import os
from typing import Dict, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.auth_middleware import get_current_user

router = APIRouter()

# Ruta absoluta al archivo de configuración del ticket
_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "config",
    "ticket_config.json",
)


class TicketConfigUpdate(BaseModel):
    company_name: Optional[str] = None
    company_address: Optional[str] = None
    company_city: Optional[str] = None
    company_phone: Optional[str] = None
    company_email: Optional[str] = None
    company_ruc: Optional[str] = None
    footer_message: Optional[str] = None
    footer_message_2: Optional[str] = None
    show_logo: Optional[bool] = None
    print_copy: Optional[bool] = None
    show_barcode: Optional[bool] = None


def _read_config() -> dict:
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_config(data: dict) -> None:
    with open(_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


@router.get("/ticket")
def get_ticket_config(current_user: Dict = Depends(get_current_user)):
    """Obtener configuración actual del ticket"""
    try:
        config = _read_config()
        return {"success": True, "data": config}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo de configuración no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/ticket")
def update_ticket_config(
    config: TicketConfigUpdate, current_user: Dict = Depends(get_current_user)
):
    """Actualizar configuración del ticket"""
    try:
        current = _read_config()
        updates = {k: v for k, v in config.dict().items() if v is not None}
        current.update(updates)
        _write_config(current)
        return {"success": True, "message": "Configuración actualizada", "data": current}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
