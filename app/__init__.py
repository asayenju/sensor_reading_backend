from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("host")
DB_USER = os.getenv("user")
DB_PASSWORD = os.getenv("password")
DB_NAME=os.getenv("database")
JWT_SECRET = os.getenv("JWT_SECRET_KEY")
JWT_REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET_KEY")