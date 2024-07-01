from datetime import datetime
from pytz import timezone
from PackArquivos import app, db


def horarioCriado():
    # Define o fuso horário de Brasília
    brasilia_timezone = timezone('America/Sao_Paulo')

    # Obtém a data e hora atual em Brasília
    return datetime.now(brasilia_timezone).strftime('%Y/%m/%d')


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
