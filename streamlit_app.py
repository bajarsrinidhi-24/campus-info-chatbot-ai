import streamlit as st
import re

# Page config
st.set_page_config(
    page_title="CampusBot - GNITS Assistant",
    page_icon="🎓",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# College Data
COLLEGE_INFO = {
    "admissions": """📝 **ADMISSIONS**

🎓 **UG Admissions (B.Tech):**
• TG-EAPCET exam required
• Eligibility: 10+2 with Physics, Chemistry, Mathematics
• Counseling based on rank

🎓 **PG Admissions (M.Tech):**
• Based on GATE score
• TS-PGECET for Non-GATE candidates

📞 Contact: 040-29565856""",

    "fees": """💰 **FEE STRUCTURE**

💵 **B.Tech:** ₹1,62,000 per year + JNTUH fees
💵 **M.Tech:** ₹1,12,000 per year
💵 **NRI Category:** USD 5,000 + JNTUH fees per year

*Additional fees may apply for hostel and other facilities*""",

    "placements": """🏆 **PLACEMENTS**

✨ **Highest Package:** 50 LPA (Microsoft)
✨ **Second Highest:** 42.6 LPA (ServiceNow)

🏢 **Top Recruiters:**
• Microsoft - 50 LPA
• ServiceNow - 42.6 LPA
• Deloitte
• Snowflake
• PwC

💪 GNITS has an excellent placement record!""",

    "facilities": """📚 **FACILITIES**

📖 **Library:** 8 AM to 8 PM (Monday-Saturday)
🏠 **Hostel:** Girls hostel with 24/7 security
🏃‍♀️ **Sports:** Indoor badminton, table tennis, volleyball, basketball
🍽️ **Canteen:** Vegetarian and non-vegetarian options
💻 **Labs:** State-of-the-art computer and engineering labs""",

    "clubs": """🎉 **CLUBS & EVENTS**

🎮 **Coding Club** - CodeChef, LeetCode competitions
🤖 **Robotics Club**
💡 **Entrepreneurship Development Cell (EDC)**
🎭 **Cultural Committee** - Organizes Splash annual fest
🔧 **Technical Club** - GNITS ACM Student Chapter

📅 **Upcoming Events:**
• IEEE ICoECIT-2026 (March 2026)
• Splash 2026 (October 2026)
• Hackathon (February 2026)
• Alumni Meet (December 2026)""",

    "contacts": """📞 **IMPORTANT CONTACTS**

👩‍💼 **Principal Office:** 040-29565850
📝 **Admissions:** 040-29565856
🏢 **Training & Placement Cell:** 040-29565860
📚 **Library:** 040-29565870

🕐 Office hours: 9:30 AM to 5:00 PM (Monday-Friday)""",

    "about": """🏫 **ABOUT GNITS**

G. Narayanamma Institute of Technology and Sciences (GNITS) is a prestigious women's engineering college in Hyderabad, established in 1997.

⭐ **Accreditations:** NBA, NAAC 'A' Grade

📚 **Courses Offered:**
• B.Tech: CSE, IT, ECE, EEE, Data Science, AI & ML
• M.Tech: Various specializations

📍 **Location:** Hyderabad, Telangana

🎯 **Vision:** Empowering women in engineering since 1997"""
}

def get_bot_response(user_input):
    text = user_input.lower().strip()
    
    # Greetings
    if re.search(r'^(hi|hello|hey|namaste|good morning|good afternoon|good evening|hola)', text):
        return "Hello! 👋 Welcome to CampusBot! 😊 How can I help you with GNITS today? You can ask me about admissions, fees, placements, facilities, clubs, or contacts!"
    
    # How are you
    if re.search(r'how are you', text):
        return "I'm doing great! 🎉 Thanks for asking! I'm here to help you with any questions about GNITS college. What would you like to know? 😊"
    
    # Thank you
    if re.search(r'thank|thanks|appreciate', text):
        return "You're very welcome! 😊 I'm happy to help! Is there anything else you'd like to know about GNITS? 🎓"
    
    # Goodbye
    if re.search(r'bye|goodbye|see you|cya|tata', text):
        return "Goodbye! 👋 Have a wonderful day! Feel free to come back if you have more questions about GNITS. 🎓"
    
    # Fee related
    if re.search(r'(fee|fees|cost|price|tuition|fees structure|fees for btech)', text):
        return COLLEGE_INFO["fees"]
    
    # Admission related
    if re.search(r'(admission|apply|eligibility|how to get|join|counseling|how to take admission|admission process)', text):
        return COLLEGE_INFO["admissions"]
    
    # Placement related
    if re.search(r'(placement|package|recruiter|company|job|salary|lpa|hiring|offer|placements record|highest package)', text):
        return COLLEGE_INFO["placements"]
    
    # Facility related
    if re.search(r'(library|hostel|canteen|sports|lab|facility|gym|playground|mess|food)', text):
        return COLLEGE_INFO["facilities"]
    
    # Club/Event related
    if re.search(r'(club|event|fest|hackathon|splash|competition|cultural|technical|activities|workshop|seminar)', text):
        return COLLEGE_INFO["clubs"]
    
    # Contact related
    if re.search(r'(contact|phone|number|email|call|reach|mobile|telephone)', text):
        return COLLEGE_INFO["contacts"]
    
    # About college
    if re.search(r'(about|what is|tell me about|information|overview|introduction|details about college)', text):
        return COLLEGE_INFO["about"]
    
    # Default response
    return """😊 **I'm here to help!**

You can ask me about:

📝 **Admissions** - How to apply, eligibility, entrance exams
💰 **Fees** - B.Tech and M.Tech fee structure
🏆 **Placements** - Packages, top recruiters
📚 **Facilities** - Library, Hostel, Sports, Canteen
🎉 **Clubs & Events** - Activities, fests, competitions
📞 **Contacts** - Important phone numbers

Just type your question! For example: "What is the fee for B.Tech?" or "How to get admission?" 🎓"""

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    .main-header {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #e94560 0%, #533483 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .main-header h1 {
        font-size: 2.5rem;
        color: white;
        margin: 0;
    }
    .main-header p {
        color: rgba(255,255,255,0.9);
        margin-top: 8px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #e94560 0%, #533483 100%);
        color: white;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(233,69,96,0.4);
    }
    .user-message {
        background: linear-gradient(135deg, #e94560 0%, #533483 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 20px;
        margin: 10px 0;
        border-radius: 20px 20px 5px 20px;
        max-width: 75%;
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
        max-width: 75%;
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
    .stTextInput > div > div > input:focus {
        border-color: #e94560;
        box-shadow: none;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎓 CampusBot</h1>
    <p>Your friendly 24/7 AI assistant for GNITS college</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 About CampusBot")
    st.markdown("""
    Hey there! 👋 I'm CampusBot.
    
    I can help you with:
    - 📝 **Admissions**
    - 💰 **Fees**  
    - 🏆 **Placements**
    - 📚 **Facilities**
    - 🎉 **Clubs & Events**
    - 📞 **Contacts**
    """)
    
    st.markdown("---")
    st.markdown("### 📌 Quick Info")
    st.markdown("""
    - 🏫 **GNITS Hyderabad**
    - 🎓 **Est:** 1997
    - 👩‍🎓 **Women's College**
    - ⭐ **NAAC 'A' Grade**
    """)
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

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
        st.session_state.messages.append({"role": "user", "content": "Tell me about placements"})
        st.rerun()
with col4:
    if st.button("📞 Contacts", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Give me contact numbers"})
        st.rerun()

st.markdown("---")

# Chat display
st.markdown("### 💬 Chat with CampusBot")

# Display messages
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

# Chat input
question = st.text_input("", placeholder="Type your message here...", key="input", label_visibility="collapsed")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    response = get_bot_response(question)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Welcome message
if not st.session_state.messages:
    st.info("👋 **Hello!** I'm CampusBot. Ask me about admissions, fees, placements, or just say hi! 😊")
