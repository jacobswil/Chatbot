# FUL AI Agent

Streamlit chat assistant for Federal University Lokoja questions.
Chat input is pinned to the bottom and messages scroll upward, like ChatGPT/WhatsApp.

## Knowledge base
`knowledge/ful_dataset.json` uses the intents format (`tag`, `patterns`, `responses`, `source`).
It contains the 2026 FUL chatbot dataset plus extra entries added from the official website
(per-faculty admission requirements, portal links, news highlights, other site sections).
To add knowledge, append a new intent with several example questions in `patterns`.

## Setup
1. Install Python 3.10+
2. `pip install -r requirements.txt`
3. `streamlit run app.py`

## Local mode (default, free)
No API key needed. The agent finds the best matching intent and shows its answer.

## OpenAI mode
1. Copy `.env.example` to `.env`
2. Set `USE_OPENAI=true` and paste your key in `OPENAI_API_KEY`
3. Restart the app. Never put your key in the code.
The model answers only from the retrieved FUL entries. Greetings/thanks skip the API call.

## Features
- Conversation context (short follow-ups use the previous question)
- Source shown under answers
- Unknown questions get a polite "I don't know" (tune `MIN_SCORE` in `config.py`)
- Thumbs up/down feedback saved to `data/feedback.jsonl`

## Evaluation
Edit `data/test_questions.json` (`expected_id` = intent tag), then run
`python evaluation/evaluate.py` and adjust `MIN_SCORE` if needed.

## Keeping it current
Admission dates, fees, cut-off marks and office holders change often. Re-check
www.fulokoja.edu.ng each session and update the dataset.
