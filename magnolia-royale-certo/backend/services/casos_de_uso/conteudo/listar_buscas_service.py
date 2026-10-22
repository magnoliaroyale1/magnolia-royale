"""Caso de uso ListarBuscasService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Publicacao, Portfolio, Questionario, Clinica, Profissional, Denuncia, Contato, Busca, Checkout, Usuario
from backend.models.usuario import agora
from backend.services.base import BaseService, texto, email, inteiro



class ListarBuscasService(BaseService):
    def executar(self):
        data = None
        user = self.usuario()
        if data is None:
            return [dict(b.to_dict(), query=b.term) for b in list(reversed(Busca.listar(userId=user.id)))[:20]]
        filters = data.get('filters', {})
        if not isinstance(filters, dict):
            raise AppError('Filtros inválidos.')
        return Busca.criar(userId=user.id, term=texto(data, 'query', 180, False), filters=filters).to_dict()
