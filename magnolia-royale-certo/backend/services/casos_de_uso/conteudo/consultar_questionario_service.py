"""Caso de uso ConsultarQuestionarioService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Publicacao, Portfolio, Questionario, Clinica, Profissional, Denuncia, Contato, Busca, Checkout, Usuario
from backend.models.usuario import agora
from backend.services.base import BaseService, texto, email, inteiro



class ConsultarQuestionarioService(BaseService):
    def executar(self, clinic_id):
        data = None
        clinic = self.clinica(clinic_id, manage=True)
        item = Questionario.primeiro(clinicId=clinic_id)
        if data is None:
            return item.answers if item else None
        if any(not isinstance(data.get(k), dict) for k in ('documentacao', 'profissionais', 'estrutura', 'horarios')):
            raise AppError('Preencha as etapas do questionário.')
        fields = {k: data[k] for k in ('documentacao', 'profissionais', 'estrutura', 'horarios')}
        fields['status'] = 'completed'
        if item:
            item.atualizar(answers=fields, updatedAt=agora())
        else:
            Questionario.criar(clinicId=clinic_id, answers=fields)
        clinic.atualizar(assessmentCompleted=True)
        return fields
