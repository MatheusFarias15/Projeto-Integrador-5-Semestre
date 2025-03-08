import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

chave_api_google = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=chave_api_google)
modelo_escolhido = "gemini-1.5-flash"

# Carregar instruções do analisador
with open("Prompt\Analisador.txt", "r", encoding="utf-8") as file:
    Analisador = file.read()

# Criar o modelo
model = genai.GenerativeModel(
    model_name=modelo_escolhido,
    system_instruction=Analisador
)

def carregar_modelo(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo: 
            return arquivo.read()
    except IOError as e:
        print(f"Erro ao carregar o arquivo {nome_do_arquivo}: {e}")
        return None
    
def salvar_modelo(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar o arquivo {nome_do_arquivo}: {e}")

# Nome do produto para análise
nome_produto = "Teste_Leitura"

# Carregar o prompt do usuário
prompt_usuario = carregar_modelo(f"{nome_produto}.txt")

if prompt_usuario:
    print(f"Iniciando a análise do produto... {nome_produto}")
    
    # Gerar resposta usando o modelo carregado
    resposta = model.generate_content(prompt_usuario, generation_config={
        "temperature": 1,
        "top_p": 0.95,
        "max_output_tokens": 100,
        "response_mime_type": "text/plain",
    })

    if resposta:
        texto_resposta = resposta.text if hasattr(resposta, "text") else resposta.candidates[0].text
        salvar_modelo(f"{nome_produto}-resposta.txt", texto_resposta)
    else:
        print("Erro ao gerar a resposta")

# Carregar e imprimir a resposta gerada
resposta_texto = carregar_modelo(f"{nome_produto}-resposta.txt")

if resposta_texto:
    print(f"Resposta gerada: {resposta_texto}")
else:
    print("Erro ao carregar a resposta")
