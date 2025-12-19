from flask import Flask, request, jsonify
from flask_cors import CORS  # <--- NUEVO: Importamos la librería
from classifier import classify_intent

app = Flask(__name__)
CORS(app)  # <--- NUEVO: Esto abre la puerta al navegador (Frontend)

# ==========================================
# 🟢 ZONA DE EDICIÓN: TUS RESPUESTAS
# ==========================================
BOT_RESPONSES = {
    "PRICING": "Nuestras tarifas son 30€/mes por 1 clase semanal.",
    "SCHEDULE": "Abrimos de Lunes a Viernes de 17:00 a 20:00.",
    "FEDERATION": "Para federarte necesitas rellenar el formulario FIDA.",
    "LICHESS": "Entra en lichess.org/signup para crear tu cuenta.",
    "CONTACT": "Escríbenos a contacto@chessattitude.com",
    "TOURNAMENTS": "Organizamos torneos Blitz todos los viernes a las 19:00. ¡Apúntate en la web!",
    
    # RESPUESTA HUMAN
    "HUMAN": "Hola, soy el bot de Chess Attitude. No soy humano, solo puedo responder dudas sobre PRECIOS, HORARIOS, LICENCIAS o LICHESS.",
    
    # RESPUESTA ERROR
    "ERROR": "⚠️ Lo siento, tengo un error técnico interno de conexión. Por favor intenta más tarde."
}

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Punto de entrada principal. Recibe el mensaje, piensa y responde.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        user_message = data.get('message', '')
        
        # 1. El Cerebro piensa (Gemini)
        intent = classify_intent(user_message)
        
        # 2. Buscamos la respuesta en el diccionario
        response_text = BOT_RESPONSES.get(intent, BOT_RESPONSES["HUMAN"])

        return jsonify({
            "response": response_text,
            "intent": intent
        })

    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({
            "response": BOT_RESPONSES["ERROR"],
            "intent": "CRITICAL_FAILURE"
        }), 500

if __name__ == '__main__':
    print("--- ♟️ SERVER RUNNING (CORS ENABLED) ♟️ ---")
    app.run(host='0.0.0.0', port=5000, debug=True)