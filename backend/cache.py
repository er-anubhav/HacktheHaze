"""Caching utilities for the HackTheHaze API."""
from functools import wraps
from typing import Any, Callable
import hashlib
import json
import time
from config import settings


# Simple in-memory cache
_cache = {}


def cache_key(func: Callable, *args: Any, **kwargs: Any) -> str:
    """Generate a cache key from function name and arguments."""
    key_parts = [func.__name__]
    
    # Add positional args to key
    for arg in args:
        key_parts.append(str(arg))
        
    # Add keyword args to key (sorted for consistency)
    for k in sorted(kwargs.keys()):
        key_parts.append(f"{k}:{kwargs[k]}")
        
    # Create a hash of the combined key
    key_str = ":".join(key_parts)
    return hashlib.md5(key_str.encode()).hexdigest()


def cached(expires_in_seconds: int = 3600):
    """
    Cache decorator for functions.
    
    Args:
        expires_in_seconds: Cache TTL in seconds
        
    Returns:
        Decorated function with caching
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not settings.CACHE_ENABLED:
                return await func(*args, **kwargs)
                
            key = cache_key(func, *args, **kwargs)
            
            # Check if result is in cache and not expired
            if key in _cache:
                cached_time, cached_result = _cache[key]
                if time.time() - cached_time < expires_in_seconds:
                    return cached_result
                    
            # Call function and cache result
            result = await func(*args, **kwargs)
            _cache[key] = (time.time(), result)
            return result
            
        return wrapper
    return decorator


def clear_cache():
    """Clear the entire cache."""
    global _cache
    _cache = {}
