"""Caso de uso AtualizarClinicaService: uma ação pública, com validações e persistência nas Models/Repositories."""
import re
from datetime import date, datetime, timedelta
from backend.errors import AppError
from backend.models import Clinica, Procedimento, Agenda, Usuario, Profissional, Agendamento, Notificacao
from backend.services.base import BaseService, texto, email, inteiro, dinheiro
from backend.repositories.clinica_repository import ClinicaRepository

from backend.services.auxiliares.clinica import ClinicaHelpers


class AtualizarClinicaService(ClinicaHelpers):
    def executar(self, id, data):
        from backend.services.casos_de_uso.avaliacao.recalcular_avaliacao_service import RecalcularAvaliacaoService
        from backend.services.casos_de_uso.clinica.salvar_procedimentos_service import SalvarProcedimentosService
        clinic = self.clinica(id, manage=True)
        changes = {}
        for field, size in [('name', 160), ('phone', 25), ('description', 5000)]:
            if field in data:
                changes[field] = texto(data, field, size, field != 'description')
        if 'email' in data:
            changes['email'] = email(data)
        if 'address' in data:
            address = data['address']
            if not isinstance(address, dict):
                raise AppError('Endereço inválido.')
            for key, size in [('city', 100), ('state', 2), ('street', 180), ('number', 20), ('zipCode', 12), ('neighborhood', 100)]:
                if key in address:
                    changes[key] = texto(address, key, size, key in ('city', 'state'))
        if 'images' in data:
            images = data['images']
            if not isinstance(images, list) or len(images) > 12 or any(not isinstance(i, str) or (i != '/clinic-demo.svg' and not i.startswith('/api/files/')) for i in images):
                raise AppError('Envie as imagens pela ferramenta de upload.')
            changes['images'] = images
        if 'cancellationPolicy' in data:
            policy = data['cancellationPolicy']
            if not isinstance(policy, dict):
                raise AppError('Política inválida.')
            result = {}
            for key in ('allowCancellation', 'chargeCancellationFee', 'allowRescheduling'):
                if type(policy.get(key)) is not bool:
                    raise AppError('Política inválida.')
                result[key] = policy[key]
            for key in ('minHoursBeforeCancel', 'minHoursBeforeReschedule'):
                result[key] = inteiro(policy.get(key, 24), key, 0, 8760)
            result['cancellationFee'] = float(dinheiro(policy.get('cancellationFee', 0)))
            changes['cancellationPolicy'] = result
        if 'services' in data or 'procedures' in data:
            SalvarProcedimentosService().executar(clinic, data.get('services', data.get('procedures')))
        clinic.atualizar(**changes)
    
        RecalcularAvaliacaoService().executar(clinic.id)
        return clinic.to_dict()
