#############  FROM MAIN ********************
# class Shotel(BaseModel):
#     address: str
#     name: str
#     stars: int
#
# class HotelsSearchArgs:
#     def __init__(self,
#                  locations: str,
#                  date_from: date,
#                  date_to: date,
#                  stars: Optional[int] = None,
#                  has_spa: Optional[bool] = Query(None, ge=1, le=5),
#                  ):
#         self.locations = locations
#         self.date_from = date_from
#         self.date_to = date_to
#         self.stars = stars
#         self.has_spa = has_spa
#
#
#
#
# @app.get("/hotels/")
# def get_hotels(
#         search_args: HotelsSearchArgs=Depends()
#
# ):
#     # hotels = [
#     #     {
#     #         "address": "улю Гагарина, 1, Алтай",
#     #         "name": "Super Hotel",
#     #         "stars": 5,
#     #     }
#     # ]
#
#     return search_args
#
# class SBooking(BaseModel):
#     room_id: int
#     date_from: date
#     date_to: date
#
#
#
# @app.post("/bookings")
# def add_bookings(bookings: SBooking):
#     pass
#############  FROM MAIN ********************