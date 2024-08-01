import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import xml.etree.ElementTree as ET

class DomainCrawler:
    def __init__(self, start_url, docs_path, avoid_keywords=None):
        self.start_url = start_url
        self.base_domain = urlparse(start_url).netloc
        self.docs_path = docs_path
        self.crawled_urls = []
        self.to_visit = set()
        self.avoid_keywords = avoid_keywords or []
        self.sitemap_urls = self.get_urls_from_sitemap()

        # If no URLs found in sitemap, start with the docs_path
        if not self.to_visit:
            self.to_visit.add(urljoin(self.start_url, self.docs_path))

    def get_urls_from_sitemap(self):
        sitemap_urls = set()
        try:
            sitemap_url = urljoin(self.start_url, '/sitemap.xml')
            response = requests.get(sitemap_url, timeout=10)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                for loc in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                    url = loc.text
                    defragged_url, _ = urldefrag(url)
                    if self.is_valid_url(defragged_url):
                        sitemap_urls.add(defragged_url)
                        self.to_visit.add(defragged_url)
            print(f"Found {len(sitemap_urls)} URLs in sitemap")
        except Exception as e:
            print(f"Error fetching sitemap: {str(e)}")
            print("Falling back to crawling from the docs path.")
        return sitemap_urls

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return (bool(parsed.netloc) and
                bool(parsed.scheme) and
                parsed.netloc == self.base_domain and
                url.startswith(urljoin(self.start_url, self.docs_path)) and
                not any(keyword in url for keyword in self.avoid_keywords))

    def crawl_url(self, url):
        defragged_url, _ = urldefrag(url)
        if defragged_url in self.crawled_urls:
            return None

        try:
            response = requests.get(defragged_url, timeout=10)
            if response.status_code == 200 and 'text/html' in response.headers.get('Content-Type', ''):
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    full_url = urljoin(defragged_url, link['href'])
                    defragged_full_url, _ = urldefrag(full_url)
                    if self.is_valid_url(defragged_full_url) and defragged_full_url not in self.crawled_urls and defragged_full_url not in self.to_visit:
                        self.to_visit.add(defragged_full_url)
                print(f"Crawled: {defragged_url}")
                return defragged_url
            elif response.status_code == 404:
                print(f"404 Error: {defragged_url}")
            else:
                print(f"Unexpected status code {response.status_code}: {defragged_url}")
        except Exception as e:
            print(f"Error crawling {defragged_url}: {str(e)}")
        return None

    def crawl(self):
        print(f"Starting the crawl process with {len(self.to_visit)} initial URLs...")

        with ThreadPoolExecutor(max_workers=10) as executor:
            while self.to_visit:
                urls_to_crawl = list(self.to_visit)[:10]  # Limit batch size
                self.to_visit = self.to_visit - set(urls_to_crawl)

                for url in executor.map(self.crawl_url, urls_to_crawl):
                    if url and url not in self.crawled_urls:
                        self.crawled_urls.append(url)

                time.sleep(1) 

                print(f"Crawled: {len(self.crawled_urls)}, To visit: {len(self.to_visit)}")
        return self.crawled_urls

def run_crawler(config):
    crawler = DomainCrawler(config['start_url'], config['docs_path'], config.get('avoid_keywords'))
    crawled_urls = crawler.crawl()

    # Remove any potential duplicates before saving
    unique_urls = list(dict.fromkeys(crawled_urls))

    return {
        'start_url': config['start_url'],
        'crawled_urls': unique_urls,
        'total_crawled': len(unique_urls),
        'sitemap_urls': len(crawler.sitemap_urls)
    }

def run_multiple_crawlers(configs, output_file):
    results = []

    with ThreadPoolExecutor(max_workers=len(configs)) as executor:
        future_to_config = {executor.submit(run_crawler, config): config for config in configs}
        for future in as_completed(future_to_config):
            config = future_to_config[future]
            try:
                result = future.result()
                results.append(result)
                print(f"Crawl completed for {config['start_url']}")
                print(f"Total unique URLs crawled: {result['total_crawled']}")
                if result['sitemap_urls']:
                    print(f"Crawled {result['total_crawled']} out of {result['sitemap_urls']} URLs from sitemap")
                else:
                    print("No sitemap was used. All URLs were discovered through crawling.")
            except Exception as exc:
                print(f"{config['start_url']} generated an exception: {exc}")

    # Combine all crawled URLs into a single list
    all_urls = []
    for result in results:
        all_urls.extend([{"url": url} for url in result['crawled_urls']])

    # Save combined results to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_urls, f, ensure_ascii=False, indent=2)

    print(f"All crawls completed. Combined results saved to {output_file}")
    print(f"Total unique URLs crawled across all sites: {len(all_urls)}")


