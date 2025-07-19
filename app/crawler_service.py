import logging
import uuid
import time
from typing import Optional, Dict, Any, List, Union
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy, DFSDeepCrawlStrategy, BestFirstCrawlingStrategy
from crawl4ai.deep_crawling.filters import FilterChain, URLPatternFilter
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from .config import settings

logger = logging.getLogger(__name__)

class CrawlerService:
    def __init__(self):
        self.crawler: Optional[AsyncWebCrawler] = None

    async def initialize(self):
        logger.info("Initializing godly browser (no proxy)")
        try:
            browser_config = BrowserConfig(
                headless=settings.browser_headless,
                verbose=settings.browser_verbose,
                user_data_dir=settings.user_data_dir,
                use_persistent_context=settings.use_persistent_context,
                viewport_width=settings.browser_viewport_width,
                viewport_height=settings.browser_viewport_height,
            )
            if settings.browser_user_agent:
                browser_config.user_agent = settings.browser_user_agent
            
            logger.info(f"Browser config: headless={settings.browser_headless}, viewport={settings.browser_viewport_width}x{settings.browser_viewport_height}")
            self.crawler = AsyncWebCrawler(config=browser_config)
            logger.info("Browser initialized (no proxy)")
        except Exception as e:
            logger.error(f"Failed to initialize browser: {str(e)}")
            raise

    async def shutdown(self):
        if self.crawler:
            try:
                # Close the crawler properly
                await self.crawler.close()
                logger.info("Browser shut down")
            except Exception as e:
                logger.error(f"Error during shutdown: {e}")

    async def crawl_sub_urls(self, url: str, **kwargs) -> Dict[str, Any]:
        total_start_time = time.time()
        try:
            # Ensure crawler is initialized
            if not self.crawler:
                await self.initialize()
                
            # Get deep crawling parameters
            depth = kwargs.get("depth", settings.deep_crawl_depth)
            max_pages = kwargs.get("max_pages", settings.deep_crawl_max_pages)
            strategy = kwargs.get("strategy", settings.deep_crawl_strategy)
            
            # Create URL filter to exclude auth-related pages
            url_filter = self._build_url_filter(kwargs.get("exclude_patterns", []))
            
            # Create deep crawling strategy based on parameter
            if strategy == "dfs":
                crawl_strategy = DFSDeepCrawlStrategy(
                    max_depth=depth,
                    max_pages=max_pages,
                    # filter_chain=url_filter
                )
            elif strategy == "best_first":
                crawl_strategy = BestFirstCrawlingStrategy(
                    max_depth=depth,
                    max_pages=max_pages,
                    # filter_chain=url_filter
                )
            else:  # Default to BFS
                crawl_strategy = BFSDeepCrawlStrategy(
                    max_depth=depth,
                    max_pages=max_pages,
                    # filter_chain=url_filter
                )
            
            # Set up the configuration with deep crawling strategy
            config = CrawlerRunConfig(
                deep_crawl_strategy=crawl_strategy,
                scraping_strategy=LXMLWebScrapingStrategy(),
                stream=True,
                verbose=settings.browser_verbose
            )
            
            # Run deep crawling
            assert self.crawler is not None
            results = []
            async for result in await self.crawler.arun(url, config=config):  # type: ignore
                results.append(result)
                if hasattr(result, 'url'):
                    logger.info(f"Found URL: {result.url}")
            
            # Extract all URLs from deep crawl results
            all_urls = set()
            metadata = {}
            
            # Process all crawled pages
            for result in results:
                if hasattr(result, 'url'):
                    all_urls.add(result.url)
                
                # Get metadata from the first result (main page)
                if not metadata and hasattr(result, 'metadata'):
                    metadata = result.metadata
                elif not metadata and hasattr(result, 'title'):
                    metadata = {'title': result.title}
            
            # Convert to list and filter out the original URL
            sub_urls = [found_url for found_url in all_urls if found_url != url]
            
            logger.info(f"Deep crawl completed: {len(sub_urls)} sub-URLs found")
            logger.info(f"Sub-URLs: {sub_urls[:5]}...")  # Log first 5 URLs
            
            total_end_time = time.time()
            execution_time = round(total_end_time - total_start_time, 2)
            
            return {
                "task_id": str(uuid.uuid4()),
                "url": url,
                "sub_urls": sub_urls,
                "metadata": metadata,
                "success": True,
                "execution_time_seconds": execution_time,
                "urls_found": len(sub_urls),
                "crawl_depth": depth,
                "max_pages": max_pages,
                "strategy": strategy
            }
        except Exception as e:
            total_end_time = time.time()
            execution_time = round(total_end_time - total_start_time, 2)
            logger.error(f"Error crawling sub-URLs: {str(e)}")
            raise

    async def crawl_urls(self, urls: List[str], **kwargs) -> Dict[str, Any]:
        total_start_time = time.time()
        try:
            # Ensure crawler is initialized
            if not self.crawler:
                logger.info("Initializing crawler...")
                await self.initialize()
                logger.info("Crawler initialized successfully")
            
            if not self.crawler:
                raise Exception("Failed to initialize crawler")
                
            results = []
            run_config = self._build_run_config(**kwargs)
            total_urls = len(urls)
            logger.info(f"Starting to crawl {total_urls} URLs")
            
            for i, url in enumerate(urls, 1):
                url_start_time = time.time()
                try:
                    if not self.crawler:
                        raise Exception("Crawler is None")
                    
                    logger.info(f"Processing URL {i}/{total_urls}: {url}")
                    result = await self.crawler.arun(url=url, config=run_config)
                    
                    metadata = self._extract_metadata(result)
                    content_type = kwargs.get("content_type", "markdown")
                    content = self._extract_content(result, content_type)
                    
                    url_end_time = time.time()
                    url_execution_time = round(url_end_time - url_start_time, 2)
                    
                    results.append({
                        "url": url,
                        "metadata": metadata,
                        "content": content,
                        "success": getattr(result, 'success', True),
                        "execution_time_seconds": url_execution_time
                    })
                    
                    logger.info(f"Processed {i}/{total_urls}: {url} in {url_execution_time}s")
                except Exception as url_error:
                    url_end_time = time.time()
                    url_execution_time = round(url_end_time - url_start_time, 2)
                    logger.error(f"Error processing URL {url}: {str(url_error)}")
                    
                    results.append({
                        "url": url,
                        "metadata": {},
                        "content": "",
                        "success": False,
                        "execution_time_seconds": url_execution_time,
                        "error": str(url_error)
                    })
            
            total_end_time = time.time()
            total_execution_time = round(total_end_time - total_start_time, 2)
            
            return {
                "task_id": str(uuid.uuid4()),
                "results": results,
                "success": all(r["success"] for r in results),
                "total_execution_time_seconds": total_execution_time,
                "urls_processed": total_urls,
                "average_time_per_url": round(total_execution_time / total_urls, 2) if total_urls > 0 else 0
            }
        except Exception as e:
            total_end_time = time.time()
            execution_time = round(total_end_time - total_start_time, 2)
            logger.error(f"Error crawling URLs: {str(e)}")
            raise



    def _build_run_config(self, **kwargs) -> CrawlerRunConfig:
        # Use settings, allow override from kwargs
        extract_links = kwargs.get("extract_links", settings.extract_links)
        output_format = kwargs.get("output_format", settings.output_format)
        
        return CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            check_robots_txt=kwargs.get("respect_robots_txt", settings.respect_robots_txt),
            mean_delay=kwargs.get("crawl_delay", settings.crawl_delay),
            verbose=settings.browser_verbose,
            wait_until="domcontentloaded" if kwargs.get("wait_for_js", settings.wait_for_js) else "load",
            page_timeout=kwargs.get("js_timeout", settings.js_timeout),
            exclude_external_links=not extract_links,  # This should be False to include external links
            exclude_all_images=not kwargs.get("extract_images", settings.extract_images),
            exclude_external_images=not kwargs.get("extract_images", settings.extract_images),
            only_text=output_format == "text",
            prettiify=output_format == "html",
            # Enable markdown generation
            markdown_generator=DefaultMarkdownGenerator() if output_format == "markdown" else DefaultMarkdownGenerator(),
        )

    def _build_url_filter(self, exclude_patterns: Optional[List[str]] = None) -> FilterChain:
        """Build URL filter to exclude unwanted pages"""
        exclude_patterns = exclude_patterns or []
        
        # Default patterns to exclude auth-related pages
        default_exclude_patterns = [
            r".*login.*",
            r".*signup.*", 
            r".*register.*",
            r".*sign-in.*",
            r".*sign-up.*",
            r".*auth.*",
            r".*password.*",
            r".*reset.*",
            r".*logout.*",
            r".*admin.*",
            r".*dashboard.*",
            r".*profile.*",
            r".*account.*",
            r".*checkout.*",
            r".*cart.*",
            r".*payment.*",
            r".*billing.*",
            r".*subscribe.*",
            r".*newsletter.*",
            r".*contact.*",
            r".*support.*",
            r".*help.*",
            r".*faq.*",
            r".*sitemap.*",
            r".*robots.*",
            r".*\.(pdf|doc|docx|xls|xlsx|ppt|pptx|zip|rar|exe|dmg)$",  # File extensions
        ]
        
        # Combine default and custom patterns
        all_patterns = default_exclude_patterns + exclude_patterns
        
        # Create URL pattern filter
        url_filter = URLPatternFilter(patterns=all_patterns)  # type: ignore
        
        return FilterChain([url_filter])

    def _extract_links(self, result) -> List[str]:
        # Extract links from the result object
        links = []
        
        # Check for links attribute first
        if hasattr(result, 'links'):
            if isinstance(result.links, list):
                links = result.links
            elif isinstance(result.links, dict):
                links = list(result.links.keys())
        
        # If no links found, try to extract from HTML content
        if not links and hasattr(result, 'html_content') and result.html_content:
            import re
            # Extract href attributes from anchor tags
            href_pattern = r'href=["\']([^"\']+)["\']'
            matches = re.findall(href_pattern, result.html_content)
            links = [url for url in matches if url.startswith(('http://', 'https://', '/'))]
        elif not links and hasattr(result, 'html') and result.html:
            # Fallback to old field name
            import re
            href_pattern = r'href=["\']([^"\']+)["\']'
            matches = re.findall(href_pattern, result.html)
            links = [url for url in matches if url.startswith(('http://', 'https://', '/'))]
        
        # If still no links, try to extract from markdown content
        if not links and hasattr(result, 'markdown_content') and result.markdown_content:
            import re
            # Extract markdown links
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            matches = re.findall(link_pattern, result.markdown_content)
            links = [url for _, url in matches if url.startswith(('http://', 'https://', '/'))]
        elif not links and hasattr(result, 'markdown') and result.markdown:
            # Fallback to old field name
            import re
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            matches = re.findall(link_pattern, result.markdown)
            links = [url for _, url in matches if url.startswith(('http://', 'https://', '/'))]
        
        # Remove duplicates and filter out invalid URLs
        unique_links = []
        seen = set()
        for link in links:
            if link not in seen and link.strip():
                seen.add(link)
                unique_links.append(link)
        
        return unique_links

    def _extract_metadata(self, result) -> Dict[str, Any]:
        metadata = {}
        if hasattr(result, 'metadata') and isinstance(result.metadata, dict):
            metadata = result.metadata
        elif hasattr(result, 'title'):
            metadata['title'] = result.title
        elif hasattr(result, 'markdown_content') and result.markdown_content:
            # Try to extract title from markdown content
            import re
            title_match = re.search(r'^#\s+(.+)$', result.markdown_content, re.MULTILINE)
            if title_match:
                metadata['title'] = title_match.group(1)
        elif hasattr(result, 'markdown') and result.markdown:
            # Fallback to old field name
            import re
            title_match = re.search(r'^#\s+(.+)$', result.markdown, re.MULTILINE)
            if title_match:
                metadata['title'] = title_match.group(1)
        return metadata

    def _extract_content(self, result, content_type: str = "markdown") -> Union[str, Dict[str, str]]:
        if content_type == "all":
            # Return all content types as a dictionary
            content = {}
            # Try the actual CrawlResult field names first
            for attr in ["markdown", "html", "text"]:
                if hasattr(result, attr):
                    val = getattr(result, attr)
                    if val:
                        content[attr] = str(val)  # Convert to string
            
            # Fallback to content field names
            for attr in ["markdown_content", "html_content", "text_content"]:
                if hasattr(result, attr):
                    val = getattr(result, attr)
                    if val and attr.replace("_content", "") not in content:
                        content[attr.replace("_content", "")] = str(val)
            
            return content if content else ""
        
        # Try the actual CrawlResult field names first (markdown, html, text)
        if hasattr(result, content_type):
            val = getattr(result, content_type)
            if val:
                return str(val)  # Convert to string
        
        # Fallback to content field names (markdown_content, html_content, text_content)
        content_field = f"{content_type}_content"
        if hasattr(result, content_field):
            val = getattr(result, content_field)
            if val:
                return str(val)
        
        # If specific content type not found, try any available content
        for attr in ["markdown", "html", "text"]:
            if hasattr(result, attr):
                val = getattr(result, attr)
                if val:
                    return str(val)
        
        # Final fallback to content field names
        for attr in ["markdown_content", "html_content", "text_content"]:
            if hasattr(result, attr):
                val = getattr(result, attr)
                if val:
                    return str(val)
        
        return ""

    def get_health_status(self) -> Dict[str, Any]:
        import asyncio
        return {
            "status": "healthy",
            "timestamp": asyncio.get_event_loop().time(),
            "crawler_ready": self.crawler is not None
        }

    def get_config_status(self) -> Dict[str, Any]:
        return {
            "browser": {
                "headless": settings.browser_headless,
                "viewport_width": settings.browser_viewport_width,
                "viewport_height": settings.browser_viewport_height,
                "user_agent": settings.browser_user_agent,
                "verbose": settings.browser_verbose,
                "use_persistent_context": settings.use_persistent_context,
            },
            "crawling": {
                "delay": settings.crawl_delay,
                "respect_robots_txt": settings.respect_robots_txt,
                "timeout": settings.crawl_timeout,
            },
            "extraction": {
                "extract_links": settings.extract_links,
                "extract_images": settings.extract_images,
                "metadata_fields": settings.metadata_fields,
            },
            "output": {
                "format": settings.output_format,
                "wait_for_js": settings.wait_for_js,
                "js_timeout": settings.js_timeout,
                "include_js_rendered": settings.include_js_rendered,
            }
        }

crawler_service = CrawlerService() 