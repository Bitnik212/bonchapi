from typing import Type, NamedTuple, Union
from datetime import date, datetime, time, timedelta

from pydantic import BaseModel


class BonchTimeTableItem:
    class Model(BaseModel):
        def __init__(self, **data):
            super().__init__(**data)
            self.building: BonchTimeTableItem.BuildingModel
            self.time: BonchTimeTableItem.TimeModel

        number: str
        name: str
        type: str
        remotely: bool
        prepod: str
        started_at: Union[str, None]
        link: Union[str, None]
        waiting: bool
        date: str

    class TimeModel(BaseModel):
        def __init__(self, **data):
            super().__init__(**data)
            self.parsed: BonchTimeTableItem.TimeParsedModel
        raw: str

    class TimeParsedModel(NamedTuple):
        start: str
        end: str

    class BuildingModel(NamedTuple):
        cabinet: str
        building: str
