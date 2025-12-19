from flask import Flask, request, jsonify
from classifier import classify_intent

app = Flask(__name__)

# ==========================================
# 🟢 EDIT ZONE: YOUR RESPONSES
# ==========================================
# Map the INTENT (Left) to the RESPONSE (Right).
BOT_RESPONSES = {
    "PRICING": "Nuestras tarifas son 30€/mes por 1 clase semanal.",
    "SCHEDULE": "Abrimos de Lunes a Viernes de 17:00 a 20:00.",
    "FEDERATION": "Para federarte necesitas rellenar el formulario FIDA.",
    "LICHESS": "Entra en lichess.org/signup para crear tu cuenta.",
    "CONTACT": "Puedes escribirnos a contacto@chessattitude.com", # <--- New example
    
    # Default response if intent is unclear or for greetings
    "HUMAN": "Hola, soy el bot de Chess Attitude. ¿En qué puedo ayudarte?"
}

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Main webhook entry point. Receives JSON payload, determines intent, and sends response.
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        # 1. Detect intent using the AI classifier
        intent = classify_intent(user_message)
        
        # 2. Retrieve response from the dictionary
        # If the intent is not in the list, use the default HUMAN response
        response_text = BOT_RESPONSES.get(intent, BOT_RESPONSES["HUMAN"])

        return jsonify({
            "response": response_text,
            "intent": intent
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the application on localhost port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)