import streamlit as st
from chatbot import GNITSChatbot
import time

# Page config
st.set_page_config(
    page_title="GNITS Campus Assistant",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
    }
    .bot-message {
        background-color: #f5f5f5;
        border-left: 5px solid #4caf50;
    }
    .source-info {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize chatbot
@st.cache_resource
def init_chatbot():
    return GNITSChatbot()

# Header
st.markdown("""
<div class="main-header">
    <h1>🎓 GNITS Campus Assistant</h1>
    <p>Your AI guide for G. Narayanamma Institute of Technology and Sciences</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with info
with st.sidebar:
    st.image("https://gnits.ac.in/assets/images/logo.png", use_container_width=True)
    st.markdown("## ℹ️ About")
    st.markdown("""
    This chatbot can answer questions about:
    - 📚 **Academics & Rules** (attendance, exams, grading)
    - 🏆 **Placements** (packages, companies, statistics)
    - 🎉 **Events & Clubs** (festivals, hackathons, committees)
    - 📞 **Contacts** (faculty, departments, offices)
    - 🏫 **Facilities** (library, hostel, canteen, sports)
    - 📜 **Policies** (code of conduct, anti-ragging)
    
    **Data Sources:**
    - GNITS Official Website
    - Student Handbook
    - College Documents
    """)
    
    st.markdown("---")
    st.markdown("### 🔧 Tech Stack")
    st.code("""
    - LangChain (RAG)
    - FAISS (Vector DB)
    - Gemini AI (LLM)
    - BeautifulSoup
    - Streamlit
    """, language="text")

# Initialize chatbot
try:
    chatbot = init_chatbot()
    st.success("✅ Chatbot is ready! Ask me anything about GNITS.")
except Exception as e:
    st.error(f"⚠️ Error loading chatbot: {e}")
    st.info("Please run scrape_gnits.py and build_vectorstore.py first.")
    st.stop()

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your GNITS Campus Assistant. Ask me anything about admissions, placements, events, facilities, or college policies! 🎓"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            st.caption(f"📚 Sources: {', '.join(set(message['sources']))}")

# Chat input
if prompt := st.chat_input("Ask me about GNITS..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer, sources = chatbot.ask(prompt)
                st.markdown(answer)
                if sources:
                    st.caption(f"📚 Sources: {', '.join(set(sources))}")
                
                # Save to session
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer,
                    "sources": sources
                })
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Clear chat button
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Chat cleared! How can I help you today? 🎓"}
    ]
    st.rerun()
