from fastapi import APIRouter, Response, Depends
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.users.dependencies import get_current_user, get_current_admin_user
from app.users.models import Users

from app.users.schemas import SUserAuth
from app.users.dao import UsersDAO
from app.users.auth import get_passwords_hash, verify_password, authenticate_user, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth и Пользователи"]
)

# Пост запрос на регистрацию
# user_data: SUserAuth определяем заданный тип
@router.post("/register")
async def register_user(user_data: SUserAuth):
    # запрос в базу данных данного пользователя по почте
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)

    # Если он есть,то ошибка
    if existing_user:
        raise UserAlreadyExistsException

    # хэшируем пароль
    hash_password = get_passwords_hash(user_data.password)

    # Добавляем в базу
    await UsersDAO.add2(email=user_data.email, hashed_password=hash_password)

# Пост запрос на вход
@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):

    # Проверяем, есть ли такой в базе
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException

    # Добавляем данные в токен
    access_token = create_access_token({"sub": str(user.id)})

    # Добавить куку в ответ
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token

# Пост запрос на выход
@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("booking_access_token")

# гет запрос на конкретного пользователя
@router.get("/me")
async def read_users(current_user: Users = Depends(get_current_user)):
    return current_user

# гет запрос на всех пользователя
@router.get("/all")
async def read_users_all(current_user: Users = Depends(get_current_admin_user)):
    return await UsersDAO.find_all()
