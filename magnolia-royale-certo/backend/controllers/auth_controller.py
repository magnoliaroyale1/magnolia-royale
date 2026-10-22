from backend.controllers.base import ApiController, dados
from backend.errors import AppError
from backend.services.casos_de_uso.auth.cadastrar_cliente_service import CadastrarClienteService
from backend.services.casos_de_uso.auth.autenticar_usuario_service import AutenticarUsuarioService
from backend.services.casos_de_uso.auth.consultar_sessao_service import ConsultarSessaoService
from backend.services.casos_de_uso.auth.encerrar_sessao_service import EncerrarSessaoService
from backend.services.casos_de_uso.auth.consultar_perfil_service import ConsultarPerfilService
from backend.services.casos_de_uso.auth.atualizar_perfil_service import AtualizarPerfilService
from backend.services.casos_de_uso.auth.salvar_preferencias_service import SalvarPreferenciasService
from backend.services.casos_de_uso.auth.alterar_senha_service import AlterarSenhaService
from backend.services.casos_de_uso.auth.desativar_conta_service import DesativarContaService
from backend.services.casos_de_uso.auth.consultar_caixa_demo_service import ConsultarCaixaDemoService
from backend.services.casos_de_uso.auth.solicitar_verificacao_email_service import SolicitarVerificacaoEmailService
from backend.services.casos_de_uso.auth.solicitar_redefinicao_senha_service import SolicitarRedefinicaoSenhaService
from backend.services.casos_de_uso.auth.confirmar_email_service import ConfirmarEmailService
from backend.services.casos_de_uso.auth.redefinir_senha_service import RedefinirSenhaService


class AuthController(ApiController):
    def get(self, action):
        actions = {
            'session': ConsultarSessaoService,
            'me': ConsultarPerfilService,
            'mailbox': ConsultarCaixaDemoService,
        }
        service = actions.get(action)
        if not service:
            raise AppError('Rota não encontrada.', 404)
        return service().executar()

    def post(self, action):
        if action == 'logout':
            return EncerrarSessaoService().executar()
        actions = {
            'register': CadastrarClienteService,
            'login': AutenticarUsuarioService,
            'password': AlterarSenhaService,
            'verification-request': SolicitarVerificacaoEmailService,
            'password-request': SolicitarRedefinicaoSenhaService,
            'verify': ConfirmarEmailService,
            'reset': RedefinirSenhaService,
        }
        service = actions.get(action)
        if not service:
            raise AppError('Rota não encontrada.', 404)
        return service().executar(dados())

    def patch(self, action):
        if action != 'me':
            raise AppError('Rota não encontrada.', 404)
        data = dados()
        if set(data) == {'preferences'}:
            return SalvarPreferenciasService().executar(data['preferences'])
        return AtualizarPerfilService().executar(data)

    def delete(self, action):
        if action != 'me':
            raise AppError('Rota não encontrada.', 404)
        return DesativarContaService().executar(dados())
