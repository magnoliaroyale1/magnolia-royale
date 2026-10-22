"""Apoio compartilhado para autenticação, autorização e normalização."""
import re
from datetime import date, datetime, timedelta
from backend.errors import AppError
from backend.models import Clinica, Procedimento, Agenda, Usuario, Profissional, Agendamento, Notificacao
from backend.services.base import BaseService, texto, email, inteiro, dinheiro
from backend.repositories.clinica_repository import ClinicaRepository


class ClinicaHelpers(BaseService):
    @staticmethod
    def minutos(value):
        if not isinstance(value, str) or not re.fullmatch(r'\d{2}:\d{2}', value):
            raise AppError('Horário inválido.')
        h, m = map(int, value.split(':'))
        if h > 23 or m > 59:
            raise AppError('Horário inválido.')
        return h * 60 + m
