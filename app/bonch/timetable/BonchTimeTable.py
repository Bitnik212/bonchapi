import requests
from bs4 import BeautifulSoup
from yaml import warnings

from bonch.BonchGetPage import BonchGetPage
from bonch import Settings
from bonch.auth import BonchAuth
from bonch.timetable.BonchTimeTableParser import BonchTimeTableParser


class BonchTimeTable:

    def __init__(self, miden: str):
        self.parse = BonchTimeTableParser()
        self.auth_wrapper = BonchAuth().auth_wrapper
        self.page = BonchGetPage(miden)

    def day(self) -> (int, list or str):
        """
        Расписания на день
        """
        status_code, response_text = self.auth_wrapper(self.page.timetable_response())
        if status_code == 200:
            parsed = self.parse.day(BeautifulSoup(response_text, "html.parser"))
            if parsed:
                return status_code, parsed
            else:
                return 404, "Не нашел расписания на этот день"
        else:
            return status_code, ""

    def week(self, week: int = 0) -> (int, list or str):
        """
        Получение страницы с раписанием и само расписание на неделю

        :return: dict
        """
        status_code, response_text = self.auth_wrapper(self.page.timetable_response(week))
        if status_code == 200:
            soup = BeautifulSoup(response_text, "html.parser")
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

    def otmetka(self, raspId: str = "", week_number: str = "") -> (int, str):
        """
        отметка на паре
        """
        # TODO Нужно протестить и похоошему сделать нормально
        if bool(raspId) and bool(week_number) is False:
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
            self.__send_otmetka(raspId, week_number)
            return 200, "Усепшно отмечен"

    @staticmethod
    def __send_otmetka(rasp: str, week: str):
        # TODO Сделать проверку на все случаи жизни
        r = requests.post(BonchGetPage.timetable_link,
                    data='open=1&rasp=' + rasp + '&week=' + week,
                    headers=Settings.headers.value)

