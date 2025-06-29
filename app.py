import streamlit as st
import requests

# ---- Page Setup ----
st.set_page_config(
    page_title="AI Therapist",
    page_icon="🧠",
    layout="centered",  # better for mobile
    initial_sidebar_state="collapsed",
)

# ---- Styling ----
st.markdown("""
    <style>
    .stChatMessage { padding: 1rem; border-radius: 1.25rem; margin-bottom: 0.5rem; }
    .stChatMessage.user { background-color: #DCF8C6; text-align: right; }
    .stChatMessage.assistant { background-color: #F1F0F0; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    textarea { font-size: 1rem !important; }
    </style>
""", unsafe_allow_html=True)

# ---- Chat Memory ----
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title("🧠 AI Therapist")

st.markdown(
    "Talk to a supportive AI therapist trained in CBT techniques. This is for emotional support only — not medical advice."
)

# ---- Display Chat ----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- User Input ----
if prompt := st.chat_input("How are you feeling today?"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Format prompt history for backend
    history_prompt = "\n".join(
        [f"User: {m['content']}" if m["role"] == "user" else f"Therapist: {m['content']}"
         for m in st.session_state.messages]
    ) + "\nTherapist:"

    # Send to backend
    with st.spinner("Thinking..."):
        res = requests.post("http://localhost:8000/chat", json={"prompt": history_prompt})
        reply = res.json()["reply"]

    # Show therapist reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
