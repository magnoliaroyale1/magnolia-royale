from backend.database import db
from backend.models.base import CrudModel
from backend.models.usuario import agora


class Avaliacao(CrudModel):
    __tablename__ = 'avaliacoes'
    __table_args__ = (db.UniqueConstraint('clinicId', 'clientId'), db.CheckConstraint('rating BETWEEN 1 AND 5'))
    clinicId = db.Column(db.Integer, db.ForeignKey('clinicas.id'), nullable=False)
    clientId = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    professionalId = db.Column(db.Integer, db.ForeignKey('profissionais.id'), nullable=True)
    appointmentId = db.Column(db.Integer, db.ForeignKey('agendamentos.id'), nullable=False)
    clientName = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    images = db.Column(db.JSON, nullable=False, default=list)
    helpful = db.Column(db.Integer, nullable=False, default=0)
    createdAt = db.Column(db.DateTime, nullable=False, default=agora)


class Favorito(CrudModel):
    __tablename__ = 'favoritos'
    __table_args__ = (db.UniqueConstraint('userId', 'clinicId'),)
    userId = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    clinicId = db.Column(db.Integer, db.ForeignKey('clinicas.id'), nullable=False)
