from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from PackArquivos.models import *
from datetime import date

with app.app_context():
    recibos = Recibo.query.all()
proximoRecibo = len(recibos) + 1


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar_dados = BooleanField('Manter Acesso?')
    submitLogin = SubmitField('Login')


class CriarContaForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    nascimento = DateField('Nascimento', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    confirmar_email = StringField('Confirmar e-mail', validators=[DataRequired(), EqualTo('email')])
    telefone = StringField('Telefone', validators=[DataRequired(), Length(min=11, max=11)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmar_senha = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('senha')])
    submitCriarConta = SubmitField('Crie sua conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar.")


class GerarReciboForm(FlaskForm):
    empresa = StringField('Empresa', validators=[DataRequired()])
    numero = StringField('Numero', validators=[DataRequired()], render_kw={'readonly': True, "value": proximoRecibo})
    valor = StringField('Valor', validators=[DataRequired()], render_kw={"value": "R$ "})
    valorExtenso = StringField('Valor Extenso', validators=[DataRequired()], render_kw={'readonly': True})
    data = DateField('Data', validators=[DataRequired()], render_kw={"value": date.today().strftime("%Y-%m-%d")})
    nome = StringField('Nome', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired(), Length(11, 11)])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    submitRecibo = SubmitField('Gerar recibo')
    clearRecibo = SubmitField('Limpar recibo')
    limparAssinatura = SubmitField('Limpar assinatura')
    salvarRecibo = SubmitField('Salvar recibo')
    voltarRecibo = SubmitField('Voltar ao formulário')


class AtrasoCadeirasForm(FlaskForm):
    data = DateField('Data', validators=[DataRequired()], render_kw={"value": date.today().strftime("%Y-%m-%d")})
    lote = IntegerField('Lote', validators=[DataRequired()])
    pecas = StringField('Peças', validators=[DataRequired()])
    cor = StringField('cor', validators=[DataRequired()])
    quantidadeTotal = IntegerField('Quantidade total', validators=[DataRequired()])
    quantidadeEntregue = IntegerField('Quantidade entregue', render_kw={"value": 0})
    obs = TextAreaField('OBSERVAÇÃO')
    submitAtraso = SubmitField('Adicionar')


class AtrasoCurvadosForm(FlaskForm):
    data = DateField('Data', validators=[DataRequired()], render_kw={"value": date.today().strftime("%Y-%m-%d")})
    lote = IntegerField('Lote', validators=[DataRequired()])
    pecas = StringField('Peças', validators=[DataRequired()])
    cor = StringField('cor', validators=[DataRequired()])
    quantidadeTotal = IntegerField('Quantidade total', validators=[DataRequired()])
    quantidadeEntregue = IntegerField('Quantidade entregue', render_kw={"value": 0})
    obs = TextAreaField('OBSERVAÇÃO')
    submitAtraso = SubmitField('Adicionar')


