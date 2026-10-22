from datetime import datetime, timezone
from backend.database import db
from backend.models.base import CrudModel


def agora():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Usuario(CrudModel):
    __tablename__ = 'usuarios'
    email = db.Column(db.String(180), unique=True, nullable=False)
    displayName = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='client')
    photoURL = db.Column(db.String(500), default='')
    phone = db.Column(db.String(25), default='')
    emailVerified = db.Column(db.Boolean, nullable=False, default=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    session_version = db.Column(db.Integer, nullable=False, default=1)
    createdAt = db.Column(db.DateTime, nullable=False, default=agora)
    preferences = db.Column(db.JSON, nullable=False, default=dict)

    def to_dict(self):
        from backend.models.clinica import Clinica
        from backend.models.profissional import Profissional
        data = super().to_dict()
        data['uid'] = data['id']
        clinic = Clinica.primeiro(ownerId=self.id)
        professional = Profissional.primeiro(uid=self.id)
        data['clinicId'] = str(clinic.id) if clinic else (str(professional.clinicId) if professional else None)
        data['professionalId'] = str(professional.id) if professional else None
        return data


class TokenConta(CrudModel):
    __tablename__ = 'tokens_conta'
    userId = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    token_hash = db.Column(db.String(64), unique=True, nullable=False)
    purpose = db.Column(db.String(20), nullable=False)
    expiresAt = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, nullable=False, default=False)
