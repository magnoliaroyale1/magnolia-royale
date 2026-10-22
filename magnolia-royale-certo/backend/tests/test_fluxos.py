import ast
import io
import json
import os
import secrets
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from pathlib import Path
from threading import Barrier
from urllib.parse import urlparse, parse_qs
import pytest
from werkzeug.security import generate_password_hash
from backend.app import create_app
from backend.database import db
from backend.models import Usuario, Clinica, Agenda, Profissional, Procedimento, ProfissionalProcedimento, Agendamento, Avaliacao
from backend.services.auxiliares.agendamento import AgendamentoHelpers

PASSWORD = 'TesteSeguro@123'


@pytest.fixture(scope='session')
def app(tmp_path_factory):
    uri = os.environ.get('TEST_DATABASE_URL', '')
    if not uri or urlparse(uri).path != '/magnolia_royale_test':
        pytest.fail('Defina TEST_DATABASE_URL apontando exclusivamente para magnolia_royale_test.')
    temporary = tmp_path_factory.mktemp('magnolia')
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': uri, 'SECRET_KEY': 'test-secret',
        'UPLOAD_DIR': temporary/'uploads', 'MAILBOX_DIR': temporary/'mailbox', 'DEMO_MODE': True})
    with app.app_context():
        db.create_all()
    return app


@pytest.fixture()
def world(app):
    suffix = secrets.token_hex(6)
    with app.app_context():
        hashed = generate_password_hash(PASSWORD)
        def user(role):
            return Usuario.criar(email=f'{role}-{suffix}@example.test', displayName=f'Pessoa {role}', role=role, password_hash=hashed, emailVerified=True)
        users = {role: user(role) for role in ['client','clinic','professional','admin']}
        outsider = user('other')
        outsider.atualizar(role='client')
        clinic = Clinica.criar(ownerId=users['clinic'].id, name='Clínica Teste '+suffix, cnpj=str(secrets.randbelow(10**14)).zfill(14), email=users['clinic'].email, phone='11988887777', city='Campinas',state='SP',status='approved')
        Agenda.criar(clinicId=clinic.id,daysOfWeek=[0,1,2,3,4,5,6],startTime='08:00',endTime='20:00',slotDuration=60)
        professional=Profissional.criar(uid=users['professional'].id,clinicId=clinic.id,name='Profissional Teste',email=users['professional'].email)
        procedure=Procedimento.criar(clinicId=clinic.id,name='Limpeza de Pele',price=180)
        ProfissionalProcedimento.criar(professionalId=professional.id,procedureId=procedure.id)
        db.session.commit()
        result={'suffix':suffix,'clinic':clinic.id,'professional':professional.id,'procedure':procedure.id,
            'users':{k:{'id':u.id,'email':u.email} for k,u in users.items()},'outsider':{'id':outsider.id,'email':outsider.email}}
    return result


def client_for(app, account):
    client=app.test_client()
    client.csrf=client.get('/api/auth/session').json['csrfToken']
    if account:
        result=send(client,'POST','/auth/login',{'email':account['email'],'password':PASSWORD})
        assert result.status_code==200,result.json
    return client


def send(client,method,path,data=None):
    return client.open('/api'+path,method=method,json=data,headers={'X-CSRF-Token':client.csrf})


def booking(world, days=3, hour='10:00'):
    return {'clinicId':world['clinic'],'professionalId':world['professional'],'procedure':'Limpeza de Pele',
        'date':(AgendamentoHelpers.agora_local().date()+timedelta(days=days)).isoformat(),'time':hour}


