from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Reservation(Base):
    customer_name: Mapped[str]
    reservation_time: Mapped[datetime]
    duration_minutes: Mapped[int]

    table_id: Mapped[int] = mapped_column(
        ForeignKey("table.id"), nullable=False
    )
    table: Mapped["Table"] = relationship("Table", back_populates="reservations")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"reservation_time={self.reservation_time}, "
                f"duration_minutes={self.duration_minutes})")

    def __repr__(self):
        return str(self)
