"""Caso de uso ListarNotificacoesService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Conversa, Mensagem, Clinica, Usuario, Notificacao
from backend.models.usuario import agora
from backend.services.base import BaseService, texto

from backend.services.auxiliares.chat import ChatHelpers


class ListarNotificacoesService(ChatHelpers):
    def executar(self):
        user = self.usuario()
        return [n.to_dict() for n in list(reversed(Notificacao.listar(userId=user.id)))[:50]]
