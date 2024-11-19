import os
import logging
from flask import Flask, request, jsonify, redirect, url_for
import requests
from atproto import Client, models
from dotenv import load_dotenv

app = Flask(__name__)

# Garantir que o diretório de log existe
log_directory = './back'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configuração de logging
logging.basicConfig(filename=os.path.join(log_directory, 'error_log.txt'), level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

# Carregar variáveis de ambiente
load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')

if not client_id or not client_secret or not redirect_uri:
    logging.error("Variáveis de ambiente CLIENT_ID, CLIENT_SECRET ou REDIRECT_URI não estão definidas.")
    print("Erro: Variáveis de ambiente CLIENT_ID, CLIENT_SECRET ou REDIRECT_URI não estão definidas.")
    exit(1)

# Inicializar cliente
client = Client(base_url='https://bsky.social')

# Função para autenticação OAuth
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Iniciar o fluxo OAuth
    auth_url = f"https://bsky.social/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope=read write"
    return redirect(auth_url)

# Função para lidar com o callback OAuth
@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return jsonify({'success': False, 'message': 'Código de autorização não fornecido.'}), 400

    # Trocar o código de autorização por um token de acesso
    token_url = "https://bsky.social/oauth/token"
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()

    if 'access_token' in token_json:
        access_token = token_json['access_token']
        return jsonify({'success': True, 'access_token': access_token})
    else:
        return jsonify({'success': False, 'message': 'Falha ao obter token de acesso.'}), 400

if __name__ == '__main__':
    app.run(debug=True)