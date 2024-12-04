import os
import logging
from datetime import datetime
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

# Diretório base
base_dir = os.path.dirname(os.path.abspath(__file__))

# Diretório para arquivos de sessão na raiz do projeto
session_directory = os.path.join(base_dir, 'flask_session')
if not os.path.exists(session_directory):
    os.makedirs(session_directory)
app.config['SESSION_FILE_DIR'] = session_directory

Session(app)

# Configuração de logging
base_dir = os.path.dirname(os.path.abspath(__file__))

# Diretório de logs na raiz do projeto
log_directory = os.path.join(base_dir, 'logs')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Diretório para logs de posts bloqueados
log_blocked_directory = log_directory  # Usar o mesmo diretório para simplificar

# Configuração de logging para erros
logging.basicConfig(
    filename=os.path.join(log_directory, 'error_log.txt'),
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s'
)

# Configuração de logging para comunicações da API
api_logger = logging.getLogger('api_logger')
api_logger.setLevel(logging.DEBUG)
api_handler = logging.FileHandler(os.path.join(log_directory, 'api_reqs.txt'))
api_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(message)s'))
api_logger.addHandler(api_handler)

# Configuração de logging para o servidor Werkzeug
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)
werkzeug_handler = logging.FileHandler(os.path.join(log_directory, 'werkzeug_log.txt'))
werkzeug_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
werkzeug_logger.addHandler(werkzeug_handler)

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

def log_post_content(post):
    """Registra o conteúdo da postagem em um arquivo de log único."""
    try:
        # Nome do arquivo de log dentro de 'logs'
        filename = os.path.join(log_blocked_directory, 'blocked_accounts_log.txt')

        # Formata o timestamp atual
        timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

        # Cria o conteúdo do log
        author = post.author.display_name
        handle = post.author.handle
        content = post.record.text
        uri = post.uri

        # Formata o conteúdo para ter no máximo 120 caracteres por linha
        formatted_content = format_text(content, max_length=120)

        with open(filename, 'a', encoding='utf-8') as file:  # Usar 'a' para adicionar ao arquivo existente
            file.write(f"Timestamp: {timestamp}\n")
            file.write(f"Author: {author} ({handle})\n")
            for line in formatted_content:
                file.write(f"{line}\n")
            # file.write(f"URI: {uri}\n")
            file.write("______________________________________________________________________________________________\n\n")  # Adiciona uma linha em branco após a separação
    except Exception as e:
        logging.error(f"Erro ao registrar post bloqueado: {e}")

def log_blocked_post(post_content, user_handle):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{user_handle}_{timestamp}.txt"
    filepath = os.path.join(log_blocked_directory, filename)

    # Salvar o conteúdo no arquivo
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(post_content)

def format_text(text, max_length=120):
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        # Verifica se adicionar a próxima palavra ultrapassaria o limite de caracteres
        if sum(len(w) for w in current_line) + len(word) + len(current_line) > max_length:
            lines.append(' '.join(current_line))
            current_line = [word]
        else:
            current_line.append(word)

    # Adiciona a última linha
    if current_line:
        lines.append(' '.join(current_line))

    return lines

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

            # Logar o conteúdo da postagem
            log_post_content(item)

        # Exemplo de processamento de posts e bloqueio
        for post in search_response.posts:
            post_content = post['record']['text']
            user_handle = post['author']['handle']
            
            # Lógica para identificar posts que devem ser bloqueados
            if should_block_post(post_content):
                # Bloqueia a conta do usuário
                client.mute_account(account=user_handle)
                
                # Registra o post bloqueado
                log_blocked_post(post_content, user_handle)
                
                # Log adicional (opcional)
                api_logger.info(f"Usuário {user_handle} bloqueado. Post registrado em {log_blocked_directory}")

        return jsonify({
            'success': True,
            'message': f'Contas que usaram a palavra "{word}" foram bloqueadas com sucesso.',
            'blocked_accounts': blocked_accounts
        }), 200
    except Exception as e:
        app.logger.error(f"Erro ao bloquear contas: {e}")
        return jsonify({'success': False, 'message': f'Erro ao bloquear contas: {str(e)}'}), 500

def should_block_post(post_content):
    # Define your logic to determine if a post should be blocked
    # For example, check if the post content contains certain keywords
    blocked_keywords = ['spam', 'offensive']
    return any(keyword in post_content.lower() for keyword in blocked_keywords)

if __name__ == '__main__':
    app.run(debug=True)