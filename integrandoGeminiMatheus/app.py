from time import sleep
import uuid
from flask import Flask, render_template, request, Response
import google.generativeai as genai
from dotenv import load_dotenv
from personalidade import personas, selecionar_persona
from gerenciar_imagem import gerar_imagem_gemini
import os

# Carregar instruções
with open("integrandoGeminiMatheus/Analisador.txt", "r", encoding="utf-8") as file:
    instrucoes = file.read()

caminho_imagem_enviada = None
UPLOAD_FOLDER = "imagens_temporarias"

# Carregar variáveis de ambiente
load_dotenv()
CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")

# Configurar API Gemini
genai.configure(api_key=CHAVE_API_GOOGLE)
MODELO_ESCOLHIDO = "gemini-1.5-pro"

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Criar Chatbot

def criar_chatbot():
    configuracao_modelo = {
        "temperature": 0.1,
        "max_output_tokens": 8192,
    }

    modelo = genai.GenerativeModel(
        model_name=MODELO_ESCOLHIDO,
        system_instruction=instrucoes,
        generation_config=configuracao_modelo
    )

    return modelo



chatbot = criar_chatbot()

# Função para upload da imagem
@app.route("/upload_imagem", methods=["POST"])
def upload_imagem():
    global caminho_imagem_enviada

    if "imagem" in request.files:
        imagem_enviada = request.files["imagem"]
        nome_arquivo = str(uuid.uuid4()) + os.path.splitext(imagem_enviada.filename)[1]
        caminho_arquivo = os.path.join(UPLOAD_FOLDER, nome_arquivo)
        imagem_enviada.save(caminho_arquivo)
        caminho_imagem_enviada = caminho_arquivo

        # Retorna o caminho correto para o JavaScript
        return {"caminho": caminho_arquivo}, 200  

    return "Nenhum arquivo enviado", 400

@app.after_request
def log_request(response):
    print("---- REQUEST ----")
    print(request.method, request.path)
    print("Body:", request.get_data())
    print("-----------------")
    return response


def bot(prompt, caminho_imagem=None):
    maximo_tentativas = 3
    repeticao = 0
    global caminho_imagem_enviada

    while repeticao < maximo_tentativas:
        try:
            # Criar chatbot sem manter histórico
            chatbot = genai.GenerativeModel(
                model_name=MODELO_ESCOLHIDO,
                system_instruction=instrucoes,
                generation_config={
                    "temperature": 0.1,
                    "max_output_tokens": 512  # Reduzido para respostas mais curtas
                }
            )

            personalidade = personas.get(selecionar_persona(prompt), personas["neutra"])

            mensagem_usuario = (
                f"Considere essa personalidade para responder: {personalidade}. "
                f"Responda brevemente a esta mensagem: {prompt}. "
                f"Se houver imagem, analise suas características e classifique como 'Apto' ou 'Não apto para venda'. "
                f"Se o assunto não for relacionado, diga que a funcionalidade está em desenvolvimento."
            )

            if caminho_imagem:
                mensagem_usuario += "\nUtilize a imagem enviada para responder."
                arquivo_imagem = gerar_imagem_gemini(caminho_imagem)
                resposta = chatbot.generate_content([arquivo_imagem, mensagem_usuario])
            else:
                resposta = chatbot.generate_content(mensagem_usuario)

            if resposta and resposta.text:
                return resposta.text.strip()
            else:
                return "Erro: Nenhuma resposta recebida do Gemini."

        except Exception as erro:
            repeticao += 1
            print(f"Erro na tentativa {repeticao}: {erro}")
            sleep(2)

    return "Erro no Gemini após várias tentativas."


# Rotas Flask
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    dados = request.get_json()
    mensagem = dados.get("msg")
    imagem = dados.get("imagem")

    print("Mensagem recebida:", mensagem)
    print("Caminho da imagem:", imagem)

    # Aqui você processa e devolve a resposta
    resposta = f"Recebi sua mensagem: '{mensagem}' e imagem: '{imagem}'"
    return resposta  # <- precisa ser uma string

 

if __name__ == "__main__":
    app.run(debug=True)