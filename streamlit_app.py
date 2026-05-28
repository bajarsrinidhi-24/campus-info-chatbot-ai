import streamlit as st
import re

# Page config
st.set_page_config(
    page_title="CampusBot - GNITS Assistant",
    page_icon="🎓",
    layout="wide"
)

# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# College Data
COLLEGE_INFO = {
    "admissions": "📝 ADMISSIONS\n\nUG: TG-EAPCET exam required. Eligibility: 10+2 with Physics, Chemistry, Mathematics\nPG: Based on GATE score or TS-PGECET\nContact: 040-29565856",
    "fees": "💰 FEE STRUCTURE\n\nB.Tech: ₹1,62,000 per year + JNTUH fees\nM.Tech: ₹1,12,000 per year\nNRI Category: USD 5,000 + JNTUH fees",
    "placements": "🏆 PLACEMENTS\n\nHighest Package: 50 LPA (Microsoft)\nTop Recruiters: Microsoft, ServiceNow (42.6 LPA), Deloitte, Snowflake, PwC",
    "facilities": "📚 FACILITIES\n\nLibrary: 8 AM to 8 PM (Mon-Sat)\nHostel: Girls hostel with 24/7 security\nSports: Indoor games, volleyball, basketball\nCanteen: Available",
    "clubs": "🎉 CLUBS & EVENTS\n\nCoding Club, Robotics Club, Entrepreneurship Cell\nCultural Committee, Technical Club (ACM)\nIEEE ICoECIT-2026 (March 2026)\nSplash 2026 (October 2026)",
    "contacts": "📞 CONTACTS\n\nPrincipal: 040-29565850\nAdmissions: 040-29565856\nPlacements: 040-29565860\nLibrary: 040-29565870"
}

def get_response(question):
    q = question.lower().strip()
    
    # Greetings
    if re.search(r'^(hi|hello|hey|namaste|good morning|good afternoon|good evening)', q):
        return "Hello! 👋 Welcome to CampusBot! How can I help you with GNITS today?"
    
    # Fee related
    if re.search(r'(fee|fees|cost|price|tuition)', q):
        return COLLEGE_INFO["fees"]
    
    # Admission related
    if re.search(r'(admission|apply|eligibility|how to get|join|counseling)', q):
        return COLLEGE_INFO["admissions"]
    
    # Placement related
    if re.search(r'(placement|package|recruiter|company|job|salary|lpa|hiring|offer)', q):
        return COLLEGE_INFO["placements"]
    
    # Facility related
    if re.search(r'(library|hostel|canteen|sports|lab|facility|gym|playground)', q):
        return COLLEGE_INFO["facilities"]
    
    # Club/Event related
    if re.search(r'(club|event|fest|hackathon|splash|competition|cultural|technical)', q):
        return COLLEGE_INFO["clubs"]
    
    # Contact related
    if re.search(r'(contact|phone|number|email|call|reach|mobile)', q):
        return COLLEGE_INFO["contacts"]
    
    # About college
    if re.search(r'(about|what is|tell me about|information|overview)', q):
        return "🏫 ABOUT GNITS\n\nG. Narayanamma Institute of Technology and Sciences (GNITS) is a prestigious women's engineering college in Hyderabad, established in 1997.\n\nAccreditations: NBA, NAAC 'A' Grade\nCourses: B.Tech (CSE, IT, ECE, EEE, Data Science, AI & ML), M.Tech\n\n📍 Location: Hyderabad, Telangana"
    
    # Thank you
    if re.search(r'(thank|thanks|great|awesome|helpful)', q):
        return "You're welcome! 😊 Glad I could help! Is there anything else you'd like to know about GNITS?"
    
    # Default
    return "I'm here to help! 😊\n\nYou can ask me about:\n• 📝 Admissions & Eligibility\n• 💰 Fee Structure\n• 🏆 Placements & Packages\n• 📚 Facilities (Library, Hostel, Sports)\n• 🎉 Clubs & Events\n• 📞 Contact Numbers\n\nWhat would you like to know?"

# Custom CSS - Clean and professional
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #e94560 0%, #533483 100%);
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
        margin-top: 10px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #e94560 0%, #533483 100%);
        color: white;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(233,69,96,0.4);
    }
    .user-message {
        background: linear-gradient(135deg, #e94560 0%, #533483 100%);
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
    st.markdown("### 🤖 About CampusBot")
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
    
    st.markdown("---")
    st.markdown("### 📌 Quick Info")
    st.markdown("""
    - 🏫 **GNITS Hyderabad**
    - 🎓 **Est:** 1997
    - 👩‍🎓 **Women's College**
    - ⭐ **NAAC 'A' Grade**
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

# Display chat history
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

# Chat input
question = st.text_input("", placeholder="Type your message here...", key="input", label_visibility="collapsed")

if question:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": question})
    
    # Get bot response
    response = get_response(question)
    
    # Add bot message
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun to update display
    st.rerun()

# Welcome message
if not st.session_state.messages:
    st.info("👋 **Hello!** I'm CampusBot. Ask me about admissions, fees, placements, or just say hi! 😊")
