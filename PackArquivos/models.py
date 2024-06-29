import secrets
from datetime import datetime
from pytz import timezone
from PackArquivos import app, db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(id_usuario)


def horarioCriado():
    # Define o fuso horário de Brasília
    brasilia_timezone = timezone('America/Sao_Paulo')

    # Obtém a data e hora atual em Brasília
    return datetime.now(brasilia_timezone).strftime('%Y-%m-%d-%H-%M-%S')


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), nullable=False)
    sobrenome = db.Column(db.String(80), nullable=False)
    nascimento = db.Column(db.Date, nullable=False, default="0001-01-01")
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(11), nullable=False)
    senha = db.Column(db.String(80), nullable=False)
    foto_perfil = db.Column(db.String(80), default='default.jpg')
    recibo = db.relationship('Recibo', backref='usuario', lazy=True)


class Recibo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.String(80), nullable=False)
    valor = db.Column(db.String(80), nullable=False)
    data = db.Column(db.Date, nullable=False, default=horarioCriado)
    nome = db.Column(db.String(80), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    descricao = db.Column(db.Text(), nullable=False)
    token = db.Column(db.String(8), nullable=False, default=secrets.token_hex(4))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)


class Cadeiras(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False, default=horarioCriado)
    lote = db.Column(db.Integer)
    pecas = db.Column(db.String(80), nullable=False, default="Undefined")
    cor = db.Column(db.String(80), nullable=False, default="Undefined")
    quantidadeTotal = db.Column(db.Integer, nullable=False, default=0)
    quantidadeEntregue = db.Column(db.Integer, default=0)
    obs = db.Column(db.Text(), default="-")


class Curvados(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False, default=horarioCriado)
    lote = db.Column(db.Integer)
    pecas = db.Column(db.String(80), nullable=False, default="Undefined")
    cor = db.Column(db.String(80), nullable=False, default="Undefined")
    quantidadeTotal = db.Column(db.Integer, nullable=False, default=0)
    quantidadeEntregue = db.Column(db.Integer, default=0)
    obs = db.Column(db.Text(), default="-")


with app.app_context():
    db.create_all()
