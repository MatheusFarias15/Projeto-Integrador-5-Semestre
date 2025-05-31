import google.generativeai as genai
from dotenv import load_dotenv
import os
import base64

load_dotenv()
with open("integrandoGeminiMatheus\Analisador.txt", "r", encoding="utf-8") as file:
    instrucoes = file.read()
CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=CHAVE_API_GOOGLE)
MODELO_ESCOLHIDO = "gemini-1.5-flash"

def gerar_imagem_gemini(caminho_imagem): 
    arquivo_temporario = genai.upload_file(
        file_path=caminho_imagem,
        display_name= "imagem enviada"
    )

    print(f"Arquivo temporário gerado: {arquivo_temporario}")

    return arquivo_temporario


# um código curto que permite abrir uma imagem, dado um caminho passado como parâmetro para a função encode_image().

def encode_image(image):
    with open(image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

