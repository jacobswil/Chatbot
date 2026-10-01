import os
from dotenv import load_dotenv

load_dotenv()

KB_PATH = "knowledge/ful_dataset.json"
FEEDBACK_PATH = "data/feedback.jsonl"
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
