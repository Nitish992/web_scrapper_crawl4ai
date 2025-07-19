# 🚀 Web Crawler API Documentation

This document provides detailed information about all available API endpoints and their parameters for the Web Crawler powered by Crawl4AI.

## Base URL
```
http://localhost:8000
```

## API Endpoints

### 1. 🕷️ Crawl Sub-URLs
**POST** `/api/v1/crawl-suburls`

Crawl a URL and extract all sub-URLs with metadata.

#### Request Body
```json
{
  "url": "https://example.com",
  "depth": 5,
  "max_pages": 10,
  "strategy": "best_first",
  "exclude_patterns": [],
  "extract_links": true,
  "extract_images": true,
  "output_format": "markdown",
  "wait_for_js": true,
  "js_timeout": 8000,
  "crawl_delay": 1.0
}
```

#### Parameters

| Parameter | Type | Default | Description | Options |
|-----------|------|---------|-------------|---------|
| `url` | string | **Required** | The URL to crawl | Any valid URL |
| `depth` | integer | `5` | Crawl depth for deep crawling | 1-5 |
| `max_pages` | integer | `10` | Maximum pages to crawl | 1-100 |
| `strategy` | string | `"best_first"` | Crawl strategy | `"bfs"`, `"dfs"`, `"best_first"` |
| `exclude_patterns` | array[string] | `[]` | Custom regex patterns to exclude URLs | Array of regex patterns |
| `extract_links` | boolean | `true` | Extract links from pages | `true`, `false` |
| `extract_images` | boolean | `true` | Extract images from pages | `true`, `false` |
| `output_format` | string | `"markdown"` | Output format for content | `"markdown"`, `"html"`, `"text"` |
| `wait_for_js` | boolean | `true` | Wait for JavaScript to load | `true`, `false` |
| `js_timeout` | integer | `8000` | JavaScript timeout in milliseconds | 1000-60000 |
| `crawl_delay` | float | `1.0` | Delay between requests in seconds | 0.1-10.0 |

#### URL Filtering

The crawler automatically excludes common unwanted pages to focus on valuable content. You can customize this behavior using the `exclude_patterns` parameter.

**Default Excluded Patterns:**
- **Authentication pages:** `login`, `signup`, `register`, `sign-in`, `sign-up`, `auth`, `password`, `reset`, `logout`
- **Admin/User pages:** `admin`, `dashboard`, `profile`, `account`
- **E-commerce pages:** `checkout`, `cart`, `payment`, `billing`, `subscribe`
- **Utility pages:** `privacy`, `terms`, `contact`, `support`, `help`, `faq`, `sitemap`, `robots`, `newsletter`
- **File downloads:** `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.zip`, `.rar`, `.exe`, `.dmg`

**Custom Patterns Example:**
```json
{
  "exclude_patterns": [
    ".*login.*",
    ".*signup.*", 
    ".*admin.*",
    ".*checkout.*",
    ".*\.pdf$"
  ]
}
```

**Default Behavior:**
By default, `exclude_patterns` is an empty array `[]`, meaning no custom filtering is applied. The crawler will still use its built-in smart filtering to exclude common unwanted pages.

#### Response
```json
{
  "task_id": "uuid-string",
  "success": true,
  "url": "https://example.com",
  "sub_urls": [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/about",
    "https://example.com/contact"
  ],
  "metadata": {
    "title": "Example Site",
    "description": "A great example website"
  },
  "execution_time_seconds": 2.34,
  "urls_found": 12,
  "crawl_depth": 2,
  "max_pages": 10,
  "strategy": "bfs"
}
```

---

### 2. 🔗 Crawl Multiple URLs
**POST** `/api/v1/crawl-urls`

Crawl multiple URLs and extract content/metadata.

#### Request Body
```json
{
  "urls": [
    "https://example1.com",
    "https://example2.com",
    "https://example3.com"
  ],
  "extract_links": true,
  "extract_images": true,
  "output_format": "markdown",
  "content_type": "markdown",
  "wait_for_js": true,
  "js_timeout": 8000,
  "crawl_delay": 1.0
}
```

#### Parameters

| Parameter | Type | Default | Description | Options |
|-----------|------|---------|-------------|---------|
| `urls` | array[string] | **Required** | List of URLs to crawl | Array of valid URLs |
| `extract_links` | boolean | `true` | Extract links from pages | `true`, `false` |
| `extract_images` | boolean | `true` | Extract images from pages | `true`, `false` |
| `output_format` | string | `"markdown"` | Output format for content | `"markdown"`, `"html"`, `"text"` |
| `content_type` | string | `"markdown"` | Type of content to return | `"markdown"`, `"html"`, `"text"`, `"all"` |
| `wait_for_js` | boolean | `true` | Wait for JavaScript to load | `true`, `false` |
| `js_timeout` | integer | `8000` | JavaScript timeout in milliseconds | 1000-60000 |
| `crawl_delay` | float | `1.0` | Delay between requests in seconds | 0.1-10.0 |

#### Response
```json
{
  "task_id": "uuid-string",
  "success": true,
  "results": [
    {
      "url": "https://example1.com",
      "metadata": {
        "title": "Example Site 1"
      },
      "content": "# Example Site 1\n\nThis is the content...",
      "success": true,
      "execution_time_seconds": 1.23
    },
    {
      "url": "https://example2.com",
      "metadata": {
        "title": "Example Site 2"
      },
      "content": "# Example Site 2\n\nThis is the content...",
      "success": true,
      "execution_time_seconds": 2.45
    }
  ],
  "total_execution_time_seconds": 3.68,
  "urls_processed": 2,
  "average_time_per_url": 1.84
}
```

