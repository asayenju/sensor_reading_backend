from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    password: str
    email: str

class UserResponse(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    # Don't include password in response for security
