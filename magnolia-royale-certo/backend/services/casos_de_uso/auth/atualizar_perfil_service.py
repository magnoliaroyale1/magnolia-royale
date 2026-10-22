"""Caso de uso AtualizarPerfilService: uma ação pública, com validações e persistência nas Models/Repositories."""
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


class AtualizarPerfilService(AuthHelpers):
    def executar(self, data):
        user = self.usuario(verified=False)
        if data is not None:
            changes = {}
            if 'displayName' in data:
                changes['displayName'] = texto(data, 'displayName', 120)
            if 'phone' in data:
                changes['phone'] = texto(data, 'phone', 25, False)
            if 'preferences' in data:
                from backend.services.casos_de_uso.auth.salvar_preferencias_service import SalvarPreferenciasService
                SalvarPreferenciasService().executar(data['preferences'])
            user.atualizar(**changes)
        return user.to_dict()
