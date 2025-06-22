import streamlit as st
import requests

st.title("AI Therapist (Mistral 7B)")

user_input = st.text_area("How are you feeling today?", height=150)

if st.button("Send"):
    with st.spinner("Thinking..."):
        res = requests.post("http://localhost:8000/chat", json={"message": user_input})
        reply = res.json()["reply"]
        st.markdown(f"**Therapist:** {reply}")
