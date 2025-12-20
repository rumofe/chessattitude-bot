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
    "CONTACT": "Si tienes alguna duda adicional, contáctanos en info@chessattitude.com. Estaremos encantados de ayudarte.",
    "TOURNAMENTS": "Toda la información sobre nuestros torneos y resultados está disponible en el siguiente enlace: <a href='https://chessattitude.com/torneos-y-cronicas' target='_blank' style='color:#3498db; font-weight:bold;'>Ir a la Web de Torneos</a>",
    "TRIAL_CLASS": "¡Exacto! La primera clase es totalmente <b>GRATUITA y sin compromiso</b>. ♟️<br>Queremos que pruebes y conozcas a los profes. <br><br> <a href='https://api.whatsapp.com/send?phone=34600000000&text=Hola,%20quiero%20mi%20clase%20gratis' target='_blank' style='background:#27ae60; color:white; padding:10px 15px; text-decoration:none; border-radius:5px; font-weight:bold;'>📅 Reservar Clase Gratis</a>",    # RESPUESTA HUMAN
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