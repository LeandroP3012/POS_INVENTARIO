"""
Ruta: /api/reports
Reportes de ventas, productos e inventario
"""

from typing import Dict, Optional
from fastapi import APIRouter, Depends, Query
from datetime import date, timedelta

from api.auth_middleware import get_current_user
from controllers.report_controller import ReportController

router = APIRouter()
report_ctrl = ReportController()


@router.get("/sales")
def sales_report(
    start_date: str = Query(default=str(date.today() - timedelta(days=30))),
    end_date: str = Query(default=str(date.today())),
    user_id: Optional[int] = None,
    current_user: Dict = Depends(get_current_user),
):
    """Reporte de ventas por rango de fechas"""
    return report_ctrl.get_sales_report(start_date, end_date, user_id)


@router.get("/products-sold")
def products_sold_report(
    start_date: str = Query(default=str(date.today() - timedelta(days=30))),
    end_date: str = Query(default=str(date.today())),
    current_user: Dict = Depends(get_current_user),
):
    """Reporte de productos vendidos"""
    return report_ctrl.get_products_sold_report(start_date, end_date)


@router.get("/inventory")
def inventory_report(current_user: Dict = Depends(get_current_user)):
    """Reporte de inventario actual"""
    return report_ctrl.get_inventory_report()


@router.get("/cashier")
def cashier_report(
    start_date: str = Query(default=str(date.today() - timedelta(days=30))),
    end_date: str = Query(default=str(date.today())),
    current_user: Dict = Depends(get_current_user),
):
    """Reporte de ventas por cajero"""
    return report_ctrl.get_cashier_report(start_date, end_date)


@router.get("/daily")
def daily_summary(
    report_date: str = Query(default=str(date.today())),
    current_user: Dict = Depends(get_current_user),
):
    """Resumen diario de ventas"""
    return report_ctrl.get_daily_summary(report_date)
