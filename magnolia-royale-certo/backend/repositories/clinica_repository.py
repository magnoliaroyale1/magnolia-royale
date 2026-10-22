from sqlalchemy import or_
from backend.models import Clinica, Procedimento


class ClinicaRepository:
    def recomendar(self, preferences):
        query = Clinica.query.filter(Clinica.status == 'approved')
        if preferences.get('verifiedOnly'):
            query = query.filter(Clinica.verified.is_(True))
        if preferences.get('minRating'):
            query = query.filter(Clinica.rating >= preferences['minRating'])
        if preferences.get('cities'):
            query = query.filter(Clinica.city.in_(preferences['cities']))
        if preferences.get('procedures'):
            query = query.join(Procedimento, Procedimento.clinicId == Clinica.id).filter(Procedimento.active.is_(True), Procedimento.name.in_(preferences['procedures']))
        return query.distinct().order_by(Clinica.score.desc(), Clinica.id).limit(6).all()

    def pesquisar(self, filters, public=True):
        query = Clinica.query
        if public:
            query = query.filter(Clinica.status == 'approved')
        elif filters.get('status'):
            query = query.filter(Clinica.status == filters['status'])
        if filters.get('location'):
            location = '%' + filters['location'][:100] + '%'
            query = query.filter(or_(Clinica.city.ilike(location), Clinica.state.ilike(location)))
        if filters.get('verifiedOnly') in (True, 'true', '1'):
            query = query.filter(Clinica.verified.is_(True))
        if filters.get('minRating'):
            query = query.filter(Clinica.rating >= filters['minRating'])
        if any(filters.get(k) not in (None, '') for k in ('procedure', 'minPrice', 'maxPrice')):
            query = query.join(Procedimento, Procedimento.clinicId == Clinica.id).filter(Procedimento.active.is_(True))
            if filters.get('procedure'):
                query = query.filter(Procedimento.name == filters['procedure'])
            if filters.get('minPrice') not in (None, ''):
                query = query.filter(Procedimento.price >= filters['minPrice'])
            if filters.get('maxPrice') not in (None, ''):
                query = query.filter(Procedimento.price <= filters['maxPrice'])
        return query.distinct().order_by(Clinica.rating.desc(), Clinica.id).all()
