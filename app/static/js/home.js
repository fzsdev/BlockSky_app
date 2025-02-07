document.addEventListener('DOMContentLoaded', function () {
  const keywordForm = document.getElementById('keyword-form');
  const keywordInput = document.getElementById('keywords');
  const keywordButton = document.querySelector('.keyword-button');

  keywordForm.addEventListener('submit', async function (event) {
    event.preventDefault(); // Impede o envio padrão do formulário

    // Capturar o valor do campo de entrada keywords
    const keyword = keywordInput.value;

    // Criar o objeto JSON com a palavra-chave
    const keywordData = {
      word: keyword
    };

    try {
      // Enviar a requisição POST ao backend
      const response = await fetch('http://localhost:5000/block_word', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',  // Incluir credenciais na requisição
        body: JSON.stringify(keywordData)
      });

      const data = await response.json();

      // Tratar a resposta do servidor
      if (!response.ok || !data.success) {
        alert('Erro ao bloquear palavra-chave: ' + data.message);
      }

      // Buscar e exibir o conteúdo do arquivo de log
      const logResponse = await fetch('http://localhost:5000/get_log', {
        credentials: 'include'  // Incluir credenciais na requisição
      });
      const logData = await logResponse.json();

      if (logResponse.ok && logData.success) {
        const formattedLog = formatLog(logData.log);
        document.getElementById('info-log').innerHTML = formattedLog;
      } else {
        document.getElementById('info-log').textContent = 'Erro ao carregar o log.';
      }
    } catch (error) {
      alert('Erro ao bloquear palavra-chave. Por favor, tente novamente.');
    }
  });

  // Adicionar evento de escuta para a tecla "Enter"
  keywordInput.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
      event.preventDefault(); // Impede o comportamento padrão
      keywordButton.click(); // Aciona o clique no botão
    }
  });
});

/**
* Formata o conteúdo do log para ter quebras de linha a cada 120 caracteres
* e adiciona uma linha de separação responsiva após cada mensagem.
* @param {string} logContent - O conteúdo do log a ser formatado.
* @returns {string} - O conteúdo do log formatado.
*/
function formatLog(logContent) {
  const lines = logContent.split('\n');
  const formattedLines = [];
  let currentMessage = [];

  lines.forEach(line => {
    if (line.startsWith('Timestamp:')) {
      if (currentMessage.length > 0) {
        formattedLines.push(currentMessage.join(' '));
        formattedLines.push('<hr class="separator">');
        currentMessage = [];
      }
    }
    currentMessage.push(line);
  });

  if (currentMessage.length > 0) {
    formattedLines.push(currentMessage.join(' '));
    formattedLines.push('<hr class="separator">');
  }

  return formattedLines.join('<br>');
}

/**
* Formata uma mensagem para ter quebras de linha a cada 120 caracteres.
* @param {string} message - A mensagem a ser formatada.
* @returns {string} - A mensagem formatada.
*/
function formatMessage(message) {
  const maxLength = 120;
  const formattedMessage = [];
  for (let i = 0; i < message.length; i += maxLength) {
    formattedMessage.push(message.substring(i, i + maxLength));
  }
  return formattedMessage.join('<br>');
}