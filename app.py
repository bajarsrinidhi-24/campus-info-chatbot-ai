import streamlit as st
import time
import json
from datetime import datetime
from src.chatbot import get_answer

st.set_page_config(
    page_title="Campus Info Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stChatMessage { border-radius: 12px; margin-bottom: 0.5rem; }
    .suggestion-btn { margin: 0.25rem; }
    .feedback-row { display: flex; gap: 8px; margin-top: 4px; }
    .stat-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        text-align: center;
        border: 1px solid #e9ecef;
    }
    .stat-card h3 { margin: 0; font-size: 1.5rem; color: #1a1a2e; }
    .stat-card p  { margin: 0; font-size: 0.78rem; color: #6c757d; }
    .topic-badge {
        display: inline-block;
        background: #e8f4f8;
        color: #0077b6;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.75rem;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ── Session state initialisation ──────────────────────────────────────────────
defaults = {
    "messages": [],
    "conversations": [],        # saved past conversations
    "feedback": {},             # {msg_index: "👍"/"👎"}
    "total_questions": 0,
    "session_start": datetime.now().strftime("%H:%M"),
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Quick-question suggestions ────────────────────────────────────────────────
SUGGESTIONS = [
    "📅 Academic calendar",
    "🏛️ Library hours",
    "🍽️ Cafeteria menu",
    "🚌 Campus shuttle",
    "📝 Admission process",
    "💰 Fee structure",
    "🏥 Health centre",
    "📞 Emergency contacts",
]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 Campus Chatbot")
    st.caption(f"Session started at {st.session_state.session_start}")
    st.divider()

    # Stats
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{st.session_state.total_questions}</h3>
            <p>Questions asked</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        thumbs_up = sum(1 for v in st.session_state.feedback.values() if v == "👍")
        st.markdown(f"""
        <div class="stat-card">
            <h3>{thumbs_up}</h3>
            <p>Helpful answers</p>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # Popular topics
    st.markdown("**Popular topics**")
    for topic in ["Admissions", "Exams", "Hostel", "Fees", "Events"]:
        st.markdown(f'<span class="topic-badge">{topic}</span>', unsafe_allow_html=True)

    st.divider()

    # Conversation history
    st.markdown("**Past conversations**")
    if st.session_state.conversations:
        for i, convo in enumerate(reversed(st.session_state.conversations[-5:])):
            with st.expander(f"💬 {convo['title']}", expanded=False):
                st.caption(convo["timestamp"])
                for msg in convo["messages"][:4]:
                    role_icon = "🧑" if msg["role"] == "user" else "🤖"
                    st.caption(f"{role_icon} {msg['content'][:80]}{'…' if len(msg['content'])>80 else ''}")
    else:
        st.caption("No past conversations yet.")

    st.divider()

    # Settings
    st.markdown("**Settings**")
    show_timestamps = st.toggle("Show timestamps", value=False)
    auto_scroll     = st.toggle("Auto-scroll",     value=True)
    typing_delay    = st.slider("Response speed (s)", 0.0, 2.0, 0.5, 0.1)

    st.divider()

    # Export & clear
    if st.button("💾 Save conversation", use_container_width=True):
        if st.session_state.messages:
            convo = {
                "title": st.session_state.messages[0]["content"][:40] + "…",
                "timestamp": datetime.now().strftime("%d %b %Y, %H:%M"),
                "messages": st.session_state.messages.copy(),
            }
            st.session_state.conversations.append(convo)
            st.toast("Conversation saved!", icon="✅")

    if st.session_state.messages:
        chat_export = json.dumps(
            [{"role": m["role"], "content": m["content"],
              "time": m.get("time", "")}
             for m in st.session_state.messages],
            indent=2, ensure_ascii=False
        )
        st.download_button(
            "📥 Export as JSON",
            data=chat_export,
            file_name=f"campus_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True,
        )

    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.feedback = {}
        st.rerun()

# ── Main chat area ────────────────────────────────────────────────────────────
st.title("🎓 Campus Info Chatbot")
st.write("Ask me anything about our campus!")

# Quick-question chips
st.markdown("**Quick questions:**")
cols = st.columns(4)
for i, suggestion in enumerate(SUGGESTIONS):
    if cols[i % 4].button(suggestion, key=f"sug_{i}", use_container_width=True):
        # Treat the chip click as a user message
        clean_text = suggestion.split(" ", 1)[1]   # strip the emoji prefix
        st.session_state.messages.append({
            "role": "user",
            "content": clean_text,
            "time": datetime.now().strftime("%H:%M"),
        })
        st.session_state.total_questions += 1
        with st.spinner("Thinking…"):
            time.sleep(typing_delay)
            response = get_answer(clean_text)
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "time": datetime.now().strftime("%H:%M"),
        })
        st.rerun()

st.divider()

# Render existing messages
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if show_timestamps and "time" in message:
            st.caption(f"🕐 {message['time']}")

        # Feedback buttons (only on assistant messages)
        if message["role"] == "assistant":
            current_fb = st.session_state.feedback.get(idx)
            fb_col1, fb_col2, fb_col3 = st.columns([1, 1, 8])
            with fb_col1:
                if st.button(
                    "👍" if current_fb != "👍" else "✅",
                    key=f"up_{idx}",
                    help="Helpful",
                ):
                    st.session_state.feedback[idx] = "👍"
                    st.toast("Thanks for the feedback!", icon="👍")
                    st.rerun()
            with fb_col2:
                if st.button(
                    "👎" if current_fb != "👎" else "❌",
                    key=f"dn_{idx}",
                    help="Not helpful",
                ):
                    st.session_state.feedback[idx] = "👎"
                    st.toast("We'll work on improving that.", icon="👎")
                    st.rerun()

# Chat input
if prompt := st.chat_input("Ask your question here…"):
    now = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({"role": "user", "content": prompt, "time": now})
    st.session_state.total_questions += 1

    with st.chat_message("user"):
        st.write(prompt)
        if show_timestamps:
            st.caption(f"🕐 {now}")

    # Typing indicator
    with st.chat_message("assistant"):
        with st.spinner("Typing…"):
            time.sleep(typing_delay)
            response = get_answer(prompt)
        st.write(response)
        now_resp = datetime.now().strftime("%H:%M")
        if show_timestamps:
            st.caption(f"🕐 {now_resp}")
        msg_idx = len(st.session_state.messages)
        st.session_state.messages.append(
            {"role": "assistant", "content": response, "time": now_resp}
        )
