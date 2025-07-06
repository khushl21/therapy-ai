import streamlit as st
import requests
import speech_recognition as sr
from textblob import TextBlob
from gradio_client import Client

# ------------------- Config & Setup -------------------
st.set_page_config(page_title="AI Therapist", layout="centered")
st.title("🧠 AI Therapist with Voice & Emotion Support")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ------------------- Emotion Analysis -------------------
def analyze_emotion(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.3:
        return "😊 Positive"
    elif polarity < -0.3:
        return "😞 Negative"
    else:
        return "😐 Neutral"

# ------------------- Voice Input -------------------
def transcribe_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now.")
        audio = r.listen(source, phrase_time_limit=5)
    try:
        text = r.recognize_google(audio)
        st.success(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I couldn't understand.")
        return ""
    except sr.RequestError:
        st.error("Speech Recognition error.")
        return ""

# ------------------- Voice Output using Hugging Face API -------------------
def speak_text(text, selected_voice):
    try:
        client = Client("NihalGazi/Text-To-Speech-Unlimited")
        result = client.predict(
            prompt=text,
            voice=selected_voice,
            emotion="calm, soothing and understanding",
            use_random_seed=True,
            specific_seed=12345,
            api_name="/text_to_speech_app"
        )
        audio_path = result[0]  # This is a local file path, not a URL

        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        st.audio(audio_bytes, format="audio/mp3")
    except Exception as e:
        st.error(f"🔊 Text-to-Speech failed: {e}")

# ------------------- Chat Interface -------------------
st.markdown("This AI provides emotional support. Not a replacement for real therapy.")

col1, col2 = st.columns([1, 1])
with col1:
    use_voice = st.button("🎤 Use Voice Input")
with col2:
    voice_output = st.checkbox("🔊 Speak Therapist Reply")

# ------------------- Voice Selection -------------------
gender = st.radio("Choose voice type:", ["Male", "Female"], index=0, horizontal=True)
selected_voice = "echo" if gender == "Male" else "nova"

# ------------------- Input Handling -------------------
if use_voice:
    prompt = transcribe_speech()
else:
    prompt = st.chat_input("Type or use voice to start talking...")

# ------------------- Chat History -------------------
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------- On New Message -------------------
if prompt:
    emotion = analyze_emotion(prompt)
    st.markdown(f"🧠 Emotion detected: **{emotion}**")

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    history = "\n".join(
        [f"User: {m['content']}" if m["role"] == "user" else f"Therapist: {m['content']}"
         for m in st.session_state["messages"]]
    ) + "\nTherapist:"

    with st.spinner("Thinking..."):
        res = requests.post("http://localhost:8000/chat", json={"prompt": history})
        reply = res.json()["reply"]

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

    if voice_output:
        speak_text(reply, selected_voice)