def test_01_cadastro_login_verificacao_e_recuperacao(app,world):
    c=client_for(app,None)
    email=f'novo-{world["suffix"]}@example.test'
    r=send(c,'POST','/auth/register',{'email':email,'password':PASSWORD,'name':'Nova Cliente','role':'client'})
    assert r.status_code==200 and r.json['emailVerified'] is False
    assert c.get('/api/appointments').status_code==403
    with app.app_context():
        mail=next(json.loads(p.read_text(encoding='utf-8')) for p in app.config['MAILBOX_DIR'].glob('*.json') if json.loads(p.read_text(encoding='utf-8'))['to']==email)
    token=parse_qs(urlparse(mail['link']).query)['token'][0]
    assert send(c,'POST','/auth/verify',{'token':token}).status_code==200
    assert send(c,'POST','/auth/verify',{'token':token}).status_code==400
    assert c.get('/api/appointments').status_code==200
    send(c,'POST','/auth/logout',{})
    c.csrf=c.get('/api/auth/session').json['csrfToken']
    assert send(c,'POST','/auth/login',{'email':email,'password':PASSWORD}).status_code==200
    assert send(c,'POST','/auth/password-request',{'email':email}).status_code==200
    with app.app_context():
        reset=next(json.loads(p.read_text(encoding='utf-8')) for p in app.config['MAILBOX_DIR'].glob('*.json') if json.loads(p.read_text(encoding='utf-8'))['to']==email and 'Redefina' in json.loads(p.read_text(encoding='utf-8'))['subject'])
    reset_token=parse_qs(urlparse(reset['link']).query)['token'][0]
    assert send(c,'POST','/auth/reset',{'token':reset_token,'password':'NovaSenha@123'}).status_code==200
    assert c.get('/api/appointments').status_code==401
    assert send(c,'POST','/auth/login',{'email':email,'password':PASSWORD}).status_code==401
    assert send(c,'POST','/auth/login',{'email':email,'password':'NovaSenha@123'}).status_code==200


def test_02_clinica_cadastro_aprovacao_edicao_listagem(app,world):
    c=client_for(app,None)
    data={'name':'Clínica Nova','email':f'nova-clinica-{world["suffix"]}@example.test','password':PASSWORD,
        'cnpj':str(secrets.randbelow(10**14)).zfill(14),'phone':'11977776666','city':'Santos','state':'SP','procedures':['Peeling']}
    r=send(c,'POST','/clinics',data)
    assert r.status_code==200,r.json
    id=r.json['clinicId']
    public=app.test_client()
    assert public.get(f'/api/clinics/{id}').status_code==404
    admin=client_for(app,world['users']['admin'])
    assert send(admin,'PATCH',f'/clinics/{id}/approval',{'status':'rejected','feedback':'Completar documentos'}).json['status']=='rejected'
    assert send(admin,'PATCH',f'/clinics/{id}/approval',{'status':'approved'}).status_code==200
    assert public.get(f'/api/clinics/{id}').status_code==200
    assert send(admin,'PATCH',f'/clinics/{id}',{'description':'Descrição atualizada'}).json['description']=='Descrição atualizada'


def test_03_profissional_crud_vinculo_e_login(app,world):
    clinic=client_for(app,world['users']['clinic'])
    r=send(clinic,'POST','/professionals',{'clinicId':world['clinic'],'name':'Novo Profissional','email':f'prof-{world["suffix"]}@example.test','password':PASSWORD,'bio':'Perfil','procedures':['Limpeza de Pele']})
    assert r.status_code==200,r.json
    id=r.json['id']
    assert r.json['uid']!=id
    assert send(clinic,'PATCH',f'/professionals/{id}',{'bio':'Perfil atualizado'}).json['bio']=='Perfil atualizado'
    assert any(p['id']==id for p in clinic.get(f'/api/professionals?clinicId={world["clinic"]}').json)
    assert send(clinic,'DELETE',f'/professionals/{id}').status_code==200
    assert all(p['id']!=id for p in clinic.get(f'/api/professionals?clinicId={world["clinic"]}').json)


