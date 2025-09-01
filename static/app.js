const emailInput = document.getElementById('emailInput');
const sendBtn = document.getElementById('sendBtn');
const fileInput = document.getElementById('fileInput');
const attachBtn = document.getElementById('attachBtn');

// Add this function
function addMessage(content, isUser = false) {
    const messageList = document.getElementById('messageList');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'assistant-message'}`;
    messageDiv.innerHTML = `<div class="message-content">${content}</div>`;
    messageList.appendChild(messageDiv);
    messageList.scrollTop = messageList.scrollHeight;
}

sendBtn.addEventListener('click', async () => {
    const emailText = emailInput.value.trim();
    if (!emailText) {
        addMessage('<div class="error-message">Por favor, insira o conteúdo do email</div>');
        return;
    }

    // Add user message
    addMessage(`<p>${emailText.replace(/\n/g, '<br>')}</p>`, true);

    // Clear input
    emailInput.value = '';

    const response = await fetch('/api/classify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email_content: emailText })
    });

    const result = await response.json();

    addMessage(`
        <div class="classification-result">
            <div class="classification-badge ${result.classification.toLowerCase()}">
                ${result.classification}
            </div>
            <div class="response-section">
                <h4>Suggested Response:</h4>
                <p>${result.suggested_response}</p>
            </div>
        </div>
    `);
});

attachBtn.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();

    if (response.ok) {
        emailInput.value = result.email_content;
        addMessage(`
            <div class="success-message">
                ✅ Arquivo carregado com sucesso: <strong>${result.filename}</strong>
            </div>
        `);
    } else {
        addMessage(`
            <div class="error-message">
                ❌ Erro: ${result.error}
            </div>
        `);
    }
});
