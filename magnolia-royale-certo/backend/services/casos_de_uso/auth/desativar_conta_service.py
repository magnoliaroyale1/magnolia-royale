"""Caso de uso DesativarContaService: uma ação pública, com validações e persistência nas Models/Repositories."""
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


class DesativarContaService(AuthHelpers):
    def executar(self, data):
        user = self.usuario(verified=False)
        if not check_password_hash(user.password_hash, str(data.get('password', ''))):
            raise AppError('Senha incorreta.')
        if user.role != 'client':
            raise AppError('Contas vinculadas a clínicas devem ser administradas pelo responsável.')
        if any(a.status in ('pending', 'confirmed') for a in Agendamento.listar(clientId=user.id)):
            raise AppError('Cancele seus agendamentos em aberto antes de excluir a conta.')
        user.atualizar(active=False, session_version=user.session_version + 1)
        session.clear()
        return {'ok': True}
