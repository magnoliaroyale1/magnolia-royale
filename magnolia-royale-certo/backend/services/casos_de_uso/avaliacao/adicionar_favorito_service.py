"""Caso de uso AdicionarFavoritoService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Avaliacao, Agendamento, Clinica, Procedimento, Favorito
from backend.services.base import BaseService, texto, inteiro
from backend.repositories.avaliacao_repository import AvaliacaoRepository



class AdicionarFavoritoService(BaseService):
    def executar(self, clinic_id):
        remove = False
        user = self.usuario(['client'])
        self.clinica(clinic_id)
        # Bloqueio do usuário evita duplicidade em cliques simultâneos.
        from backend.models import Usuario
        Usuario.buscar(user.id, bloquear=True)
        item = Favorito.primeiro(userId=user.id, clinicId=clinic_id)
        if not item:
            Favorito.criar(userId=user.id, clinicId=clinic_id)
        return {'ok': True}
