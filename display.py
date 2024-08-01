import streamlit as st
from phi.assistant import Assistant

def display_framework(assistant: Assistant, framework_name: str):
    st.markdown(f"<h1 style='text-align:center;'>{framework_name} Framework Docs AI</h1>", unsafe_allow_html=True)

    if f"messages_{framework_name.lower().replace('.', '_')}" not in st.session_state:
        st.session_state[f"messages_{framework_name.lower().replace('.', '_')}"] = [{"role": "assistant", "content": f"Ask me anything you want about {framework_name}. I can answer you!"}]

    messages = st.session_state[f"messages_{framework_name.lower().replace('.', '_')}"]

    for msg in messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("Ask me anything:", max_chars=8000)

    if prompt:
        messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
    
        response = assistant.run(prompt, stream=False)
        messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)