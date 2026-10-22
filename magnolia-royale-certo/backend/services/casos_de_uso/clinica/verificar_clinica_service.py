"""Caso de uso VerificarClinicaService: uma ação pública, com validações e persistência nas Models/Repositories."""
import re
from datetime import date, datetime, timedelta
from backend.errors import AppError
from backend.models import Clinica, Procedimento, Agenda, Usuario, Profissional, Agendamento, Notificacao
from backend.services.base import BaseService, texto, email, inteiro, dinheiro
from backend.repositories.clinica_repository import ClinicaRepository

from backend.services.auxiliares.clinica import ClinicaHelpers


class VerificarClinicaService(ClinicaHelpers):
    def executar(self, id, data):
        from backend.services.casos_de_uso.avaliacao.recalcular_avaliacao_service import RecalcularAvaliacaoService
        self.usuario(['admin'])
        clinic = Clinica.buscar(id)
        criteria = data.get('criteria', {})
        keys = ('documentacaoValida', 'profissionaisQualificados', 'boasAvaliacoes', 'assessmentCompleto')
        if any(type(criteria.get(k)) is not bool for k in keys):
            raise AppError('Critérios inválidos.')
        clinic.atualizar(verificationCriteria={k: criteria[k] for k in keys}, verified=all(criteria[k] for k in keys))
    
        RecalcularAvaliacaoService().executar(id)
        return clinic.to_dict()
