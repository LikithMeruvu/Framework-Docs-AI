# import os
# import json
# import time
# from typing import List
# from sentence_transformers import SentenceTransformer
# import numpy as np
# from groq import Groq
# from dotenv import load_dotenv
# from langchain.schema import Document

# # Load environment variables
# load_dotenv()

# ABOUT = "LANGCHAIN FRAMEWORK"

# # Initialize Groq client
# client = Groq(api_key="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") # type: ignore

# model = 'llama3-70b-8192'

# # Load documents
# def load_documents(filename: str) -> List[Document]:
#     documents = []
#     try:
#         with open(filename, 'r', encoding='utf-8') as f:
#             data = json.load(f)
#         for item in data:
#             doc = Document(
#                 page_content=item.get('page_content', ''),
#                 metadata=item.get('metadata', {})
#             )
#             documents.append(doc)
#     except Exception as e:
#         print(f"Error loading documents: {e}")
#         raise
#     return documents

# # Initialize SentenceTransformer model
# sentence_model = SentenceTransformer("Alibaba-NLP/gte-base-en-v1.5", trust_remote_code=True)

# # Load the documents
# try:
#     documents = load_documents('data/Scraped_data/scraped_langchain_docs.json')
# except Exception as e:
#     print(f"Failed to load documents: {e}")
#     exit(1)

# # Extract titles and content
# titles = [doc.metadata.get('title', '') for doc in documents]
# contents = [doc.page_content for doc in documents]

# # Encode titles
# title_embeddings = sentence_model.encode(titles, normalize_embeddings=True)

# def title_based_retrieval(prompt: str) -> dict:
#     """Retrieves information from the knowledge base based on query"""
#     prompt_embedding = sentence_model.encode(prompt, normalize_embeddings=True)
#     similarities = np.dot(title_embeddings, prompt_embedding)
#     top_2_idx = np.argsort(similarities)[-2:][::-1]
#     combined_content = " ".join([contents[idx] for idx in top_2_idx])
#     retrieved_titles = [titles[idx] for idx in top_2_idx]
#     print(f"the results : {retrieved_titles} \n 👇 \n  {combined_content}")
#     return {"content": combined_content, "titles": retrieved_titles}

# # Define tools
# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "title_based_retrieval",
#             "description": "Retrieves information from the knowledge base",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "prompt": {
#                         "type": "string",
#                         "description": "Search query for Knowledge base",
#                     }
#                 },
#                 "required": ["prompt"],
#             },
#         },
#     }
# ]

# def process_query(query: str, max_retries=2, initial_wait=1):
#     messages = [
#         {"role": "system", "content": f"You are a helpful assistant with access to a knowledge base about {ABOUT}. Use the retrieval function to answer questions. Dont mention that you are having knowledge base or according to this function call or my knowledge base keep it abstract"},
#         {"role": "user", "content": query},
#     ]

#     for attempt in range(max_retries):
#         try:
#             # Make initial API call
#             response = client.chat.completions.create(
#                 model=model, messages=messages, tools=tools, tool_choice="auto", max_tokens=8192
#             )

#             response_message = response.choices[0].message

#             # Check if tool was used
#             tool_calls = response_message.tool_calls or []
#             tool_used = len(tool_calls) > 0

#             retrieved_titles = []
#             if tool_used:
#                 messages.append(
#                     {
#                         "role": "assistant",
#                         "content": response_message.content,
#                         "tool_calls": [
#                             {
#                                 "id": tool_call.id,
#                                 "function": {
#                                     "name": tool_call.function.name,
#                                     "arguments": tool_call.function.arguments,
#                                 },
#                                 "type": tool_call.type,
#                             }
#                             for tool_call in tool_calls
#                         ],
#                     }
#                 )

#                 available_functions = {
#                     "title_based_retrieval": title_based_retrieval,
#                 }

#                 for tool_call in tool_calls:
#                     function_name = tool_call.function.name
#                     function_to_call = available_functions[function_name]
#                     function_args = json.loads(tool_call.function.arguments)
#                     function_response = function_to_call(**function_args)

#                     messages.append(
#                         {
#                             "role": "tool",
#                             "content": json.dumps(function_response["content"]),
#                             "tool_call_id": tool_call.id,
#                         }
#                     )
#                     retrieved_titles.extend(function_response["titles"])

#                 # Make final API call
#                 final_response = client.chat.completions.create(
#                     model=model, messages=messages, tools=tools, tool_choice="auto", max_tokens=8192
#                 )
#                 final_content = final_response.choices[0].message.content
#             else:
#                 final_content = response_message.content

