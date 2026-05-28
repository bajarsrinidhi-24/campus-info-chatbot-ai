import streamlit as st
import re

st.set_page_config(page_title="GNITS Campus Assistant", page_icon="🎓")

st.title("🎓 GNITS Campus Assistant")
st.markdown("Ask me anything about GNITS college!")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# College information database
def get_answer(question):
    q = question.lower()

    if re.search(r'fee|cost|price|tuition', q):
        return """💰 **B.Tech Fee Structure:**
- Category A/B (JEE): ₹1,62,000 per annum + JNTUH fees
- NRI Category: USD 5,000 + JNTUH fees per annum
- M.Tech: ₹1,12,000 per annum"""

    elif re.search(r'admission|apply|eligibility|how to get|qualify', q):
        return """📝 **Admission Process:**
- Qualify TG-EAPCET examination
- 10+2 with PCM
- Attend counseling session"""

    elif re.search(r'placement|package|company|salary|lpa', q):
        return """🏆 **Placement Highlights:**
- Highest Package: 50 LPA
- Top Recruiters: Microsoft, Deloitte, ServiceNow"""

    elif re.search(r'library|hostel|canteen|sports|facility', q):
        return """📚 **Facilities:**
- Library: 8 AM - 8 PM
- Hostel available
- Sports facilities available"""

    elif re.search(r'club|event|fest|hackathon', q):
        return """🎉 **Clubs & Events:**
- Coding Club
- Robotics Club
- Splash Fest
- Hackathons"""

    elif re.search(r'contact|phone|number|email', q):
        return """📞 **Contacts:**
- Admissions: 040-29565856
- Placement Cell: 040-29565860"""

    else:
        return "😊 Ask me about admissions, fees, placements, facilities, clubs, or contacts."

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input("Ask your question here...")

if question:
    # Store user message
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    # Show user message
    with st.chat_message("user"):
        st.markdown(question)

    # Get bot response
    answer = get_answer(question)

    # Store assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(answer)

# Sidebar
with st.sidebar:
    st.markdown("### 📌 About This Bot")
    st.info("This chatbot provides information about GNITS.")
