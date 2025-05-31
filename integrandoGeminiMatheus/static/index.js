let chat = document.querySelector('#chat');''
let input = document.querySelector('#input');
let botaoEnviar = document.querySelector('#botao-enviar');
let imagemSelecionada;
let botaoAnexo = document.querySelector("#mais_arquivo");
let miniaturaImagem;
let caminhoImagemServidor; // Variável para armazenar o caminho da imagem no servidor
let inputContainer = document.querySelector('.entrada__input-container');


async function pegarImagem() {
    let fileInput = document.createElement("input");
    fileInput.type = 'file';
    fileInput.accept = "image/*";

    fileInput.onchange = async e => {
        if (miniaturaImagem) {
            miniaturaImagem.remove();
        }

        imagemSelecionada = e.target.files[0];

        miniaturaImagem = document.createElement('img');
        miniaturaImagem.src = URL.createObjectURL(imagemSelecionada);
        miniaturaImagem.style.maxWidth = '3rem';
        miniaturaImagem.style.maxHeight = '3rem';
        miniaturaImagem.style.margin = '0.5rem';

        let inputContainer = document.querySelector('.entrada__input-container');
        document.querySelector('.entrada__container').insertBefore(miniaturaImagem, inputContainer);

        let formData = new FormData();
        formData.append('imagem', imagemSelecionada);

        const response = await fetch('http://127.0.0.1:5000/upload_imagem', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const resposta = await response.json(); // Alterado para response.json()
            console.log(resposta);

            // Armazena o caminho da imagem no servidor
            caminhoImagemServidor = resposta.caminho; // Acessa o caminho retornado pelo servidor
            console.log("Caminho da imagem no servidor:", caminhoImagemServidor);
        } else {
            console.error('Erro no upload da imagem');
        }
    }
    fileInput.click();
}


async function enviarMensagem() {
    if (input.value == "" || input.value == null) return;
    let mensagem = input.value;
    input.value = "";

    let novaBolha = criaBolhaUsuario();
    novaBolha.innerHTML = mensagem;
    chat.appendChild(novaBolha);

    let novaBolhaBot = criaBolhaBot();
    chat.appendChild(novaBolhaBot);
    vaiParaFinalDoChat();
    novaBolhaBot.innerHTML = "Analisando";

    let estados = ["Analisando .", "Analisando ..", "Analisando ...", "Analisando ."]
    let indiceEstado = 0;
    let intervaloAnimacao = setInterval(() => {
        novaBolhaBot.innerHTML = estados[indiceEstado];
        indiceEstado = (indiceEstado + 1) % estados.length;
    }, 500);


    // Envia requisição com a mensagem e o caminho da imagem para a API do ChatBot
    const resposta = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            'msg': mensagem,
            'imagem': caminhoImagemServidor  // Envia o caminho da imagem
        }),
    });

    console.log(resposta);

    const textoDaResposta = await resposta.text();
    novaBolhaBot.innerHTML = textoDaResposta.replace(/\n/g, '<br>');
    vaiParaFinalDoChat();

    // Limpa o caminho da imagem após enviar a mensagem
    caminhoImagemServidor = null;
    if (miniaturaImagem) {
        miniaturaImagem.remove();
        miniaturaImagem = null;
    }
}

function criaBolhaUsuario() {
    let bolha = document.createElement('p');
    bolha.classList = 'chat__bolha chat__bolha--usuario';
    return bolha;
}

function criaBolhaBot() {
    let bolha = document.createElement('p');
    bolha.classList = 'chat__bolha chat__bolha--bot';
    return bolha;
}

function vaiParaFinalDoChat() {
    chat.scrollTop = chat.scrollHeight;
}

botaoEnviar.addEventListener('click', enviarMensagem);
input.addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        botaoEnviar.click();
    }
});

botaoAnexo.addEventListener('click', pegarImagem);