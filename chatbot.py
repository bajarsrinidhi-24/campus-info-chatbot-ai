import streamlit as st
import re
import random
from datetime import datetime

st.set_page_config(page_title="GNITS Campus Assistant", page_icon="🎓", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main-header {
        text-align: center;
        padding: 2rem;
        background: rgba(255,255,255,0.95);
        border-radius: 20px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        font-size: 2rem;
        color: #667eea;
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 20px;
        margin: 10px 0;
        max-width: 75%;
        float: right;
        clear: both;
    }
    .bot-message {
        background: white;
        color: #2c3e50;
        padding: 12px 18px;
        border-radius: 20px;
        margin: 10px 0;
        max-width: 75%;
        float: left;
        clear: both;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        border: none;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎓 GNITS Campus Assistant</h1>
    <p>Ask me anything about GNITS - admissions, placements, fees, facilities, clubs, and more!</p>
</div>
""", unsafe_allow_html=True)

# College Information Database
COLLEGE_DATA = """
G. Narayanamma Institute of Technology and Sciences (GNITS), Hyderabad

📝 ADMISSIONS:
- UG: TG-EAPCET exam required. Eligibility: 10+2 with Physics, Chemistry, Mathematics
- PG: Based on GATE score or TS-PGECET
- Contact Admissions: 040-29565856

💰 FEE STRUCTURE:
- B.Tech: ₹1,62,000 per year + JNTUH fees
- M.Tech: ₹1,12,000 per year
- NRI Category: USD 5,000 + JNTUH fees per year

🏆 PLACEMENTS:
- Highest Package: 50 LPA (Microsoft)
- Second Highest: 42.6 LPA (ServiceNow)
- Top Recruiters: Microsoft, ServiceNow, Deloitte, Snowflake, PwC

📚 FACILITIES:
- Library: 8 AM to 8 PM (Monday-Saturday)
- Hostel: Girls hostel with 24/7 security
- Sports: Indoor badminton, table tennis, volleyball, basketball
- Canteen: Vegetarian and non-vegetarian options

🎉 CLUBS & EVENTS:
- Coding Club (CodeChef, LeetCode competitions)
- Robotics Club
- Entrepreneurship Development Cell (EDC)
- Cultural Committee (Splash annual fest)
- Technical Club (GNITS ACM Student Chapter)
- IEEE ICoECIT-2026 (AI & Quantum Computing) - March 2026
- Hackathon - February 2026
- Alumni Meet (TU TURNO-26) - December 2026

📞 IMPORTANT CONTACTS:
- Principal Office: 040-29565850
- Admissions: 040-29565856
- Training & Placement Cell: 040-29565860
- Library: 040-29565870

🏫 ABOUT:
- Established: 1997
- Type: Women's Engineering College
- Location: Hyderabad, Telangana
- Accreditation: NBA, NAAC 'A' Grade
- Courses: B.Tech (CSE, IT, ECE, EEE, Data Science, AI & ML), M.Tech
"""

def get_response(question):
    q = question.lower().strip()
    
    # Greetings
    if re.search(r'^(hi|hello|hey|namaste|good morning|good afternoon)', q):
        return "Hello! 👋 Welcome to GNITS Campus Assistant! How can I help you today? 😊"
    
    # Fee related
    if re.search(r'(fee|fees|cost|price|tuition)', q):
        return COLLEGE_DATA.split("💰 FEE STRUCTURE:")[1].split("🏆 PLACEMENTS:")[0]
    
    # Admission related
    if re.search(r'(admission|apply|eligibility|how to get|join|counseling)', q):
        return COLLEGE_DATA.split("📝 ADMISSIONS:")[1].split("💰 FEE STRUCTURE:")[0]
    
    # Placement related
    if re.search(r'(placement|package|recruiter|company|job|salary|lpa|hiring|offer)', q):
        return COLLEGE_DATA.split("🏆 PLACEMENTS:")[1].split("📚 FACILITIES:")[0]
    
    # Facility related
    if re.search(r'(library|hostel|canteen|sports|lab|facility|gym|playground)', q):
        return COLLEGE_DATA.split("📚 FACILITIES:")[1].split("🎉 CLUBS & EVENTS:")[0]
    
    # Club/Event related
    if re.search(r'(club|event|fest|hackathon|splash|competition|cultural|technical)', q):
        return COLLEGE_DATA.split("🎉 CLUBS & EVENTS:")[1].split("📞 IMPORTANT CONTACTS:")[0]
    
    # Contact related
    if re.search(r'(contact|phone|number|email|call|reach|mobile)', q):
        return COLLEGE_DATA.split("📞 IMPORTANT CONTACTS:")[1].split("🏫 ABOUT:")[0]
    
    # About college
    if re.search(r'(about|what is|tell me about|information|overview)', q):
        return COLLEGE_DATA.split("🏫 ABOUT:")[1]
    
    # Thank you
    if re.search(r'(thank|thanks|great|awesome|helpful)', q):
        return "You're welcome! 😊 Glad I could help! Is there anything else you'd like to know about GNITS?"
    
    # Default
    return """😊 **I'm here to help!**

You can ask me about:
• 📝 Admissions & Eligibility
• 💰 Fee Structure
• 🏆 Placements & Packages
• 📚 Facilities (Library, Hostel, Sports)
• 🎉 Clubs & Events
• 📞 Contact Numbers

What would you like to know?"""

# Initialize session
if 'messages' not in st.session_state:
    st.session_state.messages = []

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

# Chat input
question = st.chat_input("Type your question here...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    response = get_response(question)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Welcome message
if not st.session_state.messages:
    st.info("👋 **Hello!** I'm CampusBot. Ask me about admissions, fees, placements, facilities, clubs, or just say hi! 😊")