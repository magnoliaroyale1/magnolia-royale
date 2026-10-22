"""Caso de uso CadastrarClienteService: uma ação pública, com validações e persistência nas Models/Repositories."""
import hashlib
import json
import secrets
from datetime import timedelta
from flask import current_app, session
from werkzeug.security import generate_password_hash, check_password_hash
from backend.errors import AppError
from backend.models import Usuario, TokenConta, Agendamento, Profissional
from backend.models.usuario import agora
from backend.services.base import BaseService, texto, email

from backend.services.auxiliares.auth import AuthHelpers


class CadastrarClienteService(AuthHelpers):
    def executar(self, data):
        from backend.services.casos_de_uso.auth.criar_usuario_service import CriarUsuarioService
        from backend.services.casos_de_uso.auth.emitir_token_service import EmitirTokenService
        if data.get('role', 'client') != 'client':
            raise AppError('O cadastro público cria apenas contas de cliente.')
        user = CriarUsuarioService().executar(data)
        self.entrar_sessao(user)
        EmitirTokenService().executar(user, 'verify')
        return user.to_dict()
