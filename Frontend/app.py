# app.py
import streamlit as st
import os

from components.mode_select import mode_selector
from components.trans import show_transcript
from services.recorder import start_recording, stop_recording_and_save
from services.STT import transcribe_audio

# Set credentials for Google STT
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials/google_stt.json"

# Streamlit UI setup
st.set_page_config(page_title="Speech ⇌ Sign", layout="centered")
st.title("🔊 Speech ⇌ Sign Translator")

# Initialize state variables
if "mode" not in st.session_state:
    st.session_state.mode = None
if "recording" not in st.session_state:
    st.session_state.recording = False
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""
if "audio_path" not in st.session_state:
    st.session_state.audio_path = ""

# UI: Mode selector
mode_selector()

# --- Speech to Sign Mode ---
if st.session_state.mode == "speech":
    st.markdown("---")
    st.success("🚘 Speech to Sign mode activated")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶️ Start Recording") and not st.session_state.recording:
            st.session_state.recording = True
            st.session_state.transcribed_text = ""
            start_recording()

    with col2:
        if st.button("⏹️ Stop and Transcribe") and st.session_state.recording:
            st.session_state.recording = False
            with st.spinner("🧠 Transcribing..."):
                audio_path = stop_recording_and_save()
                if audio_path:
                    st.session_state.audio_path = audio_path
                    transcript = transcribe_audio(audio_path)
                    st.session_state.transcribed_text = transcript or "⚠️ No speech detected."

    if st.session_state.recording:
        st.info("🔴 Recording... Speak now")

    # Show final transcription
    show_transcript()
    st.write("**📝 Raw Transcript Output:**", st.session_state.transcribed_text)

# --- Sign to Speech Placeholder ---
elif st.session_state.mode == "sign":
    st.subheader("🤟 Sign to Speech Mode (Coming Soon)")

# --- Idle Mode ---
else:
    st.info("👆 Please choose a mode above to start.")
