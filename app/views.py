from flask import Blueprint, render_template, request, jsonify, session
from atproto import Client, models, SessionEvent, Session as AtprotoSession

views = Blueprint("views", __name__)


@views.route("/")
def index():
    return render_template("index.html")


@views.route("/home")
def home():
    return render_template("home.html")


@views.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    app_password = data.get("password")

    if not username or not app_password:
        return (
            jsonify(
                {"success": False, "message": "Usuário e App Password são necessários."}
            ),
            400,
        )

    try:
        client = Client()
        client.login(username, app_password)
        # Armazenar informações na sessão
        session["handle"] = client.me.handle
        session["did"] = client.me.did
        session["session_string"] = client.export_session_string()

        return (
            jsonify({"success": True, "message": "Login realizado com sucesso."}),
            200,
        )
    except Exception as e:
        return (
            jsonify({"success": False, "message": f"Falha na autenticação: {str(e)}"}),
            401,
        )
