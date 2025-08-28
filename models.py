# models.py
from pydantic import BaseModel
from typing import Optional

class CoralData(BaseModel):
    """Data model for the prediction input."""
    Turbidity: float
    Depth_m: float
    Temperature_Maximum: float
    SSTA_DHW: float
    TSA_DHW: float

class Token(BaseModel):
    """Data model for the JWT token response."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Data model for the data embedded in the token."""
    username: Optional[str] = None

class User(BaseModel):
    """Data model for a user in the system."""
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    """Data model for a user as stored in the database (includes hashed password)."""
    hashed_password: str
