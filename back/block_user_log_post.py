import requests
from atproto import Client, models
from dotenv import load_dotenv
import os
import logging

# Configuração de logging
logging.basicConfig(filename='./back/error_log.txt', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

# Carregar variáveis de ambiente
load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

if not username or not password:
    logging.error("Variáveis de ambiente USERNAME ou PASSWORD não estão definidas.")
    print("Erro: Variáveis de ambiente USERNAME ou PASSWORD não estão definidas.")
    exit(1)

# Inicializar cliente
client = Client(base_url='https://bsky.social')

# Função para autenticação
def authenticate():
    try:
        client.login(username, password)
        print("Autenticado com sucesso!")
    except Exception as e:
        logging.error(f"Erro na autenticação: {e}")
        print("Falha na autenticação. Verifique os logs para mais detalhes.")
        exit(1)

# Função para buscar postagens por uma palavra-chave
# Função para buscar postagens por uma palavra-chave
def search_posts(client, keyword, with_hashtag=False):
    try:
        query = f"#{keyword}" if with_hashtag else keyword  # Adiciona o # se necessário
        params = models.app.bsky.feed.search_posts.Params(
            q=query,  # Passa a palavra-chave para pesquisa.
            limit=100  # Limite para evitar grandes volumes de dados, o padrão é 25.
        )
        response = client.app.bsky.feed.search_posts(params)
        if response.status_code == 429:
            logging.error("Limite de taxa atingido. Tente novamente mais tarde.")
            print("Erro: Limite de taxa atingido. Tente novamente mais tarde.")
            return None
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"Erro HTTP ao buscar postagens: {http_err}")
        print("Falha ao buscar postagens. Verifique os logs para mais detalhes.")
        return None
    except Exception as e:
        logging.error(f"Erro ao buscar postagens: {e}")
        print("Falha ao buscar postagens. Verifique os logs para mais detalhes.")
        return None

# Função para inicializar o cliente HTTP endurecido
def create_hardened_http_client():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'BlockSky_UNISA/1.0',
        'Accept': 'application/json',
    })
    return session

# Autenticar
authenticate()

# Exemplo de uso da função search_posts
keyword = "example"
posts = search_posts(client, keyword)
if posts:
    print(f"Encontradas {len(posts)} postagens com a palavra-chave '{keyword}'.")
else:
    print("Nenhuma postagem encontrada ou erro na busca.")