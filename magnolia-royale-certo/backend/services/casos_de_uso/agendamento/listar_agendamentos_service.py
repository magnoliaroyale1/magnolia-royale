"""Caso de uso ListarAgendamentosService: regras de uma ação de agendamento."""
from datetime import datetime, date, timezone, timedelta
from backend.errors import AppError
from backend.models import Agendamento, HistoricoAgendamento, Profissional, Clinica, Procedimento, ProfissionalProcedimento, Agenda, Notificacao
from backend.services.base import BaseService, texto, inteiro
from backend.repositories.agendamento_repository import AgendamentoRepository

from backend.services.auxiliares.agendamento import AgendamentoHelpers


class ListarAgendamentosService(AgendamentoHelpers):
    def executar(self, filters):
        user = self.usuario()
        return [a.to_dict() for a in AgendamentoRepository().visiveis(user, filters)]
