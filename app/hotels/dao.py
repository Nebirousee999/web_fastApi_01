from app.dao.base import BaseDAO
from app.hotels.models import Hotels


# наследование от базового класса по sql запросам
class HotelDAO(BaseDAO):# SQL запрос по отелям
    # запросы по отелям
    model = Hotels

