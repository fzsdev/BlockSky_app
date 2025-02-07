import os
import logging
from datetime import datetime


def setup_logging(base_dir):
    log_directory = os.path.join(base_dir, "app", "logs")
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    logging.basicConfig(
        filename=os.path.join(log_directory, "error_log.txt"),
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s:%(message)s",
    )

    api_logger = logging.getLogger("api_logger")
    api_logger.setLevel(logging.DEBUG)
    api_handler = logging.FileHandler(os.path.join(log_directory, "api_reqs.txt"))
    api_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s:%(message)s"))
    api_logger.addHandler(api_handler)

    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(logging.INFO)
    werkzeug_handler = logging.FileHandler(
        os.path.join(log_directory, "werkzeug_log.txt")
    )
    werkzeug_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    )
    werkzeug_logger.addHandler(werkzeug_handler)

    logging.getLogger("werkzeug").propagate = False

    # Configuração do logger para routes
    routes_logger = logging.getLogger("routes_logger")
    routes_logger.setLevel(logging.DEBUG)
    routes_handler = logging.FileHandler(os.path.join(log_directory, "routes_log.txt"))
    routes_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s:%(message)s")
    )
    routes_logger.addHandler(routes_handler)


def format_text(text, max_length=120):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 > max_length:
            lines.append(current_line)
            current_line = word
        else:
            if current_line:
                current_line += " "
            current_line += word
    if current_line:
        lines.append(current_line)
    return lines


def log_post_content(post, log_directory):
    """Registra o conteúdo da postagem em um arquivo de log único."""
    try:
        # Nome do arquivo de log dentro de 'logs'
        filename = os.path.join(log_directory, "blocked_accounts_log.txt")

        # Formata o timestamp atual
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # Cria o conteúdo do log
        author = post.author.display_name
        handle = post.author.handle
        content = post.record.text
        uri = post.uri

        # Formata o conteúdo para ter no máximo 120 caracteres por linha
        formatted_content = format_text(content, max_length=120)

        with open(
            filename, "a", encoding="utf-8"
        ) as file:  # Usar 'a' para adicionar ao arquivo existente
            file.write(f"Timestamp: {timestamp}\n")
            file.write(f"Author: {author} ({handle})\n")
            for line in formatted_content:
                file.write(f"{line}\n")
            # file.write(f"URI: {uri}\n")
            file.write(
                "______________________________________________________________________________________________\n\n"
            )  # Adiciona uma linha em branco após a separação
    except Exception as e:
        logging.error(f"Erro ao registrar post bloqueado: {e}")


def log_blocked_word(word, log_directory):
    """Registra a palavra bloqueada em um arquivo de log único."""
    try:
        # Nome do arquivo de log dentro de 'logs'
        filename = os.path.join(log_directory, "blocked_accounts_log.txt")

        # Formata o timestamp atual
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        with open(
            filename, "a", encoding="utf-8"
        ) as file:  # Usar 'a' para adicionar ao arquivo existente
            file.write(f"Timestamp: {timestamp}\n")
            file.write(f"Blocked Word: {word}\n")
            file.write(
                "______________________________________________________________________________________________\n\n"
            )  # Adiciona uma linha em branco após a separação
    except Exception as e:
        logging.error(f"Erro ao registrar palavra bloqueada: {e}")
