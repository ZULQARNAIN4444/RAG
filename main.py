import os
import streamlit as st
from doc_chat_utility import get_answer

working_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Document Q&A - Mistral - Ollama",
    page_icon="📄",
    layout="centered",
)

st.title("Document Q&A - Mistral - Ollama")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

# Upload multiple files
uploaded_files = st.file_uploader(
    label="Upload one or more PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

# --- Display Chat History in Reverse Order ---
if st.session_state.chat_history:
    st.subheader("Chat History (Latest on Top)")
    for q, a in reversed(st.session_state.chat_history):
        st.markdown(f"**You:** {q}")
        st.markdown(f"**Answer:** {a}")
        st.markdown("---")

# --- Query Input Section (Bottom) ---

st.markdown("### Ask a Question")

# Clear input if flagged
query_default = "" if st.session_state.clear_input else st.session_state.get("query_input", "")
user_query = st.text_input("Your query", key="query_input", value=query_default)

# Process question
if st.button("Run"):
    if uploaded_files and user_query.strip() != "":
        # Save uploaded files
        saved_paths = []
        for file in uploaded_files:
            file_path = os.path.join(working_dir, file.name)
            with open(file_path, "wb") as f:
                f.write(file.read())
            saved_paths.append(file_path)

        # Get answer
        answer = get_answer(saved_paths, user_query)

        # Store in chat history immediately (so it's visible in same run)
        st.session_state.chat_history.append((user_query, answer))

        # Clear input for next question
        st.session_state.clear_input = True
    else:
        st.warning("Please upload at least one file and enter a query.")
else:
    st.session_state.clear_input = False
