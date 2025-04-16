from sqlalchemy.orm import Mapped, relationship

from app.database import Base, str_uniq


class Table(Base):
    """
    Модель "Стол" для хранения информации о столиках в ресторане.

    Fields:
        name (str): Уникальное название столика.
        seats (int): Количество посадочных мест за столом.
        location (str): Местоположение столика в зале.
        reservations: Бронировния, привязанные
        к данному столу.
    """
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
