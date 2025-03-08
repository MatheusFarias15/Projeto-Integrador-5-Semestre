import os
import google.generativeai as genai
from dotenv import load_dotenv

# Corrigindo a leitura do arquivo TXT
with open("Prompt\instrucao.txt", "r", encoding="utf-8") as file:
    instrucoes = file.read()

load_dotenv()

CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=CHAVE_API_GOOGLE)
MODELO_ESCOLHIDO = "gemini-1.5-flash"

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  system_instruction=instrucoes
)

chat_session = model.start_chat(
  history=[]
)

response = chat_session.send_message("Quais foram as tecnologias utilizadas no projeto?")

print(response.text)