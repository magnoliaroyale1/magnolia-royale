"""Caso de uso EnviarArquivoService: uma ação pública, com validações e persistência nas Models/Repositories."""
import secrets
from flask import current_app
from werkzeug.utils import secure_filename
from backend.errors import AppError
from backend.models import Arquivo
from backend.services.base import BaseService



class EnviarArquivoService(BaseService):
    def executar(self, file, context='image'):
        user = self.usuario()
        if not file:
            raise AppError('Selecione um arquivo.')
        content = file.read(5 * 1024 * 1024 + 1)
        if len(content) > 5 * 1024 * 1024:
            raise AppError('O arquivo deve ter no máximo 5 MB.')
        suffix, mime = None, None
        if content.startswith(b'\x89PNG\r\n\x1a\n'):
            suffix, mime = 'png', 'image/png'
        elif content.startswith(b'\xff\xd8\xff'):
            suffix, mime = 'jpg', 'image/jpeg'
        elif content.startswith((b'GIF87a', b'GIF89a')):
            suffix, mime = 'gif', 'image/gif'
        elif content.startswith(b'RIFF') and content[8:12] == b'WEBP':
            suffix, mime = 'webp', 'image/webp'
        elif content.startswith(b'%PDF-') and context == 'document':
            suffix, mime = 'pdf', 'application/pdf'
        if not suffix:
            raise AppError('Formato inválido. Use PNG, JPEG, GIF, WebP ou PDF para documentos.')
        name = secrets.token_hex(24) + '.' + suffix
        directory = current_app.config['UPLOAD_DIR']
        directory.mkdir(parents=True, exist_ok=True)
        (directory / name).write_bytes(content)
        Arquivo.criar(ownerId=user.id, name=name, originalName=secure_filename(file.filename)[:255], mimeType=mime, private=context == 'document')
        return {'url': '/api/files/' + name}
