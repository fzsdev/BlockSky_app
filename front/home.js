document.addEventListener('DOMContentLoaded', function () {
  const username = sessionStorage.getItem('username');
  if (!username) {
    alert('Você não está autenticado. Redirecionando para a página de login.');
    window.location.href = 'index.html';
    return;
  }

  document.getElementById('keyword-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const word = document.getElementById('keywords').value.trim();

    if (!word) {
      alert('Por favor, insira uma palavra-chave.');
      return;
    }

    fetch('http://127.0.0.1:5000/block_word', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ word, access_token: sessionStorage.getItem('access_token') })
    })
      .then(response => response.json())
      .then(data => {
        const infoLogDiv = document.getElementById('info-log');
        infoLogDiv.innerHTML = '';
        if (data.success) {
          data.blocked_accounts.forEach(account => {
            const accountDiv = document.createElement('div');
            accountDiv.textContent = account;
            infoLogDiv.appendChild(accountDiv);
          });
        } else {
          infoLogDiv.textContent = 'Erro ao bloquear contas.';
        }
      })
      .catch(error => {
        console.error('Erro:', error);
        alert('Ocorreu um erro ao bloquear contas. Tente novamente mais tarde.');
      });
  });
});