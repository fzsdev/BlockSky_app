import os
import logging
from flask import Blueprint, request, session, jsonify
from atproto import Client, models, SessionEvent, Session as AtprotoSession
from .utils import log_post_content, log_blocked_word

routes = Blueprint("routes", __name__)

# Diretório base
base_dir = os.path.dirname(os.path.abspath(__file__))

# Diretório para logs de posts bloqueados
log_blocked_directory = os.path.join(base_dir, "logs")
if not os.path.exists(log_blocked_directory):
    os.makedirs(log_blocked_directory)

# Configuração de logging
logger = logging.getLogger("routes_logger")


def init_client(session_string: str = None) -> Client:
    client = Client()
    client.on_session_change(on_session_change)

    if session_string:
        logger.debug("Reusing session")
        client.login(session_string=session_string)
    else:
        logger.debug("No session found")
        # Não fazemos login aqui, pois os dados virão do frontend

    return client


def on_session_change(event: SessionEvent, session_obj: AtprotoSession) -> None:
    logger.debug(f"Session changed: {event}, {repr(session_obj)}")
    if event in (SessionEvent.CREATE, SessionEvent.REFRESH):
        logger.debug("Saving changed session")
        save_session(session_obj.export())


def save_session(session_string: str) -> None:
    session["session_string"] = session_string


@routes.route("/block_word", methods=["POST"])
def block_word_route():
    # Debug da sessão
    print("Session data:", dict(session))
    session_string = session.get("session_string")
    print("Session string:", session_string[:30] if session_string else None)

    if not session_string:
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Sessão expirada. Por favor, faça login novamente.",
                }
            ),
            401,
        )

    try:
        data = request.get_json()
        word = data.get("word")

        if not word:
            return jsonify({"success": False, "message": "Palavra inválida"}), 400

        client = init_client(session_string)

        # Procurar por postagens contendo a palavra
        params = {"q": word, "limit": 10}
        search_response = client.app.bsky.feed.search_posts(params)

        # Adicionar log para inspecionar a estrutura da resposta
        logger.debug(f"search_response: {search_response}")

        # Verificar a estrutura da resposta
        if not hasattr(search_response, "posts"):
            raise ValueError("A resposta não contém o atributo 'posts'")

        # Lista para armazenar as contas bloqueadas
        blocked_accounts = []

        # Iterar pelas postagens encontradas e bloquear os autores
        for item in search_response.posts:
            author_did = item.author.did
            # Criar o registro de bloqueio
            block_record = models.AppBskyGraphBlock.Record(
                subject=author_did, created_at=client.get_current_time_iso()
            )
            uri = client.app.bsky.graph.block.create(client.me.did, block_record).uri
            blocked_accounts.append(author_did)

            # Logar o conteúdo da postagem
            log_post_content(item, log_blocked_directory)

        if blocked_accounts:
            # Registrar a palavra bloqueada
            log_blocked_word(word, log_blocked_directory)

            return (
                jsonify(
                    {
                        "success": True,
                        "message": f'Contas que usaram a palavra "{word}" foram bloqueadas com sucesso.',
                        "blocked_accounts": blocked_accounts,
                    }
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "success": True,
                        "message": f'Nenhuma conta encontrada usando a palavra "{word}".',
                    }
                ),
                200,
            )
    except Exception as e:
        print("Erro na rota block_word:", str(e))
        return (
            jsonify(
                {"success": False, "message": f"Erro ao bloquear contas: {str(e)}"}
            ),
            500,
        )


@routes.route("/get_log", methods=["GET"])
def get_log_route():
    if "session_string" not in session:
        return (
            jsonify(
                {"success": False, "message": "Sessão expirada. Faça login novamente."}
            ),
            401,
        )

    try:
        log_file_path = os.path.join(log_blocked_directory, "blocked_accounts_log.txt")

        # Criar arquivo se não existir
        if not os.path.exists(log_file_path):
            with open(log_file_path, "w", encoding="utf-8") as f:
                f.write("")

        with open(log_file_path, "r", encoding="utf-8") as file:
            log_content = file.read()
        return jsonify({"success": True, "log": log_content}), 200
    except Exception as e:
        logger.error(f"Erro ao ler o arquivo de log: {e}")
        return (
            jsonify(
                {"success": False, "message": f"Erro ao ler o arquivo de log: {str(e)}"}
            ),
            500,
        )
