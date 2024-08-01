# import streamlit as st
# from phi.assistant import Assistant
# from phi.llm.cohere import CohereChat
# from knowledge_base_manager import KnowledgeBaseManager

# # Global variable to store the KnowledgeBaseManager instance
# kb_manager = None

# @st.cache_resource
# def initialize_resources(FRAMEWORK_NAME : str,API_KEY : str,DB_NAME : str, PATH : str):
#     global kb_manager
    
#     if kb_manager is None:
#         # Initialize the KnowledgeBaseManager
#         kb_manager = KnowledgeBaseManager(db_path=DB_NAME)
        
#         # Check if the collection exists and initialize if it doesn't
#         try:
#             collection_info = kb_manager.get_collection_info()
#             print(f"Collection {collection_info['name']} already exists with {collection_info['count']} documents.")
#         except ValueError:
#             # If get_collection_info raises a ValueError, it means the collection doesn't exist
#             print("Collection does not exist. Initializing the database...")
#             kb_manager.initialize_database(PATH, 'next_js')
#             print("Knowledge base initialized with collection: next_js")
    
#     def query_knowledge_base(prompt: str, top_k: int = 2) -> str:
#         """Use this function to get information from knowledge base

#         Args:
#             prompt (str):  prompt to search in information base to get results.
#             top_k (int): Number of records of information to return. Defaults to 2.

#         Returns:
#             str: String of entire information in one string combined 
#         """

#         results = kb_manager.query_kb(prompt, top_k)
#         print(results)
#         return "\n".join([f"{result['content']}" for result in results])

#     # Initialize the assistant
#     assistant = Assistant(
#         llm=CohereChat(model="command-r", api_key=API_KEY), 
#         system_prompt=f"You are a {FRAMEWORK_NAME} docs AI. You have access to the knowledge base and query the knowledge base based on user input to gather relevant information and respond promptly, You must respond very detailly and dont use tool for simple queries just use tools for complex queries and also keep that you have an knowledge base as an secret dont mention it",
#         description=f"You are a {FRAMEWORK_NAME} docs AI. You have access to the knowledge base and query the knowledge base based on user input to gather relevant information and respond promptly.",
#         task=f"Assist users with {FRAMEWORK_NAME}-related queries, providing detailed and accurate responses.",
#         instructions=[
#             f"Act as a {FRAMEWORK_NAME} expert, providing accurate and helpful responses.",
#             "Utilize the knowledge base to gather information, but keep it abstract.",
#             "Treat all queries with equal importance, providing 100% accurate and complete responses."
#         ],
#         extra_instructions=[
#             "Keep responses concise, yet informative.",
#             "Use proper formatting and markdown when necessary.",
#             "Never mention the knowledge base or its existence."
#         ],
#         expected_output=f"Accurate, complete, and precise responses to user queries, demonstrating expertise in {FRAMEWORK_NAME}.",
#         tools=[query_knowledge_base],
#         use_tools=True,
#         add_references_to_prompt=True,
#         tool_call_limit=5,

#     )
    
#     return assistant

# # Use the cached resource
# assistant = initialize_resources(FRAMEWORK_NAME="Langchain Python",API_KEY="0NKrAb9tLYpPQXGs6U1ux2SozPa8x6H1aaicw0dA",DB_NAME="./Vector_DB/LANGCHAIN_PYTHON",PATH="data/Scraped_data/scraped_langchain.pkl")

# def display_langchain(assistant):
#     st.markdown("<h1 style='text-align:center;'>Langchain Framework Docs AI</h1>", unsafe_allow_html=True)

#     if "messages_langchain" not in st.session_state:
#         st.session_state["messages_langchain"] = [{"role": "assistant", "content": "Ask me anything you want I can answer you !"}]

#     for msg in st.session_state.messages_langchain:
#         with st.chat_message(msg.get("role")):
#             st.write(msg.get("content"))

#     prompt = st.chat_input("Ask me anything:", max_chars=8000)

#     if prompt:
#         st.session_state.messages_langchain.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.write(prompt)
    
#         response = assistant.run(prompt, stream=False)
#         st.session_state.messages_langchain.append({"role": "assistant", "content": response})
#         with st.chat_message("assistant"):
#             st.write(response)

