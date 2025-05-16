"""Configuration settings for the HackTheHaze backend."""
import os
from typing import List


class Settings:
    """App settings."""
    
    # API Information
    API_TITLE: str = "HackTheHaze Image Scraper API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API for scraping images from websites"
    
    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "https://hackthehaze.vercel.app",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    CORS_ORIGIN_REGEX: str = r"https://.*\.vercel\.app"
    
    # Outbound Static IP Addresses (for whitelisting)
    OUTBOUND_IPS: List[str] = [
        "44.226.145.213",
        "54.187.200.255",
        "34.213.214.55",
        "35.164.95.156", 
        "44.230.95.183",
        "44.229.200.200",
    ]
    
    # Timeouts
    REQUEST_TIMEOUT: int = 10  # seconds
    
    # Environment
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = ENV == "development"


settings = Settings()
