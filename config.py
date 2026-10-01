import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


def _find_kb():
    """Locate the dataset next to this file, whatever folder the app is started from."""
    wanted = BASE_DIR / "knowledge" / "ful_dataset.json"
    if wanted.exists():
        return str(wanted)
    # Fallbacks for uploads that landed in the wrong place
    for p in (BASE_DIR / "ful_dataset.json", *BASE_DIR.rglob("ful_dataset*.json")):
        if p.exists():
            return str(p)
    return str(wanted)  # missing: the error message will show exactly where it looked


KB_PATH = _find_kb()
FEEDBACK_PATH = str(BASE_DIR / "data" / "feedback.jsonl")
TOP_K = 3
MIN_SCORE = 0.20  # below this, the agent says it doesn't know (tune with evaluation/evaluate.py)
SMALLTALK_SCORE = 0.60
SKIP_TAGS = {"unknown_question"}
SMALLTALK_TAGS = {"greeting", "goodbye", "thanks", "chatbot_identity", "chatbot_capabilities"}
USE_OPENAI = os.getenv("USE_OPENAI", "false").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
UNKNOWN_REPLY = (
    "I'm sorry, I couldn't find that in my FUL information. "
    "Please check www.fulokoja.edu.ng or call +234 707 3199 972."
)
