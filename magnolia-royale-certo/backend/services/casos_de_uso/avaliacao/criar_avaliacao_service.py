"""Caso de uso CriarAvaliacaoService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Avaliacao, Agendamento, Clinica, Procedimento, Favorito
from backend.services.base import BaseService, texto, inteiro
from backend.repositories.avaliacao_repository import AvaliacaoRepository



class CriarAvaliacaoService(BaseService):
    def executar(self, clinic_id, data):
        from backend.services.casos_de_uso.avaliacao.recalcular_avaliacao_service import RecalcularAvaliacaoService
        from backend.services.casos_de_uso.avaliacao.verificar_elegibilidade_avaliacao_service import VerificarElegibilidadeAvaliacaoService
        user = self.usuario(['client'])
        Clinica.buscar(clinic_id, bloquear=True)
        professional_id = inteiro(data['professionalId']) if data.get('professionalId') else None
        eligibility = VerificarElegibilidadeAvaliacaoService().executar(clinic_id, professional_id)
        if not eligibility['canReview']:
            raise AppError(eligibility['reason'], 409)
        completed = Agendamento.listar(clinicId=clinic_id, clientId=user.id, status='completed')
        appointment = next(a for a in completed if not professional_id or a.professionalId == professional_id)
        images = data.get('images', [])
        if not isinstance(images, list) or len(images) > 5 or any(not isinstance(x, str) or not x.startswith('/api/files/') for x in images):
            raise AppError('Imagens inválidas.')
        review = Avaliacao.criar(clinicId=clinic_id, clientId=user.id, professionalId=professional_id,
            appointmentId=appointment.id, clientName=user.displayName, rating=inteiro(data.get('rating'), 'Nota', 1, 5),
            comment=texto(data, 'comment', 5000), images=images)
        RecalcularAvaliacaoService().executar(clinic_id)
        return review.to_dict()
