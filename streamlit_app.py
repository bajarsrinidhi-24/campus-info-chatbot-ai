import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="GNITS Campus Assistant", page_icon="🎓")
st.title("🎓 GNITS Campus Assistant")
st.markdown("Powered by DeepSeek AI 🚀")

# College information
COLLEGE_INFO = """
G. Narayanamma Institute of Technology and Sciences (GNITS), Hyderabad

ADMISSIONS:
- UG: TG-EAPCET exam required. Eligibility: 10+2 with Physics, Chemistry, Mathematics
- PG: Based on GATE score or TS-PGECET

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

CLUBS:
- Coding Club, Robotics Club, Entrepreneurship Cell (EDC)
- Cultural Committee, Technical Club (ACM)

CONTACTS:
- Admissions: 040-29565856
- Principal: 040-29565850
- Placements: 040-29565860
"""

# Get DeepSeek API key from secrets
DEEPSEEK_API_KEY = st.secrets["DEEPSEEK_API_KEY"]

# Initialize DeepSeek client
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

# Quick questions
st.markdown("### 💡 Quick Questions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💰 Fee Structure"):
        st.session_state.question = "What is the fee structure for B.Tech?"
with col2:
    if st.button("📝 How to get admission?"):
        st.session_state.question = "How can I get admission in GNITS?"
with col3:
    if st.button("🏆 Placement details"):
        st.session_state.question = "What is the placement record?"
with col4:
    if st.button("📞 Contact numbers"):
        st.session_state.question = "Give me contact numbers"

# Chat input
question = st.text_input("Your question:", value=st.session_state.get("question", ""))

if question:
    with st.spinner("🤔 CampusBot is thinking..."):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": f"You are CampusBot, a helpful assistant for GNITS college. Answer based on: {COLLEGE_INFO}. Be concise and friendly."},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=500
            )
            st.write("**Answer:**", response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Please check your API key in Secrets.")

st.caption("💡 Ask about admissions, fees, placements, facilities, and contacts!")
