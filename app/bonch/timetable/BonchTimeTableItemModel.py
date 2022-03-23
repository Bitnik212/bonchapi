from typing import Type, NamedTuple, Union, List

from pydantic import BaseModel


class BonchTimeTableItem:
    class TimeModel(BaseModel):
        raw: str
        parsed: List[str]

    class TimeParsedModel(NamedTuple):
        start: str
        end: str

    class BuildingModel(NamedTuple):
        cabinet: str
        building: str


class BonchTimeTableItemModel(BaseModel):
    number: str
    name: str
    type: str
    remotely: bool
    prepod: str
    started_at: Union[str, None]
    link: Union[str, None]
    waiting: bool
    date: str
    building: BonchTimeTableItem.BuildingModel
    time: BonchTimeTableItem.TimeModel
