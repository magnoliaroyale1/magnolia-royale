"""Caso de uso ConsultarClientesClinicaService: uma ação pública, com validações e persistência nas Models/Repositories."""
from datetime import date
from backend.errors import AppError
from backend.models import Clinica, Agendamento, Usuario
from backend.repositories.relatorio_repository import RelatorioRepository
from backend.services.base import BaseService



class ConsultarClientesClinicaService(BaseService):
    def executar(self, clinic_id):
        self.clinica(clinic_id, manage=True)
        results = RelatorioRepository().clientes(clinic_id)
        for item in results:
            appts = Agendamento.listar(clinicId=clinic_id, clientId=item['clientId'])
            item['clientId'] = str(item['clientId'])
            item['appointments'] = [a.to_dict() for a in appts]
            item['procedures'] = sorted(set(a.procedure for a in appts))
            item['professionals'] = sorted(set(a.professionalName for a in appts))
        return results
