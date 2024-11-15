
let zoomLevel = 1;

function toggleContrast() {
    // Alterna uma classe CSS para aplicar o contraste alto
    document.body.classList.toggle('high-contrast');
}

function zoomIn() {
    // Aumenta o zoom da página ajustando o tamanho da fonte
    document.body.style.fontSize = (parseFloat(window.getComputedStyle(document.body).fontSize) + 2) + "px";
}

function zoomOut() {
    // Diminui o zoom da página ajustando o tamanho da fonte
    const currentSize = parseFloat(window.getComputedStyle(document.body).fontSize);
    if (currentSize > 10) { // Evita um tamanho de fonte muito pequeno
        document.body.style.fontSize = (currentSize - 2) + "px";
    }
}

document.addEventListener("DOMContentLoaded", function() {
    // Adicionar o listener para o formulário de contato
    document.getElementById('contactForm').addEventListener('submit', function(event) {
        event.preventDefault();

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;

        fetch('https://exemplo.com/api/enviar-contato', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, email, message }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao enviar a mensagem.');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('responseMessage').innerHTML = '<div class="alert alert-success">Mensagem enviada com sucesso!</div>';
            document.getElementById('contactForm').reset();
        })
        .catch(error => {
            document.getElementById('responseMessage').innerHTML = '<div class="alert alert-danger">Erro: ' + error.message + '</div>';
        });
    });

    // Adicionar o listener para o formulário de login
    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Evita o envio padrão do formulário

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Simulando o envio para um servidor (substitua a URL pelo endpoint real)
        fetch('https://exemplo.com/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao realizar o login.');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('loginResponseMessage').innerHTML = '<div class="alert alert-success">Login realizado com sucesso!</div>';
            // Aqui você pode redirecionar para outra página ou armazenar um token de autenticação, etc.
        })
        .catch(error => {
            document.getElementById('loginResponseMessage').innerHTML = '<div class="alert alert-danger">Erro: ' + error.message + '</div>';
        });
    });
});