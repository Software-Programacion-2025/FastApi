
from __future__ import annotations
from config.basemodel import Base
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from tasks.model import user_task_association

    # Usamos TYPE_CHECKING para evitar referencias circulares en tiempo de ejecución.
    # Esto permite usar anotaciones de tipo para relaciones sin importar el modelo opuesto directamente,
    # ya que solo se evalúan en tiempo de chequeo de tipos (mypy, IDEs), no en tiempo de ejecución.
if TYPE_CHECKING:
    # Solo para tipado estático, no se ejecuta en tiempo de ejecución
    from tasks.model import Task

class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default='')
    firstName: Mapped[str] = mapped_column(String(50), default='', nullable=False)
    lastName: Mapped[str] = mapped_column(String(50), default='', nullable=False)
    emails: Mapped[str] = mapped_column(String(30), default='', nullable=False)
    password: Mapped[str] = mapped_column(String(30), default='', nullable=False)
    ages: Mapped[int] = mapped_column(Integer, default=0)

    create_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.now, nullable=True)
    update_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    delete_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    tasks: Mapped[List["Task"]] = relationship('Task', secondary=user_task_association, back_populates='users')

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, firstname={self.firstName!r}, lastname={self.lastName!r})"