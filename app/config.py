import logging
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Browser
    browser_headless: bool = True
    browser_viewport_width: int = 1920
    browser_viewport_height: int = 1080
    browser_user_agent: Optional[str] = None
    user_data_dir: str = str(Path.home() / ".crawl4ai" / "browser_profile")
    browser_verbose: bool = False
    use_persistent_context: bool = True

    # Crawl
    crawl_delay: float = 1.0
    respect_robots_txt: bool = True
    crawl_timeout: int = 60

    # Extraction
    extract_links: bool = True
    extract_images: bool = True
    output_format: str = "markdown"  # markdown, html, text
    wait_for_js: bool = True
    js_timeout: int = 8000
    include_js_rendered: bool = True

    # Deep Crawling Defaults
    deep_crawl_depth: int = 5
    deep_crawl_max_pages: int = 10
    deep_crawl_strategy: str = "best_first"  # bfs, dfs, best_first

    @property
    def metadata_fields(self) -> List[str]:
        return ["title", "description", "keywords"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra fields from old proxy config

# Global settings instance
settings = Settings() 