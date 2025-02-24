from fastapi import APIRouter, Request, Depends
from datetime import date
from app.bookings.dao import BookingDAO
from app.bookings.schemas import Sbooking
from app.exceptions import RoomCannotBooked
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/booking",
    tags=["Бронирование"]
)

#Get запрос на вывод всех пользователей
# Проверка на валидность пользователя(куки)
@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)):
    return await BookingDAO.find_all(user_id=user.id)


#Пост запрос на бронт номера
@router.post("")
async def add_bookings(
        room_id: int, date_from: date, date_to: date,
        user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add33(user.id, room_id, date_from, date_to )
    if not booking:
        raise RoomCannotBooked