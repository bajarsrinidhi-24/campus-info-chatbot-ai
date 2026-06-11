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
                    test_response = model.generate_content("OK")
                    return model, model_name
                except:
                    continue
    except Exception as e:
        st.sidebar.error(f"Gemini init error: {e}")
    return None, None

gemini_model, gemini_model_name = init_gemini()

# ============================================
# Session State
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = ""
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# ============================================
# PDF Processing
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
# GNITS College Information
# ============================================
GNITS_INFO = """
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
- Canteen: Available

🎉 CLUBS & EVENTS:
- Coding Club, Robotics Club, Entrepreneurship Cell
- Cultural Committee, Technical Club
- IEEE ICoECIT-2026, Splash Fest, Hackathon

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
# Extract Name from Message
# ============================================
def extract_name_from_message(message):
    patterns = [r'call me (\w+)', r'my name is (\w+)', r"i'?m (\w+)", r'i am (\w+)']
    for pattern in patterns:
        match = re.search(pattern, message.lower())
        if match:
            return match.group(1).capitalize()
    return None

# ============================================
# Main Response Function
# ============================================
def get_response(question):
    q = question.lower().strip()
    
    # 1. Check for name setting
    name = extract_name_from_message(question)
    if name:
        st.session_state.user_name = name
        return f"Nice to meet you, {name}! 👋 I'm Campus Bot. How can I help you today?"
    
    name_prefix = f"Hey {st.session_state.user_name}, " if st.session_state.user_name else ""
    
    # 2. Check if Gemini is available
    if gemini_model:
        # Build prompt based on available data
        context = ""
        
        # Add PDF content if available
        if st.session_state.pdf_text:
            # Take first 5000 chars of PDF for context
            context += f"DOCUMENT CONTENT (from {st.session_state.uploaded_file_name}):\n{st.session_state.pdf_text[:5000]}\n\n"
        
        # Add GNITS info
        context += f"GNITS COLLEGE INFORMATION:\n{GNITS_INFO}\n\n"
        
        prompt = f"""You are Campus Bot, a friendly and helpful assistant.

{context}

USER QUESTION: {question}

INSTRUCTIONS:
- Answer based on the document content if the question is about the uploaded PDF
- Answer based on GNITS info if the question is about the college
- For casual questions like "How are you?", respond naturally
- Be friendly, use emojis, and be conversational
- If you can't find the answer in the context, say "I couldn't find that information"

ANSWER:"""
        
        try:
            response = gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return fallback_response(question, name_prefix)
    
    # 3. Fallback without Gemini
    return fallback_response(question, name_prefix)

def fallback_response(question, name_prefix):
    """Fallback responses when Gemini is not available"""
    q = question.lower().strip()
    
    # Greetings
    if re.search(r'^(hi|hello|hey|namaste)', q):
        return f"{name_prefix}Hello! 👋 Welcome to Campus Bot! How can I help you today?"
    
    if re.search(r'how are you', q):
        return f"{name_prefix}I'm doing great! 😊 Thanks for asking!"
    
    if re.search(r'thank|thanks', q):
        return f"{name_prefix}You're very welcome! 😊"
    
    if re.search(r'tell me a joke', q):
        return f"{name_prefix}Why did the student eat their homework? Because the teacher said it was a piece of cake! 😄"
    
    # GNITS Questions
    if re.search(r'fee|fees|cost|tuition', q):
        return f"{name_prefix}💰 **Fee Structure:**\n\nB.Tech: ₹1,62,000 per year\nM.Tech: ₹1,12,000 per year"
    
    if re.search(r'admission|apply|eligibility', q):
        return f"{name_prefix}📝 **Admissions:**\n\nUG: TG-EAPCET exam required\nPG: Based on GATE score\nContact: 040-29565856"
    
    if re.search(r'placement|package|lpa', q):
        return f"{name_prefix}🏆 **Placements:**\n\nHighest Package: 50 LPA (Microsoft)\nTop Recruiters: Microsoft, ServiceNow, Deloitte"
    
    if re.search(r'library|hostel|canteen|sports|facility', q):
        return f"{name_prefix}📚 **Facilities:**\n\nLibrary: 8 AM - 8 PM\nHostel: Girls hostel with security\nSports and Canteen available"
    
    if re.search(r'contact|phone|number', q):
        return f"{name_prefix}📞 **Contacts:**\n\nAdmissions: 040-29565856\nPrincipal: 040-29565850\nPlacements: 040-29565860"
    
    # PDF Questions
    if st.session_state.pdf_text:
        # Simple PDF search
        pdf_lower = st.session_state.pdf_text.lower()
        words = q.split()
        for word in words:
            if len(word) > 3 and word in pdf_lower:
                # Find relevant line
                lines = st.session_state.pdf_text.split('\n')
                for line in lines:
                    if word in line.lower() and len(line) > 30:
                        return f"📄 **From your PDF ({st.session_state.uploaded_file_name}):**\n\n{line[:500]}"
    
    # Default
    if st.session_state.pdf_text:
        return f"""{name_prefix}📄 **I see you uploaded a PDF!**

Ask me questions like:
- "What is this document about?"
- "Summarize the key points"
- "Tell me about [specific topic]"

Or ask about GNITS college! 🎓"""
    else:
        return f"""{name_prefix}😊 **Welcome to Campus Bot!**

You can:
📄 **Upload a PDF** - Ask questions about its content
🏫 **Ask about GNITS** - Admissions, fees, placements, facilities
💬 **Chat casually** - "How are you?", "Tell me a joke"

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
    <p>Upload PDFs | Ask Questions | Get Answers</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# Sidebar
# ============================================
with st.sidebar:
    st.markdown("### 📄 Upload PDF")
    
    uploaded_file = st.file_uploader("Choose PDF file", type=['pdf'])
    
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name} selected")
        if st.button("🚀 Process PDF", use_container_width=True):
            with st.spinner("Processing PDF..."):
                st.session_state.pdf_text = extract_pdf_text(uploaded_file)
                st.session_state.uploaded_file = uploaded_file
                st.session_state.uploaded_file_name = uploaded_file.name
                st.success("✅ Ready!")
                st.rerun()
    
    if st.session_state.uploaded_file:
        st.info(f"📄 Active: {st.session_state.uploaded_file_name}")
    
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
        st.success(f"✅ Gemini Active")
    else:
        st.warning("⚠️ Gemini not available")
    
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

question = st.chat_input("Ask about your PDF, GNITS college, or just chat...")

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
        st.info(f"📄 **Ready!** Ask me anything about {st.session_state.uploaded_file_name}")
    else:
        st.info("👋 **Hello!** Upload a PDF, ask about GNITS college, or just chat with me!")
