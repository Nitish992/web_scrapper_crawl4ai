from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class CrawlSubUrlsRequest(BaseModel):
    url: str = Field(..., description="The URL to crawl and extract sub-URLs from")
    depth: Optional[int] = Field(5, description="Crawl depth for deep crawling", ge=1, le=5)
    max_pages: Optional[int] = Field(10, description="Maximum pages to crawl", ge=1, le=100)
    strategy: Optional[str] = Field("best_first", description="Crawl strategy", pattern="^(bfs|dfs|best_first)$")
    exclude_patterns: Optional[List[str]] = Field([], description="Custom regex patterns to exclude URLs (e.g., ['login', 'signup', 'admin'])")
    extract_links: Optional[bool] = Field(True, description="Extract links from pages")
    extract_images: Optional[bool] = Field(True, description="Extract images from pages")
    output_format: Optional[str] = Field("markdown", description="Output format for content", pattern="^(markdown|html|text)$")
    wait_for_js: Optional[bool] = Field(True, description="Wait for JavaScript to load")
    js_timeout: Optional[int] = Field(8000, description="JavaScript timeout in milliseconds", ge=1000, le=60000)
    crawl_delay: Optional[float] = Field(1.0, description="Delay between requests in seconds", ge=0.1, le=10.0)

class CrawlUrlsRequest(BaseModel):
    urls: List[str] = Field(..., description="List of URLs to crawl and extract content from")
    extract_links: Optional[bool] = Field(True, description="Extract links from pages")
    extract_images: Optional[bool] = Field(True, description="Extract images from pages")
    output_format: Optional[str] = Field("markdown", description="Output format for content", pattern="^(markdown|html|text)$")
    content_type: Optional[str] = Field("markdown", description="Type of content to return", pattern="^(markdown|html|text|all)$")
    wait_for_js: Optional[bool] = Field(True, description="Wait for JavaScript to load")
    js_timeout: Optional[int] = Field(8000, description="JavaScript timeout in milliseconds", ge=1000, le=60000)
    crawl_delay: Optional[float] = Field(1.0, description="Delay between requests in seconds", ge=0.1, le=10.0)



class CrawlResponse(BaseModel):
    task_id: str = Field(..., description="Unique identifier for the crawling task")
    success: bool = Field(..., description="Whether the crawling operation was successful")

class CrawlSubUrlsResponse(CrawlResponse):
    url: str = Field(..., description="The URL that was crawled")
    sub_urls: List[str] = Field(..., description="List of sub-URLs found on the page")
    metadata: Dict[str, Any] = Field(..., description="Metadata extracted from the page (title, description, etc.)")
    execution_time_seconds: float = Field(..., description="Total execution time in seconds")
    urls_found: int = Field(..., description="Number of URLs found on the page")
    crawl_depth: int = Field(..., description="Depth used for deep crawling")
    max_pages: int = Field(..., description="Maximum pages limit used")
    strategy: str = Field(..., description="Crawl strategy used (bfs, dfs, best_first)")

class CrawlUrlsResponse(CrawlResponse):
    results: List[Dict[str, Any]] = Field(..., description="List of results for each crawled URL")
    total_execution_time_seconds: float = Field(..., description="Total execution time for all URLs in seconds")
    urls_processed: int = Field(..., description="Number of URLs processed")
    average_time_per_url: float = Field(..., description="Average time per URL in seconds")



class HealthResponse(BaseModel):
    status: str = Field(..., description="Current health status of the service")
    timestamp: float = Field(..., description="Current timestamp in seconds since epoch")
    crawler_ready: bool = Field(..., description="Whether the crawler is ready to process requests")

class ConfigResponse(BaseModel):
    browser: Dict[str, Any] = Field(..., description="Browser configuration settings")
    crawling: Dict[str, Any] = Field(..., description="Crawling behavior settings")
    extraction: Dict[str, Any] = Field(..., description="Content extraction settings")
    output: Dict[str, Any] = Field(..., description="Output format settings") 