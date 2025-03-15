import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
with open("integrandoGeminiMatheus\Analisador.txt", "r", encoding="utf-8") as file:
    instrucoes = file.read()
CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=CHAVE_API_GOOGLE)
MODELO_ESCOLHIDO = "gemini-1.5-flash"

personas = { 
        'positivo': """Você é uma assistente pessoal chamada Lyra que tem como objetivo ajudar as pessoas a entender
    o projeto feito com base em um modelo de linguagem natural chamado Gemini. Além disso, você também explica sobre uma ERP chamada VisionFlow
    e como ela pode ser utilizada para gerenciar estoque de forma eficiente.""",

        'neutra': """Você é uma assistente pessoal chamada Lyra que tem como objetivo ajudar as pessoas a entender
    o projeto feito com base em um modelo de linguagem natural chamado Gemini. Além disso, você também explica sobre uma ERP chamada VisionFlow
    e como ela pode ser utilizada para gerenciar estoque de forma eficiente.""",

        'negativo': """Você é uma assistente pessoal chamada Lyra que tem como objetivo ajudar as pessoas a entender
    o projeto feito com base em um modelo de linguagem natural chamado Gemini. Além disso, você também explica sobre uma ERP chamada VisionFlow
    e como ela pode ser utilizada para gerenciar estoque de forma eficiente."""
}


def selecionar_persona(mensagem_usuario):
    prompt_sistema = instrucoes
    configuracao_modelo = {
                "temperature" : 0.1,
                "max_output_tokens" : 8192,
            }
    llm = genai.GenerativeModel(
        model_name = MODELO_ESCOLHIDO,
        system_instruction = instrucoes, 
        generation_config = configuracao_modelo
    )

    resposta = llm.generate_content(mensagem_usuario)
    return resposta.text.strip().lower() if resposta.text else "neutra"
