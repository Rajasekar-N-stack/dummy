import streamlit as st
from services import recorder, STT

def show_mic_buttons():
    # ✅ Initialize session_state keys safely
    if "recording" not in st.session_state:
        st.session_state.recording = False
    if "audio_buffer" not in st.session_state:
        st.session_state.audio_buffer = []
    if "transcript" not in st.session_state:
        st.session_state.transcript = ""

    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶️ Start Recording"):
            st.session_state.audio_buffer = recorder.start_recording()
            st.session_state.recording = True
            st.session_state.transcript = ""

    with col2:
        if st.button("⏹️ Stop Recording") and st.session_state.recording:
            audio_path = recorder.stop_and_save(st.session_state.audio_buffer)
            st.session_state.recording = False
            st.success("✅ Recording saved. Transcribing...")
            st.session_state.transcript = STT.transcribe_audio(audio_path)

    if st.session_state.recording:
        st.info("🎙️ Recording... Speak now!")

    return st.session_state.get("transcript", "")
