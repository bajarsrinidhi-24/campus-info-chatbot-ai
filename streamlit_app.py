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
# Initialize Gemini AI (FIXED)
# ============================================
def init_gemini():
    """Initialize Google Gemini AI from secrets"""
    try:
        # Try to get API key from secrets
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            # Use gemini-pro which is most stable
            model = genai.GenerativeModel('gemini-pro')
            # Quick test
            test_response = model.generate_content("OK")
            return model, 'gemini-pro'
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
if "pdf_full_text" not in st.session_state:
    st.session_state.pdf_full_text = ""
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# ============================================
# PDF Processing Functions (IMPROVED)
# ============================================
def extract_pdf_text(uploaded_file):
    """Extract text from uploaded PDF"""
    text = ""
    try:
        pdf_reader = PdfReader(uploaded_file)
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text

def process_pdfs(uploaded_files):
    """Process all uploaded PDFs and combine text"""
    all_text = ""
    for uploaded_file in uploaded_files:
        text = extract_pdf_text(uploaded_file)
        all_text += f"\n\n{'='*50}\n📄 FILE: {uploaded_file.name}\n{'='*50}\n{text}\n"
    return all_text

# ============================================
# Search PDF for Answer (IMPROVED)
# ============================================
def search_pdf_for_answer(question, pdf_text):
    """Search through PDF content to find relevant answer"""
    if not pdf_text or not question:
        return None
    
    question_lower = question.lower()
    
    # Extract keywords from question
    keywords = re.findall(r'\b\w{3,}\b', question_lower)
    stop_words = {'what', 'is', 'are', 'the', 'and', 'for', 'with', 'from', 'have', 'was', 'were', 'about', 'tell', 'explain', 'from', 'resume', 'pdf'}
    search_terms = [w for w in keywords if w not in stop_words]
    
    if not search_terms:
        return None
    
    # Search through PDF
    pdf_lines = pdf_text.split('\n')
    best_lines = []
    best_score = 0
    
    for i, line in enumerate(pdf_lines):
        if len(line) > 20:
            line_lower = line.lower()
            score = sum(1 for term in search_terms if term in line_lower)
            if score > best_score and score >= 1:
                best_score = score
                # Get surrounding context (3 lines before and after)
                start = max(0, i-2)
                end = min(len(pdf_lines), i+3)
                context = '\n'.join(pdf_lines[start:end])
                best_lines = [context]
    
    if best_lines and best_score > 0:
        result = f"📄 **From your uploaded PDF ({st.session_state.uploaded_files[0].name if st.session_state.uploaded_files else 'document'}):**\n\n"
        result += best_lines[0][:1500]
        return result
    
    return None

# ============================================
# GNITS College Data
# ============================================
GNITS_DATA = """
G. Narayanamma Institute of Technology and Sciences (GNITS), Hyderabad

📝 ADMISSIONS:
- UG: TG-EAPCET exam required. Eligibility: 10+2 with PCM
- Contact: 040-29565856

💰 FEE STRUCTURE:
- B.Tech: ₹1,62,000 per year
- M.Tech: ₹1,12,000 per year

🏆 PLACEMENTS:
- Highest Package: 50 LPA (Microsoft)
- Top Recruiters: Microsoft, ServiceNow, Deloitte

📚 FACILITIES:
- Library: 8 AM to 8 PM
- Hostel: Girls hostel with security
- Sports, Canteen available

📞 CONTACTS:
- Principal: 040-29565850
- Admissions: 040-29565856
- Placements: 040-29565860
"""

# ============================================
# IT Syllabus Database
# ============================================
IT_SYLLABUS = {
    "attendance": "📊 Attendance: 75% minimum required. 65-74% can be condoned.",
    "grading": "🎯 Grading: O(10), A+(9), A(8), B+(7), B(6), C(5), F(0). 40% to pass.",
    "pe_electives": """📚 **PROFESSIONAL ELECTIVES (PE1-PE6):**

PE-1: Distributed Systems | AI | Cryptography | Optimization
PE-2: High Performance Computing | Deep Learning | Web Security
PE-3: Distributed Databases | Data Analytics | Mobile Computing
PE-4: Scalable Architecture | Data Mining | Blockchain
PE-5: Edge Computing | Reinforcement Learning | Quantum Computing
PE-6: AR/VR | Generative AI | Digital Forensics"""
}

# ============================================
# Extract Name from User Message
# ============================================
def extract_name_from_message(message):
    patterns = [r'call me (\w+)', r'my name is (\w+)', r"i'?m (\w+)", r'i am (\w+)']
    for pattern in patterns:
        match = re.search(pattern, message.lower())
        if match:
            return match.group(1).capitalize()
    return None

# ============================================
# Get AI Response from Gemini
# ============================================
def get_gemini_response(question, context):
    if not gemini_model:
        return None
    
    prompt = f"""You are Campus Bot, a friendly assistant.

Context from PDF: {context[:3000]}

User Question: {question}

Answer based on the context. If not found, say so naturally."""

    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except:
        return None

