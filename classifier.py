import os
import sys
import time
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Load environment variables
load_dotenv()

# 2. Securely retrieve the API Key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("CRITICAL ERROR: GEMINI_API_KEY not found in .env file.")
    sys.exit(1)

# 3. Configure Google Gemini Client
genai.configure(api_key=api_key)

# Constants for Intents (Standardized categories)
INTENT_PRICING = "PRICING"
INTENT_SCHEDULE = "SCHEDULE"
INTENT_FEDERATION = "FEDERATION"
INTENT_LICHESS = "LICHESS"
INTENT_HUMAN = "HUMAN"

def classify_intent(user_message: str) -> str:
    """
    Analyzes the user's message using Google Gemini Stable (Flash Latest).
    Returns the detected Intent Category.
    """
    
    # Configuration
    # Temperature 0.0 forces deterministic (non-creative) results.
    # Max output tokens increased to 100 to avoid cut-off errors.
    generation_config = {
        "temperature": 0.0,
        "max_output_tokens": 100, 
    }

    try:
        # We use 'gemini-flash-latest' for stability and free-tier compatibility.
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest", 
            generation_config=generation_config,
            system_instruction=f"""
            You are a strictly deterministic classifier for a Chess Academy bot.
            Classify the user input into ONE of these categories:
            
            - {INTENT_PRICING}: Questions about cost, price, money, payments.
            - {INTENT_SCHEDULE}: Questions about time, hours, calendar, thursday/friday.
            - {INTENT_FEDERATION}: Questions about official licenses, joining the federation.
            - {INTENT_LICHESS}: Questions about creating accounts, Lichess usage.
            - {INTENT_HUMAN}: Greetings, complex questions, or anything else.
            
            RULES:
            1. Reply ONLY with the category name (e.g. "{INTENT_PRICING}").
            2. Do not explain. Do not add punctuation.
            """
        )

        response = model.generate_content(user_message)
        
        # Safety check: Validate that the response contains text
        if not response.parts:
            return INTENT_HUMAN

        # Normalize response (remove spaces and convert to uppercase)
        detected_intent = response.text.strip().upper()
        return detected_intent

    except Exception as e:
        # Fallback to HUMAN if API fails or rate limit is exceeded
        print(f"⚠️ Error classifying (Probable Rate Limit): {e}")
        return INTENT_HUMAN

# --- UNIT TEST ---
if __name__ == "__main__":
    print("--- 🤖 STARTING GEMINI STABLE TEST (With Rate Limiting) ---")
    
    # Test phrases kept in Spanish to verify the bot understands the target language
    test_phrases = [
        "Hola buenas tardes",
        "Cuanto vale apuntarse?",
        "A que hora abris los jueves?",
        "Como me hago la cuenta en lichess?",
        "Quiero federarme ya"
    ]
    
    for phrase in test_phrases:
        print(f"User: '{phrase}'")
        intent = classify_intent(phrase)
        print(f" >> Gemini Detected: {intent}\n")
        
        # Rate Limiting: 2-second pause to respect the Free Tier quota
        time.sleep(2)