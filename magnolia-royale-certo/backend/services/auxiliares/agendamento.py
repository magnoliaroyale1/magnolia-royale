"""Apoio compartilhado para autenticação, autorização e normalização."""
from datetime import datetime, date, timezone, timedelta
from backend.errors import AppError
from backend.models import Agendamento, HistoricoAgendamento, Profissional, Clinica, Procedimento, ProfissionalProcedimento, Agenda, Notificacao
from backend.services.base import BaseService, texto, inteiro
from backend.repositories.agendamento_repository import AgendamentoRepository

from backend.services.auxiliares.clinica import ClinicaHelpers


class AgendamentoHelpers(BaseService):
    @staticmethod
    def agora_local():
        return datetime.now(timezone(timedelta(hours=-3))).replace(tzinfo=None)

    def data(self, value):
        try:
            if not isinstance(value, str):
                raise ValueError()
            return date.fromisoformat(value[:10])
        except ValueError:
            raise AppError('Data inválida. Use AAAA-MM-DD.')

    def acessar(self, id):
        user = self.usuario()
        a = Agendamento.buscar(id, bloquear=True)
        clinic = Clinica.buscar(a.clinicId)
        professional = Profissional.buscar(a.professionalId)
        if user.role != 'admin' and user.id not in (a.clientId, clinic.ownerId, professional.uid):
            raise AppError('Este agendamento pertence a outro usuário.', 403)
        return a, user, clinic

    def historico(self, a, user, action, details=None):
        HistoricoAgendamento.criar(appointmentId=a.id, actorId=user.id, action=action, details=details or {})

    def validar_prazo(self, a, clinic, action):
        policy = clinic.cancellationPolicy
        allow = 'allowCancellation' if action == 'cancel' else 'allowRescheduling'
        minimum = 'minHoursBeforeCancel' if action == 'cancel' else 'minHoursBeforeReschedule'
        if not policy.get(allow, False):
            raise AppError('A política da clínica não permite esta alteração.')
        instant = datetime.combine(a.date, datetime.strptime(a.time, '%H:%M').time())
        hours = (instant - self.agora_local()).total_seconds() / 3600
        if hours < policy.get(minimum, 24):
            raise AppError(f"É necessário solicitar com pelo menos {policy.get(minimum, 24)} horas de antecedência.")
