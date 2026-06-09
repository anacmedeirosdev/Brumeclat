from app import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), unique=True, nullable=False)
    senha = db.Column(db.String(300), nullable=False)
    tipo = db.Column(db.String(20), default='cliente', nullable=False)

    agendamento = db.relationship('Agendamento', backref='cliente', lazy=True)