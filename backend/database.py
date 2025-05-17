"""Database utilities for the HackTheHaze API."""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

import httpx
from config import settings
from models import HistoryResponse, HistoryEntry

# Configure logging
logger = logging.getLogger(__name__)

async def save_scrape_history(
    user_id: str, 
    urls: List[str], 
    image_count: int
) -> Dict[str, Any]:
    """
    Save a scrape history entry to Supabase.
    
    Args:
        user_id: The user ID
        urls: List of scraped URLs
        image_count: Total number of images found
        
    Returns:
        The created history entry
    """
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
        logger.error("Missing Supabase URL or service key")
        return {"error": "Database configuration missing"}
    
    logger.info(f"Saving history for user {user_id}: {len(urls)} URLs, {image_count} images")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            client.headers.update({
                "apikey": settings.SUPABASE_SERVICE_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SERVICE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            })
            
            payload = {
                "user_id": user_id,
                "urls": urls,
                "image_count": image_count,
                "created_at": datetime.now().isoformat()
            }
            
            logger.debug(f"POST request to {settings.SUPABASE_URL}/rest/v1/scrape_history")
            response = await client.post(
                f"{settings.SUPABASE_URL}/rest/v1/scrape_history",
                json=payload
            )
            
            if response.status_code >= 400:
                logger.error(f"Supabase error: {response.status_code} - {response.text}")
                return {"error": f"Database error: {response.status_code}"}
                
            return response.json()
    except Exception as e:
        logger.exception(f"Error saving history: {str(e)}")
        return {"error": f"Failed to save: {str(e)}"}


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
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
        logger.error("Missing Supabase URL or service key")
        raise ValueError("Database configuration missing")
    
    logger.info(f"Getting history for user {user_id}, page {page}, size {page_size}")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            client.headers.update({
                "apikey": settings.SUPABASE_SERVICE_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SERVICE_KEY}"
            })
            
            # Calculate pagination
            offset = (page - 1) * page_size
            
            # Get records with range
            logger.debug(f"GET request to {settings.SUPABASE_URL}/rest/v1/scrape_history")
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
            
            if response.status_code >= 400:
                logger.error(f"Supabase error: {response.status_code} - {response.text}")
                raise Exception(f"Database error: {response.status_code}")
                
            # Get total count using a separate count query
            count_response = await client.get(
                f"{settings.SUPABASE_URL}/rest/v1/scrape_history",
                params={
                    "select": "count",
                    "user_id": f"eq.{user_id}"
                },
                headers={"Prefer": "count=exact"}
            )
            
            # Parse the count from the content-range header
            content_range = count_response.headers.get("content-range", "*/0")
            total_count = int(content_range.split("/")[1])
            
            # Create history items
            items = []
            for item in response.json():
                try:
                    items.append(HistoryEntry(
                        id=item.get("id"),
                        user_id=item.get("user_id"),
                        urls=item.get("urls", []),
                        image_count=item.get("image_count", 0),
                        created_at=item.get("created_at")
                    ))
                except Exception as e:
                    logger.error(f"Error parsing history item: {str(e)}")
            
            # Calculate total pages
            total_pages = (total_count + page_size - 1) // page_size if total_count > 0 else 1
            
            return HistoryResponse(
                items=items,
                total=total_count,
                page=page,
                page_size=page_size,
                pages=total_pages
            )
    except Exception as e:
        logger.exception(f"Error getting history: {str(e)}")
        raise
