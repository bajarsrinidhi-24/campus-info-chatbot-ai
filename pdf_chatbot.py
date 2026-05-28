import streamlit as st
import re
import os

st.set_page_config(page_title="GNITS Syllabus Assistant", page_icon="📚", layout="wide")

# Load the extracted syllabus content
SYLLABUS_FILE = "syllabus/cse_syllabus.txt"

def load_syllabus():
    if os.path.exists(SYLLABUS_FILE):
        with open(SYLLABUS_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

SYLLABUS_CONTENT = load_syllabus()

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
        background: #667eea;
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
        background: #667eea;
        color: white;
        border-radius: 25px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>📚 GNITS Syllabus Assistant</h1>
    <p>CSE Department | R22 Regulations | Complete Academic Guide</p>
</div>
""", unsafe_allow_html=True)

def search_syllabus(question):
    """Search through the syllabus content for relevant information"""
    q = question.lower()
    results = []
    
    # Key sections to search
    sections = {
        "attendance": ["attendance", "75%", "condonation", "shortage"],
        "promotion": ["promotion", "credits", "year to", "next semester"],
        "grading": ["grade", "grading", "o grade", "a+", "sgpa", "cgpa"],
        "exam": ["exam", "mid", "semester end", "cie", "see", "evaluation"],
        "courses": ["b.tech", "course structure", "semester", "credits"]
    }
    
    # Simple keyword matching
    for keyword in ["attendance", "promotion", "credit", "grade", "exam", "cgpa", "sgpa", 
                    "elective", "project", "lab", "semester", "syllabus", "regulation"]:
        if keyword in q:
            # Find relevant paragraphs from syllabus
            lines = SYLLABUS_CONTENT.split('\n')
            for i, line in enumerate(lines):
                if keyword in line.lower() and len(line) > 50:
                    results.append(line[:500])
                    if len(results) >= 3:
                        break
            break
    
    if results:
        return "\n\n".join(results)
    
    # Default response
    return """📚 **I found information in the syllabus!**

Based on the GNITS CSE Syllabus (R22 Regulations), I can help you with:

• **Academic Regulations** - Attendance, Promotion, Grading
• **Course Structure** - I Year to IV Year courses
• **Examination Pattern** - CIE (40%) + SEE (60%)
• **Electives** - Professional Electives (PE1 to PE6)
• **Projects** - Mini Projects and Major Project
• **SGPA/CGPA Calculation**

What specific topic would you like to know about?

Example questions:
- "What is the attendance requirement?"
- "Tell me about III year courses"
- "How is CGPA calculated?"
- "List the professional electives" """

# Initialize session
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.markdown("### 📚 About")
    st.info(f"""
    This assistant is trained on:
    - GNITS Academic Regulations (R22)
    - CSE Course Structure (I to IV Year)
    - Exam Pattern & Grading System
    - Professional & Open Electives
    
    **Syllabus loaded:** {len(SYLLABUS_CONTENT):,} characters
    """)
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Quick questions
st.markdown("### 💡 Quick Questions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📊 Attendance", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "What is the attendance requirement?"})
        st.rerun()
with col2:
    if st.button("🎯 CGPA Calculation", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "How is CGPA calculated?"})
        st.rerun()
with col3:
    if st.button("📚 III Year Courses", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "What are the III year courses?"})
        st.rerun()
with col4:
    if st.button("🎓 Electives", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "List all professional electives"})
        st.rerun()

st.markdown("---")

# Chat display
st.markdown("### 💬 Ask about GNITS Syllabus")

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
                <strong>📚 Syllabus Assistant</strong><br>{msg["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Input
question = st.chat_input("Ask about GNITS syllabus, courses, rules...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    response = search_syllabus(question)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

if not st.session_state.messages:
    st.info("👋 **Hello!** I'm your GNITS Syllabus Assistant. I've been trained on the complete CSE syllabus (R22 Regulations). Ask me about attendance rules, course structure, exam pattern, electives, or anything from the syllabus! 📚")