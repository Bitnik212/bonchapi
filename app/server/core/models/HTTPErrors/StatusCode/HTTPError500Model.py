from pydantic import Field

from server.core.models.DefaultResponseModel import DefaultResponseModel


class HTTPError500Model(DefaultResponseModel):
    info: str = Field("Внутрняя ошибка сервера", description="Дополнительная информация")
