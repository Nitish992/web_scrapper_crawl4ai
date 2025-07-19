"""
Enhanced Web Scraper with Crawl4AI - Main Application

This is the entry point for the web scraping microservice.
"""

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app import crawler_service, router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    await crawler_service.initialize()
    yield
    # Shutdown
    await crawler_service.shutdown()

app = FastAPI(
    title="Web Crawler with Crawl4AI",
    description="A powerful, feature-rich web crawling microservice powered by Crawl4AI",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Include API routes
app.include_router(router, prefix="/api/v1", tags=["crawling"])

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "Web Crawler with Crawl4AI",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/api/v1/health",
        "config": "/api/v1/config"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)