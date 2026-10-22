from backend.controllers.auth_controller import AuthController
from backend.controllers.clinica_controller import ClinicaController, AprovacaoController, VerificacaoController, AgendaController, DisponibilidadeController
from backend.controllers.profissional_controller import ProfissionalController, MeuProfissionalController
from backend.controllers.agendamento_controller import AgendamentoController
from backend.controllers.avaliacao_controller import AvaliacaoController, MinhasAvaliacoesController, ElegibilidadeController, FavoritoController
from backend.controllers.relatorio_controller import RelatorioController, ClientesClinicaController, RankingController, EstatisticasController, UsuariosController, EstatisticasPublicasController
from backend.controllers.conteudo_controller import BlogController, PortfolioController, QuestionarioController, ContatoController, DenunciaController, BuscaController, CheckoutController, ArquivoController, AtendimentoAdminController
from backend.controllers.chat_controller import ChatController, MensagemController, NotificacaoController
from backend.controllers.clinica_controller import RecomendacaoController


def registrar_rotas(app):
    routes = [
        ('/public/stats', EstatisticasPublicasController, ['GET'], {}),
        ('/recommendations', RecomendacaoController, ['GET'], {}),
        ('/auth/<action>', AuthController, ['GET', 'POST', 'PATCH', 'DELETE'], {}),
        ('/clinics', ClinicaController, ['GET', 'POST'], {}),
        ('/clinics/<int:id>', ClinicaController, ['GET', 'PATCH'], {}),
        ('/clinics/<int:id>/approval', AprovacaoController, ['PATCH'], {}),
        ('/clinics/<int:id>/verification', VerificacaoController, ['PATCH'], {}),
        ('/clinics/<int:id>/schedule', AgendaController, ['GET', 'PUT'], {}),
        ('/clinics/<int:id>/availability', DisponibilidadeController, ['GET'], {}),
        ('/professionals', ProfissionalController, ['GET', 'POST'], {}),
        ('/professionals/me', MeuProfissionalController, ['GET'], {}),
        ('/professionals/<int:id>', ProfissionalController, ['PATCH', 'DELETE'], {}),
        ('/appointments', AgendamentoController, ['GET', 'POST'], {}),
        ('/appointments/<int:id>', AgendamentoController, ['PATCH'], {}),
        ('/clinics/<int:clinic_id>/reviews', AvaliacaoController, ['GET', 'POST'], {}),
        ('/clinics/<int:clinic_id>/review-eligibility', ElegibilidadeController, ['GET'], {}),
        ('/reviews/<int:id>', AvaliacaoController, ['PATCH'], {}),
        ('/reviews/me', MinhasAvaliacoesController, ['GET'], {}),
        ('/favorites', FavoritoController, ['GET'], {}),
        ('/favorites/<int:clinic_id>', FavoritoController, ['PUT', 'DELETE'], {}),
        ('/clinics/<int:clinic_id>/reports', RelatorioController, ['GET'], {}),
        ('/clinics/<int:clinic_id>/clients', ClientesClinicaController, ['GET'], {}),
        ('/ranking', RankingController, ['GET'], {}),
        ('/admin/stats', EstatisticasController, ['GET'], {}),
        ('/admin/clients', UsuariosController, ['GET'], {}),
        ('/blog', BlogController, ['GET', 'POST'], {}),
        ('/blog/<int:id>', BlogController, ['PATCH', 'DELETE'], {}),
        ('/professionals/<int:id>/portfolio', PortfolioController, ['GET', 'POST'], {}),
        ('/portfolio/<int:item_id>', PortfolioController, ['DELETE'], {}),
        ('/clinics/<int:id>/assessment', QuestionarioController, ['GET', 'PUT'], {}),
        ('/contacts', ContatoController, ['POST'], {}),
        ('/reports', DenunciaController, ['POST'], {}),
        ('/search-history', BuscaController, ['GET', 'POST'], {}),
        ('/checkouts/<int:id>', CheckoutController, ['GET'], {}),
        ('/clinics/<int:clinic_id>/checkouts', CheckoutController, ['POST'], {}),
        ('/clinics/<int:clinic_id>/checkouts/<int:id>', CheckoutController, ['PATCH'], {}),
        ('/files', ArquivoController, ['POST'], {}),
        ('/files/<name>', ArquivoController, ['GET'], {}),
        ('/chats', ChatController, ['GET', 'POST'], {'kind': 'direct'}),
        ('/support-chats', ChatController, ['GET', 'POST'], {'kind': 'support'}),
        ('/chats/<int:id>/messages', MensagemController, ['GET', 'POST', 'PATCH'], {}),
        ('/notifications', NotificacaoController, ['GET', 'PATCH'], {}),
        ('/notifications/<int:id>', NotificacaoController, ['PATCH'], {}),
        ('/admin/contacts', AtendimentoAdminController, ['GET'], {'kind': 'contacts'}),
        ('/admin/reports', AtendimentoAdminController, ['GET'], {'kind': 'reports'}),
        ('/admin/reports/<int:id>', AtendimentoAdminController, ['PATCH'], {'kind': 'reports'}),
    ]
    for index, (path, controller, methods, defaults) in enumerate(routes):
        app.add_url_rule('/api' + path, view_func=controller.as_view(f'{controller.__name__}_{index}'), methods=methods, defaults=defaults)
