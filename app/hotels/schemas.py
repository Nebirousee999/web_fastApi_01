from pydantic import BaseModel
from datetime import date

class Sbooking(BaseModel):
    id: int
    room_id: int
    user_i: int
    date_from: date
    date_to: date
    price: int

    class Config:
        orm_mode = True