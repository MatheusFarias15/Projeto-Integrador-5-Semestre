import requests

# Defina a chave de assinatura e o endpoint
subscription_key = "AKjQDcII6jx1HwsBmuUsIRFjMXe7SAmUkJJ3gWuGSGklOkDyRHfzJQQJ99BCACZoyfiXJ3w3AAAEACOGFx7H"
endpoint = "https://gus.cognitiveservices.azure.com//"

# Defina o URL de análise de sentimentos
sentiment_url = endpoint + "/text/analytics/v3.0/sentiment"

# Defina os documentos a serem analisados
documents = {"documents": [
    {"id": "1", "language": "pt", "text": "eu odeio java "}
]}

# Faça a solicitação à API
response = requests.post(sentiment_url, headers={
    "Ocp-Apim-Subscription-Key": subscription_key,
    "Content-Type": "application/json"
}, json=documents)

# Verifique se a solicitação foi bem-sucedida
if response.status_code == 200:
    sentiment_analysis = response.json()
    # Exiba os resultados
    for document in sentiment_analysis['documents']:
        print(f"ID: {document['id']}")
        print(f"Sentimento: {document['sentiment']}")
        print(f"Pontuações: {document['confidenceScores']}")
else:
    print(f"Erro: {response.status_code}")
    print(response.json())