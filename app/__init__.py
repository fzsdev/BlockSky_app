from flask import Flask
from .views import views
from .models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    app.register_blueprint(views)

    return app
