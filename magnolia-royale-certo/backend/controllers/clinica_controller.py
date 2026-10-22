from flask import request
from backend.controllers.base import ApiController, dados
from backend.services.casos_de_uso.clinica.pesquisar_clinicas_service import PesquisarClinicasService
from backend.services.casos_de_uso.clinica.consultar_clinica_service import ConsultarClinicaService
from backend.services.casos_de_uso.clinica.cadastrar_clinica_service import CadastrarClinicaService
from backend.services.casos_de_uso.clinica.atualizar_clinica_service import AtualizarClinicaService
from backend.services.casos_de_uso.clinica.aprovar_clinica_service import AprovarClinicaService
from backend.services.casos_de_uso.clinica.rejeitar_clinica_service import RejeitarClinicaService
from backend.services.casos_de_uso.clinica.solicitar_ajustes_clinica_service import SolicitarAjustesClinicaService
from backend.errors import AppError
from backend.services.casos_de_uso.clinica.verificar_clinica_service import VerificarClinicaService
from backend.services.casos_de_uso.clinica.consultar_agenda_service import ConsultarAgendaService
from backend.services.casos_de_uso.clinica.atualizar_agenda_service import AtualizarAgendaService
from backend.services.casos_de_uso.clinica.recomendar_clinicas_service import RecomendarClinicasService
from backend.services.casos_de_uso.agendamento.consultar_disponibilidade_service import ConsultarDisponibilidadeService


class ClinicaController(ApiController):
    def get(self, id=None):
        return ConsultarClinicaService().executar(id) if id else PesquisarClinicasService().executar(request.args)

    def post(self):
        return CadastrarClinicaService().executar(dados())

    def patch(self, id):
        return AtualizarClinicaService().executar(id, dados())


class AprovacaoController(ApiController):
    def patch(self, id):
        data = dados()
        service = {'approved': AprovarClinicaService,
                   'rejected': RejeitarClinicaService,
                   'pending': SolicitarAjustesClinicaService}.get(data.get('status'))
        if service is None:
            raise AppError('Status inválido.')
        return service().executar(id, data)


class VerificacaoController(ApiController):
    def patch(self, id):
        return VerificarClinicaService().executar(id, dados())


class AgendaController(ApiController):
    def get(self, id):
        return ConsultarAgendaService().executar(id)

    def put(self, id):
        return AtualizarAgendaService().executar(id, dados())


class DisponibilidadeController(ApiController):
    def get(self, id):
        return ConsultarDisponibilidadeService().executar(id, request.args.get('professionalId'), request.args.get('date'))


class RecomendacaoController(ApiController):
    def get(self):
        return RecomendarClinicasService().executar()
