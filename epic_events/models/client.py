from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from epic_events.models.base import Base


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    phone: Mapped[str] = mapped_column(String(10), nullable=True)
    company: Mapped[str] = mapped_column(String(255), nullable=True)
    creation_date: Mapped[datetime]
    update_date: Mapped[datetime]
    commercial_contact_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __repr__(self):
        return f"Client(id={self.id}, name={self.name}, contact_id={self.commercial_contact_id})"
