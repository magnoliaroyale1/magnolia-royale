"""Caso de uso AtualizarAgendaService: uma ação pública, com validações e persistência nas Models/Repositories."""
import re
from datetime import date, datetime, timedelta
from backend.errors import AppError
from backend.models import Clinica, Procedimento, Agenda, Usuario, Profissional, Agendamento, Notificacao
from backend.services.base import BaseService, texto, email, inteiro, dinheiro
from backend.repositories.clinica_repository import ClinicaRepository

from backend.services.auxiliares.agendamento import AgendamentoHelpers
from backend.services.auxiliares.clinica import ClinicaHelpers


class AtualizarAgendaService(ClinicaHelpers):
    def executar(self, id, data):
        clinic = self.clinica(id, manage=data is not None)
        if data is not None:
            Clinica.buscar(clinic.id, bloquear=True)
        agenda = Agenda.primeiro(clinicId=clinic.id)
        if data is not None:
            days = data.get('daysOfWeek')
            if not isinstance(days, list) or not days:
                raise AppError('Selecione os dias de atendimento.')
            days = sorted(set(inteiro(d, 'Dia da semana', 0, 6) for d in days))
            start = self.minutos(data.get('startTime'))
            end = self.minutos(data.get('endTime'))
            duration = inteiro(data.get('slotDuration'), 'Duração', 15, 480)
            if end <= start or duration > end - start:
                raise AppError('Horários de funcionamento inválidos.')
            blocked = data.get('blockedDates', [])
            if not isinstance(blocked, list):
                raise AppError('Datas bloqueadas inválidas.')
            try:
                blocked = sorted(set(date.fromisoformat(d).isoformat() for d in blocked))
            except (ValueError, TypeError):
                raise AppError('Data bloqueada inválida.')
            # Alterar a agenda não pode invalidar reservas já confirmadas/pendentes.
        
            today = AgendamentoHelpers.agora_local().date()
            for a in Agendamento.listar(clinicId=clinic.id):
                minute = self.minutos(a.time)
                if a.status in ('pending', 'confirmed') and a.date >= today and ((a.date.weekday()+1)%7 not in days or a.date.isoformat() in blocked or minute < start or minute+a.duration > end):
                    raise AppError('A alteração conflita com agendamentos existentes. Reagende-os antes.', 409)
            agenda.atualizar(daysOfWeek=days, startTime=data['startTime'], endTime=data['endTime'], slotDuration=duration, blockedDates=blocked)
        return agenda.to_dict()