#             return tool_used, retrieved_titles, final_content

#         except Exception as e:
#             if attempt < max_retries - 1:
#                 wait_time = initial_wait * (2 ** attempt)
#                 print(f"Error occurred: {e}. Retrying in {wait_time} seconds...")
#                 time.sleep(wait_time)
#             else:
#                 print(f"Error processing query after {max_retries} attempts: {e}")
#                 return False, [], "Sorry, an error occurred while processing your query."

# def main():
#     print(f"Welcome to the {ABOUT} Q&A system. Type 'exit' to quit.")
#     while True:
#         query = input("\nEnter your question: ")
#         if query.lower() == 'exit':
#             print(f"Thank you for using the {ABOUT} Q&A system. Goodbye!")
#             break

#         tool_used, retrieved_titles, response = process_query(query)

#         print(f"\nTool used: {tool_used}")
#         if tool_used:
#             print("Retrieved information titles:")
#             for title in retrieved_titles:
#                 print(f"- {title}")
#         print(f"\nResponse: {response}")

# if __name__ == "__main__":
#     main()



# 🥲👇👇👇👇

# import os
# import json
# import time
# from typing import List, Tuple
# from sentence_transformers import SentenceTransformer
# import numpy as np
# from groq import Groq
# from dotenv import load_dotenv
# from langchain.schema import Document

# # Load environment variables
# load_dotenv()

# ABOUT = "LANGCHAIN FRAMEWORK"

# # Initialize Groq client
# client = Groq(api_key="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") # type: ignore
# model = 'llama3-70b-8192'

# # Load documents
# def load_documents(filename: str) -> List[Document]:
#     documents = []
#     try:
#         with open(filename, 'r', encoding='utf-8') as f:
#             data = json.load(f)
#         for item in data:
#             doc = Document(
#                 page_content=item.get('page_content', ''),
#                 metadata=item.get('metadata', {})
#             )
#             documents.append(doc)
#     except Exception as e:
#         print(f"Error loading documents: {e}")
#         raise
#     return documents

# # Initialize SentenceTransformer model
# sentence_model = SentenceTransformer("Alibaba-NLP/gte-base-en-v1.5", trust_remote_code=True)

# # Load the documents
# try:
#     documents = load_documents('data/Scraped_data/scraped_langchain_docs.json')
# except Exception as e:
#     print(f"Failed to load documents: {e}")
#     exit(1)

# # Extract titles and content
# titles = [doc.metadata.get('title', '') for doc in documents]
# contents = [doc.page_content for doc in documents]

# # Encode titles and contents
# title_embeddings = sentence_model.encode(titles, normalize_embeddings=True)
# content_embeddings = sentence_model.encode(contents, normalize_embeddings=True)

# def combined_retrieval(prompt: str, top_k: int = 3, title_weight: float = 0.5) -> List[Tuple[str, str, float]]:
#     # Encode the prompt
#     prompt_embedding = sentence_model.encode(prompt, normalize_embeddings=True)
#     # Calculate similarities for titles and contents
#     title_similarities = np.dot(title_embeddings, prompt_embedding)
#     content_similarities = np.dot(content_embeddings, prompt_embedding)
#     # Combine similarities with weighting
#     combined_similarities = title_weight * title_similarities + (1 - title_weight) * content_similarities
#     # Get top k similar documents
#     top_k_idx = np.argsort(combined_similarities)[-top_k:][::-1]
#     # Prepare results
#     results = []
#     for idx in top_k_idx:
#         title = titles[idx]
#         content = contents[idx]
#         similarity = combined_similarities[idx]
#         results.append((title, content, float(similarity)))
#     return results

# def knowledge_base_retrieval(prompt: str) -> dict:
#     """Retrieves information from the knowledge base based on query"""
#     results = combined_retrieval(prompt, top_k=2, title_weight=0.5)
#     combined_content = " ".join([content for _, content, _ in results])
#     retrieved_titles = [title for title, _, _ in results]
#     print(f"Retrieved titles: {retrieved_titles} \n 👇 \n  {combined_content[:200]}...")
#     return {"content": combined_content, "titles": retrieved_titles}

# # Define tools
# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "knowledge_base_retrieval",
#             "description": "Retrieves information from the knowledge base",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "prompt": {
#                         "type": "string",
#                         "description": "Search query for Knowledge base",
#                     }
#                 },
#                 "required": ["prompt"],
#             },
#         },
#     }
# ]

