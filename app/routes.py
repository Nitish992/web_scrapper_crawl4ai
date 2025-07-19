from fastapi import APIRouter, HTTPException
from .models import (
    CrawlSubUrlsRequest, CrawlUrlsRequest,
    CrawlSubUrlsResponse, CrawlUrlsResponse,
    HealthResponse, ConfigResponse
)
from .crawler_service import crawler_service

router = APIRouter()

@router.post(
    "/crawl-suburls", 
    response_model=CrawlSubUrlsResponse,
    summary="Crawl Sub-URLs",
    description="""
    Crawl a URL and extract all sub-URLs with metadata.
    
    **Features:**
    - Extract links from the target URL
    - Extract images and metadata
    - Support for JavaScript rendering
    - Configurable output formats
    - Rate limiting with crawl delays
    - Smart URL filtering to exclude unwanted pages
    
    **Use Cases:**
    - Site mapping and discovery
    - Link extraction for analysis
    - Content inventory creation
    - Focused crawling (skip login, admin, checkout pages)
    """,
    response_description="Returns extracted sub-URLs and metadata from the crawled page"
)
async def crawl_suburls(request: CrawlSubUrlsRequest):
    """
    Crawl a URL and extract all sub-URLs with metadata.
    
    This endpoint crawls a single URL and returns:
    - All links found on the page
    - Page metadata (title, description, etc.)
    - Success status and task ID
    
    **Parameters:**
    - `url`: Target URL to crawl (required)
    - `depth`: Crawl depth for deep crawling (default: 5)
    - `max_pages`: Maximum pages to crawl (default: 10)
    - `strategy`: Crawl strategy - bfs, dfs, or best_first (default: best_first)
    - `exclude_patterns`: Custom regex patterns to exclude URLs (default: [])
    - `extract_links`: Extract links from pages (default: true)
    - `extract_images`: Extract images from pages (default: true)
    - `output_format`: Content format - markdown, html, or text (default: markdown)
    - `wait_for_js`: Wait for JavaScript to load (default: true)
    - `js_timeout`: JavaScript timeout in milliseconds (default: 8000)
    - `crawl_delay`: Delay between requests in seconds (default: 1.0)
    """
    try:
        result = await crawler_service.crawl_sub_urls(
            url=request.url,
            depth=request.depth,
            max_pages=request.max_pages,
            strategy=request.strategy,
            exclude_patterns=request.exclude_patterns,
            extract_links=request.extract_links,
            extract_images=request.extract_images,
            output_format=request.output_format,
            wait_for_js=request.wait_for_js,
            js_timeout=request.js_timeout,
            crawl_delay=request.crawl_delay,
        )
        return CrawlSubUrlsResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/crawl-urls", 
    response_model=CrawlUrlsResponse,
    summary="Crawl Multiple URLs",
    description="""
    Crawl multiple URLs and extract content/metadata from each.
    
    **Features:**
    - Batch processing of multiple URLs
    - Extract content and metadata from each URL
    - Configurable extraction options
    - Support for JavaScript rendering
    - Rate limiting with crawl delays
    
    **Use Cases:**
    - Batch content extraction
    - Multi-site analysis
    - Content aggregation
    - Data collection from multiple sources
    """,
    response_description="Returns extracted content and metadata from all crawled URLs"
)
async def crawl_urls(request: CrawlUrlsRequest):
    """
    Crawl multiple URLs and extract content/metadata from each.
    
    This endpoint crawls multiple URLs in sequence and returns:
    - Content extracted from each URL
    - Metadata for each page
    - Success status for each URL
    - Overall task status
    
    **Parameters:**
    - `urls`: List of URLs to crawl (required)
    - `extract_links`: Extract links from pages (default: true)
    - `extract_images`: Extract images from pages (default: true)
    - `output_format`: Content format - markdown, html, or text (default: markdown)
    - `content_type`: Type of content to return - markdown, html, text, or all (default: markdown)
    - `wait_for_js`: Wait for JavaScript to load (default: true)
    - `js_timeout`: JavaScript timeout in milliseconds (default: 8000)
    - `crawl_delay`: Delay between requests in seconds (default: 1.0)
    """
    try:
        result = await crawler_service.crawl_urls(
            urls=request.urls,
            extract_links=request.extract_links,
            extract_images=request.extract_images,
            output_format=request.output_format,
            content_type=request.content_type,
            wait_for_js=request.wait_for_js,
            js_timeout=request.js_timeout,
            crawl_delay=request.crawl_delay,
        )
        return CrawlUrlsResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/health", 
    response_model=HealthResponse,
    summary="Health Check",
    description="""
    Get the current health status of the web crawler service.
    
    **Returns:**
    - Service status (healthy/unhealthy)
    - Current timestamp
    - Crawler readiness status
    """,
    response_description="Returns the health status of the crawler service"
)
async def health():
    """
    Get service health status.
    
    This endpoint provides information about the current health and status of the web crawler service.
    
    **Returns:**
    - `status`: Current service status ("healthy" or "unhealthy")
    - `timestamp`: Current timestamp in seconds since epoch
    - `crawler_ready`: Boolean indicating if the crawler is ready to process requests
    """
    try:
        status = crawler_service.get_health_status()
        return HealthResponse(**status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/config", 
    response_model=ConfigResponse,
    summary="Get Configuration",
    description="""
    Get the current configuration settings of the web crawler service.
    
    **Returns:**
    - Browser configuration settings
    - Crawling behavior settings
    - Content extraction settings
    - Output format settings
    """,
    response_description="Returns the current configuration of the crawler service"
)
async def config():
    """
    Get current configuration.
    
    This endpoint returns the current configuration settings for the web crawler service,
    including browser settings, crawling behavior, and extraction options.
    
    **Returns:**
    - `browser`: Browser configuration (headless, viewport, user agent, etc.)
    - `crawling`: Crawling behavior settings (depth, max pages, strategy, etc.)
    - `extraction`: Content extraction settings (links, images, metadata, etc.)
    - `output`: Output format settings (format, JavaScript rendering, etc.)
    """
    try:
        config = crawler_service.get_config_status()
        return ConfigResponse(**config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 