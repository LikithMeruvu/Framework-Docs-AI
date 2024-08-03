import streamlit as st
from streamlit_option_menu import option_menu
from phi.assistant import Assistant
# from phi.llm.cohere import CohereChat
from phi.llm.openai import OpenAIChat
from knowledge_base_manager import KnowledgeBaseManager
import os

# # Import the display functions
# from STREAMLIT_UI.langchain import display_langchain
# from STREAMLIT_UI.nextjs import display_next

from display import display_framework

@st.cache_resource
def initialize_kb(framework_name, db_name, path):
    collection_name = framework_name.lower().replace(" ", "_").replace(".", "_")
    kb_manager = KnowledgeBaseManager(db_path=db_name)
    
    try:
        kb_manager.initialize_database(path, collection_name)
        collection_info = kb_manager.get_collection_info()
        print(f"Collection {collection_info['name']} initialized with {collection_info['count']} documents.")
    except Exception as e:
        st.error(f"Error initializing knowledge base for {framework_name}: {str(e)}")
        return None
    
    return kb_manager

def create_assistant(framework_name, api_key, kb_manager):
    def query_knowledge_base(prompt: str, top_k: int = 2) -> str:
        """Use this function to get information from knowledge base

        Args:
            prompt (str):  prompt to search in information base to get results.
            top_k (int): Number of records of information to return. Defaults to 2.

        Returns:
            str: String of entire information in one string combined 
        """
        results = kb_manager.query_kb(prompt, top_k)
        return "\n".join([f"{result['content']}" for result in results])

    return Assistant(
        llm=OpenAIChat(model="gpt-4o-mini", temperature=0.1,api_key=api_key),
        system_prompt=f"You are a {framework_name} docs AI. You have access to a knowledge base and query it based on user input to gather relevant information and respond promptly. Respond in detail and use tools for complex queries. Do not mention the existence of the knowledge base.",
        description=f"You are a {framework_name} docs AI with access to a comprehensive knowledge base.",
        task=f"Assist users with {framework_name}-related queries, providing detailed and accurate responses.",
        instructions=[
            f"Act as a {framework_name} expert, providing accurate and helpful responses.",
            "Utilize the knowledge base to gather information, but keep it abstract.",
            "Treat all queries with equal importance, providing 100% accurate and complete responses."
        ],
        extra_instructions=[
            "Keep responses concise, yet informative.",
            "Use proper formatting and markdown when necessary.",
            "Never mention the knowledge base or its existence."
        ],
        expected_output=f"Accurate, complete, and precise responses to user queries, demonstrating expertise in {framework_name}.",
        tools=[query_knowledge_base],
        use_tools=True,
        add_references_to_prompt=True,
        tool_call_limit=5,
    )

# Initialize knowledge bases
kb_manager_nextjs = initialize_kb("Next.js", "./Vector_DB/next_js", "data/Scraped_data/scraped_nextjs.pkl")
kb_manager_langchain = initialize_kb("Langchain Python", "./Vector_DB/LANGCHAIN_PYTHON", "data/Scraped_data/scraped_langchain.pkl")
kb_manager_Vuejs = initialize_kb("Vue.js", "./Vector_DB/Vue_js", "data/Scraped_data/Vue_scraped.pkl")
kb_manager_Pytorch = initialize_kb("Pytorch", "./Vector_DB/Pytorch", "data/Scraped_data/Pytorch_scraped.pkl")
kb_manager_MDN = initialize_kb("MDN web developer Docs", "./Vector_DB/MDN", "data/Scraped_data/MDN_WEB_scraped.pkl")
kb_manager_Chainlit = initialize_kb("Chainlit", "./Vector_DB/Chainlit", "data/Scraped_data/Chainlit_scraped.pkl")

# Create assistants
api_key = os.environ['OPENAI_API_kEY']


assistant_nextjs = create_assistant("Next.js", api_key, kb_manager_nextjs) if kb_manager_nextjs else None
assistant_langchain = create_assistant("Langchain Python", api_key, kb_manager_langchain) if kb_manager_langchain else None
assistant_Vuejs = create_assistant("Vue.js", api_key, kb_manager_Vuejs) if kb_manager_Vuejs else None
assistant_Pytorch = create_assistant("Pytorch", api_key, kb_manager_Pytorch) if kb_manager_Pytorch else None
assistant_MDN = create_assistant("MDN WEB docs", api_key, kb_manager_MDN) if kb_manager_MDN else None
assistant_Chainlit = create_assistant("Chainlit", api_key, kb_manager_Chainlit) if kb_manager_Chainlit else None

# Define the sidebar
with st.sidebar:
    selected = option_menu(
        menu_title="Framework Docs AI",
        options=["Langchain Python", "Next.js","Vue.js","MDN_WEB","Pytorch","Chainlit"],
        icons=["box", "box","box","box","box","box"],
        menu_icon="boxes",
        default_index=0
    )

if selected == "Langchain Python" and assistant_langchain:
    # display_langchain(assistant_langchain)
    display_framework(assistant_langchain,"Langchain Python")

elif selected == "Next.js" and assistant_nextjs:
    # display_next(assistant_nextjs)
    display_framework(assistant_nextjs,"Next.js")

elif selected == "Vue.js" and assistant_nextjs:
    # display_next(assistant_nextjs)
    display_framework(assistant_Vuejs,"Vue.js")

elif selected == "MDN_WEB" and assistant_nextjs:
    # display_next(assistant_nextjs)
    display_framework(assistant_MDN,"MDN_WEB")

elif selected == "Pytorch" and assistant_nextjs:
    # display_next(assistant_nextjs)
    display_framework(assistant_Pytorch,"Pytorch")

elif selected == "Chainlit" and assistant_nextjs:
    # display_next(assistant_nextjs)
    display_framework(assistant_Chainlit,"Chainlit")

elif selected in ["Langchain Python", "Next.js","Vue.js","MDN_WEB","Pytorch","Chainlit"]:
    st.error(f"The assistant for {selected} could not be initialized. Please check the logs for more information.")