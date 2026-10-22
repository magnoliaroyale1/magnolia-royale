from backend.models import Agendamento, Clinica, Profissional


class AgendamentoRepository:
    def visiveis(self, user, filters):
        query = Agendamento.query
        if user.role == 'client':
            query = query.filter(Agendamento.clientId == user.id)
        elif user.role == 'clinic':
            query = query.join(Clinica, Clinica.id == Agendamento.clinicId).filter(Clinica.ownerId == user.id)
        elif user.role == 'professional':
            query = query.join(Profissional, Profissional.id == Agendamento.professionalId).filter(Profissional.uid == user.id)
        for key in ('clinicId', 'professionalId', 'clientId', 'status'):
            if filters.get(key):
                query = query.filter(getattr(Agendamento, key) == filters[key])
        return query.order_by(Agendamento.date, Agendamento.time, Agendamento.id).all()

    def ocupados(self, professional_id, date, excluding=None):
        query = Agendamento.query.filter(Agendamento.professionalId == professional_id,
            Agendamento.date == date, Agendamento.status.in_(['pending', 'confirmed', 'completed']))
        if excluding:
            query = query.filter(Agendamento.id != excluding)
        return query.all()
