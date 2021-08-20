from pydantic import Field

from server.core.models.DefaultResponseModel import DefaultResponseModel


class DefaultHTTPStatus200Model(DefaultResponseModel):
    __data_example = {
        "name": "",
        "link": "",
        "idinfo": 0
    }
    data: dict = Field(__data_example)
