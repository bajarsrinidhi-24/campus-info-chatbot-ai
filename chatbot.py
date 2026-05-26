from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class GNITSChatbot:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0.3,
            top_p=0.85
        )
        self.vectorstore = None
        self.qa_chain = None
        self.load_vectorstore()
    
    def load_vectorstore(self):
        """Load FAISS vector store"""
        if os.path.exists("vectorstore/gnits_faiss"):
            self.vectorstore = FAISS.load_local(
                "vectorstore/gnits_faiss", 
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            self.setup_qa_chain()
            print("✅ Vectorstore loaded")
        else:
            print("⚠️ No vectorstore found. Run build_vectorstore.py first.")
    
    def setup_qa_chain(self):
        """Setup retrieval QA chain with custom prompt"""
        prompt_template = """
        You are a helpful campus chatbot for G. Narayanamma Institute of Technology and Sciences (GNITS), Hyderabad.
        Answer questions based ONLY on the following context about GNITS. 
        If the answer is not in the context, say "I don't have that information from the college handbook or website. Please contact the college directly."
        Be friendly, concise, and accurate.
        
        Context from GNITS website & handbook:
        {context}
        
        Question: {question}
        
        Answer:
        """
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
    
    def ask(self, question):
        """Ask a question to the chatbot"""
        if not self.qa_chain:
            return "Chatbot not ready. Please check vectorstore.", []
        
        result = self.qa_chain.invoke({"query": question})
        answer = result['result']
        sources = [doc.metadata.get('source', 'Unknown') for doc in result['source_documents']]
        
        return answer, sources

# Test the bot
if __name__ == "__main__":
    bot = GNITSChatbot()
    test_questions = [
        "What is the placement percentage at GNITS?",
        "Tell me about clubs at GNITS",
        "What is the library timing?"
    ]
    
    for q in test_questions:
        print(f"\n❓ {q}")
        ans, src = bot.ask(q)
        print(f"🤖 {ans}")
        print(f"📚 Sources: {src}")
