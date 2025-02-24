from passlib.context import CryptContext
from pydantic import EmailStr
from datetime import datetime, timedelta
from app.config11 import settings
from app.users.dao import UsersDAO
from jose import jwt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# хешировать пароль
def get_passwords_hash(password: str) -> str:
    return pwd_context.hash(password)

# проверка пароля
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# access токен
def create_access_token(data:dict) -> str:
    # копировать словарь
    to_encode = data.copy()

    # время заканчивая действия токена
    expire = datetime.utcnow() + timedelta(minutes=30)

    #Обновление словарика
    to_encode.update({"exp": expire})

    # кодирование
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITM
    )
    return encoded_jwt


# аутентификация пользователя
async def authenticate_user(email: EmailStr, password: str):
    # Найти пользователя из базы по почте
    user = await UsersDAO.find_one_or_none(email=email)
    if not user and verify_password(password, user.hashed_password):
        return None

    return user