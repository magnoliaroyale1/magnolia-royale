from backend.errors import AppError
from backend.models import Avaliacao, Agendamento, Clinica, Procedimento, Favorito
from backend.services.base import BaseService, texto, inteiro
from backend.repositories.avaliacao_repository import AvaliacaoRepository



class RemoverFavoritoService(BaseService):
    def executar(self, clinic_id):
        remove = True
        user = self.usuario(['client'])
        self.clinica(clinic_id)
        # p não duplicar em varios cliques
        from backend.models import Usuario
        Usuario.buscar(user.id, bloquear=True)
        item = Favorito.primeiro(userId=user.id, clinicId=clinic_id)
        if item:
            item.excluir()
        return {'ok': True}
