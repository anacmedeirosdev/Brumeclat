from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.agendamento import Agendamento
from flask_login import login_required, current_user
from app import db

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin/dashboard')
@login_required
def dashboard():
    if not current_user.is_authenticated or current_user.tipo != 'admin':
        return redirect(url_for('auth.login'))
    todos = Agendamento.query.all()
    total_pendentes = Agendamento.query.filter_by(status='pendente').count()
    total_concluidos = Agendamento.query.filter_by(status='concluido').count()
    total_cancelados = Agendamento.query.filter_by(status='cancelado').count()

    return render_template(
        'admin_dashboard.html', 
        agendamentos=todos,
        pendentes=total_pendentes,
        concluidos=total_concluidos,
        cancelados=total_cancelados
    )

@admin_bp.route('/admin/alterar/<int:id>', methods=['POST'])
def alterar_status(id):
    if not current_user.is_authenticated or current_user.tipo != 'admin':
        return redirect(url_for('auth.login'))
    
    agendamento = Agendamento.query.get_or_404(id)
    novo_status = request.form.get('status') 
    agendamento.status = novo_status
    db.session.commit()

    return redirect(url_for('admin.dashboard'))

