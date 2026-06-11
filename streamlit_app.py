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
# Initialize Gemini AI
# ============================================
def init_gemini():
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Test the model
            test_response = model.generate_content("OK")
            return model, 'gemini-1.5-flash'
    except Exception as e:
        st.error(f"Gemini init error: {e}")
    return None, None

gemini_model, gemini_model_name = init_gemini()

# ============================================
# Session State
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "pdf_full_text" not in st.session_state:
    st.session_state.pdf_full_text = ""
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# ============================================
# PDF Processing (Extract ALL text)
# ============================================
def extract_pdf_text(uploaded_file):
    """Extract ALL text from uploaded PDF"""
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

# ============================================
# Search PDF for Relevant Content (RAG)
# ============================================
def find_relevant_content(question, pdf_text, max_chunks=3):
    """Find most relevant chunks from PDF based on question"""
    if not pdf_text or not question:
        return None
    
    # Split PDF into chunks (paragraphs/sections)
    chunks = pdf_text.split('\n\n')
    relevant_chunks = []
    
    # Extract keywords from question
    question_lower = question.lower()
    keywords = set(re.findall(r'\b\w{4,}\b', question_lower))
    
    # Score each chunk based on keyword matches
    chunk_scores = []
    for chunk in chunks:
        if len(chunk) > 50:  # Ignore very small chunks
            chunk_lower = chunk.lower()
            score = sum(1 for keyword in keywords if keyword in chunk_lower)
            if score > 0:
                chunk_scores.append((score, chunk))
    
    # Sort by score and get top chunks
    chunk_scores.sort(reverse=True)
    for score, chunk in chunk_scores[:max_chunks]:
        relevant_chunks.append(chunk)
    
    return relevant_chunks

# ============================================
# Get AI Response using RAG
# ============================================
def get_response(question):
    q = question.lower().strip()
    
    # 1. Check for name setting
    name_match = re.search(r'call me (\w+)|my name is (\w+)|i am (\w+)|i\'m (\w+)', q)
    if name_match:
        name = next((g for g in name_match.groups() if g), None)
        if name:
            st.session_state.user_name = name.capitalize()
            return f"Nice to meet you, {st.session_state.user_name}! 👋 I'm Campus Bot. How can I help you today?"
    
    name_prefix = f"Hey {st.session_state.user_name}, " if st.session_state.user_name else ""
    
    # 2. Check if there's an uploaded PDF
    if st.session_state.pdf_text and st.session_state.uploaded_file:
        # Find relevant content from PDF
        relevant_chunks = find_relevant_content(question, st.session_state.pdf_text)
        
        if relevant_chunks and gemini_model:
            # Build prompt with relevant PDF content
            context = "\n\n---\n\n".join(relevant_chunks)
            
            prompt = f"""You are Campus Bot, a helpful assistant. Answer the question based on the provided document content.

DOCUMENT CONTENT (from {st.session_state.uploaded_file.name}):
{context[:8000]}

USER QUESTION: {question}

INSTRUCTIONS:
- Answer based ONLY on the document content above
- If the answer is not in the document, say "I couldn't find that information in the uploaded document."
- Be helpful and conversational
- Use emojis occasionally

ANSWER:"""
            
            try:
                response = gemini_model.generate_content(prompt)
                return response.text
            except Exception as e:
                return f"Error: {e}"
    
    # 3. No PDF uploaded - use general GNITS info
    # GNITS Data
    gnits_info = """
GNITS College Information:

ADMISSIONS: UG through TG-EAPCET exam. Contact: 040-29565856
FEES: B.Tech ₹1,62,000 per year, M.Tech ₹1,12,000 per year
PLACEMENTS: Highest 50 LPA (Microsoft). Top recruiters: Microsoft, ServiceNow, Deloitte
FACILITIES: Library 8 AM-8 PM, Hostel, Sports, Canteen
CONTACTS: Principal 040-29565850, Admissions 040-29565856, Placements 040-29565860
"""
    
    # Check if question is about GNITS
    gnits_keywords = ['gnits', 'college', 'admission', 'fee', 'placement', 'library', 'hostel', 'contact']
    if any(keyword in q for keyword in gnits_keywords):
        return f"{name_prefix}{gnits_info}"
    
    # 4. Default response
    if st.session_state.pdf_text:
        return f"""{name_prefix}📄 **Document loaded: {st.session_state.uploaded_file.name}**

Ask me anything about this document! For example:
- "Summarize this document"
- "What are the main points?"
- "Tell me about [specific topic]"

Or ask me about GNITS college information! 🎓"""
    else:
        return f"""{name_prefix}😊 **Welcome!**

📄 **Upload a PDF** to ask questions about its content
🏫 **Ask about GNITS college** (admissions, fees, placements)

What would you like to know? 🎓"""

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
    <p>Upload ANY PDF + Ask Questions + GNITS Info</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# Sidebar
# ============================================
with st.sidebar:
    st.markdown("### 📄 Upload Document")
    
    uploaded_file = st.file_uploader("Choose PDF file", type=['pdf'])
    
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name} selected")
        if st.button("🚀 Process Document", use_container_width=True):
            with st.spinner("Processing PDF..."):
                st.session_state.pdf_text = extract_pdf_text(uploaded_file)
                st.session_state.uploaded_file = uploaded_file
                st.success("✅ Document processed!")
                st.rerun()
    
    if st.session_state.pdf_text:
        st.info(f"📊 Active: {st.session_state.uploaded_file.name}")
    
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

question = st.chat_input("Ask about your document or GNITS college...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("🤔 Searching..."):
            response = get_response(question)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if not st.session_state.messages:
    if st.session_state.pdf_text:
        st.info(f"📄 **Document loaded: {st.session_state.uploaded_file.name}**\n\nAsk me anything about this document! Example: 'Summarize this document' or 'What are the main points?'")
    else:
        st.info("👋 **Hello!** Upload any PDF (resume, syllabus, article, report) and ask questions about it! Or ask about GNITS college!")
