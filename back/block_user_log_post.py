import os
import logging
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
from atproto import Client, models, SessionEvent, Session as AtprotoSession
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas as rotas

# Configuração de Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'supersecretkey'  # Troque por uma chave secreta segura
Session(app)

# Configuração de logging
log_directory = './'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configuração de logging para erros
logging.basicConfig(filename=os.path.join(log_directory, 'back/error_log.txt'), level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

# Configuração de logging para comunicações da API
api_logger = logging.getLogger('api_logger')
api_logger.setLevel(logging.DEBUG)
api_handler = logging.FileHandler(os.path.join(log_directory, 'back/api_reqs.txt'))
api_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(message)s'))
api_logger.addHandler(api_handler)

# Função para obter a sessão persistente
def get_session() -> str:
    return session.get('session_string')

# Função para salvar a sessão persistente
def save_session(session_string: str) -> None:
    session['session_string'] = session_string

# Função para lidar com mudanças na sessão
def on_session_change(event: SessionEvent, session_obj: AtprotoSession) -> None:
    api_logger.debug(f'Session changed: {event}, {repr(session_obj)}')
    if event in (SessionEvent.CREATE, SessionEvent.REFRESH):
        api_logger.debug('Saving changed session')
        save_session(session_obj.export())

# Inicializar o cliente
def init_client(session_string: str = None) -> Client:
    client = Client()
    client.on_session_change(on_session_change)

    if session_string:
        api_logger.debug('Reusing session')
        client.login(session_string=session_string)
    else:
        api_logger.debug('No session found')
        # Não fazemos login aqui, pois os dados virão do frontend

    return client

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    app_password = data.get('password')

    if not username or not app_password:
        return jsonify({'success': False, 'message': 'Usuário e App Password são necessários.'}), 400

    try:
        client = Client()
        client.login(username, app_password)
        # Armazenar informações na sessão
        session['handle'] = client.me.handle
        session['did'] = client.me.did
        session['session_string'] = client.export_session_string()

        return jsonify({'success': True, 'message': 'Login realizado com sucesso.'}), 200
    except Exception as e:
        app.logger.error(f"Erro na autenticação: {e}")
        return jsonify({'success': False, 'message': f'Falha na autenticação: {str(e)}'}), 401

@app.route('/block_word', methods=['POST'])
def block_word():
    if 'session_string' not in session:
        return jsonify({'success': False, 'message': 'Usuário não autenticado.'}), 401

    data = request.get_json()
    word = data.get('word')

    if not word:
        return jsonify({'success': False, 'message': 'A palavra a ser bloqueada é necessária.'}), 400

    try:
        client = init_client(session.get('session_string'))

        # Procurar por postagens contendo a palavra
        params = {
            'q': word,
            'limit': 10
        }
        search_response = client.app.bsky.feed.search_posts(params)

        # Adicionar log para inspecionar a estrutura da resposta
        app.logger.debug(f"search_response: {search_response}")

        # Verificar a estrutura da resposta
        if not hasattr(search_response, 'posts'):
            raise ValueError("A resposta não contém o atributo 'posts'")

        # Lista para armazenar as contas bloqueadas
        blocked_accounts = []

        # Iterar pelas postagens encontradas e bloquear os autores
        for item in search_response.posts:
            author_did = item.author.did
            # Criar o registro de bloqueio
            block_record = models.AppBskyGraphBlock.Record(
                subject=author_did,
                created_at=client.get_current_time_iso()
            )
            uri = client.app.bsky.graph.block.create(client.me.did, block_record).uri
            blocked_accounts.append(author_did)

        return jsonify({
            'success': True,
            'message': f'Contas que usaram a palavra "{word}" foram bloqueadas com sucesso.',
            'blocked_accounts': blocked_accounts
        }), 200
    except Exception as e:
        app.logger.error(f"Erro ao bloquear contas: {e}")
        return jsonify({'success': False, 'message': f'Erro ao bloquear contas: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)