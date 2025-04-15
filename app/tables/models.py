from sqlalchemy.orm import Mapped, relationship

from app.database import Base, str_uniq


class Table(Base):
    name: Mapped[str_uniq]
    seats: Mapped[int]
    location: Mapped[str]

    reservations = relationship("Reservation", back_populates="table")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"name={self.name}, "
                f"seats={self.seats})")

    def __repr__(self):
        return str(self)
