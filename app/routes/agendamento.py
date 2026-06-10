from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.agendamento import Agendamento
from flask_login import login_required, current_user
from app import db
from datetime import datetime

agendamento_bp = Blueprint('agendamento', __name__)

@agendamento_bp.route('/agendar', methods=['GET', 'POST'])
def fazer_agendamento():
    if request.method == 'POST':
        servico = request.form.get('servico')
        data = request.form.get('data')
        horario = request.form.get('horario')

        data = datetime.strptime(data, '%Y-%m-%d').date()
        horario = datetime.strptime(horario, '%H:%M').time()

        novo_agendamento = Agendamento(
            usuario_id=current_user.id,
            servico=servico,
            data=data,
            horario=horario,
            status='pendente'
        )

        db.session.add(novo_agendamento)
        db.session.commit()

        return redirect(url_for('agendamento.confirmacao'))

    servico_selecionado = request.args.get('servico', '')
    return render_template('agendar.html', servico_selecionado=servico_selecionado)


@agendamento_bp.route('/cliente/confirmacao')
@login_required
def confirmacao():
    return render_template('confirmacao.html')

@agendamento_bp.route('/cliente/historico')
def historico():
    meus_agendamentos = Agendamento.query.filter_by(usuario_id=current_user.id).all()
    return render_template('historico.html', agendamentos=meus_agendamentos)

