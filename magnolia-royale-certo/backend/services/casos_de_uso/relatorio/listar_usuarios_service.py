"""Caso de uso ListarUsuariosService: uma ação pública, com validações e persistência nas Models/Repositories."""
from datetime import date
from backend.errors import AppError
from backend.models import Clinica, Agendamento, Usuario
from backend.repositories.relatorio_repository import RelatorioRepository
from backend.services.base import BaseService



class ListarUsuariosService(BaseService):
    def executar(self):
        self.usuario(['admin'])
        return [u.to_dict() for u in Usuario.listar(role='client', active=True)]
