import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Cargar variables
load_dotenv()

# 2. API Key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("CRITICAL ERROR: GEMINI_API_KEY not found in .env file.")
    sys.exit(1)

# 3. Cliente Nuevo
client = genai.Client(api_key=api_key)

# Constants
INTENT_PRICING = "PRICING"
INTENT_SCHEDULE = "SCHEDULE"
INTENT_FEDERATION = "FEDERATION"
INTENT_LICHESS = "LICHESS"
INTENT_LOCATIONS = "LOCATIONS"
INTENT_CONTACT = "CONTACT"
INTENT_HUMAN = "HUMAN"
INTENT_TOURNAMENTS = "TOURNAMENTS"
INTENT_ERROR = "ERROR"
INTENT_TRIAL = "TRIAL_CLASS"
INTENT_MATERIAL = "MATERIAL"
INTENT_GREETING = "GREETING"
INTENT_CHANNEL = "CHANNEL"

def classify_intent(user_message: str) -> str:
    """
    Analiza el mensaje.
    IMPORTANTE: Ya no tiene try-except para que los errores (como el 429)
    suban hasta main.py y se puedan gestionar allí.
    """
    
    # --- LLAMADA DIRECTA (Sin red de seguridad aquí) ---
    response = client.models.generate_content(
        model='gemini-2.0-flash', # Asegúrate que este es el modelo que elegiste
        config=types.GenerateContentConfig(
            temperature=0.0, 
            max_output_tokens=50 
        ),
        contents=f"""
        You are a helpful assistant for a chess school (Chess Attitude).
        Classify the user's input into exactly one of the following categories:
        
        - {INTENT_PRICING}: Cost, price, money.
        - {INTENT_SCHEDULE}: Time, hours, calendar, days, when, schedule.
        - {INTENT_FEDERATION}: Federation, official license, registration, fees, insurance.
        - {INTENT_LICHESS}: Lichess, create account, sign up, register.
        - {INTENT_LOCATIONS}: Address, location, map, street, where are you.
        - {INTENT_GREETING}: Hola, hello, hi, good morning.
        - {INTENT_CHANNEL}: Youtube channel, videos, stream, recordings.
        - {INTENT_CONTACT}: Email, phone.
        - {INTENT_MATERIAL}: Access class material, password, lichess studies.
        - {INTENT_HUMAN}: Greetings, random chat, nonsense, human help.
        - {INTENT_TOURNAMENTS}: Competitions, blitz, rapid chess, trophies.
        - {INTENT_TRIAL}: Free trial, first class free, try out.
        
        Input: "{user_message}"
        
        RULES:
        1. Output ONLY the category name.
        2. If uncertain, output {INTENT_HUMAN}.
        3. Do NOT abbreviate.
        """
    )

    if not response.text:
        return INTENT_HUMAN # Si viene vacío, tratamos como humano por defecto

    detected = response.text.strip().upper()
    
    if detected == "HUM":
        return INTENT_HUMAN

    return detected