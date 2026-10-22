from flask import request
from backend.controllers.base import ApiController, dados
from backend.services.casos_de_uso.agendamento.listar_agendamentos_service import ListarAgendamentosService
from backend.services.casos_de_uso.agendamento.criar_agendamento_service import CriarAgendamentoService
from backend.services.casos_de_uso.agendamento.remarcar_agendamento_service import RemarcarAgendamentoService
from backend.services.casos_de_uso.agendamento.cancelar_agendamento_service import CancelarAgendamentoService
from backend.services.casos_de_uso.agendamento.confirmar_agendamento_service import ConfirmarAgendamentoService
from backend.services.casos_de_uso.agendamento.concluir_agendamento_service import ConcluirAgendamentoService
from backend.errors import AppError


class AgendamentoController(ApiController):
    def get(self):
        return ListarAgendamentosService().executar(request.args)

    def post(self):
        return CriarAgendamentoService().executar(dados())

    def patch(self, id):
        data = dados()
        # A Controller interpreta a operação solicitada; validações e regras são do Service.
        if data.get('action') == 'reschedule':
            service = RemarcarAgendamentoService
        elif data.get('action') == 'cancel' or data.get('status') in ('cancelled','cancelled_by_client'):
            service = CancelarAgendamentoService
        else:
            service = {'confirmed': ConfirmarAgendamentoService,
                       'completed': ConcluirAgendamentoService}.get(data.get('status'))
            if service is None:
                raise AppError('Transição de status inválida.')
        return service().executar(id, data)
