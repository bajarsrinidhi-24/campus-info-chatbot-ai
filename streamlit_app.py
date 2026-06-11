import streamlit as st
import re
import os
import tempfile
from PyPDF2 import PdfReader
from difflib import get_close_matches

# ============================================
# Try to import Google Gemini AI
# ============================================
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
# Initialize Gemini AI (if API key available)
# ============================================
def init_gemini():
    """Initialize Google Gemini AI from secrets"""
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            # Try different model names
            models_to_try = [
                'gemini-2.0-flash-lite',
                'gemini-2.0-flash', 
                'gemini-1.5-flash',
                'gemini-pro'
            ]
            for model_name in models_to_try:
                try:
                    model = genai.GenerativeModel(model_name)
                    # Quick test
                    test_response = model.generate_content("OK")
                    return model, model_name
                except:
                    continue
    except Exception as e:
        st.error(f"Gemini init error: {e}")
    return None, None

# Initialize Gemini
gemini_model, gemini_model_name = init_gemini()

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
# Spelling Correction Function
# ============================================
def correct_spelling(word, word_list):
    """Correct spelling mistakes using fuzzy matching"""
    matches = get_close_matches(word.lower(), word_list, n=1, cutoff=0.6)
    if matches:
        return matches[0]
    return word

def preprocess_question(question):
    """Preprocess question to handle spelling mistakes"""
    keywords = [
        'admission', 'fee', 'placement', 'library', 'hostel', 'canteen', 
        'sports', 'club', 'event', 'contact', 'principal', 'attendance',
        'grade', 'exam', 'syllabus', 'semester', 'btech', 'mtech',
        'cse', 'it', 'ece', 'eee', 'gnits', 'college', 'sum', 'rule'
    ]
    
    words = question.split()
    corrected_words = []
    for word in words:
        if len(word) > 3:
            corrected = correct_spelling(word, keywords)
            corrected_words.append(corrected)
        else:
            corrected_words.append(word)
    
    return ' '.join(corrected_words)

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
# Search PDF Content for Answer
# ============================================
def search_pdf_for_answer(question, pdf_text):
    """Search through PDF content to find relevant answer"""
    if not pdf_text:
        return None
    
    keywords = question.lower().split()
    stop_words = {'what', 'is', 'are', 'the', 'a', 'an', 'of', 'to', 'for', 'in', 'on', 'at', 'by', 'with', 'from'}
    search_terms = [w for w in keywords if w not in stop_words and len(w) > 2]
    
    if not search_terms:
        return None
    
    pdf_lines = pdf_text.split('\n')
    best_line = None
    best_score = 0
    
    for line in pdf_lines:
        if len(line) > 30:
            line_lower = line.lower()
            score = sum(1 for term in search_terms if term in line_lower)
            if score > best_score and score >= 1:
                best_score = score
                best_line = line
    
    if best_line and best_score > 0:
        return f"📄 **From your uploaded PDF:**\n\n{best_line[:600]}"
    
    return None

# ============================================
# GNITS College Data (Hardcoded)
# ============================================
GNITS_DATA = """
G. Narayanamma Institute of Technology and Sciences (GNITS), Hyderabad

📝 ADMISSIONS:
- UG: TG-EAPCET exam required. Eligibility: 10+2 with PCM
- PG: Based on GATE or TS-PGECET
- Contact: 040-29565856

💰 FEE STRUCTURE:
- B.Tech: ₹1,62,000 per year + JNTUH fees
- M.Tech: ₹1,12,000 per year

🏆 PLACEMENTS:
- Highest: 50 LPA (Microsoft)
- Top Recruiters: Microsoft, ServiceNow, Deloitte, Snowflake

📚 FACILITIES:
- Library: 8 AM to 8 PM
- Hostel: Girls hostel with security
- Sports, Canteen available

🎉 CLUBS:
- Coding Club, Robotics Club, EDC, Cultural Committee

📞 CONTACTS:
- Principal: 040-29565850
- Admissions: 040-29565856
- Placements: 040-29565860
"""

# ============================================
# IT Syllabus Database
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
| Lab | Physics Lab | 1 |
| Lab | Programming Lab | 1 |
| Lab | Electrical Lab | 1 |
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

    "sgpa_cgpa": """📊 **SGPA & CGPA:**

SGPA = Σ(Credit × Grade Point) / Σ(Credits)
Percentage = (CGPA - 0.5) × 10""",

    "exam_pattern": """📝 **EXAM PATTERN (R25):**

• CIE (Internal): 40 marks
• SEE (End Sem): 60 marks
• Duration: 3 hours""",

    "pe_electives": """📚 **PROFESSIONAL ELECTIVES (PE1-PE6):**

**PE-1:** Distributed Systems | AI | Cryptography | Optimization
**PE-2:** High Performance Computing | Deep Learning | Web Security
**PE-3:** Distributed Databases | Data Analytics | Mobile Computing
**PE-4:** Scalable Architecture | Data Mining | Blockchain
**PE-5:** Edge Computing | Reinforcement Learning | Quantum Computing
**PE-6:** AR/VR | Generative AI | Digital Forensics"""
}

