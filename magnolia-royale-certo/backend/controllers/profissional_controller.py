from flask import request
from backend.controllers.base import ApiController, dados
from backend.services.casos_de_uso.profissional.listar_profissionais_service import ListarProfissionaisService
from backend.services.casos_de_uso.profissional.consultar_meu_profissional_service import ConsultarMeuProfissionalService
from backend.services.casos_de_uso.profissional.cadastrar_profissional_service import CadastrarProfissionalService
from backend.services.casos_de_uso.profissional.atualizar_profissional_service import AtualizarProfissionalService
from backend.services.casos_de_uso.profissional.desativar_profissional_service import DesativarProfissionalService


class ProfissionalController(ApiController):
    def get(self):
        return ListarProfissionaisService().executar(request.args.get('clinicId'))

    def post(self):
        return CadastrarProfissionalService().executar(dados())

    def patch(self, id):
        return AtualizarProfissionalService().executar(id, dados())

    def delete(self, id):
        return DesativarProfissionalService().executar(id)


class MeuProfissionalController(ApiController):
    def get(self):
        return ConsultarMeuProfissionalService().executar()
