from fastapi import APIRouter, HTTPException, status
from typing import List
from database import get_cursor, get_database_connection
from models.user_model import User
import bcrypt

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
async def get_users():
    """Get all users"""
    connection, cursor = get_cursor()
    try:
        select_query = "SELECT id, username, email FROM users"
        cursor.execute(select_query)
        results = cursor.fetchall()
        return {"users": results}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int):
    connection, cursor = get_cursor()
    try:

        select_query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(select_query, (user_id,))
        result = cursor.fetchone()
        return {"user": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )



@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    """Create a new user"""
    connection, cursor = get_cursor()
    saltround = bcrypt.gensalt(12)
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), saltround)
    insert_query = """
    INSERT INTO users (username, password, email)
    VALUES (%s, %s, %s)
    """
    values = (user.username, hashed_password, user.email)
    try:
        cursor.execute(insert_query, values)
        connection.commit()

        return {"message": "successful creation"}
        
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    finally:
        cursor.close()
        connection.close()

@router.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: User):
    connection, cursor = get_cursor()
    saltround = bcrypt.gensalt(12)
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), saltround)
    update_query = """
    UPDATE users
    SET username = %s, password = %s, email = %s
    WHERE id = %s
    """
    values = (user.username, hashed_password, user.email, user_id)
    try:
        cursor.execute(update_query, values)
        connection.commit()
        return {"message": "Successfully updated user"}
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    finally:
        cursor.close()
        connection.close()


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int):
    """Delete a user"""
    connection, cursor = get_cursor()
    
    try:
        # Check if user exists
        check_query = "SELECT id FROM users WHERE id = %s"
        cursor.execute(check_query, (user_id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Delete user
        delete_query = "DELETE FROM users WHERE id = %s"
        cursor.execute(delete_query, (user_id,))
        connection.commit()
        return {"message": "User deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    finally:
        cursor.close()
        connection.close()