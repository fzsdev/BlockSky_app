document.addEventListener('DOMContentLoaded', function () {
  const keywordForm = document.getElementById('keyword-form');
  const keywordInput = document.getElementById('keywords');
  const keywordButton = document.querySelector('.keyword-button');

  keywordForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const keyword = keywordInput.value;

    try {
      const response = await fetch('http://127.0.0.1:5000/block_word', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ word: keyword })
      });

      const data = await response.json();

      if (response.status === 401) {
        alert('Sessão expirada. Por favor, faça login novamente.');
        return;
      }

      alert(data.message);

      if (data.success) {
        // Atualizar logs apenas se sucesso
        await updateLogs();
      }

    } catch (error) {
      console.error('Erro:', error);
      alert('Erro ao executar operação. Por favor, tente novamente.');
    }
  });

  async function updateLogs() {
    try {
      const response = await fetch('http://127.0.0.1:5000/get_log', {
        method: 'GET',
        credentials: 'include'
      });
      if (!response.ok) {
        console.error('Erro ao obter logs:', response.status);
        return;
      }
      const data = await response.json();
      if (data.success) {
        const formattedLog = formatLog(data.log);
        document.getElementById('info-log').innerHTML = formattedLog;
      } else {
        console.error('Erro ao obter logs:', data.message);
      }
    } catch (error) {
      console.error('Erro ao atualizar logs:', error);
    }
  }

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
  const allMessages = [];
  let currentMessage = [];

  lines.forEach(line => {
    if (line.startsWith('Timestamp:')) {
      if (currentMessage.length > 0) {
        allMessages.push(currentMessage.join(' '));
        currentMessage = [];
      }
    }
    currentMessage.push(line);
  });

  if (currentMessage.length > 0) {
    allMessages.push(currentMessage.join(' '));
  }

  // Inverter a ordem, para que as recentes venham primeiro
  allMessages.reverse();

  // Construir o resultado com separadores
  const formattedLines = [];
  allMessages.forEach(msg => {
    formattedLines.push(msg);
    formattedLines.push('<hr class="separator">');
  });

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