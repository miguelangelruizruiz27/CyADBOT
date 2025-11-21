document.addEventListener("DOMContentLoaded", () => {
  const chatButton = document.getElementById("chat-button");
  const chatWindow = document.getElementById("chat-window");
  const sendBtn = document.getElementById("send-btn");
  const userInput = document.getElementById("user-input");
  const chatMessages = document.getElementById("chat-messages");
  const chatContainer = document.getElementById("chat-container");
  const chatCloseBtn = document.getElementById("chat-close-btn");

  // Crear overlay detrás del chat
  let overlay = document.createElement("div");
  overlay.classList.add("chat-overlay");
  document.body.appendChild(overlay);

  // Chat inicia oculto
  chatWindow.classList.add("hidden");
  chatWindow.style.display = "none";

  // Mostrar burbuja automáticamente
  chatContainer.classList.add("show-message");

  // Abrir chat al hacer clic en uamito
  chatButton.addEventListener("click", () => {
    chatWindow.classList.remove("hidden");
    chatWindow.style.display = "flex";
    chatContainer.classList.remove("show-message");
    overlay.style.display = "block"; // mostrar overlay

    // Mensaje de bienvenida solo la primera vez
    if (!chatWindow.dataset.welcomeShown) {
      appendMessage("CyADBot", "¡Hola! 👋 Bienvenido a CyADBot. ¿En qué te puedo ayudar?");
      chatWindow.dataset.welcomeShown = "true";
    }
  });

  // Cerrar chat con tache
  chatCloseBtn.addEventListener("click", closeChat);

  // Cerrar chat al hacer clic en overlay
  overlay.addEventListener("click", closeChat);

  function closeChat() {
    chatWindow.classList.add("hidden");
    chatWindow.style.display = "none";
    chatContainer.classList.add("show-message");
    overlay.style.display = "none";
  }

  // Evitar que clic dentro del chat no cierre el chat
  chatWindow.addEventListener("click", (e) => {
    e.stopPropagation();
  });

  // Enviar mensaje desde botón
  sendBtn.addEventListener("click", (e) => {
    e.preventDefault();
    sendMessage();
  });

  // Enviar mensaje con Enter
  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  });

  function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    appendMessage("Tú", text);
    userInput.value = "";

    fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    })
      .then(res => res.json())
      .then(data => appendMessage("CyADBot", data.response))
      .catch(() => appendMessage("CyADBot", "Ocurrió un error. Intenta de nuevo."));
  }

  function appendMessage(sender, text) {
    const msg = document.createElement("div");
    msg.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
});