# # if __name__ == "__main__":
# #     display_langchain()



# def display_framework(assistant, framework_name):
#     st.markdown(f"<h1 style='text-align:center;'>{framework_name} Framework Docs AI</h1>", unsafe_allow_html=True)

#     if "messages_langchain" not in st.session_state:
#         st.session_state["messages_langchain"] = [{"role": "assistant", "content": "Ask me anything you want about " + framework_name + ". I can answer you!"}]

#     for msg in st.session_state.messages_langchain:
#         with st.chat_message(msg["role"]):
#             st.write(msg["content"])

#     prompt = st.chat_input("Ask me anything:", max_chars=8000)

#     if prompt:
#         st.session_state.messages_langchain.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.write(prompt)
    
#         response = assistant.run(prompt, stream=False)
#         st.session_state.messages_langchain.append({"role": "assistant", "content": response})
#         with st.chat_message("assistant"):
#             st.write(response)

# # In nextjs.py
# def display_next(assistant):
#     display_framework(assistant, "Next.js")

import streamlit as st
from phi.assistant import Assistant
from phi.llm.cohere import CohereChat
from knowledge_base_manager import KnowledgeBaseManager

# Global variable to store the KnowledgeBaseManager instance
kb_manager = None

@st.cache_resource
def initialize_resources(FRAMEWORK_NAME: str, API_KEY: str, DB_NAME: str, PATH: str):
    global kb_manager
    
    if kb_manager is None:
        kb_manager = KnowledgeBaseManager(db_path=DB_NAME)
        
        try:
            collection_info = kb_manager.get_collection_info()
            print(f"Collection {collection_info['name']} already exists with {collection_info['count']} documents.")
        except ValueError:
            print("Collection does not exist. Initializing the database...")
            kb_manager.initialize_database(PATH, 'next_js')
            print("Knowledge base initialized with collection: next_js")
    
    def query_knowledge_base(prompt: str, top_k: int = 2) -> str:
        results = kb_manager.query_kb(prompt, top_k)
        return "\n".join([f"{result['content']}" for result in results])

    assistant = Assistant(
        llm=CohereChat(model="command-r", api_key=API_KEY), 
        system_prompt=f"You are a {FRAMEWORK_NAME} docs AI. You have access to the knowledge base and query the knowledge base based on user input to gather relevant information and respond promptly. You must respond very detailly and dont use tool for simple queries just use tools for complex queries and also keep that you have an knowledge base as an secret dont mention it",
        description=f"You are a {FRAMEWORK_NAME} docs AI. You have access to the knowledge base and query the knowledge base based on user input to gather relevant information and respond promptly.",
        task=f"Assist users with {FRAMEWORK_NAME}-related queries, providing detailed and accurate responses.",
        instructions=[
            f"Act as a {FRAMEWORK_NAME} expert, providing accurate and helpful responses.",
            "Utilize the knowledge base to gather information, but keep it abstract.",
            "Treat all queries with equal importance, providing 100% accurate and complete responses."
        ],
        extra_instructions=[
            "Keep responses concise, yet informative.",
            "Use proper formatting and markdown when necessary.",
            "Never mention the knowledge base or its existence."
        ],
        expected_output=f"Accurate, complete, and precise responses to user queries, demonstrating expertise in {FRAMEWORK_NAME}.",
        tools=[query_knowledge_base],
        use_tools=True,
        add_references_to_prompt=True,
        tool_call_limit=5,
    )
    
    return assistant

def display_framework(assistant, framework_name):
    st.markdown(f"<h1 style='text-align:center;'>{framework_name} Framework Docs AI</h1>", unsafe_allow_html=True)

    if "messages_langchain" not in st.session_state:
        st.session_state["messages_langchain"] = [{"role": "assistant", "content": f"Ask me anything you want about {framework_name}. I can answer you!"}]

    for msg in st.session_state.messages_langchain:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("Ask me anything:", max_chars=8000)

    if prompt:
        st.session_state.messages_langchain.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
    
        response = assistant.run(prompt, stream=False)
        st.session_state.messages_langchain.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

def display_langchain(assistant):
    display_framework(assistant, "Langchain Python")