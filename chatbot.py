import os
import pickle
from google import genai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()

API_KEY = "AIzaSyDXlKYyFfC2Ays0_ULNApJyfznF7Iwd8Eg"
client = genai.Client(api_key=API_KEY)

class GNITSChatbot:
    def __init__(self):
        print("Loading chatbot...")
        # Load chunks and embeddings
        with open('vectorstore/chunks.pkl', 'rb') as f:
            self.chunks = pickle.load(f)
        with open('vectorstore/embeddings.pkl', 'rb') as f:
            self.embeddings = pickle.load(f)
        print(f"✅ Loaded {len(self.chunks)} knowledge chunks")
    
    def ask(self, question):
        # Embed the question
        result = client.models.embed_content(
            model='gemini-embedding-2-preview',
            contents=[question],
            config={'output_dimensionality': 768}
        )
        question_embedding = result.embeddings[0].values
        
        # Find similar chunks
        similarities = cosine_similarity([question_embedding], self.embeddings)[0]
        top_indices = np.argsort(similarities)[-3:][::-1]
        
        # Get relevant context
        context = '\n'.join([self.chunks[i] for i in top_indices])
        
        # Generate answer
        prompt = f"""You are a helpful campus chatbot for GNITS. Answer based on this context.

Context: {context}

Question: {question}

Answer:"""
        
        response = client.models.generate_content(
            model='gemini-2.0-flash-lite',
            contents=[prompt]
        )
        return response.text
