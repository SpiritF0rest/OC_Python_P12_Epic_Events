from typing import Literal

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

Roles = Literal["commercial", "support", "management"]


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String())
    role: Mapped[Roles]

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, role={self.role})"
