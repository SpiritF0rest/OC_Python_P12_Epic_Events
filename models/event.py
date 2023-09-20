from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True)
    contract_id: Mapped[int] = mapped_column(ForeignKey("contract.id"))
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"))
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]
    support_contact_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    location: Mapped[str] = mapped_column(String(255))
    attendees: Mapped[int]
    notes: Mapped[str]
    creation_date: Mapped[datetime]
    update_date: Mapped[datetime]

    def __repr__(self):
        return (f"Event(id={self.id}, contract_id={self.contract_id}, client_id={self.client_id}, "
                f"contact_id={self.support_contact_id})")