def test_04_catalogo_precos_agenda_bloqueios(app,world):
    c=client_for(app,world['users']['clinic']); id=world['clinic']
    r=send(c,'PATCH',f'/clinics/{id}',{'services':[{'name':'Limpeza de Pele','price':230},{'name':'Peeling','price':350}]})
    assert r.status_code==200 and r.json['services'][0]['price']==230
    day=booking(world)['date']
    agenda={'daysOfWeek':[0,1,2,3,4,5,6],'startTime':'09:00','endTime':'18:00','slotDuration':30,'blockedDates':[day]}
    assert send(c,'PUT',f'/clinics/{id}/schedule',agenda).status_code==200
    assert c.get(f'/api/clinics/{id}/availability?professionalId={world["professional"]}&date={day}').json==[]
    agenda['slotDuration']=0
    assert send(c,'PUT',f'/clinics/{id}/schedule',agenda).status_code==400


def test_05_agendamento_confirmacao_conclusao_e_preco_historico(app,world):
    c=client_for(app,world['users']['client']); clinic=client_for(app,world['users']['clinic'])
    r=send(c,'POST','/appointments',{**booking(world),'valor':1,'clientId':world['outsider']['id']})
    assert r.status_code==200,r.json
    a=r.json
    assert a['valor']==180 and a['clientId']==str(world['users']['client']['id'])
    assert send(c,'PATCH',f'/appointments/{a["id"]}',{'status':'completed'}).status_code==403
    assert send(clinic,'PATCH',f'/appointments/{a["id"]}',{'status':'confirmed'}).status_code==200
    assert send(clinic,'PATCH',f'/appointments/{a["id"]}',{'status':'completed'}).status_code==200
    send(clinic,'PATCH',f'/clinics/{world["clinic"]}',{'services':[{'name':'Limpeza de Pele','price':999}]})
    assert c.get('/api/appointments').json[0]['valor']==180
    prof=client_for(app,world['users']['professional'])
    assert prof.get('/api/appointments').json[0]['id']==a['id']


def test_06_reagendamento_cancelamento_e_liberacao(app,world):
    c=client_for(app,world['users']['client'])
    data=booking(world); a=send(c,'POST','/appointments',data).json
    r=send(c,'PATCH',f'/appointments/{a["id"]}',{'action':'reschedule','date':data['date'],'time':'11:00'})
    assert r.status_code==200 and r.json['time']=='11:00'
    assert send(c,'PATCH',f'/appointments/{a["id"]}',{'action':'cancel','reason':'Imprevisto'}).json['status']=='cancelled_by_client'
    data['time']='11:00'
    assert send(c,'POST','/appointments',data).status_code==200


def test_07_avaliacao_e_recalculo_apos_edicao(app,world):
    c=client_for(app,world['users']['client']);clinic=client_for(app,world['users']['clinic']);id=world['clinic']
    data={'rating':5,'comment':'Ótimo atendimento','professionalId':world['professional']}
    assert send(c,'POST',f'/clinics/{id}/reviews',data).status_code==409
    a=send(c,'POST','/appointments',booking(world)).json
    send(clinic,'PATCH',f'/appointments/{a["id"]}',{'status':'confirmed'})
    send(clinic,'PATCH',f'/appointments/{a["id"]}',{'status':'completed'})
    review=send(c,'POST',f'/clinics/{id}/reviews',data)
    assert review.status_code==200,review.json
    assert send(c,'POST',f'/clinics/{id}/reviews',data).status_code==409
    assert send(c,'PATCH',f'/reviews/{review.json["id"]}',{'rating':3,'comment':'Comentário revisado'}).status_code==200
    assert c.get(f'/api/clinics/{id}').json['rating']==3
    assert c.get('/api/reviews/me').json[0]['clinicName'].startswith('Clínica Teste')


def test_08_favoritos_idempotentes_persistentes(app,world):
    c=client_for(app,world['users']['client']);id=world['clinic']
    assert send(c,'PUT',f'/favorites/{id}').status_code==200
    assert send(c,'PUT',f'/favorites/{id}').status_code==200
    other_session=client_for(app,world['users']['client'])
    assert len(other_session.get('/api/favorites').json)==1
    assert send(other_session,'DELETE',f'/favorites/{id}').status_code==200
    assert c.get('/api/favorites').json==[]


