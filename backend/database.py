"""Database utilities for the HackTheHaze API."""
from contextlib import asynccontextmanager
from typing import List, AsyncGenerator
import json
from datetime import datetime

import httpx
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Text, select, insert

from config import settings
from models import HistoryEntry, HistoryResponse


# Initialize Supabase client for direct database access
async def get_supabase_client():
    """Get a Supabase client."""
    async with httpx.AsyncClient() as client:
        return client.headers.update({
            "apikey": settings.SUPABASE_SERVICE_KEY,
            "Authorization": f"Bearer {settings.SUPABASE_SERVICE_KEY}"
        })


async def save_scrape_history(
    user_id: str, 
    urls: List[str], 
    image_count: int
) -> dict:
    """
    Save a scrape history entry to Supabase.
    
    Args:
        user_id: The user ID
        urls: List of scraped URLs
        image_count: Total number of images found
        
    Returns:
        The created history entry
    """
    async with httpx.AsyncClient() as client:
        client.headers.update({
            "apikey": settings.SUPABASE_SERVICE_KEY,
            "Authorization": f"Bearer {settings.SUPABASE_SERVICE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        })
        
        response = await client.post(
            f"{settings.SUPABASE_URL}/rest/v1/scrape_history",
            json={
                "user_id": user_id,
                "urls": urls,
                "image_count": image_count,
                "created_at": datetime.now().isoformat()
            }
        )
        response.raise_for_status()
        return response.json()


async def get_user_history(
    user_id: str,
    page: int = 1,
    page_size: int = 20
) -> HistoryResponse:
    """
    Get scrape history for a user.
    
    Args:
        user_id: The user ID
        page: Page number (1-indexed)
        page_size: Items per page
        
    Returns:
        Paginated history entries
    """
    async with httpx.AsyncClient() as client:
        client.headers.update({
            "apikey": settings.SUPABASE_SERVICE_KEY,
            "Authorization": f"Bearer {settings.SUPABASE_SERVICE_KEY}"
        })
        
        # Get count first
        count_response = await client.get(
            f"{settings.SUPABASE_URL}/rest/v1/scrape_history",
            params={
                "select": "count",
                "user_id": f"eq.{user_id}"
            }
        )
        count_response.raise_for_status()
        total = int(count_response.headers.get("content-range", "0-0/0").split("/")[1])
        
        # Calculate pagination values
        offset = (page - 1) * page_size
        total_pages = (total + page_size - 1) // page_size if total > 0 else 1
        
        # Get records
        response = await client.get(
            f"{settings.SUPABASE_URL}/rest/v1/scrape_history",
            params={
                "select": "*",
                "user_id": f"eq.{user_id}",
                "order": "created_at.desc",
                "limit": str(page_size),
                "offset": str(offset)
            }
        )
        response.raise_for_status()
        
        items = [HistoryEntry(**item) for item in response.json()]
        
        return HistoryResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=total_pages
        )
