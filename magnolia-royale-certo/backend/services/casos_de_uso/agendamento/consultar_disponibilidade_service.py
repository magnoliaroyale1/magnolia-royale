"""Caso de uso ConsultarDisponibilidadeService: regras de uma ação de agendamento."""
from datetime import datetime, date, timezone, timedelta
from backend.errors import AppError
from backend.models import Agendamento, HistoricoAgendamento, Profissional, Clinica, Procedimento, ProfissionalProcedimento, Agenda, Notificacao
from backend.services.base import BaseService, texto, inteiro
from backend.repositories.agendamento_repository import AgendamentoRepository

from backend.services.auxiliares.clinica import ClinicaHelpers
from backend.services.auxiliares.agendamento import AgendamentoHelpers


class ConsultarDisponibilidadeService(AgendamentoHelpers):
    def executar(self, clinic_id, professional_id, day, excluding=None):
        clinic = self.clinica(clinic_id)
        professional = self.profissional(professional_id)
        if not professional.active or professional.clinicId != clinic.id or clinic.status != 'approved':
            raise AppError('Profissional indisponível nesta clínica.')
        selected = self.data(day)
        agenda = Agenda.primeiro(clinicId=clinic.id)
        if (selected.weekday()+1)%7 not in agenda.daysOfWeek or selected.isoformat() in agenda.blockedDates:
            return []
        occupied = AgendamentoRepository().ocupados(professional.id, selected, excluding)
        start = ClinicaHelpers.minutos(agenda.startTime)
        end = ClinicaHelpers.minutos(agenda.endTime)
        slots = []
        while start + agenda.slotDuration <= end:
            hour = f'{start//60:02d}:{start%60:02d}'
            instant = datetime.combine(selected, datetime.strptime(hour, '%H:%M').time())
            conflict = any(start < ClinicaHelpers.minutos(a.time)+a.duration and start+agenda.slotDuration > ClinicaHelpers.minutos(a.time) for a in occupied)
            if not conflict and instant > self.agora_local():
                slots.append(hour)
            start += agenda.slotDuration
        return slots
