<<<<<<< HEAD
from fastapi import FastAPI, HTTPException, Depends, Query, Path, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
import traceback
import validators
from typing import Optional, List
import logging

from config import settings
from models import ScrapeRequest, ScrapeResponse, HealthResponse, HistoryResponse, User
from scraper import scrape_images
from auth import get_current_user, get_optional_user
from database import save_scrape_history, get_user_history
from cache import cached, clear_cache

# Configure logging
logging.basicConfig(level=logging.INFO if settings.DEBUG else logging.WARNING)
logger = logging.getLogger(__name__)
=======
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from typing import List, Dict
import validators
from scraper import scrape_images  # This is your async scraping function
>>>>>>> parent of 573dfad (Updated Backend)

# Define allowed origins (React/Vite frontend)
origins = [
    "https://hackthehaze.vercel.app/",
]

# Create FastAPI app
<<<<<<< HEAD
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)
=======
app = FastAPI(title="Image Scraper API")
>>>>>>> parent of 573dfad (Updated Backend)

# Enable CORS - Support all headers including Authorization
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # ✅ Use specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD
# Custom middleware to log requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    path = request.url.path
    method = request.method
    client = request.client.host if request.client else "unknown"
    auth_header = request.headers.get("Authorization", "No Auth")
    auth_present = "Auth header present" if auth_header != "No Auth" else "No Auth header"
    
    logger.info(f"Request: {method} {path} from {client} - {auth_present}")
    
    response = await call_next(request)
    
    logger.info(f"Response: {method} {path} - Status: {response.status_code}")
    return response

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
    # Debug logging
    logger.info(f"Processing scrape request for URLs: {request.urls}")
    logger.info(f"Current user: {current_user}")
    
=======
# Request body model
class ScrapeRequest(BaseModel):
    urls: List[str]

# Response model
class ScrapeResponse(BaseModel):
    results: Dict[str, List[str]]
    errors: List[Dict[str, str]]

# Main POST endpoint
@app.post("/scrape", response_model=ScrapeResponse)
async def scrape_urls(request: ScrapeRequest) -> ScrapeResponse:
>>>>>>> parent of 573dfad (Updated Backend)
    results = {}
    errors = []

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
            errors.append({"url": url, "error": f"Failed to scrape: {str(e)}"})

    await asyncio.gather(*[scrape_url(url) for url in valid_urls])

    # Save history for authenticated users
    if current_user and results:
        total_images = sum(len(images) for images in results.values())
        try:
            logger.info(f"Saving history for user {current_user.id}")
            await save_scrape_history(
                user_id=current_user.id,
                urls=request.urls,
                image_count=total_images
            )
        except Exception as e:
            logger.error(f"Failed to save history: {str(e)}")
            if settings.DEBUG:
                print(f"Failed to save history: {str(e)}")

    return ScrapeResponse(results=results, errors=errors)

<<<<<<< HEAD
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

# DEBUG endpoint to check authentication
@app.get("/auth-check", tags=["Debug"])
async def auth_check(current_user: Optional[User] = Depends(get_optional_user)):
    """Debug endpoint to check authentication status."""
    if current_user:
        return {
            "authenticated": True,
            "user_id": current_user.id,
            "email": current_user.email
        }
    else:
        return {
            "authenticated": False,
            "message": "No valid authentication token found"
        }

# Clear cache endpoint (admin only - would need additional auth in production)
@app.post("/admin/clear-cache", tags=["Admin"])
async def admin_clear_cache():
    """Clear the API cache (admin only)."""
    if settings.DEBUG:
        clear_cache()
        return {"status": "Cache cleared"}
    raise HTTPException(status_code=403, detail="Not allowed in production")

=======
>>>>>>> parent of 573dfad (Updated Backend)
# Run the app (for standalone testing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
