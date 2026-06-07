from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    login_manager.login_view = 'auth.login'

    from app.routes.auth import auth_bp
    from app.routes.agendamento import agendamento_bp
    from app.routes.admin import admin_bp

    

    app.register_blueprint(auth_bp)
    app.register_blueprint(agendamento_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()

    return app
@login_manager.user_loader
def load_user(user_id): 
    from app.models.usuario import Usuario
    return Usuario.query.get(int(user_id))