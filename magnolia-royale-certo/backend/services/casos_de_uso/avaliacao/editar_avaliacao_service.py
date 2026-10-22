"""Caso de uso EditarAvaliacaoService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Avaliacao, Agendamento, Clinica, Procedimento, Favorito
from backend.services.base import BaseService, texto, inteiro
from backend.repositories.avaliacao_repository import AvaliacaoRepository



class EditarAvaliacaoService(BaseService):
    def executar(self, id, data):
        from backend.services.casos_de_uso.avaliacao.recalcular_avaliacao_service import RecalcularAvaliacaoService
        user = self.usuario(['client'])
        review = Avaliacao.buscar(id)
        if review.clientId != user.id:
            raise AppError('Você só pode editar sua própria avaliação.', 403)
        Clinica.buscar(review.clinicId, bloquear=True)
        changes = {}
        if 'rating' in data:
            changes['rating'] = inteiro(data['rating'], 'Nota', 1, 5)
        if 'comment' in data:
            changes['comment'] = texto(data, 'comment', 5000)
        review.atualizar(**changes)
        RecalcularAvaliacaoService().executar(review.clinicId)
        return review.to_dict()
