"""Caso de uso CriarDenunciaService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Publicacao, Portfolio, Questionario, Clinica, Profissional, Denuncia, Contato, Busca, Checkout, Usuario
from backend.models.usuario import agora
from backend.services.base import BaseService, texto, email, inteiro



class CriarDenunciaService(BaseService):
    def executar(self, data):
        user = self.usuario()
        clinic = self.clinica(data.get('clinicId'))
        return Denuncia.criar(clinicId=clinic.id, reporterId=user.id, reason=texto(data, 'reason', 150), description=texto(data, 'description', 5000)).to_dict()
