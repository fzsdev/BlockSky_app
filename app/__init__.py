from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar o banco de dados
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Configurações do app
    app.config.from_object("config.Config")
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_FILE_DIR"] = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "flask_session"
    )
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecretkey")

    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)
    Session(app)
    CORS(
        app, supports_credentials=True
    )  # Adicionar esta linha para configurar Flask-CORS

    # Registrar blueprints (rotas)
    from .routes import routes
    from .auth import auth
    from .views import views

    app.register_blueprint(routes)
    app.register_blueprint(auth)
    app.register_blueprint(views)

    return app
