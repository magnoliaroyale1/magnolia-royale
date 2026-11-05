from backend.errors import AppError
from backend.models import Profissional, ProfissionalProcedimento, Procedimento, Usuario, Agendamento
from backend.services.base import BaseService, texto, email



class ListarProfissionaisService(BaseService):
    def executar(self, clinic_id):
        clinic = self.clinica(clinic_id)
        return [p.to_dict() for p in Profissional.listar(clinicId=clinic.id, active=True)]
