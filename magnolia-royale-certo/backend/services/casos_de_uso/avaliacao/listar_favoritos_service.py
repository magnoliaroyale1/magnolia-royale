"""Caso de uso ListarFavoritosService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Avaliacao, Agendamento, Clinica, Procedimento, Favorito
from backend.services.base import BaseService, texto, inteiro
from backend.repositories.avaliacao_repository import AvaliacaoRepository



class ListarFavoritosService(BaseService):
    def executar(self):
        user = self.usuario(['client'])
        return [Clinica.buscar(f.clinicId).to_dict() for f in Favorito.listar(userId=user.id) if Clinica.buscar(f.clinicId).status == 'approved']
