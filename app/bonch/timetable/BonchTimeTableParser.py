from bs4 import BeautifulSoup

from bonch import Settings
import datetime

from bonch.BonchGetPage import BonchGetPage
from bonch.auth import BonchAuth
from bonch.timetable.BonchTimeTableItemModel import BonchTimeTableItem


class BonchTimeTableParser:

    def __init__(self):
        self.domain = Settings.domain.value
        self.auth_wrapper = BonchAuth().auth_wrapper
        self.days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']

    @property
    def __now_date(self) -> str:
        """
        """
        return datetime.datetime.now().isoformat().split('T')[0].split("-")[2] + '.' + \
               datetime.datetime.now().isoformat().split('T')[0].split("-")[1] + '.' + \
               datetime.datetime.now().isoformat().split('T')[0].split("-")[0]

    @property
    def __reverse_now_date(self) -> str:
        """
        """
        return datetime.datetime.now().isoformat().split('T')[0]

    def day(self, soup: BeautifulSoup) -> dict or None:
        """
        Парсер расписания на день

        :param soup: soup элемент с страницей расписания на неделю
        :return: словарь или None если не нашел
        """
        # перевод в формат 2020-10-25 из 25.10.2020
        # revnowdate = date.split("-")[2] + '.' + date.split("-")[1] + '.' + date.split("-")[0]
        try:
            resp = []
            if soup.find(string=self.__now_date).parent.parent.parent.next_sibling.next_sibling == \
                    soup.find_all('tr', attrs={'style': 'background: #FF9933 !important '})[0]:
                for item in soup.find_all('tr', attrs={'style': 'background: #FF9933 !important '}):
                    resp.append(dict(self.__parse_item(item, self.__reverse_now_date)))
            return resp
        except IndexError:
            return None

    @staticmethod
    def __parse_item(item: BeautifulSoup, revnowdate: str) -> BonchTimeTableItem().Model:
        """
        Парсер пары

        :param item: soup элемент с парой
        :param revnowdate: str. Время
        """

        para = item.find_all('td')[0].text.split('(')[0].replace(' ', '')
        paratime = item.find_all('td')[0].text.split('(')[1].replace(')', '').replace(' ', '')
        paratimeparsed = [revnowdate.replace('.', '-') + "T" + paratime.split('-')[0] + ":00",
                          revnowdate.replace('.', '-') + "T" + paratime.split('-')[1] + ":00"]
        itemname = item.find_all('td')[1].b.text
        itemtype = item.find_all('td')[1].small.text.split('  занятие началось ')[0]
        global attended, link, remote, waiting
        attended = waiting = False
        startedat = link = None
        item4 = item.find_all('td')[4]
        item4a = ""
        # print(item4.text)
        try:
            item4a = item4.a['title']
        except TypeError:
            pass
        if item4.text == "" and item4a != "Ссылка на видеолекцию":
            # print(1)
            try:
                startedat = item.find_all('td')[1].small.text.split(' занятие началось ')[1]
                attended = True
                ended = True
            except IndexError:
                # attended = False
                ended = True
        elif item4a == "Ссылка на видеолекцию":
            # print(2)
            link = item4.a['href'].replace(" ", "")
            try:  # фикс на одновременно ссылка и время
                startedat = item4.text
                startedat = item.find_all('td')[1].small.text.split(' занятие началось ')[1]
                attended = True
            except:
                pass
        elif item4.text == "ждем начала от преподавателяПопробуйте обновить страницу через минуту.":
            # print(3)
            attended = False
            waiting = True
        else:
            # print(4)
            attended = True
            ended = False
            startedat = item4.text
        remote = False
        try:
            if item.find_all('td')[2].text == "Дистанционно":
                remote = True
        except TypeError:
            pass

        if remote:
            cabinet = building = None
        else:
            build = item.find_all('td')[2].text.replace(" ", "").split(';')
            cabinet = build[0]
            building = build[1]
        prepod = item.find_all('td')[3].text

        if startedat == "ждем начала от преподавателяПопробуйте обновить страницу через минуту.":
            startedat = None
            waiting = True
        if startedat is None:
            ended = False

        return BonchTimeTableItem().Model(
            time=BonchTimeTableItem().TimeModel(
                raw=paratime,
                parsed=BonchTimeTableItem.TimeParsedModel(
                    start=paratimeparsed[0],
                    end=paratimeparsed[1]
                )
            ),
            number=para,
            name=itemname,
            type=itemtype,
            remotely=remote,
            prepod=prepod,
            started_at=startedat,
            link=link,
            waiting=waiting,
            date=revnowdate,
            building=BonchTimeTableItem.BuildingModel(
                cabinet=cabinet,
                building=building
            )
        )

    def week(self, soup: BeautifulSoup) -> dict or None:
        """
        Парсер недели

        :param soup:
        :return: list
        """
        try:
            resp = {day: "" for day in self.days}
            trigger = True
            now_item_name = now_item_date = ""
            tbody = soup.find("tbody", attrs={'style': 'text-shadow:none;'})
            for tag in tbody.find_all('tr'):
                if tag.b.text in self.days:
                    now_item_name = tag.b.text
                    now_item_date = tag.small.text
                    resp[now_item_name] = []
                    trigger = False
                else:
                    trigger = True
                if trigger:
                    parsed_item = self.__parse_item(tag, now_item_date)
                    resp[now_item_name].append(parsed_item)
            return resp
        except:
            return None

    @staticmethod
    def __convert_date_to_ico(date):
        return date.split(".")[2] + '-' + date.split(".")[1] + '-' + date.split(".")[0]
