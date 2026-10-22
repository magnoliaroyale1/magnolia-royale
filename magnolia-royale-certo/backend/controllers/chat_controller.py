from backend.controllers.base import ApiController, dados
from backend.services.casos_de_uso.chat.listar_conversas_service import ListarConversasService
from backend.services.casos_de_uso.chat.criar_conversa_service import CriarConversaService
from backend.services.casos_de_uso.chat.listar_mensagens_service import ListarMensagensService
from backend.services.casos_de_uso.chat.enviar_mensagem_service import EnviarMensagemService
from backend.services.casos_de_uso.chat.marcar_conversa_lida_service import MarcarConversaLidaService
from backend.services.casos_de_uso.chat.listar_notificacoes_service import ListarNotificacoesService
from backend.services.casos_de_uso.chat.marcar_notificacoes_lidas_service import MarcarNotificacoesLidasService


class ChatController(ApiController):
    def get(self, kind='direct'):
        return ListarConversasService().executar(kind)

    def post(self, kind='direct'):
        return CriarConversaService().executar(dados(), kind)


class MensagemController(ApiController):
    def get(self, id):
        return ListarMensagensService().executar(id)

    def post(self, id):
        return EnviarMensagemService().executar(id, dados())

    def patch(self, id):
        return MarcarConversaLidaService().executar(id)


class NotificacaoController(ApiController):
    def get(self):
        return ListarNotificacoesService().executar()

    def patch(self, id=None):
        return MarcarNotificacoesLidasService().executar(id)
