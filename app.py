import streamlit as st
import asyncio
import os
from agent import MedicalAgent
from langchain_core.messages import HumanMessage, AIMessage
import time

st.set_page_config(
    page_title="HTU Bioinformatics Lab: Clinical AI",
    page_icon="🏥",
    layout="wide"
)

# --- Sidebar Configuration ---
with st.sidebar:
    st.title("🛠️ Lab Configuration")
    st.info("Clinical AI Assistant Lab - HTU")
    
    groq_key = st.text_input("Groq API Key", type="password", value=os.getenv("GROQ_API_KEY", ""))
    
    st.divider()
    st.subheader("Observability (Langfuse)")
    lf_public = st.text_input("Public Key", value=os.getenv("LANGFUSE_PUBLIC_KEY", ""))
    lf_secret = st.text_input("Secret Key", type="password", value=os.getenv("LANGFUSE_SECRET_KEY", ""))
    lf_host = st.text_input("Host", value="https://cloud.langfuse.com")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- Main App ---
st.title("🏥 Clinical AI Assistant Lab")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about history, drugs, or research..."):
    if not groq_key:
        st.error("Please enter your Groq API Key.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                with st.status("🩺 Processing Clinical Request...", expanded=True) as status:
                    history = []
                    for m in st.session_state.messages[:-1]:
                        if m["role"] == "user":
                            history.append(HumanMessage(content=m["content"]))
                        else:
                            history.append(AIMessage(content=m["content"]))

                    agent = MedicalAgent(
                        groq_api_key=groq_key,
                        langfuse_public_key=lf_public,
                        langfuse_secret_key=lf_secret,
                        langfuse_host=lf_host
                    )
                    
                    response = asyncio.run(agent.run_query(prompt, history))
                    status.update(label="✅ Analysis Complete", state="complete", expanded=False)
                
                if response:
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {str(e)}")

# --- Lab Submission Guide ---
st.markdown("---")
with st.expander("📝 **Submission Requirements**"):
    st.markdown("""
    1. **System Prompts**: Try 3 different versions of your instructions in `agent.py`.
    2. **Langfuse Traces**: Capture screenshots of your thinking traces.
    3. **Word Doc**: Submit your report with images and answers to the README questions.
    """)
