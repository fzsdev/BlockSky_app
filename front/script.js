document.getElementById("login-button").addEventListener("click", async () => {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  if (!username || !password) {
    alert("Por favor, preencha todos os campos.");
    return;
  }

  try {
    // Configuração da requisição
    const response = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "/", // Aceita qualquer resposta, como no Insomnia
      },
      credentials: "include", // Para incluir cookies automaticamente
      body: JSON.stringify({ username, password }),
    });

    // Processando a resposta da API
    const data = await response.json();

    if (response.ok) {
      alert(data.message); // Exibe a mensagem retornada
      console.log("Sucesso:", data);

      // Lida com os cookies, se necessário
      const cookies = document.cookie; // Exibe os cookies armazenados
      console.log("Cookies armazenados:", cookies);
    } else {
      console.error("Erro:", data);
      alert(data.message || "Erro ao realizar login.");
    }
  } catch (error) {
    console.error("Erro na conexão com o servidor:", error);
    alert("Falha ao conectar ao servidor. Detalhes no console.");
  }
});