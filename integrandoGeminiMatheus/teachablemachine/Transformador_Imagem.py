import cv2
import numpy as np
import os

def ajustar_iluminacao(img, alpha=1.0, beta=0):
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

def simular_condicoes_luminosas_em_lote(pasta_entrada, pasta_saida):
    os.makedirs(pasta_saida, exist_ok=True)

    condicoes = [
        {"nome": "luz_fraca", "alpha": 1.0, "beta": -60},
        {"nome": "luz_forte", "alpha": 1.0, "beta": 60},
        {"nome": "alto_contraste", "alpha": 1.5, "beta": 0},
        {"nome": "baixo_contraste", "alpha": 0.7, "beta": 0},
        {"nome": "claro_contraste", "alpha": 1.3, "beta": 40},
    ]

    # Percorre todas as imagens da pasta
    for nome_arquivo in os.listdir(pasta_entrada):
        caminho_img = os.path.join(pasta_entrada, nome_arquivo)

        # Verifica se é uma imagem
        if nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            imagem = cv2.imread(caminho_img)
            if imagem is None:
                print(f"Não foi possível ler a imagem: {nome_arquivo}")
                continue

            nome_base = os.path.splitext(nome_arquivo)[0]

            for cond in condicoes:
                img_modificada = ajustar_iluminacao(imagem, alpha=cond["alpha"], beta=cond["beta"])
                nome_novo = f"{nome_base}_{cond['nome']}.jpg"
                caminho_salvar = os.path.join(pasta_saida, nome_novo)
                cv2.imwrite(caminho_salvar, img_modificada)
                print(f"Salvo: {caminho_salvar}")

# Exemplo de uso
simular_condicoes_luminosas_em_lote("integrandoGeminiMatheus/teachablemachine/Nao_apto-samples", "imagens_transformadas2")