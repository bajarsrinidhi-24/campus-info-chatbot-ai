import streamlit as st
import re
import os
import tempfile
from PyPDF2 import PdfReader
import google.generativeai as genai

# ============================================
# Page Configuration
# ============================================
st.set_page_config(page_title="Campus Chatbot", page_icon="🎓", layout="wide")

# ============================================
# Get API Key from Streamlit Secrets
# ============================================
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except:
    st.error("⚠️ Google API Key not found in Secrets")
    st.stop()

# ============================================
# Initialize Gemini Model - gemini-2.0-flash-lite
# ============================================
@st.cache_resource
def get_model():
    try:
        # Using gemini-2.0-flash-lite for higher free tier limits
        # Free tier: ~100+ requests per day
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        # Test the model
        test_response = model.generate_content("OK")
        st.success("✅ AI Model Ready (gemini-2.0-flash-lite)")
        return model
    except Exception as e:
        st.error(f"Model error: {e}")
        return None

model = get_model()

# ============================================
# GNITS Website Data (Pre-scraped knowledge)
# ============================================
GNITS_WEBSITE_DATA = """
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
# Session State Initialization
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

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
# Response Generation
# ============================================
def get_response(question):
    """Generate response using ALL available sources"""
    
    # Build context from all sources
    context_sources = []
    
    # 1. Add GNITS Website Data
    context_sources.append(f"GNITS WEBSITE INFORMATION:\n{GNITS_WEBSITE_DATA}")
    
    # 2. Add PDF content if available
    if st.session_state.pdf_text:
        context_sources.append(f"UPLOADED PDF DOCUMENTS:\n{st.session_state.pdf_text[:15000]}")
    
    combined_context = "\n\n---\n\n".join(context_sources)
    
    prompt = f"""You are Campus Bot, a helpful assistant for GNITS college.
    
    Use the following information to answer questions. If the information is not in any source, use your general knowledge but be honest that it's not from official sources.
    
    SOURCES:
    {combined_context}
    
    QUESTION: {question}
    
    INSTRUCTIONS:
    - Be friendly and conversational
    - Use emojis occasionally
    - If answering from personal knowledge (not sources), say "Based on general knowledge..."
    - For casual questions like "How are you?", respond naturally
    
    ANSWER:"""
    
    try:
        if model:
            response = model.generate_content(prompt)
            return response.text
        else:
            return "Model not available. Please check API key."
    except Exception as e:
        return f"Error: {str(e)}"

def get_simple_response(question):
    """Fallback response when no model is available"""
    q = question.lower()
    if re.search(r'(hi|hello|hey)', q):
        return "Hello! 👋 Welcome to Campus Chatbot! How can I help you today?"
    else:
        return "📚 **Welcome to Campus Chatbot!**\n\nAsk me about GNITS college, upload PDFs, or just chat with me! 😊"

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
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# Header
# ============================================
st.markdown("""
<div class="main-header">
    <h1>🎓 Campus Chatbot</h1>
    <p>GNITS Website Info + PDF Documents + AI Assistant</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# Sidebar
# ============================================
with st.sidebar:
    st.markdown("### 📄 Upload PDF Documents")
    
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload additional PDFs (syllabus, regulations, etc.)"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) selected")
        
        if st.button("🚀 Process PDFs", use_container_width=True):
            with st.spinner("📚 Processing PDFs..."):
                st.session_state.pdf_text = process_pdfs(uploaded_files)
                st.session_state.uploaded_files = uploaded_files
                st.success(f"✅ Processed {len(uploaded_files)} PDF(s)!")
                st.rerun()
    
    if st.session_state.pdf_text:
        st.info(f"📊 PDFs Loaded: {len(st.session_state.uploaded_files)}")
    
    st.markdown("---")
    st.markdown("### ℹ️ Data Sources")
    st.info("""
    ✅ **GNITS Website** (Always available)
    ✅ **Uploaded PDFs** (Your documents)
    ✅ **Gemini AI** (General knowledge)
    """)
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ============================================
# Main Chat Interface
# ============================================
# Status indicators
st.success("✅ GNITS Website Data Loaded")
if st.session_state.pdf_text:
    st.success(f"✅ PDF Knowledge Base Active ({len(st.session_state.uploaded_files)} file(s))")
if model:
    st.success("✅ AI Model Ready (gemini-2.0-flash-lite)")
else:
    st.error("❌ AI Model Failed to Load")

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
question = st.chat_input("Ask about GNITS, uploaded PDFs, or anything...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    
    with st.chat_message("user"):
        st.markdown(question)
    
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                if model:
                    answer = get_response(question)
                else:
                    answer = get_simple_response(question)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error: {e}")

if not st.session_state.messages:
    st.info("👋 **Hello!** Ask me about GNITS college, your uploaded PDFs, or just chat with me! 😊")
