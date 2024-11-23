import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from atproto import Client
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas as rotas

# Garantir que o diretório de log existe
log_directory = './back'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configuração de logging
logging.basicConfig(filename=os.path.join(log_directory, 'error_log.txt'), level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

# Carregar variáveis de ambiente
load_dotenv()

# Função para autenticação usando App Password
def authenticate(username, password):
    client = Client(base_url='https://bsky.social')
    try:
        logging.debug(f"Tentando autenticar usuário: {username}")
        client.login(username, password)
        logging.debug(f"Autenticação bem-sucedida para o usuário: {username}")
        return True
    except Exception as e:
        logging.error(f"Erro na autenticação para o usuário {username}: {e}")
        return False

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    logging.debug(f"Recebido pedido de login para o usuário: {username}")

    if authenticate(username, password):
        logging.debug(f"Login bem-sucedido para o usuário: {username}")
        return jsonify({'success': True})
    else:
        logging.debug(f"Falha no login para o usuário: {username}")
        return jsonify({'success': False}), 401

# Função para buscar postagens por uma palavra-chave
@app.route('/search_posts', methods=['POST'])
def search_posts():
    data = request.get_json()
    keyword = data.get('keyword')
    with_hashtag = data.get('with_hashtag', False)
    access_token = data.get('access_token')

    if not keyword or not access_token:
        logging.debug("Palavra-chave e token de acesso são necessários.")
        return jsonify({'success': False, 'message': 'Palavra-chave e token de acesso são necessários.'}), 400

    client = Client(base_url='https://bsky.social', access_token=access_token)
    try:
        query = f"#{keyword}" if with_hashtag else keyword
        params = {
            'q': query,
            'limit': 100
        }
        response = client.app.bsky.feed.search_posts(params)
        logging.debug(f"Postagens encontradas: {response}")
        return jsonify({'success': True, 'posts': response})
    except Exception as e:
        logging.error(f"Erro ao buscar postagens: {e}")
        return jsonify({'success': False, 'message': 'Erro ao buscar postagens.'}), 500

# Função para bloquear palavras
@app.route('/block_word', methods=['POST'])
def block_word():
    data = request.get_json()
    word = data.get('word')
    access_token = data.get('access_token')

    if not word or not access_token:
        logging.debug("Palavra e token de acesso são necessários.")
        return jsonify({'success': False, 'message': 'Palavra e token de acesso são necessários.'}), 400

    client = Client(base_url='https://bsky.social', access_token=access_token)
    try:
        # Implementar a lógica para bloquear a palavra
        # Exemplo: adicionar a palavra a uma lista de bloqueio no banco de dados
        # Aqui você pode adicionar a lógica específica para bloquear a palavra
        logging.debug(f"Bloqueando a palavra: {word}")
        return jsonify({'success': True, 'message': f'Palavra "{word}" bloqueada com sucesso.'})
    except Exception as e:
        logging.error(f"Erro ao bloquear palavra: {e}")
        return jsonify({'success': False, 'message': 'Erro ao bloquear palavra.'}), 500

if __name__ == '__main__':
    app.run(debug=True)