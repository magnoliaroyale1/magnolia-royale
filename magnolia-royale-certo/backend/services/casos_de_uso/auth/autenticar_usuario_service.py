"""Caso de uso AutenticarUsuarioService: uma ação pública, com validações e persistência nas Models/Repositories."""
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


class AutenticarUsuarioService(AuthHelpers):
    def executar(self, data):
        user = Usuario.primeiro(email=email(data))
        if not user or not user.active or not check_password_hash(user.password_hash, str(data.get('password', ''))):
            raise AppError('E-mail ou senha incorretos.', 401)
        self.entrar_sessao(user)
        return user.to_dict()
