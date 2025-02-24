
from app.database import async_session_maker
from app.users.models import Users
from sqlalchemy import select
from app.dao.base import BaseDAO


class UsersDAO(BaseDAO):
    model = Users