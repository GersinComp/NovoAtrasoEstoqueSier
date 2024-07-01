from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired
from datetime import date


class AtrasoCadeirasForm(FlaskForm):
    data = DateField('Data', validators=[DataRequired()],
                     render_kw={"value": date.today().strftime("%Y-%m-%d")})
    lote = IntegerField('Lote', validators=[DataRequired()])
    pecas = StringField('Peças', validators=[DataRequired()])
    cor = StringField('cor', validators=[DataRequired()])
    quantidadeTotal = IntegerField('Quantidade total', validators=[DataRequired()])
    quantidadeEntregue = IntegerField('Quantidade entregue', default=0)
    obs = TextAreaField('OBSERVAÇÃO')
    submitAtraso = SubmitField('Adicionar')
    editarAtraso = SubmitField('Salvar alterações')


class AtrasoCurvadosForm(FlaskForm):
    data = DateField('Data', validators=[DataRequired()],
                     render_kw={"value": date.today().strftime("%Y-%m-%d")})
    lote = IntegerField('Lote', validators=[DataRequired()])
    pecas = StringField('Peças', validators=[DataRequired()])
    cor = StringField('cor', validators=[DataRequired()])
    quantidadeTotal = IntegerField('Quantidade total', validators=[DataRequired()])
    quantidadeEntregue = IntegerField('Quantidade entregue', default=0)
    obs = TextAreaField('OBSERVAÇÃO')
    submitAtraso = SubmitField('Adicionar')
    editarAtraso = SubmitField('Salvar alterações')

