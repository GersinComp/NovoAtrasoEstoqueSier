import io
from urllib import request
from flask import render_template, flash, request, jsonify, redirect, url_for, make_response, Response
from PackArquivos.forms import *
from PackArquivos.models import *
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/generate_pdf/<categoria>')
def generate_pdf(categoria):
    if categoria == 'cadeiras':
        items = Cadeiras.query.all()
        titulo = "Relatorio de cadeiras"
    elif categoria == 'curvados':
        items = Curvados.query.all()
        titulo = "Relatorio de curvados"

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter),
                            rightMargin=72, leftMargin=72, topMargin=0, bottomMargin=0)
    elements = []

    styles = getSampleStyleSheet()
    title = Paragraph(titulo, styles['Title'])
    elements.append(title)

    data = [['ID', 'DATA', 'LOTE', 'PEÇA', 'COR', 'OBSERVAÇÃO', 'TOTAL', 'ENTREGUE', 'FALTAM']]

    for item in items:
        data.append([item.id, item.data, item.lote, item.pecas, item.cor, item.obs, item.quantidadeTotal,
                     item.quantidadeEntregue, (item.quantidadeTotal - item.quantidadeEntregue)])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    doc.build(elements)

    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    if categoria == 'cadeiras':
        response.headers['Content-Disposition'] = 'attachment; filename=relatorio_cadeiras.pdf'
    elif categoria == 'curvados':
        response.headers['Content-Disposition'] = 'attachment; filename=relatorio_curvados.pdf'

    return response


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
        return jsonify({'success': True, 'message': f'{cadeira.pecas} foi adicionado ao atraso!'})

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
    if request.method == 'GET':
        formCadeira.data.data = cadeira.data
        formCadeira.lote.data = cadeira.lote
        formCadeira.pecas.data = cadeira.pecas
        formCadeira.cor.data = cadeira.cor
        formCadeira.obs.data = cadeira.obs
        formCadeira.quantidadeTotal.data = cadeira.quantidadeTotal
        formCadeira.quantidadeEntregue.data = cadeira.quantidadeEntregue

    elif formCadeira.validate_on_submit():
        cadeira.data = formCadeira.data.data
        cadeira.lote = formCadeira.lote.data
        cadeira.pecas = formCadeira.pecas.data
        cadeira.cor = formCadeira.cor.data
        cadeira.obs = formCadeira.obs.data
        cadeira.quantidadeTotal = formCadeira.quantidadeTotal.data
        cadeira.quantidadeEntregue = formCadeira.quantidadeEntregue.data
        db.session.commit()
        flash('Cadeira editada com sucesso!', 'alert-success')
        return redirect(url_for('listarCadeiras'))

    return render_template('cadeira.html', formCadeira=formCadeira, cadeira=cadeira)


@app.route('/Cadeira/<int:cadeira_id>/excluirCadeira', methods=['GET', 'POST'])
def excluirCadeira(cadeira_id):
    cadeira = Cadeiras.query.get(cadeira_id)
    db.session.delete(cadeira)
    db.session.commit()
    flash(f'{cadeira.pecas} excluido!', 'alert-danger')
    return redirect(url_for('listarCadeiras'))


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
        return jsonify({'success': True, 'message': f'{curvado.pecas} foi adicionado ao atraso!'})

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
    formCurvado = AtrasoCurvadosForm()
    if request.method == 'GET':
        formCurvado.data.data = curvado.data
        formCurvado.lote.data = curvado.lote
        formCurvado.pecas.data = curvado.pecas
        formCurvado.cor.data = curvado.cor
        formCurvado.obs.data = curvado.obs
        formCurvado.quantidadeTotal.data = curvado.quantidadeTotal
        formCurvado.quantidadeEntregue.data = curvado.quantidadeEntregue

    elif formCurvado.validate_on_submit():
        curvado.data = formCurvado.data.data
        curvado.lote = formCurvado.lote.data
        curvado.pecas = formCurvado.pecas.data
        curvado.cor = formCurvado.cor.data
        curvado.obs = formCurvado.obs.data
        curvado.quantidadeTotal = formCurvado.quantidadeTotal.data
        curvado.quantidadeEntregue = formCurvado.quantidadeEntregue.data
        db.session.commit()
        flash('Curvado editado com sucesso!', 'alert-success')
        return redirect(url_for('listarCurvados'))

    return render_template('Curvado.html', formCurvado=formCurvado, curvado=curvado)


@app.route('/Curvado/<int:curvado_id>/excluirCurvado', methods=['GET', 'POST'])
def excluirCurvado(curvado_id):
    curvado = Curvados.query.get(curvado_id)
    db.session.delete(curvado)
    db.session.commit()
    flash(f'{curvado.pecas} excluido!', 'alert-danger')
    return redirect(url_for('listarCurvados'))