---

### 3. 💚 Health Check
**GET** `/api/v1/health`

Get service health status.

#### Response
```json
{
  "status": "healthy",
  "timestamp": 1234567890.123,
  "crawler_ready": true
}
```

---

### 4. ⚙️ Configuration
**GET** `/api/v1/config`

Get current service configuration.

#### Response
```json
{
  "browser": {
    "headless": true,
    "viewport_width": 1920,
    "viewport_height": 1080,
    "user_agent": "Mozilla/5.0...",
    "verbose": false,
    "use_persistent_context": true
  },
  "crawling": {
    "delay": 1.0,
    "respect_robots_txt": true,
    "timeout": 60
  },
  "extraction": {
    "extract_links": true,
    "extract_images": true,
    "metadata_fields": ["title", "description", "keywords"]
  },
  "output": {
    "format": "markdown",
    "wait_for_js": true,
    "js_timeout": 8000,
    "include_js_rendered": true
  }
}
```

---

## 🔧 Advanced Configuration Options

### CrawlerRunConfig Parameters (Internal)

The following parameters are used internally by the crawler service:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cache_mode` | CacheMode | `BYPASS` | Cache behavior |
| `check_robots_txt` | boolean | `true` | Respect robots.txt |
| `mean_delay` | float | `1.0` | Delay between requests |
| `verbose` | boolean | `false` | Verbose logging |
| `wait_until` | string | `"domcontentloaded"` | Page load condition |
| `page_timeout` | integer | `8000` | Page timeout in ms |
| `exclude_external_links` | boolean | `false` | Exclude external links |
| `exclude_all_images` | boolean | `false` | Exclude all images |
| `exclude_external_images` | boolean | `false` | Exclude external images |
| `only_text` | boolean | `false` | Extract only text |
| `prettiify` | boolean | `false` | Pretty format HTML |

### Wait Until Options
- `"domcontentloaded"` - Wait for DOM content to load
- `"load"` - Wait for full page load
- `"networkidle"` - Wait for network to be idle
- `"commit"` - Wait for navigation to commit

### Cache Mode Options
- `"enabled"` - Enable caching
- `"disabled"` - Disable caching
- `"read_only"` - Read-only cache
- `"write_only"` - Write-only cache
- `"bypass"` - Bypass cache

### Output Format Options
- `"markdown"` - Clean markdown format
- `"html"` - Raw HTML content
- `"text"` - Plain text only

---

## 📝 Usage Examples

### cURL Examples

**Crawl Sub-URLs:**
```bash
curl -X POST "http://localhost:8000/api/v1/crawl-suburls" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "extract_links": true,
    "extract_images": true,
    "output_format": "markdown",
    "wait_for_js": true,
    "js_timeout": 10000,
    "crawl_delay": 2.0
  }'
```



**Health Check:**
```bash
curl "http://localhost:8000/api/v1/health"
```

### Python Examples

```python
import requests
import json

base_url = "http://localhost:8000"

# Crawl sub-URLs
response = requests.post(f"{base_url}/api/v1/crawl-suburls", json={
    "url": "https://example.com",
    "extract_links": True,
    "extract_images": True,
    "output_format": "markdown",
    "wait_for_js": True,
    "js_timeout": 10000
})

print("Sub-URLs:", response.json()["sub_urls"])

# Crawl multiple URLs
response = requests.post(f"{base_url}/api/v1/crawl-urls", json={
    "urls": ["https://example1.com", "https://example2.com"],
    "content_type": "markdown"
})

print("Results:", response.json()["results"])
```

---

## 🚨 Important Notes

1. **Content Type Selection**: Use `content_type` parameter to specify what type of content to return:
   - `"markdown"`: Clean markdown format (default)
   - `"html"`: Raw HTML content
   - `"text"`: Plain text only
   - `"all"`: Returns all content types as a dictionary

2. **Deep Crawling**: The sub-URLs endpoint now uses deep crawling strategies to discover multiple pages:
   - **BFS (Breadth-First Search)**: Explores all links at one depth before moving deeper
   - **DFS (Depth-First Search)**: Explores as far down a branch as possible before backtracking
   - **Best-First**: Uses intelligent scoring to prioritize the most relevant pages

3. **Crawl Depth**: Set `depth` to control how many levels deep to crawl (1-5 recommended)

4. **Page Limits**: Use `max_pages` to control the total number of pages crawled

5. **JavaScript Rendering**: Set `wait_for_js: true` for dynamic content, `false` for static content.

6. **Rate Limiting**: Use `crawl_delay` to avoid overwhelming target servers.

7. **Robots.txt**: Respect robots.txt by keeping `extract_links: true` (which enables `check_robots_txt`).

8. **Timeout**: Increase `js_timeout` for complex JavaScript-heavy sites.

9. **Output Formats**: 
   - `markdown`: Best for readability and processing
   - `html`: Raw HTML for further processing
   - `text`: Plain text only

---

## 🔗 Related Links

- [Crawl4AI GitHub Repository](https://github.com/unclecode/crawl4ai)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Interactive API Docs](http://localhost:8000/docs)
- [ReDoc Documentation](http://localhost:8000/redoc) 