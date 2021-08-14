from pydantic import Field

from server.core.models.DefaultResponseModel import DefaultResponseModel


class SignInHTTPStatus200Model(DefaultResponseModel):
    __data_example = {
        "miden": "068ba78552bbd879cf2bf3e56dd4a4f0"
    }
    info: str = Field("Токен успешно получен", description="Состояние получения токена")
    data: dict = Field(__data_example)
