import streamlit as st
import os
import pickle
from google import genai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="GNITS Campus Assistant", page_icon="🎓")

st.title("🎓 GNITS Campus Assistant")
st.markdown("Ask me anything about GNITS!")

# College data (embedded directly)
COLLEGE_DATA = """
GNITS (G. Narayanamma Institute of Technology and Sciences) - Hyderabad

ADMISSIONS:
- UG: TG-EAPCET exam required. Eligibility: 10+2 with Physics, Chemistry, Mathematics
- PG: Based on GATE score or TS-PGECET

FEE STRUCTURE:
- B.Tech: ₹1,62,000 per annum + JNTUH fees
- M.Tech: ₹1,12,000 per annum

PLACEMENTS:
- Highest package: 50 LPA (Microsoft)
- Top recruiters: Microsoft, ServiceNow, Deloitte, Snowflake

FACILITIES:
- Library: 8 AM to 8 PM (Monday-Saturday)
- Hostel: Girls hostel with 24/7 security
- Sports: Indoor games, volleyball, basketball

CLUBS:
- Coding Club, Robotics Club, Entrepreneurship Cell, Cultural Committee

CONTACTS:
- Admissions: 040-29565856
- Principal: 040-29565850
- Placements: 040-29565860
"""

@st.cache_resource
def get_chatbot():
    # Create embeddings from college data
    API_KEY = "AIzaSyDXlKYyFfC2Ays0_ULNApJyfznF7Iwd8Eg"
    client = genai.Client(api_key=API_KEY)
    
    # Split into chunks
    chunks = [COLLEGE_DATA[i:i+500] for i in range(0, len(COLLEGE_DATA), 500)]
    
    # Create embeddings
    embeddings = []
    for chunk in chunks:
        result = client.models.embed_content(
            model='gemini-embedding-2-preview',
            contents=[chunk],
            config={'output_dimensionality': 768}
        )
        embeddings.append(result.embeddings[0].values)
    
    return client, chunks, embeddings

# Quick questions
st.markdown("### 💡 Quick Questions")
cols = st.columns(3)
questions = ["Fee structure?", "How to get admission?", "Placement details?"]
for i, q in enumerate(questions):
    if cols[i].button(q):
        st.session_state.question = q

# Chat input
question = st.text_input("Your question:", value=st.session_state.get("question", ""))

if question:
    with st.spinner("Thinking..."):
        client, chunks, embeddings = get_chatbot()
        
        # Embed question
        result = client.models.embed_content(
            model='gemini-embedding-2-preview',
            contents=[question],
            config={'output_dimensionality': 768}
        )
        q_embedding = result.embeddings[0].values
        
        # Find similar chunks
        similarities = cosine_similarity([q_embedding], embeddings)[0]
        top_idx = np.argsort(similarities)[-2:][::-1]
        context = '\n'.join([chunks[i] for i in top_idx])
        
        # Generate answer
        prompt = f"Answer based on this college info:\n{context}\n\nQuestion: {question}\nAnswer:"
        response = client.models.generate_content(model='gemini-2.0-flash-lite', contents=[prompt])
        
        st.write("**Answer:**", response.text)
