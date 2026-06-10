import streamlit as st
import os
import re
from PyPDF2 import PdfReader
import google.generativeai as genai

# ============================================
# Page Configuration
# ============================================
st.set_page_config(page_title="Campus Chatbot with PDF Upload", page_icon="🎓", layout="wide")

# ============================================
# Get API Key from Streamlit Secrets
# ============================================
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except:
    st.error("⚠️ Google API Key not found in Secrets. Please add GOOGLE_API_KEY.")
    st.stop()

# ============================================
# Initialize Model - Use the correct model name
# ============================================
@st.cache_resource
def init_model():
    """Initialize Gemini model with correct configuration"""
    try:
        # List available models for debugging
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        # Try models in order of preference
        preferred_models = [
            'models/gemini-2.0-flash-exp',
            'models/gemini-2.0-flash',
            'models/gemini-1.5-flash',
            'models/gemini-pro'
        ]
        
        for model_name in preferred_models:
            if model_name in available_models or 'gemini' in model_name:
                try:
                    model = genai.GenerativeModel(model_name)
                    # Quick test
                    test_response = model.generate_content("test")
                    print(f"✅ Using model: {model_name}")
                    return model
                except:
                    continue
        
        # If no model works, try the first available
        if available_models:
            first_model = available_models[0]
            model = genai.GenerativeModel(first_model)
            return model
            
        return None
    except Exception as e:
        st.error(f"Model init error: {e}")
        return None

# ============================================
# Initialize Session State
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "model" not in st.session_state:
    st.session_state.model = None

# Initialize model on first run
if st.session_state.model is None:
    with st.spinner("Initializing AI model..."):
        st.session_state.model = init_model()

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
    <h1>🎓 Campus Chatbot with PDF Upload</h1>
    <p>Upload PDFs and ask questions - AI answers based on your documents!</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# Extract PDF Text
# ============================================
def extract_pdf_text(uploaded_file):
    """Extract text from uploaded PDF"""
    text = ""
    try:
        pdf_reader = PdfReader(uploaded_file)
        for page_num, page in enumerate(pdf_reader.pages):
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
# Get AI Response based on PDF content
# ============================================
def get_response(question, pdf_content):
    """Get response from Gemini based on PDF content"""
    if not pdf_content:
        return "📚 **Please upload PDF files first!**\n\nGo to the sidebar, upload your PDFs, and click 'Process PDFs' to start asking questions."
    
    if st.session_state.model is None:
        return "❌ **Model not initialized. Please refresh the page or check your API key.**"
    
    prompt = f"""You are Campus Bot, a helpful assistant for GNITS college.
    
    Answer questions based ONLY on the following document content. 
    
    DOCUMENT CONTENT:
    {pdf_content[:20000]}
    
    QUESTION: {question}
    
    RULES:
    - Answer ONLY based on the document content above
    - Be friendly and helpful
    - If the answer is not in the document, say "I don't have that information in the uploaded PDFs"
    - Keep answers concise
    
    ANSWER:"""
    
    try:
        response = st.session_state.model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def get_simple_response(question):
    """Fallback response when no PDFs are uploaded"""
    q = question.lower()
    if re.search(r'(hi|hello|hey)', q):
        return "Hello! 👋 Welcome to Campus Chatbot! Please upload PDF files first, then I can answer questions based on them. 😊"
    else:
        return "📚 **Welcome to Campus Chatbot!**\n\nPlease upload PDF files in the sidebar and click 'Process PDFs'.\n\nThen I can answer any question based on those documents! 📄"

# ============================================
# Sidebar - PDF Upload Section
# ============================================
with st.sidebar:
    st.markdown("### 📄 Upload PDF Documents")
    
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload PDFs containing academic information"
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
        st.info(f"📊 Active: {len(st.session_state.uploaded_files)} PDF(s) loaded")
    
    st.markdown("---")
    st.markdown("### ℹ️ How it works")
    st.info("""
    1. 📄 Upload PDF files
    2. 🔄 Click 'Process PDFs'
    3. 💬 Ask questions
    4. 🤖 AI answers based on your PDFs
    """)
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ============================================
# Main Chat Interface
# ============================================
# Show model status
if st.session_state.model:
    st.success("✅ AI Model Ready")
else:
    st.error("❌ AI Model Failed to Load. Please check your API key.")
    st.info("Go to Settings → Secrets and make sure GOOGLE_API_KEY is set correctly.")

if st.session_state.pdf_text:
    st.success(f"✅ Knowledge Base Active: {len(st.session_state.uploaded_files)} PDF(s) loaded")
else:
    st.warning("⚠️ No PDFs processed. Upload PDFs in the sidebar and click 'Process PDFs'.")

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
question = st.chat_input("Ask about your uploaded PDFs...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    
    with st.chat_message("user"):
        st.markdown(question)
    
    with st.chat_message("assistant"):
        with st.spinner("🤔 Reading your documents..."):
            try:
                if st.session_state.pdf_text and st.session_state.model:
                    answer = get_response(question, st.session_state.pdf_text)
                elif not st.session_state.pdf_text:
                    answer = get_simple_response(question)
                else:
                    answer = "❌ **AI Model not available.** Please check your API key in Secrets."
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)

if not st.session_state.messages:
    if st.session_state.pdf_text:
        st.info("📚 **Ready!** Ask me anything about your uploaded PDFs! 🎓")
    else:
        st.info("📄 **Upload PDF files** in the sidebar and click 'Process PDFs' to start asking questions!")
