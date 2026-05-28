import streamlit as st
import google.generativeai as genai

# Page config
st.set_page_config(
    page_title="CampusBot - GNITS Assistant",
    page_icon="🎓",
    layout="wide"
)

# Initialize session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'messages' not in st.session_state:
    st.session_state.messages = []

# College Data
COLLEGE_DATA = """
GNITS (G. Narayanamma Institute of Technology and Sciences), Hyderabad

ADMISSIONS:
- UG: TG-EAPCET required. 10+2 with Physics, Chemistry, Mathematics
- PG: Based on GATE score or TS-PGECET
- Contact Admissions: 040-29565856

FEE STRUCTURE:
- B.Tech: ₹1,62,000 per year + JNTUH fees
- M.Tech: ₹1,12,000 per year

PLACEMENTS:
- Highest Package: 50 LPA (Microsoft)
- Top Recruiters: Microsoft, ServiceNow (42.6 LPA), Deloitte, Snowflake

FACILITIES:
- Library: 8 AM to 8 PM (Monday-Saturday)
- Hostel: Girls hostel with 24/7 security
- Sports: Indoor games, volleyball, basketball
- Canteen available

CLUBS:
- Coding Club, Robotics Club, Entrepreneurship Cell
- Cultural Committee, Technical Club (ACM)

CONTACTS:
- Principal: 040-29565850
- Admissions: 040-29565856
- Placements: 040-29565860
"""

# Initialize Gemini - CORRECT MODEL NAME
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# List available models to find the correct one
try:
    # Try different model names
    model_names = [
        'models/gemini-1.5-flash',
        'gemini-1.5-flash',
        'models/gemini-pro',
        'gemini-pro'
    ]
    
    model = None
    for model_name in model_names:
        try:
            model = genai.GenerativeModel(model_name)
            # Test the model
            test_response = model.generate_content("test")
            print(f"✅ Using model: {model_name}")
            break
        except:
            continue
    
    if model is None:
        st.error("No working model found. Please check your API key.")
        st.stop()
        
except Exception as e:
    st.error(f"Error initializing Gemini: {e}")
    st.info("Please make sure your Google API key is valid.")
    st.stop()

# Custom CSS with better colors
def apply_theme():
    if st.session_state.dark_mode:
        st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            }
            .main-header {
                text-align: center;
                padding: 2rem;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 20px;
                margin-bottom: 2rem;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }
            .main-header h1 {
                font-size: 2.5rem;
                color: white;
            }
            .main-header p {
                color: rgba(255,255,255,0.9);
            }
            .stButton > button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 25px;
                padding: 10px 20px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102,126,234,0.4);
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
                clear: both;
            }
            .bot-message {
                background: rgba(255,255,255,0.1);
                color: white;
                padding: 12px 18px;
                border-radius: 20px;
                margin: 10px 0;
                border-radius: 20px 20px 20px 5px;
                max-width: 70%;
                float: left;
                clear: both;
                backdrop-filter: blur(10px);
            }
            .stTextInput > div > div > input {
                background: rgba(255,255,255,0.1);
                color: white;
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 25px;
                padding: 12px 20px;
            }
            .stTextInput > div > div > input::placeholder {
                color: rgba(255,255,255,0.6);
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
                background: white;
                color: #667eea;
                border-radius: 25px;
                padding: 10px 20px;
                font-weight: 600;
                border: none;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .user-message {
                background: white;
                color: #667eea;
                padding: 12px 18px;
                border-radius: 20px;
                margin: 10px 0;
                border-radius: 20px 20px 5px 20px;
                max-width: 70%;
                float: right;
                clear: both;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .bot-message {
                background: rgba(255,255,255,0.95);
                color: #2c3e50;
                padding: 12px 18px;
                border-radius: 20px;
                margin: 10px 0;
                border-radius: 20px 20px 20px 5px;
                max-width: 70%;
                float: left;
                clear: both;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .stTextInput > div > div > input {
                background: white;
                border: 2px solid #e0e0e0;
                border-radius: 25px;
                padding: 12px 20px;
            }
        </style>
        """, unsafe_allow_html=True)

apply_theme()

# Header
st.markdown("""
<div class="main-header">
    <h1>🎓 CampusBot</h1>
    <p>Your friendly AI assistant for GNITS college</p>
    <p style="font-size: 0.85rem;">💬 Ask me anything - I'm here to help!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    theme_toggle = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    if theme_toggle != st.session_state.dark_mode:
        st.session_state.dark_mode = theme_toggle
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🎤 About Me")
    st.markdown("""
    Hey there! 👋 I'm CampusBot.
    
    I can help you with:
    - 📝 Admissions
    - 💰 Fees  
    - 🏆 Placements
    - 📚 Facilities
    - 🎉 Events
    - 📞 Contacts
    """)
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 💡 Quick Links")
    st.markdown("[🌐 GNITS Website](https://gnits.ac.in)")

# Quick questions
st.markdown("### 💡 Quick Questions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💰 Fee Structure", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "What is the fee structure?"})
        st.rerun()
with col2:
    if st.button("📝 Admissions", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "How to get admission in GNITS?"})
        st.rerun()
with col3:
    if st.button("🏆 Placements", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "What is the placement record?"})
        st.rerun()
with col4:
    if st.button("📞 Contacts", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Give me important contact numbers"})
        st.rerun()

st.markdown("---")

# Chat display
st.markdown("### 💬 Chat with CampusBot")

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
            # Get recent conversation for context
            recent = st.session_state.messages[-5:] if len(st.session_state.messages) > 5 else st.session_state.messages
            context = "\n".join([f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}" for m in recent])
            
            prompt = f"""You are CampusBot, a friendly assistant for GNITS college.

College Info: {COLLEGE_DATA}

Conversation:
{context}

Current message: {question}

Rules:
1. Greet warmly when someone says hi/hello
2. Be conversational and use emojis
3. Answer based on college info above
4. If info not available, say "I don't have that info. Please call GNITS at 040-29565856"

Response:"""
            
            response = model.generate_content(prompt)
            answer = response.text
            
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Please check your API key in Secrets.")

# Welcome message
if not st.session_state.messages:
    st.info("👋 **Hello!** I'm CampusBot. Ask me about admissions, fees, placements, or just say hi! 😊")
