import streamlit as st
import random
import html
import re
import difflib

# ============================================================
# FUL CHATBOT FOR ENQUIRY AND INFORMATION
# Fully offline application
# ============================================================

st.set_page_config(
    page_title="FUL Chatbot for Enquiry and Information",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------------------------------------------

# ------------------------------------------------------------
# Chatbot knowledge base
# ------------------------------------------------------------
INTENTS_DATA = {
    "intents": [
        {
            "tag": "greeting",
            "patterns": [
                "hi", "hello", "hey", "heyy", "good day", "good morning",
                "good afternoon", "good evening", "how are you?", "is anyone there?",
                "what's up", "how are ya", "whatsup"
            ],
            "responses": [
                "Hello! Welcome to the FUL Enquiry and Information Chatbot.",
                "Good to see you. How can I help you with Federal University Lokoja information?",
                "Hello! What would you like to know about FUL?"
            ]
        },
        {
            "tag": "goodbye",
            "patterns": [
                "bye", "bye bye", "goodbye", "see you", "see you later",
                "i am leaving", "have a good day", "talk to you later", "ttyl", "gtg"
            ],
            "responses": [
                "Goodbye! Have a great day.",
                "Thank you for using the FUL Enquiry Chatbot. See you again.",
                "Goodbye! Feel free to return whenever you need information."
            ]
        },
        {
            "tag": "creator",
            "patterns": [
                "who created you", "who made you", "who designed you",
                "who are your developers", "your developers", "your creators",
                "who is your creator", "who developed you"
            ],
            "responses": [
                "I was developed as an academic chatbot project for Federal University Lokoja enquiries."
            ]
        },
        {
            "tag": "name",
            "patterns": [
                "name", "your name", "what is your name", "whats your name",
                "what are you called", "who are you", "what am i chatting to",
                "who is this"
            ],
            "responses": [
                "I am the FUL Chatbot for Enquiry and Information.",
                "You can call me the FUL Enquiry Chatbot."
            ]
        },
        {
            "tag": "hours",
            "patterns": [
                "university timing", "university hours", "working hours",
                "what are your hours", "when is the university open",
                "when should i come to university", "is university open on saturday"
            ],
            "responses": [
                "University administrative opening hours may vary by office. Please confirm with the relevant FUL office or department."
            ]
        },
        {
            "tag": "number",
            "patterns": [
                "contact info", "contact information", "how to contact university",
                "university telephone number", "university number", "phone number",
                "phone no", "how can i contact you", "how can i call you", "call"
            ],
            "responses": [
                "For official contact information, please visit the Federal University Lokoja website or contact the appropriate university office."
            ]
        },
        {
            "tag": "course",
            "patterns": [
                "list of courses", "list of courses offered", "courses offered",
                "courses available", "what courses are offered", "what are the courses",
                "courses in federal university lokoja", "courses in ful", "computer science",
                "computer engineering", "information technology", "mechanical engineering",
                "civil engineering", "chemical engineering"
            ],
            "responses": [
                "Federal University Lokoja offers programmes across several faculties and departments. For the current and complete list of programmes, check the official FUL admission information."
            ]
        },
        {
            "tag": "fees",
            "patterns": [
                "fee", "fees", "school fees", "university fee", "school fee",
                "fee per semester", "how much is the fees", "how much are the fees",
                "fees for first year", "about the fees", "hostel fees"
            ],
            "responses": [
                "School charges and fees can change by programme and session. Please check the current official FUL fee information before making payment."
            ]
        },
        {
            "tag": "location",
            "patterns": [
                "where is the university located", "where is university located",
                "university location", "university address", "address of university",
                "how to reach university", "where is ful", "location"
            ],
            "responses": [
                "Federal University Lokoja is located in Lokoja, Kogi State, Nigeria. The permanent site is along the Lokoja-Okene Expressway at Felele."
            ]
        },
        {
            "tag": "hostel",
            "patterns": [
                "hostel", "hostel facility", "hostel facilities", "hostel location",
                "hostel fees", "does university provide hostel", "is there any hostel",
                "do you have hostel", "where is hostel", "hostel capacity"
            ],
            "responses": [
                "Hostel availability, accommodation arrangements and charges should be confirmed from the current FUL accommodation information or the appropriate university office."
            ]
        },
        {
            "tag": "event",
            "patterns": [
                "events", "events organised", "list of events", "university events",
                "what events are conducted", "are there any events", "event information"
            ],
            "responses": [
                "University events may include academic, cultural, sporting and student activities. Check official FUL announcements for current events."
            ]
        },
        {
            "tag": "document",
            "patterns": [
                "documents", "documents needed", "documents required",
                "documents needed for admission", "what documents do i need",
                "which document to bring for admission", "admission documents"
            ],
            "responses": [
                "Required documents depend on the admission process. Applicants should check the current FUL admission requirements for the exact documents required."
            ]
        },
        {
            "tag": "syllabus",
            "patterns": [
                "syllabus", "course outline", "course content", "timetable",
                "what is next lecture", "lecture timetable", "academic timetable"
            ],
            "responses": [
                "Course outlines and lecture timetables are normally provided through the relevant department or faculty. Please check with your department for the current version."
            ]
        },
        {
            "tag": "library",
            "patterns": [
                "library", "is there any library", "library facility",
                "library facilities", "do you have library", "university library",
                "where can i get books", "library information", "library books"
            ],
            "responses": [
                "FUL provides library services for students and staff. For current opening hours, facilities and services, please check with the university library."
            ]
        },
        {
            "tag": "infrastructure",
            "patterns": [
                "infrastructure", "university infrastructure", "how is university infrastructure"
            ],
            "responses": [
                "Federal University Lokoja has academic, administrative and student facilities supporting teaching, learning and university activities."
            ]
        },
        {
            "tag": "canteen",
            "patterns": [
                "canteen", "food facilities", "canteen facility", "is there any canteen",
                "does university have canteen", "where is canteen", "cafeteria", "food"
            ],
            "responses": [
                "Food and refreshment services may be available around the university environment. Students can check the campus facilities and approved vendors for current options."
            ]
        },
        {
            "tag": "menu",
            "patterns": [
                "food menu", "food in canteen", "what is on the menu",
                "what is available in university canteen", "what foods can we get",
                "what is there to eat"
            ],
            "responses": [
                "Available food depends on the food vendors operating on campus. Students can check the current options available around the university."
            ]
        },
        {
            "tag": "placement",
            "patterns": [
                "placement", "recruitment", "companies", "companies visit",
                "career", "job opportunities", "industrial training"
            ],
            "responses": [
                "Career, industrial training and employment opportunities may be coordinated through relevant departments and university units. Check current FUL announcements for available opportunities."
            ]
        },
        {
            "tag": "HOD",
            "patterns": [
                "who is hod", "where is hod", "hod name", "name of hod", "hod"
            ],
            "responses": [
                "HODs differ by department. Please specify the department if you need information about a particular HOD."
            ]
        },
        {
            "tag": "VC",
            "patterns": [
                "what is the name of vc", "vice chancellor", "vice chancellor name",
                "vc name", "who is university vc", "where is vc office",
                "who is the vc", "who is the vc of federal university lokoja"
            ],
            "responses": [
                "For the current Vice Chancellor and other principal officers, please confirm the latest information from the official Federal University Lokoja website."
            ]
        },
        {
            "tag": "sem",
            "patterns": [
                "exam dates", "exam schedule", "when is semester exam",
                "semester exam timetable", "exam", "when is exam", "exam timetable",
                "semester"
            ],
            "responses": [
                "Examination dates and timetables are subject to the current academic calendar. Please check official FUL academic announcements."
            ]
        },
        {
            "tag": "admission",
            "patterns": [
                "what is the process of admission", "what is the admission process",
                "how to take admission", "process for admission", "admission",
                "admission process", "how can i gain admission", "how do i apply"
            ],
            "responses": [
                "Admission requirements and procedures depend on the programme and admission route. Applicants should check the current FUL admission guidelines before applying."
            ]
        },
        {
            "tag": "scholarship",
            "patterns": [
                "scholarship", "is scholarship available", "available scholarships",
                "list of scholarship", "scholarship for students", "student scholarship"
            ],
            "responses": [
                "Scholarship opportunities may be available from government bodies, organisations and other sponsors. Students should check current official announcements for available opportunities."
            ]
        },
        {
            "tag": "facilities",
            "patterns": [
                "what facilities university provide", "university facility",
                "what are the university facilities", "facilities", "facilities provided"
            ],
            "responses": [
                "University facilities include academic buildings, lecture spaces, laboratories, library services, administrative offices and other student support facilities."
            ]
        },
        {
            "tag": "college intake",
            "patterns": [
                "max number of students", "number of seats per class",
                "maximum number of seats", "maximum students intake",
                "what is university intake", "how many students are taken",
                "seat allocation", "seats"
            ],
            "responses": [
                "Student intake varies by programme and admission requirements. The approved number of students depends on the relevant programme and session."
            ]
        },
        {
            "tag": "uniform",
            "patterns": [
                "university dress code", "dress code", "what is the uniform",
                "can we wear casuals", "does university have uniform",
                "is there any uniform", "uniform"
            ],
            "responses": [
                "Dress requirements may differ by programme or activity. Students should follow the dress guidelines provided by their faculty or department."
            ]
        },
        {
            "tag": "committee",
            "patterns": [
                "committee", "different committee in university",
                "are there any committee", "committee details"
            ],
            "responses": [
                "The university has different committees and administrative structures. For a specific committee, please contact the relevant university unit."
            ]
        },
        {
            "tag": "random",
            "patterns": [
                "i love you", "will you marry me", "do you love me"
            ],
            "responses": [
                "I am here to help with Federal University Lokoja enquiries. Please ask me a university related question."
            ]
        },
        {
            "tag": "swear",
            "patterns": [
                "fuck", "bitch", "shut up", "stupid", "idiot", "dumb ass",
                "asshole", "fucker"
            ],
            "responses": [
                "Please use appropriate language and ask a university related question."
            ]
        },
        {
            "tag": "vacation",
            "patterns": [
                "holidays", "when will semester start", "when will semester end",
                "when are the holidays", "holiday list", "vacation",
                "when is vacation", "how long will be the vacation"
            ],
            "responses": [
                "Vacation and semester dates are determined by the current academic calendar. Please check the latest official FUL academic calendar."
            ]
        },
        {
            "tag": "sports",
            "patterns": [
                "sports", "sports and games", "sports facilities",
                "sports infrastructure", "sports activities", "information about sports"
            ],
            "responses": [
                "Students can participate in sporting activities organised through the university and student community. Check current campus announcements for activities."
            ]
        },
        {
            "tag": "salutaion",
            "patterns": [
                "ok", "okay", "okk", "okie", "nice work", "well done",
                "good job", "thank you", "thanks", "its ok", "k"
            ],
            "responses": [
                "You are welcome. Is there anything else you would like to know about FUL?",
                "Glad I could help. Feel free to ask another question."
            ]
        },
        {
            "tag": "task",
            "patterns": [
                "what can you do", "what are the things you can do",
                "things you can do", "how can you help me", "why should i use you"
            ],
            "responses": [
                "I can provide automated answers to common Federal University Lokoja enquiries, including admission, courses, fees, accommodation, facilities and general student information."
            ]
        }
    ]
}

# ------------------------------------------------------------
# Build lookup tables
# ------------------------------------------------------------
tag_to_responses = {
    intent["tag"]: intent["responses"]
    for intent in INTENTS_DATA["intents"]
}

pattern_lookup = []
for intent in INTENTS_DATA["intents"]:
    for pattern in intent["patterns"]:
        pattern_lookup.append((pattern.lower().strip(), intent["tag"]))

all_patterns = [p for p, _ in pattern_lookup]


def preprocess_text(text):
    return re.sub(r"\s+", " ", text.lower().strip())


def match_tag(processed_input, cutoff=0.68):
    # 1. Exact match
    for pattern, tag in pattern_lookup:
        if processed_input == pattern:
            return tag

    # 2. Phrase / word matching
    best_tag = None
    best_len = 0

    for pattern, tag in pattern_lookup:
        if len(pattern.split()) <= 7:
            if re.search(r"\b" + re.escape(pattern) + r"\b", processed_input):
                if len(pattern) > best_len:
                    best_len = len(pattern)
                    best_tag = tag

    if best_tag:
        return best_tag

    # 3. Fuzzy matching
    close = difflib.get_close_matches(
        processed_input,
        all_patterns,
        n=1,
        cutoff=cutoff
    )

    if close:
        matched_pattern = close[0]
        for pattern, tag in pattern_lookup:
            if pattern == matched_pattern:
                return tag

    return None


def get_response(user_input):
    tag = match_tag(preprocess_text(user_input))

    if tag and tag in tag_to_responses:
        return random.choice(tag_to_responses[tag])

    return (
        "I could not find a suitable answer for that enquiry. "
        "Please try asking about admission, courses, fees, hostel, "
        "location, library, examinations or other FUL services."
    )


# ------------------------------------------------------------
# CSS - completely redesigned interface
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Main application */
    .stApp {
        background: #f1eee7;
        color: #17201c;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Hide Streamlit decoration */
    #MainMenu, footer, header {
        visibility: hidden;
    }

    /* Top navigation */
    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 4px 22px 4px;
        border-bottom: 1px solid #d6d1c7;
        margin-bottom: 28px;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 13px;
    }

    .brand-mark {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: #17201c;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #f2c76e;
        font-size: 23px;
        font-weight: 800;
    }

    .brand-text {
        line-height: 1.1;
    }

    .brand-text strong {
        display: block;
        font-size: 17px;
        letter-spacing: .4px;
    }

    .brand-text span {
        display: block;
        font-size: 11px;
        color: #77736c;
        margin-top: 4px;
        letter-spacing: 1.3px;
        text-transform: uppercase;
    }

    .status-pill {
        border: 1px solid #c9c3b8;
        border-radius: 999px;
        padding: 8px 13px;
        font-size: 12px;
        color: #4f554f;
        background: #f8f6f1;
    }

    .status-dot {
        display: inline-block;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #4b8b65;
        margin-right: 7px;
    }

    /* Hero */
    .hero {
        background: #17201c;
        border-radius: 28px;
        min-height: 315px;
        padding: 34px 42px;
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 18px 45px rgba(31, 35, 31, .12);
    }

    .hero:before {
        content: "";
        position: absolute;
        width: 360px;
        height: 360px;
        border-radius: 50%;
        border: 1px solid rgba(242,199,110,.18);
        right: -130px;
        top: -145px;
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        border-radius: 50%;
        border: 1px solid rgba(242,199,110,.12);
        right: -50px;
        bottom: -155px;
    }

    .hero-copy {
        max-width: 650px;
        z-index: 2;
    }

    .eyebrow {
        color: #f2c76e;
        text-transform: uppercase;
        font-size: 11px;
        letter-spacing: 3px;
        font-weight: 700;
        margin-bottom: 14px;
    }

    .hero h1 {
        color: #ffffff;
        font-size: 42px;
        line-height: 1.06;
        margin: 0;
        letter-spacing: -1.3px;
        font-family: Georgia, "Times New Roman", serif;
    }

    .hero p {
        color: #c9d0ca;
        margin-top: 17px;
        font-size: 15px;
        line-height: 1.65;
        max-width: 610px;
    }

        color: #7c786f;
        font-weight: 800;
        margin: 30px 0 12px 2px;
    }

    .info-card {
        background: #faf8f3;
        border: 1px solid #dcd7ce;
        border-radius: 18px;
        padding: 18px 19px;
        height: 100%;
        box-shadow: 0 5px 18px rgba(45,45,40,.04);
    }

    .info-icon {
        font-size: 20px;
        margin-bottom: 9px;
    }

    .info-card strong {
        font-size: 14px;
        display: block;
        margin-bottom: 5px;
    }

    .info-card span {
        font-size: 12px;
        color: #77736b;
        line-height: 1.5;
    }

    /* Quick buttons */
    div.stButton > button {
        border: 1px solid #cfc9bf !important;
        background: #faf8f3 !important;
        color: #28302b !important;
        border-radius: 13px !important;
        min-height: 48px !important;
        font-size: 13px !important;
        transition: all .2s ease !important;
    }

    div.stButton > button:hover {
        border-color: #17201c !important;
        background: #17201c !important;
        color: #ffffff !important;
        transform: translateY(-1px);
    }

    /* Chat area */
    .chat-panel {
        background: #faf8f3;
        border: 1px solid #dcd7ce;
        border-radius: 24px;
        padding: 24px;
        margin-top: 12px;
        box-shadow: 0 8px 25px rgba(45,45,40,.05);
    }

    .chat-heading {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 17px;
        border-bottom: 1px solid #e3ded5;
        margin-bottom: 18px;
    }

    .chat-heading strong {
        font-family: Georgia, "Times New Roman", serif;
        font-size: 22px;
    }

    .chat-heading span {
        font-size: 11px;
        color: #858077;
    }

    .message-row {
        display: flex;
        margin: 14px 0;
    }

    .message-row.user {
        justify-content: flex-end;
    }

    .message-row.bot {
        justify-content: flex-start;
    }

    .bubble {
        max-width: 76%;
        padding: 13px 16px;
        border-radius: 17px;
        font-size: 13px;
        line-height: 1.6;
    }

    .user-bubble {
        background: #24352c;
        color: #ffffff;
        border-bottom-right-radius: 5px;
    }

    .bot-bubble {
        background: #ece8df;
        color: #252b27;
        border-bottom-left-radius: 5px;
    }

    .bot-label {
        display: block;
        color: #697169;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
        font-weight: 800;
    }

    /* Input */
    .stTextInput > div > div > input {
        background: #faf8f3 !important;
        border: 1px solid #cfc9bf !important;
        color: #17201c !important;
        border-radius: 14px !important;
        padding: 14px !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #24352c !important;
        box-shadow: 0 0 0 1px #24352c !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #858077;
        font-size: 11px;
        padding: 28px 0 8px;
        letter-spacing: .4px;
    }

    /* Responsive */
    @media (max-width: 800px) {
        .hero {
            padding: 28px;
        }

        .hero h1 {
            font-size: 31px;
        }


        .bubble {
            max-width: 88%;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------

st.markdown(
    """
    <div class="topbar">
        <div class="brand">
            <div class="brand-mark">FUL</div>
            <div class="brand-text">
                <strong>Federal University Lokoja</strong>
                <span>Enquiry & Information Centre</span>
            </div>
        </div>
        <div class="status-pill">
            <span class="status-dot"></span>Offline Assistant
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
st.markdown(
    f"""
    <div class="hero">
        <div class="hero-copy">
            <div class="eyebrow">Student Information Service</div>
            <h1>FUL Chatbot for<br>Enquiry and Information</h1>
            <p>
                Get quick answers to common questions about Federal University
                Lokoja, including admission, courses, fees, accommodation,
                examinations, facilities and general student enquiries.
            </p>
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# Quick enquiry cards
# ------------------------------------------------------------
st.markdown('<div class="section-label">Popular enquiries</div>', unsafe_allow_html=True)

quick_cards = [
    ("🎓", "Admission", "Application and admission process"),
    ("📚", "Courses", "Programmes offered at FUL"),
    ("💳", "Fees", "School charges and payments"),
    ("🏠", "Hostel", "Accommodation information"),
]

card_cols = st.columns(4)

for col, (icon, title, description) in zip(card_cols, quick_cards):
    with col:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-icon">{icon}</div>
                <strong>{title}</strong>
                <span>{description}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

# ------------------------------------------------------------
# Quick question buttons
# ------------------------------------------------------------
st.markdown('<div class="section-label">Quick questions</div>', unsafe_allow_html=True)

suggested_questions = [
    "What is the admission process?",
    "What courses are offered?",
    "How much are the school fees?",
    "Do you have hostel?",
    "Where is Federal University Lokoja located?",
    "Who is the Vice Chancellor?",
]

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "pending_input" not in st.session_state:
    st.session_state["pending_input"] = ""

if "clear_chat" not in st.session_state:
    st.session_state["clear_chat"] = False

button_cols = st.columns(3)

for i, question in enumerate(suggested_questions):
    with button_cols[i % 3]:
        if st.button(question, key=f"quick_{i}", use_container_width=True):
            st.session_state["pending_input"] = question

# ------------------------------------------------------------
# Chat panel
# ------------------------------------------------------------
st.markdown(
    """
    <div class="chat-heading">
        <strong>Ask FUL</strong>
        <span>Answers are generated from the local knowledge base</span>
    </div>
    """,
    unsafe_allow_html=True
)

# Clear button
clear_col1, clear_col2 = st.columns([7, 1])

with clear_col2:
    if st.button("Clear chat", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

# ------------------------------------------------------------
# Process quick question
# ------------------------------------------------------------
pending = st.session_state.get("pending_input", "")

if pending:
    response = get_response(pending)
    st.session_state["messages"].append(("user", pending))
    st.session_state["messages"].append(("bot", response))
    st.session_state["pending_input"] = ""
    st.rerun()

# ------------------------------------------------------------
# Display messages
# ------------------------------------------------------------
if not st.session_state["messages"]:
    st.markdown(
        """
        <div style="
            background:#ece8df;
            border-radius:17px;
            padding:18px;
            color:#5d625d;
            font-size:13px;
            line-height:1.6;
            margin-bottom:18px;
        ">
            <span style="font-size:18px;">👋</span>
            <strong> Welcome to the FUL Enquiry Centre.</strong><br>
            Ask a question above or choose one of the quick enquiries to get started.
        </div>
        """,
        unsafe_allow_html=True
    )

for sender, msg in st.session_state["messages"]:
    safe_msg = html.escape(str(msg)).replace("\n", "<br>")

    if sender == "user":
        st.markdown(
            f"""
            <div class="message-row user">
                <div class="bubble user-bubble">{safe_msg}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="message-row bot">
                <div class="bubble bot-bubble">
                    <span class="bot-label">FUL Assistant</span>
                    {safe_msg}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ------------------------------------------------------------
# User input
# ------------------------------------------------------------
def submit_question():
    question = st.session_state.get("user_input", "").strip()
    if not question:
        return

    response = get_response(question)
    st.session_state["messages"].append(("user", question))
    st.session_state["messages"].append(("bot", response))

    # Clear the input after processing so the same question is not
    # submitted again on Streamlit's next rerun.
    st.session_state["user_input"] = ""

if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

st.text_input(
    "Ask your question",
    key="user_input",
    placeholder="e.g. What courses are offered at Federal University Lokoja?",
    label_visibility="collapsed",
    on_change=submit_question
)

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------
st.markdown(
    """
    <div class="footer">
        FUL Chatbot for Enquiry and Information &nbsp;•&nbsp;
        Federal University Lokoja &nbsp;•&nbsp;
        Offline Knowledge Based Assistant
    </div>
    """,
    unsafe_allow_html=True
)
