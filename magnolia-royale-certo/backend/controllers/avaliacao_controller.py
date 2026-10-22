from backend.controllers.base import ApiController, dados
from backend.services.casos_de_uso.avaliacao.listar_avaliacoes_service import ListarAvaliacoesService
from backend.services.casos_de_uso.avaliacao.criar_avaliacao_service import CriarAvaliacaoService
from backend.services.casos_de_uso.avaliacao.editar_avaliacao_service import EditarAvaliacaoService
from backend.services.casos_de_uso.avaliacao.listar_minhas_avaliacoes_service import ListarMinhasAvaliacoesService
from backend.services.casos_de_uso.avaliacao.verificar_elegibilidade_avaliacao_service import VerificarElegibilidadeAvaliacaoService
from backend.services.casos_de_uso.avaliacao.listar_favoritos_service import ListarFavoritosService
from backend.services.casos_de_uso.avaliacao.adicionar_favorito_service import AdicionarFavoritoService
from backend.services.casos_de_uso.avaliacao.remover_favorito_service import RemoverFavoritoService


class AvaliacaoController(ApiController):
    def get(self, clinic_id):
        return ListarAvaliacoesService().executar(clinic_id)

    def post(self, clinic_id):
        return CriarAvaliacaoService().executar(clinic_id, dados())

    def patch(self, id):
        return EditarAvaliacaoService().executar(id, dados())


class MinhasAvaliacoesController(ApiController):
    def get(self):
        return ListarMinhasAvaliacoesService().executar()


class ElegibilidadeController(ApiController):
    def get(self, clinic_id):
        return VerificarElegibilidadeAvaliacaoService().executar(clinic_id)


class FavoritoController(ApiController):
    def get(self):
        return ListarFavoritosService().executar()

    def put(self, clinic_id):
        return AdicionarFavoritoService().executar(clinic_id)

    def delete(self, clinic_id):
        return RemoverFavoritoService().executar(clinic_id)
