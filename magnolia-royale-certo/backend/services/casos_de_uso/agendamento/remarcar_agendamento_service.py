"""Caso de uso RemarcarAgendamentoService: regras de uma ação de agendamento."""
from datetime import datetime, date, timezone, timedelta
from backend.errors import AppError
from backend.models import Agendamento, HistoricoAgendamento, Profissional, Clinica, Procedimento, ProfissionalProcedimento, Agenda, Notificacao
from backend.services.base import BaseService, texto, inteiro
from backend.repositories.agendamento_repository import AgendamentoRepository

from backend.services.auxiliares.agendamento import AgendamentoHelpers


class RemarcarAgendamentoService(AgendamentoHelpers):
    def executar(self, id, data):
        from backend.services.casos_de_uso.agendamento.consultar_disponibilidade_service import ConsultarDisponibilidadeService
        a, user, clinic = self.acessar(id)
        if a.status not in ('pending', 'confirmed'):
            raise AppError('Somente agendamentos em aberto podem ser reagendados.')
        if user.role == 'client':
            self.validar_prazo(a, clinic, 'reschedule')
        Clinica.buscar(clinic.id, bloquear=True)
        Profissional.buscar(a.professionalId, bloquear=True)
        day = self.data(data.get('date'))
        time = texto(data, 'time', 5)
        if time not in ConsultarDisponibilidadeService().executar(clinic.id, a.professionalId, day.isoformat(), a.id):
            raise AppError('Novo horário indisponível.', 409)
        old = {'date': a.date.isoformat(), 'time': a.time}
        a.atualizar(date=day, time=time, status='pending', duration=Agenda.primeiro(clinicId=clinic.id).slotDuration)
        self.historico(a, user, 'rescheduled', {'before': old, 'after': {'date': day.isoformat(), 'time': time}})
        Notificacao.criar(userId=a.clientId if user.role != 'client' else clinic.ownerId, type='appointment_reminder', title='Agendamento atualizado', message=f'{a.procedure}: {a.status}.', link='/dashboard/client' if user.role != 'client' else '/dashboard/clinic')
        return a.to_dict()
