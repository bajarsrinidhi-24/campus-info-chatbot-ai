import streamlit as st
import re
import os
import tempfile
from PyPDF2 import PdfReader

# ============================================
# Try to import AI libraries (optional)
# ============================================
try:
    import openai
    OPENAI_AVAILABLE = True
except:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except:
    GEMINI_AVAILABLE = False

# ============================================
# Page Configuration
# ============================================
st.set_page_config(page_title="Campus Chatbot", page_icon="🎓", layout="wide")

# ============================================
# Initialize AI Client (if API key available)
# ============================================
def init_ai_client():
    """Initialize OpenAI or Gemini client from secrets"""
    
    # Try OpenAI first
    try:
        openai.api_key = st.secrets.get("OPENAI_API_KEY")
        if openai.api_key:
            return "openai", openai
    except:
        pass
    
    # Try Gemini
    try:
        genai.configure(api_key=st.secrets.get("GOOGLE_API_KEY"))
        return "gemini", genai
    except:
        pass
    
    return None, None

AI_TYPE, AI_CLIENT = init_ai_client()

# ============================================
# Session State Initialization
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# ============================================
# PDF Processing Functions
# ============================================
def extract_pdf_text(uploaded_file):
    """Extract text from uploaded PDF"""
    text = ""
    try:
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text

def process_pdfs(uploaded_files):
    """Process all uploaded PDFs and combine text"""
    all_text = ""
    for uploaded_file in uploaded_files:
        text = extract_pdf_text(uploaded_file)
        all_text += f"\n\n--- {uploaded_file.name} ---\n\n{text}"
    return all_text

