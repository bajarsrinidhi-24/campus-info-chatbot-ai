import streamlit as st
import re

st.set_page_config(page_title="GNITS Campus Assistant", page_icon="🎓")
st.title("🎓 GNITS Campus Assistant")
st.markdown("Ask me anything about GNITS college!")

# College information database
def get_answer(question):
    q = question.lower()
    
    # Fee structure
    if re.search(r'fee|cost|price|tuition', q):
        return """💰 **B.Tech Fee Structure:**
- Category A/B (JEE): ₹1,62,000 per annum + JNTUH fees
- NRI Category: USD 5,000 + JNTUH fees per annum
- M.Tech: ₹1,12,000 per annum

*Additional fees may apply for hostel and other facilities.*"""
    
    # Admissions
    elif re.search(r'admission|apply|eligibility|how to get|qualify', q):
        return """📝 **Admission Process:**
        
**UG Admissions (B.Tech):**
- Qualify TG-EAPCET examination
- 10+2 with Physics, Chemistry, Mathematics
- Attend counseling session based on rank

**PG Admissions (M.Tech):**
- Based on GATE score
- TS-PGECET for Non-GATE candidates

**Contact Admissions:** 040-29565856"""
    
    # Placements
    elif re.search(r'placement|package|recruiter|company|job|salary|lpa', q):
        return """🏆 **Placement Highlights:**
        
- **Highest Package:** 50 LPA (Microsoft)
- **Second Highest:** 42.6 LPA (ServiceNow)
- **Top Recruiters:** Microsoft, ServiceNow, Deloitte, Snowflake, PwC
- **Notable Alumni:** Shreya Arukala (ServiceNow), Joy Princy (Microsoft)

*GNITS has an excellent placement track record!*"""
    
    # Facilities
    elif re.search(r'library|hostel|canteen|sports|facility|gym|lab', q):
        return """📚 **Facilities at GNITS:**
        
- **Library:** 8 AM to 8 PM (Monday-Saturday)
- **Hostel:** Separate girls hostel with 24/7 security
- **Canteen:** Vegetarian and non-vegetarian options
- **Sports:** Indoor badminton, table tennis, volleyball, basketball court
- **Labs:** State-of-the-art computer and engineering labs"""
    
    # Clubs
    elif re.search(r'club|committee|activity|fest|event|hackathon', q):
        return """🎉 **Clubs & Events:**
        
**Clubs:**
- Coding Club (CodeChef, LeetCode competitions)
- Robotics Club
- Entrepreneurship Development Cell (EDC)
- Cultural Committee
- Technical Club (GNITS ACM Student Chapter)

**Upcoming Events:**
- IEEE ICoECIT-2026 (AI & Quantum Computing) - March 2026
- Splash 2026 (Annual Cultural Fest) - October 2026
- Hackathon - February 2026"""
    
    # Contacts
    elif re.search(r'contact|phone|number|email|call|reach', q):
        return """📞 **Important Contacts:**
        
- **Admissions:** 040-29565856
- **Principal Office:** 040-29565850
- **Training & Placement Cell:** 040-29565860
- **Library:** 040-29565870

*Office hours: 9:30 AM to 5:00 PM (Monday-Friday)*"""
    
    # About college
    elif re.search(r'about|what is|college|institute', q):
        return """🏫 **About GNITS:**
        
G. Narayanamma Institute of Technology and Sciences (GNITS) is a prestigious women's engineering college in Hyderabad, established in 1997.

**Accreditations:** NBA, NAAC 'A' Grade
**Courses:** B.Tech (CSE, IT, ECE, EEE, Data Science, AI & ML), M.Tech

The college is known for academic excellence, strong placements, and empowering women in engineering."""
    
    # Default response
    else:
        return "I'm here to help! 😊\n\nYou can ask me about:\n- 📝 Admissions & Eligibility\n- 💰 Fee Structure\n- 🏆 Placements & Packages\n- 📚 Facilities (Library, Hostel, Sports)\n- 🎉 Clubs & Events\n- 📞 Contact Numbers\n\nWhat would you like to know?"

# Quick question buttons
st.markdown("### 💡 Quick Questions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💰 Fee Structure"):
        st.session_state.question = "What is the fee structure?"
with col2:
    if st.button("📝 How to get admission?"):
        st.session_state.question = "How to get admission in GNITS?"
with col3:
    if st.button("🏆 Placement details"):
        st.session_state.question = "What is the placement package?"
with col4:
    if st.button("📞 Contact numbers"):
        st.session_state.question = "Give me contact numbers"

# Chat input
question = st.text_input("Your question:", value=st.session_state.get("question", ""))

if question:
    answer = get_answer(question)
    st.write(answer)
    
    # Add helpful footer
    st.caption("💡 For more details, contact GNITS directly at 040-29565856")

# Sidebar info
with st.sidebar:
    st.markdown("### 📌 About This Bot")
    st.info("This chatbot provides information about GNITS college based on official data.")
    st.markdown("---")
    st.markdown("### 🏫 GNITS Hyderabad")
    st.markdown("Empowering women in engineering since 1997")
