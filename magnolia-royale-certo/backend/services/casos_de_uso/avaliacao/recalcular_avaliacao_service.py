"""Caso de uso RecalcularAvaliacaoService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Avaliacao, Agendamento, Clinica, Procedimento, Favorito
from backend.services.base import BaseService, texto, inteiro
from backend.repositories.avaliacao_repository import AvaliacaoRepository



class RecalcularAvaliacaoService(BaseService):
    def executar(self, clinic_id):
        clinic = Clinica.buscar(clinic_id, bloquear=True)
        rating, count = AvaliacaoRepository().resumo(clinic_id)
        score = rating*10 + min(count*0.1, 20) + {'basic': 5, 'professional': 10, 'premium': 15}[clinic.plan]
        score += 10 if clinic.verified else 0
        score += 5 if clinic.description else 0
        score += 5 if clinic.images else 0
        score += 5 if Procedimento.listar(clinicId=clinic.id, active=True) else 0
        score += 3 if clinic.city else 0
        score += 2 if clinic.phone else 0
        clinic.atualizar(rating=rating, reviewCount=count, score=min(100, round(score)))