# def process_query(query: str, max_retries=2, initial_wait=1):
#     messages = [
#         {"role": "system", "content": f"You are a helpful assistant with access to a knowledge base about {ABOUT}. Use the retrieval function to answer questions. Don't mention that you are having a knowledge base or according to this function call or my knowledge base; keep it abstract."},
#         {"role": "user", "content": query},
#     ]

#     for attempt in range(max_retries):
#         try:
#             # Make initial API call
#             response = client.chat.completions.create(
#                 model=model, messages=messages, tools=tools, tool_choice="auto", max_tokens=8192
#             )

#             response_message = response.choices[0].message

#             # Check if tool was used
#             tool_calls = response_message.tool_calls or []
#             tool_used = len(tool_calls) > 0

#             retrieved_titles = []
#             if tool_used:
#                 messages.append(
#                     {
#                         "role": "assistant",
#                         "content": response_message.content,
#                         "tool_calls": [
#                             {
#                                 "id": tool_call.id,
#                                 "function": {
#                                     "name": tool_call.function.name,
#                                     "arguments": tool_call.function.arguments,
#                                 },
#                                 "type": tool_call.type,
#                             }
#                             for tool_call in tool_calls
#                         ],
#                     }
#                 )

#                 available_functions = {
#                     "knowledge_base_retrieval": knowledge_base_retrieval,
#                 }

#                 for tool_call in tool_calls:
#                     function_name = tool_call.function.name
#                     function_to_call = available_functions[function_name]
#                     function_args = json.loads(tool_call.function.arguments)
#                     function_response = function_to_call(**function_args)

#                     messages.append(
#                         {
#                             "role": "tool",
#                             "content": json.dumps(function_response["content"]),
#                             "tool_call_id": tool_call.id,
#                         }
#                     )
#                     retrieved_titles.extend(function_response["titles"])

#                 # Make final API call
#                 final_response = client.chat.completions.create(
#                     model=model, messages=messages, tools=tools, tool_choice="auto", max_tokens=8192
#                 )
#                 final_content = final_response.choices[0].message.content
#             else:
#                 final_content = response_message.content

#             return tool_used, retrieved_titles, final_content

#         except Exception as e:
#             if attempt < max_retries - 1:
#                 wait_time = initial_wait * (2 ** attempt)
#                 print(f"Error occurred: {e}. Retrying in {wait_time} seconds...")
#                 time.sleep(wait_time)
#             else:
#                 print(f"Error processing query after {max_retries} attempts: {e}")
#                 return False, [], "Sorry, an error occurred while processing your query."

# def main():
#     print(f"Welcome to the {ABOUT} Q&A system. Type 'exit' to quit.")
#     while True:
#         query = input("\nEnter your question: ")
#         if query.lower() == 'exit':
#             print(f"Thank you for using the {ABOUT} Q&A system. Goodbye!")
#             break

#         tool_used, retrieved_titles, response = process_query(query)

#         print(f"\nTool used: {tool_used}")
#         if tool_used:
#             print("Retrieved information titles:")
#             for title in retrieved_titles:
#                 print(f"- {title}")
#         print(f"\nResponse: {response}")

# if __name__ == "__main__":
#     main()




# 💀💀💀💀

import os
import pickle
import json
import time
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np
from groq import Groq
from dotenv import load_dotenv
from langchain.schema import Document

# Load environment variables
load_dotenv()

ABOUT = "LANGCHAIN FRAMEWORK"

# Initialize Groq client
client = Groq(api_key="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")
model = 'mixtral-8x7b-32768'

def load_documents(filename: str) -> List[Document]:
    documents = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for item in data:
            doc = Document(
                page_content=item.get('page_content', ''),
                metadata=item.get('metadata', {})
            )
            documents.append(doc)
    except Exception as e:
        print(f"Error loading documents: {e}")
        raise
    return documents

def load_documents_pkl(filename: str) -> List:
    with open(filename, 'rb') as f:
        documents = pickle.load(f)
    return documents

# Initialize SentenceTransformer model
sentence_model = SentenceTransformer("Alibaba-NLP/gte-base-en-v1.5", trust_remote_code=True)

# Load the documents
try:
    documents = load_documents_pkl('data/Scraped_data/scraped_nextjs.pkl')
except Exception as e:
    print(f"Failed to load documents: {e}")
    exit(1)

# Extract titles and content
titles = [doc.metadata.get('title', '') for doc in documents]
full_contents = [doc.page_content for doc in documents]

