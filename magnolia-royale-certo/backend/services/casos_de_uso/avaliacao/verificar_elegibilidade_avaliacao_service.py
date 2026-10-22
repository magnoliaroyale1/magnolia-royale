"""Caso de uso VerificarElegibilidadeAvaliacaoService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Avaliacao, Agendamento, Clinica, Procedimento, Favorito
from backend.services.base import BaseService, texto, inteiro
from backend.repositories.avaliacao_repository import AvaliacaoRepository



class VerificarElegibilidadeAvaliacaoService(BaseService):
    def executar(self, clinic_id, professional_id=None):
        user = self.usuario(['client'])
        if Avaliacao.primeiro(clinicId=clinic_id, clientId=user.id):
            return {'canReview': False, 'reason': 'Você já avaliou esta clínica.'}
        completed = Agendamento.listar(clinicId=clinic_id, clientId=user.id, status='completed')
        if professional_id:
            completed = [a for a in completed if a.professionalId == professional_id]
        return {'canReview': bool(completed), 'reason': '' if completed else 'Realize um atendimento nesta clínica com o profissional selecionado antes de avaliar.'}
