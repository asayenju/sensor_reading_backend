from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# SQLAlchemy User model
class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uuid = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('UserTable', back_populates='sensors')
class sensor_model(BaseModel):
    uuid: str
    user_id: int