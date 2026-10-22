"""Apoio compartilhado para autenticação, autorização e normalização."""
from backend.errors import AppError
from backend.models import Conversa, Mensagem, Clinica, Usuario, Notificacao
from backend.models.usuario import agora
from backend.services.base import BaseService, texto


class ChatHelpers(BaseService):
    def acessar(self, id):
        user = self.usuario()
        chat = Conversa.buscar(id)
        if user.id == chat.clientId:
            return chat, user
        if chat.kind == 'support' and user.role == 'admin':
            return chat, user
        if chat.kind == 'direct' and Clinica.buscar(chat.clinicId).ownerId == user.id:
            return chat, user
        raise AppError('Você não participa desta conversa.', 403)

    def apresentar(self, chat, user):
        data = chat.to_dict()
        data['unreadCount'] = sum(1 for m in Mensagem.listar(chatId=chat.id, read=False) if m.senderId != user.id)
        owner_id = Clinica.buscar(chat.clinicId).ownerId if chat.clinicId else 'admin'
        data['participants'] = [str(chat.clientId), str(owner_id)]
        data['userId'] = str(chat.clientId)
        data['userName'] = chat.clientName
        data['userRole'] = Usuario.buscar(chat.clientId).role
        data['createdAt'] = data['lastMessageAt']
        return data
