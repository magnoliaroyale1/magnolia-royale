"""Atualiza exclusivamente as preferências persistidas do cliente."""
from backend.errors import AppError
from backend.services.base import BaseService, inteiro


class SalvarPreferenciasService(BaseService):
    def executar(self, prefs):
        user = self.usuario(['client'], verified=False)
        if not isinstance(prefs, dict):
            raise AppError('Preferências inválidas.')
        for key in ('procedures', 'cities'):
            if not isinstance(prefs.get(key, []), list) or any(
                not isinstance(value, str) or len(value) > 120 for value in prefs.get(key, [])
            ):
                raise AppError('Preferências inválidas.')
        if type(prefs.get('verifiedOnly', False)) is not bool:
            raise AppError('Preferências inválidas.')
        user.atualizar(preferences={
            'procedures': prefs.get('procedures', [])[:30],
            'cities': prefs.get('cities', [])[:30],
            'verifiedOnly': prefs.get('verifiedOnly', False),
            'minRating': inteiro(prefs.get('minRating', 0), 'Nota mínima', 0, 5),
        })
        return user.to_dict()
