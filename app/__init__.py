from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "supersecretkey"  # Troque por uma chave secreta segura

    # Importar e registrar os blueprints
    from .views import views

    app.register_blueprint(views, url_prefix="/")

    return app
