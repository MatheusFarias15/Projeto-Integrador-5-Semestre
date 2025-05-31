import os
import google.generativeai as genai
from dotenv import load_dotenv

# Corrigindo a leitura do arquivo TXT
with open("integrandoGeminiMatheus\Analisador.txt", "r", encoding="utf-8") as file:
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

response = chat_session.send_message(""""Analise esses produtos e poderia me dizer como o projeto foi feito Produto 1: Smartphone Samsung Galaxy S23 Ultra
Classificado: Apto para venda

Produto 2: Notebook Dell XPS 15
Classificado: Apto para venda

Produto 3: Monitor Gamer LG UltraGear 27"
Classificado: Apto para venda

Produto 4: Fone de Ouvido Sony WH-1000XM5
Classificado: Apto para venda

Produto 5: Teclado Mecânico HyperX Alloy Origins
Classificado: Apto para venda

Produto 6: Mouse Gamer Logitech G502 HERO
Classificado: Apto para venda

Produto 7: Smartwatch Apple Watch Series 9
Classificado: Apto para venda

Produto 8: Tablet iPad Pro M2 12.9"
Classificado: Apto para venda

Produto 9: Placa de Vídeo NVIDIA RTX 4080
Classificado: Apto para venda

Produto 10: Console PlayStation 5
Classificado: Apto para venda

Produto 11: Caixa de Som JBL Charge 5
Classificado: Apto para venda

Produto 12: Câmera GoPro Hero 12 Black
Classificado: Apto para venda

Produto 13: SSD NVMe Samsung 990 Pro 2TB
Classificado: Apto para venda

Produto 14: Processador AMD Ryzen 9 7950X
Classificado: Apto para venda

Produto 15: Roteador Wi-Fi 6 TP-Link Archer AX73
Classificado: Apto para venda

Produto 16: Monitor Gamer ASUS ROG Swift 32"
Classificado: Não apto para venda

Produto 17: Notebook Acer Predator Helios 300
Classificado: Não apto para venda

Produto 18: Controle Xbox Elite Series 2
Classificado: Não apto para venda

Produto 19: HD Externo Seagate 5TB
Classificado: Não apto para venda

Produto 20: Carregador MagSafe para iPhone
Classificado: Não apto para venda""""")



print(response.text)