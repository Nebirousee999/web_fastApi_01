from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
import asyncio
from app.config11 import settings
#alembic revision --autogenerate -m "Initial migration"
#alembic upgrade head
#import config11


# Условия для тестовой базы данных и нормальной
if settings.MODE == "TEST":
    DATABASE_URL = settings.get_test_database_url()
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.get_database_url()
    DATABASE_PARAMS = {}


# Варианты для сессиис базой данных
engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
ses_mark = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

