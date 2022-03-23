from pydantic import Field

from app.server.core.models.DefaultResponseModel import DefaultResponseModel


class HTTPError500Model(DefaultResponseModel):
    info: str = Field("Внутрняя ошибка сервера", description="Дополнительная информация")
