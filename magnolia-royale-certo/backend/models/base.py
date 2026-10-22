from datetime import date, datetime
from decimal import Decimal
from backend.database import db
from backend.errors import AppError


class CrudModel(db.Model):
    """CRUD compartilhado pelas Models. A transação termina na Controller.

    flush envia o INSERT ao MySQL, mas permite desfazer toda a operação
    caso um segundo cadastro relacionado falhe.
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def buscar(cls, id, bloquear=False):
        query = cls.query.filter_by(id=id)
        if bloquear:
            query = query.with_for_update()
        item = query.first()
        if not item:
            raise AppError('Registro não encontrado.', 404)
        return item

    @classmethod
    def listar(cls, **filtros):
        return cls.query.filter_by(**filtros).order_by(cls.id).all()

    @classmethod
    def primeiro(cls, **filtros):
        return cls.query.filter_by(**filtros).first()

    @classmethod
    def criar(cls, **dados):
        item = cls(**dados)
        db.session.add(item)
        db.session.flush()
        return item

    def atualizar(self, **dados):
        for campo, valor in dados.items():
            setattr(self, campo, valor)
        db.session.flush()
        return self

    def excluir(self):
        db.session.delete(self)
        db.session.flush()

    # Nomes de CRUD exigidos na rubrica. O comportamento transacional e os
    # métodos antigos permanecem compatíveis com o restante da aplicação.
    @classmethod
    def buscar_por_id(cls, id, bloquear=False):
        return cls.buscar(id, bloquear=bloquear)

    @classmethod
    def listar_todos(cls):
        return cls.listar()

    def salvar(self):
        db.session.add(self)
        db.session.flush()
        return self

    def deletar(self):
        self.excluir()

    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            if column.name in ('password_hash', 'token_hash', 'session_version'):
                continue
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat() + 'Z'
            elif isinstance(value, date):
                value = value.isoformat()
            elif isinstance(value, Decimal):
                value = float(value)
            elif value is not None and (column.name == 'id' or column.foreign_keys):
                value = str(value)
            result[column.name] = value
        return result
