import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from trafilatura import fetch_url, extract
from langchain.schema import Document
from bs4 import BeautifulSoup
import requests
import os


#working ✅✅✅✅
def scrape_url(url):
    try:
        downloaded = fetch_url(url)
        if downloaded is None:
            raise Exception("Failed to download the webpage")

        result = extract(downloaded, output_format='json')
        if result is None:
            raise Exception("Failed to extract content")

        content = json.loads(result)

        # Use BeautifulSoup to extract the title
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else ''

        # Create a dictionary instead of a Document object
        doc = {
            "page_content": content.get('text', ''),
            "metadata": {
                "source": url,
                "title": title
            }
        }
        print(f"Extracted title for {url}: {title}")  # Debug print
        return doc
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None

def read_urls_from_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return [item['url'] for item in data]


def save_documents(filename, documents):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)

def load_documents(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [Document(**doc) for doc in data]

def Scrape(filepath,savefile):
    urls = read_urls_from_file(filepath)
    documents = []
    total_urls = len(urls)

    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_url = {executor.submit(scrape_url, url): url for url in urls}
        for i, future in enumerate(tqdm(as_completed(future_to_url), total=total_urls)):
            doc = future.result()
            if doc:
                documents.append(doc)

            if (i + 1) % (total_urls // 10) == 0:
                print(f"{(i + 1) / total_urls * 100:.0f}% completed")
                # Save intermediate results
                # save_documents(f'scraped_pytorch_docs_intermediate_{i+1}.json', documents)

    # Save final results
    save_documents(savefile, documents)
    print(f"Scraped {len(documents)} URLs. Data saved to 'scraped_pytorch_docs.json'")

if __name__ == "__main__":
    Scrape("data/Crawled_url/MDN_WEB_crawled.json", "data/Scraped_data/MDN_WEB_scraped.json")