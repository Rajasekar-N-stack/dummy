import streamlit as st

def show_transcript():
    st.markdown("### 2️⃣ Transcribed Text")
    st.text_area("Speech Output:", value=st.session_state.get("transcribed_text", ""), height=100)