if __name__ == "__main__":
    CONFIGS = [
        {
            "start_url": "https://developer.mozilla.org/en-US/docs/Web/",
            "docs_path": "/",
            "avoid_keywords": ["blog", "about", "community"]
        },
        {
            "start_url": "https://developer.mozilla.org/en-US/docs/Web/",
            "docs_path": "HTML/",
            "avoid_keywords": ["blog", "about", "community"]
        },
        {
            "start_url": "https://developer.mozilla.org/en-US/docs/Web/",
            "docs_path": "CSS/",
            "avoid_keywords": ["blog", "about", "community"]
        },
        {
            "start_url": "https://developer.mozilla.org/en-US/docs/Web/",
            "docs_path": "JavaScript/",
            "avoid_keywords": ["blog", "about", "community"]
        },
        {
            "start_url": "https://developer.mozilla.org/en-US/docs/Web/",
            "docs_path": "HTTP/",
            "avoid_keywords": ["blog", "about", "community"]
        },
        {
            "start_url": "https://developer.mozilla.org/en-US/docs/Web/",
            "docs_path": "API/",
            "avoid_keywords": ["blog", "about", "community"]
        },
        {
            "start_url": "https://developer.mozilla.org/en-US/docs/Learn/",
            "docs_path": "/",
            "avoid_keywords": ["blog", "about", "community"]
        },
        {
            "start_url": "https://developer.mozilla.org/en-US/docs/Learn/",
            "docs_path": "HTML/",
            "avoid_keywords": ["blog", "about", "community"]
        },
        {
            "start_url": "https://developer.mozilla.org/en-US/docs/Learn/",
            "docs_path": "CSS/",
            "avoid_keywords": ["blog", "about", "community"]
        },
        {
            "start_url": "https://developer.mozilla.org/en-US/docs/Learn/",
            "docs_path": "JavaScript/",
            "avoid_keywords": ["blog", "about", "community"]
        },
        {
            "start_url": "https://developer.mozilla.org/en-US/docs/Learn/",
            "docs_path": "Accessibility/",
            "avoid_keywords": ["blog", "about", "community"]
        }
        # {
        #     "start_url": "https://pytorch.org/vision/",
        #     "docs_path": "stable/",
        #     "avoid_keywords": ["blog", "about", "community"]
        # },
        # {
        #     "start_url": "https://pytorch.org/torcharrow/",
        #     "docs_path": "beta/",
        #     "avoid_keywords": ["blog", "about", "community"]
        # },
        # {
        #     "start_url": "https://pytorch.org/data/",
        #     "docs_path": "beta/",
        #     "avoid_keywords": ["blog", "about", "community"]
        # },
        # {
        #     "start_url": "https://pytorch.org/torchrec/",
        #     "docs_path": "",
        #     "avoid_keywords": ["blog", "about", "community"]
        # },
        # {
        #     "start_url": "https://pytorch.org/serve/",
        #     "docs_path": "",
        #     "avoid_keywords": ["blog", "about", "community"]
        # },
        # {
        #     "start_url": "https://pytorch.org/rl/",
        #     "docs_path": "stable/",
        #     "avoid_keywords": ["blog", "about", "community"]
        # },
        # {
        #     "start_url": "https://pytorch.org/tensordict/",
        #     "docs_path": "stable/",
        #     "avoid_keywords": ["blog", "about", "community"]
        # },
        # {
        #     "start_url": "https://pytorch.org/text/",
        #     "docs_path": "stable/",
        #     "avoid_keywords": ["blog", "about", "community"]
        # },

        # {
        #     "start_url": "https://pytorch.org/",
        #     "docs_path": "resources/",
        #     "avoid_keywords": ["blog", "about", "community"]
        # },
        # # Add more configurations as needed
    ]

    
    OUTPUT_PATH = "data/Crawled_url/"
    FILE_NAME="MDN_WEB_crawled.json"
    

    run_multiple_crawlers(CONFIGS, OUTPUT_PATH+FILE_NAME)