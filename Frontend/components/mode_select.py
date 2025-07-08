import streamlit as st

def mode_selector():
    st.markdown("## 🧠 Speech ⇔ Sign Translator")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗣️ Speech to Sign"):
            st.session_state.mode = "speech"
    with col2:
        if st.button("🤟 Sign to Speech"):
            st.session_state.mode = "sign"
