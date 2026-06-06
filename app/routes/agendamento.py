from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.agendamento import Agendamento
from app import db

agendamento_bp = Blueprint('agendamento', __name__)

@agendamento_bp.route('/agendamento', methods=['GET', 'POST'])
def dashboard():
    if 'usuario_id' not in session or session['tipo'] != 'cliente':
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        servico = request.form['servico']
        data = request.form['data']
        horario = request.form['horario']

        novo_agendamento = Agendamento(
            usuario_id=session['usuario_id'],
            servico=servico,
            data=data,
            horario=horario
        )
        db.session.add(novo_agendamento)
        db.session.commit()

        flash('Agendamento realizado com sucesso!', 'success')
        return redirect(url_for('agendamento.dashboard'))
    
    meus_agendamentos = Agendamento.query.filter_by(usuario_id=session['usuario_id']).all()
    return render_template('historico.html', agendamentos=meus_agendamentos)

@agendamento_bp.route('/cliente/confirmacao')
def confirmacao():
    render_template('confirmacao.html')

@agendamento_bp.route('/cliente/historico')
def historico():
    meus_agendamentos = Agendamento.query.filter_by(usuario_id=session['usuario_id']).all()
    return render_template('historico.html', agendamentos=meus_agendamentos)
