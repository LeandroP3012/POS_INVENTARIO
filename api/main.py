"""
Backend FastAPI - Sistema POS
Punto de entrada de la API REST para la app móvil
"""

import sys
import os

# Asegurar que el directorio raíz del POS esté en el path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import auth, products, sales, categories, reports, users, customers, credit_notes, print as print_router, roles, settings

app = FastAPI(
    title="Sistema POS API",
    description="API REST para el Sistema POS - T-Gestiona",
    version="1.0.0",
)

# CORS para permitir conexiones desde la app móvil y web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(auth.router,         prefix="/api/auth",         tags=["Autenticación"])
app.include_router(products.router,     prefix="/api/products",     tags=["Productos"])
app.include_router(sales.router,        prefix="/api/sales",        tags=["Ventas"])
app.include_router(categories.router,   prefix="/api/categories",   tags=["Categorías"])
app.include_router(reports.router,      prefix="/api/reports",      tags=["Reportes"])
app.include_router(users.router,        prefix="/api/users",        tags=["Usuarios"])
app.include_router(customers.router,    prefix="/api/customers",    tags=["Clientes"])
app.include_router(credit_notes.router, prefix="/api/credit-notes", tags=["Notas de Crédito"])
app.include_router(print_router.router,  prefix="/api/print",         tags=["Impresión"])
app.include_router(roles.router,         prefix="/api/roles",         tags=["Roles"])
app.include_router(settings.router,      prefix="/api/settings",      tags=["Configuración"])


@app.get("/")
def root():
    return {"status": "ok", "message": "Sistema POS API activa"}


@app.get("/health")
def health():
    return {"status": "healthy"}
