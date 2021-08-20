from pydantic import Field

from server.core.models.DefaultResponseModel import DefaultResponseModel


class MessageHistoryHTTPStatus200Model(DefaultResponseModel):
    __data_example = {
        "sendto": 2233211,
        "history": [
            {
              "date": "30-06-2021 13:18:37",
              "name_fizlico": "Вы",
              "name": "Re: К590 Производственная практика",
              "annotation": "Это относится только к той производственной практике которая закончилась ?",
              "files": ""
            },
            {
              "date": "(см.Сообщения->Входящие)30-06-2021 09:27:43",
              "name_fizlico": "Кривоносова Наталья Викторовна",
              "name": "Производственная практика",
              "annotation": "Уважаемые студенты! Добрый день!<div>Сегодня до 18.00 срочно сдать все документы по практике - аттестационный лист, дневник, отчет. У некоторых студентов еще не сданы документы а майскую практику.&nbsp;</div><div>Если до 18.00 не успеваете - то приносить в кабинет 421 до 19.00, я завтра утром передам руководителю практики</div>",
              "files": ""
            }
        ]
      }
    info: str = Field("Сообжения успешно получены", description="Состояние получения сообщений")
    data: dict = Field(__data_example)

