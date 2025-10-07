const socket = io();
const messages = document.getElementById('messages');
const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('user');
const textInput = document.getElementById('text');

function addMessage(msg) {
  const div = document.createElement('div');
  div.className = 'message';
  const time = msg && msg.ts ? new Date(msg.ts).toLocaleTimeString() : '';
  const user = (msg && msg.user) ? msg.user : 'anonymous';
  const text = (msg && msg.text) ? msg.text : '';
  div.innerHTML = `<strong>${user}:</strong> ${text} <span class="ts">${time}</span>`;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

socket.on('message', (msg) => {
  addMessage(msg);
});

chatForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const user = userInput.value || 'anonymous';
  const text = textInput.value.trim();
  if (!text) return;
  socket.emit('send_message', { user, text });
  textInput.value = '';
  textInput.focus();
});
