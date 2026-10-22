"""Caso de uso ConsultarRankingService: uma ação pública, com validações e persistência nas Models/Repositories."""
from datetime import date
from backend.errors import AppError
from backend.models import Clinica, Agendamento, Usuario
from backend.repositories.relatorio_repository import RelatorioRepository
from backend.services.base import BaseService



class ConsultarRankingService(BaseService):
    def executar(self):
        return [Clinica.buscar(row['id']).to_dict() for row in RelatorioRepository().ranking()]
