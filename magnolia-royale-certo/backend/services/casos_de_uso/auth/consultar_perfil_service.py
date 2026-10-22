"""Caso de uso ConsultarPerfilService: uma ação pública, com validações e persistência nas Models/Repositories."""
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


class ConsultarPerfilService(AuthHelpers):
    def executar(self):
        data = None
        user = self.usuario(verified=False)
        if data is not None:
            changes = {}
            if 'displayName' in data:
                changes['displayName'] = texto(data, 'displayName', 120)
            if 'phone' in data:
                changes['phone'] = texto(data, 'phone', 25, False)
            if 'preferences' in data:
                prefs = data['preferences']
                if not isinstance(prefs, dict):
                    raise AppError('Preferências inválidas.')
                for key in ('procedures', 'cities'):
                    if not isinstance(prefs.get(key, []), list) or any(not isinstance(x, str) or len(x) > 120 for x in prefs.get(key, [])):
                        raise AppError('Preferências inválidas.')
                if type(prefs.get('verifiedOnly', False)) is not bool:
                    raise AppError('Preferências inválidas.')
                from backend.services.base import inteiro
                changes['preferences'] = {'procedures': prefs.get('procedures', [])[:30], 'cities': prefs.get('cities', [])[:30],
                    'verifiedOnly': prefs.get('verifiedOnly', False), 'minRating': inteiro(prefs.get('minRating', 0), 'Nota mínima', 0, 5)}
            user.atualizar(**changes)
        return user.to_dict()
