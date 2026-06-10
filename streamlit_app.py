import streamlit as st
import re
import openai

# ============================================
# SECURE: Get API key from Streamlit Secrets
# DO NOT hardcode your key here!
# ============================================
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except:
    openai.api_key = None
# ============================================

st.set_page_config(page_title="Campus Chatbot", page_icon="🎓", layout="wide")

# Custom CSS - White/Light Theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
    }
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        font-size: 2rem;
        color: white;
    }
    .main-header p {
        color: rgba(255,255,255,0.9);
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
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
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
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102,126,234,0.4);
    }
    .stTextInput > div > div > input {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 25px;
        padding: 12px 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🎓 Campus Chatbot</h1>
    <p>GNITS IT Syllabus | R25 Regulations (2025-2026) | Complete Academic Guide</p>
</div>
""", unsafe_allow_html=True)

# ============ IT SYLLABUS DATABASE (Fallback) ============

IT_SYLLABUS = {
    "i_year_i_sem": """📚 **I YEAR I SEMESTER (R25) - 20 Credits**

| Course | Subject | Credits |
|--------|---------|---------|
| BSC | Matrices and Calculus | 4 |
| BSC | Advanced Engineering Physics | 3 |
| ESC | Programming for Problem Solving | 3 |
| ESC | Basic Electrical Engineering | 3 |
| MEC | Engineering Drawing & CAD | 3 |
| Lab | Advanced Engineering Physics Lab | 1 |
| Lab | Programming Lab | 1 |
| Lab | Basic Electrical Engineering Lab | 1 |
| Lab | IT Workshop | 1 |""",

    "attendance": """📊 **ATTENDANCE REQUIREMENTS (R25):**
• Minimum 75% attendance required
• Shortage up to 10% (65-74%) can be condoned
• Below 65% → NO condonation, detained""",

    "grading": """🎯 **GRADING SYSTEM (R25):**
| % Marks | Grade | Points |
|---------|-------|--------|
| ≥ 90% | O | 10 |
| 80-89% | A+ | 9 |
| 70-79% | A | 8 |
| 60-69% | B+ | 7 |
| 50-59% | B | 6 |
| 40-49% | C | 5 |
| < 40% | F | 0 |""",

    "fee": """💰 **FEE STRUCTURE:**
• B.Tech: ₹1,62,000 per year + JNTUH fees
• M.Tech: ₹1,12,000 per year
• NRI Category: USD 5,000 + JNTUH fees
📞 Contact Admissions: 040-29565856""",

    "placements": """🏆 **PLACEMENTS:**
• Highest Package: 50 LPA (Microsoft)
• Second Highest: 42.6 LPA (ServiceNow)
• Top Recruiters: Microsoft, ServiceNow, Deloitte, Snowflake, PwC""",

    "sgpa_cgpa": """📊 **SGPA & CGPA:**
SGPA = Σ(Credit × Grade Point) / Σ(Credits)
Percentage = (CGPA - 0.5) × 10""",

    "exam_pattern": """📝 **EXAM PATTERN:**
• CIE (Internal): 40 marks
• SEE (End Sem): 60 marks
• Duration: 3 hours""",

    "pe_electives": """📚 **PROFESSIONAL ELECTIVES (PE1-PE6):**

**PE-1 (III-I):** Distributed Systems | AI | Cryptography | Optimization
**PE-2 (III-II):** High Performance Computing | Deep Learning | Web Security | Software Testing
**PE-3 (IV-I):** Distributed Databases | Data Analytics | Secure Coding | Mobile Computing
**PE-4 (IV-I):** Scalable Architecture | Data Mining | Blockchain | 5G Technologies
**PE-5 (IV-II):** Edge/Fog Computing | Reinforcement Learning | Cloud Security | Quantum Computing
**PE-6 (IV-II):** AR/VR | Generative AI | Digital Forensics | Storage Area Networks"""
}

def get_rule_based_response(question):
    """Fallback response when OpenAI is not available"""
    q = question.lower().strip()
    
    if re.search(r'(i year|1st year|semester 1)', q):
        return IT_SYLLABUS["i_year_i_sem"]
    if re.search(r'(attendance|75%)', q):
        return IT_SYLLABUS["attendance"]
    if re.search(r'(grade|grading|gpa|cgpa)', q):
        return IT_SYLLABUS["grading"] + "\n\n" + IT_SYLLABUS["sgpa_cgpa"]
    if re.search(r'(exam|pattern|cie|see)', q):
        return IT_SYLLABUS["exam_pattern"]
    if re.search(r'(professional elective|pe)', q):
        return IT_SYLLABUS["pe_electives"]
    if re.search(r'(fee|cost|price|tuition)', q):
        return IT_SYLLABUS["fee"]
    if re.search(r'(placement|package|salary|lpa|microsoft|servicenow)', q):
        return IT_SYLLABUS["placements"]
    if re.search(r'(library|hostel|canteen|sports)', q):
        return "📚 **FACILITIES:**\n\nLibrary: 8 AM - 8 PM\nHostel: Girls hostel with security\nSports, Canteen available"
    if re.search(r'^hi|hello|hey', q):
        return "Hello! 👋 Welcome to Campus Chatbot! How can I help you today?"
    
    return """😊 **I'm Campus Chatbot!**

Ask me about:
• 📚 I, II, III, IV Year IT syllabus
• 📊 Attendance (75% required)
• 🎯 Grading system (O to F)
• 💰 Fee structure (B.Tech: ₹1.62L)
• 🏆 Placements (50 LPA highest)
• 📝 Exam pattern (CIE + SEE)
• 🎓 Professional Electives (PE1-PE6)

Try: "What are I year subjects?" or "What is the fee?" """

def get_response(question):
    """Main response - tries OpenAI first, falls back to rule-based"""
    if openai.api_key:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": """You are Campus Bot, a helpful assistant for GNITS college.
                    Answer questions about IT syllabus, attendance (75% required), grading (O to F), 
                    SGPA/CGPA calculation, exam pattern (CIE 40% + SEE 60%), electives, 
                    fee structure (B.Tech ₹1.62L, M.Tech ₹1.12L), placements (highest 50 LPA Microsoft). 
                    Be friendly and use emojis occasionally. If unsure, say you don't know."""},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return get_rule_based_response(question)
    else:
        return get_rule_based_response(question)

# Initialize session
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.markdown("### 🎓 Campus Chatbot")
    st.info("""
    **R25 Regulations (2025-2026)**
    
    This assistant covers:
    - ✅ I, II, III, IV Year IT syllabus
    - ✅ Professional Electives (PE1-PE6)
    - ✅ Fee Structure & Placements
    - ✅ Academic Regulations
    """)
    
    # Show OpenAI status
    if openai.api_key:
        st.success("✅ OpenAI Connected")
    else:
        st.warning("⚠️ OpenAI API key not set. Add it in Settings → Secrets")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Quick questions
st.markdown("### 💡 Quick Questions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📚 I Year Syllabus", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "What are I year IT subjects?"})
        st.rerun()
with col2:
    if st.button("📊 Attendance", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "What is the attendance requirement?"})
        st.rerun()
with col3:
    if st.button("💰 Fee Structure", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "What is the fee for B.Tech?"})
        st.rerun()
with col4:
    if st.button("🏆 Placements", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "What is the placement record?"})
        st.rerun()

st.markdown("---")

# Chat display
st.markdown("### 💬 Ask me anything about GNITS")

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
                <strong>🎓 Campus Bot</strong><br>{msg["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Input
question = st.chat_input("Ask about IT syllabus, courses, fees, placements...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    response = get_response(question)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

if not st.session_state.messages:
    st.info("👋 **Hello!** I'm Campus Chatbot. Ask me about I, II, III, IV year IT subjects, attendance, grading, exams, fees, placements, or electives! 🎓")
