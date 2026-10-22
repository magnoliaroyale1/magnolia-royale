from backend.database import db
from backend.models.base import CrudModel
from backend.models.usuario import agora


class Clinica(CrudModel):
    __tablename__ = 'clinicas'
    ownerId = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True, nullable=False)
    name = db.Column(db.String(160), nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(180), nullable=False)
    phone = db.Column(db.String(25), nullable=False)
    street = db.Column(db.String(180), nullable=False, default='')
    number = db.Column(db.String(20), nullable=False, default='')
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipCode = db.Column(db.String(12), nullable=False, default='')
    neighborhood = db.Column(db.String(100), nullable=False, default='')
    description = db.Column(db.Text, nullable=False, default='')
    status = db.Column(db.String(20), nullable=False, default='pending')
    verified = db.Column(db.Boolean, nullable=False, default=False)
    rating = db.Column(db.Numeric(3, 1), nullable=False, default=0)
    reviewCount = db.Column(db.Integer, nullable=False, default=0)
    score = db.Column(db.Integer, nullable=False, default=0)
    plan = db.Column(db.String(20), nullable=False, default='basic')
    images = db.Column(db.JSON, nullable=False, default=list)
    cancellationPolicy = db.Column(db.JSON, nullable=False, default=lambda: {
        'allowCancellation': True, 'minHoursBeforeCancel': 24,
        'chargeCancellationFee': False, 'cancellationFee': 0,
        'allowRescheduling': True, 'minHoursBeforeReschedule': 24})
    adminFeedback = db.Column(db.Text, default='')
    assessmentCompleted = db.Column(db.Boolean, nullable=False, default=False)
    verificationCriteria = db.Column(db.JSON, default=dict)
    createdAt = db.Column(db.DateTime, nullable=False, default=agora)

    def to_dict(self):
        data = super().to_dict()
        data['address'] = {k: data.pop(k) for k in ('street', 'number', 'city', 'state', 'zipCode', 'neighborhood')}
        data['approved'] = self.status == 'approved'
        services = Procedimento.listar(clinicId=self.id, active=True)
        data['procedures'] = [item.name for item in services]
        data['services'] = [item.to_dict() for item in services]
        return data


class Procedimento(CrudModel):
    __tablename__ = 'procedimentos'
    __table_args__ = (db.UniqueConstraint('clinicId', 'name'),)
    clinicId = db.Column(db.Integer, db.ForeignKey('clinicas.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    active = db.Column(db.Boolean, nullable=False, default=True)


class Agenda(CrudModel):
    __tablename__ = 'agendas'
    clinicId = db.Column(db.Integer, db.ForeignKey('clinicas.id'), nullable=False, unique=True)
    daysOfWeek = db.Column(db.JSON, nullable=False, default=lambda: [1, 2, 3, 4, 5])
    startTime = db.Column(db.String(5), nullable=False, default='09:00')
    endTime = db.Column(db.String(5), nullable=False, default='17:00')
    slotDuration = db.Column(db.Integer, nullable=False, default=60)
    blockedDates = db.Column(db.JSON, nullable=False, default=list)
