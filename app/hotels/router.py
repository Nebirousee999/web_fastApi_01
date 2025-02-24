
from fastapi import APIRouter, Request, Depends
from app.hotels.dao import HotelDAO
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/Hotels",
    tags=["Отели"]
)

# get запрос на сервер
@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)):

    # запрос в базу данных
    return await HotelDAO.find_all()

