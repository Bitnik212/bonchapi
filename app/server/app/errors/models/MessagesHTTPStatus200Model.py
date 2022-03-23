from typing import Type, List

from pydantic import Field

from bonch.msg.BonchMessageModel import BonchMessageModel
from server.core.models.DefaultResponseModel import DefaultResponseModel


class MessagesHTTPStatus200Model(DefaultResponseModel):
    __data_example = [
        {
            "id": 2267814,
            "readed": False,
            "sender": "ФИО",
            "date": "15-08-2021",
            "time": "15:37:12",
            "title": "Заголовок",
            "files": [
                {
                    "name": "",
                    "href": ""
                }
            ]
        }
    ]
    info: str = Field("Сообжения успешно получены", description="Состояние получения сообщений")
    data: List[BonchMessageModel] = [BonchMessageModel(**data) for data in __data_example]
