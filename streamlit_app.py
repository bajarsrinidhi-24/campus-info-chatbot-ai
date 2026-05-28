import streamlit as st
import google.generativeai as genai

# Page config
st.set_page_config(
    page_title="CampusBot - GNITS Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for dark mode
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

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
                border: 1px solid rgba(255,255,255,0.2);
            }
            .main-header h1 {
                font-size: 2.5rem;
                background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .main-header p {
                color: #ccc;
            }
            .stButton > button {
                background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
                color: white;
                border: none;
                border-radius: 25px;
                padding: 10px 20px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,210,255,0.3);
            }
            .user-message {
                background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
                color: white;
                padding: 15px 20px;
                border-radius: 20px;
                margin: 10px 0;
                border-radius: 20px 20px 5px 20px;
            }
            .bot-message {
                background: rgba(255,255,255,0.1);
                color: #fff;
                padding: 15px 20px;
                border-radius: 20px;
                margin: 10px 0;
                border-radius: 20px 20px 20px 5px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.1);
            }
            .info-box {
                background: rgba(255,255,255,0.1);
                padding: 20px;
                border-radius: 15px;
                margin: 10px 0;
                backdrop-filter: blur(10px);
            }
            .stTextInput > div > div > input {
                background: rgba(255,255,255,0.1);
                color: white;
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 25px;
                padding: 12px 20px;
            }
            .stTextInput > div > div > input:focus {
                border-color: #00d2ff;
            }
            .stSelectbox > div > div {
                background: rgba(255,255,255,0.1);
                color: white;
            }
            .sidebar .sidebar-content {
                background: rgba(0,0,0,0.3);
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
            .main-header p {
                color: #666;
            }
            .stButton > button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 25px;
                padding: 10px 20px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .user-message {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 20px;
                border-radius: 20px;
                margin: 10px 0;
                border-radius: 20px 20px 5px 20px;
            }
            .bot-message {
                background: white;
                color: #2c3e50;
                padding: 15px 20px;
                border-radius: 20px;
                margin: 10px 0;
                border-radius: 20px 20px 20px 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .info-box {
                background: rgba(255,255,255,0.95);
                padding: 20px;
                border-radius: 15px;
                margin: 10px 0;
            }
            .stTextInput > div > div > input {
                background: white;
                border: 2px solid #e0e0e0;
                border-radius: 25px;
                padding: 12px 20px;
            }
            .stTextInput > div > div > input:focus {
                border-color: #667eea;
            }
        </style>
        """, unsafe_allow_html=True)

apply_theme()

# Header
st.markdown("""
<div class="main-header">
    <h1>🎓 CampusBot - GNITS Assistant</h1>
    <p>Your 24/7 AI-powered campus assistant</p>
    <p style="font-size: 0.85rem;">Powered by Google Gemini</p>
</div>
""", unsafe_allow_html=True)

# College Information Database
COLLEGE_DATA = """
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
- Canteen: Vegetarian and non-vegetarian options

🎉 CLUBS & EVENTS:
- Coding Club (CodeChef, LeetCode competitions)
- Robotics Club
- Entrepreneurship Development Cell (EDC)
- Cultural Committee (Splash annual fest)
- Technical Club (GNITS ACM Student Chapter)
- IEEE ICoECIT-2026 (AI & Quantum Computing) - March 2026
- Hackathon - February 2026
- Alumni Meet (TU TURNO-26) - December 2026

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
- Courses: B.Tech (CSE, IT, ECE, EEE, Data Science, AI & ML), M.Tech
"""

# Initialize Gemini with correct model name
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')  # Fixed: dash instead of space

# Sidebar with theme toggle
with st.sidebar:
    st.markdown("### 🎨 Appearance")
    theme_toggle = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    if theme_toggle != st.session_state.dark_mode:
        st.session_state.dark_mode = theme_toggle
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🤖 About CampusBot")
    st.info("""
    **CampusBot** is your AI-powered assistant for GNITS college.
    
    Ask me anything about:
    - 📝 Admissions
    - 💰 Fee Structure  
    - 🏆 Placements
    - 📚 Facilities
    - 🎉 Events & Clubs
    - 📞 Contacts
    """)
    
    st.markdown("---")
    st.markdown("### 📌 Quick Info")
    st.markdown("""
    - 🏫 **GNITS Hyderabad**
    - 🎓 **Established:** 1997
    - 👩‍🎓 **Type:** Women's Engineering College
    - ⭐ **NAAC:** 'A' Grade
    """)
    
    st.markdown("---")
    st.markdown("### 🔗 Useful Links")
    st.markdown("[🌐 Official Website](https://gnits.ac.in)")

# Quick Questions Section
st.markdown("### 💡 Quick Questions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💰 Fee Structure", use_container_width=True):
        st.session_state.question = "What is the fee structure for B.Tech?"
with col2:
    if st.button("📝 Admissions", use_container_width=True):
        st.session_state.question = "How to get admission in GNITS?"
with col3:
    if st.button("🏆 Placements", use_container_width=True):
        st.session_state.question = "What is the placement package?"
with col4:
    if st.button("🎉 Events & Clubs", use_container_width=True):
        st.session_state.question = "What clubs and events are available?"

st.markdown("---")

# Chat Interface
st.markdown("### 💬 Ask Me Anything")

question = st.text_input(
    "Type your question here...",
    value=st.session_state.get("question", ""),
    placeholder="e.g., What is the hostel facility like? Tell me about placements",
    label_visibility="collapsed"
)

if question:
    # Show user message
    st.markdown(f"""
    <div class="user-message">
        <strong>You</strong><br>{question}
    </div>
    """, unsafe_allow_html=True)
    
    with st.spinner("🤔 CampusBot is thinking..."):
        try:
            prompt = f"""You are CampusBot, a friendly, professional campus assistant for GNITS college.
            
Answer based on this college information:
{COLLEGE_DATA}

User Question: {question}

Instructions:
- Be VERY helpful, warm and friendly
- Use emojis generously 😊🎓💡
- Keep responses clear and concise
- If the question is about something not in the data, politely say you don't have that info
- For greetings like "hi", "hello", respond warmly
- For thanks, respond with "You're welcome! 😊"
- Make the conversation feel natural and engaging

Answer:"""
            
            response = model.generate_content(prompt)
            
            st.markdown(f"""
            <div class="bot-message">
                <strong>🎓 CampusBot</strong><br>{response.text}
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Please make sure your Google API key is valid in Secrets.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.8rem;">
    <p>💡 CampusBot - Your 24/7 Campus Assistant | Powered by Google Gemini AI</p>
    <p>For urgent queries, contact GNITS directly: 📞 040-29565856</p>
</div>
""", unsafe_allow_html=True)
