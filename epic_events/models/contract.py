from datetime import datetime
from typing import Literal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from epic_events.models.base import Base

Status = Literal["SIGNED", "UNSIGNED"]


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    total_amount: Mapped[int]
    left_to_pay: Mapped[int]
    status: Mapped[Status]
    creation_date: Mapped[datetime] = mapped_column(insert_default=datetime.utcnow())
    update_date: Mapped[datetime] = mapped_column(insert_default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __repr__(self):
        return f"Contract(id={self.id}, client_id={self.client_id}, status={self.status})"
