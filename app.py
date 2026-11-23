import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from assistant_core import MAX_HISTORY, run_turn


st.set_page_config(
    page_title="StudyMate",
    page_icon="📚",
    layout="centered",
)

st.title("📚 StudyMate")
st.caption("Your personal AI Study Planner Assistant")

with st.sidebar:
    st.header("Gemini API Key")
    api_key = st.text_input(
        "Enter your Gemini API key",
        type="password",
        help="Enter a Google Gemini API key. It is kept only in this browser session.",
    )
    st.caption("Get your API key from Google AI Studio.")
    st.divider()
    st.subheader("Available Tools")
    st.write("1. Days Until Exam")
    st.write("2. Split Study Hours")
    if st.button("Clear Chat"):
        st.session_state.chat = []
        st.rerun()

if "chat" not in st.session_state:
    st.session_state.chat = []

for message in st.session_state.chat:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            tools_used = message.get("tools", [])
            with st.expander("Tools used"):
                if tools_used:
                    for tool_name in tools_used:
                        st.write("✓", tool_name)
                else:
                    st.write("No tools used.")

user_question = st.chat_input("Ask me about your studies...")

if user_question:
    st.session_state.chat.append({"role": "user", "content": user_question})

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        if not api_key.strip():
            answer = "Please enter your Gemini API key in the sidebar."
            used_tools = []
        else:
            try:
                history = []
                previous_messages = st.session_state.chat[:-1][-MAX_HISTORY:]

                for message in previous_messages:
                    if message["role"] == "user":
                        history.append(HumanMessage(content=message["content"]))
                    elif message["role"] == "assistant":
                        history.append(AIMessage(content=message["content"]))

                with st.spinner("StudyMate is thinking..."):
                    answer, used_tools = run_turn(
                        api_key,
                        history,
                        user_question,
                    )
            except Exception as error:
                answer = (
                    f"Something went wrong: {type(error).__name__}. "
                    "Please check your API key, quota or model availability."
                )
                used_tools = []

        st.markdown(answer)
        with st.expander("Tools used"):
            if used_tools:
                for tool_name in used_tools:
                    st.write("✓", tool_name)
            else:
                st.write("No tools used.")

    st.session_state.chat.append({
        "role": "assistant",
        "content": answer,
        "tools": used_tools,
    })
