"""Caso de uso AtualizarDenunciaService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Publicacao, Portfolio, Questionario, Clinica, Profissional, Denuncia, Contato, Busca, Checkout, Usuario
from backend.models.usuario import agora
from backend.services.base import BaseService, texto, email, inteiro



class AtualizarDenunciaService(BaseService):
    def executar(self, kind, id, data):
        self.usuario(['admin'])
        if kind == 'contacts':
            return [c.to_dict() for c in reversed(Contato.listar())]
        if data is not None:
            status = data.get('status')
            if status not in ('open', 'investigating', 'resolved'):
                raise AppError('Status inválido.')
            return Denuncia.buscar(id).atualizar(status=status).to_dict()
        return [dict(d.to_dict(), clinicName=Clinica.buscar(d.clinicId).name) for d in reversed(Denuncia.listar())]
