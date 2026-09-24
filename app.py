import streamlit as st
import random
import html
import re
import difflib

# ---------------------------------------------------------------------------
# All chatbot data lives right here now — no external dataset.json needed.
# To add/change a question or answer, edit the INTENTS_DATA list below.
# ---------------------------------------------------------------------------
INTENTS_DATA = {
    "intents": [
        {
            "tag": "greeting",
            "patterns": [
                "Hi", "How are you?", "Is anyone there?", "Hello", "Good day",
                "What's up", "how are ya", "heyy", "whatsup", "??? ??? ??"
            ],
            "responses": [
                "Hello!", "Good to see you again!", "Hi there, how can I help?"
            ]
        },
        {
            "tag": "goodbye",
            "patterns": [
                "cya", "see you", "bye bye", "See you later", "Goodbye",
                "I am Leaving", "Bye", "Have a Good day", "talk to you later",
                "ttyl", "i got to go", "gtg"
            ],
            "responses": [
                "Sad to see you go :(", "Talk to you later", "Goodbye!", "Come back soon"
            ]
        },
        {
            "tag": "creator",
            "patterns": [
                "what is the name of your developers", "what is the name of your creators",
                "what is the name of the developers", "what is the name of the creators",
                "who created you", "your developers", "your creators",
                "who are your developers", "developers", "you are made by",
                "you are made by whom", "who create you", "creators",
                "who made you", "who designed you"
            ],
            "responses": [
                "Abdulhamid Omeiza Idris, A Computer Science Student of Federal University Lokoja"
            ]
        },
        {
            "tag": "name",
            "patterns": [
                "name", "your name", "do you have a name", "what are you called",
                "what is your name", "what should I call you", "whats your name?",
                "what are you", "who are you", "who is this",
                "what am i chatting to", "who am i taking to"
            ],
            "responses": [
                "You can call me University Guide.", "I am a Chatbot.", "I am your A.I helper"
            ]
        },
        {
            "tag": "hours",
            "patterns": [
                "timing of university", "what is university timing", "working days",
                "when are you guys open", "what are your hours", "hours of operation",
                "when is the university open", "university timing",
                "what about university timing", "is university open on saturday",
                "tell something about university timing", "what is the university  hours",
                "when should i come to university", "when should i attend university",
                "what is my university time", "timing university"
            ],
            "responses": [
                "The University is open 8am-5pm Monday-Saturday!"
            ]
        },
        {
            "tag": "number",
            "patterns": [
                "more info", "contact info", "how to contact university",
                "university telephone number", "university number",
                "What is your contact no", "university number?", "how to call you",
                "university phone no?", "how can i contact you",
                "Can i get your phone number", "how can i call you",
                "phone number", "phone no", "call"
            ],
            "responses": [
                "You can contact the university via call or whatsapp at: +2349012345678"
            ]
        },
        {
            "tag": "course",
            "patterns": [
                "list of courses", "list of courses offered", "list of courses offered in",
                "what are the courses offered in your college?", "courses?",
                "courses offered", "courses offered in (Federal University Lokoja)",
                "courses you offer", "branches?", "courses available at UNI?",
                "branches available at your university?", "what are the courses in UNI?",
                "what are branches in UNI?", "what are courses in UNI?",
                "branches available in UNI?", "can you tell me the courses available in UNI?",
                "can you tell me the branches available in UNI?", "computer engineering?",
                "computer", "Computer engineering?", "it", "IT",
                "Information Technology", "AI/Ml", "Mechanical engineering",
                "Chemical engineering", "Civil engineering"
            ],
            "responses": [
                "Our university offers Information Technology, computer Engineering, Mechanical engineering,Chemical engineering, Civil engineering and extc Engineering and many more. for more information Visit www.fulokoja.edu.ng"
            ]
        },
        {
            "tag": "fees",
            "patterns": [
                "information about fee", "information on fee", "tell me the fee",
                "university fee", "fee per semester", "what is the fee of each semester",
                "what is the fees of each year", "what is fee", "what is the fees",
                "how much is the fees", "fees for first year", "fees", "about the fees",
                "tell me something about the fees", "What is the fees of hostel",
                "hostel fees", "fees for AC room", "fees for non-AC room",
                "fees for Ac room for girls", "fees for non-Ac room for girls",
                "fees for Ac room for boys", "fees for non-Ac room for boys"
            ],
            "responses": [
                "For Fee detail visit www.fulokoja.edu.ng"
            ]
        },
        {
            "tag": "location",
            "patterns": [
                "where is the university located", "university is located at",
                "where is university", "where is university located",
                "address of university", "how to reach university",
                "university location", "university address", "wheres the university",
                "how can I reach university", "whats is the university address",
                "what is the address of university", "address", "location"
            ],
            "responses": [
                "P.M.B 1154, Main Campus, Felele (Permanent Site) Lokoja-Okene expressway, Felele, Lokoja, Kogi State, Nigeria"
            ]
        },
        {
            "tag": "hostel",
            "patterns": [
                "hostel facility", "hostel servive", "hostel location", "hostel address",
                "hostel facilities", "hostel fees", "Does university provide hostel",
                "Is there any hostel", "Where is hostel", "do you have hostel",
                "do you guys have hostel", "hostel", "hostel capacity",
                "what is the hostel fee", "how to get in hostel",
                "what is the hostel address", "how far is hostel from university",
                "hostel university distance", "where is the hostel",
                "how big is the hostel", "distance between university and hostel",
                "distance between hostel and university"
            ],
            "responses": [
                "For hostel detail visit federal University Lokoja Admission office OR www.fulokoja.edu.ng"
            ]
        },
        {
            "tag": "event",
            "patterns": [
                "events organised", "list of events", "list of events organised in university",
                "list of events conducted in university", "What events are conducted in university",
                "Are there any event held at university", "Events?", "functions",
                "what are the events", "tell me about events", "what about events"
            ],
            "responses": [
                "For event detail visit www.fulokoja.edu.ng"
            ]
        },
        {
            "tag": "document",
            "patterns": [
                "document to bring", "documents needed for admision",
                "documents needed at the time of admission", "documents needed during admission",
                "documents required for admision", "documents required at the time of admission",
                "documents required during admission", "What document are required for admission",
                "Which document to bring for admission", "documents",
                "what documents do i need", "what documents do I need for admission",
                "documents needed"
            ],
            "responses": [
                "To know more about document required visit www.fulokoja.edu.ng"
            ]
        },
        {
            "tag": "floors",
            "patterns": [
                "size of campus", "building size", "How many floors does college have",
                "floors in university", "how tall is UNI's College of Engineering college building",
                "floors"
            ],
            "responses": [
                "The University has many notable buildings"
            ]
        },
        {
            "tag": "syllabus",
            "patterns": [
                "Syllabus for IT", "what is the Information Technology syllabus",
                "syllabus", "timetable", "what is IT syllabus", "What is next lecture"
            ],
            "responses": [
                "Timetable provide direct to the students OR To know about syllabus visit your department"
            ]
        },
        {
            "tag": "library",
            "patterns": [
                "is there any library", "library facility", "library facilities",
                "do you have library", "does the university have library facility",
                "university library", "where can i get books", "book facility",
                "Where is library", "Library", "Library information",
                "Library books information", "Tell me about library", "how many libraries"
            ],
            "responses": [
                "There is one huge and spacious library located beside the ICT centre. Timings are 8am to 4pm"
            ]
        },
        {
            "tag": "infrastructure",
            "patterns": [
                "how is university infrastructure", "infrastructure", "university infrastructure"
            ],
            "responses": [
                "Our University has Excellent Infrastructure. Campus is clean. Good IT Labs With Good Speed of Internet connection"
            ]
        },
        {
            "tag": "canteen",
            "patterns": [
                "food facilities", "canteen facilities", "canteen facility",
                "is there any canteen", "Is there a cafetaria in university",
                "Does university have canteen", "Where is canteen", "where is cafetaria",
                "canteen", "Food", "Cafetaria"
            ],
            "responses": [
                "Our university has canteen with variety of food available"
            ]
        },
        {
            "tag": "menu",
            "patterns": [
                "food menu", "food in canteen", "Whats there on menu",
                "what is available in university canteen",
                "what foods can we get in university canteen", "food variety",
                "What is there to eat?"
            ],
            "responses": [
                "we serve different type of Rice, Swallows and Soups, Snacks, Drinks, and many more on menu"
            ]
        },
        {
            "tag": "placement",
            "patterns": [
                "What is college placement", "Which companies visit in college",
                "What is average package", "companies visit", "package",
                "About placement", "placement", "recruitment", "companies"
            ],
            "responses": [
                "To know about placement visit www.fulokoja.edu.ng"
            ]
        },
        {
            "tag": "HOD",
            "patterns": [
                "Who is HOD", "Where is HOD", "it hod", "name of it hod"
            ],
            "responses": [
                "All departments have their hods, to find specific HODs please visit the department"
            ]
        },
        {
            "tag": "computerhod",
            "patterns": [
                "Who is computer HOD", "Where is computer HOD", "computer hod",
                "name of computer hod"
            ],
            "responses": [
                "All departments have their hods, to find specific HODs please visit the department"
            ]
        },
        {
            "tag": "extchod",
            "patterns": [
                "Who is extc HOD", "Where is  extc HOD", "extc hod", "name of extc hod"
            ],
            "responses": [
                "All departments have their hods, to find specific HODs please visit the department"
            ]
        },
        {
            "tag": "VC",
            "patterns": [
                "what is the name of VC", "whatv is the Vice Chancellor name", "VC name",
                "Who is University VC", "Where is VC's office", "VC", "Vice Chancellor",
                "name of VC", "who is the vc", "who is the vc of federal university lokoja"
            ],
            "responses": [
                "Prof. Gbenga Ibileye is University Vice Chancellor and if you need any help then call your department hod first. That is more appropriate"
            ]
        },
        {
            "tag": "sem",
            "patterns": [
                "exam dates", "exam schedule", "When is semester exam",
                "Semester exam timetable", "sem", "semester", "exam", "when is exam",
                "exam timetable", "when is semester"
            ],
            "responses": [
                "To know more about the academic calender plese visit www.fulokoja.edu.ng"
            ]
        },
        {
            "tag": "admission",
            "patterns": [
                "what is the process of admission", "what is the admission process",
                "How to take admission in your university", "What is the process for admission",
                "admission", "admission process"
            ],
            "responses": [
                "Application can also be submitted online through the Unversity's  website at www.fulokoja.edu.ng"
            ]
        },
        {
            "tag": "scholarship",
            "patterns": [
                "scholarship", "Is scholarship available", "scholarship engineering",
                "scholarship it", "scholarship ce", "scholarship mechanical",
                "scholarship civil", "scholarship chemical", "scholarship for AI/ML",
                "available scholarships", "scholarship for computer engineering",
                "scholarship for IT engineering", "scholarship for mechanical engineering",
                "scholarship for civil engineering", "scholarship for chemical engineering",
                "list of scholarship", "comps scholarship", "IT scholarship",
                "mechanical scholarship", "civil scholarship", "chemical scholarship",
                "automobile scholarship", "first year scholarship", "second year scholarship",
                "third year scholarship", "fourth year scholarship"
            ],
            "responses": [
                "Many government scholarships are supported by our university. For details and updates visit www.fulokoja.edu.ng"
            ]
        },
        {
            "tag": "facilities",
            "patterns": [
                "What facilities University provide", "University facility",
                "What are the university facilities", "facilities", "facilities provided"
            ],
            "responses": [
                "Our university's provides fully AC Lab with internet connection, smart classroom, Auditorium, library, canteen"
            ]
        },
        {
            "tag": "college intake",
            "patterns": [
                "max number of students", "number of seats per class",
                "number of seats in each class", "maximum number of seats",
                "maximum students intake", "What is university intake",
                "how many stundent are taken in each department", "seat allotment", "seats"
            ],
            "responses": [
                "Seat allocation differs for different department."
            ]
        },
        {
            "tag": "uniform",
            "patterns": [
                "university dress code", "university dresscode", "what is the uniform",
                "can we wear casuals", "Does university have an uniform",
                "Is there any uniform", "uniform", "what about uniform",
                "do we have to wear uniform"
            ],
            "responses": [
                "some department has dress code but a few"
            ]
        },
        {
            "tag": "committee",
            "patterns": [
                "what are the different committe in university",
                "different committee in university", "Are there any committee in university",
                "Give me committee details", "committee", "how many committee are there in college"
            ],
            "responses": [
                "For the various committe in university contact this number: +2349065558888"
            ]
        },
        {
            "tag": "random",
            "patterns": [
                "I love you", "Will you marry me", "Do you love me"
            ],
            "responses": [
                "I am not program for this, please ask appropriate query"
            ]
        },
        {
            "tag": "swear",
            "patterns": [
                "fuck", "bitch", "shut up", "hell", "stupid", "idiot", "dumb ass",
                "asshole", "fucker"
            ],
            "responses": [
                "please use appropriate language", "Maintaining decency would be appreciated"
            ]
        },
        {
            "tag": "vacation",
            "patterns": [
                "holidays", "when will semester starts", "when will semester end",
                "when is the holidays", "list of holidays", "Holiday in these year",
                "holiday list", "about vacations", "about holidays", "When is vacation",
                "When is holidays", "how long will be the vacation"
            ],
            "responses": [
                "Academic calender is given to you by your class-soordinators after you join your respective classes"
            ]
        },
        {
            "tag": "sports",
            "patterns": [
                "sports and games", "give sports details", "sports infrastructure",
                "sports facilities", "information about sports", "Sports activities",
                "please provide sports and games information"
            ],
            "responses": [
                "Our university encourages all-round development of students and hence provides sports facilities in the campus"
            ]
        },
        {
            "tag": "salutaion",
            "patterns": [
                "okk", "okie", "nice work", "well done", "good job", "thanks for the help",
                "Thank You", "its ok", "Thanks", "Good work", "k", "ok", "okay"
            ],
            "responses": [
                "I am glad I helped you", "welcome, anything else i can assist you with?"
            ]
        },
        {
            "tag": "task",
            "patterns": [
                "what can you do", "what are the thing you can do", "things you can do",
                "what can u do for me", "how u can help me", "why i should use you"
            ],
            "responses": [
                "I can answer to low-intermediate questions regarding Federal University Lokoja",
                "You can ask me questions regarding the University, and i will try to answer them or direct you"
            ]
        },
        {
            "tag": "ragging",
            "patterns": [
                "ragging", "is ragging practice active in college",
                "does college have any antiragging facility", "is there any ragging cases",
                "is ragging done here", "ragging against", "antiragging facility",
                "ragging juniors", "ragging history", "ragging incidents"
            ],
            "responses": [
                "We are Proud to tell you that our college provides ragging free environment, and we have strict rules against ragging"
            ]
        },
        {
            "tag": "hod",
            "patterns": [
                "hod", "hod name", "who is the hod"
            ],
            "responses": [
                "HODs differ for each branch, please be more specific like: (HOD it)"
            ]
        }
    ]
}

