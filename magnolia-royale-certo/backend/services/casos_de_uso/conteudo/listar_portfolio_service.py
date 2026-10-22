"""Caso de uso ListarPortfolioService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Publicacao, Portfolio, Questionario, Clinica, Profissional, Denuncia, Contato, Busca, Checkout, Usuario
from backend.models.usuario import agora
from backend.services.base import BaseService, texto, email, inteiro



class ListarPortfolioService(BaseService):
    def executar(self, id):
        data = None
        professional = self.profissional(id, manage=data is not None)
        if data is None:
            self.clinica(professional.clinicId)
            return [i.to_dict() for i in reversed(Portfolio.listar(professionalId=id))]
        url = texto(data, 'imageUrl', 500)
        if not url.startswith('/api/files/'):
            raise AppError('Envie a imagem antes de salvar.')
        return Portfolio.criar(professionalId=id, imageUrl=url, procedure=texto(data, 'procedure', 120), description=texto(data, 'description', 3000, False)).to_dict()
