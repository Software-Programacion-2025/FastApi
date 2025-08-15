from config.basemodel import Base
from sqlalchemy import Column, UUID, String, Boolean, Integer, DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default='')
    firstName = Column(String(50), default='', nullable=False)
    lastName = Column(String(50), default='', nullable=False)
    emails = Column(String(30), default='', nullable=False)
    password = Column(String(30), default='', nullable=False)
    ages = Column(Integer, default=0)

    #Modificacion para que no apareza el error de no poder asignar datetime.now() a un campo de tipo DateTime
    create_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.now(), nullable=True)
    update_at : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    delete_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, firstname={self.firstName!r}, lastname={self.lastName!r})"