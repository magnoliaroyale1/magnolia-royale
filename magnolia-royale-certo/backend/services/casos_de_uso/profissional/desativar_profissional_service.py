"""Caso de uso DesativarProfissionalService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Profissional, ProfissionalProcedimento, Procedimento, Usuario, Agendamento
from backend.services.base import BaseService, texto, email



class DesativarProfissionalService(BaseService):
    def executar(self, id):
        p = Profissional.buscar(id, bloquear=True)
        self.clinica(p.clinicId, manage=True)
        if any(a.status in ('pending', 'confirmed') for a in Agendamento.listar(professionalId=p.id)):
            raise AppError('Reagende ou cancele os atendimentos em aberto antes de inativar.', 409)
        p.atualizar(active=False)
        user = Usuario.buscar(p.uid)
        user.atualizar(active=False, session_version=user.session_version + 1)
        return {'ok': True}
