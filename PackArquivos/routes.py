from urllib import request
from flask import render_template, flash, request, jsonify, redirect, url_for, make_response, send_file
from PackArquivos.forms import *
from PackArquivos.models import *
from reportlab.pdfgen import canvas
from io import BytesIO


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/gerar_pdf/<>', methods=['GET'])
def gerar_pdf():
    # Consulta ao banco de dados para obter os dados
    itens = Cadeiras.query.all()

    # Início da geração do PDF usando reportlab
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Configurações de estilos e conteúdo do PDF
    p.setFont("Helvetica", 12)
    text = "Relatório de Cadeiras:\n\n"
    for item in itens:
        text += f"Data: {item.data}\n"
        text += f"Lote: {item.lote}\n"
        text += f"Peças: {item.pecas}\n"
        text += f"Cor: {item.cor}\n"
        text += f"Quantidade Total: {item.quantidadeTotal}\n"
        text += f"Quantidade Entregue: {item.quantidadeEntregue}\n"
        text += f"Observações: {item.obs}\n\n"

    # Quebrando linhas automaticamente se o texto for longo
    p.drawString(100, 700, text)

    # Salvando o PDF
    p.showPage()
    p.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True)


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
