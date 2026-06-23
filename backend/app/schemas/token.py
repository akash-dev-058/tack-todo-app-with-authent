from datetime import datetime
from pydantic import BaseModel, Field

class TokenData(BaseModel):
    sub: int = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    exp: datetime
    type: str

class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RefreshTokenResponse(BaseModel):
    refresh_token: str
    token_type: str = "bearer"
