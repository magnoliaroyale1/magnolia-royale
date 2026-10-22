"""Caso de uso EmitirTokenService: uma ação pública, com validações e persistência nas Models/Repositories."""
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


class EmitirTokenService(AuthHelpers):
    def executar(self, user, purpose):
        from backend.services.casos_de_uso.auth.enviar_email_service import EnviarEmailService
        token = secrets.token_urlsafe(32)
        TokenConta.criar(userId=user.id, purpose=purpose, token_hash=hashlib.sha256(token.encode()).hexdigest(), expiresAt=agora() + timedelta(hours=1))
        link = f"{current_app.config['FRONTEND_URL']}/{'verify-email' if purpose == 'verify' else 'reset-password'}?token={token}"
        subject = 'Verifique seu e-mail' if purpose == 'verify' else 'Redefina sua senha'
        EnviarEmailService().executar(user.email, subject, f'{subject}: {link}', link)
