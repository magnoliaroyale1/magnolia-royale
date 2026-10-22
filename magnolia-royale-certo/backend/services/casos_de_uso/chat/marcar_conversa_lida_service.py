"""Caso de uso MarcarConversaLidaService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Conversa, Mensagem, Clinica, Usuario, Notificacao
from backend.models.usuario import agora
from backend.services.base import BaseService, texto

from backend.services.auxiliares.chat import ChatHelpers


class MarcarConversaLidaService(ChatHelpers):
    def executar(self, id):
        chat, user = self.acessar(id)
        for message in Mensagem.listar(chatId=chat.id, read=False):
            if message.senderId != user.id:
                message.atualizar(read=True)
        return {'ok': True}
