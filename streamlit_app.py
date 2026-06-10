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
# Initialize Gemini Model
# ============================================
@st.cache_resource
def get_model():
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        test_response = model.generate_content("OK")
        return model
    except Exception as e:
        st.error(f"Model error: {e}")
        return None

model = get_model()

# ============================================
# GNITS Website Data
# ============================================
GNITS_WEBSITE_DATA = """
G. Narayanamma Institute of Technology and Sciences (GNITS), Hyderabad

📝 ADMISSIONS:
- UG: TG-EAPCET exam required. Eligibility: 10+2 with PCM
- PG: Based on GATE or TS-PGECET
- Contact Admissions: 040-29565856

💰 FEE STRUCTURE:
- B.Tech: ₹1,62,000 per year + JNTUH fees
- M.Tech: ₹1,12,000 per year

🏆 PLACEMENTS:
- Highest Package: 50 LPA (Microsoft)
- Top Recruiters: Microsoft, ServiceNow, Deloitte, Snowflake

📚 FACILITIES:
- Library: 8 AM to 8 PM (Monday-Saturday)
- Hostel: Girls hostel with 24/7 security
- Sports, Canteen available

🎉 CLUBS:
- Coding Club, Robotics Club, EDC, Cultural Committee

📞 CONTACTS:
- Principal: 040-29565850
- Admissions: 040-29565856
- Placements: 040-29565860
"""

# ============================================
# Session State
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
# PDF Processing
# ============================================
def extract_pdf_text(uploaded_file):
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
# Response Generation
# ============================================
def get_response(question):
    # Check if user is telling their name
    extracted_name = extract_name_from_message(question)
    if extracted_name:
        st.session_state.user_name = extracted_name
        return f"Nice to meet you, {extracted_name}! 👋 I'm Campus Bot. How can I help you today?"
    
    # Build context
    context_sources = []
    context_sources.append(f"GNITS WEBSITE:\n{GNITS_WEBSITE_DATA}")
    
    if st.session_state.pdf_text:
        context_sources.append(f"UPLOADED PDFS:\n{st.session_state.pdf_text[:15000]}")
    
    combined_context = "\n\n---\n\n".join(context_sources)
    
    # Personalized prompt with user's name
    name_context = ""
    if st.session_state.user_name:
        name_context = f"The user's name is {st.session_state.user_name}. Call them by their name in responses."
    
    prompt = f"""You are Campus Bot, a helpful assistant for GNITS college.
    
    {name_context}
    
    SOURCES:
    {combined_context}
    
    QUESTION: {question}
    
    RULES:
    - Be friendly and conversational
    - Use emojis occasionally
    - If you know the user's name, use it naturally in your response
    - For casual questions like "How are you?", respond naturally and ask how you can help
    - Answer based on sources when possible
    
    ANSWER:"""
    
    try:
        if model:
            response = model.generate_content(prompt)
            return response.text
        else:
            return "Model not available. Please check API key."
    except Exception as e:
        return f"Error: {str(e)}"

def get_welcome_message():
    if st.session_state.user_name:
        return f"Welcome back, {st.session_state.user_name}! 👋 How can I help you with GNITS today?"
    else:
        return "👋 **Hello!** I'm Campus Bot. You can tell me your name by saying 'Call me [name]' or 'My name is [name]'. Ask me about GNITS college, upload PDFs, or just chat with me! 😊"

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
        "Choose PDF files", type=['pdf'], accept_multiple_files=True
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) selected")
        if st.button("🚀 Process PDFs", use_container_width=True):
            with st.spinner("Processing..."):
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
        st.info("No name set. Say 'Call me [name]'")
    
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
st.success("✅ GNITS Website Data Loaded")
if st.session_state.pdf_text:
    st.success(f"✅ PDF Knowledge Base Active")
if model:
    st.success("✅ AI Model Ready")

st.markdown("### 💬 Chat with Campus Bot")

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end;">
            <div class="user-message"><strong>You</strong><br>{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start;">
            <div class="bot-message"><strong>🎓 Campus Bot</strong><br>{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

# Chat input
question = st.chat_input("Ask about GNITS, uploaded PDFs, or tell me your name...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    
    with st.chat_message("user"):
        st.markdown(question)
    
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            if model:
                answer = get_response(question)
            else:
                answer = "Model not available. Please check API key."
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

if not st.session_state.messages:
    st.info(get_welcome_message())
