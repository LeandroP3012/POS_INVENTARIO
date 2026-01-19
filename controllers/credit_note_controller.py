"""Controlador para notas de crédito"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from models.credit_note_model import CreditNoteModel
from models.report_model import ReportModel


class CreditNoteController:
    """Expone operaciones de notas de crédito para la capa de UI"""

    def __init__(self):
        self.model = CreditNoteModel()
        self.report_model = ReportModel()

    def list_credit_notes(self, limit: int = 200) -> Dict[str, Any]:
        try:
            notes = self.model.list_credit_notes(limit)
            return {'success': True, 'notes': notes}
        except Exception as exc:
            return {'success': False, 'message': str(exc)}

    def create_credit_note(self, sale_id: int, user_id: int, reason: str = "", items: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        try:
            return self.model.create_credit_note(sale_id, user_id, reason, items)
        except Exception as exc:
            return {'success': False, 'message': str(exc)}

    def report(self, days_back: int = 30, user_id: Optional[int] = None) -> Dict[str, Any]:
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            return self.report_model.get_credit_notes_report(start_date, end_date, user_id)
        except Exception as exc:
            return {'success': False, 'message': str(exc)}
