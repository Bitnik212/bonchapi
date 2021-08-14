from fastapi import APIRouter, Form

from bonch.auth import BonchAuth
from server.app.errors.SignInErrors import SignInErrors
from server.core.utils.ResponseBuilder import ResponseBuilder

router = APIRouter(
    prefix="/signin"
)


@router.post(
    path="",
    responses=SignInErrors().errors,
    tags=["Авторизация"],
    summary="Получение токена"
)
async def sign_in(
        login: str = Form(..., description="Логин"),
        password: str = Form(..., description="Пароль")
):
    """
    Авторизация пользователя
    """
    bonch = BonchAuth()
    token = bonch.sign_in(email=login, password=password)
    miden = token[1]
    status = token[0]
    if status != 200:
        return ResponseBuilder().result(data={}, info=miden)
    else:
        return ResponseBuilder().result(data={
            "miden": miden
        }, info="Токен успешно получен")
