from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Client(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(10))
    company: Mapped[str] = mapped_column(String(255))
    creation_date: Mapped[datetime]
    update_date: Mapped[datetime]
    commercial_contact_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def __repr__(self):
        return f"Client(id={self.id}, name={self.name}, contact_id={self.commercial_contact_id})"
