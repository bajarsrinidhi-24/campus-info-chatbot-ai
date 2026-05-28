import streamlit as st
import re
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="GNITS AI Assistant",
    page_icon="🎓",
    layout="wide"
)

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.title("🎓 GNITS AI")

    st.markdown("### 💬 Chats")

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []

    st.text_input("🔍 Search Chats")

    st.markdown("---")

    st.markdown("### 📌 Pinned Chats")
    st.markdown("""
    - 📍 Placement Queries  
    - 📍 Fee Structure  
    """)

    st.markdown("---")

    st.markdown("### 🕒 Recent Chats")
    st.markdown("""
    - Admission Details  
    - Hostel Facilities  
    - Clubs & Events  
    - Placement Packages  
    """)

    st.markdown("---")

    st.markdown("### 📂 Menu")
    st.markdown("""
    - 📁 Projects  
    - 📚 Library  
    - 🧩 Apps  
    - ⚙️ More  
    """)

# ---------------- MAIN TITLE ----------------
st.title("🎓 GNITS Campus Assistant")
st.caption("Your smart AI chatbot for GNITS information")

# ---------------- CHAT HISTORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- RANDOM RESPONSES ----------------
default_responses = [
    "😊 I can help you with admissions, placements, fees, facilities, clubs, and contacts.",
    "🎓 Ask me anything related to GNITS college.",
    "📚 You can ask about library, hostel, placements, events, and admissions.",
    "🚀 I'm your GNITS AI assistant. Ask your question!",
]

# ---------------- BOT FUNCTION ----------------
def get_answer(question):

    q = question.lower()

    # Greetings
    if re.search(r'hi|hello|hey', q):
        return random.choice([
            "👋 Hello! Welcome to GNITS AI Assistant.",
            "😊 Hi there! How can I help you today?",
            "🎓 Hey! Ask me anything about GNITS."
        ])

    # Fee Structure
    elif re.search(r'fee|cost|price|tuition', q):
        return """
💰 **Fee Structure**

- B.Tech: ₹1,62,000 per year
- M.Tech: ₹1,12,000 per year
- Additional hostel fees applicable
"""

    # Admissions
    elif re.search(r'admission|apply|eligibility', q):
        return """
📝 **Admissions**

- Through TG-EAPCET
- 10+2 with PCM
- Counseling required
"""

    # Placements
    elif re.search(r'placement|package|salary|job|company', q):
        return """
🏆 **Placements**

- Highest Package: 50 LPA
- Companies:
  - Microsoft
  - Deloitte
  - ServiceNow
  - PwC
"""

    # Facilities
    elif re.search(r'library|hostel|canteen|sports|gym|lab', q):
        return """
📚 **Facilities**

- Library: 8 AM – 8 PM
- Hostel with security
- Sports courts
- Modern labs
"""

    # Clubs
    elif re.search(r'club|event|fest|hackathon', q):
        return """
🎉 **Clubs & Events**

- Coding Club
- Robotics Club
- Cultural Fest
- Hackathons
"""

    # Timings
    elif re.search(r'when|time|start|date', q):
        return random.choice([
            "⏰ Events usually start at 10 AM.",
            "📅 Hackathons generally happen in February.",
            "🎉 Splash Fest usually happens in October.",
            "📌 Check official GNITS website for exact dates."
        ])

    # Contacts
    elif re.search(r'contact|phone|email|number', q):
        return """
📞 **Contacts**

- Admissions: 040-29565856
- Placement Cell: 040-29565860
"""

    # About College
    elif re.search(r'about|college|gnits', q):
        return """
🏫 **About GNITS**

GNITS is a top women's engineering college in Hyderabad established in 1997.
"""

    # Random fallback
    else:
        return random.choice(default_responses)

# ---------------- DISPLAY OLD MESSAGES ----------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- CHAT INPUT ----------------
question = st.chat_input("Ask your question here...")

if question:

    # Store User Message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Display User Message
    with st.chat_message("user"):
        st.markdown(question)

    # Bot Reply
    answer = get_answer(question)

    # Store Bot Reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    # Display Bot Reply
    with st.chat_message("assistant"):
        st.markdown(answer)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("✨ Developed for GNITS Campus Assistant Project")
