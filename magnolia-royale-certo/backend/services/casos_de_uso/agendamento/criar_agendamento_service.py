"""Caso de uso CriarAgendamentoService: regras de uma ação de agendamento."""
from datetime import datetime, date, timezone, timedelta
from backend.errors import AppError
from backend.models import Agendamento, HistoricoAgendamento, Profissional, Clinica, Procedimento, ProfissionalProcedimento, Agenda, Notificacao
from backend.services.base import BaseService, texto, inteiro
from backend.repositories.agendamento_repository import AgendamentoRepository

from backend.services.auxiliares.agendamento import AgendamentoHelpers


class CriarAgendamentoService(AgendamentoHelpers):
    def executar(self, data):
        from backend.services.casos_de_uso.agendamento.consultar_disponibilidade_service import ConsultarDisponibilidadeService
        user = self.usuario(['client'])
        clinic_id = inteiro(data.get('clinicId'))
        # Bloqueio da clínica serializa alterações da agenda e reservas.
        clinic = Clinica.buscar(clinic_id, bloquear=True)
        professional = Profissional.buscar(inteiro(data.get('professionalId')), bloquear=True)
        if professional.clinicId != clinic.id or not professional.active:
            raise AppError('Profissional inválido para esta clínica.')
        procedure = Procedimento.primeiro(clinicId=clinic.id, name=texto(data, 'procedure', 120), active=True)
        if not procedure or not ProfissionalProcedimento.primeiro(professionalId=professional.id, procedureId=procedure.id):
            raise AppError('O profissional não atende esse procedimento.')
        day = self.data(data.get('date'))
        time = texto(data, 'time', 5)
        if time not in ConsultarDisponibilidadeService().executar(clinic.id, professional.id, day.isoformat()):
            raise AppError('Horário indisponível. Escolha outro horário.', 409)
        agenda = Agenda.primeiro(clinicId=clinic.id)
        appt = Agendamento.criar(clinicId=clinic.id, professionalId=professional.id, clientId=user.id,
            procedureId=procedure.id, clientName=user.displayName, professionalName=professional.name,
            procedure=procedure.name, date=day, time=time, duration=agenda.slotDuration,
            valor=procedure.price, notes=texto(data, 'notes', 2000, False))
        self.historico(appt, user, 'created')
        Notificacao.criar(userId=clinic.ownerId, type='appointment_reminder', title='Novo agendamento',
            message=f'{user.displayName}: {procedure.name} em {day.isoformat()} às {time}.', link='/dashboard/clinic')
        return appt.to_dict()
