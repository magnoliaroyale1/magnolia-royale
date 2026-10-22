from flask import request, current_app, send_from_directory
from backend.controllers.base import ApiController, dados
from backend.services.casos_de_uso.conteudo.listar_publicacoes_service import ListarPublicacoesService
from backend.services.casos_de_uso.conteudo.criar_publicacao_service import CriarPublicacaoService
from backend.services.casos_de_uso.conteudo.atualizar_publicacao_service import AtualizarPublicacaoService
from backend.services.casos_de_uso.conteudo.excluir_publicacao_service import ExcluirPublicacaoService
from backend.services.casos_de_uso.conteudo.listar_portfolio_service import ListarPortfolioService
from backend.services.casos_de_uso.conteudo.adicionar_portfolio_service import AdicionarPortfolioService
from backend.services.casos_de_uso.conteudo.excluir_portfolio_service import ExcluirPortfolioService
from backend.services.casos_de_uso.conteudo.consultar_questionario_service import ConsultarQuestionarioService
from backend.services.casos_de_uso.conteudo.salvar_questionario_service import SalvarQuestionarioService
from backend.services.casos_de_uso.conteudo.enviar_contato_service import EnviarContatoService
from backend.services.casos_de_uso.conteudo.criar_denuncia_service import CriarDenunciaService
from backend.services.casos_de_uso.conteudo.listar_buscas_service import ListarBuscasService
from backend.services.casos_de_uso.conteudo.registrar_busca_service import RegistrarBuscaService
from backend.services.casos_de_uso.conteudo.criar_checkout_service import CriarCheckoutService
from backend.services.casos_de_uso.conteudo.confirmar_checkout_service import ConfirmarCheckoutService
from backend.services.casos_de_uso.conteudo.consultar_checkout_service import ConsultarCheckoutService
from backend.services.casos_de_uso.conteudo.listar_atendimentos_admin_service import ListarAtendimentosAdminService
from backend.services.casos_de_uso.conteudo.atualizar_denuncia_service import AtualizarDenunciaService
from backend.services.casos_de_uso.arquivo.enviar_arquivo_service import EnviarArquivoService
from backend.services.casos_de_uso.arquivo.consultar_arquivo_service import ConsultarArquivoService


class BlogController(ApiController):
    def get(self):
        return ListarPublicacoesService().executar(request.args.get('clinicId', type=int))

    def post(self):
        return CriarPublicacaoService().executar(dados())

    def patch(self, id):
        return AtualizarPublicacaoService().executar(dados(), id)

    def delete(self, id):
        return ExcluirPublicacaoService().executar(id)


class PortfolioController(ApiController):
    def get(self, id):
        return ListarPortfolioService().executar(id)

    def post(self, id):
        return AdicionarPortfolioService().executar(id, dados())

    def delete(self, item_id):
        return ExcluirPortfolioService().executar(item_id)


class QuestionarioController(ApiController):
    def get(self, id):
        return ConsultarQuestionarioService().executar(id)

    def put(self, id):
        return SalvarQuestionarioService().executar(id, dados())


class ContatoController(ApiController):
    def post(self):
        return EnviarContatoService().executar(dados())


class DenunciaController(ApiController):
    def post(self):
        return CriarDenunciaService().executar(dados())


class BuscaController(ApiController):
    def get(self):
        return ListarBuscasService().executar()

    def post(self):
        return RegistrarBuscaService().executar(dados())


class CheckoutController(ApiController):
    def get(self, id):
        return ConsultarCheckoutService().executar(id)

    def post(self, clinic_id):
        return CriarCheckoutService().executar(clinic_id, dados())

    def patch(self, clinic_id, id):
        return ConfirmarCheckoutService().executar(clinic_id, dados(), id)


class ArquivoController(ApiController):
    def post(self):
        return EnviarArquivoService().executar(request.files.get('file'), request.form.get('context', 'image'))

    def get(self, name):
        filename, mime = ConsultarArquivoService().executar(name)
        return send_from_directory(current_app.config['UPLOAD_DIR'], filename, mimetype=mime)


class AtendimentoAdminController(ApiController):
    def get(self, kind):
        return ListarAtendimentosAdminService().executar(kind)

    def patch(self, kind, id):
        return AtualizarDenunciaService().executar(kind, id, dados())
