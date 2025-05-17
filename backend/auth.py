"""Authentication and authorization utilities."""
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, HTTPBearer as HTTPBearerBase
from jose import jwt, JWTError
from typing import Optional

from config import settings
from models import User

# Create a custom HTTPBearer that doesn't raise an exception for missing auth
class OptionalHTTPBearer(HTTPBearerBase):
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        authorization = request.headers.get("Authorization")
        
        if not authorization:
            return None
            
        scheme, credentials = authorization.split()
        if scheme.lower() != "bearer":
            return None
            
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


# Setup auth schemes
security = HTTPBearer()
optional_security = OptionalHTTPBearer()


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
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(optional_security)
) -> Optional[User]:
    """
    Attempt to get current user, but don't require authentication.
    
    Args:
        credentials: The HTTP Authorization header containing the JWT token.
        
    Returns:
        User or None: The authenticated user or None if not authenticated.
    """
    if not credentials:
        return None
        
    try:
        token = credentials.credentials
        
        # Decode and verify JWT token
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_aud": False}
        )
        
        user_id = payload.get("sub")
        email = payload.get("email")
        
        if user_id is None or email is None:
            return None
        
        return User(id=user_id, email=email)
    except (JWTError, Exception):
        return None
