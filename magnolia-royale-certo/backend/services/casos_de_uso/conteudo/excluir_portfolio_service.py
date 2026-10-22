"""Caso de uso ExcluirPortfolioService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Publicacao, Portfolio, Questionario, Clinica, Profissional, Denuncia, Contato, Busca, Checkout, Usuario
from backend.models.usuario import agora
from backend.services.base import BaseService, texto, email, inteiro



class ExcluirPortfolioService(BaseService):
    def executar(self, id):
        item = Portfolio.buscar(id)
        self.profissional(item.professionalId, manage=True)
        item.excluir()
        return {'ok': True}
