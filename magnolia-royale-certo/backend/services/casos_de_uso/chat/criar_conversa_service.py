"""Caso de uso CriarConversaService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Conversa, Mensagem, Clinica, Usuario, Notificacao
from backend.models.usuario import agora
from backend.services.base import BaseService, texto

from backend.services.auxiliares.chat import ChatHelpers


class CriarConversaService(ChatHelpers):
    def executar(self, data, kind='direct'):
        user = self.usuario()
        if kind == 'direct':
            if user.role != 'client':
                raise AppError('A conversa com a clínica é iniciada pelo cliente.', 403)
            clinic = self.clinica(data.get('clinicId'))
        else:
            clinic = None
        Usuario.buscar(user.id, bloquear=True)
        existing = Conversa.primeiro(clientId=user.id, clinicId=clinic.id if clinic else None, kind=kind)
        chat = existing or Conversa.criar(clientId=user.id, clinicId=clinic.id if clinic else None, kind=kind,
            clientName=user.displayName, clinicName=clinic.name if clinic else 'Suporte Magnolia')
        return self.apresentar(chat, user)
