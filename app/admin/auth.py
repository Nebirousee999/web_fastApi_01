from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.exceptions import IncorrectEmailOrPasswordException
from app.users.auth import authenticate_user, create_access_token
from app.users.dependencies import get_current_user

"""
Класс для логирования админа
"""

# Аутентификация админа
class AdminAuth(AuthenticationBackend):
    # Логирование админа
    async def login(self, request: Request, user_data=None) -> bool:
        # форма для админа
        form = await request.form()
        email, password = form["username"], form["password"]

        # Ищет админа в базе
        user = await authenticate_user(email, password)
        if user:
            # Обновляет токен с таким пользователем
            access_token = create_access_token({"sub": str(user.id)})
            request.session.update({"token": access_token})
        return True

    # Выход их профиля
    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    # Аутентификация админа
    async def authenticate(self, request: Request) -> bool:
        # Получаем текущий токен
        token = request.session.get("token")
        if not token:
            return False

        # Определяем этого пользователя
        user = await get_current_user(token)
        if not user:
            return False

        # Check the token in depth
        return True


authentication_backend = AdminAuth(secret_key="...")
