from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_cors import CORS
from flask_talisman import Talisman
from dotenv import load_dotenv
import os
from datetime import timedelta

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar o banco de dados
db = SQLAlchemy()
migrate = Migrate()

# Configuração de segurança do Talisman
csp = {
    "default-src": [
        "'self'",
        "https://stackpath.bootstrapcdn.com",  # Exemplo de CDN permitida
        "https://blocksky-app-3d752ea35673.herokuapp.com",
        "https://blocksky.social",
    ],
    "script-src": [
        "'self'",
        "'unsafe-inline'",  # Permitir scripts inline
    ],
    "style-src": [
        "'self'",
        "'unsafe-inline'",  # Permitir estilos inline
    ],
    "connect-src": [
        "'self'",
        "https://blocksky-app-3d752ea35673.herokuapp.com",
        "https://blocksky.social",
    ],
}


def create_app():
    app = Flask(__name__)

    # Configurações do app
    app.config.from_object("config.Config")
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_PERMANENT"] = True
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)
    app.config["SESSION_FILE_DIR"] = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "flask_session"
    )
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecretkey")

    # Importante para cookies cross-site
    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_SECURE"] = False  # Em produção, usar True com HTTPS

    # Criar diretório de logs se não existir
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)
    Session(app)
    CORS(app, supports_credentials=True)
    Talisman(app, content_security_policy=csp)  # Configurar Talisman com CSP

    # Registrar blueprints (rotas)
    from .routes import routes
    from .auth import auth
    from .views import views

    app.register_blueprint(routes)
    app.register_blueprint(auth)
    app.register_blueprint(views)

    return app
