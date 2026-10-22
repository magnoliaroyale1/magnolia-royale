"""Caso de uso ListarConversasService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Conversa, Mensagem, Clinica, Usuario, Notificacao
from backend.models.usuario import agora
from backend.services.base import BaseService, texto

from backend.services.auxiliares.chat import ChatHelpers


class ListarConversasService(ChatHelpers):
    def executar(self, kind):
        user = self.usuario()
        result = []
        for chat in Conversa.listar(kind=kind):
            own = chat.clientId == user.id or (kind == 'support' and user.role == 'admin') or (chat.clinicId and Clinica.buscar(chat.clinicId).ownerId == user.id)
            if own:
                result.append(self.apresentar(chat, user))
        return sorted(result, key=lambda c: c['lastMessageAt'], reverse=True)
