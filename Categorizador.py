import os
import google.generativeai as genai
from dotenv import load_dotenv

with open("Prompt\instrucao.txt", "r", encoding="utf-8") as file:
    resumo = file.read()

load_dotenv()

CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=CHAVE_API_GOOGLE)
MODELO_ESCOLHIDO = "gemini-1.5-flash"

llm = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=resumo,
)

while True:
    pergunta = input("Digite sua pergunta (ou pressione Enter para sair): \n ")
    if pergunta.strip() == "":
        print("Tchau! Precisando estou a disposição ")
        break

    resposta = llm.generate_content(pergunta)
    print(f"Resposta: {resposta.text}")