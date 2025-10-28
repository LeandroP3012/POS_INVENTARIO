"""
Controlador de Reportes
Autor: Sistema POS
Fecha: 2025-10-27
"""

from models.report_model import ReportModel
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class ReportController:
    """Controlador para gestión de reportes"""
    
    def __init__(self):
        self.report_model = ReportModel()
    
    def get_sales_report(self, start_date: str, end_date: str, 
                        user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Obtener reporte de ventas
        
        Args:
            start_date: Fecha inicio (formato: YYYY-MM-DD)
            end_date: Fecha fin (formato: YYYY-MM-DD)
            user_id: ID del cajero (opcional)
        """
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            end = end.replace(hour=23, minute=59, second=59)
            
            return self.report_model.get_sales_report(start, end, user_id)
            
        except ValueError as e:
            return {'success': False, 'message': f'Formato de fecha inválido: {str(e)}'}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def get_products_sold_report(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Reporte de productos vendidos"""
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            end = end.replace(hour=23, minute=59, second=59)
            
            return self.report_model.get_products_sold_report(start, end)
            
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def get_inventory_report(self) -> Dict[str, Any]:
        """Reporte de inventario"""
        return self.report_model.get_inventory_report()
    
    def get_cashier_report(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Reporte por cajero"""
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            end = end.replace(hour=23, minute=59, second=59)
            
            return self.report_model.get_cashier_report(start, end)
            
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def get_daily_summary(self, date: str) -> Dict[str, Any]:
        """Resumen del día"""
        try:
            report_date = datetime.strptime(date, '%Y-%m-%d')
            return self.report_model.get_daily_summary(report_date)
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def get_period_comparison(self, period1_start: str, period1_end: str,
                             period2_start: str, period2_end: str) -> Dict[str, Any]:
        """Comparar dos períodos"""
        try:
            report1 = self.get_sales_report(period1_start, period1_end)
            report2 = self.get_sales_report(period2_start, period2_end)
            
            if not report1['success'] or not report2['success']:
                return {'success': False, 'message': 'Error al obtener datos'}
            
            summary1 = report1['data']['summary']
            summary2 = report2['data']['summary']
            
            # Calcular diferencias
            diff_sales = summary1['total_sales'] - summary2['total_sales']
            diff_amount = summary1['total_amount'] - summary2['total_amount']
            diff_avg = summary1['average_ticket'] - summary2['average_ticket']
            
            # Calcular porcentajes
            pct_sales = (diff_sales / summary2['total_sales'] * 100) if summary2['total_sales'] > 0 else 0
            pct_amount = (diff_amount / summary2['total_amount'] * 100) if summary2['total_amount'] > 0 else 0
            pct_avg = (diff_avg / summary2['average_ticket'] * 100) if summary2['average_ticket'] > 0 else 0
            
            return {
                'success': True,
                'data': {
                    'period1': {
                        'dates': report1['data']['period'],
                        'summary': summary1
                    },
                    'period2': {
                        'dates': report2['data']['period'],
                        'summary': summary2
                    },
                    'comparison': {
                        'sales_diff': diff_sales,
                        'sales_pct': round(pct_sales, 2),
                        'amount_diff': round(diff_amount, 2),
                        'amount_pct': round(pct_amount, 2),
                        'avg_diff': round(diff_avg, 2),
                        'avg_pct': round(pct_avg, 2)
                    }
                }
            }
            
        except Exception as e:
            return {'success': False, 'message': str(e)}
