import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_database_connection():
    """Create and return a database connection"""
    return mysql.connector.connect(
        host=os.getenv('host'),
        port=3306, 
        user=os.getenv('root'),
        password=os.getenv('password'),
        database=os.getenv('database')
    )

def get_cursor():
    """Get database cursor"""
    connection = get_database_connection()
    cursor = connection.cursor()
    return connection, cursor