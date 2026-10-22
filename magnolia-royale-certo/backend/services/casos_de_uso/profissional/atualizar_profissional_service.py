"""Caso de uso AtualizarProfissionalService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Profissional, ProfissionalProcedimento, Procedimento, Usuario, Agendamento
from backend.services.base import BaseService, texto, email



class AtualizarProfissionalService(BaseService):
    def executar(self, id, data):
        from backend.services.casos_de_uso.auth.criar_usuario_service import CriarUsuarioService
        from backend.services.casos_de_uso.auth.emitir_token_service import EmitirTokenService
        from backend.services.casos_de_uso.profissional.vincular_procedimentos_service import VincularProcedimentosService
        professional = self.profissional(id, manage=True)
        user = Usuario.buscar(professional.uid)
        changes = {}
        if 'name' in data:
            changes['name'] = texto(data, 'name', 120)
            user.atualizar(displayName=changes['name'])
        if 'email' in data:
            new_email = email(data)
            other = Usuario.primeiro(email=new_email)
            if other and other.id != user.id:
                raise AppError('E-mail já cadastrado.', 409)
            if new_email != user.email:
                user.atualizar(email=new_email, emailVerified=False, session_version=user.session_version+1)
                EmitirTokenService().executar(user, 'verify')
            changes['email'] = new_email
        if 'bio' in data:
            changes['bio'] = texto(data, 'bio', 5000, False)
        if 'procedures' in data:
            VincularProcedimentosService().executar(professional, data['procedures'])
        professional.atualizar(**changes)
        return professional.to_dict()
