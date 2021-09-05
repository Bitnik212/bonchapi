import requests
from bs4 import BeautifulSoup
import datetime as dt

from bonch.BonchGetPage import BonchGetPage
from bonch import Settings
from bonch.auth import BonchAuth
from bonch.timetable.BonchTimeTableParser import BonchTimeTableParser


class BonchTimeTable:

    def __init__(self, miden: str):
        self.parse = BonchTimeTableParser()
        self.auth_wrapper = BonchAuth().auth_wrapper
        self.page = BonchGetPage(miden)

    @property
    def PARSER_TYPE(self) -> str:
        return "html.parser"

    @property
    def __now_day_number(self) -> int:
        return dt.datetime.now().weekday()

    @property
    def __now_day_number_iso(self) -> int:
        return dt.datetime.now().isoweekday()

    def day(self, day_number: int = 0, week_number: int = 0) -> (int, list or str):
        """
        Расписания на день
        """
        status_code, response_text = self.auth_wrapper(self.page.timetable_response(week_number))
        if status_code == 200:
            parsed = self.parse.week(BeautifulSoup(response_text, self.PARSER_TYPE))
            if parsed:
                if week_number or day_number:
                    parsed = parsed[self.parse.days[day_number-1]]
                else:
                    parsed = parsed[self.parse.days[self.__now_day_number]]
                if parsed == "":
                    return 404, "Не нашел расписания на этот день"
                else:
                    return status_code, parsed
            else:
                return 500, "Не получилось спарсить расписания на этот день"
        else:
            return status_code, ""

    def week(self, week: int = 0) -> (int, dict or str):
        """
        Получение страницы с раписанием и само расписание на неделю

        :return: dict
        """
        status_code, response_text = self.auth_wrapper(self.page.timetable_response(week))
        if status_code == 200:
            soup = BeautifulSoup(response_text, self.PARSER_TYPE)
            if soup.find(string="Занятий не найдено"):
                return 404, "Занятий не найдено"
            else:
                parsed = self.parse.week(soup)
                if parsed:
                    return 200, parsed
                else:
                    return 404, "Не нашел такую неделю"
        else:
            return status_code, ""

    def otmetka(self, schedule_id: str = "", week_number: str = "") -> (int, str):
        """
        отметка на паре
        """
        # TODO Нужно протестить и похорошему сделать нормально
        if bool(schedule_id) and bool(week_number) is False:
            r = self.page.timetable_response()
            status_code, response_text = self.auth_wrapper(r)
            if status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                for i in soup.find_all('a'):
                    if (i.get_text() == "Начать занятие"):
                        data = str(i)
                        for i in range(len(data)):
                            if (data[i] == '('):
                                a = i
                                b = i
                                while (data[a] != ')'):
                                    a += 1
                        text = data[b + 1:a]
                        rasp = text.split(",")[0]
                        week = text.split(",")[1]
                        self.__send_otmetka(rasp, week)
                        return 200, "Усепшно отмечен"
                    else:
                        continue
            return 200, "Усепшно отмечен"
        else:
            self.__send_otmetka(schedule_id, week_number)
            return 200, "Усепшно отмечен"

    @staticmethod
    def __send_otmetka(rasp: str, week: str):
        # TODO Сделать проверку на все случаи жизни
        r = requests.post(BonchGetPage.timetable_link,
                    data='open=1&rasp=' + rasp + '&week=' + week,
                    headers=Settings.headers.value)

