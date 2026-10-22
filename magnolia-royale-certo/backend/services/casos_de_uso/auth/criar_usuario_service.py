"""Caso de uso CriarUsuarioService: uma ação pública, com validações e persistência nas Models/Repositories."""
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


class CriarUsuarioService(AuthHelpers):
    def executar(self, data, role='client', verified=False):
        address = email(data)
        if Usuario.primeiro(email=address):
            raise AppError('Este e-mail já está cadastrado.', 409)
        return Usuario.criar(email=address, displayName=texto(data, 'name', 120),
            password_hash=generate_password_hash(self.validar_senha(data.get('password'))),
            role=role, emailVerified=verified)
