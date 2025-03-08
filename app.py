from time import sleep
from flask import Flask, render_template, request, Response
import google.generativeai as genai
from dotenv import load_dotenv
import os

with open("Analisador.txt", "r", encoding="utf-8") as file:
    instrucoes = file.read()

load_dotenv()

CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=CHAVE_API_GOOGLE)
MODELO_ESCOLHIDO = "gemini-1.5-flash"

app = Flask(__name__)
app.secret_key = 'mysecretkey'

def bot(prompt):
    maximo_tentativas = 1
    repeticao = 0

    while True: 
        try: 

            prompt_sistema = instrucoes
            configuracao_modelo = {
                "temperature" : 0.1,
                "max_output_tokens" : 8192,
            }

            llm = genai.GenerativeModel(
                model_name= MODELO_ESCOLHIDO,
                system_instruction= instrucoes,
                generation_config= configuracao_modelo
            )
            

            resposta = llm.generate_content(prompt)
            return resposta.text
        except Exception as erro: 
            repeticao += 1
            if repeticao >= maximo_tentativas:
                return "Erro no Gemini:"
            sleep(50) 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    print('testacga')
    resposta = bot(prompt)

    return resposta

if __name__ == "__main__":
    app.run(debug = True)

