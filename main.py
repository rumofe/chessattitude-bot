from flask import Flask, request, jsonify
from classifier import classify_intent

app = Flask(__name__)

# ==========================================
# 🟢 EDIT ZONE: YOUR RESPONSES
# ==========================================
BOT_RESPONSES = {
    "PRICING": "Nuestras tarifas son 30€/mes por 1 clase semanal.",
    "SCHEDULE": "Abrimos de Lunes a Viernes de 17:00 a 20:00.",
    "FEDERATION": "Para federarte necesitas rellenar el formulario FIDA.",
    "LICHESS": "Entra en lichess.org/signup para crear tu cuenta.",
    "CONTACT": "Escríbenos a contacto@chessattitude.com",
    
    # CASO 1: HUMAN -> El sistema funciona, pero el usuario dice cosas raras o saluda
    # Aquí es donde dices "No te entiendo" o das la bienvenida.
    "HUMAN": "Hola, soy el bot de Chess Attitude. No soy humano, así que solo puedo responder dudas sobre PRECIOS, HORARIOS o LICENCIAS.",
    
    # CASO 2: ERROR -> El sistema ha fallado (Internet caído, API rota)
    "ERROR": "⚠️ Lo siento, tengo un error técnico interno. Por favor intenta contactar por email."
}

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Main webhook entry point.
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        # 1. Detect intent
        intent = classify_intent(user_message)
        
        # 2. Get Response
        # Busca la respuesta en el diccionario. Si el intent llega raro, usa HUMAN.
        response_text = BOT_RESPONSES.get(intent, BOT_RESPONSES["HUMAN"])

        return jsonify({
            "response": response_text,
            "intent": intent
        })

    except Exception as e:
        # Error gravísimo del servidor Flask
        return jsonify({
            "response": BOT_RESPONSES["ERROR"],
            "intent": "CRITICAL_FAILURE"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)