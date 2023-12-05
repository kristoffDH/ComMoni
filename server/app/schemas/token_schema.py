from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """
    access token schema
    """
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    token data schema
    """
    user_id: str
    expire: int
