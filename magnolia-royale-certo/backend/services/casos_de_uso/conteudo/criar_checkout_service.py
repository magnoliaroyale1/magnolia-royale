"""Caso de uso CriarCheckoutService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Publicacao, Portfolio, Questionario, Clinica, Profissional, Denuncia, Contato, Busca, Checkout, Usuario
from backend.models.usuario import agora
from backend.services.base import BaseService, texto, email, inteiro



class CriarCheckoutService(BaseService):
    def executar(self, clinic_id, data):
        id = None
        from backend.services.casos_de_uso.avaliacao.recalcular_avaliacao_service import RecalcularAvaliacaoService
        from flask import current_app
        if not current_app.config['DEMO_MODE']:
            raise AppError('Checkout disponível apenas como demonstração acadêmica.', 403)
        clinic = self.clinica(clinic_id, manage=True)
        prices = {'basic': 97, 'professional': 197, 'premium': 397}
        if id is None:
            plan = data.get('plan')
            if plan not in prices:
                raise AppError('Plano inválido.')
            return Checkout.criar(clinicId=clinic.id, plan=plan, price=prices[plan]).to_dict()
        checkout = Checkout.buscar(id, bloquear=True)
        if checkout.clinicId != clinic.id:
            raise AppError('Checkout não pertence a esta clínica.', 403)
        method = data.get('paymentMethod')
        if method not in ('credit_card', 'boleto', 'pix'):
            raise AppError('Forma de pagamento inválida.')
        if checkout.status == 'pending':
            checkout.atualizar(status='completed', paymentMethod=method, paidAt=agora())
            clinic.atualizar(plan=checkout.plan)
        
            RecalcularAvaliacaoService().executar(clinic.id)
        return checkout.to_dict()
