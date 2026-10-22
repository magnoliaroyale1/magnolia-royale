"""Caso de uso PesquisarClinicasService: uma ação pública, com validações e persistência nas Models/Repositories."""
import re
from datetime import date, datetime, timedelta
from backend.errors import AppError
from backend.models import Clinica, Procedimento, Agenda, Usuario, Profissional, Agendamento, Notificacao
from backend.services.base import BaseService, texto, email, inteiro, dinheiro
from backend.repositories.clinica_repository import ClinicaRepository

from backend.services.auxiliares.clinica import ClinicaHelpers


class PesquisarClinicasService(ClinicaHelpers):
    def executar(self, filters):
        user = self.usuario(required=False, verified=False)
        public = not (user and user.role == 'admin')
        filters = dict(filters)
        for key in ('minPrice', 'maxPrice', 'minRating'):
            if filters.get(key):
                filters[key] = dinheiro(filters[key])
        return [c.to_dict() for c in ClinicaRepository().pesquisar(filters, public)]