# ============================================
# Extract Name from User Message
# ============================================
def extract_name_from_message(message):
    """Extract name from phrases like 'call me X', 'my name is X', 'I am X'"""
    message_lower = message.lower()
    
    patterns = [
        r'call me (\w+)',
        r'my name is (\w+)',
        r"i'?m (\w+)",
        r'i am (\w+)',
        r'name is (\w+)',
        r'you can call me (\w+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, message_lower)
        if match:
            return match.group(1).capitalize()
    
    return None

# ============================================
# GNITS College Data (Hardcoded - Always Available)
# ============================================
GNITS_DATA = """
G. Narayanamma Institute of Technology and Sciences (GNITS), Hyderabad

📝 ADMISSIONS:
- UG: TG-EAPCET exam required. Eligibility: 10+2 with PCM
- PG: Based on GATE score or TS-PGECET
- Contact Admissions: 040-29565856

💰 FEE STRUCTURE:
- B.Tech: ₹1,62,000 per year + JNTUH fees
- M.Tech: ₹1,12,000 per year
- NRI Category: USD 5,000 + JNTUH fees

🏆 PLACEMENTS:
- Highest Package: 50 LPA (Microsoft)
- Second Highest: 42.6 LPA (ServiceNow)
- Top Recruiters: Microsoft, ServiceNow, Deloitte, Snowflake, PwC

📚 FACILITIES:
- Library: 8 AM to 8 PM (Monday-Saturday)
- Hostel: Girls hostel with 24/7 security
- Sports: Indoor badminton, table tennis, volleyball, basketball
- Canteen available

🎉 CLUBS & EVENTS:
- Coding Club (CodeChef, LeetCode competitions)
- Robotics Club
- Entrepreneurship Development Cell (EDC)
- Cultural Committee (Splash annual fest)
- Technical Club (GNITS ACM Student Chapter)

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
"""

# ============================================
# IT Syllabus Database (R25 Regulations)
# ============================================
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

    "i_year_ii_sem": """📚 **I YEAR II SEMESTER (R25) - 20 Credits**

| Course | Subject | Credits |
|--------|---------|---------|
| BSC | ODE and Vector Calculus | 3 |
| BSC | Engineering Chemistry | 3 |
| ESC | Data Structures | 3 |
| ESC | Basic Electronics | 3 |
| HSC | English for Skill Enhancement | 3 |
| Lab | Engineering Chemistry Lab | 1 |
| Lab | Data Structures Lab | 1 |
| Lab | English & Communication Skills Lab | 1 |
| Lab | Engineering Workshop | 1 |
| Lab | Python Programming Lab | 1 |""",

    "ii_year_i_sem": """📚 **II YEAR I SEMESTER (R25) - 22 Credits**

| Course | Subject | Credits |
|--------|---------|---------|
| BSC | Mathematical & Statistical Foundations | 3 |
| PC | Computer Organization & Microprocessor | 3 |
| PC | Java Programming | 3 |
| PC | Web Programming | 3 |
| PC | Introduction to IoT | 3 |
| HSC | Innovation and Entrepreneurship | 2 |
| Lab | Java Programming Lab | 1 |
| Lab | Web Programming Lab | 1 |
| Lab | Internet of Things Lab | 1 |
| SDC | Data Visualization | 1 |""",

    "ii_year_ii_sem": """📚 **II YEAR II SEMESTER (R25) - 20 Credits**

| Course | Subject | Credits |
|--------|---------|---------|
| PC | Discrete Mathematics | 3 |
| PC | Full Stack Development | 3 |
| PC | Operating Systems | 3 |
| PC | Database Management Systems | 3 |
| PC | Algorithm Design and Analysis | 3 |
| Lab | Full Stack Development Lab | 1 |
| Lab | Operating Systems Lab | 1 |
| Lab | DBMS Lab | 1 |
| SDC | UI Design - Flutter | 1 |""",

    "iii_year_i_sem": """📚 **III YEAR I SEMESTER (R25) - 21 Credits**

| Course | Subject | Credits |
|--------|---------|---------|
| PC | Software Engineering | 3 |
| PC | Machine Learning | 3 |
| PC | Computer Networks | 3 |
| PE1 | Professional Elective-I | 3 |
| OE1 | Open Elective-I | 2 |
| Lab | Software Engineering Lab | 1 |
| Lab | Machine Learning Lab | 1 |
| Lab | Computer Networks Lab | 1 |
| SDC | Prompt Engineering | 1 |""",

    "iii_year_ii_sem": """📚 **III YEAR II SEMESTER (R25) - 20 Credits**

| Course | Subject | Credits |
|--------|---------|---------|
| PC | Information Security | 3 |
| PC | Automata & Compiler Design | 3 |
| HSC | Business Economics | 3 |
| PE2 | Professional Elective-II | 3 |
| OE2 | Open Elective-II | 2 |
| Lab | Information Security Lab | 1 |
| Lab | Automata & Compiler Design Lab | 1 |
| Lab | DevOps Lab | 1 |
| SDC | Big Data - Spark | 1 |""",

    "iv_year_i_sem": """📚 **IV YEAR I SEMESTER (R25) - 21 Credits**

| Course | Subject | Credits |
|--------|---------|---------|
| PC | Cloud Computing | 3 |
| PC | Natural Language Processing | 3 |
| HSC | Fundamentals of Management | 3 |
| PE3 | Professional Elective-III | 3 |
| PE4 | Professional Elective-IV | 3 |
| OE3 | Open Elective-III | 2 |
| Lab | Cloud Computing Lab | 1 |
| Lab | NLP Lab | 1 |""",

    "iv_year_ii_sem": """📚 **IV YEAR II SEMESTER (R25) - 20 Credits**

| Course | Subject | Credits |
|--------|---------|---------|
| PE5 | Professional Elective-V | 3 |
| PE6 | Professional Elective-VI | 3 |
| PW | Project Work | 14 |""",

    "attendance": """📊 **ATTENDANCE REQUIREMENTS (R25):**

• Minimum 75% attendance required to appear for exams
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

    "sgpa_cgpa": """📊 **SGPA & CGPA:**

SGPA = Σ(Credit × Grade Point) / Σ(Credits)
Percentage = (CGPA - 0.5) × 10""",

    "exam_pattern": """📝 **EXAM PATTERN (R25):**

**Theory Courses (100 marks):**
• CIE: 40 marks (Mid-Terms:30, Assignments:5, Viva:5)
• SEE: 60 marks (Part-A:10, Part-B:50)
• Duration: 3 hours""",

    "pe_electives": """📚 **PROFESSIONAL ELECTIVES (PE1-PE6):**

**PE-1 (III-I):** Distributed Systems | AI | Cryptography | Optimization
**PE-2 (III-II):** High Performance Computing | Deep Learning | Web Security | Software Testing
**PE-3 (IV-I):** Distributed Databases | Data Analytics | Secure Coding | Mobile Computing
**PE-4 (IV-I):** Scalable Architecture | Data Mining | Blockchain | 5G Technologies
**PE-5 (IV-II):** Edge/Fog Computing | Reinforcement Learning | Cloud Security | Quantum Computing
**PE-6 (IV-II):** AR/VR | Generative AI | Digital Forensics | Storage Area Networks""",

    "open_electives": """📚 **OPEN ELECTIVES:**

**By CSE:** OS Fundamentals, SQL, Computer Networks
**By IT:** Java Programming, Full Stack, DBMS, DevOps
**By CSM/CSD:** AI, Machine Learning, Data Mining, NLP
**By ECE:** Image Processing, Wearable Devices"""
}

# ============================================
# AI-Powered Response (if available)
# ============================================
def get_ai_response(question, context):
    """Get response from AI (OpenAI or Gemini)"""
    
    prompt = f"""You are Campus Bot, a helpful assistant for GNITS college.
    
    Context from GNITS data and PDFs:
    {context}
    
    User question: {question}
    
    Rules:
    - Be friendly and conversational
    - Use emojis occasionally
    - If you know the user's name (from conversation), use it
    - Answer based on the context when possible
    - For casual questions, respond naturally
    
    Answer:"""
    
    try:
        if AI_TYPE == "openai":
            response = AI_CLIENT.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Campus Bot, a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        elif AI_TYPE == "gemini":
            model = AI_CLIENT.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text
    except Exception as e:
        return None
    
    return None

# ============================================
# Main Response Function (Hybrid: AI + Rule-based)
# ============================================
def get_response(question):
    q = question.lower().strip()
    
    # 1. Check for name setting (always rule-based for reliability)
    extracted_name = extract_name_from_message(question)
    if extracted_name:
        st.session_state.user_name = extracted_name
        return f"Nice to meet you, {extracted_name}! 👋 I'm Campus Bot. How can I help you today?"
    
    # 2. Get user's name for personalized responses
    name_prefix = f"Hey {st.session_state.user_name}, " if st.session_state.user_name else ""
    
    # 3. Build context from all sources
    context = GNITS_DATA
    if st.session_state.pdf_text:
        context += f"\n\nPDF CONTENT:\n{st.session_state.pdf_text[:5000]}"
    
    # 4. Try AI first if available (for better conversations)
    if AI_TYPE:
        try:
            ai_response = get_ai_response(question, context)
            if ai_response:
                return ai_response
        except:
            pass  # Fall back to rule-based
    
    # 5. Rule-based fallback responses (works without AI)
    
    # Casual conversations
    if re.search(r'^(hi|hello|hey|namaste|good morning|good afternoon|good evening)', q):
        return f"{name_prefix}Hello! 👋 Welcome to Campus Bot! How can I help you today?"
    
    if re.search(r'how are you|how\'s it going', q):
        return f"{name_prefix}I'm doing great! 😊 Thanks for asking! Ready to help you with GNITS info. How can I assist you?"
    
    if re.search(r'tell me a joke|make me laugh', q):
        jokes = [
            "Why did the student eat their homework? Because the teacher said it was a piece of cake! 😄",
            "What do you call a computer that sings? A Dell-ophone! 🎵",
            "Why did the programmer quit his job? Because he didn't get arrays! 😂"
        ]
        import random
        return f"{name_prefix}{random.choice(jokes)}"
    
    if re.search(r'thank|thanks|appreciate', q):
        return f"{name_prefix}You're very welcome! 😊 I'm always here to help with anything about GNITS. Feel free to ask anytime!"
    
    if re.search(r'stressed|worried|nervous', q):
        return f"{name_prefix}Don't worry! 😊 GNITS has great support systems. Take a deep breath, make a plan, and remember you've got this! 💪"
    
    if re.search(r'favorite thing about gnits', q):
        return f"{name_prefix}I love GNITS's strong placement record (50 LPA from Microsoft! 🏆) and the amazing clubs like Coding Club and Robotics Club! 🎓"
    
    # PDF content search
    if st.session_state.pdf_text and len(q) > 5:
        lines = st.session_state.pdf_text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in q.split()[:3]):
                if len(line) > 50:
                    return f"📄 **From your uploaded PDF:**\n\n{line[:500]}"
    
    # IT Syllabus queries
    if re.search(r'i year|1st year|first year|semester 1', q):
        return IT_SYLLABUS["i_year_i_sem"]
    if re.search(r'i year ii|1st year 2nd|i-ii', q):
        return IT_SYLLABUS["i_year_ii_sem"]
    if re.search(r'ii year|2nd year|second year|ii-i', q):
        return IT_SYLLABUS["ii_year_i_sem"]
    if re.search(r'ii year ii|2nd year 2nd|ii-ii', q):
        return IT_SYLLABUS["ii_year_ii_sem"]
    if re.search(r'iii year|3rd year|third year', q):
        return IT_SYLLABUS["iii_year_i_sem"]
    if re.search(r'iv year|4th year|fourth year|final year', q):
        return IT_SYLLABUS["iv_year_i_sem"]
    
    # Academic rules
    if re.search(r'attendance|condonation|75%', q):
        return IT_SYLLABUS["attendance"]
    if re.search(r'grade|grading|gpa|sgpa|cgpa', q):
        return IT_SYLLABUS["grading"] + "\n\n" + IT_SYLLABUS["sgpa_cgpa"]
    if re.search(r'exam|mid|see|cie|evaluation|pattern', q):
        return IT_SYLLABUS["exam_pattern"]
    if re.search(r'professional elective|pe', q):
        return IT_SYLLABUS["pe_electives"]
    
    # GNITS queries
    if re.search(r'fee|fees|cost|tuition', q):
        return f"{name_prefix}{GNITS_DATA.split('💰 FEE STRUCTURE:')[1].split('🏆 PLACEMENTS:')[0]}"
    if re.search(r'admission|apply|eligibility', q):
        return f"{name_prefix}{GNITS_DATA.split('📝 ADMISSIONS:')[1].split('💰 FEE STRUCTURE:')[0]}"
    if re.search(r'placement|package|recruiter|lpa', q):
        return f"{name_prefix}{GNITS_DATA.split('🏆 PLACEMENTS:')[1].split('📚 FACILITIES:')[0]}"
    if re.search(r'library|hostel|canteen|sports|facility', q):
        return f"{name_prefix}{GNITS_DATA.split('📚 FACILITIES:')[1].split('🎉 CLUBS & EVENTS:')[0]}"
    if re.search(r'club|event|hackathon|coding|robotics', q):
        return f"{name_prefix}{GNITS_DATA.split('🎉 CLUBS & EVENTS:')[1].split('📞 IMPORTANT CONTACTS:')[0]}"
    if re.search(r'contact|phone|number', q):
        return f"{name_prefix}{GNITS_DATA.split('📞 IMPORTANT CONTACTS:')[1].split('🏫 ABOUT:')[0]}"
    
    # Default
    return f"""{name_prefix}😊 **I'm here to help!**

You can ask me about:

📝 **Admissions & Eligibility**
💰 **Fee Structure**  
🏆 **Placements & Packages**
📚 **Facilities** (Library, Hostel, Sports)
🎉 **Clubs & Events**
📞 **Contact Numbers**
📖 **IT Syllabus** (I to IV Year)
📊 **Attendance & Grading Rules**

**Also:** Say "Call me [your name]" to personalize our chat!

**What would you like to know?** 🎓"""

# ============================================
# Custom CSS
# ============================================
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
</style>
""", unsafe_allow_html=True)

