from fastapi import APIRouter, Form, Header, Query

from bonch import Settings
from server.app.errors.DefaultErrors import DefaultErrors
from server.core.utils.ResponseBuilder import ResponseBuilder

from bonch.timetable.BonchTimeTable import BonchTimeTable

router = APIRouter(
    prefix="/schedule"
)

@router.get(
    path="/day",
    tags=["Расписание"],
    summary="Получить расписание на день",
    responses=DefaultErrors().errors
)
async def get_day_schedule(
    miden=Settings.miden_key.value,
    day: int = Query(0, description="Номер дня в недели начинается с 1 по 7 включительно"),
    week: int = Query(0, description="Номер учебной недели начинается с 1 по 54 включительно"),
):
    """
    Если укзать 0, то вернет текущий день, если он есть.
    """
    if day < 8 and week < 55:
        day = BonchTimeTable(miden).day(day_number=day, week_number=week)
    else:
        return ResponseBuilder().bad_request()
    if day[0] == 200:
        return ResponseBuilder().result(data=day[1])
    else:
        return ResponseBuilder().result(info=day[1], status=day[0], data=None)

@router.get(
    path="/week",
    tags=["Расписание"],
    summary="Получить расписание на неделю",
    responses=DefaultErrors().errors
)
async def get_week_schedule(
    miden=Settings.miden_key.value,
    number: int = Query(0, description="Номер учебной недели начинается с 1 по 54 включительно"),
):
    week = BonchTimeTable(miden).week(number)
    if week[0] == 200:
        return ResponseBuilder().result(data=week[1])
    else:
        return ResponseBuilder().result(info=week[1], status=week[0], data=None)
