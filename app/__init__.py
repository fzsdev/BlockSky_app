from flask import Flask
from .views import views
from .models import db


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "your_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://username:password@localhost/dbname"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(views)

    with app.app_context():
        db.create_all()

    return app
