import streamlit as st
import re
import random
from datetime import datetime

st.set_page_config(
    page_title="GNITS Academic Assistant",
    page_icon="🎓",
    layout="wide"
)

# ===================== CUSTOM CSS =====================
st.markdown("""
<style>

/* Main App Background */
.stApp {
    background-color: white;
    color: black;
}

/* Main Header */
.main-header {
    text-align: center;
    padding: 1.5rem;
    background: linear-gradient(135deg, #e94560 0%, #533483 100%);
    border-radius: 20px;
    margin-bottom: 2rem;
}

.main-header h1 {
    font-size: 2.2rem;
    color: white;
    margin: 0;
}

.main-header p {
    color: white;
}

/* User Chat Bubble */
.user-message {
    background: linear-gradient(135deg, #e94560 0%, #533483 100%);
    color: white;
    padding: 12px 18px;
    border-radius: 20px;
    margin: 10px 0;
    max-width: 75%;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
}

/* Bot Chat Bubble */
.bot-message {
    background: #f1f3f6;
    color: black;
    padding: 12px 18px;
    border-radius: 20px;
    margin: 10px 0;
    max-width: 75%;
    border: 1px solid #ddd;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #e94560 0%, #533483 100%);
    color: white;
    border-radius: 25px;
    border: none;
    padding: 0.5rem 1rem;
    font-weight: bold;
}

.stButton > button:hover {
    opacity: 0.9;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #f8f9fc;
}

/* Chat Input */
.stChatInputContainer {
    background-color: white;
}

/* Text Colors */
h1, h2, h3, h4, h5, h6, p, div, span {
    color: black;
}

</style>
""", unsafe_allow_html=True)

# ===================== HEADER =====================
st.markdown("""
<div class="main-header">
    <h1>🎓 GNITS Academic Assistant</h1>
    <p>R22 & R25 Regulations | Course Structure | Syllabus | Exam Rules</p>
</div>
""", unsafe_allow_html=True)

# ===================== SESSION =====================
if 'messages' not in st.session_state:
    st.session_state.messages = []

# ===================== KNOWLEDGE BASE =====================

ACADEMIC_RULES = {
    "attendance": """
📊 **ATTENDANCE REQUIREMENTS**

• Minimum 75% attendance required  
• 65-74% can be condoned  
• Below 65% → detained  
• Condonation fee applicable
""",

    "grading": """
🎯 **GRADING SYSTEM**

| Marks | Grade |
|--------|-------|
| 90+ | O |
| 80-89 | A+ |
| 70-79 | A |
| 60-69 | B+ |
| 50-59 | B |
| 40-49 | C |
| <40 | F |

✅ Minimum passing marks: 40%
""",

    "exam": """
📝 **EXAM PATTERN**

• Internal (CIE): 40 Marks  
• External (SEE): 60 Marks  
• 2 Mid Exams per semester  
• SEE Duration: 3 Hours
"""
}

# ===================== RESPONSE FUNCTION =====================

def get_academic_response(user_input):

    text = user_input.lower()

    # Greetings
    if re.search(r'hi|hello|hey', text):
        return """
👋 Hello! Welcome to GNITS Academic Assistant.

You can ask me about:
• Attendance
• Exams
• SGPA/CGPA
• Placements
• Clubs
• Fees
• Syllabus
"""

    # Attendance
    elif re.search(r'attendance|absent|condonation', text):
        return ACADEMIC_RULES["attendance"]

    # Grading
    elif re.search(r'grade|cgpa|sgpa|percentage', text):
        return ACADEMIC_RULES["grading"]

    # Exam
    elif re.search(r'exam|mid|internal|external', text):
        return ACADEMIC_RULES["exam"]

    # Placement
    elif re.search(r'placement|package|job|salary', text):
        return """
🏆 **PLACEMENT DETAILS**

✨ Highest Package: 50 LPA  
✨ Top Recruiters:
• Microsoft
• ServiceNow
• Deloitte
• PwC
"""

    # Facilities
    elif re.search(r'library|hostel|canteen|sports', text):
        return """
📚 **FACILITIES**

📖 Library: 8 AM - 8 PM  
🏠 Hostel Available  
🏃 Sports Facilities  
🍽️ Canteen Available
"""

    # Clubs
    elif re.search(r'club|hackathon|event|fest', text):
        return """
🎉 **CLUBS & EVENTS**

💻 Coding Club  
🤖 Robotics Club  
🎭 Cultural Committee  
📅 Splash Fest
"""

    # Fee
    elif re.search(r'fee|fees|cost|tuition', text):
        return """
💰 **FEE STRUCTURE**

B.Tech: ₹1,62,000/year  
M.Tech: ₹1,12,000/year
"""

    # Default
    else:
        return """
😊 I can help you with:

• Attendance Rules  
• Exams & Grading  
• Placements  
• Facilities  
• Clubs & Events  
• Fee Structure  

Please ask your question clearly.
"""

# ===================== SIDEBAR =====================

with st.sidebar:

    st.title("📚 GNITS Menu")

    st.markdown("### 💬 Chats")
    st.markdown("• New Chat")
    st.markdown("• Search Chats")
    st.markdown("• Recent Chats")

    st.markdown("---")

    st.markdown("### 📌 Features")
    st.markdown("• Projects")
    st.markdown("• Library")
    st.markdown("• Apps")
    st.markdown("• More")

    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.markdown("### 🌐 Website")
    st.markdown("[GNITS Official Site](https://gnits.ac.in)")

# ===================== QUICK QUESTIONS =====================

st.markdown("## 💡 Quick Questions")

col1, col2, col3, col4 = st.columns(4)

quick_questions = {
    "📊 Attendance": "What is attendance rule?",
    "🎯 CGPA": "How is CGPA calculated?",
    "📝 Exams": "Explain exam pattern",
    "🏆 Placements": "Highest placement package"
}

for i, (label, q) in enumerate(quick_questions.items()):
    if [col1, col2, col3, col4][i].button(label, use_container_width=True):
        st.session_state.messages.append(
            {"role": "user", "content": q}
        )

        answer = get_academic_response(q)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        st.rerun()

st.markdown("---")

# ===================== CHAT DISPLAY =====================

st.markdown("## 💬 Chat")

for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.markdown(f"""
        <div style="display:flex; justify-content:flex-end;">
            <div class="user-message">
                <b>You</b><br>
                {msg["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown(f"""
        <div style="display:flex; justify-content:flex-start;">
            <div class="bot-message">
                <b>🎓 GNITS Assistant</b><br>
                {msg["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ===================== CHAT INPUT =====================

question = st.chat_input("Ask your question about GNITS...")

if question:

    # Save User Message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Generate Response
    response = get_academic_response(question)

    # Save Bot Response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()

# ===================== WELCOME MESSAGE =====================

if len(st.session_state.messages) == 0:

    st.info("""
👋 Welcome to GNITS Academic Assistant!

Ask me anything about:
• Attendance
• Exams
• CGPA
• Placements
• Clubs
• Fee Structure
• Facilities
""")
