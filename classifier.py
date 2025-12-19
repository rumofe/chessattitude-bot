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
INTENT_CONTACT = "CONTACT"
INTENT_HUMAN = "HUMAN"
INTENT_ERROR = "ERROR"

def classify_intent(user_message: str) -> str:
    """
    Analyzes the user's message using the modern Google GenAI SDK.
    Returns the detected Intent Category.
    """
    
    try:
        # 🔴 CAMBIO ESTRATÉGICO: 'gemini-flash-lite-latest'
        # Este modelo está diseñado para alta concurrencia y tareas rápidas.
        # Es ideal para un chatbot que recibe muchas consultas simultáneas.
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            config=types.GenerateContentConfig(
                temperature=0.0, # Deterministic
                max_output_tokens=50 
            ),
            contents=f"""
            You are a classifier. Classify the input into ONE category:
            
            - {INTENT_PRICING}: Cost, price, money.
            - {INTENT_SCHEDULE}: Time, hours, calendar.
            - {INTENT_FEDERATION}: Licenses, FIDA.
            - {INTENT_LICHESS}: Accounts, online.
            - {INTENT_CONTACT}: Email, phone.
            - {INTENT_HUMAN}: Greetings, random chat, nonsense.
            
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