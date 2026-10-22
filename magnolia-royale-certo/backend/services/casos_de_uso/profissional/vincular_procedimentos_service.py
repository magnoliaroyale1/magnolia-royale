"""Caso de uso VincularProcedimentosService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Profissional, ProfissionalProcedimento, Procedimento, Usuario, Agendamento
from backend.services.base import BaseService, texto, email



class VincularProcedimentosService(BaseService):
    def executar(self, professional, names):
        if not isinstance(names, list) or any(not isinstance(n, str) for n in names):
            raise AppError('Procedimentos inválidos.')
        selected = []
        for name in set(names):
            item = Procedimento.primeiro(clinicId=professional.clinicId, name=name, active=True)
            if not item:
                raise AppError(f'Cadastre o procedimento {name} na clínica primeiro.')
            selected.append(item)
        for link in ProfissionalProcedimento.listar(professionalId=professional.id):
            link.excluir()
        for item in selected:
            ProfissionalProcedimento.criar(professionalId=professional.id, procedureId=item.id)
