from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio
from typing import List, Dict
import validators
from scraper import scrape_images  # This is your async scraping function

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs" if settings.DEBUG else None,  # Hide docs in production
    redoc_url="/redoc" if settings.DEBUG else None  # Hide redoc in production
)

# Enable CORS - Support all headers including Authorization
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # ✅ Use specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=86400  # Cache preflight requests for 24 hours
)

# Models
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

    return ScrapeResponse(results=results, errors=errors)

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
    return HealthResponse(status="ok", version="1.0.0")

# Run the app (for standalone testing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
