import streamlit as st
from chatbot_fixed import GNITSChatbot

st.set_page_config(page_title='GNITS Campus Assistant', page_icon='🎓')

st.title('🎓 GNITS Campus Assistant')
st.markdown('Ask me anything about GNITS - admissions, placements, fees, facilities, clubs, and more!')

@st.cache_resource
def init_chatbot():
    return GNITSChatbot()

try:
    chatbot = init_chatbot()
    
    st.markdown('### 💡 Try asking:')
    cols = st.columns(3)
    suggestions = [
        'What is the fee structure?',
        'How to get admission?',
        'What is the highest package?',
        'Tell me about clubs',
        'Library timings?',
        'Contact for admissions?'
    ]
    for i, suggestion in enumerate(suggestions):
        if cols[i % 3].button(suggestion, key=suggestion):
            st.session_state.question = suggestion
    
    question = st.text_input('Your question:', value=st.session_state.get('question', ''))
    
    if question:
        with st.spinner('Thinking...'):
            answer = chatbot.ask(question)
            st.write('**Answer:**', answer)
            
            st.session_state.last_question = question
            st.session_state.last_answer = answer
    
    if 'last_answer' in st.session_state and not question:
        st.write('**Last answer:**', st.session_state.last_answer)
        
except Exception as e:
    st.error(f'Error: {e}')
    st.info('Please run python build_vectorstore_fixed.py first!')
