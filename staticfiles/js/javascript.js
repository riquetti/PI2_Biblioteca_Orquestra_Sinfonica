//Script para esconder filtros
    
function mostrar_form(v1) {
    categoria = document.getElementById('categoria')
    livro = document.getElementById('livro')
    emprestimo = document.getElementById('emprestimos')
    devolucao = document.getElementById('devolucao')

    if (v1 == 1) {
        categoria.style.display = 'block';

        devolucao.style.display = 'none';
        livro.style.display = 'none';
        emprestimo.style.display = 'none';
    } else if (v1 == 2) {
        livro.style.display = 'block';

        devolucao.style.display = 'none';
        categoria.style.display = 'none';
        emprestimo.style.display = 'none';

    } else if (v1 == 3) {
        emprestimo.style.display = 'block';

        devolucao.style.display = 'none';
        categoria.style.display = 'none';
        livro.style.display = 'none';

    } else if (v1 == 4) {
        devolucao.style.display = 'block';

        categoria.style.display = 'none';
        livro.style.display = 'none';
        emprestimo.style.display = 'none';
    }

}

function exibe_input_emprestado(v1) {

    if (v1 == 1) {
        document.getElementById('nome_emprestado').style.display = "none"
        document.getElementById('nome_emprestado_anonimo').style.display = "block"

    } else {
        document.getElementById('nome_emprestado').style.display = "block"
        document.getElementById('nome_emprestado_anonimo').style.display = "none"

    }

}

//Script para alto contraste

function toggleContraste() {
// Alterna a classe 'alto-contraste' no corpo da página
    document.body.classList.toggle('alto-contraste');
    lista_livros = document.getElementsByClassName("livro");
    for (i of lista_livros) {
        i.classList.toggle('alto-contraste');
    lista_cards = document.getElementsByClassName("card");
    }
    for (j of lista_cards) {
        j.classList.toggle('alto-contraste');
    }

// Salva a preferência do usuário no localStorage
    if (document.body.classList.contains('alto-contraste')) {
        localStorage.setItem('contraste', 'ativo');
    } else {
        localStorage.removeItem('contraste');
    }
    }

// Ao carregar a página, verifica se o usuário já ativou o alto contraste antes
    window.onload = function() {
        lista_livros = document.getElementsByClassName("livro");
        lista_cards = document.getElementsByClassName("card");
        if (localStorage.getItem('contraste') === 'ativo') {
            document.body.classList.add('alto-contraste');
            for (i of lista_livros) {
                i.classList.add('alto-contraste');
            }
            for (j of lista_cards) {
                j.classList.add('alto-contraste');
            }
        }
    }

//Script pra ajuste do tamanho da fonte

document.addEventListener('DOMContentLoaded', function () {
    const increaseButton = document.getElementById('increase-font');
    const decreaseButton = document.getElementById('decrease-font');
    
    // Seletor para os elementos cujas fontes serão ajustadas
    const elements = document.querySelectorAll('body, p, h1, h2, h3, h4, h5, h6, button, nav, a, span, li, input, select, textarea');
    const largerTextElements = document.querySelectorAll('.larger-text'); // Seleciona textos maiores

    let currentFontSize = 16; // Tamanho padrão do texto em pixels

    // Função para ajustar o tamanho da fonte em todos os elementos
    function setFontSize(size) {
        elements.forEach(element => {
            element.style.fontSize = size + 'px';
        });
        // Ajusta a fonte para os elementos com .larger-text para que fiquem maiores
        largerTextElements.forEach(element => {
            element.style.fontSize = (size * 3) + 'px'; // O dobro do tamanho
        });
    }

    increaseButton.addEventListener('click', function () {
        currentFontSize += 2; // Aumenta o tamanho do texto
        setFontSize(currentFontSize);
    });

    decreaseButton.addEventListener('click', function () {
        if (currentFontSize > 10) { // Define um tamanho mínimo
            currentFontSize -= 2; // Diminui o tamanho do texto
            setFontSize(currentFontSize);
        }
    });

    // Inicializa o tamanho da fonte ao carregar a página
    setFontSize(currentFontSize);

});