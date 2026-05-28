import streamlit as st
import re
import random
from datetime import datetime

st.set_page_config(page_title="GNITS Campus Assistant", page_icon="🎓", layout="wide")

# Custom CSS for better sidebar styling
st.markdown("""
<style>
    .sidebar-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .sidebar-header h2 {
        color: white;
        margin: 0;
    }
    .nav-item {
        padding: 0.5rem;
        margin: 0.2rem 0;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .nav-item:hover {
        background: rgba(102, 126, 234, 0.1);
        transform: translateX(5px);
    }
    .pinned-item {
        background: rgba(102, 126, 234, 0.05);
        border-left: 3px solid #667eea;
        padding: 0.5rem;
        margin: 0.3rem 0;
        border-radius: 5px;
        font-size: 0.9rem;
    }
    .recent-item {
        padding: 0.5rem;
        margin: 0.3rem 0;
        border-radius: 5px;
        font-size: 0.9rem;
        cursor: pointer;
    }
    .recent-item:hover {
        background: rgba(102, 126, 234, 0.1);
    }
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
    }
    .stTextInput > div > div > input {
        border-radius: 25px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "recent_chats" not in st.session_state:
    st.session_state.recent_chats = []
if "pinned_chats" not in st.session_state:
    st.session_state.pinned_chats = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "Chat"

# College information database with more random responses
def get_answer(question):
    q = question.lower()
    
    # Random greeting responses
    greetings = [
        "Hello! 👋 How can I help you with GNITS today?",
        "Hey there! 😊 What would you like to know about GNITS?",
        "Hi! 🎓 I'm here to answer all your GNITS questions!",
        "Greetings! 🌟 Ask me anything about GNITS college!"
    ]
    
    random_thanks = [
        "You're welcome! 😊 Anything else?",
        "Happy to help! 🎓 Feel free to ask more!",
        "My pleasure! 👍 What else would you like to know?",
        "Glad I could help! 😊 Ask away!"
    ]
    
    # Greetings
    if re.search(r'^(hi|hello|hey|namaste|good morning|good afternoon|good evening|hola|greetings)', q):
        return random.choice(greetings)
    
    # Thanks
    elif re.search(r'thank|thanks|appreciate|good job|great', q):
        return random.choice(random_thanks)
    
    # How are you
    elif re.search(r'how are you|how\'s it going|what\'s up', q):
        return "I'm doing great! 🎉 Thanks for asking! Ready to help you with GNITS queries! 😊"
    
    # Goodbye
    elif re.search(r'bye|goodbye|see you|cya|tata|exit|quit', q):
        return "Goodbye! 👋 Have a great day! Visit again if you have more questions about GNITS! 🎓"
    
    # Fee structure
    elif re.search(r'fee|fees|cost|price|tuition|fees structure|btech fee|mtech fee', q):
        return """💰 **B.Tech Fee Structure:**
- Category A/B (JEE): ₹1,62,000 per annum + JNTUH fees
- NRI Category: USD 5,000 + JNTUH fees per annum
- M.Tech: ₹1,12,000 per annum

*Additional fees may apply for hostel and other facilities*"""
    
    # Admissions
    elif re.search(r'admission|apply|eligibility|how to get|qualify|join|counseling|entrance', q):
        return """📝 **Admission Process:**

**UG Admissions (B.Tech):**
- Qualify TG-EAPCET examination
- 10+2 with Physics, Chemistry, Mathematics
- Attend counseling session based on rank

**PG Admissions (M.Tech):**
- Based on GATE score
- TS-PGECET for Non-GATE candidates

📞 Contact Admissions: 040-29565856"""
    
    # Placements
    elif re.search(r'placement|package|recruiter|company|job|salary|lpa|hiring|offer', q):
        return """🏆 **Placement Highlights:**

**Highest Package:** 50 LPA (Microsoft)
**Second Highest:** 42.6 LPA (ServiceNow)

**Top Recruiters:**
- Microsoft - 50 LPA
- ServiceNow - 42.6 LPA
- Deloitte
- Snowflake
- PwC

**Placement Percentage:** Excellent track record!"""
    
    # Facilities
    elif re.search(r'library|hostel|canteen|sports|facility|lab|gym|playground|mess', q):
        return """📚 **Facilities at GNITS:**

📖 **Library:** 8 AM to 8 PM (Monday-Saturday)
🏠 **Hostel:** Girls hostel with 24/7 security
🏃‍♀️ **Sports:** Indoor badminton, table tennis, volleyball, basketball
🍽️ **Canteen:** Vegetarian and non-vegetarian options
💻 **Labs:** State-of-the-art computer and engineering labs"""
    
    # Clubs
    elif re.search(r'club|clubs|committee|activity|technical|cultural|splash|coding|robotics|edc|acm', q):
        return """🎉 **Clubs & Committees:**

💻 **Coding Club** - CodeChef, LeetCode competitions
🤖 **Robotics Club**
💡 **Entrepreneurship Development Cell (EDC)**
🎭 **Cultural Committee** - Organizes Splash annual fest
🔧 **Technical Club** - GNITS ACM Student Chapter

**Upcoming Events:**
- IEEE ICoECIT-2026 (March 2026)
- Splash 2026 (October 2026)
- Hackathon (February 2026)"""
    
    # Events
    elif re.search(r'event|fest|splash|hackathon|workshop|seminar|ieee|alumni', q):
        return """🎪 **Upcoming Events:**

✨ **IEEE ICoECIT-2026** (AI & Quantum Computing) - March 2026
✨ **Splash 2026** (Annual Cultural Fest) - October 2026
✨ **Hackathon** - February 2026
✨ **Alumni Meet** (TU TURNO-26) - December 2026"""
    
    # Contacts
    elif re.search(r'contact|phone|number|email|call|reach|mobile|telephone|principal', q):
        return """📞 **Important Contacts:**

👩‍💼 **Principal Office:** 040-29565850
📝 **Admissions:** 040-29565856
🏢 **Training & Placement Cell:** 040-29565860
📚 **Library:** 040-29565870

🕐 Office hours: 9:30 AM to 5:00 PM (Monday-Friday)"""
    
    # About college
    elif re.search(r'about|what is|tell me about|information|overview|introduction|history', q):
        return """🏫 **About GNITS:**

G. Narayanamma Institute of Technology and Sciences (GNITS) is a prestigious women's engineering college in Hyderabad, established in 1997.

**Accreditations:** NBA, NAAC 'A' Grade

**Courses Offered:**
- B.Tech: CSE, IT, ECE, EEE, Data Science, AI & ML
- M.Tech: Various specializations

📍 **Location:** Hyderabad, Telangana

🎯 **Vision:** Empowering women in engineering since 1997"""
    
    # Random responses for unrecognized questions
    random_responses = [
        "😊 I'm here to help! You can ask me about admissions, fees, placements, facilities, clubs, or contacts. What would you like to know?",
        "🎓 Great question! I can help with information about GNITS. Try asking about fee structure, admission process, or placement details!",
        "💡 Let me help you with that! I know about GNITS admissions, fees, placements, facilities, clubs, and events. What specifically interests you?",
        "📚 I have information about GNITS college! Feel free to ask about B.Tech fees (₹1.62L/year), placements (50 LPA highest), or admission through TG-EAPCET."
    ]
    
    return random.choice(random_responses)

# Sidebar Navigation
with st.sidebar:
    st.markdown('<div class="sidebar-header"><h2>🎓 GNITS</h2></div>', unsafe_allow_html=True)
    
    # Navigation menu
    st.markdown("### 🧭 Navigation")
    
    nav_items = {
        "Chat": "💬",
        "Search Chats": "🔍",
        "Projects": "📁",
        "Library": "📚",
        "Apps": "📱",
        "More": "⚙️"
    }
    
    for item, icon in nav_items.items():
        col1, col2 = st.columns([1, 10])
        with col1:
            st.markdown(f"{icon}")
        with col2:
            if st.button(item, key=f"nav_{item}", use_container_width=True):
                st.session_state.current_page = item
                st.rerun()
    
    st.markdown("---")
    
    # Pinned Chats Section
    st.markdown("### 📌 Pinned")
    
    if st.session_state.pinned_chats:
        for i, chat in enumerate(st.session_state.pinned_chats):
            with st.container():
                col1, col2 = st.columns([10, 1])
                with col1:
                    if st.button(f"📌 {chat[:30]}...", key=f"pinned_{i}", use_container_width=True):
                        st.session_state.question_input = chat
                        st.rerun()
                with col2:
                    if st.button("❌", key=f"unpin_{i}"):
                        st.session_state.pinned_chats.pop(i)
                        st.rerun()
    else:
        st.caption("No pinned chats yet. Pin a chat from recent chats!")
    
    st.markdown("---")
    
    # Recent Chats Section
    st.markdown("### 🕐 Recent Chats")
    
    if st.session_state.recent_chats:
        for i, chat in enumerate(st.session_state.recent_chats[:10]):
            col1, col2 = st.columns([10, 1])
            with col1:
                if st.button(f"💬 {chat[:35]}...", key=f"recent_{i}", use_container_width=True):
                    st.session_state.question_input = chat
                    st.rerun()
            with col2:
                if st.button("📌", key=f"pin_{i}"):
                    if chat not in st.session_state.pinned_chats:
                        st.session_state.pinned_chats.append(chat)
                        st.rerun()
    else:
        st.caption("No recent chats yet. Start chatting!")
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🗑️ Clear All Chats", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main content area
if st.session_state.current_page == "Chat":
    # Header
    st.markdown('<div class="main-header"><h1>🎓 GNITS Campus Assistant</h1><p>Ask me anything about GNITS college!</p></div>', unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    default_question = st.session_state.get("question_input", "")
    question = st.chat_input("Ask your question here...", key="chat_input")
    
    # Handle direct question input from sidebar
    if default_question and not question:
        question = default_question
        st.session_state.question_input = ""
    
    if question:
        # Add to recent chats
        if question not in st.session_state.recent_chats:
            st.session_state.recent_chats.insert(0, question)
            if len(st.session_state.recent_chats) > 20:
                st.session_state.recent_chats.pop()
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        
        # Get bot response
        with st.spinner("🤔 Thinking..."):
            answer = get_answer(question)
        
        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)
        
        st.rerun()

elif st.session_state.current_page == "Search Chats":
    st.markdown('<div class="main-header"><h1>🔍 Search Chats</h1></div>', unsafe_allow_html=True)
    search_term = st.text_input("Search your chat history...")
    if search_term:
        results = [msg for msg in st.session_state.messages if search_term.lower() in msg["content"].lower()]
        if results:
            for result in results[:20]:
                st.info(f"**{result['role'].upper()}:** {result['content'][:100]}...")
        else:
            st.warning("No results found!")

elif st.session_state.current_page == "Projects":
    st.markdown('<div class="main-header"><h1>📁 My Projects</h1></div>', unsafe_allow_html=True)
    st.info("This section will show your saved projects and conversations.")

elif st.session_state.current_page == "Library":
    st.markdown('<div class="main-header"><h1>📚 Knowledge Library</h1></div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["📝 Admissions", "💰 Fees", "🏆 Placements", "📞 Contacts", "🎉 Events"])
    
    with tabs[0]:
        st.markdown(get_answer("admission"))
    with tabs[1]:
        st.markdown(get_answer("fee"))
    with tabs[2]:
        st.markdown(get_answer("placement"))
    with tabs[3]:
        st.markdown(get_answer("contact"))
    with tabs[4]:
        st.markdown(get_answer("events"))

elif st.session_state.current_page == "Apps":
    st.markdown('<div class="main-header"><h1>📱 Apps & Tools</h1></div>', unsafe_allow_html=True)
    st.info("Connect with other GNITS tools and resources.")

elif st.session_state.current_page == "More":
    st.markdown('<div class="main-header"><h1>⚙️ More Options</h1></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Analytics", use_container_width=True):
            st.info("Coming soon!")
        if st.button("🎨 Theme Settings", use_container_width=True):
            st.info("Coming soon!")
    with col2:
        if st.button("🔔 Notifications", use_container_width=True):
            st.info("Coming soon!")
        if st.button("❓ Help & Support", use_container_width=True):
            st.info("Contact: support@gnits.edu.in")
