import os
import pickle
from google import genai
import time

# YOUR NEW API KEY
API_KEY = "AIzaSyDXlKYyFfC2Ays0_ULNApJyfznF7Iwd8Eg"

# Initialize client with new API key
client = genai.Client(api_key=API_KEY)

print('=' * 50)
print('BUILDING VECTOR DATABASE')
print('=' * 50)

# Read the data file
if not os.path.exists('data/gnits_data.txt'):
    print('ERROR: data/gnits_data.txt not found!')
    exit(1)

with open('data/gnits_data.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print(f'✅ Read {len(text)} characters')

# Simple chunking
print('Splitting text into chunks...')
chunks = []
chunk_size = 500
for i in range(0, len(text), chunk_size):
    chunk = text[i:i+chunk_size]
    if chunk.strip():
        chunks.append(chunk)

print(f'✅ Created {len(chunks)} chunks')

# Create embeddings using gemini-embedding-2-preview
print('Creating embeddings with gemini-embedding-2-preview...')
print('(This model supports 768 dimensions, perfect for our vector DB)')
embeddings = []
for i, chunk in enumerate(chunks):
    print(f'  Processing chunk {i+1}/{len(chunks)}...')
    try:
        result = client.models.embed_content(
            model='gemini-embedding-2-preview',
            contents=[chunk],
            config={'output_dimensionality': 768}
        )
        embeddings.append(result.embeddings[0].values)
        print(f'    ✓ Success!')
    except Exception as e:
        print(f'    ✗ Error: {e}')
        embeddings.append([0.0] * 768)
    time.sleep(0.5)  # Small delay to avoid rate limits

# Save everything
os.makedirs('vectorstore', exist_ok=True)
with open('vectorstore/chunks.pkl', 'wb') as f:
    pickle.dump(chunks, f)
with open('vectorstore/embeddings.pkl', 'wb') as f:
    pickle.dump(embeddings, f)

print('=' * 50)
print('✅ VECTOR DATABASE CREATED SUCCESSFULLY!')
print(f'📁 Saved {len(chunks)} chunks with embeddings')
print('=' * 50)
