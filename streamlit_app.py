import streamlit as st
import os
import tempfile
from typing import List
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# ============================================
# Page Configuration
# ============================================
st.set_page_config(page_title="Campus Chatbot with PDF Upload", page_icon="🎓", layout="wide")

# ============================================
# Get API Key from Streamlit Secrets
# ============================================
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# ============================================
# Initialize Session State
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# ============================================
# Custom CSS
# ============================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
    }
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        font-size: 2rem;
        color: white;
    }
    .main-header p {
        color: rgba(255,255,255,0.9);
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 20px;
        margin: 10px 0;
        max-width: 75%;
        float: right;
        clear: both;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .bot-message {
        background: white;
        color: #2c3e50;
        padding: 12px 18px;
        border-radius: 20px;
        margin: 10px 0;
        max-width: 75%;
        float: left;
        clear: both;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102,126,234,0.4);
    }
    .upload-box {
        border: 2px dashed #667eea;
        border-radius: 20px;
        padding: 1rem;
        text-align: center;
        background: rgba(102,126,234,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# Header
# ============================================
st.markdown("""
<div class="main-header">
    <h1>🎓 Campus Chatbot with PDF Upload</h1>
    <p>Upload PDFs and ask questions - Gemini AI will answer based on the documents!</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# Helper Functions
# ============================================
def process_uploaded_files(uploaded_files):
    """Process uploaded PDF files and create vector store"""
    if not uploaded_files:
        return None
    
    all_documents = []
    
    with st.spinner("📚 Processing PDF files... This may take a moment."):
        for uploaded_file in uploaded_files:
            # Save uploaded file to temp location
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            try:
                # Load PDF
                loader = PyPDFLoader(tmp_path)
                documents = loader.load()
                
                # Add metadata
                for doc in documents:
                    doc.metadata["source"] = uploaded_file.name
                
                all_documents.extend(documents)
                
                # Clean up temp file
                os.unlink(tmp_path)
                
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {e}")
    
    if not all_documents:
        return None
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(all_documents)
    
    # Create embeddings and vector store
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="pdf_knowledge"
    )
    
    # Setup QA chain
    prompt_template = """You are Campus Bot, a helpful assistant for GNITS college.
    Answer based on the provided context from uploaded PDFs.
    Be friendly, accurate, and helpful.
    
    Context: {context}
    
    Question: {question}
    
    Answer:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    return qa_chain

def get_simple_response(question):
    """Fallback response when no PDFs are uploaded"""
    q = question.lower()
    
    if re.search(r'(hi|hello|hey)', q):
        return "Hello! 👋 Welcome to Campus Chatbot! Please upload PDF files first, then I can answer questions based on them. 😊"
    elif re.search(r'(fee|fees|cost|tuition)', q):
        return "💰 Please upload the fee structure PDF to get accurate information about B.Tech fees."
    elif re.search(r'(attendance|75%)', q):
        return "📊 Please upload the academic regulations PDF to get accurate attendance policy information."
    elif re.search(r'(placement|package|lpa)', q):
        return "🏆 Please upload the placement brochure PDF to get detailed placement statistics."
    else:
        return "📚 **Welcome to Campus Chatbot!**\n\nPlease upload PDF files (syllabus, regulations, handbooks) using the sidebar. Once uploaded, I can answer any question based on those documents!\n\n**You can ask me about:**\n• Course syllabus and subjects\n• Academic regulations and attendance\n• Fee structure\n• Placement details\n• Exam patterns and grading\n\n**Upload your PDFs to get started!** 📄"

# ============================================
# Sidebar - PDF Upload Section
# ============================================
with st.sidebar:
    st.markdown("### 📄 Upload PDF Documents")
    st.markdown("Upload your academic PDFs (syllabus, regulations, handbooks)")

    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload PDFs containing academic information"
    )

    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) selected")
        
        if st.button("🚀 Process PDFs", use_container_width=True):
            with st.spinner("Processing PDFs and building knowledge base..."):
                st.session_state.qa_chain = process_uploaded_files(uploaded_files)
                if st.session_state.qa_chain:
                    st.session_state.uploaded_files = uploaded_files
                    st.success("✅ PDFs processed successfully! You can now ask questions.")
                    st.rerun()
    
    st.markdown("---")
    st.markdown("### ℹ️ How it works")
    st.info("""
    1. 📄 Upload PDF files
    2. 🔄 Click 'Process PDFs'
    3. 💬 Ask questions based on the documents
    4. 🤖 AI answers using PDF content
    """)
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ============================================
# Main Chat Interface
# ============================================
if st.session_state.qa_chain:
    st.success(f"✅ Active Knowledge Base: {len(st.session_state.uploaded_files)} PDF(s) loaded")
else:
    st.warning("⚠️ No PDFs processed yet. Upload PDFs in the sidebar and click 'Process PDFs' to start.")

st.markdown("### 💬 Chat with Campus Bot")

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end;">
            <div class="user-message">
                <strong>You</strong><br>{msg["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start;">
            <div class="bot-message">
                <strong>🎓 Campus Bot</strong><br>{msg["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Chat input
question = st.chat_input("Ask about your uploaded PDFs...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    
    with st.chat_message("user"):
        st.markdown(question)
    
    with st.chat_message("assistant"):
        with st.spinner("🤔 Searching through your documents..."):
            try:
                if st.session_state.qa_chain:
                    result = st.session_state.qa_chain.invoke({"query": question})
                    answer = result["result"]
                else:
                    answer = get_simple_response(question)
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

if not st.session_state.messages:
    if st.session_state.qa_chain:
        st.info("📚 **Ready!** Uploaded PDFs are processed. Ask me anything about the content! 🎓")
    else:
        st.info("📄 **Upload PDF files** in the sidebar and click 'Process PDFs' to start asking questions!")
