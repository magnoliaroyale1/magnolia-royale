"""Caso de uso CriarPublicacaoService: uma ação pública, com validações e persistência nas Models/Repositories."""
from backend.errors import AppError
from backend.models import Publicacao, Portfolio, Questionario, Clinica, Profissional, Denuncia, Contato, Busca, Checkout, Usuario
from backend.models.usuario import agora
from backend.services.base import BaseService, texto, email, inteiro



class CriarPublicacaoService(BaseService):
    def executar(self, data):
        id = None
        existing = Publicacao.buscar(id) if id else None
        clinic = self.clinica(existing.clinicId if existing else data.get('clinicId'), manage=True)
        fields = {key: texto(data, key, size, key not in ('image', 'category')) for key, size in
            [('title',180),('excerpt',500),('content',20000),('image',500),('category',80)]}
        if fields['image'] and fields['image'] != '/clinic-demo.svg' and not fields['image'].startswith(('/api/files/', 'https://')):
            raise AppError('Endereço de imagem inválido.')
        fields['readTime'] = max(1, round(len(fields['content'].split()) / 200))
        result = existing.atualizar(**fields) if existing else Publicacao.criar(clinicId=clinic.id, author=clinic.name, **fields)
        return result.to_dict()