# ============================================
# Main Response Function (IMPROVED)
# ============================================
def get_response(question):
    q = question.lower().strip()
    
    # 1. Check for name
    name = extract_name_from_message(question)
    if name:
        st.session_state.user_name = name
        return f"Nice to meet you, {name}! 👋 I'm Campus Bot. How can I help you today?"
    
    name_prefix = f"Hey {st.session_state.user_name}, " if st.session_state.user_name else ""
    
    # 2. SEARCH PDF FIRST (for questions about uploaded documents)
    if st.session_state.pdf_text:
        # Check if question is about resume or PDF
        if any(word in q for word in ['resume', 'pdf', 'document', 'file', 'experience', 'education', 'skills', 'project', 'work']):
            pdf_answer = search_pdf_for_answer(question, st.session_state.pdf_text)
            if pdf_answer:
                return pdf_answer
        
        # Also try general search
        pdf_answer = search_pdf_for_answer(question, st.session_state.pdf_text)
        if pdf_answer:
            return pdf_answer
    
    # 3. Try Gemini AI
    if gemini_model:
        context = st.session_state.pdf_text[:5000] if st.session_state.pdf_text else GNITS_DATA
        ai_response = get_gemini_response(question, context)
        if ai_response:
            return ai_response
    
    # 4. Rule-based responses
    if re.search(r'fee|fees|cost|tuition', q):
        return f"{name_prefix}{GNITS_DATA.split('💰 FEE STRUCTURE:')[1].split('🏆 PLACEMENTS:')[0]}"
    
    if re.search(r'admission|apply|eligibility', q):
        return f"{name_prefix}{GNITS_DATA.split('📝 ADMISSIONS:')[1].split('💰 FEE STRUCTURE:')[0]}"
    
    if re.search(r'placement|package|lpa', q):
        return f"{name_prefix}{GNITS_DATA.split('🏆 PLACEMENTS:')[1].split('📚 FACILITIES:')[0]}"
    
    if re.search(r'library|hostel|canteen|sports|facility', q):
        return f"{name_prefix}{GNITS_DATA.split('📚 FACILITIES:')[1].split('📞 CONTACTS:')[0]}"
    
    if re.search(r'attendance', q):
        return IT_SYLLABUS["attendance"]
    
    if re.search(r'grade|grading|gpa|cgpa', q):
        return IT_SYLLABUS["grading"]
    
    if re.search(r'professional elective|pe', q):
        return IT_SYLLABUS["pe_electives"]
    
    # 5. Casual
    if re.search(r'^(hi|hello|hey)', q):
        return f"{name_prefix}Hello! 👋 Welcome to Campus Bot! How can I help you?"
    
    if re.search(r'how are you', q):
        return f"{name_prefix}I'm doing great! 😊 Thanks for asking!"
    
    if re.search(r'thank|thanks', q):
        return f"{name_prefix}You're very welcome! 😊"
    
    # 6. Default with PDF info if available
    if st.session_state.pdf_text:
        return f"""{name_prefix}📄 **I see you've uploaded a PDF!**

Ask me specific questions about your document like:
- "What experience does this resume show?"
- "What skills are mentioned?"
- "Tell me about the education"
- "Summarize this document"

Or ask about GNITS college: admissions, fees, placements, facilities!

What would you like to know? 🎓"""
    
    return f"""{name_prefix}😊 **I'm here to help!**

You can ask me about:

📝 **Admissions & Eligibility**
💰 **Fee Structure**  
🏆 **Placements & Packages**
📚 **Facilities** (Library, Hostel, Sports)
📞 **Contact Numbers**
📖 **IT Syllabus**
📊 **Attendance & Grading Rules**

**Also:** Upload a PDF and ask questions about it!

**What would you like to know?** 🎓"""

# ============================================
# Custom CSS
# ============================================
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%); }
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
    }
    .main-header h1 { font-size: 2rem; color: white; }
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
        border: 1px solid #e0e0e0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# Header
# ============================================
st.markdown("""
<div class="main-header">
    <h1>🎓 Campus Chatbot</h1>
    <p>GNITS Info + PDF Upload + Gemini AI</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# Sidebar
# ============================================
with st.sidebar:
    st.markdown("### 📄 Upload PDF")
    uploaded_files = st.file_uploader("Choose PDF", type=['pdf'], accept_multiple_files=False)
    
    if uploaded_files:
        st.success(f"✅ {uploaded_files.name} selected")
        if st.button("🚀 Process PDF", use_container_width=True):
            with st.spinner("Processing PDF..."):
                st.session_state.pdf_text = process_pdfs([uploaded_files])
                st.session_state.uploaded_files = [uploaded_files]
                st.success("✅ PDF Processed!")
                st.rerun()
    
    if st.session_state.pdf_text:
        st.info(f"📊 PDF Loaded: {st.session_state.uploaded_files[0].name}")
    
    st.markdown("---")
    st.markdown("### 👤 Profile")
    if st.session_state.user_name:
        st.success(f"Name: {st.session_state.user_name}")
        if st.button("Reset Name", use_container_width=True):
            st.session_state.user_name = None
            st.rerun()
    else:
        st.info("Say 'Call me [name]'")
    
    st.markdown("---")
    st.markdown("### 🤖 AI Status")
    if gemini_model:
        st.success("✅ Google Gemini Active")
    else:
        st.warning("⚠️ Gemini not available")
        st.info("Add GOOGLE_API_KEY to Secrets")
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ============================================
# Main Chat
# ============================================
st.markdown("### 💬 Chat")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message"><strong>You</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message"><strong>🎓 Campus Bot</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)

question = st.chat_input("Ask about GNITS or your uploaded PDF...")

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
    if st.session_state.pdf_text:
        st.info(f"📄 **PDF Loaded: {st.session_state.uploaded_files[0].name}**\n\nAsk me questions about this document! Example: 'What experience is mentioned?' or 'Summarize this resume'")
    else:
        st.info("👋 **Hello!** Upload a PDF or ask about GNITS college!")
