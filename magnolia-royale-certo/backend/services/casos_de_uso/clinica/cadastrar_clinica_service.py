"""Caso de uso CadastrarClinicaService: uma ação pública, com validações e persistência nas Models/Repositories."""
import re
from datetime import date, datetime, timedelta
from backend.errors import AppError
from backend.models import Clinica, Procedimento, Agenda, Usuario, Profissional, Agendamento, Notificacao
from backend.services.base import BaseService, texto, email, inteiro, dinheiro
from backend.repositories.clinica_repository import ClinicaRepository

from backend.services.auxiliares.clinica import ClinicaHelpers
from backend.services.auxiliares.auth import AuthHelpers


class CadastrarClinicaService(ClinicaHelpers):
    def executar(self, data):
        from backend.services.casos_de_uso.auth.criar_usuario_service import CriarUsuarioService
        from backend.services.casos_de_uso.auth.emitir_token_service import EmitirTokenService
        from backend.services.casos_de_uso.clinica.salvar_procedimentos_service import SalvarProcedimentosService
    
        address = data.get('address', data)
        cnpj = re.sub(r'\D', '', texto(data, 'cnpj', 30))
        if len(cnpj) != 14 or len(set(cnpj)) == 1:
            raise AppError('Informe um CNPJ com 14 dígitos.')
        if Clinica.primeiro(cnpj=cnpj):
            raise AppError('CNPJ já cadastrado.', 409)
        user = CriarUsuarioService().executar(data, 'clinic')
        clinic = Clinica.criar(ownerId=user.id, name=texto(data, 'name', 160), cnpj=cnpj,
            email=user.email, phone=texto(data, 'phone', 25),
            city=texto(address, 'city', 100), state=texto(address, 'state', 2).upper(),
            street=texto(address, 'street', 180, False), number=texto(address, 'number', 20, False),
            zipCode=texto(address, 'zipCode', 12, False), neighborhood=texto(address, 'neighborhood', 100, False),
            description=texto(data, 'description', 5000, False))
        Agenda.criar(clinicId=clinic.id)
        SalvarProcedimentosService().executar(clinic, data.get('services', data.get('procedures', [])))
        AuthHelpers().entrar_sessao(user)
        EmitirTokenService().executar(user, 'verify')
        return user.to_dict()
