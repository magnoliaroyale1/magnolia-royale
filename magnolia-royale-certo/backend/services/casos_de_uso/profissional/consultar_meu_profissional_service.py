from backend.errors import AppError
from backend.models import Profissional, ProfissionalProcedimento, Procedimento, Usuario, Agendamento
from backend.services.base import BaseService, texto, email



class ConsultarMeuProfissionalService(BaseService):
    def executar(self):
        user = self.usuario(['professional'])
        p = Profissional.primeiro(uid=user.id, active=True)
        return p.to_dict() if p else None