# ============================================
# Get AI Response from Gemini
# ============================================
def get_gemini_response(question, context):
    """Get response from Google Gemini AI"""
    if not gemini_model:
        return None
    
    name_context = f"The user's name is {st.session_state.user_name}. " if st.session_state.user_name else ""
    
    prompt = f"""You are Campus Bot, a friendly assistant for GNITS college.

{name_context}
Context from college data:
{context}

User Question: {question}

Rules:
- Be friendly and conversational
- Use emojis occasionally
- Answer based on context
- For casual questions, respond naturally

Answer:"""

    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return None

# ============================================
# Main Response Function
# ============================================
def get_response(question):
    # Preprocess for spelling mistakes
    corrected_question = preprocess_question(question)
    q = corrected_question.lower().strip()
    
    # 1. Check for name setting
    extracted_name = extract_name_from_message(question)
    if extracted_name:
        st.session_state.user_name = extracted_name
        return f"Nice to meet you, {extracted_name}! 👋 I'm Campus Bot. How can I help you today?"
    
    name_prefix = f"Hey {st.session_state.user_name}, " if st.session_state.user_name else ""
    
    # 2. Search uploaded PDFs
    if st.session_state.pdf_text:
        pdf_answer = search_pdf_for_answer(question, st.session_state.pdf_text)
        if pdf_answer:
            return pdf_answer
    
    # 3. Build context for AI
    context = GNITS_DATA
    
    # 4. Try Gemini AI first (if available)
    if gemini_model:
        ai_response = get_gemini_response(question, context)
        if ai_response:
            return ai_response
    
    # 5. Rule-based fallback (works without AI)
    
    if re.search(r'fee|fees|cost|tuition', q):
        return f"{name_prefix}{GNITS_DATA.split('💰 FEE STRUCTURE:')[1].split('🏆 PLACEMENTS:')[0]}"
    
    if re.search(r'admission|apply|eligibility', q):
        return f"{name_prefix}{GNITS_DATA.split('📝 ADMISSIONS:')[1].split('💰 FEE STRUCTURE:')[0]}"
    
    if re.search(r'placement|package|lpa|recruiter', q):
        return f"{name_prefix}{GNITS_DATA.split('🏆 PLACEMENTS:')[1].split('📚 FACILITIES:')[0]}"
    
    if re.search(r'library|hostel|canteen|sports|facility', q):
        return f"{name_prefix}{GNITS_DATA.split('📚 FACILITIES:')[1].split('🎉 CLUBS:')[0]}"
    
    if re.search(r'club|event|hackathon|coding', q):
        return f"{name_prefix}{GNITS_DATA.split('🎉 CLUBS:')[1].split('📞 CONTACTS:')[0]}"
    
    if re.search(r'contact|phone|number', q):
        return f"{name_prefix}{GNITS_DATA.split('📞 CONTACTS:')[1]}"
    
    if re.search(r'i year|1st year|semester 1', q):
        return IT_SYLLABUS["i_year_i_sem"]
    
    if re.search(r'attendance|condonation', q):
        return IT_SYLLABUS["attendance"]
    
    if re.search(r'grade|grading|gpa|cgpa', q):
        return IT_SYLLABUS["grading"] + "\n\n" + IT_SYLLABUS["sgpa_cgpa"]
    
    if re.search(r'exam|pattern|cie|see', q):
        return IT_SYLLABUS["exam_pattern"]
    
    if re.search(r'professional elective|pe', q):
        return IT_SYLLABUS["pe_electives"]
    
    # Casual conversations
    if re.search(r'^(hi|hello|hey|namaste)', q):
        return f"{name_prefix}Hello! 👋 Welcome to Campus Bot! How can I help you today?"
    
    if re.search(r'how are you', q):
        return f"{name_prefix}I'm doing great! 😊 Thanks for asking! How can I assist you?"
    
    if re.search(r'thank|thanks', q):
        return f"{name_prefix}You're very welcome! 😊 Anything else I can help with?"
    
    if re.search(r'stressed|worried', q):
        return f"{name_prefix}Don't worry! 😊 You've got this! Take a deep breath. 💪"
    
    if re.search(r'sum rule', q):
        if st.session_state.pdf_text:
            return search_pdf_for_answer("sum rule", st.session_state.pdf_text)
        return f"{name_prefix}I don't see a PDF uploaded. Please upload a PDF containing the sum rule information."
    
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
    <p>GNITS College Info + IT Syllabus (R25) + PDF Upload + Gemini AI</p>
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
        st.info("Say 'Call me [name]'")
    
    st.markdown("---")
    st.markdown("### 🤖 AI Status")
    if gemini_model:
        st.success(f"✅ Google Gemini Active ({gemini_model_name})")
    else:
        st.warning("⚠️ Gemini not available. Add GOOGLE_API_KEY to Secrets")
    
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
    st.info("👋 **Hello!** I'm Campus Bot with Gemini AI. Say 'Call me [your name]' to personalize! Ask about GNITS college, IT syllabus, or upload PDFs. I handle spelling mistakes too! 😊")
