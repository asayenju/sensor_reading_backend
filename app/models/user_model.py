from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

# SQLAlchemy User model
class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)

    sensors = relationship('Sensor', back_populates='user')

# Pydantic models for API
class User(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    # Don't include password in response for security

class LoginResponse(BaseModel):
    message: str
    user: UserResponse
    access_token: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True
