"""
Godly Web Crawler with Crawl4AI

A powerful, feature-rich web crawling microservice powered by Crawl4AI.
"""

from .config import settings
from .models import *
from .crawler_service import crawler_service
from .routes import router

__version__ = "2.0.0"
__description__ = "Godly Web Crawler with Crawl4AI"

__all__ = [
    "settings",
    "crawler_service",
    "router",
    "CrawlSubUrlsRequest",
    "CrawlUrlsRequest", 
    "CrawlSubUrlsResponse",
    "CrawlUrlsResponse",
    "HealthResponse",
    "ConfigResponse"
] 