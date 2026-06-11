import streamlit as st
from PyPDF2 import PdfReader
from groq import Groq

# ============================================
# Page Configuration
# ============================================
st.set_page_config(page_title="Campus Chatbot", page_icon="🎓", layout="wide")

# ============================================
# Initialize Groq Client
# ============================================
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "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")
client = Groq(api_key=GROQ_API_KEY)

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

# ============================================
# GNITS Information Database
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
# Main Response Function - Groq AI Only
# ============================================
def get_response(question):
    # Build context based on available data
    context = ""
    
    # Add PDF content if uploaded
    if st.session_state.pdf_text:
        context += f"""
DOCUMENT CONTENT (from {st.session_state.uploaded_file_name}):
{st.session_state.pdf_text[:8000]}

"""
    
    # Always add GNITS info
    context += f"""
GNITS COLLEGE INFORMATION:
{GNITS_INFO}

"""
    
    # Add user's name if set
    name_context = ""
    if st.session_state.user_name:
        name_context = f"The user's name is {st.session_state.user_name}. Address them by their name in your response.\n"
    
    # Create the prompt for Groq
    prompt = f"""{name_context}You are Campus Bot, a friendly, helpful AI assistant for GNITS college.

{context}

USER QUESTION: {question}

INSTRUCTIONS:
1. Answer based on the provided context (PDF document or GNITS information)
2. If the user asks about something not in the context, use your general knowledge
3. Be conversational, friendly, and use emojis occasionally 😊
4. If the user sets a name, use it naturally in conversation
5. Handle casual chat like "How are you?", "Tell me a joke" naturally
6. For PDF questions, answer based on the document content
7. For GNITS questions, answer based on the college information above
8. Keep answers clear and helpful

ANSWER:"""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

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
    .main-header p { color: rgba(255,255,255,0.9); }
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
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        border: none;
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
    <p>Powered by Groq AI | Upload PDF | Ask Anything</p>
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
                st.success("✅ PDF Ready!")
                st.rerun()
    
    if st.session_state.uploaded_file:
        st.info(f"📄 Active PDF: {st.session_state.uploaded_file_name}")
    
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
    st.success("✅ Groq AI Active")
    st.caption("Model: Llama 3.3 70B")
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ============================================
# Main Chat Interface
# ============================================
st.markdown("### 💬 Chat")

# Display chat history
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
question = st.chat_input("Ask me anything about GNITS college or your uploaded PDF...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    
    with st.chat_message("user"):
        st.markdown(question)
    
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            response = get_response(question)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Welcome message
if not st.session_state.messages:
    if st.session_state.uploaded_file:
        st.info(f"📄 **PDF Loaded: {st.session_state.uploaded_file_name}**\n\nAsk me anything about this document! I can summarize, answer questions, or extract information. Also feel free to ask about GNITS college! 🎓")
    else:
        st.info("👋 **Hello!** I'm Campus Bot powered by Groq AI. I can answer ANY question about GNITS college, or you can upload a PDF and ask questions about its content. Just type your question below! 😊")
