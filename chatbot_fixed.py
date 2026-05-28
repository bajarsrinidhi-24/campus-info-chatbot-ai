import os
import pickle
from google import genai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

API_KEY = "AIzaSyDXlKYyFfC2Ays0_ULNApJyfznF7Iwd8Eg"

client = genai.Client(api_key=API_KEY)

class GNITSChatbot:
    def __init__(self):
        print('Loading chatbot...')
        with open('vectorstore/chunks.pkl', 'rb') as f:
            self.chunks = pickle.load(f)
        with open('vectorstore/embeddings.pkl', 'rb') as f:
            self.embeddings = pickle.load(f)
        print(f'✅ Loaded {len(self.chunks)} knowledge chunks')
    
    def ask(self, question):
        result = client.models.embed_content(
            model='gemini-embedding-2-preview',
            contents=[question],
            config={'output_dimensionality': 768}
        )
        question_embedding = result.embeddings[0].values
        similarities = cosine_similarity([question_embedding], self.embeddings)[0]
        top_indices = np.argsort(similarities)[-3:][::-1]
        context = '\n'.join([self.chunks[i] for i in top_indices])
        prompt = f"""You are a helpful campus chatbot for GNITS. Answer based ONLY on this context. Be concise.

Context: {context}

Question: {question}

Answer:"""
        response = client.models.generate_content(model='gemini-2.0-flash', contents=[prompt])
        return response.text