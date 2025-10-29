"""Catálogo centralizado de permisos del sistema POS.

Este módulo define una única fuente de verdad para los permisos disponibles en la
aplicación, su categorización, metadatos y reglas de publicación en la UI.
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional

PermissionItem = Dict[str, object]
PermissionCatalog = Dict[str, List[PermissionItem]]

PERMISSIONS_CATALOG: PermissionCatalog = {
    "Usuarios": [
        {
            "code": "users.view",
            "label": "Ver usuarios",
            "description": "Permite acceder al listado de usuarios y ver sus detalles.",
            "module": "users",
            "action": "view",
            "scope": "read",
            "assignable": True,
        },
        {
            "code": "users.create",
            "label": "Crear usuarios",
            "description": "Permite registrar nuevos usuarios en el sistema.",
            "module": "users",
            "action": "create",
            "scope": "write",
            "requires": ["users.view"],
            "assignable": True,
        },
        {
            "code": "users.edit",
            "label": "Editar usuarios",
            "description": "Autoriza la modificación de datos de usuarios existentes.",
            "module": "users",
            "action": "edit",
            "scope": "write",
            "requires": ["users.view"],
            "assignable": True,
        },
        {
            "code": "users.delete",
            "label": "Eliminar usuarios",
            "description": "Permite eliminar usuarios del sistema.",
            "module": "users",
            "action": "delete",
            "scope": "write",
            "requires": ["users.view"],
            "assignable": True,
        },
        {
            "code": "users.activate",
            "label": "Activar usuarios",
            "description": "Permite reactivar usuarios previamente deshabilitados.",
            "module": "users",
            "action": "activate",
            "scope": "write",
            "requires": ["users.view"],
            "assignable": True,
        },
        {
            "code": "users.deactivate",
            "label": "Desactivar usuarios",
            "description": "Autoriza suspender usuarios sin eliminarlos definitivamente.",
            "module": "users",
            "action": "deactivate",
            "scope": "write",
            "requires": ["users.view"],
            "assignable": True,
        },
        {
            "code": "users.export",
            "label": "Exportar usuarios",
            "description": "Permite exportar información de usuarios a archivos externos.",
            "module": "users",
            "action": "export",
            "scope": "read",
            "requires": ["users.view"],
            "assignable": True,
        },
    ],
    "Roles y Permisos": [
        {
            "code": "roles.view",
            "label": "Ver roles",
            "description": "Permite acceder al listado de roles y consultar sus detalles.",
            "module": "roles",
            "action": "view",
            "scope": "read",
            "assignable": True,
        },
        {
            "code": "roles.create",
            "label": "Crear roles",
            "description": "Autoriza la creación de nuevos roles personalizados.",
            "module": "roles",
            "action": "create",
            "scope": "write",
            "requires": ["roles.view"],
            "assignable": True,
        },
        {
            "code": "roles.edit",
            "label": "Editar roles",
            "description": "Permite modificar roles existentes (nombre, descripción, permisos).",
            "module": "roles",
            "action": "edit",
            "scope": "write",
            "requires": ["roles.view"],
            "assignable": True,
        },
        {
            "code": "roles.delete",
            "label": "Eliminar roles",
            "description": "Autoriza eliminar roles personalizados que no estén en uso.",
            "module": "roles",
            "action": "delete",
            "scope": "write",
            "requires": ["roles.view"],
            "assignable": True,
        },
        {
            "code": "roles.permissions",
            "label": "Gestionar permisos",
            "description": "Permite abrir el gestor de permisos y actualizar permisos asignados.",
            "module": "roles",
            "action": "permissions",
            "scope": "write",
            "requires": ["roles.view"],
            "assignable": True,
        },
        {
            "code": "roles.assign",
            "label": "Asignar roles",
            "description": "Permite asignar roles a usuarios desde el gestor (función legacy).",
            "module": "roles",
            "action": "assign",
            "scope": "write",
            "assignable": False,
            "requires": ["roles.view"],
            "status": "legacy",
        },
    ],
    "Sistema": [
        {
            "code": "system.config",
            "label": "Configurar sistema",
            "description": "Permite acceder y modificar la configuración general del sistema.",
            "module": "system",
            "action": "config",
            "scope": "admin",
            "assignable": True,
        },
        {
            "code": "system.backup",
            "label": "Respaldos",
            "description": "Autoriza generar respaldos completos del sistema (en desarrollo).",
            "module": "system",
            "action": "backup",
            "scope": "admin",
            "assignable": False,
            "status": "planned",
        },
        {
            "code": "system.restore",
            "label": "Restaurar sistema",
            "description": "Permite restaurar un respaldo previo del sistema (en desarrollo).",
            "module": "system",
            "action": "restore",
            "scope": "admin",
            "assignable": False,
            "status": "planned",
        },
        {
            "code": "system.logs",
            "label": "Ver logs",
            "description": "Permite visualizar el historial de logs del sistema.",
            "module": "system",
            "action": "logs",
            "scope": "read",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "system.maintenance",
            "label": "Modo mantenimiento",
            "description": "Permite habilitar el modo mantenimiento (característica legacy).",
            "module": "system",
            "action": "maintenance",
            "scope": "admin",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "system.reports",
            "label": "Reportes del sistema",
            "description": "Acceso a reportes técnicos del sistema (no disponible actualmente).",
            "module": "system",
            "action": "reports",
            "scope": "admin",
            "assignable": False,
            "status": "planned",
        },
    ],
    "Dashboard": [
        {
            "code": "dashboard.view",
            "label": "Ver dashboard",
            "description": "Permite ingresar al panel principal con indicadores.",
            "module": "dashboard",
            "action": "view",
            "scope": "read",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "dashboard.stats",
            "label": "Ver estadísticas",
            "description": "Autoriza la vista de estadísticas avanzadas en el dashboard.",
            "module": "dashboard",
            "action": "stats",
            "scope": "read",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "dashboard.analytics",
            "label": "Ver analíticas",
            "description": "Permite acceder a reportes analíticos (feature pendiente).",
            "module": "dashboard",
            "action": "analytics",
            "scope": "read",
            "assignable": False,
            "status": "planned",
        },
    ],
    "Inventario": [
        {
            "code": "inventory.view",
            "label": "Ver inventario",
            "description": "Permite acceder al catálogo de productos y ver existencias.",
            "module": "inventory",
            "action": "view",
            "scope": "read",
            "assignable": True,
        },
        {
            "code": "inventory.create",
            "label": "Crear productos",
            "description": "Autoriza agregar nuevos productos al inventario.",
            "module": "inventory",
            "action": "create",
            "scope": "write",
            "requires": ["inventory.view"],
            "assignable": True,
        },
        {
            "code": "inventory.edit",
            "label": "Editar inventario",
            "description": "Permite modificar información de productos existentes.",
            "module": "inventory",
            "action": "edit",
            "scope": "write",
            "requires": ["inventory.view"],
            "assignable": True,
        },
        {
            "code": "inventory.delete",
            "label": "Eliminar productos",
            "description": "Autoriza remover productos del inventario.",
            "module": "inventory",
            "action": "delete",
            "scope": "write",
            "requires": ["inventory.view"],
            "assignable": True,
        },
        {
            "code": "inventory.stock",
            "label": "Ajustar stock",
            "description": "Permite realizar ajustes manuales de existencia.",
            "module": "inventory",
            "action": "stock",
            "scope": "write",
            "requires": ["inventory.view"],
            "assignable": True,
        },
        {
            "code": "inventory.export",
            "label": "Exportar inventario",
            "description": "Permite exportar listado de productos y existencias.",
            "module": "inventory",
            "action": "export",
            "scope": "read",
            "requires": ["inventory.view"],
            "assignable": True,
        },
        {
            "code": "inventory.reports",
            "label": "Reportes de inventario",
            "description": "Acceso a reportes históricos de inventario (pendiente).",
            "module": "inventory",
            "action": "reports",
            "scope": "read",
            "assignable": False,
            "status": "planned",
        },
    ],
    "Ventas": [
        {
            "code": "sales.view",
            "label": "Ver ventas",
            "description": "Permite revisar el historial completo de ventas.",
            "module": "sales",
            "action": "view",
            "scope": "read",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "sales.create",
            "label": "Registrar ventas",
            "description": "Autoriza generar nuevas ventas desde el punto de venta.",
            "module": "sales",
            "action": "create",
            "scope": "write",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "sales.edit",
            "label": "Editar ventas",
            "description": "Permite modificar ventas registradas (solo supervisores).",
            "module": "sales",
            "action": "edit",
            "scope": "write",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "sales.delete",
            "label": "Eliminar ventas",
            "description": "Autoriza anular ventas existentes.",
            "module": "sales",
            "action": "delete",
            "scope": "write",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "sales.view_own",
            "label": "Ver ventas propias",
            "description": "Permite a un usuario consultar solo sus ventas registradas.",
            "module": "sales",
            "action": "view_own",
            "scope": "read",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "sales.reports",
            "label": "Reportes de ventas",
            "description": "Acceso a reportes globales de ventas.",
            "module": "sales",
            "action": "reports",
            "scope": "read",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "sales.export",
            "label": "Exportar ventas",
            "description": "Permite exportar el registro de ventas a archivos externos.",
            "module": "sales",
            "action": "export",
            "scope": "read",
            "assignable": False,
            "status": "legacy",
        },
    ],
    "Caja": [
        {
            "code": "cash.register",
            "label": "Operar caja",
            "description": "Permite usar la caja registradora en el punto de venta.",
            "module": "cash",
            "action": "register",
            "scope": "write",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "cash.open",
            "label": "Abrir caja",
            "description": "Autoriza la apertura del turno de caja (en desarrollo).",
            "module": "cash",
            "action": "open",
            "scope": "write",
            "assignable": False,
            "status": "planned",
        },
        {
            "code": "cash.close",
            "label": "Cerrar caja",
            "description": "Permite cerrar y cuadrar la caja (en desarrollo).",
            "module": "cash",
            "action": "close",
            "scope": "write",
            "assignable": False,
            "status": "planned",
        },
        {
            "code": "cash.reports",
            "label": "Reportes de caja",
            "description": "Permite acceder a reportes de movimientos de caja.",
            "module": "cash",
            "action": "reports",
            "scope": "read",
            "assignable": False,
            "status": "planned",
        },
    ],
    "Productos": [
        {
            "code": "products.view",
            "label": "Ver productos",
            "description": "Permite consultar el listado de productos disponibles.",
            "module": "products",
            "action": "view",
            "scope": "read",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "products.create",
            "label": "Crear productos",
            "description": "Autoriza la creación de nuevos productos (módulo legacy).",
            "module": "products",
            "action": "create",
            "scope": "write",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "products.edit",
            "label": "Editar productos",
            "description": "Permite actualizar información detallada de productos.",
            "module": "products",
            "action": "edit",
            "scope": "write",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "products.delete",
            "label": "Eliminar productos",
            "description": "Autoriza borrar productos del catálogo (legacy).",
            "module": "products",
            "action": "delete",
            "scope": "write",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "products.prices",
            "label": "Gestionar precios",
            "description": "Permite actualizar listas de precios de productos.",
            "module": "products",
            "action": "prices",
            "scope": "write",
            "assignable": False,
            "status": "planned",
        },
        {
            "code": "products.categories",
            "label": "Gestionar categorías",
            "description": "Permite administrar la jerarquía de categorías de productos.",
            "module": "products",
            "action": "categories",
            "scope": "write",
            "assignable": False,
            "status": "planned",
        },
    ],
    "Clientes": [
        {
            "code": "customers.view",
            "label": "Ver clientes",
            "description": "Permite revisar el listado de clientes registrados.",
            "module": "customers",
            "action": "view",
            "scope": "read",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "customers.create",
            "label": "Crear clientes",
            "description": "Autoriza registrar nuevos clientes en el sistema.",
            "module": "customers",
            "action": "create",
            "scope": "write",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "customers.edit",
            "label": "Editar clientes",
            "description": "Permite actualizar datos de clientes.",
            "module": "customers",
            "action": "edit",
            "scope": "write",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "customers.delete",
            "label": "Eliminar clientes",
            "description": "Autoriza eliminar clientes del sistema.",
            "module": "customers",
            "action": "delete",
            "scope": "write",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "customers.export",
            "label": "Exportar clientes",
            "description": "Permite exportar el listado de clientes.",
            "module": "customers",
            "action": "export",
            "scope": "read",
            "assignable": False,
            "status": "legacy",
        },
    ],
    "Proveedores": [
        {
            "code": "suppliers.view",
            "label": "Ver proveedores",
            "description": "Permite consultar proveedores registrados.",
            "module": "suppliers",
            "action": "view",
            "scope": "read",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "suppliers.create",
            "label": "Crear proveedores",
            "description": "Autoriza registrar nuevos proveedores (módulo legacy).",
            "module": "suppliers",
            "action": "create",
            "scope": "write",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "suppliers.edit",
            "label": "Editar proveedores",
            "description": "Permite actualizar información de proveedores.",
            "module": "suppliers",
            "action": "edit",
            "scope": "write",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "suppliers.delete",
            "label": "Eliminar proveedores",
            "description": "Autoriza eliminar proveedores del sistema.",
            "module": "suppliers",
            "action": "delete",
            "scope": "write",
            "assignable": False,
            "status": "legacy",
        },
    ],
    "Reportes": [
        {
            "code": "reports.basic",
            "label": "Reportes básicos",
            "description": "Permite acceder a reportes resumidos (Ventas del día).",
            "module": "reports",
            "action": "basic",
            "scope": "read",
            "assignable": True,
            "aliases": ["reports_basic"],
        },
        {
            "code": "reports.full",
            "label": "Reportes completos",
            "description": "Autoriza reportes completos y avanzados dentro del módulo.",
            "module": "reports",
            "action": "full",
            "scope": "read",
            "assignable": True,
            "requires": ["reports.basic"],
            "aliases": ["reports_full"],
        },
        {
            "code": "reports.sales",
            "label": "Reportes de ventas",
            "description": "Reportes detallados de ventas (feature en transición).",
            "module": "reports",
            "action": "sales",
            "scope": "read",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "reports.inventory",
            "label": "Reportes de inventario",
            "description": "Reportes especializados de inventario (feature en transición).",
            "module": "reports",
            "action": "inventory",
            "scope": "read",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "reports.users",
            "label": "Reportes de usuarios",
            "description": "Reportes centrados en actividad de usuarios.",
            "module": "reports",
            "action": "users",
            "scope": "read",
            "assignable": False,
            "status": "legacy",
        },
        {
            "code": "reports.financial",
            "label": "Reportes financieros",
            "description": "Reportes financieros avanzados (feature pendiente).",
            "module": "reports",
            "action": "financial",
            "scope": "read",
            "assignable": False,
            "status": "planned",
        },
        {
            "code": "reports.export",
            "label": "Exportar reportes",
            "description": "Permite exportar reportes en diferentes formatos.",
            "module": "reports",
            "action": "export",
            "scope": "read",
            "assignable": False,
            "status": "legacy",
        },
    ],
}

_PERMISSION_INDEX: Dict[str, PermissionItem] = {}
_CATEGORY_BY_CODE: Dict[str, str] = {}
_ALIAS_TO_CODE: Dict[str, str] = {}

for category, items in PERMISSIONS_CATALOG.items():
    for item in items:
        code = item["code"]
        _PERMISSION_INDEX[code] = item
        _CATEGORY_BY_CODE[code] = category
        for alias in item.get("aliases", []):
            _ALIAS_TO_CODE[alias] = code

ALL_PERMISSION_CODES = set(_PERMISSION_INDEX.keys())
ASSIGNABLE_PERMISSION_CODES = {
    code for code, item in _PERMISSION_INDEX.items() if item.get("assignable", True)
}


def get_permissions_by_category(assignable_only: bool = False) -> Dict[str, List[str]]:
    """Retornar permisos organizados por categoría.

    Args:
        assignable_only: Si es True, solo incluye los permisos marcados como asignables.
    """
    result: Dict[str, List[str]] = {}
    for category, items in PERMISSIONS_CATALOG.items():
        codes: List[str] = []
        for item in items:
            if assignable_only and not item.get("assignable", True):
                continue
            codes.append(item["code"])
        if codes:
            result[category] = codes
    return result


def get_all_permission_codes(assignable_only: bool = False) -> List[str]:
    """Obtener lista plana de códigos de permisos."""
    if assignable_only:
        return list(ASSIGNABLE_PERMISSION_CODES)
    return list(ALL_PERMISSION_CODES)


def get_permission_info(code: str) -> Optional[PermissionItem]:
    """Obtener metadatos completos de un permiso."""
    canonical = normalize_permission_code(code)
    return _PERMISSION_INDEX.get(canonical)


def get_permission_label(code: str) -> str:
    """Obtener etiqueta amigable de un permiso."""
    info = get_permission_info(code)
    if not info:
        return code
    label = info.get("label")
    return str(label) if label else info["code"]


def normalize_permission_code(code: str) -> str:
    """Convertir un permiso a su código canónico."""
    return _ALIAS_TO_CODE.get(code, code)


def normalize_permissions(
    permissions: Iterable[str],
    drop_unknown: bool = True,
) -> List[str]:
    """Normalizar una lista de permisos (alias, duplicados, orden).

    Args:
        permissions: Secuencia de códigos a normalizar.
        drop_unknown: Si es True se descartan permisos desconocidos.
    """
    normalized: List[str] = []
    seen: set[str] = set()
    for permission in permissions:
        if not permission:
            continue
        canonical = normalize_permission_code(permission)
        if canonical in ALL_PERMISSION_CODES:
            if canonical not in seen:
                normalized.append(canonical)
                seen.add(canonical)
        elif not drop_unknown and permission not in seen:
            normalized.append(permission)
            seen.add(permission)
    return normalized


def is_assignable(code: str) -> bool:
    """Indica si el permiso está disponible para asignarse desde la UI."""
    canonical = normalize_permission_code(code)
    return canonical in ASSIGNABLE_PERMISSION_CODES


def get_category(code: str) -> Optional[str]:
    """Retorna la categoría asociada a un permiso."""
    canonical = normalize_permission_code(code)
    return _CATEGORY_BY_CODE.get(canonical)


def iter_permission_items(assignable_only: bool = False):
    """Iterar sobre los permisos con sus metadatos."""
    for category, items in PERMISSIONS_CATALOG.items():
        for item in items:
            if assignable_only and not item.get("assignable", True):
                continue
            yield category, item


__all__ = [
    "PERMISSIONS_CATALOG",
    "get_permissions_by_category",
    "get_all_permission_codes",
    "get_permission_info",
    "get_permission_label",
    "normalize_permission_code",
    "normalize_permissions",
    "is_assignable",
    "get_category",
    "iter_permission_items",
]
