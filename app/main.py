# from contextlib import asynccontextmanager
import time
from datetime import date
from typing import Optional
from sqladmin import Admin, ModelView
from fastapi import Depends, FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, UserAdmin
from app.bookings.router import router as router_bookings
from app.database import engine
from app.hotels.router import router as hotel_pages
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.users.models import Users
from app.users.router import router as router_users
from app.logger import logger
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# from redis import asyncio as aioredis
from prometheus_fastapi_instrumentator import Instrumentator


# Запуск приложения
app = FastAPI()
# uvicorn app.main:app --reload
# CMD ["gunicorn", "app.main:app", "--worker", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]


# Примонтировать картинки статитеские
app.mount("/static", StaticFiles(directory="app/static"), "static")


# Все роутеры
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_pages)
app.include_router(hotel_pages)
app.include_router(router_images)


# Площадка, которая может обращаться к нашему сайту
origins = [
    "http://localhost:3000",
]

# Настройки origins(взоимодействие фронтенда)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Autorization"]
)


# @asynccontextmanager
# async def lifespan(_: FastAPI):
#     redis = aioredis.from_url("redis://localhost")
#     FastAPICache.init(RedisBackend(redis), prefix="cache")
#     yield



instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
Instrumentator().instrument(app).expose(app)


# Админка
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    response.headers["X-Process-Time"] = str(process_time)
    return response
