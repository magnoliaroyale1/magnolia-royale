"""Caso de uso ListarAvaliacoesService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Avaliacao, Agendamento, Clinica, Procedimento, Favorito
from backend.services.base import BaseService, texto, inteiro
from backend.repositories.avaliacao_repository import AvaliacaoRepository



class ListarAvaliacoesService(BaseService):
    def executar(self, clinic_id):
        self.clinica(clinic_id)
        return [a.to_dict() for a in reversed(Avaliacao.listar(clinicId=clinic_id))]
