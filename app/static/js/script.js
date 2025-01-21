document.addEventListener('DOMContentLoaded', function () {
  const loginButton = document.getElementById('login-button');
  const usernameInput = document.getElementById('username');
  const passwordInput = document.getElementById('password');
  const loadingElement = document.getElementById('loading');
  const loginContainer = document.querySelector('.login-container');

  loginButton.addEventListener('click', async function () {
    // Mostrar o elemento de "loading" e adicionar a classe de desfoque ao login-container
    loadingElement.style.display = 'flex';
    loginContainer.classList.add('blur-background');

    // Capturar os dados dos campos username e password
    const username = usernameInput.value;
    const password = passwordInput.value;

    // Criar o objeto JSON com os dados capturados
    const loginData = {
      username: username,
      password: password
    };

    console.log('Login Data:', loginData);

    try {
      // Enviar a requisição POST ao backend
      const response = await fetch('/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(loginData)
      });

      console.log('Response Status:', response.status);

      const data = await response.json();

      console.log('Response Data:', data);

      // Tratar a resposta do servidor
      if (response.ok && data.success) {
        // Redirecionar para a página home.html
        window.location.href = '/home';
      } else {
        console.error('Erro ao realizar login:', data.message);
        alert('Usuário e senha incorretos.');
      }
    } catch (error) {
      console.error('Erro ao realizar login:', error);
      alert('Erro ao realizar login. Por favor, tente novamente.');
    } finally {
      // Esconder o elemento de "loading" e remover a classe de desfoque do login-container
      loadingElement.style.display = 'none';
      loginContainer.classList.remove('blur-background');
    }
  });

  // Adicionar evento de escuta para a tecla "Enter" nos campos de entrada
  [usernameInput, passwordInput].forEach(input => {
    input.addEventListener('keydown', function (event) {
      if (event.key === 'Enter') {
        event.preventDefault(); // Impede o comportamento padrão
        loginButton.click(); // Aciona o clique no botão
      }
    });
  });
});