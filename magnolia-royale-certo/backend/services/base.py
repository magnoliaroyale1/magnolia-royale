import re
from decimal import Decimal, InvalidOperation
from flask import session
from backend.errors import AppError
from backend.models import Usuario, Clinica, Profissional


def texto(data, key, max_length=180, required=True):
    value = data.get(key, '')
    if not isinstance(value, str):
        raise AppError(f'{key}: informe um texto.')
    value = value.strip()
    if (required and not value) or len(value) > max_length:
        raise AppError(f'{key}: campo obrigatório, máximo de {max_length} caracteres.' if required else f'{key}: texto muito longo.')
    return value


def inteiro(value, field='id', minimum=1, maximum=2147483647):
    try:
        if isinstance(value, bool) or float(value) != int(value):
            raise ValueError()
        value = int(value)
    except (TypeError, ValueError, OverflowError):
        raise AppError(f'{field}: número inteiro inválido.')
    if not minimum <= value <= maximum:
        raise AppError(f'{field}: valor fora do intervalo permitido.')
    return value


def dinheiro(value):
    try:
        amount = Decimal(str(value))
        if not amount.is_finite() or amount < 0 or amount > 99999999:
            raise InvalidOperation()
        return amount.quantize(Decimal('0.01'))
    except (InvalidOperation, ValueError):
        raise AppError('Valor monetário inválido.')


def email(data):
    value = texto(data, 'email').lower()
    if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', value):
        raise AppError('E-mail inválido.')
    return value


class BaseService:
    def usuario(self, roles=None, required=True, verified=True):
        uid = session.get('user_id')
        user = Usuario.primeiro(id=uid) if uid else None
        if user and (not user.active or session.get('version') != user.session_version):
            user = None
        if not user:
            if required:
                raise AppError('Entre na sua conta para continuar.', 401)
            return None
        if roles and user.role not in roles:
            raise AppError('Você não tem permissão para esta ação.', 403)
        if verified and not user.emailVerified and user.role != 'admin':
            raise AppError('Verifique seu e-mail para continuar.', 403)
        return user

    def clinica(self, clinic_id, manage=False):
        clinic = Clinica.buscar(inteiro(clinic_id))
        if manage:
            user = self.usuario()
            if user.role != 'admin' and clinic.ownerId != user.id:
                raise AppError('Esta clínica pertence a outro usuário.', 403)
        elif clinic.status != 'approved':
            user = self.usuario(required=False, verified=False)
            professional = Profissional.primeiro(uid=user.id) if user else None
            if not user or (user.role != 'admin' and clinic.ownerId != user.id and not (professional and professional.clinicId == clinic.id)):
                raise AppError('Clínica não disponível.', 404)
        return clinic

    def profissional(self, professional_id, manage=False):
        item = Profissional.buscar(inteiro(professional_id))
        if manage:
            user = self.usuario()
            clinic = Clinica.buscar(item.clinicId)
            if user.role != 'admin' and user.id not in (item.uid, clinic.ownerId):
                raise AppError('Sem permissão para este profissional.', 403)
        return item
