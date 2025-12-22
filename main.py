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
    💰 <b>TARIFAS Y CUOTAS POR SEDE:</b><br><br>
    
    🏫 <b>CEIP Miguel Hernández (Benalmádena):</b><br>
    - <b>Ajedrez en Infantil:</b> 30€ niños (Curso adaptado de 4 a 7 años).<br>
    - <b>Inicial/Intermedio:</b> Precio niño 30€ | Adultos 40€.<br>
    🎁 <i>Oferta después de septiembre:</i> 30€ mensual y matrícula con camiseta de la escuela 15€.<br><br>
    
    🏫 <b>Escuela Municipal de Fuengirola:</b><br>
    - <b>Inicial:</b> Precio 27€.<br>
    - <b>Intermedio/Avanzado:</b> Precio 35€.<br><br>
    
    🏫 <b>Club de Ajedrez Miraflores (Málaga):</b><br>
    - <b>Inicial/Intermedio:</b> Precio 33€.<br>
    - <b>Avanzado:</b> Precio 40€.<br>
    - <b>Adultos:</b> 40€.<br><br>
    
    🏫 <b>Colegio El Atabal (Málaga):</b><br>
    - <b>Inicial/Intermedio:</b> Precio 30€.
    """,
    "LOCATIONS": """
    📍 <b>Aquí tienes nuestras ubicaciones:</b><br><br>
    
    ❶ <b>Benalmádena:</b> <a href='https://www.google.com/maps/search/?api=1&query=Av.+Inmaculada+Concepción,+138,+Benalmádena' target='_blank'>Av. Inmaculada Concepción, 138</a><br>
    <i>(CEIP Miguel Hernández)</i><br><br>
    
    ❷ <b>Fuengirola:</b> <a href='https://www.google.com/maps/search/?api=1&query=Edificio+Colores,+Fuengirola' target='_blank'>Edificio Colores, 1ª Planta</a><br>
    <i>(Ayto. de Fuengirola)</i><br><br>
    
    ❸ <b>Málaga (Club Ajedrez Miraflores):</b> <a href='https://www.google.com/maps/search/?api=1&query=Calle+Bocanegra,+3,+Málaga' target='_blank'>C. Bocanegra, 3</a><br>
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
    "MATERIAL": """
    📚 <b>Material de Clase (Estudios Lichess):</b><br>
    Aquí subimos las <b>aperturas, finales y partidas clásicas</b> que vemos en clase para que repases.<br><br>
    
    1️⃣ Entra aquí: <a href='https://chessattitude.com/material-clases-ajedrez' target='_blank' style='text-decoration:none; color:#2980b9; font-weight:bold;'>🔐 Zona de Alumnos</a><br>
    2️⃣ Usa la <b>contraseña</b> de tu profesor.<br>
    3️⃣ ⚠️ <b>Importante:</b> Inicia sesión en Lichess antes de entrar.<br><br>
    
    ¿No tienes cuenta? Pregúntame: <i>"¿Cómo crear cuenta en Lichess?"</i>
    """,
    "FEDERATE": """
    🏆 <b>Cómo Federarse (Temporada 2026):</b><br>
    ¡Genial! Federarse es necesario para jugar torneos oficiales.<br><br>
    
    📋 <b>Precios Oficiales de Licencias:</b><br>
    - 🧒 <b>Sub-08:</b> 22,00 €<br>
    - 👦 <b>Sub-18:</b> 38,00 €<br>
    - 👨 <b>Senior (Adultos):</b> 50,00 €<br>
    - 🦅 <b>Independiente:</b> 63,00 €<br>
    - 🎫 <i>Habilitante (solo 1 torneo):</i> 2,00 €<br><br>
    
    💳 <b>Datos para el pago:</b><br>
    Haz una transferencia o ingreso a:<br>
    <b>IBAN:</b> ES89 0182 3427 5702 0160 2674<br>
    <b>Titular:</b> Club Ajedrez Miraflores de los Angeles<br>
    <b>Concepto:</b> "LICENCIA + Nombre y Apellidos del jugador"<br><br>
    
    ⚠️ <b>Importante:</b> Una vez pagado, envía el justificante por WhatsApp al director o al email de contacto para tramitarlo.
    """,
    "LICHESS": """
    ♟️ <b>GUÍA: Cómo crear tu cuenta GRATIS en Lichess</b><br><br>
    
    1️⃣ <b>Entra al registro:</b><br>
    Haz clic aquí: <a href='https://lichess.org/signup' target='_blank' style='color:#2980b9; font-weight:bold;'>🔗 Crear Cuenta en Lichess.org</a><br><br>
    
    2️⃣ <b>Rellena los datos:</b><br>
    Elige un nombre de usuario, contraseña y pon tu email real.<br><br>
    
    3️⃣ <b>⚠️ IMPORTANTE: Los Semáforos</b><br>
    Verás 4 frases con un botón rojo al lado. Tienes que hacer clic en <b>TODAS</b> para ponerlas en 🟢 <b>VERDE</b>.<br>
    <i>(Prometes no usar ayuda de ordenadores, ser amable, etc.)</i><br><br>
    
    4️⃣ <b>Confirma tu correo:</b><br>
    Te llegará un email de Lichess. Ábrelo y pulsa el enlace para activar la cuenta.<br><br>
    
    ¡Y listo! Ya puedes jugar y acceder al material de clase. 🎉

    Tutorial en vídeo y como acceder a torneos: <a href='https://www.youtube.com/watch?v=W4_zCjhD5Pc' target='_blank' style='color:#2980b9; font-weight:bold;'>
    """,
    "GREETING": """
    ¡Hola! Soy <b>Tablerito</b> ♟️😃<br>
    La mascota y asistente virtual de <i>Chess Attitude</i>.<br><br>
    Estoy aquí para resolver tus dudas sobre <b>horarios, precios, torneos</b> o lo que necesites.<br>
    ¿En qué puedo ayudarte hoy?
    """,
    "CONTACT": "Si tienes alguna duda adicional, contáctanos en info@chessattitude.com. Estaremos encantados de ayudarte.",
    "TOURNAMENTS": "Toda la información sobre nuestros torneos y resultados está disponible en el siguiente enlace: <a href='https://chessattitude.com/torneos-y-cronicas' target='_blank' style='color:#3498db; font-weight:bold;'>Ir a la Web de Torneos</a>",
    "TRIAL_CLASS": "¡Exacto! La primera clase es totalmente <b>GRATUITA y sin compromiso</b>. ♟️<br>Queremos que pruebes y conozcas a los profes. <br><br> <a href='https://api.whatsapp.com/send?phone=34600000000&text=Hola,%20quiero%20mi%20clase%20gratis' target='_blank' style='background:#27ae60; color:white; padding:10px 15px; text-decoration:none; border-radius:5px; font-weight:bold;'>📅 Reservar Clase Gratis</a>",
    "HUMAN": """
    📞 <b>¿Prefieres hablar con un profe?</b><br><br>
    ¡Sin problema! A veces los humanos se explican mejor que yo. 😅<br><br>
    Puedes contactar directamente en:<br>
    📧 <b>Email:</b> info@chessattitude.com<br><br>
    """,
    
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