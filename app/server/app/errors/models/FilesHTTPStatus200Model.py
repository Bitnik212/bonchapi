from pydantic import Field

from server.core.models.DefaultResponseModel import DefaultResponseModel


class FilesHTTPStatus200Model(DefaultResponseModel):
    __data_example = {
        "name": "",
        "link": "",
        "idinfo": 0
    }
    info: str = Field("Файл успешно загружен", description="Состояние загрузки файла")
    data: dict = Field(__data_example)
