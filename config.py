import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("CRITICAL ERROR: GROQ_API_KEY not found in .env")

# Default Model
MODEL_NAME = "llama-3.3-70b-versatile"
TOTAL_ROUNDS = 8

# Global Temperature Control
# Default is 0.7 (Creative). If Seed is set, we switch to 0.0 (Deterministic).
TEMPERATURE = 0.7

def SET_DETERMINISTIC(is_deterministic: bool):
    global TEMPERATURE
    if is_deterministic:
        TEMPERATURE = 0.0