"""Caso de uso ConsultarArquivoService: uma ação pública, com validações e persistência nas Models/Repositories."""
import secrets
from flask import current_app
from werkzeug.utils import secure_filename
from backend.errors import AppError
from backend.models import Arquivo
from backend.services.base import BaseService



class ConsultarArquivoService(BaseService):
    def executar(self, name):
        item = Arquivo.primeiro(name=name)
        if not item:
            raise AppError('Arquivo não encontrado.', 404)
        if item.private:
            user = self.usuario()
            if user.role != 'admin' and item.ownerId != user.id:
                raise AppError('Documento privado.', 403)
        return item.name, item.mimeType
