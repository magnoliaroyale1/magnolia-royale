"""Caso de uso ListarProfissionaisService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Profissional, ProfissionalProcedimento, Procedimento, Usuario, Agendamento
from backend.services.base import BaseService, texto, email



class ListarProfissionaisService(BaseService):
    def executar(self, clinic_id):
        clinic = self.clinica(clinic_id)
        return [p.to_dict() for p in Profissional.listar(clinicId=clinic.id, active=True)]
