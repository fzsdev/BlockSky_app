document.getElementById('login-form').addEventListener('submit', function (event) {
  event.preventDefault();

  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();

  // Validação básica
  if (!username || !password) {
    alert('Por favor, preencha todos os campos.');
    return;
  }

  console.log(`Tentando autenticar usuário: ${username}`);

  // Mostrar feedback visual (opcional)
  const loginButton = document.querySelector('.login-button');
  loginButton.disabled = true;
  loginButton.textContent = 'Entrando...';

  fetch('http://127.0.0.1:5000/login', {  // Certifique-se de que o URL está correto
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, password })
  })
    .then(response => {
      console.log('Resposta recebida do backend:', response);
      if (!response.ok) {
        throw new Error('Erro na resposta do servidor');
      }
      return response.json();
    })
    .then(data => {
      loginButton.disabled = false;
      loginButton.textContent = 'Entrar';
      console.log('Dados recebidos do backend:', data);
      if (data.success) {
        console.log('Login bem-sucedido!');
        alert('Login bem-sucedido!');
        // Armazenar tokens na sessão do navegador
        sessionStorage.setItem('access_token', data.access_token);
        sessionStorage.setItem('refresh_token', data.refresh_token);
        window.location.href = 'home.html'; // Redirecionar para home.html
      } else {
        console.log('Falha no login. Verifique suas credenciais.');
        alert(`Falha no login: ${data.message}`);
      }
    })
    .catch(error => {
      loginButton.disabled = false;
      loginButton.textContent = 'Entrar';
      console.error('Erro:', error);
      alert('Ocorreu um erro. Tente novamente mais tarde.');
    });
});