from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.usuario import Usuario
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def landing_page():
    return render_template('landingpage.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        telefone = request.form['telefone']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(telefone=telefone).first()

        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)

            if usuario.tipo == 'admin':
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('admin.dashboard'))

        flash('Telefone ou senha incorretos!', 'error')

    return redirect(url_for('auth.home'))

@auth_bp.route('/cliente/home')
@login_required
def home():
    if not current_user.is_authenticated or current_user.tipo != 'cliente':
        return redirect(url_for('auth.login'))
    return render_template('home.html')

@auth_bp.route('/cliente/perfil')
@login_required
def perfil():
    if not current_user.is_authenticated or current_user.tipo != 'cliente':
        return redirect(url_for('auth.login'))
    return render_template('perfil.html')

@auth_bp.route('/cadastro', methods=[ 'GET','POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')

        if senha != confirmar_senha:
            flash('As senhas não coincidem!', 'error')
            return render_template('cadastro.html')

        if Usuario.query.filter_by(telefone=telefone).first():
            flash('Telefone já cadastrado!', 'error')
            return redirect(url_for('auth.login'))
        
        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(nome=nome, telefone=telefone, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template ('cadastro.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
