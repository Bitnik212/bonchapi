from fastapi import APIRouter, Form

from bonch.auth import BonchAuth
from server.core.models.HTTPErrors import HTTPErrors
from server.core.utils.ResponseBuilder import ResponseBuilder

"""
Авторизация пользователя
"""
router = APIRouter(
    prefix="/signin"
)
bonch = BonchAuth()


@router.post(
    path="",
    responses=HTTPErrors().errors,
    tags=["Авторизация"],
    summary="Получение токена"
)
async def sign_in(
        login: str = Form(..., description="Логин"),
        password: str = Form(..., description="Пароль")
):
    miden = bonch.login(email=login, password=password)
    return ResponseBuilder().result({"miden": miden}, "Токен получен")
