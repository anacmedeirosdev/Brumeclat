from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.agendamento import agendamento_bp
    from app.routes.admin import admin_bp


    app.register_blueprint(auth_bp)
    app.register_blueprint(agendamento_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()

    return app