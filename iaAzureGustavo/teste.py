import cv2
import requests
import mysql.connector
import time

# Função para capturar imagens da câmera
def capture_images():
    print("Iniciando captura de imagens...")  # Mensagem de depuração
    cap = cv2.VideoCapture(0)  # Abre a câmera (0 indica a câmera padrão)
    if not cap.isOpened():
        print("Erro ao abrir a câmera")
        return

    while True:
        ret, frame = cap.read()  # Captura uma imagem da câmera
        if ret:  # Verifica se a captura foi bem-sucedida
            cv2.imshow('Captured Image', frame)  # Mostra a imagem capturada em uma janela
            cv2.imwrite('product_image.jpg', frame)  # Salva a imagem capturada em um arquivo
            print("Imagem capturada e salva.")  # Mensagem de depuração
            analyze_and_store_image('product_image.jpg')  # Analisa e armazena a imagem
        else:
            print("Erro ao capturar a imagem")

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Pressione 'q' para sair do loop
            break
        time.sleep(1)  # Espera 1 segundo antes de capturar a próxima imagem

    cap.release()  # Libera a câmera
    cv2.destroyAllWindows()  # Fecha a janela da imagem
    print("Captura de imagens finalizada.")  # Mensagem de depuração

# Função para analisar a imagem usando o serviço de Visão Computacional do Azure
def analyze_image(image_path):
    print("Analisando imagem...")  # Mensagem de depuração
    subscription_key = "MQPyjhXNj2n6bsgnBX9u4tLMGHY6EdguYDwZQ7cLeeIQ9WSj2SaBJQQJ99BCACZoyfiXJ3w3AAAEACOG1ZHY"  # Chave de assinatura do Azure
    endpoint = "https://gus.cognitiveservices.azure.com/vision/v3.1/analyze"  # Endpoint correto do serviço de Visão Computacional

    try:
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()  # Lê a imagem do arquivo em modo binário
    except FileNotFoundError:
        print(f"Erro: Arquivo {image_path} não encontrado")
        return None

    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Description,Tags'}

    response = requests.post(endpoint, headers=headers, params=params, data=image_data)  # Faz a requisição POST para o serviço de Visão Computacional
    if response.status_code == 200:  # Verifica se a requisição foi bem-sucedida
        print("Análise da imagem bem-sucedida.")  # Mensagem de depuração
        return response.json()  # Retorna a resposta em formato JSON
    else:
        print("Erro na análise da imagem:", response.status_code, response.text)  # Imprime o erro se a requisição falhar
        return None  # Retorna None se houver um erro

# Função para conectar ao banco de dados MySQL
def connect_to_db():
    print("Conectando ao banco de dados...")  # Mensagem de depuração
    try:
        db = mysql.connector.connect(
            host="bddgus.mysql.database.azure.com",
            user="gam",
            password="alterar"
        )
        print("Conexão ao banco de dados estabelecida.")  # Mensagem de depuração
        return db
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None

# Função para armazenar os resultados da análise no banco de dados
def store_analysis(db, description, tags):
    if db is None:
        print("Conexão ao banco de dados não estabelecida")
        return

    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS meu_novo_banco_de_dados")
    cursor.execute("USE meu_novo_banco_de_dados")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_analysis (
            id INT AUTO_INCREMENT PRIMARY KEY,
            description TEXT,
            tags TEXT
        )
    """)
    sql = "INSERT INTO product_analysis (description, tags) VALUES (%s, %s)"
    val = (description, tags)
    cursor.execute(sql, val)
    db.commit()
    print("Resultados armazenados no banco de dados.")  # Mensagem de depuração

# Função para analisar e armazenar a imagem
def analyze_and_store_image(image_path):
    analysis = analyze_image(image_path)  # Analisa a imagem capturada
    if analysis:  # Verifica se a análise foi bem-sucedida
        description = analysis['description']['captions'][0]['text']
        tags = ','.join([tag['name'] for tag in analysis['tags']])
        db = connect_to_db()  # Conecta ao banco de dados
        store_analysis(db, description, tags)  # Armazena os resultados da análise no banco de dados
        if db:
            db.close()  # Fecha a conexão com o banco de dados
        print("Produto impróprio")  # Imprime que o produto é próprio
    else:
        print("Produto próprio")  # Imprime que o produto é impróprio

if __name__ == "__main__":
    capture_images()  # Captura e analisa imagens continuamente