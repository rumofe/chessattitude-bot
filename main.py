from flask import Flask, request, jsonify
from flask_cors import CORS  # <--- NUEVO: Importamos la librería
from classifier import classify_intent

app = Flask(__name__)
CORS(app)  # <--- NUEVO: Esto abre la puerta al navegador (Frontend)

# ==========================================
# 🟢 ZONA DE EDICIÓN: TUS RESPUESTAS
# ==========================================
BOT_RESPONSES = {
    "PRICING": """
    💰 <b>TARIFAS Y CUOTAS:</b><br><br>
    
    🏫 <b>CEIP Miguel Hernández (Benalmádena):</b><br>
    - Ajedrez en Infantil (4-7 años): <b>30€ niños</b>.<br>
    - Inicial/Intermedio: <b>30€ niño</b> | <b>40€ adultos</b>.<br>
    - <i>Oferta después de septiembre:</i> 30€ mensual y matrícula con camiseta de la escuela 15€.<br><br>
    
    🏫 <b>Escuela Municipal de Fuengirola:</b><br>
    - Inicial: <b>27€</b>.<br>
    - Intermedio/Avanzado: <b>35€</b>.<br><br>
    
    🏫 <b>Club de Ajedrez Miraflores (Málaga):</b><br>
    - Inicial/Intermedio: <b>33€</b>.<br>
    - Avanzado: <b>40€</b>.<br>
    - Adultos: <b>40€</b>.<br><br>
    
    🏫 <b>Colegio El Atabal (Málaga):</b><br>
    - Inicial/Intermedio: <b>30€</b>.
    """,
    "LOCATIONS": """
    📍 <b>Aquí tienes nuestras ubicaciones:</b><br><br>
    
    ❶ <b>Benalmádena:</b> <a href='https://www.google.com/maps/search/?api=1&query=Av.+Inmaculada+Concepción,+138,+Benalmádena' target='_blank'>Av. Inmaculada Concepción, 138</a><br>
    <i>(CEIP Miguel Hernández)</i><br><br>
    
    ❷ <b>Fuengirola:</b> <a href='https://www.google.com/maps/search/?api=1&query=Edificio+Colores,+Fuengirola' target='_blank'>Edificio Colores, 1ª Planta</a><br>
    <i>(Ayto. de Fuengirola)</i><br><br>
    
    ❸ <b>Málaga (Miraflores):</b> <a href='https://www.google.com/maps/search/?api=1&query=Calle+Bocanegra,+3,+Málaga' target='_blank'>C. Bocanegra, 3</a><br>
    <i>(Club de Ajedrez Miraflores)</i><br><br>
    
    ❹ <b>Málaga (El Atabal):</b> <a href='https://www.google.com/maps/search/?api=1&query=Av.+de+Lope+de+Vega,+12,+Málaga' target='_blank'>Av. de Lope de Vega, 12</a><br>
    <i>(Colegio El Atabal)</i>
    """,
    "SCHEDULE": """
    🕒 <b>Horarios por Sede:</b><br><br>
    
    🏫 <b>Benalmádena (Miguel Hernández):</b><br>
    📅 <i>Jueves</i><br>
    - Infantil y Niveles: 18:15 a 19:30<br><br>
    
    🏫 <b>Fuengirola (Edif. Colores):</b><br>
    📅 <i>Viernes</i><br>
    - Inicial: 16:30 a 18:00<br>
    - Intermedio/Avanzado: 18:00 a 19:30<br><br>
    
    🏫 <b>Málaga (Miraflores):</b><br>
    📅 <i>Lunes y Miércoles</i><br>
    - Inicial/Intermedio: 18:00 a 19:00<br>
    - Avanzado: 19:00 a 20:30<br><br>
    
    🏫 <b>Málaga (El Atabal):</b><br>
    📅 <i>Lunes y Miércoles</i><br>
    - Inicial/Intermedio: 13:45 a 14:45
    """,
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
@app.route('/ping', methods=['GET', 'POST'])
def ping():
    """Ruta sencilla para que el despertador no de error"""
    return "¡Estoy despierto!", 200
if __name__ == '__main__':
    print("--- ♟️ SERVER RUNNING (CORS ENABLED) ♟️ ---")
    app.run(host='0.0.0.0', port=5000, debug=True)