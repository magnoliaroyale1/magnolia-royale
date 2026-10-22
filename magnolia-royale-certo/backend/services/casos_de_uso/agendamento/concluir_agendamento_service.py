"""Caso de uso ConcluirAgendamentoService: regras de uma ação de agendamento."""
from datetime import datetime, date, timezone, timedelta
from backend.errors import AppError
from backend.models import Agendamento, HistoricoAgendamento, Profissional, Clinica, Procedimento, ProfissionalProcedimento, Agenda, Notificacao
from backend.services.base import BaseService, texto, inteiro
from backend.repositories.agendamento_repository import AgendamentoRepository

from backend.services.auxiliares.agendamento import AgendamentoHelpers


class ConcluirAgendamentoService(AgendamentoHelpers):
    def executar(self, id, data):
        a, user, clinic = self.acessar(id)
        if user.role == 'client':
            raise AppError('Somente a equipe pode confirmar ou concluir atendimentos.', 403)
        status = 'completed'
        allowed = {'pending': ['confirmed'], 'confirmed': ['completed']}
        if status not in allowed.get(a.status, []):
            raise AppError('Transição de status inválida.')
        a.atualizar(status=status)
        self.historico(a, user, status)
        Notificacao.criar(userId=a.clientId if user.role != 'client' else clinic.ownerId, type='appointment_reminder', title='Agendamento atualizado', message=f'{a.procedure}: {a.status}.', link='/dashboard/client' if user.role != 'client' else '/dashboard/clinic')
        return a.to_dict()
