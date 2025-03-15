from time import sleep
from flask import Flask, render_template, request, Response
import google.generativeai as genai
from dotenv import load_dotenv
from personalidade import personas, selecionar_persona
import os

# Carregar instruções
with open("integrandoGeminiMatheus/Analisador.txt", "r", encoding="utf-8") as file:
    instrucoes = file.read()


# Carregar variáveis de ambiente
load_dotenv()
CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")

# Configurar API Gemini
genai.configure(api_key=CHAVE_API_GOOGLE)
MODELO_ESCOLHIDO = "gemini-1.5-flash"

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Criar Chatbot
def criar_chatbot():
    configuracao_modelo = {
        "temperature": 0.1,
        "max_output_tokens": 8192,
    }

    llm = genai.GenerativeModel(
        model_name=MODELO_ESCOLHIDO,
        system_instruction=instrucoes,
        generation_config=configuracao_modelo
    ) 

    chatbot = llm.start_chat(history=[])
    return chatbot

chatbot = criar_chatbot()

# Função do Bot
def bot(prompt):
    maximo_tentativas = 3
    repeticao = 0

    while repeticao < maximo_tentativas: 
        try:
            personalidade = personas.get(selecionar_persona(prompt), personas["neutra"])

            # Construção correta da mensagem
            mensagem_usuario = f"Considerar essa personalidade para responder a mensagem: {personalidade}. " \
                               f"Responda a seguinte mensagem sempre lembrando do histórico: {prompt}"

            resposta = chatbot.send_message(mensagem_usuario)
            
            return resposta.text if resposta else "Erro: Nenhuma resposta recebida do Gemini."

        except Exception as erro:
            repeticao += 1
            print(f"Erro na tentativa {repeticao}: {erro}")  # Log para depuração
            sleep(2)

    return "Erro no Gemini após várias tentativas."

# Rotas Flask
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    resposta = bot(prompt)
    return resposta

if __name__ == "__main__":
    app.run(debug=True)
