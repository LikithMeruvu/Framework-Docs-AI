# import pickle
# import chromadb
# from chromadb.utils import embedding_functions
# from sentence_transformers import SentenceTransformer
# from typing import List, Dict, Any
# import os
# import shutil

# class KnowledgeBaseManager:
#     def __init__(self, db_path: str = "./chroma_db"):
#         self.db_path = db_path
#         self.client = None
#         self.model = SentenceTransformer("all-MiniLM-L6-v2")
#         self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
#         self.collection = None

#     def load_documents(self, filename: str) -> List:
#         if not os.path.exists(filename):
#             raise FileNotFoundError(f"The file {filename} does not exist.")
#         with open(filename, 'rb') as f:
#             return pickle.load(f)
        
    

#     def initialize_database(self, filename: str, collection_name: str):
#         # Attempt to remove the entire database directory
#         try:
#             shutil.rmtree(self.db_path)
#             print(f"Deleted existing database directory: {self.db_path}")
#         except Exception as e:
#             print(f"Error deleting database directory: {e}")

#         # Reinitialize the client
#         self.client = chromadb.PersistentClient(path=self.db_path)

#         documents = self.load_documents(filename)
        
#         # Create a new collection
#         self.collection = self.client.create_collection(name=collection_name, embedding_function=self.embedding_function)
        
#         # Batch add documents for better performance
#         batch_size = 1000
#         for i in range(0, len(documents), batch_size):
#             batch = documents[i:i+batch_size]
#             self.collection.add(
#                 documents=[doc.page_content for doc in batch],
#                 metadatas=[{"title": doc.metadata.get('title', '')} for doc in batch],
#                 ids=[f"doc_{j}" for j in range(i, i+len(batch))]
#             )
#         print(f"Initialized database with {len(documents)} documents from {filename}")

#     def query_kb(self, prompt: str, top_k: int = 3) -> List[Dict[str, Any]]:
#         if not self.collection:
#             raise ValueError("Database not initialized. Please initialize a database first.")

#         results = self.collection.query(
#             query_texts=[prompt],
#             n_results=top_k
#         )

#         retrieved_results = []
#         for i in range(len(results['ids'][0])):
#             doc_id = results['ids'][0][i]
#             content = results['documents'][0][i]
#             metadata = results['metadatas'][0][i]
#             title = metadata['title']
#             similarity = 1 - results['distances'][0][i]  # Convert distance to similarity
#             retrieved_results.append({
#                 "id": doc_id,
#                 "title": title,
#                 "content": content,
#                 "similarity": round(similarity, 4)
#             })

#         return retrieved_results

#     def get_collection_info(self) -> Dict[str, Any]:
#         if not self.collection:
#             raise ValueError("Database not initialized. Please initialize a database first.")
#         return {
#             "name": self.collection.name,
#             "count": self.collection.count()
#         }
    

# # if __name__ == "__main__":
# #     # Create an instance of the KnowledgeBaseManager
# #     kb_manager = KnowledgeBaseManager()

# #     # Load documents from a file (replace with your own file path)
# #     filename = "data/Scraped_data/scraped_nextjs.pkl"
# #     collection_name = "next_js"

# #     # Initialize the database
# #     kb_manager.initialize_database(filename, collection_name)

# #     # Query the knowledge base
# #     prompt = "What is rendering and routing"
# #     top_k = 2 
# #     results = kb_manager.query_knowledge_base(prompt, top_k)

# #     # Print the results
# #     print("Results:")
# #     for result in results:
# #         print(f"Title: {result['title']}")
# #         print(f"Content: {result['content'][:200]}...")
# #         print(f"Similarity: {result['similarity']:.4f}")
# #         print()

# #     # Get collection info
# #     collection_info = kb_manager.get_collection_info()
# #     print("Collection Info:")
# #     print(f"Name: {collection_info['name']}")
# #     print(f"Count: {collection_info['count']}")











import os
import shutil
import pickle
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

class KnowledgeBaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.client = None
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.collection = None

    def load_documents(self, filename: str) -> List:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"The file {filename} does not exist.")
        with open(filename, 'rb') as f:
            return pickle.load(f)

    def initialize_database(self, filename: str, collection_name: str):
        if self.client is None:
            self.client = chromadb.PersistentClient(path=self.db_path)

        # Check if collection already exists
        existing_collections = self.client.list_collections()
        if any(col.name == collection_name for col in existing_collections):
            print(f"Collection {collection_name} already exists. Skipping initialization.")
            self.collection = self.client.get_collection(name=collection_name, embedding_function=self.embedding_function)
            return

        documents = self.load_documents(filename)
        
        # Create a new collection
        self.collection = self.client.create_collection(name=collection_name, embedding_function=self.embedding_function)
        
        # Batch add documents for better performance
        batch_size = 1000
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            self.collection.add(
                documents=[doc.page_content for doc in batch],
                metadatas=[{"title": doc.metadata.get('title', '')} for doc in batch],
                ids=[f"doc_{j}" for j in range(i, i+len(batch))]
            )
        print(f"Initialized database with {len(documents)} documents from {filename}")

    def query_kb(self, prompt: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Use this function to get information from knowledge base

        Args:
            prompt (str):  prompt to search in information base to get results.
            top_k (int): Number of records of information to return. Defaults to 3.

        Returns:
            str: String of entire information in one string combined 
        """

        if not self.collection:
            raise ValueError("Database not initialized. Please initialize a database first.")

        results = self.collection.query(
            query_texts=[prompt],
            n_results=top_k
        )

        retrieved_results = []
        for i in range(len(results['ids'][0])):
            doc_id = results['ids'][0][i]
            content = results['documents'][0][i]
            metadata = results['metadatas'][0][i]
            title = metadata['title']
            similarity = 1 - results['distances'][0][i]  # Convert distance to similarity
            retrieved_results.append({
                "id": doc_id,
                "title": title,
                "content": content,
                "similarity": round(similarity, 4)
            })

        return retrieved_results

    def get_collection_info(self) -> Dict[str, Any]:
        if not self.collection:
            raise ValueError("Database not initialized. Please initialize a database first.")
        return {
            "name": self.collection.name,
            "count": self.collection.count()
        }