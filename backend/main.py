from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from typing import List, Dict
import validators
from scraper import scrape_images  # This is your async scraping function

# Define allowed origins (React/Vite frontend)
origins = [
    "https://hackthehaze.vercel.app/",
]

# Create FastAPI app
app = FastAPI(title="Image Scraper API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # ✅ Use specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    return ScrapeResponse(results=results, errors=errors)

# Run the app (for standalone testing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
