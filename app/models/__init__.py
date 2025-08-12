from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models here so SQLAlchemy knows about them
from .user_model import User
from .sensor_data import Sensor
