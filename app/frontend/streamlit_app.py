# frontend/app.py

import sys
from pathlib import Path

# Ensure project root is on sys.path so absolute imports like `app` work when
# this file is run directly by Streamlit (which sets the script dir on sys.path).
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st
from app.frontend.base_llm import generate_llm_response

from app.frontend.optimizer_api import optimize_raw_prompt

st.set_page_config("Prompt Optimizer AI", layout="wide")
st.title("🤖 Live AI → Prompt Optimizer")

# ---- Session state ----
if "chat_response" not in st.session_state:
    st.session_state.chat_response = None

# ---- Chat input ----
user_input = st.text_area(
    "Ask anything (ChatGPT / Gemini style)",
    height=150,
    placeholder="Explain Artificial Intelligence simply"
)

# ---- Generate AI response ----
if st.button("💬 Ask AI"):
    if not user_input.strip():
        st.warning("Please type something")
    else:
        with st.spinner("AI is thinking..."):
            st.session_state.chat_response = generate_llm_response(user_input)

# ---- Display AI response ----
if st.session_state.chat_response:
    st.subheader("🧠 AI Response (Captured Automatically)")
    st.code(st.session_state.chat_response, language="text")

    # ---- Optimize button ----
    if st.button("🚀 Optimize This Prompt"):
        with st.spinner("Optimizing..."):
            result = optimize_raw_prompt(st.session_state.chat_response)

        st.success("Optimized prompts generated")

        st.subheader("✨ Optimized Prompts")
        for p in result["optimized_prompts"]:
            st.markdown(f"**Version {p['version']}**")
            st.code(p["prompt"], language="text")
