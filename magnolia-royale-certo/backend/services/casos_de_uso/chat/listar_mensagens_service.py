"""Caso de uso ListarMensagensService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Conversa, Mensagem, Clinica, Usuario, Notificacao
from backend.models.usuario import agora
from backend.services.base import BaseService, texto

from backend.services.auxiliares.chat import ChatHelpers


class ListarMensagensService(ChatHelpers):
    def executar(self, id):
        data = None
        chat, user = self.acessar(id)
        if data is None:
            return [m.to_dict() for m in Mensagem.listar(chatId=chat.id)]
        content = texto(data, 'text', 5000)
        message = Mensagem.criar(chatId=chat.id, senderId=user.id, senderName=user.displayName, text=content)
        chat.atualizar(lastMessage=content, lastMessageAt=agora())
        recipients = [Usuario.buscar(chat.clientId)] if user.id != chat.clientId else (Usuario.listar(role='admin', active=True) if chat.kind == 'support' else [Usuario.buscar(Clinica.buscar(chat.clinicId).ownerId)])
        for recipient in recipients:
            Notificacao.criar(userId=recipient.id, type='message', title='Nova mensagem', message=content[:200],
                link='/dashboard/admin/chat' if chat.kind == 'support' and recipient.role == 'admin' else '/support-chat' if chat.kind == 'support' else '/chat')
        return message.to_dict()
