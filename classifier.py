import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load environment variables
load_dotenv()

# 2. Securely retrieve the API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("CRITICAL ERROR: OPENAI_API_KEY not found in .env file.")
    sys.exit(1)

# 3. Initialize the OpenAI Client
client = OpenAI(api_key=api_key)

# Constants for Intents (Avoid Magic Strings)
INTENT_PRICING = "PRICING"
INTENT_SCHEDULE = "SCHEDULE"
INTENT_FEDERATION = "FEDERATION"
INTENT_LICHESS = "LICHESS"
INTENT_HUMAN = "HUMAN"

def classify_intent(user_message: str) -> str:
    """
    Analyzes the user's message and returns the Intent Category.
    Uses GPT-4o-mini for cost-efficiency and speed.
    """
    
    system_prompt = f"""
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

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.0,  # 0.0 means maximum determinism (No creativity allowed)
            max_tokens=10
        )
        
        # Clean up the response
        detected_intent = response.choices[0].message.content.strip().upper()
        return detected_intent

    except Exception as e:
        print(f"Error classifying message: {e}")
        return INTENT_HUMAN

# --- UNIT TEST (This runs only if you execute this file directly) ---
if __name__ == "__main__":
    print("--- 🤖 STARTING DIAGNOSTIC TEST ---")
    
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
        print(f" >> AI Detected: {intent}\n")