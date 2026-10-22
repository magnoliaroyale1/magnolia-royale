"""Caso de uso EnviarEmailService: uma ação pública, com validações e persistência nas Models/Repositories."""
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


class EnviarEmailService(AuthHelpers):
    def executar(self, recipient, subject, body, link=''):
        if current_app.config['DEMO_MODE']:
            path = current_app.config['MAILBOX_DIR']
            path.mkdir(parents=True, exist_ok=True)
            (path / f'{secrets.token_hex(12)}.json').write_text(json.dumps({'to': recipient, 'subject': subject, 'body': body, 'link': link, 'createdAt': agora().isoformat() + 'Z'}, ensure_ascii=False), encoding='utf-8')
        else:
            import os, smtplib
            from email.message import EmailMessage
            host = os.environ.get('SMTP_HOST')
            if not host:
                raise AppError('Configure o servidor de e-mail antes de usar este recurso.', 503)
            message = EmailMessage()
            message['From'] = os.environ['SMTP_FROM']
            message['To'] = recipient
            message['Subject'] = subject
            message.set_content(body)
            with smtplib.SMTP(host, int(os.environ.get('SMTP_PORT', '587')), timeout=15) as smtp:
                smtp.starttls()
                smtp.login(os.environ['SMTP_USER'], os.environ['SMTP_PASSWORD'])
                smtp.send_message(message)
