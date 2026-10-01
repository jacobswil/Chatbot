import html
import json
import re
import time
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

import config
from agent import FULAgent

st.set_page_config(page_title="FUL AI Agent", page_icon="🎓", layout="centered")

# ---------- Styling (WhatsApp / Messenger look) ----------
st.markdown(
    """
<style>
#MainMenu, footer, header[data-testid="stHeader"] {visibility: hidden; height: 0;}
.stApp {
    background-color: #efeae2;
    background-image: radial-gradient(#d9d2c5 1px, transparent 1px);
    background-size: 22px 22px;
}
.block-container {max-width: 760px; padding-top: 0 !important; padding-bottom: 7rem;}

/* Top bar */
.chat-header {
    position: sticky; top: 0; z-index: 50;
    display: flex; align-items: center; gap: 12px;
    margin: 0 -1rem 14px -1rem; padding: 12px 18px;
    background: #075e54; color: #fff;
    box-shadow: 0 2px 6px rgba(0,0,0,.25);
}
.chat-header .avatar {
    width: 42px; height: 42px; border-radius: 50%;
    background: #fff; display: flex; align-items: center; justify-content: center;
    font-size: 22px;
}
.chat-header .name {font-weight: 600; font-size: 17px; line-height: 1.2;}
.chat-header .status {font-size: 12.5px; opacity: .85;}
.chat-header .dot {
    display: inline-block; width: 8px; height: 8px; border-radius: 50%;
    background: #25d366; margin-right: 5px;
}

/* Message rows and bubbles */
.row {display: flex; margin: 3px 0; width: 100%;}
.row.user {justify-content: flex-end;}
.row.bot {justify-content: flex-start;}
.bubble {
    max-width: 78%; padding: 7px 11px 6px 11px; border-radius: 10px;
    font-size: 15.5px; line-height: 1.4; color: #111b21;
    box-shadow: 0 1px 1px rgba(0,0,0,.18); word-wrap: break-word; overflow-wrap: anywhere;
}
.bubble.user {background: #d9fdd3; border-top-right-radius: 2px;}
.bubble.bot  {background: #ffffff; border-top-left-radius: 2px;}
.bubble a {color: #027eb5; text-decoration: none;}
.bubble a:hover {text-decoration: underline;}
.meta {display: block; text-align: right; font-size: 11px; color: #667781; margin-top: 2px;}
.ticks {color: #53bdeb; margin-left: 3px;}

/* Thumbs under bot replies, kept small and out of the way */
[data-testid="stFeedback"] {margin: -2px 0 6px 6px; transform: scale(.8); transform-origin: left center;}

/* Typing bubble */
.typing {display: inline-flex; gap: 4px; padding: 4px 2px;}
.typing span {width: 7px; height: 7px; border-radius: 50%; background: #9aa5ab; animation: blink 1.2s infinite;}
.typing span:nth-child(2) {animation-delay: .2s;}
.typing span:nth-child(3) {animation-delay: .4s;}
@keyframes blink {0%, 80%, 100% {opacity: .25;} 40% {opacity: 1;}}

/* Input bar: dark box with white typing text */
[data-testid="stBottom"] > div, [data-testid="stBottomBlockContainer"] {background: #202c33 !important;}
[data-testid="stChatInput"], [data-testid="stChatInput"] > div {
    background: #2a3942 !important; border: none !important; border-radius: 26px;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important; color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important; caret-color: #ffffff !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #aebac1 !important; -webkit-text-fill-color: #aebac1 !important; opacity: 1 !important;
}
[data-testid="stChatInputSubmitButton"] {background: #128c7e !important; color: #fff !important; border-radius: 50%;}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def get_agent():
    return FULAgent()


agent = get_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

URL_RE = re.compile(r"((?:https?://|www\.)[^\s<]+[^\s<.,;:!?)\]])")


def bubble_html(text):
    """Escape the text, keep line breaks, and turn web addresses into links."""
    safe = html.escape(text).replace("\n", "<br>")

    def link(m):
        url = m.group(1)
        href = url if url.startswith("http") else "https://" + url
        return f'<a href="{href}" target="_blank" rel="noopener">{url}</a>'

    return URL_RE.sub(link, safe)


def render(role, text, stamp):
    ticks = '<span class="ticks">✓✓</span>' if role == "user" else ""
    st.markdown(
        f'<div class="row {role}"><div class="bubble {role}">{bubble_html(text)}'
        f'<span class="meta">{stamp}{ticks}</span></div></div>',
        unsafe_allow_html=True,
    )


def save_feedback(idx):
    value = st.session_state.get(f"fb_{idx}")
    if value is None:
        return
    Path(config.FEEDBACK_PATH).parent.mkdir(exist_ok=True)
    msgs = st.session_state.messages
    record = {
        "time": time.time(),
        "question": msgs[idx - 1]["content"] if idx > 0 else "",
        "answer": msgs[idx]["content"],
        "rating": "up" if value == 1 else "down",
    }
    with open(config.FEEDBACK_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


# ---------- Header ----------
st.markdown(
    """
<div class="chat-header">
  <div class="avatar">🎓</div>
  <div>
    <div class="name">FUL AI Agent</div>
    <div class="status"><span class="dot"></span>online · Federal University Lokoja</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- Conversation ----------
if not st.session_state.messages:
    render("bot", "Hello! 👋 I'm the Federal University Lokoja assistant. "
                  "Ask me about admissions, fees, faculties, portals and more.", time.strftime("%H:%M"))

for i, m in enumerate(st.session_state.messages):
    render("user" if m["role"] == "user" else "bot", m["content"], m.get("time", ""))
    if m["role"] == "assistant":
        st.feedback("thumbs", key=f"fb_{i}", on_change=save_feedback, args=(i,))

# ---------- Input ----------
if prompt := st.chat_input("Type a message"):
    history = list(st.session_state.messages)
    now = time.strftime("%H:%M")
    render("user", prompt, now)
    typing = st.empty()
    typing.markdown(
        '<div class="row bot"><div class="bubble bot"><div class="typing">'
        "<span></span><span></span><span></span></div></div></div>",
        unsafe_allow_html=True,
    )
    result = agent.answer(prompt, history)
    time.sleep(0.4)  # brief pause so the typing dots are visible
    typing.empty()
    st.session_state.messages.append({"role": "user", "content": prompt, "time": now})
    st.session_state.messages.append(
        {"role": "assistant", "content": result["answer"], "time": time.strftime("%H:%M")}
    )
    st.rerun()

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Settings")
    st.write("Mode:", "OpenAI" if agent.client else "Local (offline)")
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()

# Keep the newest message in view (skipped silently if this Streamlit version lacks the helper)
try:
    components.html(
        """<script>
        const d = window.parent.document;
        const el = d.querySelector('[data-testid="stMain"]') || d.querySelector('section.main') || d.documentElement;
        el.scrollTo({top: el.scrollHeight, behavior: 'smooth'});
        </script>""",
        height=0,
    )
except Exception:
    pass
