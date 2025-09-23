from config.basemodel import Base
from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from sqlalchemy.dialects.sqlite import INTEGER
from datetime import datetime
from config.associations import user_task_association

from typing import TYPE_CHECKING

# Usamos TYPE_CHECKING para evitar referencias circulares en tiempo de ejecución.
# Esto permite usar anotaciones de tipo para relaciones sin importar el modelo opuesto directamente,
# ya que solo se evalúan en tiempo de chequeo de tipos (mypy, IDEs), no en tiempo de ejecución.
if TYPE_CHECKING:
    # Solo para tipado estático, no se ejecuta en tiempo de ejecución
    from users.model import User

class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    state: Mapped[str] = mapped_column(String(20), nullable=False, default='pending')

    create_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.now, nullable=True)
    update_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    delete_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    users: Mapped[List["User"]] = relationship('User', secondary=user_task_association, back_populates='tasks')