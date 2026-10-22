"""Caso de uso ExcluirPublicacaoService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Publicacao, Portfolio, Questionario, Clinica, Profissional, Denuncia, Contato, Busca, Checkout, Usuario
from backend.models.usuario import agora
from backend.services.base import BaseService, texto, email, inteiro



class ExcluirPublicacaoService(BaseService):
    def executar(self, id):
        post = Publicacao.buscar(id)
        self.clinica(post.clinicId, manage=True)
        post.excluir()
        return {'ok': True}
