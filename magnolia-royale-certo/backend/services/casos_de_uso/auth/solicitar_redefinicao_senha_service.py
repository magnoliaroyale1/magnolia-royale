"""Caso de uso SolicitarRedefinicaoSenhaService: uma ação pública, com validações e persistência nas Models/Repositories."""
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


class SolicitarRedefinicaoSenhaService(AuthHelpers):
    def executar(self, data):
        purpose = 'reset'
        from backend.services.casos_de_uso.auth.emitir_token_service import EmitirTokenService
        user = self.usuario(verified=False) if purpose == 'verify' else Usuario.primeiro(email=email(data))
        if user and user.active:
            EmitirTokenService().executar(user, purpose)
        return {'ok': True, 'message': 'Se a conta estiver cadastrada, as instruções foram enviadas.'}
