import streamlit as st
import requests

st.set_page_config(page_title="AI Therapist", page_icon="🧠")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title("🧠 AI Therapist Chat")

st.markdown("Talk to a supportive AI therapist trained in CBT. This is not medical advice.")

# Display previous messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# Input box
if prompt := st.chat_input("How are you feeling today?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Send full chat history to backend
    history_for_model = "\n".join(
        [f"User: {m['content']}" if m["role"] == "user" else f"Therapist: {m['content']}"
         for m in st.session_state.messages]
    )
    history_for_model += "\nTherapist:"

    # Call backend
    with st.spinner("Thinking..."):
        res = requests.post("http://localhost:8000/chat", json={"prompt": history_for_model})
        reply = res.json()["reply"]

    # Add response to history and display it
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
