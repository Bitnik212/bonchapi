from pydantic import Field

from app.server.core.models.DefaultResponseModel import DefaultResponseModel


class HTTPError422Model(DefaultResponseModel):
    __data_example = {
                "validation": {
                    "in": "",
                    "param": ""
                }
            }

    info: str = Field("Ошибка валидации", description="Дополнительная информация")
    data: dict = Field(__data_example)
