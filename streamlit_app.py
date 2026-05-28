import streamlit as st
import random
import re

# Page config
st.set_page_config(
    page_title="CampusBot - GNITS Assistant",
    page_icon="🎓",
    layout="wide"
)

# Initialize session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'messages' not in st.session_state:
    st.session_state.messages = []

# College Data
COLLEGE_DATA = {
    "admissions": {
        "ug": "UG Admissions: TG-EAPCET exam required. Eligibility: 10+2 with Physics, Chemistry, Mathematics. Contact: 040-29565856",
        "pg": "PG Admissions: Based on GATE score or TS-PGECET. Contact: 040-29565856"
    },
    "fees": {
        "btech": "B.Tech Fee: ₹1,62,000 per year + JNTUH fees",
        "mtech": "M.Tech Fee: ₹1,12,000 per year",
        "nri": "NRI Category: USD 5,000 + JNTUH fees per year"
    },
    "placements": {
        "highest": "Highest Package: 50 LPA (Microsoft)",
        "companies": "Top Recruiters: Microsoft (50 LPA), ServiceNow (42.6 LPA), Deloitte, Snowflake, PwC"
    },
    "facilities": {
        "library": "Library: 8 AM to 8 PM (Monday-Saturday)",
        "hostel": "Hostel: Girls hostel with 24/7 security",
        "sports": "Sports: Indoor badminton, table tennis, volleyball, basketball",
        "canteen": "Canteen: Vegetarian and non-vegetarian options"
    },
    "clubs": {
        "coding": "Coding Club: CodeChef, LeetCode competitions",
        "robotics": "Robotics Club",
        "edc": "Entrepreneurship Development Cell (EDC)",
        "cultural": "Cultural Committee: Splash annual fest",
        "technical": "Technical Club: GNITS ACM Student Chapter"
    },
    "contacts": {
        "principal": "Principal Office: 040-29565850",
        "admissions": "Admissions: 040-29565856",
        "placements": "Training & Placement Cell: 040-29565860",
        "library": "Library: 040-29565870"
    },
    "events": {
        "ieee": "IEEE ICoECIT-2026 (AI & Quantum Computing) - March 2026",
        "splash": "Splash 2026 (Annual Cultural Fest) - October 2026",
        "hackathon": "Hackathon - February 2026",
        "alumni": "Alumni Meet (TU TURNO-26) - December 2026"
    }
}

def get_response(user_input):
    text = user_input.lower().strip()
    
    # Greetings
    if re.search(r'\b(hi|hello|hey|greetings|sup|namaste)\b', text):
        greetings = [
            "Hello! 👋 How can I help you with GNITS today?",
            "Hey there! 😊 What would you like to know about GNITS?",
            "Hi! 🎓 I'm CampusBot. Ask me anything about GNITS!",
            "Namaste! 🙏 How can I assist you with college information?"
        ]
        return random.choice(greetings)
    
    # How are you
    elif re.search(r'how are you', text):
        responses = [
            "I'm doing great, thanks for asking! 😊 Ready to help you with GNITS queries!",
            "I'm fantastic! 🎉 How can I assist you today?",
            "All good here! 👍 What can I tell you about GNITS?"
        ]
        return random.choice(responses)
    
    # Thanks
    elif re.search(r'thank|thanks|appreciate', text):
        responses = [
            "You're very welcome! 😊 Anything else I can help with?",
            "My pleasure! 🎓 Feel free to ask more questions!",
            "Glad to help! 👍 Is there anything else you'd like to know?"
        ]
        return random.choice(responses)
    
    # Bye
    elif re.search(r'(bye|goodbye|see you|cya)', text):
        return "Goodbye! 👋 Have a great day! Visit again if you have more questions about GNITS! 🎓"
    
    # Fee structure
    elif re.search(r'(fee|fees|cost|price|tuition)', text):
        return f"💰 **Fee Structure:**\n\n{COLLEGE_DATA['fees']['btech']}\n{COLLEGE_DATA['fees']['mtech']}\n\n{COLLEGE_DATA['fees']['nri']}"
    
    # Admissions
    elif re.search(r'(admission|apply|eligibility|how to get|qualify|counseling)', text):
        return f"📝 **Admissions:**\n\n{COLLEGE_DATA['admissions']['ug']}\n\n{COLLEGE_DATA['admissions']['pg']}"
    
    # Placements
    elif re.search(r'(placement|package|recruiter|company|job|salary|lpa|hiring)', text):
        return f"🏆 **Placements:**\n\n{COLLEGE_DATA['placements']['highest']}\n\n{COLLEGE_DATA['placements']['companies']}"
    
    # Facilities
    elif re.search(r'(library|hostel|canteen|sports|facility|lab|gym)', text):
        return f"📚 **Facilities:**\n\n{COLLEGE_DATA['facilities']['library']}\n\n{COLLEGE_DATA['facilities']['hostel']}\n\n{COLLEGE_DATA['facilities']['sports']}\n\n{COLLEGE_DATA['facilities']['canteen']}"
    
    # Clubs
    elif re.search(r'(club|clubs|committee|activity|technical|cultural)', text):
        return f"🎉 **Clubs & Committees:**\n\n{COLLEGE_DATA['clubs']['coding']}\n{COLLEGE_DATA['clubs']['robotics']}\n{COLLEGE_DATA['clubs']['edc']}\n{COLLEGE_DATA['clubs']['cultural']}\n{COLLEGE_DATA['clubs']['technical']}"
    
    # Events
    elif re.search(r'(event|fest|hackathon|splash|workshop|seminar)', text):
        return f"🎪 **Upcoming Events:**\n\n{COLLEGE_DATA['events']['ieee']}\n{COLLEGE_DATA['events']['splash']}\n{COLLEGE_DATA['events']['hackathon']}\n{COLLEGE_DATA['events']['alumni']}"
    
    # Contacts
    elif re.search(r'(contact|phone|number|email|call|reach)', text):
        return f"📞 **Important Contacts:**\n\n{COLLEGE_DATA['contacts']['admissions']}\n{COLLEGE_DATA['contacts']['principal']}\n{COLLEGE_DATA['contacts']['placements']}\n{COLLEGE_DATA['contacts']['library']}"
    
    # About college
    elif re.search(r'(about|what is|tell me about college|information)', text):
        return "🏫 **About GNITS:**\n\nG. Narayanamma Institute of Technology and Sciences (GNITS) is a prestigious women's engineering college in Hyderabad, established in 1997.\n\n**Accreditations:** NBA, NAAC 'A' Grade\n**Courses:** B.Tech (CSE, IT, ECE, EEE, Data Science, AI & ML), M.Tech\n\n📍 Location: Hyderabad, Telangana"
    
    # Default response
    else:
        return "I'm here to help! 😊\n\nYou can ask me about:\n• 📝 **Admissions** - How to apply, eligibility\n• 💰 **Fees** - B.Tech, M.Tech fee structure\n• 🏆 **Placements** - Packages, recruiters\n• 📚 **Facilities** - Library, Hostel, Sports\n• 🎉 **Clubs & Events** - Activities, fests\n• 📞 **Contacts** - Phone numbers\n\nWhat would you like to know?"

