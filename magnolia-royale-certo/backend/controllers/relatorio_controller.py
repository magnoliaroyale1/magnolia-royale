from flask import request
from backend.controllers.base import ApiController
from backend.services.casos_de_uso.relatorio.gerar_relatorio_financeiro_service import GerarRelatorioFinanceiroService
from backend.services.casos_de_uso.relatorio.consultar_clientes_clinica_service import ConsultarClientesClinicaService
from backend.services.casos_de_uso.relatorio.consultar_ranking_service import ConsultarRankingService
from backend.services.casos_de_uso.relatorio.consultar_estatisticas_publicas_service import ConsultarEstatisticasPublicasService
from backend.services.casos_de_uso.relatorio.consultar_estatisticas_admin_service import ConsultarEstatisticasAdminService
from backend.services.casos_de_uso.relatorio.listar_usuarios_service import ListarUsuariosService


class RelatorioController(ApiController):
    def get(self, clinic_id):
        return GerarRelatorioFinanceiroService().executar(clinic_id, request.args)


class ClientesClinicaController(ApiController):
    def get(self, clinic_id):
        return ConsultarClientesClinicaService().executar(clinic_id)


class RankingController(ApiController):
    def get(self):
        return ConsultarRankingService().executar()


class EstatisticasController(ApiController):
    def get(self):
        return ConsultarEstatisticasAdminService().executar()


class EstatisticasPublicasController(ApiController):
    def get(self):
        return ConsultarEstatisticasPublicasService().executar()


class UsuariosController(ApiController):
    def get(self):
        return ListarUsuariosService().executar()
