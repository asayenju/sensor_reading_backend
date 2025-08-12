import os
from datetime import datetime, timedelta
from typing import Union, Any
import jwt
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')  # should be kept secret
JWT_REFRESH_SECRET_KEY = os.getenv('JWT_REFRESH_SECRET_KEY')   # should be kept secret

def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now() + expires_delta
    else:
        expires_delta = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now() + expires_delta
    else:
        expires_delta = datetime.now() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def validate_jwt_token(token_to_validate):
    try:
        decoded_payload = jwt.decode(token_to_validate, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        print("Token has expired. Please log in again.")
    except jwt.InvalidTokenError:
        print("Invalid token. Access denied.")
    return None