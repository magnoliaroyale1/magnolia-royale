from backend.database import db
from backend.models.base import CrudModel
from backend.models.usuario import agora


class Agendamento(CrudModel):
    __tablename__ = 'agendamentos'
    __table_args__ = (db.Index('ix_agenda_profissional', 'professionalId', 'date', 'status'),)
    clinicId = db.Column(db.Integer, db.ForeignKey('clinicas.id'), nullable=False)
    professionalId = db.Column(db.Integer, db.ForeignKey('profissionais.id'), nullable=False)
    clientId = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    procedureId = db.Column(db.Integer, db.ForeignKey('procedimentos.id'), nullable=False)
    clientName = db.Column(db.String(120), nullable=False)
    professionalName = db.Column(db.String(120), nullable=False)
    procedure = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(5), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30), nullable=False, default='pending')
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    notes = db.Column(db.Text, default='')
    cancelReason = db.Column(db.Text, default='')
    cancellationFee = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    createdAt = db.Column(db.DateTime, nullable=False, default=agora)


class HistoricoAgendamento(CrudModel):
    __tablename__ = 'historico_agendamentos'
    appointmentId = db.Column(db.Integer, db.ForeignKey('agendamentos.id'), nullable=False)
    actorId = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    action = db.Column(db.String(30), nullable=False)
    details = db.Column(db.JSON, nullable=False, default=dict)
    createdAt = db.Column(db.DateTime, nullable=False, default=agora)
