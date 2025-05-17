"""Authentication and authorization utilities."""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError

from config import settings
from models import User

# Setup HTTP Bearer auth scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Validate the JWT token and return the current user.
    
    Args:
        credentials: The HTTP Authorization header containing the JWT token.
        
    Returns:
        User: The authenticated user.
        
    Raises:
        HTTPException: If authentication fails.
    """
    try:
        token = credentials.credentials
        
        # Decode and verify JWT token
        # Note: In production, we would use the Supabase JWT secret for verification
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_aud": False}
        )
        
        user_id = payload.get("sub")
        email = payload.get("email")
        
        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return User(id=user_id, email=email)
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Attempt to get current user, but don't require authentication.
    
    Args:
        credentials: The HTTP Authorization header containing the JWT token.
        
    Returns:
        User or None: The authenticated user or None if not authenticated.
    """
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None
