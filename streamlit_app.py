import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="GNITS Campus Assistant", page_icon="🎓")
st.title("🎓 GNITS Campus Assistant")
st.markdown("Ask me anything about GNITS college!")

# College information database
COLLEGE_INFO = """
G. Narayanamma Institute of Technology and Sciences (GNITS), Hyderabad

📝 ADMISSIONS:
- UG: TG-EAPCET exam required. Eligibility: 10+2 with Physics, Chemistry, Mathematics
- PG: Based on GATE score or TS-PGECET

💰 FEE STRUCTURE:
- B.Tech: ₹1,62,000 per year + JNTUH fees
- M.Tech: ₹1,12,000 per year

🏆 PLACEMENTS:
- Highest Package: 50 LPA (Microsoft)
- Top Recruiters: Microsoft, ServiceNow (42.6 LPA), Deloitte, Snowflake, PwC

📚 FACILITIES:
- Library: 8 AM to 8 PM (Monday-Saturday)
- Hostel: Girls hostel with 24/7 security
- Sports: Indoor games, volleyball, basketball court

🎉 CLUBS & EVENTS:
- Coding Club, Robotics Club, Entrepreneurship Cell (EDC)
- Cultural Committee, Technical Club (ACM)
- IEEE ICoECIT-2026, Splash Fest, Hackathon

📞 CONTACTS:
- Admissions: 040-29565856
- Principal Office: 040-29565850
- Placements: 040-29565860
"""

# Configure Gemini
API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyDXlKYyFfC2Ays0_ULNApJyfznF7Iwd8Eg")
genai.configure(api_key=API_KEY)

# Use the more stable model
model = genai.GenerativeModel('gemini-1.5-flash')

# Quick questions
st.markdown("### 💡 Quick Questions")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📝 Fee Structure"):
        st.session_state.question = "What is the fee structure for B.Tech?"
with col2:
    if st.button("🎓 How to get admission?"):
        st.session_state.question = "How can I get admission in GNITS?"
with col3:
    if st.button("🏆 Placement details"):
        st.session_state.question = "What is the placement record?"

# Chat input
question = st.text_input("Your question:", value=st.session_state.get("question", ""))

if question:
    with st.spinner("Thinking..."):
        prompt = f"""You are a helpful campus assistant for GNITS college. Answer questions based ONLY on this information:

{COLLEGE_INFO}

Question: {question}

Provide a helpful, accurate answer. If the information is not available, say so politely.
Answer:"""
        
        response = model.generate_content(prompt)
        st.write("**Answer:**", response.text)
        
        # Add helpful footer
        st.caption("💡 For more details, contact GNITS directly at 040-29565856")
