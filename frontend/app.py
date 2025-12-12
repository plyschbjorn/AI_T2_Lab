import streamlit as st
import requests
import sys
import os
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui_components import apply_terminator_style
from backend.constants import BG_IMAGE_PATH, ICON_IMAGE_PATH, FILE_PATH

URL = f"https://t2chatbot.azurewebsites.net/rag/query?code={os.getenv('APP_KEY')}"

# --- APP SETUP ---
st.set_page_config(
    page_title="The T2 Lab",
    page_icon="🦾",
    layout="centered",
    initial_sidebar_state="collapsed"
    )

apply_terminator_style(BG_IMAGE_PATH, ICON_IMAGE_PATH)

st.title("🦾 The T2 Lab")
st.markdown("Chat with me if you want to lôrn about Data Engineering.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Mission Control")
    if st.button("Reset Timeline"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.caption("Mission Data Files:")

    if FILE_PATH.exists():
        for f in sorted(FILE_PATH.glob("*.md")):
            with st.expander(f"📜 {f.stem}"):
                with open(f, "r", encoding="utf-8") as file:
                    st.code(file.read(), language="markdown")
    else:
        st.error(f"Could not find directory: {FILE_PATH}")

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("I need your clothes, your boots, and your query..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Scanning Skynet neural net... "):
            try:
                payload = {
                    "prompt": prompt,
                    "memory": st.session_state.messages
                }

                response = requests.post(URL, json=payload)

                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "Negative. No data recieved")
                    st.markdown(answer)

                    if data.get("sources"):
                        with st.expander("💾 Mission Data Sources"):
                            for source in data["sources"]:
                                st.caption(f"Target: **{source}**")

                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"⚠️ System Error: {response.status_code}")

            except Exception as e:
                st.error(f"Connection terminated: {e}")