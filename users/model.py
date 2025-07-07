from config.basemodel import Base
from sqlalchemy import Column, UUID, String, Boolean, Integer, DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default='')
    firstName = Column(String(50), default='', nullable=False)
    lastName = Column(String(50), default='', nullable=False)
    emails = Column(String(30), default='', nullable=False)
    password = Column(String(30), default='', nullable=False)
    ages = Column(Integer, default=0)
    create_at = Column(DateTime, default=datetime(1900,1,1,0,0,0), nullable=True)
    update_at = Column(DateTime, nullable=True)
    delete_at = Column(DateTime, nullable=True)
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, firstname={self.firstName!r}, lastname={self.lastName!r})"