def get_first_100_words(text: str) -> str:
    words = text.split()
    return ' '.join(words[:100])

# Get truncated contents for embedding
truncated_contents = [get_first_100_words(content) for content in full_contents]

def batch_encode(texts: List[str], batch_size: int = 32) -> np.ndarray:
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        batch_embeddings = sentence_model.encode(batch, normalize_embeddings=True)
        embeddings.append(batch_embeddings)
    return np.vstack(embeddings)

# Encode titles and truncated contents in batches
print("Encoding titles...")
title_embeddings = batch_encode(titles)
print("Encoding contents...")
content_embeddings = batch_encode(truncated_contents)

def combined_retrieval(prompt: str, top_k: int = 1, title_weight: float = 0.5) -> List[Tuple[str, str, float]]:
    prompt_embedding = sentence_model.encode([prompt], normalize_embeddings=True)[0]
    title_similarities = np.dot(title_embeddings, prompt_embedding)
    content_similarities = np.dot(content_embeddings, prompt_embedding)
    combined_similarities = title_weight * title_similarities + (1 - title_weight) * content_similarities
    top_k_idx = np.argsort(combined_similarities)[-top_k:][::-1]
    results = []
    for idx in top_k_idx:
        title = titles[idx]
        content = full_contents[idx]  # Use full content for retrieval
        similarity = combined_similarities[idx]
        results.append((title, content, float(similarity)))
    return results

def knowledge_base_retrieval(prompt: str) -> dict:
    results = combined_retrieval(prompt, top_k=2, title_weight=0.5)
    combined_content = " ".join([content for _, content, _ in results])
    retrieved_titles = [title for title, _, _ in results]
    print(f"Retrieved titles: {retrieved_titles} \n 👇 \n  {combined_content[:200]}...")
    return {"content": combined_content, "titles": retrieved_titles}

# Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "knowledge_base_retrieval",
            "description": "Retrieves information from the knowledge base",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Search query for Knowledge base",
                    }
                },
                "required": ["prompt"],
            },
        },
    }
]

def process_query(query: str, max_retries=2, initial_wait=1):
    messages = [
        {"role": "system", "content": f"You are a helpful assistant with access to a knowledge base about {ABOUT}. Use the retrieval function to answer questions. Don't mention that you are having a knowledge base or according to this function call or my knowledge base; keep it abstract."},
        {"role": "user", "content": query},
    ]

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model, messages=messages, tools=tools, tool_choice="auto", max_tokens=8192
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls or []
            tool_used = len(tool_calls) > 0

            retrieved_titles = []
            if tool_used:
                messages.append(
                    {
                        "role": "assistant",
                        "content": response_message.content,
                        "tool_calls": [
                            {
                                "id": tool_call.id,
                                "function": {
                                    "name": tool_call.function.name,
                                    "arguments": tool_call.function.arguments,
                                },
                                "type": tool_call.type,
                            }
                            for tool_call in tool_calls
                        ],
                    }
                )

                available_functions = {
                    "knowledge_base_retrieval": knowledge_base_retrieval,
                }

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = available_functions[function_name]
                    function_args = json.loads(tool_call.function.arguments)
                    function_response = function_to_call(**function_args)

                    messages.append(
                        {
                            "role": "tool",
                            "content": json.dumps(function_response["content"]),
                            "tool_call_id": tool_call.id,
                        }
                    )
                    retrieved_titles.extend(function_response["titles"])

                final_response = client.chat.completions.create(
                    model=model, messages=messages, tools=tools, tool_choice="auto", max_tokens=8192
                )
                final_content = final_response.choices[0].message.content
            else:
                final_content = response_message.content

            return tool_used, retrieved_titles, final_content

        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = initial_wait * (2 ** attempt)
                print(f"Error occurred: {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Error processing query after {max_retries} attempts: {e}")
                return False, [], "Sorry, an error occurred while processing your query."

def main():
    print(f"Welcome to the {ABOUT} Q&A system. Type 'exit' to quit.")
    while True:
        query = input("\nEnter your question: ")
        if query.lower() == 'exit':
            print(f"Thank you for using the {ABOUT} Q&A system. Goodbye!")
            break

        tool_used, retrieved_titles, response = process_query(query)

        print(f"\nTool used: {tool_used}")
        if tool_used:
            print("Retrieved information titles:")
            for title in retrieved_titles:
                print(f"- {title}")
        print(f"\nResponse: {response}")

if __name__ == "__main__":
    main()