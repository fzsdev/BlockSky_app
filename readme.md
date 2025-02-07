# Projeto de Login e Bloqueio de Usuários na Rede Social Bluesky

Este projeto é uma aplicação web que permite aos usuários fazer login e bloquear outros usuários na rede social Bluesky. A aplicação consiste em duas páginas HTML principais: uma página de login e uma página de informações de log.

## Funcionalidades

- **Página de Login**: A página de login permite que os usuários façam login na aplicação utilizando seu nome de usuário e senha de aplicativo. O campo "Service" está desabilitado e exibe a instância `bsky.social`.

- **Página Home (Aplicação)**: A página Home permite que os usuários bloqueiem perfis que utilizem uma palavra-chave específica. A interface é composta por um formulário onde o usuário pode inserir a palavra-chave desejada e um botão para bloquear as contas.

## Tecnologias Utilizadas

- HTML
- CSS
- JavaScript 
- Python
- Flask Framework

## Estrutura do Projeto

```plaintext
app/
|
├── logs/
│   ├── api_req.txt
│   ├── blocked_accounts_log.txt
│   ├── error_log.txt
│   ├── werkzeug_log.txt
static/
├── assets/
│   └── logo.svg
├── css/
│   ├── home.css
│   └── index.css
├── js/
│   ├── home.js
│   └── script.js
templates/
├── home.html
├── index.html
main.py
readme.md
requirements.txt
```

## Instalação

1. Clone o repositório para sua máquina local:

  ```bash
   git clone https://github.com/fzsdev/BlockSky_UNISA
   ```

2. Navegue até o diretório do projeto:

```
  cd BlockSky_UNISA
```

4. Crie uma ambiente e ative:

```
  python -m venv venv
```

```
source venv/bin/activate
```

3.Instale as dependências do projeto:

```
  pip install -r requirements.txt 
```

## Uso

1. Inicie o servidor:

```
 python main.py
```

2. Abra o navegador:

```
http://localhost:5000
```

---

Se precisar de mais alguma informação ou ajuste, por favor, nos avise!

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

### Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE MIT](https://opensource.org/license/MIT) para mais detalhes.

### Contato

Para mais informações, entre em contato com os desenvolvedores:

<span>[Camila S.](https://github.com/c-camila)</span> (frontend) e <span>[Felipe Z.](https://github.com/fzsdev)</span> (backend).
