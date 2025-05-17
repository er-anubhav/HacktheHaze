from fastapi import FastAPI, HTTPException, Depends, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
import traceback
import validators
from typing import Optional, List

from config import settings
from models import ScrapeRequest, ScrapeResponse, HealthResponse, HistoryResponse, User
from scraper import scrape_images
from auth import get_current_user, get_optional_user
from database import save_scrape_history, get_user_history
from cache import cached, clear_cache

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs" if settings.DEBUG else None,  # Hide docs in production
    redoc_url="/redoc" if settings.DEBUG else None  # Hide redoc in production
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    max_age=86400  # Cache preflight requests for 24 hours
)

# Main POST endpoint
@app.post("/scrape", response_model=ScrapeResponse, tags=["Scraping"])
@cached(expires_in_seconds=settings.CACHE_EXPIRY)
async def scrape_urls(
    request: ScrapeRequest,
    current_user: Optional[User] = Depends(get_optional_user)
) -> ScrapeResponse:
    """
    Scrape images from URLs.
    
    Authenticated users will have their scrape history saved.
    """
    results = {}
    errors = []
    
    if not request.urls:
        raise HTTPException(status_code=400, detail="No URLs provided")
        
    if len(request.urls) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 URLs allowed per request")

    valid_urls = []
    for url in request.urls:
        if validators.url(url):
            valid_urls.append(url)
        else:
            errors.append({"url": url, "error": "Invalid URL format"})

    # Async scraping tasks
    async def scrape_url(url: str):
        try:
            image_urls = await scrape_images(url)
            results[url] = image_urls
        except Exception as e:
            error_message = str(e)
            if settings.DEBUG:
                error_message = f"{str(e)}\n{traceback.format_exc()}"
            errors.append({"url": url, "error": f"Failed to scrape: {error_message}"})

    # Use a timeout to prevent hanging requests
    try:
        await asyncio.gather(*[scrape_url(url) for url in valid_urls])
    except asyncio.TimeoutError:
        errors.append({"url": "general", "error": "Request timed out"})
    except Exception as e:
        errors.append({"url": "general", "error": f"Unexpected error: {str(e)}"})

    # Save history for authenticated users
    if current_user and results:
        total_images = sum(len(images) for images in results.values())
        try:
            await save_scrape_history(
                user_id=current_user.id,
                urls=request.urls,
                image_count=total_images
            )
        except Exception as e:
            if settings.DEBUG:
                print(f"Failed to save history: {str(e)}")

    return ScrapeResponse(results=results, errors=errors)

# History endpoint (requires authentication)
@app.get("/history", response_model=HistoryResponse, tags=["History"])
async def get_history(
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    page_size: int = Query(
        settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description="Number of items per page"
    )
):
    """
    Get user's scrape history (authenticated users only).
    """
    return await get_user_history(
        user_id=current_user.id,
        page=page,
        page_size=page_size
    )

# History detail endpoint
@app.get("/history/{history_id}", tags=["History"])
async def get_history_detail(
    history_id: int = Path(..., description="History entry ID"),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific history entry (authenticated users only).
    """
    # Implementation would fetch a specific history entry
    raise HTTPException(status_code=501, detail="Not implemented yet")

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to HackTheHaze Image Scraper API",
        "documentation": "/docs",
        "health": "/health"
    }

# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health():
    return HealthResponse(status="ok", version=settings.API_VERSION)

# Clear cache endpoint (admin only - would need additional auth in production)
@app.post("/admin/clear-cache", tags=["Admin"])
async def admin_clear_cache():
    """Clear the API cache (admin only)."""
    if settings.DEBUG:
        clear_cache()
        return {"status": "Cache cleared"}
    raise HTTPException(status_code=403, detail="Not allowed in production")

# Run the app (for standalone testing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
