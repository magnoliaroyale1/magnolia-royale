"""Caso de uso CadastrarProfissionalService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Profissional, ProfissionalProcedimento, Procedimento, Usuario, Agendamento
from backend.services.base import BaseService, texto, email



class CadastrarProfissionalService(BaseService):
    def executar(self, data):
        from backend.services.casos_de_uso.auth.criar_usuario_service import CriarUsuarioService
        from backend.services.casos_de_uso.auth.emitir_token_service import EmitirTokenService
        from backend.services.casos_de_uso.profissional.vincular_procedimentos_service import VincularProcedimentosService
        clinic = self.clinica(data.get('clinicId'), manage=True)
    
        user = CriarUsuarioService().executar(data, 'professional')
        professional = Profissional.criar(uid=user.id, clinicId=clinic.id, name=user.displayName, email=user.email, bio=texto(data, 'bio', 5000, False))
        VincularProcedimentosService().executar(professional, data.get('procedures', []))
        EmitirTokenService().executar(user, 'verify')
        return professional.to_dict()
