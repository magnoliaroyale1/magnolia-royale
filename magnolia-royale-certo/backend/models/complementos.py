from backend.database import db
from backend.models.base import CrudModel
from backend.models.usuario import agora


class Publicacao(CrudModel):
    __tablename__ = 'publicacoes'
    clinicId = db.Column(db.Integer, db.ForeignKey('clinicas.id'), nullable=False)
    title = db.Column(db.String(180), nullable=False)
    excerpt = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(500), default='')
    author = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(80), default='Estética')
    readTime = db.Column(db.Integer, nullable=False, default=3)
    createdAt = db.Column(db.DateTime, nullable=False, default=agora)


class Portfolio(CrudModel):
    __tablename__ = 'portfolio'
    professionalId = db.Column(db.Integer, db.ForeignKey('profissionais.id'), nullable=False)
    imageUrl = db.Column(db.String(500), nullable=False)
    procedure = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, default='')
    createdAt = db.Column(db.DateTime, nullable=False, default=agora)


class Questionario(CrudModel):
    __tablename__ = 'questionarios'
    clinicId = db.Column(db.Integer, db.ForeignKey('clinicas.id'), unique=True, nullable=False)
    answers = db.Column(db.JSON, nullable=False)
    updatedAt = db.Column(db.DateTime, nullable=False, default=agora)


class Notificacao(CrudModel):
    __tablename__ = 'notificacoes'
    userId = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(180), nullable=False)
    message = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(250), default='')
    read = db.Column(db.Boolean, nullable=False, default=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=agora)


class Conversa(CrudModel):
    __tablename__ = 'conversas'
    __table_args__ = (db.UniqueConstraint('clientId', 'clinicId', 'kind'),)
    clientId = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    clinicId = db.Column(db.Integer, db.ForeignKey('clinicas.id'), nullable=True)
    kind = db.Column(db.String(15), nullable=False, default='direct')
    clientName = db.Column(db.String(120), nullable=False)
    clinicName = db.Column(db.String(160), default='Suporte Magnolia')
    lastMessage = db.Column(db.Text, default='')
    lastMessageAt = db.Column(db.DateTime, nullable=False, default=agora)


class Mensagem(CrudModel):
    __tablename__ = 'mensagens'
    chatId = db.Column(db.Integer, db.ForeignKey('conversas.id'), nullable=False)
    senderId = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    senderName = db.Column(db.String(120), nullable=False)
    text = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, nullable=False, default=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=agora)


class Denuncia(CrudModel):
    __tablename__ = 'denuncias'
    clinicId = db.Column(db.Integer, db.ForeignKey('clinicas.id'), nullable=False)
    reporterId = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    reason = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='open')
    createdAt = db.Column(db.DateTime, nullable=False, default=agora)


class Contato(CrudModel):
    __tablename__ = 'contatos'
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), nullable=False)
    subject = db.Column(db.String(180), nullable=False, default='Contato')
    message = db.Column(db.Text, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=agora)


class Busca(CrudModel):
    __tablename__ = 'buscas'
    userId = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    term = db.Column(db.String(180), nullable=False, default='')
    filters = db.Column(db.JSON, nullable=False, default=dict)
    createdAt = db.Column(db.DateTime, nullable=False, default=agora)


class Checkout(CrudModel):
    __tablename__ = 'checkouts_demonstracao'
    clinicId = db.Column(db.Integer, db.ForeignKey('clinicas.id'), nullable=False)
    plan = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    paymentMethod = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    createdAt = db.Column(db.DateTime, nullable=False, default=agora)
    paidAt = db.Column(db.DateTime, nullable=True)


class Arquivo(CrudModel):
    __tablename__ = 'arquivos'
    ownerId = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    originalName = db.Column(db.String(255), nullable=False)
    mimeType = db.Column(db.String(80), nullable=False)
    private = db.Column(db.Boolean, nullable=False, default=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=agora)
