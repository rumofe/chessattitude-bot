import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Load environment variables
load_dotenv()

# 2. Securely retrieve the API Key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("CRITICAL ERROR: GEMINI_API_KEY not found in .env file.")
    sys.exit(1)

# 3. Configure the NEW Google GenAI Client
client = genai.Client(api_key=api_key)

# Constants for Intents
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
    Analyzes the user's message using the modern Google GenAI SDK.
    Returns the detected Intent Category.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            config=types.GenerateContentConfig(
                temperature=0.0, # Deterministic
                max_output_tokens=50 
            ),
            contents=f"""
            You are a helpful assistant for a chess school (Chess Attitude).
            Classify the user's input into exactly one of the following categories:
            
            - {INTENT_PRICING}: Cost, price, money.
            - {INTENT_SCHEDULE}: Time, hours, calendar, days, when, schedule, monday, tuesday, wednesday, thursday, friday.
            - {INTENT_FEDERATION}: Federation, official license, registration, fees, insurance, sign up, member card, join club.
            - {INTENT_LICHESS}: Lichess, create account, sign up, register, tutorial, how to create account, username, password.
            - {INTENT_LOCATIONS}: Address, location, map, street, where are you, place, google maps.
            - {INTENT_GREETING}: Hola, hello, hi, good morning, buenos dias, hey, saludos, tablerito.
            - {INTENT_CHANNEL}: Youtube channel, videos, stream, recordings, subscribe, watch games, analysis, content.
            - {INTENT_CONTACT}: Email, phone.
            - {INTENT_MATERIAL}: Access class material, password, lichess studies, openings, endings, classic games, strategy, tactics, homework.
            - {INTENT_HUMAN}: Greetings, random chat, nonsense.
            - {INTENT_TOURNAMENTS}: Competitions, blitz, rapid chess, matches, trophies, friday games.
            - {INTENT_TRIAL}: Free trial, first class free, try out, test class, no commitment.
            
            Input: "{user_message}"
            
            RULES:
            1. Output ONLY the category name.
            2. If uncertain, output {INTENT_HUMAN}.
            3. Do NOT abbreviate (e.g., write HUMAN, not HUM).
            """
        )

        if not response.text:
            return INTENT_ERROR

        detected = response.text.strip().upper()
        
        # 🛡️ Handle AI abbreviations
        if detected == "HUM":
            return INTENT_HUMAN

        return detected

    except Exception as e:
        print(f"⚠️ AI Error: {e}")
        return INTENT_ERROR

# --- UNIT TEST ---
if __name__ == "__main__":
    print("--- 🤖 DIAGNOSTIC ---")
    print(classify_intent("Hola"))