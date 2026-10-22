from sqlalchemy import func
from backend.database import db
from backend.models import Avaliacao, Clinica


class AvaliacaoRepository:
    def resumo(self, clinic_id):
        average, count = db.session.query(func.avg(Avaliacao.rating), func.count(Avaliacao.id)).filter(Avaliacao.clinicId == clinic_id).one()
        return round(float(average or 0), 1), count

    def por_cliente(self, client_id):
        return db.session.query(Avaliacao, Clinica.name).join(Clinica, Avaliacao.clinicId == Clinica.id).filter(Avaliacao.clientId == client_id).order_by(Avaliacao.createdAt.desc()).all()
