"""Caso de uso ListarPublicacoesService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Publicacao, Portfolio, Questionario, Clinica, Profissional, Denuncia, Contato, Busca, Checkout, Usuario
from backend.models.usuario import agora
from backend.services.base import BaseService, texto, email, inteiro



class ListarPublicacoesService(BaseService):
    def executar(self, clinic_id=None):
        if clinic_id:
            self.clinica(clinic_id)
        return [dict(p.to_dict(), clinicName=Clinica.buscar(p.clinicId).name) for p in reversed(Publicacao.listar(**({'clinicId': clinic_id} if clinic_id else {})))
            if clinic_id or Clinica.buscar(p.clinicId).status == 'approved']
