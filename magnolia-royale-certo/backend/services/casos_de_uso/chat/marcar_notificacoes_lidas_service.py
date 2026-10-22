"""Caso de uso MarcarNotificacoesLidasService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Conversa, Mensagem, Clinica, Usuario, Notificacao
from backend.models.usuario import agora
from backend.services.base import BaseService, texto

from backend.services.auxiliares.chat import ChatHelpers


class MarcarNotificacoesLidasService(ChatHelpers):
    def executar(self, id=None):
        user = self.usuario()
        items = [Notificacao.buscar(id)] if id else Notificacao.listar(userId=user.id, read=False)
        for item in items:
            if item.userId != user.id:
                raise AppError('Notificação de outro usuário.', 403)
            item.atualizar(read=True)
        return {'ok': True}
