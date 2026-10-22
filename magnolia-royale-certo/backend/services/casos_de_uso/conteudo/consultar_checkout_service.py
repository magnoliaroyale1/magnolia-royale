"""Caso de uso ConsultarCheckoutService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Publicacao, Portfolio, Questionario, Clinica, Profissional, Denuncia, Contato, Busca, Checkout, Usuario
from backend.models.usuario import agora
from backend.services.base import BaseService, texto, email, inteiro



class ConsultarCheckoutService(BaseService):
    def executar(self, id):
        item = Checkout.buscar(id)
        self.clinica(item.clinicId, manage=True)
        return item.to_dict()
