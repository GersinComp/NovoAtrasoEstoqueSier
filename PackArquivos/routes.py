import os
from urllib import request
from flask import render_template, flash, redirect, request, url_for, jsonify, session
from flask_login import current_user
from PackArquivos.forms import *
from PackArquivos.models import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from num2words import num2words


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/valor_extenso', methods=['POST'])
def valor_extenso():
    data = request.json
    valor = data.get('valor', '0')
    valor = valor.replace("R$ ", "")
    if int(valor) <= 1:
        return jsonify({'valorExtenso': num2words(valor, lang='pt_BR') + " real"})
    return jsonify({'valorExtenso': num2words(valor, lang='pt_BR') + " reais"})


def criar_recibo_pdf(filename, dadosPDF):
    c = canvas.Canvas(filename, pagesize=landscape(letter))

    width, height = landscape(letter)

    # Definindo margens
    margin_x = 0.5 * inch
    margin_y = 0.7 * inch  # Reduzindo a margem superior

    # Definindo a largura e altura do retângulo
    rect_width = width - 2 * margin_x
    rect_height = height - 2 * margin_y

    # Adicionar retângulo ao redor do recibo
    c.rect(margin_x, margin_y, rect_width, rect_height)

    # Título
    c.setFont("Helvetica-Bold", 44)
    c.drawCentredString(width / 5, height - margin_y - 0.8 * inch, "RECIBO")

    # Data e local de emissão
    c.setFont("Times-Roman", 20)
    c.setFillColorRGB(0.5, 0.5, 0.5)  # Cor cinza
    c.drawRightString(width / 2.54 - 0.5 * inch, height - margin_y - 1.4 * inch, "Local e data de emissão: ")
    c.setFillColorRGB(0, 0, 0)  # Voltando para preto
    c.setFont("Helvetica", 20)
    c.drawCentredString(width / 5.20, height - margin_y - 2.5 * inch, f"Data:  {(dadosPDF['data'])}")

    # Calculando a posição para o texto "Nº"
    num_recibo_text = f"Nº {dadosPDF['numero']}"
    num_recibo_width = c.stringWidth(num_recibo_text, "Helvetica", 30)
    num_recibo_x = width - margin_x - num_recibo_width
    num_recibo_y = height - margin_y - 0.7 * inch

    # Desenhando o texto "Nº" na margem direita
    c.drawString(num_recibo_x, num_recibo_y, num_recibo_text)

    # Recebido de
    c.drawString(margin_x + 0.5 * inch, height - margin_y - 3 * inch, f"Recebi de: {dadosPDF['empresa']}")
    c.drawString(margin_x + 5.8 * inch, height - margin_y - 3 * inch,
                 f"a quantia de: {dadosPDF['valor']}")

    # Quantia por extenso
    c.drawString(margin_x + 0.5 * inch, height - margin_y - 3.5 * inch, "Quantia por extenso:")
    c.roundRect(margin_x + 0.5 * inch, height - margin_y - 4.5 * inch, 9 * inch, 0.8 * inch, 0.1 * inch)
    c.drawString(margin_x + 0.6 * inch, height - margin_y - 4.3 * inch, f"{dadosPDF['valorExtenso']}")

    # Conceito
    c.drawString(margin_x + 0.5 * inch, height - margin_y - 5 * inch,
                 f"Referente a: {dadosPDF['descricao']}")
    c.drawString(margin_x + 0.5 * inch, height - margin_y - 5.5 * inch,
                 "__________________________________________________________")

    # Nome e assinatura
    signature_text = "Nome e assinatura do recebedor"
    signature_text_width = c.stringWidth(signature_text, "Times-Roman", 14)
    signature_text_x = margin_x + (rect_width - signature_text_width) / 2
    c.setFont("Times-Roman", 18)
    c.setFillColorRGB(0.5, 0.5, 0.5)  # Cor cinza
    c.drawCentredString(width / 2, height - margin_y - 7 * inch, signature_text)
    c.setFillColorRGB(0, 0, 0)  # Voltando para preto

    # Adicionar a imagem da assinatura
    image_width = 150
    image_height = 70
    image_x = (width - image_width) / 2
    image_y = height - margin_y - 6.6 * inch
    c.drawImage("./PackArquivos/static/arquivosPDF/assinatura.png", image_x, image_y,
                width=image_width, height=image_height)

    c.line(margin_x + 2 * inch, height - margin_y - 6.6 * inch, margin_x + rect_width - 2 * inch,
           height - margin_y - 6.6 * inch)

    c.save()


