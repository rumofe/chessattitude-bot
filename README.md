# ♟️ Chess Attitude Bot - Maintenance Manual

This bot uses Artificial Intelligence (Google Gemini) to classify user queries and respond automatically via a web API.

## 🛠️ How to Add New Topics (Intents)

The process always involves **2 STEPS**: Teaching the Brain (`classifier.py`) and Teaching the Mouth (`main.py`).

### STEP 1: The Brain (`classifier.py`)
Here we teach the AI to recognize the new intent.

1.  Open `classifier.py`.
2.  In the Constants section, add a new variable in UPPERCASE:
    ```python
    INTENT_TOURNAMENTS = "TOURNAMENTS"
    ```
3.  Scroll down to `classify_intent` and find the `contents` string. Add your new topic to the instruction list:
    ```python
    contents=f"""
    ...
    - {INTENT_CONTACT}: Email, phone.
    - {INTENT_TOURNAMENTS}: Summer tournaments, blitz, rapid chess, competitions.  <-- ADDED
    - {INTENT_HUMAN}: Greetings...
    """
    ```

### STEP 2: The Mouth (`main.py`)
Here we define what the bot actually says when that topic is detected.

1.  Open `main.py`.
2.  Find the `BOT_RESPONSES` dictionary.
3.  Add the exact response using the SAME KEY you defined in Step 1:
    ```python
    BOT_RESPONSES = {
        "PRICING": "...",
        # ...
        "TOURNAMENTS": "We organize Blitz tournaments every Friday at 19:00. Sign up on our website!",
        # ...
    }
    ```

### ✅ STEP 3: Verification
Always run the test suite before committing to ensure system stability:
```bash
python test_suite.py