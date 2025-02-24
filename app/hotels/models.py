from app.database import Base
from sqlalchemy import Column, Integer, String, JSON, ForeignKey

# Класс для таблицы sql для hotels
class Hotels(Base):
    __tablename__ = "hotels"

    # Определение всех переменных
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)


# class Rooms(Base):
#     __tablename__ = "rooms"
#
#     id = Column(Integer, primary_key=True, nullable=False)
#     hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
#     name = Column(String, nullable=False)
#     description = Column(String)
#     price = Column(Integer, nullable=False)
#     services = Column(JSON, nullable=False)
#     quantity = Column(Integer, nullable=False)
#     image_id = Column(Integer)