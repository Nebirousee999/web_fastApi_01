from app.database import Base
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Date, Computed
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    booking = relationship("Bookings", back_populates="user")

    def __str__(self):
        return f"User {self.email}"