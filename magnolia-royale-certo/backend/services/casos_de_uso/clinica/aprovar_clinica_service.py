"""Caso de uso AprovarClinicaService: uma ação pública, com validações e persistência nas Models/Repositories."""
import re
from datetime import date, datetime, timedelta
from backend.errors import AppError
from backend.models import Clinica, Procedimento, Agenda, Usuario, Profissional, Agendamento, Notificacao
from backend.services.base import BaseService, texto, email, inteiro, dinheiro
from backend.repositories.clinica_repository import ClinicaRepository

from backend.services.auxiliares.clinica import ClinicaHelpers


class AprovarClinicaService(ClinicaHelpers):
    def executar(self, id, data):
        self.usuario(['admin'])
        clinic = Clinica.buscar(id)
        status = 'approved'
        if status not in ('approved', 'rejected', 'pending'):
            raise AppError('Status inválido.')
        feedback = texto(data, 'feedback', 2000, status == 'rejected')
        clinic.atualizar(status=status, adminFeedback=feedback)
        Notificacao.criar(userId=clinic.ownerId, type='approval', title='Cadastro da clínica atualizado',
            message={'approved': 'Clínica aprovada.', 'rejected': 'Clínica não aprovada.', 'pending': 'Informações adicionais solicitadas.'}[status] + ' ' + feedback,
            link='/dashboard/clinic')
        return clinic.to_dict()