def test_09_perfil_senha_preferencias_e_papeis(app,world):
    c=client_for(app,world['users']['client'])
    r=send(c,'PATCH','/auth/me',{'displayName':'Nome atualizado','role':'admin','preferences':{'cities':['Campinas'],'procedures':['Limpeza de Pele'],'minRating':0,'verifiedOnly':False}})
    assert r.json['displayName']=='Nome atualizado' and r.json['role']=='client'
    assert c.get('/api/recommendations').status_code==200
    assert send(c,'POST','/auth/password',{'currentPassword':'errada','newPassword':'NovaSenha@123'}).status_code==400
    assert send(c,'POST','/auth/password',{'currentPassword':PASSWORD,'newPassword':'NovaSenha@123'}).status_code==200
    assert c.get('/api/auth/me').json['displayName']=='Nome atualizado'


def test_10_relatorios_mysql_periodo_crm_ranking(app,world):
    c=client_for(app,world['users']['client']);clinic=client_for(app,world['users']['clinic'])
    a=send(c,'POST','/appointments',booking(world)).json
    send(clinic,'PATCH',f'/appointments/{a["id"]}',{'status':'confirmed'})
    send(clinic,'PATCH',f'/appointments/{a["id"]}',{'status':'completed'})
    url=f'/api/clinics/{world["clinic"]}/reports'
    r=clinic.get(url)
    assert r.status_code==200 and r.json['totalRevenue']==180 and r.json['completedCount']==1
    assert clinic.get(url+'?start=2000-01-01&end=2000-12-31').json['totalRevenue']==0
    assert clinic.get(f'/api/clinics/{world["clinic"]}/clients').json[0]['totalVisits']==1
    assert app.test_client().get('/api/ranking').status_code==200


def test_concorrencia_duas_reservas_apenas_uma_aceita(app,world):
    barrier=Barrier(2)
    def reserve(account):
        c=client_for(app,account);barrier.wait()
        return send(c,'POST','/appointments',booking(world)).status_code
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(reserve,world['users']['client']),pool.submit(reserve,world['outsider'])]
        assert sorted(f.result() for f in futures)==[200,409]


def test_permissoes_csrf_prazo_e_transacao(app,world):
    c=client_for(app,world['users']['client']);other=client_for(app,world['outsider'])
    assert c.post('/api/appointments',json=booking(world)).status_code==403
    assert send(c,'PATCH',f'/clinics/{world["clinic"]}',{'name':'Invasão'}).status_code==403
    assert c.get(f'/api/clinics/{world["clinic"]}/reports').status_code==403
    assert send(c,'POST','/auth/register',{'email':'admin@inv.test','password':PASSWORD,'name':'X','role':'admin'}).status_code==400
    a=send(c,'POST','/appointments',booking(world)).json
    assert send(other,'PATCH',f'/appointments/{a["id"]}',{'action':'cancel'}).status_code==403
    with app.app_context():
        Agendamento.buscar(a['id']).atualizar(date=AgendamentoHelpers.agora_local().date(),time='00:00')
        db.session.commit()
    assert send(c,'PATCH',f'/appointments/{a["id"]}',{'action':'cancel'}).status_code==400
    clinic=client_for(app,world['users']['clinic'])
    email=f'rollback-{world["suffix"]}@example.test'
    result=send(clinic,'POST','/professionals',{'clinicId':world['clinic'],'name':'Rollback','email':email,'password':PASSWORD,'procedures':['Inexistente']})
    assert result.status_code==400
    with app.app_context():
        assert Usuario.primeiro(email=email) is None


