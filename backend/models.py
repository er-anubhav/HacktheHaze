"""Pydantic models for the HackTheHaze API."""
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class User(BaseModel):
    """User model."""
    id: str
    email: str


class ScrapeRequest(BaseModel):
    """Request model for scrape endpoint."""
    urls: List[str]


class ScrapeResponse(BaseModel):
    """Response model for scrape endpoint."""
    results: Dict[str, List[str]]
    errors: List[Dict[str, str]]


class HealthResponse(BaseModel):
    """Response model for health endpoint."""
    status: str
    version: str


class HistoryEntry(BaseModel):
    """Model for a scrape history entry."""
    id: Optional[int] = None
    user_id: str
    urls: List[str]
    image_count: int
    created_at: datetime = Field(default_factory=datetime.now)


class HistoryResponse(BaseModel):
    """Response model for history endpoint."""
    items: List[HistoryEntry]
    total: int
    page: int
    page_size: int
    pages: int