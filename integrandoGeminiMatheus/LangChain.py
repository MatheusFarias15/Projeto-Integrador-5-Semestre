from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_community.chat_models import ChatMaritalk
from my_keys import MARITACA_API_KEY
from my_models import MARITACA_SABIA
from langchain_core.messages import HumanMessage
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gerenciar_imagem import encode_image, gerar_imagem_gemini
import base64


load_dotenv()
with open("integrandoGeminiMatheus\Analisador.txt", "r", encoding="utf-8") as file:
    instrucoes = file.read()
CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=CHAVE_API_GOOGLE)
MODELO_ESCOLHIDO = "gemini-1.5-flash"

llm =  ChatGoogleGenerativeAI(
    api_key=CHAVE_API_GOOGLE,
    model=MODELO_ESCOLHIDO,
)

imagem = encode_image("integrandoGeminiMatheus\imagens_temporarias\imagem_enviada.png")

pergunta = """Por favor, analise as imagens fornecidas e separe-as de acordo com suas características visuais, contexto, atributos técnicos e tipo de imagem. Utilize as categorias abaixo para realizar a classificação:

Características Visuais: Identifique cores predominantes, formas, objetos e composição.

Contexto: Determine se as imagens estão em ambientes fechados ou abertos, se há ações ou interações, e o tema geral da cena.

Atributos Técnicos: Classifique as imagens por sua resolução, formato e qualidade.

Tipo de Imagem: Identifique se a imagem é uma fotografia, ilustração, gráfico ou arte conceitual.

Separe automaticamente as imagens nas pastas correspondentes, com base nas classificações, e forneça tags detalhadas para cada uma. Se uma imagem não puder ser classificada de forma clara, marque-a para revisão manual."""

mensagem = HumanMessage(
    content = [{
        "type" : "text",
        "text" : pergunta
    },
        {
        "type" : "image_url",
        "image_url" : f"data:image/jpeg;base64,{imagem}" } ]
)

resposta = llm.invoke([mensagem])

print(resposta)