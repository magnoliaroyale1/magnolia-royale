"""Caso de uso EnviarContatoService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Publicacao, Portfolio, Questionario, Clinica, Profissional, Denuncia, Contato, Busca, Checkout, Usuario
from backend.models.usuario import agora
from backend.services.base import BaseService, texto, email, inteiro



class EnviarContatoService(BaseService):
    def executar(self, data):
        return Contato.criar(name=texto(data, 'name', 120), email=email(data), subject=texto(data, 'subject', 180, False) or 'Contato', message=texto(data, 'message', 5000)).to_dict()
