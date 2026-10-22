"""Dados fictícios e repetíveis para a apresentação. Não apaga dados existentes."""
from datetime import timedelta
from werkzeug.security import generate_password_hash
from backend.app import create_app
from backend.database import db
from backend.models import *
from backend.services.auxiliares.agendamento import AgendamentoHelpers
from backend.services.casos_de_uso.avaliacao.recalcular_avaliacao_service import RecalcularAvaliacaoService


def seed():
    db.create_all()
    if Usuario.primeiro(email='admin@magnolia.test'):
        print('Base demonstrativa já existe; registros preservados.')
        return
    password = generate_password_hash('Magnolia@123')
    def usuario(name, email, role):
        return Usuario.criar(displayName=name, email=email, role=role, emailVerified=True, password_hash=password)
    admin = usuario('Admin Magnolia', 'admin@magnolia.test', 'admin')
    client = usuario('Marina Oliveira', 'cliente@magnolia.test', 'client')
    other = usuario('Rafael Santos', 'cliente2@magnolia.test', 'client')
    for index, (name, city, state) in enumerate([('Clínica Magnolia Jardins', 'São Paulo', 'SP'), ('Essência Royale', 'Campinas', 'SP'), ('Clínica Aurora', 'Rio de Janeiro', 'RJ')]):
        owner = usuario(name, 'clinica@magnolia.test' if index == 0 else f'clinica{index+1}@magnolia.test', 'clinic')
        clinic = Clinica.criar(ownerId=owner.id, name=name, cnpj=['11222333000181','22333444000192','33444555000103'][index], email=owner.email,
            phone='11988887777', city=city, state=state, street='Rua das Magnólias', number=str(120+index), neighborhood='Centro', zipCode='01001-000',
            description='Cuidado, acolhimento e atenção em cada detalhe. Conheça nossa equipe e escolha o melhor horário para você.',
            status='approved' if index < 2 else 'pending', verified=index == 0, plan='premium' if index == 0 else 'basic',
            assessmentCompleted=index == 0, images=['/clinic-demo.svg'])
        Agenda.criar(clinicId=clinic.id, daysOfWeek=[0,1,2,3,4,5,6], startTime='08:00', endTime='20:00', slotDuration=60)
        services = [Procedimento.criar(clinicId=clinic.id, name=n, price=p) for n,p in [('Limpeza de Pele',180),('Peeling',250),('Botox',700)]]
        profuser = usuario('Dra. Camila Alves' if index == 0 else f'Profissional {index+1}', 'profissional@magnolia.test' if index == 0 else f'profissional{index+1}@magnolia.test', 'professional')
        professional = Profissional.criar(uid=profuser.id, clinicId=clinic.id, name=profuser.displayName, email=profuser.email, bio='Profissional dedicada ao cuidado e bem-estar, com atendimento personalizado.')
        for proc in services:
            ProfissionalProcedimento.criar(professionalId=professional.id, procedureId=proc.id)
        if index < 2:
            today = AgendamentoHelpers.agora_local().date()
            for offset in range(1,7):
                proc = services[offset%3]
                Agendamento.criar(clinicId=clinic.id, professionalId=professional.id, clientId=client.id if offset%2 else other.id,
                    procedureId=proc.id, clientName=client.displayName if offset%2 else other.displayName, professionalName=professional.name,
                    procedure=proc.name, date=today-timedelta(days=offset*7), time='10:00', duration=60, status='completed', valor=proc.price)
            Agendamento.criar(clinicId=clinic.id, professionalId=professional.id, clientId=client.id,
                procedureId=services[0].id, clientName=client.displayName, professionalName=professional.name, procedure=services[0].name,
                date=today+timedelta(days=3), time='10:00', duration=60, status='confirmed', valor=services[0].price)
            completed = Agendamento.primeiro(clinicId=clinic.id, clientId=other.id, status='completed')
            Avaliacao.criar(clinicId=clinic.id, clientId=other.id, professionalId=professional.id, appointmentId=completed.id,
                clientName=other.displayName, rating=5 if index == 0 else 4, comment='Atendimento cuidadoso e equipe muito atenciosa.')
            Publicacao.criar(clinicId=clinic.id, title='Conheça nosso espaço de cuidado', excerpt='Um ambiente preparado para receber você.',
                content='Nossa equipe valoriza a escuta e o atendimento individualizado. Consulte os procedimentos e horários disponíveis no perfil da clínica.',
                image='/clinic-demo.svg', author=clinic.name, category='Bem-estar', readTime=1)
        RecalcularAvaliacaoService().executar(clinic.id)
    db.session.commit()
    print('Dados fictícios criados. Contas principais: admin, cliente, clinica e profissional @magnolia.test. Senha: Magnolia@123')


if __name__ == '__main__':
    with create_app().app_context():
        seed()