# Build lookups from the embedded data
tag_to_responses = {
    intent["tag"]: intent["responses"] for intent in INTENTS_DATA["intents"]
}

pattern_lookup = []  # list of (pattern_lower, tag)
for intent in INTENTS_DATA["intents"]:
    for pattern in intent["patterns"]:
        pattern_lookup.append((pattern.lower().strip(), intent["tag"]))

all_patterns = [p for p, _ in pattern_lookup]


# Preprocess function
def preprocess_text(text):
    return text.lower().strip()


def match_tag(processed_input, cutoff=0.7):
    """
    Resolve the user's message to a tag using only INTENTS_DATA:
    1. exact match against a known pattern
    2. whole-word / whole-phrase match (uses word boundaries so short
       patterns like "it" or "vc" don't false-match inside longer
       words like "university"); when multiple patterns match, the
       longest (most specific) one wins
    3. fuzzy match (handles typos / near-identical phrasing)
    Returns a tag, or None if nothing reasonable is found.
    """
    # 1) Exact match
    for pattern, tag in pattern_lookup:
        if processed_input == pattern:
            return tag

    # 2) Whole-word/phrase containment, longest pattern wins
    best_tag, best_len = None, 0
    for pattern, tag in pattern_lookup:
        if len(pattern.split()) <= 4:
            if re.search(r'\b' + re.escape(pattern) + r'\b', processed_input):
                if len(pattern) > best_len:
                    best_len = len(pattern)
                    best_tag = tag
    if best_tag:
        return best_tag

    # 3) Fuzzy match against the full pattern list
    close = difflib.get_close_matches(processed_input, all_patterns, n=1, cutoff=cutoff)
    if close:
        matched_pattern = close[0]
        for pattern, tag in pattern_lookup:
            if pattern == matched_pattern:
                return tag

    return None


