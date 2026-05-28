import streamlit as st
import google.generativeai as genai

# Page config
st.set_page_config(
    page_title="CampusBot - GNITS Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Custom CSS based on mode
def apply_theme():
    if st.session_state.dark_mode:
        st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            }
            .main-header {
                text-align: center;
                padding: 2rem;
                background: rgba(255,255,255,0.1);
                border-radius: 20px;
                margin-bottom: 2rem;
                backdrop-filter: blur(10px);
            }
            .main-header h1 {
                font-size: 2.5rem;
                background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .stButton > button {
                background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
                color: white;
                border-radius: 25px;
                padding: 10px 20px;
                font-weight: 600;
            }
            .user-message {
                background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
                color: white;
                padding: 12px 18px;
                border-radius: 20px;
                margin: 10px 0;
                border-radius: 20px 20px 5px 20px;
                max-width: 70%;
                float: right;
            }
            .bot-message {
                background: rgba(255,255,255,0.1);
                color: #fff;
                padding: 12px 18px;
                border-radius: 20px;
                margin: 10px 0;
                border-radius: 20px 20px 20px 5px;
                max-width: 70%;
                float: left;
            }
            .chat-container {
                max-height: 500px;
                overflow-y: auto;
                padding: 20px;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .main-header {
                text-align: center;
                padding: 2rem;
                background: rgba(255,255,255,0.95);
                border-radius: 20px;
                margin-bottom: 2rem;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .main-header h1 {
                font-size: 2.5rem;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .stButton > button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 25px;
                padding: 10px 20px;
                font-weight: 600;
            }
            .user-message {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 18px;
                border-radius: 20px;
                margin: 10px 0;
                border-radius: 20px 20px 5px 20px;
                max-width: 70%;
                float: right;
            }
            .bot-message {
                background: white;
                color: #2c3e50;
                padding: 12px 18px;
                border-radius: 20px;
                margin: 10px 0;
                border-radius: 20px 20px 20px 5px;
                max-width: 70%;
                float: left;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .chat-container {
                max-height: 500px;
                overflow-y: auto;
                padding: 20px;
            }
        </style>
        """, unsafe_allow_html=True)

apply_theme()

# Header
st.markdown("""
<div class="main-header">
    <h1>🎓 CampusBot</h1>
    <p>Your friendly campus assistant for GNITS</p>
    <p style="font-size: 0.85rem;">💬 Chat with me like you're talking to a friend!</p>
</div>
""", unsafe_allow_html=True)

# College Data
COLLEGE_DATA = """
GNITS (G. Narayanamma Institute of Technology and Sciences), Hyderabad

ADMISSIONS:
- UG: TG-EAPCET required. 10+2 with PCM
- PG: GATE or TS-PGECET
- Contact: 040-29565856

FEES:
- B.Tech: ₹1,62,000/year
- M.Tech: ₹1,12,000/year

PLACEMENTS:
- Highest: 50 LPA (Microsoft)
- Top: Microsoft, ServiceNow, Deloitte

FACILITIES:
- Library: 8 AM - 8 PM
- Hostel, Sports, Canteen

CONTACTS:
- Principal: 040-29565850
- Admissions: 040-29565856
- Placements: 040-29565860
"""

# Initialize Gemini
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Sidebar
with st.sidebar:
    theme_toggle = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    if theme_toggle != st.session_state.dark_mode:
        st.session_state.dark_mode = theme_toggle
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🎤 About Me")
    st.info("""
    Hey there! 👋 I'm CampusBot - your friendly AI assistant for GNITS college.
    
    I can help you with:
    - 📝 Admissions
    - 💰 Fees  
    - 🏆 Placements
    - 📚 Facilities
    - 🎉 Events
    - 📞 Contacts
    
    Just ask me anything! 😊
    """)
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Quick questions
st.markdown("### 💡 Quick Questions")
cols = st.columns(4)
qs = ["💰 Fee Structure", "📝 Admissions", "🏆 Placements", "📞 Contacts"]
for i, q in enumerate(qs):
    if cols[i].button(q, use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": f"Tell me about {q}"})

# Chat display
st.markdown("### 💬 Chat with CampusBot")
chat_container = st.container()

with chat_container:
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
                    <strong>🎓 CampusBot</strong><br>{msg["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

# Input
question = st.text_input("", placeholder="Type your message here...", key="input", label_visibility="collapsed")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    
    with st.spinner("🤔 Thinking..."):
        try:
            # Create conversation history
            conversation = "\n".join([f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}" for m in st.session_state.messages[-5:]])
            
            prompt = f"""You are CampusBot, a friendly, warm, and helpful assistant for GNITS college.

College info: {COLLEGE_DATA}

Previous conversation:
{conversation}

Current message: {question}

IMPORTANT RULES:
1. Be NATURAL and CONVERSATIONAL - like you're chatting with a friend
2. For greetings like "hi", "hello", "hey" - respond warmly like "Hello! 😊 How can I help you today? What would you like to know about GNITS?"
3. For "how are you" - respond like "I'm doing great, thanks for asking! 😊 Ready to help you with GNITS queries!"
4. For "thank you", "thanks" - respond like "You're very welcome! 😊 Anything else I can help you with?"
5. Use EMOJIS naturally (😊, 🎓, 💡, 👍, ❤️)
6. Keep responses friendly and engaging
7. Answer based on the college info provided

Your response should sound like a real person, not a robot! 😊

Response:"""
            
            response = model.generate_content(prompt)
            answer = response.text
            
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {e}")

# Welcome message
if not st.session_state.messages:
    st.info("👋 **Hello!** I'm CampusBot. Ask me anything about GNITS college - admissions, fees, placements, or just say hi! 😊")
