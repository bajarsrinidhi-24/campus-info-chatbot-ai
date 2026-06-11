import streamlit as st
from PyPDF2 import PdfReader
from groq import Groq
import json
import os
from datetime import datetime

# ============================================
# Page Configuration
# ============================================
st.set_page_config(page_title="Campus Chatbot", page_icon="🎓", layout="wide")

# ============================================
# Initialize Groq Client
# ============================================
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=GROQ_API_KEY)
    groq_available = True
except:
    groq_available = False

# ============================================
# File for saving chat history
# ============================================
CHAT_HISTORY_FILE = "chat_history.json"

def load_chat_history():
    """Load all saved chats from file"""
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_chat_history(chat_history):
    """Save all chats to file"""
    with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(chat_history, f, indent=2, ensure_ascii=False)

def save_current_chat(chat_id, chat_name, messages, pdf_info):
    """Save current chat to history"""
    chat_history = load_chat_history()
    chat_history[chat_id] = {
        "name": chat_name,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "messages": messages,
        "pdf_info": pdf_info
    }
    save_chat_history(chat_history)

def delete_chat(chat_id):
    """Delete a specific chat"""
    chat_history = load_chat_history()
    if chat_id in chat_history:
        del chat_history[chat_id]
        save_chat_history(chat_history)

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
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "current_chat_name" not in st.session_state:
    st.session_state.current_chat_name = "New Chat"

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
"""

# ============================================
# Get AI Response
# ============================================
def get_response(question):
    context = ""
    
    if st.session_state.pdf_text:
        context += f"""
DOCUMENT CONTENT (from {st.session_state.uploaded_file_name}):
{st.session_state.pdf_text[:6000]}

"""
    
    context += f"""
GNITS COLLEGE INFORMATION:
{GNITS_INFO}

"""
    
    if st.session_state.user_name:
        context += f"The user's name is {st.session_state.user_name}. Address them by name.\n"
    
    prompt = f"""{context}

USER QUESTION: {question}

INSTRUCTIONS:
- Answer based on the context (PDF or GNITS info)
- Be friendly, use emojis
- For casual chat like "How are you?", respond naturally
- Keep answers helpful and concise

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
        return f"Error: {str(e)}"

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
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .chat-item {
        padding: 10px;
        margin: 5px 0;
        border-radius: 10px;
        cursor: pointer;
        background: #f8f9fa;
        transition: all 0.3s ease;
    }
    .chat-item:hover {
        background: #e9ecef;
        transform: translateX(5px);
    }
    .chat-date {
        font-size: 10px;
        color: #6c757d;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# Header
# ============================================
st.markdown("""
<div class="main-header">
    <h1>🎓 Campus Chatbot</h1>
    <p>Powered by Groq AI | Save Chats | New Conversations</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# Sidebar - Chat History
# ============================================
with st.sidebar:
    st.markdown("### 💬 Conversations")
    
    # New Chat Button
    if st.button("➕ New Chat", use_container_width=True):
        # Save current chat if it has messages
        if st.session_state.messages:
            chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            chat_name = f"Chat {datetime.now().strftime('%b %d, %H:%M')}"
            save_current_chat(
                chat_id, 
                chat_name, 
                st.session_state.messages,
                {"name": st.session_state.uploaded_file_name, "text": st.session_state.pdf_text[:500] if st.session_state.pdf_text else ""}
            )
        # Reset session
        st.session_state.messages = []
        st.session_state.pdf_text = ""
        st.session_state.uploaded_file = None
        st.session_state.uploaded_file_name = ""
        st.session_state.current_chat_id = None
        st.rerun()
    
    st.markdown("---")
    
    # Load and display chat history
    chat_history = load_chat_history()
    
    if chat_history:
        st.markdown("### 📜 Saved Chats")
        for chat_id, chat_data in sorted(chat_history.items(), reverse=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(f"💬 {chat_data['name']}", key=f"chat_{chat_id}", use_container_width=True):
                    # Load selected chat
                    st.session_state.messages = chat_data["messages"]
                    st.session_state.current_chat_id = chat_id
                    st.session_state.current_chat_name = chat_data["name"]
                    if chat_data.get("pdf_info", {}).get("name"):
                        st.session_state.uploaded_file_name = chat_data["pdf_info"]["name"]
                    st.rerun()
                st.caption(f"🕐 {chat_data['created_at']}")
            with col2:
                if st.button("🗑️", key=f"del_{chat_id}"):
                    delete_chat(chat_id)
                    st.rerun()
    else:
        st.info("No saved chats yet. Start a conversation!")
    
    st.markdown("---")
    
    # PDF Upload Section
    st.markdown("### 📄 Upload PDF")
    uploaded_file = st.file_uploader("Choose PDF file", type=['pdf'], key="pdf_uploader")
    
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name} selected")
        if st.button("🚀 Process PDF", use_container_width=True):
            with st.spinner("Processing PDF..."):
                st.session_state.pdf_text = extract_pdf_text(uploaded_file)
                st.session_state.uploaded_file = uploaded_file
                st.session_state.uploaded_file_name = uploaded_file.name
                st.success("✅ PDF Ready!")
                st.rerun()
    
    if st.session_state.uploaded_file_name:
        st.info(f"📄 Active: {st.session_state.uploaded_file_name}")
    
    st.markdown("---")
    
    # Profile Section
    st.markdown("### 👤 Profile")
    if st.session_state.user_name:
        st.success(f"Name: {st.session_state.user_name}")
        if st.button("Reset Name", use_container_width=True):
            st.session_state.user_name = None
            st.rerun()
    else:
        st.info("Say 'Call me [name]'")
    
    st.markdown("---")
    
    # AI Status
    if groq_available:
        st.success("✅ Groq AI Active")
    else:
        st.error("❌ Groq AI Not Available")
    
    st.markdown("---")
    
    # Clear Current Chat Button
    if st.button("🗑️ Clear Current Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ============================================
# Main Chat Interface
# ============================================
# Show current chat name
if st.session_state.messages:
    st.caption(f"💬 Current: {st.session_state.current_chat_name if st.session_state.current_chat_name else 'New Chat'}")

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
    
    # Auto-save current chat after each message
    if st.session_state.messages:
        chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        chat_name = f"Chat {datetime.now().strftime('%b %d, %H:%M')}"
        save_current_chat(
            chat_id, 
            chat_name, 
            st.session_state.messages,
            {"name": st.session_state.uploaded_file_name, "text": st.session_state.pdf_text[:500] if st.session_state.pdf_text else ""}
        )
        st.session_state.current_chat_id = chat_id
        st.session_state.current_chat_name = chat_name
    st.rerun()

# Welcome message
if not st.session_state.messages:
    st.info("👋 **Hello!** I'm Campus Bot powered by Groq AI. I can answer ANY question about GNITS college, or you can upload a PDF and ask questions about its content. Your chats are automatically saved! 😊")
