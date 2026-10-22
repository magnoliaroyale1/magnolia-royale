"""Caso de uso ListarMinhasAvaliacoesService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Avaliacao, Agendamento, Clinica, Procedimento, Favorito
from backend.services.base import BaseService, texto, inteiro
from backend.repositories.avaliacao_repository import AvaliacaoRepository



class ListarMinhasAvaliacoesService(BaseService):
    def executar(self):
        user = self.usuario(['client'])
        return [dict(a.to_dict(), clinicName=name) for a, name in AvaliacaoRepository().por_cliente(user.id)]
