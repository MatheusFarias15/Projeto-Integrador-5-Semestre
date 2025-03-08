from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

subscription_key = "sClTOJsaCeCosOMdhd7m28rAYpz9KHcb89KyjoY0BaCJp6Z1PeSasJQQJ99BCACZoyfiXJ3w3AAAEACOGFx7H"
endpoint = "https://gus.cognitiveservices.azure.com/"
sentiment_url = endpoint + "/text/analytics/v3.0/sentiment"

def analyze_sentiment(text):
    # Faça a solicitação à API
    response = requests.post(sentiment_url, headers={
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/json"
    }, json={"id": "1", "language": "pt", "text": text})

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

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    document = analyze_sentiment(user_message)
    if document:
        sentiment = document['sentiment']
        confidence_scores = document['confidenceScores']
        print(f"Sentimento: {sentiment}, Pontuações: {confidence_scores}")
        if sentiment == 'positive':
            bot_response = "Que ótimo saber que você está feliz!"
        elif sentiment == 'negative':
            bot_response = "Sinto muito que você esteja se sentindo assim."
        else:
            bot_response = "Entendi. Conte-me mais sobre isso."
    else:
        bot_response = "Desculpe, não consegui analisar o sentimento da sua mensagem."
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)