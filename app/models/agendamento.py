from app import db
from datetime import datetime
class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    servico = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Date, nullable=False)
    horario = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='pendente', nullable=False)