# Chatbot response function — answers come only from INTENTS_DATA
def get_response(user_input):
    processed_input = preprocess_text(user_input)
    tag = match_tag(processed_input)

    responses = tag_to_responses.get(tag)
    if responses:
        return random.choice(responses)

    return "I'm sorry, I don't understand that. Please try asking your question differently."


# Streamlit page configuration
st.set_page_config(
    page_title="University Information Chatbot",
    page_icon="🎓",
    layout="centered"
)


# Custom styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f4f8fc;
    }

    .main-title {
        background-color: #0B3D91;
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 10px;
    }

    .main-title h1 {
        color: white;
        margin: 0;
    }

    .subtitle {
        color: #333333;
        text-align: center;
        margin-bottom: 25px;
    }

    .chat-container {
        overflow: hidden;
        margin-bottom: 12px;
        width: 100%;
    }

    .chat-bubble-user {
        background-color: #D9EAF7;
        color: #000000;
        padding: 12px 16px;
        border-radius: 15px;
        margin: 8px 0;
        text-align: right;
        max-width: 75%;
        float: right;
        clear: both;
    }

    .chat-bubble-bot {
        background-color: #FFFFFF;
        color: #000000;
        padding: 12px 16px;
        border-radius: 15px;
        margin: 8px 0;
        text-align: left;
        max-width: 75%;
        float: left;
        clear: both;
        border: 1px solid #D9E2EC;
    }

    .footer {
        text-align: center;
        color: #666666;
        font-size: 13px;
        margin-top: 30px;
        padding-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Application heading
st.markdown(
    """
    <div class="main-title">
        <h1>🎓 University Information Chatbot</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Ask questions about university information, admission, courses,
        registration, academic calendar and other student services.
    </div>
    """,
    unsafe_allow_html=True
)


# Keep chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "pending_input" not in st.session_state:
    st.session_state["pending_input"] = ""


# Quick-reply suggestions
suggested_questions = [
    "What is the admission process?",
    "Tell me the fees",
    "Do you have hostel?",
    "List of courses offered",
    "Where is the university located?",
    "Who is the VC?",
]

st.markdown("**Quick questions:**")
cols = st.columns(3)
for i, question in enumerate(suggested_questions):
    if cols[i % 3].button(question, use_container_width=True):
        st.session_state["pending_input"] = question


# User input
user_input = st.text_input(
    "Ask your question:",
    value=st.session_state["pending_input"],
    placeholder="Type your university related question here..."
)

# Clear the pending input now that it has been shown once
st.session_state["pending_input"] = ""


# Process user input
if user_input.strip():
    response = get_response(user_input)

    st.session_state["messages"].append(("user", user_input))
    st.session_state["messages"].append(("bot", response))


# Display chat history
for sender, msg in st.session_state["messages"]:
    safe_msg = html.escape(str(msg))

    if sender == "user":
        st.markdown(
            f"""
            <div class="chat-container">
                <div class="chat-bubble-user">
                    {safe_msg}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="chat-container">
                <div class="chat-bubble-bot">
                    🤖 {safe_msg}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# Footer
st.markdown(
    """
    <div class="footer">
        University Information Chatbot | Faculty of Computing
    </div>
    """,
    unsafe_allow_html=True
)