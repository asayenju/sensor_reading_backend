from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User, UserResponse, UserTable, UserUpdate, UserLogin, LoginResponse
import bcrypt
from app.auth.auth import create_access_token, create_refresh_token 

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db)):
    """Get all users"""
    try:
        users = db.query(UserTable).all()
        return {"users": [{"id": user.id, "username": user.username, "email": user.email} for user in users]}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    try:
        user = db.query(UserTable).filter(UserTable.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return {"user": {"id": user.id, "username": user.username, "email": user.email}}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User, db: Session = Depends(get_db)):
    """Create a new user"""
    try:
        # Check if email already exists
        existing_user = db.query(UserTable).filter(UserTable.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password
        saltround = bcrypt.gensalt(12)
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), saltround)
        
        # Create new user
        db_user = UserTable(
            username=user.username,
            password=hashed_password.decode('utf-8'),
            email=user.email
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return {"message": "successful creation", "user_id": db_user.id}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    """Update a user"""
    try:
        # Check if user exists
        db_user = db.query(UserTable).filter(UserTable.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Hash new password
        saltround = bcrypt.gensalt(12)
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), saltround)
        
        # Update user fields
        db_user.username = user.username
        db_user.password = hashed_password.decode('utf-8')
        db_user.email = user.email
        
        db.commit()
        db.refresh(db_user)
        
        return {"message": "Successfully updated user"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user"""
    try:
        # Check if user exists
        db_user = db.query(UserTable).filter(UserTable.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Delete user
        db.delete(db_user)
        db.commit()
        
        return {"message": "User deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    """Login user with email and password"""
    try:
        # Find user by email
        db_user = db.query(UserTable).filter(UserTable.email == user_login.email).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password
        if not bcrypt.checkpw(user_login.password.encode('utf-8'), db_user.password.encode('utf-8')):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Create user response
        user_response = UserResponse(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email
        )
        
        return LoginResponse(
            message="Login successful",
            user=user_response,
            access_token=create_access_token(db_user.email),
            refresh_token=create_refresh_token(db_user.email)  # You can implement JWT tokens later
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )