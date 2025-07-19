# 🚀 Web Crawler with Crawl4AI

A **powerful, feature-rich web crawling microservice** powered by [Crawl4AI](https://github.com/unclecode/crawl4ai), designed for maximum extraction capabilities and flexibility.

## ✨ Features

### 🕷️ Advanced Crawling
- **Multiple Strategies**: BFS, DFS, Priority-based crawling
- **Depth Control**: Configurable crawl depth and max pages
- **Rate Limiting**: Intelligent delays between requests
- **Robots.txt Compliance**: Respect website crawling policies
- **Redirect Handling**: Follow redirects with configurable limits

### 🔍 Content Extraction
- **Links**: Extract all internal and external links
- **Images**: Capture image URLs and metadata
- **Metadata**: Extract title, description, keywords, and more
- **Schema Data**: JSON-LD and microdata extraction
- **Tables**: HTML table extraction and parsing
- **Custom Schemas**: Define your own extraction patterns

### 📄 Output Formats
- **Markdown**: Clean, readable markdown
- **HTML**: Raw HTML content
- **Text**: Plain text extraction
- **JSON**: Structured JSON output

### 🌐 Browser Features
- **Headless Mode**: Run without GUI
- **JavaScript Rendering**: Full JS support with timeouts
- **Custom User Agents**: Spoof any browser
- **Viewport Control**: Configurable screen sizes
- **Persistent Context**: Maintain browser state

### 🏗️ Architecture
- **Async/Concurrent**: High-performance async operations
- **Modular Design**: Clean, maintainable codebase
- **RESTful API**: Modern FastAPI endpoints
- **Health Monitoring**: Built-in health checks
- **Configuration Management**: Environment-based settings

## 🛠️ Installation

### Prerequisites
- Python 3.12+
- pip or uv

### Quick Start
```bash
# Clone the repository
git clone <your-repo-url>
cd web_scrapper_crawl4ai

# Set up environment variables
cp .env.example .env
# Edit .env file with your preferred settings

# Install dependencies
pip install -r requirements.txt

# Run the service
python main.py
```

The service will be available at `http://localhost:8000`

## ⚙️ Configuration

### Environment Variables

Copy the example environment file and customize it:

```bash
cp .env.example .env
# Edit .env file with your preferred settings
```

Or create a `.env` file in the project root with these settings:

```bash
# Browser Configuration
BROWSER_HEADLESS=true
BROWSER_VIEWPORT_WIDTH=1920
BROWSER_VIEWPORT_HEIGHT=1080
BROWSER_VERBOSE=false
USE_PERSISTENT_CONTEXT=true

# Crawling Configuration
CRAWL_DELAY=1.0
RESPECT_ROBOTS_TXT=true
CRAWL_TIMEOUT=60

# Deep Crawling Defaults
DEEP_CRAWL_DEPTH=5
DEEP_CRAWL_MAX_PAGES=10
DEEP_CRAWL_STRATEGY=best_first

# Extraction Configuration
EXTRACT_LINKS=true
EXTRACT_IMAGES=true
OUTPUT_FORMAT=markdown
WAIT_FOR_JS=true
JS_TIMEOUT=8000
INCLUDE_JS_RENDERED=true
```

## 🔌 API Endpoints

For detailed API documentation with all parameters and options, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md).

### Quick Overview

1. **POST** `/api/v1/crawl-suburls` - Crawl a URL and extract sub-URLs
2. **POST** `/api/v1/crawl-urls` - Crawl multiple URLs
3. **GET** `/api/v1/health` - Health check
4. **GET** `/api/v1/config` - Get configuration

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Full API Docs**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## 📝 Usage Examples

For comprehensive usage examples with all parameters and options, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md).

### Quick Python Example

```python
import requests

base_url = "http://localhost:8000"

# Crawl sub-URLs
response = requests.post(f"{base_url}/api/v1/crawl-suburls", json={
    "url": "https://example.com",
    "extract_links": True,
    "extract_images": True,
    "output_format": "markdown",
    "wait_for_js": True
})

print("Sub-URLs:", response.json()["sub_urls"])

# Crawl multiple URLs
response = requests.post(f"{base_url}/api/v1/crawl-urls", json={
    "urls": ["https://example1.com", "https://example2.com"],
    "content_type": "markdown"
})

print("Results:", response.json()["results"])
```

### Quick cURL Example

```bash
# Crawl sub-URLs
curl -X POST "http://localhost:8000/api/v1/crawl-suburls" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "extract_links": true,
    "output_format": "markdown"
  }'

# Check health
curl "http://localhost:8000/api/v1/health"
```

**For detailed examples and all available parameters, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)**

## 🎯 Advanced Features

### Crawl Strategies

1. **BFS (Breadth-First Search)**: Crawl all pages at current depth before going deeper
2. **DFS (Depth-First Search)**: Crawl as deep as possible before moving to siblings
3. **Priority**: Crawl based on priority scores (if implemented)



### JavaScript Rendering

The crawler supports full JavaScript rendering with configurable timeouts:

```json
{
  "wait_for_js": true,
  "js_timeout": 8000,
  "include_js_rendered": true
}
```

## 🔧 Development

### Project Structure
```
web_scrapper_crawl4ai/
├── app/
│   ├── __init__.py
│   ├── config.py          # Settings and configuration
│   ├── models.py          # Pydantic models
│   ├── crawler_service.py # Core crawling logic
│   └── routes.py          # FastAPI endpoints
├── main.py                # Application entrypoint
├── requirements.txt       # Dependencies
└── README.md             # This file
```

### Running in Development
```bash
# Install in development mode
pip install -e .

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🐛 Troubleshooting

### Common Issues

1. **Browser Startup Issues**:
   - Ensure Playwright browsers are installed: `playwright install`
   - Check system resources and permissions
   - Verify user data directory permissions

2. **JavaScript Rendering Issues**:
   - Increase `JS_TIMEOUT` value
   - Set `WAIT_FOR_JS=False` for static content
   - Check for JavaScript errors in logs

3. **Memory Issues**:
   - Reduce `MAX_PAGES` and `CRAWL_DEPTH`
   - Increase `CRAWL_DELAY` to reduce load
   - Monitor system resources

### Logging

The service provides comprehensive logging:
- Browser startup and configuration
- Crawling progress and errors
- Extraction results
- Performance metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Crawl4AI](https://github.com/unclecode/crawl4ai) - Open-source LLM Friendly Web Crawler & Scraper
- Powered by [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- Uses [Playwright](https://playwright.dev/) for browser automation