def enviar_recibo(token):
    dadosPDF = session.get('dadosPDF')
    recibo = Recibo(empresa=dadosPDF['empresa'], valor=dadosPDF['valorExtenso'],
                    data=dadosPDF['data'], nome=dadosPDF['nome'],
                    cpf=dadosPDF['cpf'], descricao=dadosPDF['descricao'],
                    token=token, usuario=current_user)
    db.session.add(recibo)
    db.session.commit()


@app.route('/atrasoCadeiras', methods=['GET', 'POST'])
def atrasoCadeiras():
    formCadeiras = AtrasoCadeirasForm()

    if formCadeiras.validate_on_submit():
        cadeira = Cadeiras(data=formCadeiras.data.data, lote=formCadeiras.lote.data,
                           pecas=formCadeiras.pecas.data, cor=formCadeiras.cor.data,
                           quantidadeTotal=formCadeiras.quantidadeTotal.data,
                           quantidadeEntregue=formCadeiras.quantidadeEntregue.data,
                           obs=formCadeiras.obs.data)
        db.session.add(cadeira)
        db.session.commit()
        flash(f'{cadeira.pecas} foi adicionada ao atraso!', 'alert-success')
        redirect(url_for('atrasoCadeiras'))

    return render_template('atrasoCadeiras.html', formCadeiras=formCadeiras)


@app.route('/listarAtraso/Cadeiras', methods=['GET', 'POST'])
def listarCadeiras():
    order = request.args.get('order', 'asc')
    if order == 'desc':
        cadeiras = Cadeiras.query.order_by(Cadeiras.id.desc()).all()
    else:
        cadeiras = Cadeiras.query.order_by(Cadeiras.id.asc()).all()

    return render_template('listarCadeiras.html', cadeiras=cadeiras)


@app.route('/Cadeira/<int:cadeira_id>', methods=['GET', 'POST'], endpoint='Cadeira')
def listarCadeira(cadeira_id):
    cadeira = Cadeiras.query.get(cadeira_id)
    formCadeira = AtrasoCadeirasForm()
    return render_template('Cadeira.html', formCadeira=formCadeira, cadeira=cadeira)


@app.route('/atrasoCurvados', methods=['GET', 'POST'])
def atrasoCurvados():
    formCurvados = AtrasoCurvadosForm()

    if formCurvados.validate_on_submit():
        curvado = Curvados(data=formCurvados.data.data, lote=formCurvados.lote.data,
                           pecas=formCurvados.pecas.data, cor=formCurvados.cor.data,
                           quantidadeTotal=formCurvados.quantidadeTotal.data,
                           quantidadeEntregue=formCurvados.quantidadeEntregue.data,
                           obs=formCurvados.obs.data)
        db.session.add(curvado)
        db.session.commit()
        flash(f'{curvado.pecas} foi adicionada ao atraso!', 'alert-success')

    return render_template('atrasoCurvados.html', formCurvados=formCurvados)


@app.route('/listarAtraso/Curvados', methods=['GET', 'POST'])
def listarCurvados():
    order = request.args.get('order', 'asc')
    if order == 'desc':
        curvados = Curvados.query.order_by(Curvados.id.desc()).all()
    else:
        curvados = Curvados.query.order_by(Curvados.id.asc()).all()

    return render_template('listarCurvados.html', curvados=curvados)


@app.route('/Curvado/<int:curvado_id>', methods=['GET', 'POST'], endpoint='Curvado')
def listarCurvado(curvado_id):
    curvado = Curvados.query.get(curvado_id)
    return render_template('Curvado.html', curvado=curvado)


