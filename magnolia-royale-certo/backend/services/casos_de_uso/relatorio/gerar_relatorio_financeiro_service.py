"""Caso de uso GerarRelatorioFinanceiroService: uma ação pública, com validações e persistência nas Models/Repositories."""
from datetime import date
from backend.errors import AppError
from backend.models import Clinica, Agendamento, Usuario
from backend.repositories.relatorio_repository import RelatorioRepository
from backend.services.base import BaseService



class GerarRelatorioFinanceiroService(BaseService):
    def executar(self, clinic_id, filters):
        self.clinica(clinic_id, manage=True)
        try:
            start = date.fromisoformat(filters.get('start', '2000-01-01'))
            end = date.fromisoformat(filters.get('end', '2100-12-31'))
        except ValueError:
            raise AppError('Período inválido.')
        if end < start:
            raise AppError('A data final deve ser posterior à inicial.')
        return RelatorioRepository().financeiro(clinic_id, start, end)
