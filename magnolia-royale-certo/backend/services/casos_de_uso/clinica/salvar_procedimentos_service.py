"""Caso de uso SalvarProcedimentosService: uma ação pública, com validações e persistência nas Models/Repositories."""
import re
from datetime import date, datetime, timedelta
from backend.errors import AppError
from backend.models import Clinica, Procedimento, Agenda, Usuario, Profissional, Agendamento, Notificacao
from backend.services.base import BaseService, texto, email, inteiro, dinheiro
from backend.repositories.clinica_repository import ClinicaRepository

from backend.services.auxiliares.clinica import ClinicaHelpers


class SalvarProcedimentosService(ClinicaHelpers):
    def executar(self, clinic, values):
        if not isinstance(values, list) or len(values) > 50:
            raise AppError('Informe uma lista de até 50 procedimentos.')
        names = []
        for value in values:
            item = {'name': value} if isinstance(value, str) else value
            if not isinstance(item, dict):
                raise AppError('Procedimento inválido.')
            name = texto(item, 'name', 120)
            if name in names:
                raise AppError('Há procedimentos repetidos.')
            names.append(name)
            existing = Procedimento.primeiro(clinicId=clinic.id, name=name)
            price = dinheiro(item.get('price', existing.price if existing else 0))
            if existing:
                existing.atualizar(price=price, active=True)
            else:
                Procedimento.criar(clinicId=clinic.id, name=name, price=price)
        for service in Procedimento.listar(clinicId=clinic.id):
            if service.name not in names:
                service.atualizar(active=False)