# ============================================
# Header
# ============================================
st.markdown("""
<div class="main-header">
    <h1>🎓 Campus Chatbot</h1>
    <p>GNITS College Info + IT Syllabus (R25) + PDF Upload</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# Sidebar
# ============================================
with st.sidebar:
    st.markdown("### 📄 Upload PDF Documents")
    
    uploaded_files = st.file_uploader(
        "Choose PDF files", type=['pdf'], accept_multiple_files=True
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) selected")
        if st.button("🚀 Process PDFs", use_container_width=True):
            with st.spinner("Processing PDFs..."):
                st.session_state.pdf_text = process_pdfs(uploaded_files)
                st.session_state.uploaded_files = uploaded_files
                st.success("✅ Processed!")
                st.rerun()
    
    if st.session_state.pdf_text:
        st.info(f"📊 PDFs Loaded: {len(st.session_state.uploaded_files)}")
    
    st.markdown("---")
    st.markdown("### 👤 Your Profile")
    if st.session_state.user_name:
        st.success(f"Name: {st.session_state.user_name}")
        if st.button("🔄 Reset Name", use_container_width=True):
            st.session_state.user_name = None
            st.rerun()
    else:
        st.info("Say 'Call me [name]' to set your name")
    
    st.markdown("---")
    st.markdown("### 🤖 AI Status")
    if AI_TYPE == "openai":
        st.success("✅ OpenAI Connected")
    elif AI_TYPE == "gemini":
        st.success("✅ Google Gemini Connected")
    else:
        st.warning("⚠️ No AI API key found. Using rule-based mode.")
        st.info("Add OPENAI_API_KEY or GOOGLE_API_KEY to Secrets")
    
    st.markdown("---")
    st.markdown("### 📚 Quick Resources")
    
    if st.button("📊 Attendance Rules", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "What is the attendance requirement?"})
        st.rerun()
    if st.button("🎯 Grading System", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "How is CGPA calculated?"})
        st.rerun()
    if st.button("🎓 Professional Electives", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "List professional electives"})
        st.rerun()
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ============================================
# Main Chat Interface
# ============================================
# Status indicators
col1, col2, col3 = st.columns(3)
with col1:
    st.success("✅ GNITS College Data")
with col2:
    st.success("✅ IT Syllabus (R25)")
with col3:
    if st.session_state.pdf_text:
        st.success(f"✅ PDFs: {len(st.session_state.uploaded_files)}")
    else:
        st.info("📄 Upload PDFs")

st.markdown("### 💬 Chat with Campus Bot")

# Display chat messages
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

# Chat input
question = st.chat_input("Ask about GNITS college, syllabus, or upload PDFs...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    
    with st.chat_message("user"):
        st.markdown(question)
    
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            response = get_response(question)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if not st.session_state.messages:
    st.info("👋 **Hello!** I'm Campus Bot. Say 'Call me [your name]' to personalize our chat! Ask me about GNITS college, IT syllabus, or upload PDFs. I can have natural conversations too! 😊")
