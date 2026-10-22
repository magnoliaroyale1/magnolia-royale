"""Caso de uso CancelarAgendamentoService: regras de uma ação de agendamento."""
from datetime import datetime, date, timezone, timedelta
from backend.errors import AppError
from backend.models import Agendamento, HistoricoAgendamento, Profissional, Clinica, Procedimento, ProfissionalProcedimento, Agenda, Notificacao
from backend.services.base import BaseService, texto, inteiro
from backend.repositories.agendamento_repository import AgendamentoRepository

from backend.services.auxiliares.agendamento import AgendamentoHelpers


class CancelarAgendamentoService(AgendamentoHelpers):
    def executar(self, id, data):
        a, user, clinic = self.acessar(id)
        if a.status not in ('pending', 'confirmed'):
            raise AppError('Este agendamento já foi encerrado.')
        if user.role == 'client':
            self.validar_prazo(a, clinic, 'cancel')
        fee = clinic.cancellationPolicy.get('cancellationFee', 0) if user.role == 'client' and clinic.cancellationPolicy.get('chargeCancellationFee') else 0
        a.atualizar(status='cancelled_by_client' if user.role == 'client' else 'cancelled', cancelReason=texto(data, 'reason', 2000, False), cancellationFee=fee)
        self.historico(a, user, 'cancelled', {'fee': float(fee), 'reason': a.cancelReason})
        Notificacao.criar(userId=a.clientId if user.role != 'client' else clinic.ownerId, type='appointment_reminder', title='Agendamento atualizado', message=f'{a.procedure}: {a.status}.', link='/dashboard/client' if user.role != 'client' else '/dashboard/clinic')
        return a.to_dict()