def test_extras_chat_blog_contato_denuncia_checkout_upload(app,world):
    c=client_for(app,world['users']['client']);clinic=client_for(app,world['users']['clinic']);admin=client_for(app,world['users']['admin'])
    chat=send(c,'POST','/chats',{'clinicId':world['clinic']}).json
    assert send(c,'POST',f'/chats/{chat["id"]}/messages',{'text':'Olá!'}).status_code==200
    assert clinic.get(f'/api/chats/{chat["id"]}/messages').json[0]['text']=='Olá!'
    outsider=client_for(app,world['outsider'])
    assert outsider.get(f'/api/chats/{chat["id"]}/messages').status_code==403
    assert send(clinic,'PATCH',f'/chats/{chat["id"]}/messages',{}).status_code==200
    support=send(c,'POST','/support-chats',{}).json
    assert send(admin,'POST',f'/chats/{support["id"]}/messages',{'text':'Como podemos ajudar?'}).status_code==200
    post=send(clinic,'POST','/blog',{'clinicId':world['clinic'],'title':'Novidades','excerpt':'Resumo','content':'Conteúdo do artigo','image':'','category':'Bem-estar'})
    assert post.status_code==200,post.json
    assert send(clinic,'DELETE',f'/blog/{post.json["id"]}').status_code==200
    assert send(c,'POST','/contacts',{'name':'Cliente','email':'contato@example.test','message':'Informações'}).status_code==200
    report=send(c,'POST','/reports',{'clinicId':world['clinic'],'reason':'Informação','description':'Verificar cadastro'}).json
    assert send(admin,'PATCH',f'/admin/reports/{report["id"]}',{'status':'resolved'}).status_code==200
    checkout=send(clinic,'POST',f'/clinics/{world["clinic"]}/checkouts',{'plan':'premium','price':1}).json
    assert checkout['price']==397
    assert send(clinic,'PATCH',f'/clinics/{world["clinic"]}/checkouts/{checkout["id"]}',{'paymentMethod':'pix'}).status_code==200
    assert clinic.get(f'/api/clinics/{world["clinic"]}').json['plan']=='premium'
    image=b'\x89PNG\r\n\x1a\n'+b'test-image'
    upload=clinic.post('/api/files',data={'file':(io.BytesIO(image),'test.png'),'context':'document'},headers={'X-CSRF-Token':clinic.csrf})
    assert upload.status_code==200,upload.json
    assert clinic.get(upload.json['url']).status_code==200
    assert outsider.get(upload.json['url']).status_code==403
    assert admin.get(upload.json['url']).status_code==200


def test_estatisticas_publicas_e_filtro_preco_zero(app, world):
    c = client_for(app, None)
    stats = c.get('/api/public/stats')
    assert stats.status_code == 200
    assert set(stats.json) == {'clinics', 'reviews', 'clients', 'verified'}
    assert all(isinstance(value, int) and value >= 0 for value in stats.json.values())
    assert str(world['clinic']) not in [item['id'] for item in c.get('/api/clinics?maxPrice=0').json]
    with app.app_context():
        Procedimento.buscar(world['procedure']).atualizar(price=0)
        db.session.commit()
    assert str(world['clinic']) in [item['id'] for item in c.get('/api/clinics?maxPrice=0').json]


def test_arquitetura_sem_firebase_e_sem_crud_em_repositories():
    root=Path(__file__).resolve().parents[2]
    for path in (root/'frontend'/'src').rglob('*'):
        if path.suffix in ('.ts','.tsx'):
            assert 'firebase/' not in path.read_text(encoding='utf-8')
    for path in (root/'backend'/'controllers').glob('*.py'):
        if path.name in ('base.py', '__init__.py'): continue
        tree=ast.parse(path.read_text(encoding='utf-8'))
        assert any(isinstance(node,ast.ClassDef) for node in tree.body)
        assert 'backend.models' not in path.read_text(encoding='utf-8')
    for path in (root/'backend'/'repositories').glob('*.py'):
        source=path.read_text(encoding='utf-8')
        assert '.criar(' not in source and '.excluir(' not in source and '.atualizar(' not in source
