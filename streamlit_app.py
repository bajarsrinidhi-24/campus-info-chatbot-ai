import streamlit as st
from google import genai

st.set_page_config(page_title="GNITS Campus Assistant", page_icon="🎓")
st.title("🎓 GNITS Campus Assistant")

# College information
COLLEGE_INFO = """
GNITS (Hyderabad) - Key Information:

Admissions: UG through TG-EAPCET, PG through GATE
B.Tech Fee: ₹1,62,000 per year
M.Tech Fee: ₹1,12,000 per year
Highest Package: 50 LPA (Microsoft)
Top Recruiters: Microsoft, ServiceNow, Deloitte
Library: 8 AM to 8 PM
Contact Admissions: 040-29565856
"""

API_KEY = "AIzaSyDXlKYyFfC2Ays0_ULNApJyfznF7Iwd8Eg"
client = genai.Client(api_key=API_KEY)

st.markdown("### Ask any question about GNITS:")

question = st.text_input("Your question:")

if question:
    with st.spinner("Thinking..."):
        prompt = f"Based on this college info: {COLLEGE_INFO}\n\nAnswer this question: {question}\n\nAnswer concisely:"
        response = client.models.generate_content(model='gemini-2.0-flash-lite', contents=[prompt])
        st.write("**Answer:**", response.text)

st.info("Ask about admissions, fees, placements, facilities, or contacts!")
