import unittest
import json
import time
from main import app, BOT_RESPONSES
from classifier import classify_intent, INTENT_PRICING, INTENT_HUMAN

class TestChessBot(unittest.TestCase):

    def setUp(self):
        """
        Executes BEFORE each test.
        Sets up a test client to simulate web requests without running the actual server.
        """
        self.app = app.test_client()
        self.app.testing = True

    # ====================================================
    # TEST 1: Verify Response Dictionary
    # ====================================================
    def test_responses_exist(self):
        """Checks that the configuration dictionary in main.py is valid and not empty."""
        print("\n🔎 Verifying response dictionary...")
        for intent, response in BOT_RESPONSES.items():
            self.assertIsInstance(response, str)
            self.assertTrue(len(response) > 0, f"Response for {intent} is empty!")
        print("✅ Dictionary Config OK.")

    # ====================================================
    # TEST 2: Verify Web Server (Flask)
    # ====================================================
    def test_webhook_structure(self):
        """Simulates a POST request to the webhook and verifies JSON structure."""
        print("\n🔎 Verifying Web Server endpoints...")
        
        # Simulate a frontend payload
        payload = {"message": "Hola"}
        response = self.app.post('/webhook', 
                                 data=json.dumps(payload),
                                 content_type='application/json')
        
        # 1. Server must respond with HTTP 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # 2. Response must be valid JSON
        data = response.get_json()
        self.assertIn('response', data)
        self.assertIn('intent', data)
        print("✅ Web Server (Flask) OK.")

    # ====================================================
    # TEST 3: Real AI Brain Test (PRICING)
    # ====================================================
    def test_ai_brain_pricing(self):
        """
        Sends a real phrase to Gemini and expects 'PRICING' classification.
        WARNING: This consumes API quota.
        """
        print("\n🔎 Verifying AI Brain Connection (Gemini)...")
        phrase = "Cuanto cuestan las clases?"
        intent = classify_intent(phrase)
        
        print(f"   Phrase: '{phrase}' -> Detected: {intent}")
        
        # We expect the AI to categorize this as PRICING
        self.assertEqual(intent, INTENT_PRICING)
        print("✅ AI Brain (Pricing Logic) OK.")
        
        # Safety pause for rate limiting during tests
        time.sleep(1)

    # ====================================================
    # TEST 4: Real AI Brain Test (Fallback/Human)
    # ====================================================
    def test_ai_brain_garbage(self):
        """
        Sends nonsense text to ensure the bot defaults to HUMAN/Fallback.
        """
        # "I like pineapple pizza" -> Should not trigger chess intents
        phrase = "Me gusta la pizza con piña" 
        intent = classify_intent(phrase)
        
        print(f"   Phrase: '{phrase}' -> Detected: {intent}")
        
        self.assertEqual(intent, INTENT_HUMAN)
        print("✅ AI Brain (Fallback Logic) OK.")

if __name__ == '__main__':
    unittest.main()