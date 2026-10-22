from backend.database import db
from backend.models.base import CrudModel
from backend.models.usuario import Usuario, agora


class Profissional(CrudModel):
    __tablename__ = 'profissionais'
    uid = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True, nullable=False)
    clinicId = db.Column(db.Integer, db.ForeignKey('clinicas.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), nullable=False)
    bio = db.Column(db.Text, nullable=False, default='')
    photoURL = db.Column(db.String(500), default='')
    active = db.Column(db.Boolean, nullable=False, default=True)
    createdAt = db.Column(db.DateTime, nullable=False, default=agora)

    def to_dict(self):
        from backend.models.clinica import Procedimento
        data = super().to_dict()
        links = ProfissionalProcedimento.listar(professionalId=self.id)
        data['procedures'] = [Procedimento.buscar(link.procedureId).name for link in links]
        return data


class ProfissionalProcedimento(CrudModel):
    __tablename__ = 'profissional_procedimentos'
    __table_args__ = (db.UniqueConstraint('professionalId', 'procedureId'),)
    professionalId = db.Column(db.Integer, db.ForeignKey('profissionais.id'), nullable=False)
    procedureId = db.Column(db.Integer, db.ForeignKey('procedimentos.id'), nullable=False)
