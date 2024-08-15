# Framework Docs AI


Framework Docs AI is a powerful SaaS solution that revolutionizes documentation management for various frameworks. It seamlessly scrapes framework documentation, creates a comprehensive knowledge base, and utilizes advanced language models to provide accurate, retrieval-based responses to user queries.

## 🚀 Features

- **Automatic Documentation Scraping**: Effortlessly gather documentation from popular frameworks.
- **Intelligent Knowledge Base**: Store and organize scraped data for efficient retrieval.
- **AI-Powered Responses**: Leverage state-of-the-art language models for accurate answers.
- **Customizable Framework Support**: Add your own frameworks or use existing ones.
- **User-Friendly Interface**: Built with Streamlit for a smooth user experience.

## 🛠️ Technologies Used

- **UI**: Streamlit
- **Vector Database**: Chroma DB
- **Function Calling**: Phi Data
- **Language Model**: GPT-4o-mini

## 📚 Supported Frameworks

1. Langchain
2. Next.js
3. Vue.js
4. PyTorch
5. Chainlit
6. MDN Web Docs

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- pip

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/framework-docs-ai.git
   cd framework-docs-ai
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OPENAI API key:
   - Create a `.env` file in the root directory
   - Add your OPENAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

### Usage

1. Run the application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to the provided local URL (usually `http://localhost:8501`).

3. Start exploring framework documentation and asking questions!




## 🔧 Adding Custom Frameworks

You can add your own custom frameworks to the Framework Docs AI. Follow these steps:

# Framework Docs AI

[... previous content remains the same ...]

## 🔧 Adding Custom Frameworks

You can add your own custom frameworks to the Framework Docs AI. Follow these steps:

1. **Crawl the URLs (crawler.py)**:
   - The `crawler.py` file uses a `DomainCrawler` class to crawl websites and collect URLs.
   - Key components to modify:
     ```python
     CONFIGS = [
         {
             "start_url": "https://your-framework-docs-url.com",
             "docs_path": "/",
             "avoid_keywords": ["blog", "about", "community"]
         },
         # You can add multiple configurations for different sections of your documentation
     ]
     
     OUTPUT_PATH = "data/Crawled_url/"
     FILE_NAME = "YOUR_FRAMEWORK_crawled.json"
     ```
   - Customize the `CONFIGS` list:
     - `start_url`: The base URL of your framework's documentation.
     - `docs_path`: The specific path where the documentation starts.
     - `avoid_keywords`: List of keywords to avoid in URLs (e.g., blog posts, community pages).
   - Update `OUTPUT_PATH` and `FILE_NAME` as needed.
   - The crawler attempts to use a sitemap.xml if available, then falls back to crawling from the specified `docs_path`.
   - It uses multi-threading to crawl multiple configurations simultaneously.
   - Run `crawler.py` to save the crawled URLs in the specified output file.


2. **Scrape the Content**:
   - Use `scrape.py` to extract content from the crawled URLs.
   - Modify the file paths in `scrape.py` to match your new framework:
     ```python
     if __name__ == "__main__":
         Scrape("data/Crawled_url/YOUR_FRAMEWORK_crawled.json", "data/Scraped_data/YOUR_FRAMEWORK_scraped.json")
     ```
   - Run `scrape.py` to save the scraped content in the `data/Scraped_data` directory.

3. **Convert to Langchain Document Format**:
   - Use `save.py` to convert the scraped JSON to a pickle file compatible with Langchain's Document schema.
   - Update the file paths in `save.py`:
     ```python
     if __name__ == "__main__":
         convert_json_to_pkl('data/Scraped_data/YOUR_FRAMEWORK_scraped.json', 'data/Scraped_data/YOUR_FRAMEWORK_scraped.pkl')
     ```
   - Run `save.py` to create the pickle file.

4. **Update `app.py`**:
   - Initialize the knowledge base for your new framework:
     ```python
     kb_manager_your_framework = initialize_kb("Your Framework Name", "./Vector_DB/YOUR_FRAMEWORK", "data/Scraped_data/YOUR_FRAMEWORK_scraped.pkl")
     ```
   - Create an assistant for your framework:
     ```python
     assistant_your_framework = create_assistant("Your Framework Name", api_key, kb_manager_your_framework) if kb_manager_your_framework else None
     ```
   - Add your framework to the sidebar options:
     ```python
     options=["Langchain Python", "Next.js", "Vue.js", "MDN_WEB", "Pytorch", "Chainlit", "Your Framework Name"],
     ```
   - Handle the selection of your framework:
     ```python
     elif selected == "Your Framework Name" and assistant_your_framework:
         display_framework(assistant_your_framework, "Your Framework Name")
     ```

5. **Restart the Application**:
   - Run `app.py` again to see your new framework in action.

Remember to replace "YOUR_FRAMEWORK" and "Your Framework Name" with the appropriate names for your custom framework.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) for the intuitive UI framework
- All the open-source projects that made this possible

---