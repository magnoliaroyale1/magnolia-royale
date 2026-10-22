"""Caso de uso ConsultarEstatisticasPublicasService: uma ação pública, com validações e persistência nas Models/Repositories."""
from datetime import date
from backend.errors import AppError
from backend.models import Clinica, Agendamento, Usuario
from backend.repositories.relatorio_repository import RelatorioRepository
from backend.services.base import BaseService



class ConsultarEstatisticasPublicasService(BaseService):
    def executar(self):
        return RelatorioRepository().publico()