# Custom CSS - Clean, no blue gradient
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    .main-header {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #e84545 0%, #903749 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .main-header h1 {
        font-size: 2.5rem;
        color: white;
        margin: 0;
    }
    .main-header p {
        color: rgba(255,255,255,0.9);
        margin: 10px 0 0 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #e84545 0%, #903749 100%);
        color: white;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(233,69,69,0.4);
    }
    .user-message {
        background: linear-gradient(135deg, #e84545 0%, #903749 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 20px;
        margin: 10px 0;
        border-radius: 20px 20px 5px 20px;
        max-width: 70%;
        float: right;
        clear: both;
    }
    .bot-message {
        background: rgba(255,255,255,0.1);
        color: white;
        padding: 12px 18px;
        border-radius: 20px;
        margin: 10px 0;
        border-radius: 20px 20px 20px 5px;
        max-width: 70%;
        float: left;
        clear: both;
        backdrop-filter: blur(10px);
    }
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.1);
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 25px;
        padding: 12px 20px;
    }
    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.6);
    }
    .sidebar .sidebar-content {
        background: rgba(0,0,0,0.2);
    }
    .info-box {
        background: rgba(255,255,255,0.05);
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎓 CampusBot</h1>
    <p>Your friendly AI assistant for GNITS college</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎨 Theme")
    theme_toggle = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    if theme_toggle != st.session_state.dark_mode:
        st.session_state.dark_mode = theme_toggle
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🤖 About Me")
    st.markdown("""
    Hey there! 👋 I'm CampusBot.
    
    I can help you with:
    - 📝 **Admissions**
    - 💰 **Fees**  
    - 🏆 **Placements**
    - 📚 **Facilities**
    - 🎉 **Clubs & Events**
    - 📞 **Contacts**
    """)
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Quick questions
st.markdown("### 💡 Quick Questions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💰 Fee Structure", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "What is the fee structure?"})
        st.rerun()
with col2:
    if st.button("📝 Admissions", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "How to get admission?"})
        st.rerun()
with col3:
    if st.button("🏆 Placements", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Tell me about placements"})
        st.rerun()
with col4:
    if st.button("📞 Contacts", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Give me contact numbers"})
        st.rerun()

st.markdown("---")

# Chat display
st.markdown("### 💬 Chat with CampusBot")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end;">
            <div class="user-message">
                <strong>You</strong><br>{msg["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start;">
            <div class="bot-message">
                <strong>🎓 CampusBot</strong><br>{msg["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Input
question = st.text_input("", placeholder="Type your message here...", key="input", label_visibility="collapsed")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    response = get_response(question)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Welcome message
if not st.session_state.messages:
    st.info("👋 **Hello!** I'm CampusBot. Ask me about admissions, fees, placements, or just say hi! 😊")
