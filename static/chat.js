// JavaScript для обработки отправки сообщений
const messagesContainer = document.getElementById('messages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');

// Функция добавления нового сообщения
function addMessage(text, isOutgoing) {
  const messageElement = document.createElement('div');
  messageElement.classList.add('message');
  messageElement.classList.add(isOutgoing ? 'outgoing' : 'incoming');
  messageElement.textContent = text;

  messagesContainer.appendChild(messageElement);

  // Прокрутка вниз
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Обработка нажатия на кнопку "Отправить"
sendButton.addEventListener('click', () => {
  const messageText = messageInput.value.trim();
  if (messageText) {
    // Добавляем исходящее сообщение
    addMessage(messageText, true);

    // Очищаем поле ввода
    messageInput.value = '';

    // Имитация ответа от собеседника
    setTimeout(() => {
      addMessage('Ответ!', false);
    }, 1000);
  }
});

// Обработка нажатия Enter в поле ввода
messageInput.addEventListener('keypress', (event) => {
  if (event.key === 'Enter') {
    sendButton.click();
  }
});