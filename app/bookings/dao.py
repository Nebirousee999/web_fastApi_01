from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.logger import logger
from app.database import engine
from app.bookings.models import Bookings
from sqlalchemy import select, and_, or_, func, insert
from app.dao.base import BaseDAO
from app.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    # сложный запрос sql
    @classmethod
    async def add33(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date
    ):
        try:
            async with AsyncSession(engine) as session:
                ### запрос SQL Узнать есть ли свободный номер на такое число
                booked_rooms = select(Bookings).where(
                    and_(
                        Bookings.room_id == 1,
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to >= date_from
                            )
                        )
                    )
                ).cte()

                get_rooms_left = select(
                    (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
                ).select_from(Rooms).join(
                    booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
                ).where(Rooms.id == room_id).group_by(
                    Rooms.quantity, booked_rooms.c.room_id
                )
                ################

                print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))
                result = await session.execute(get_rooms_left)

                rooms_left: int = result.scalar()

                # Если есть свободные номера то
                if rooms_left > 0:
                    #Получаем цену этого номера
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price1 = await session.execute(get_price)
                    price: int = price1.scalar()

                    #Добавляем в базу заказ
                    add_booking = insert(Bookings).values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    ).returning(Bookings)
                    new_bookung = await session.execute(add_booking)
                    await session.commit()
                    return new_bookung.scalar()

                else:
                    return None

        # Если не получается запрос то делаем лог
        except (SQLAlchemyError, Exception) as e:
            #Првоерка типа ошибки
            if isinstance(e, SQLAlchemyError):
                msg1 = "Database Exc"
            elif isinstance(e, Exception):
                msq1 = "Unknown Exc"

            # Сбор данных для ошибки
            msg = f"{msg1}: Cannot add booking"
            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
            }

            # Отправка данных в лог
            logger.error(
                msg, extra=extra, exc_info=True
            )