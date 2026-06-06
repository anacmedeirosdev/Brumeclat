from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.usuario import Usuario
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def landing_page():
    return render_template('landinpage.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        telefone = request.form['telefone']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(telefone=telefone).first()

        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            session['tipo'] = usuario.tipo
            session['senha'] = usuario.senha
            session['telefone'] = usuario.telefone

            if usuario.tipo == 'admin':
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('admin.dashboard'))

        flash('Telefone ou senha incorretos!', 'error')

    return render_template('login.html')

@auth_bp.route('/cliente/home')
def home():
    if 'usuario_id' not in session or session['tipo'] != 'cliente':
        return redirect(url_for('auth.login'))
    return render_template('home.html')

@auth_bp.route('/cadastro', methods=[ 'POST'])
def cadastro():
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    senha = request.form.get('senha')

    if Usuario.query.filter_by(telefone=telefone).first():
        flash('Telefone já cadastrado!', 'error')
        return redirect(url_for('auth.login'))
        
    senha_hash = generate_password_hash(senha)
    novo_usuario = Usuario(nome=nome, telefone=telefone, senha=senha_hash)
    db.session.add(novo_usuario)
    db.session.commit()

    flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
