from datetime import datetime
from fastapi import Request, Depends
from jose import jwt, JWTError
from app.config11 import settings
from app.exceptions import TokenExpiredException, TokenAbsentException, IncorrectTokenFormatException, \
    UsreIsNotPresentExeptions
from app.users.dao import UsersDAO
from app.users.models import Users

# Получение токена
def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token

# получение конкретного пользователя
async def get_current_user(token: str = Depends(get_token)):
    # Проверка
    try:
        # декодировать токен
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITM
        )
    except JWTError:
        raise IncorrectTokenFormatException

    # Получить время дейсвия токена
    expire: str = payload.get("exp")

    # Если нет токена или он перестал дейсвовать то ошибка
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException

    # Получение id пользователя из токена
    user_id: str = payload.get("sub")

    # Если нет пользователя то ошибка
    if not user_id:
        raise UsreIsNotPresentExeptions

    # Находим пользователя по id
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UsreIsNotPresentExeptions

    return user


async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
    # if current_user.role != "admin":
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return current_user