import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Campus Chatbot", page_icon="🎓", layout="wide")

# Get API key from Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Custom CSS
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

st.markdown("""
<div class="main-header">
    <h1>🎓 Campus Chatbot</h1>
    <p>Ask me anything about GNITS college!</p>
</div>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 About")
    st.info("""
    I can help you with:
    - 📚 IT Syllabus (I to IV Year)
    - 📊 Attendance Rules (75% required)
    - 🎯 Grading System (O to F)
    - 💰 Fee Structure (B.Tech: ₹1.62L)
    - 🏆 Placements (50 LPA highest)
    - 📝 Exam Pattern (CIE + SEE)
    - 🎓 Professional Electives
    """)
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Quick questions
st.markdown("### 💡 Quick Questions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📚 I Year Syllabus", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "What are I year IT subjects?"})
        st.rerun()
with col2:
    if st.button("📊 Attendance", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "What is the attendance requirement?"})
        st.rerun()
with col3:
    if st.button("💰 Fee Structure", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "What is the fee for B.Tech?"})
        st.rerun()
with col4:
    if st.button("🏆 Placements", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "What is the placement record?"})
        st.rerun()

st.markdown("---")

# Chat display
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

# Chat input
question = st.chat_input("Ask me anything about GNITS...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    
    with st.chat_message("user"):
        st.markdown(question)
    
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                # Updated OpenAI v1.0+ syntax
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": """You are Campus Bot, a helpful assistant for GNITS college. 
                        Answer questions about:
                        - IT Syllabus (I, II, III, IV years)
                        - Attendance: 75% minimum, condonation up to 65%
                        - Grading: O(10), A+(9), A(8), B+(7), B(6), C(5), F(0)
                        - SGPA/CGPA calculation
                        - Exam pattern: CIE 40% + SEE 60%
                        - Fee: B.Tech ₹1,62,000/year, M.Tech ₹1,12,000/year
                        - Placements: Highest 50 LPA (Microsoft), ServiceNow 42.6 LPA
                        - Facilities: Library 8AM-8PM, Hostel, Sports
                        - Professional Electives (PE1 to PE6)
                        
                        Be friendly, helpful, and use emojis. If unsure, say so politely."""},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Please check your OpenAI API key in Secrets.")

if not st.session_state.messages:
    st.info("👋 **Hello!** I'm Campus Chatbot. Ask me about IT syllabus, attendance, fees, placements, exams, or anything about GNITS! 😊")
