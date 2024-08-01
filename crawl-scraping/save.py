import json
import pickle
from langchain.schema import Document

def convert_json_to_pkl(input_json_file, output_pkl_file):
    # Load JSON data
    with open(input_json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    # Convert JSON data to Document objects
    documents = []
    for item in json_data:
        doc = Document(
            page_content=item.get('page_content', ''),
            metadata=item.get('metadata', {})
        )
        documents.append(doc)
    
    # Save Document objects as a pickle file
    with open(output_pkl_file, 'wb') as f:
        pickle.dump(documents, f)
    
    print(f"Converted {len(documents)} documents and saved to '{output_pkl_file}'")

# Example usage
if __name__ == "__main__":
    convert_json_to_pkl('data/Scraped_data/MDN_WEB_scraped.json', 'data/Scraped_data/MDN_WEB_scraped.pkl')