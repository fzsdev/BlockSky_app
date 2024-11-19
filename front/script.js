document.getElementById('login-form').addEventListener('submit', function (event) {
  event.preventDefault();

  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();

  // Validação básica
  if (!username || !password) {
    alert('Por favor, preencha todos os campos.');
    return;
  }

  // Mostrar feedback visual (opcional)
  const loginButton = document.querySelector('.login-button');
  loginButton.disabled = true;
  loginButton.textContent = 'Entrando...';

  fetch('/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, password })
  })
    .then(response => {
      loginButton.disabled = false;
      loginButton.textContent = 'Enter';
      return response.json();
    })
    .then(data => {
      if (data.success) {
        alert('Login bem-sucedido!');
        window.location.href = 'home.html'; // Redirecionar para home.html
      } else {
        alert('Falha no login. Verifique suas credenciais.');
      }
    })
    .catch(error => {
      loginButton.disabled = false;
      loginButton.textContent = 'Enter';
      console.error('Erro:', error);
      alert('Ocorreu um erro. Tente novamente mais tarde.');
    });
});