"""Caso de uso ConsultarSessaoService: uma ação pública, com validações e persistência nas Models/Repositories."""
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


class ConsultarSessaoService(AuthHelpers):
    def executar(self):
        session.setdefault('csrf', secrets.token_urlsafe(32))
        user = self.usuario(required=False, verified=False)
        return {'user': user.to_dict() if user else None, 'csrfToken': session['csrf'], 'demoMode': current_app.config['DEMO_MODE']}
