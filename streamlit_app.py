import streamlit as st
import re

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
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🎓 GNITS Campus Assistant</h1>
    <p>Ask me anything about GNITS - admissions, placements, fees, facilities, clubs, and more!</p>
</div>
""", unsafe_allow_html=True)

# College Information
COLLEGE_DATA = """
G. Narayanamma Institute of Technology and Sciences (GNITS), Hyderabad

ADMISSIONS:
- UG: TG-EAPCET exam required. Eligibility: 10+2 with PCM
- PG: Based on GATE or TS-PGECET
- Contact: 040-29565856

FEES:
- B.Tech: ₹1,62,000 per year + JNTUH fees
- M.Tech: ₹1,12,000 per year

PLACEMENTS:
- Highest: 50 LPA (Microsoft)
- Top Recruiters: Microsoft, ServiceNow, Deloitte, Snowflake

FACILITIES:
- Library: 8 AM - 8 PM
- Hostel: Girls hostel with 24/7 security
- Sports, Canteen available

CLUBS:
- Coding Club, Robotics Club, EDC, Cultural Committee

CONTACTS:
- Principal: 040-29565850
- Admissions: 040-29565856
- Placements: 040-29565860
"""

def get_response(question):
    q = question.lower()
    
    if re.search(r'(fee|fees|cost|price)', q):
        return "💰 **Fee Structure:**\n\nB.Tech: ₹1,62,000 per year\nM.Tech: ₹1,12,000 per year"
    
    if re.search(r'(admission|apply|eligibility)', q):
        return "📝 **Admissions:**\n\nUG: TG-EAPCET required\nPG: Based on GATE\nContact: 040-29565856"
    
    if re.search(r'(placement|package|salary|lpa)', q):
        return "🏆 **Placements:**\n\nHighest Package: 50 LPA (Microsoft)\nTop Recruiters: Microsoft, ServiceNow, Deloitte"
    
    if re.search(r'(library|hostel|canteen|sports|facility)', q):
        return "📚 **Facilities:**\n\nLibrary: 8 AM - 8 PM\nHostel: Girls hostel with security\nSports, Canteen available"
    
    if re.search(r'(club|event|fest)', q):
        return "🎉 **Clubs:**\n\nCoding Club, Robotics Club, EDC, Cultural Committee"
    
    if re.search(r'(contact|phone|number)', q):
        return "📞 **Contacts:**\n\nAdmissions: 040-29565856\nPrincipal: 040-29565850\nPlacements: 040-29565860"
    
    if re.search(r'^(hi|hello|hey)', q):
        return "Hello! 👋 Welcome to GNITS Campus Assistant! How can I help you today?"
    
    return "😊 I can help with: Admissions, Fees, Placements, Facilities, Clubs, Contacts. What would you like to know?"

# Initialize session
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 About")
    st.markdown("Ask me about GNITS college!")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Quick buttons
st.markdown("### 💡 Quick Questions")
cols = st.columns(4)
questions = ["💰 Fee Structure", "📝 Admissions", "🏆 Placements", "📞 Contacts"]
for i, q in enumerate(questions):
    if cols[i].button(q, use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": q})
        st.rerun()

st.markdown("---")

# Chat display
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message"><strong>You</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message"><strong>🎓 CampusBot</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)

# Input
question = st.chat_input("Type your question here...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    response = get_response(question)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

if not st.session_state.messages:
    st.info("👋 Ask me about admissions, fees, placements, facilities, clubs, or contacts!")