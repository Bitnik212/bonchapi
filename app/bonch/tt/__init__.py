import requests
import datetime
from bs4 import BeautifulSoup as bs

from app.bonch.BonchGetPage import BonchGetPage


class BonchTimeTable:

    def __init__(self, miden: str):
        self.domain = "lk.sut.ru"
        self.nowdate = datetime.datetime.now().isoformat().split('T')[0].split("-")[2] + '.' + \
                       datetime.datetime.now().isoformat().split('T')[0].split("-")[1] + '.' + \
                       datetime.datetime.now().isoformat().split('T')[0].split("-")[0]
        self.revnowdate = datetime.datetime.now().isoformat().split('T')[0]

    def day(self, miden): #, date: str
        """
        Метод получения расписания на день

        :return: dict
        """

        try:
            r = BonchGetPage(miden).timetable_response()
            soup = bs(r.text, "html.parser")
            if r.status_code == 500 or r.status_code == 504:
                return {"status": 523}
            else:
                if len(r.text) < 400:
                    return {'status': 401}
                else:
                    try:
                        res = self.parsedaynow(soup)
                        if res['status'] == 404:
                            return {"status": 404}
                        else:
                            return {"status": 200, "responce": res['responce']}
                    except AttributeError:
                        return {"status": 404}
        except requests.exceptions.Timeout or requests.exceptions.ReadTimeout:
            return {"status": 523}

    def week(self, miden: str, week: int = 0):
        """
        Получение страницы с раписанием и само расписание на неделю

        :return: dict
        """
        # todo сделаит обработки событий на все случаи жизни
        if week != 0:
            r = BonchGetPage(miden).timetable_response(week)
        else:
            r = BonchGetPage(miden).timetable_response()
        soup = bs(r.text, "html.parser")
        if soup.find(string="Занятий не найдено"):
            resp = {"status": 404}
        else:
            resp = {"status": 200, "responce": self.parseweek(soup)}
        return resp

    def parsedaynow(self, soup):
        """
        Парсер расписания на день

        :param soup: soup элемент с страницей расписания на неделю
        :return: list
        """
        # перевод в формат 2020-10-25 из 25.10.2020
        # revnowdate = date.split("-")[2] + '.' + date.split("-")[1] + '.' + date.split("-")[0]
        try:
            resp = []
            if soup.find(string=self.nowdate).parent.parent.parent.next_sibling.next_sibling == \
                    soup.find_all('tr', attrs={'style': 'background: #FF9933 !important '})[0]:
                for item in soup.find_all('tr', attrs={'style': 'background: #FF9933 !important '}):
                    resp.append(self.parseitem(item, self.revnowdate))
            return {"status": 200, "responce": resp}
        except IndexError:
            return {"status": 404}

    def parseitem(self, item, revnowdate):
        """
        Парсер пары

        :param item: soup элемент с парой
        :param revnowdate: str. Время
        :return: dict
        """

        para = item.find_all('td')[0].text.split('(')[0].replace(' ', '')
        paratime = item.find_all('td')[0].text.split('(')[1].replace(')', '').replace(' ', '')
        paratimeparsed = [revnowdate.replace('.', '-') + "T" + paratime.split('-')[0] + ":00",
                          revnowdate.replace('.', '-') + "T" + paratime.split('-')[1] + ":00"]
        itemname = item.find_all('td')[1].b.text
        itemtype = item.find_all('td')[1].small.text.split('  занятие началось ')[0]
        global attended, link, remote, waiting
        attended = False
        ended = False
        startedat = None
        item4 = item.find_all('td')[4]
        item4a = ""
        link = None
        waiting = False
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
            try: # фикс на одновременно ссылка и время
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
        return {
                    "number": para,
                    "time": {
                        "time": paratime,
                        "parsed": {
                            "start": paratimeparsed[0],
                            "end": paratimeparsed[1]
                        }
                    },
                    "name": itemname,
                    "type": itemtype,
                    "remotely": remote,
                    "build": {
                        "cabinet": cabinet,
                        "building": building
                    },
                    "prepod": prepod,
                    # "attended": attended,
                    # "ended": ended,
                    "startedat": startedat,
                    "link": link,
                    "waiting": waiting,
                    "date": revnowdate
                }

    def parseweek(self, soup):
        """
        Парсер недели

        :param soup:
        :return: list
        """
        dates = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        resp = {"Понедельник": [], "Вторник": [], "Среда": [], "Четверг": [], "Пятница": [], "Суббота": []}
        tbody = soup.find("tbody", attrs={'style': 'text-shadow:none;'})
        for tag in tbody.find_all('tr', attrs={"style": "background: #b3b3b3; !important; "}):
            # Понедельник
            if tag.b.text == dates[0]:
                date = self.confertdatetoico(tag.small.text)
                trigger = False
                for iteem in tbody.find_all('tr'):
                    if iteem.b.text == dates[0]:
                        trigger = True
                        continue
                    if trigger:
                        try:
                            if iteem['style'] == "background: #b3b3b3; !important; ":
                                break
                        except KeyError:
                            pass
                        # print(iteem)
                        resp[dates[0]].append(self.parseitem(iteem, date))
            # Вторник
            if tag.b.text == dates[1]:
                date = self.confertdatetoico(tag.small.text)
                trigger = False
                for iteem in tbody.find_all('tr'):
                    if iteem.b.text == dates[1]:
                        trigger = True
                        continue
                    if trigger:
                        try:
                            if iteem['style'] == "background: #b3b3b3; !important; ":
                                break
                        except KeyError:
                            pass
                        # print(iteem)
                        resp[dates[1]].append(self.parseitem(iteem, date))
            # Среда
            if tag.b.text == dates[2]:
                date = self.confertdatetoico(tag.small.text)
                # print(date)
                trigger = False
                for iteem in tbody.find_all('tr'):
                    if iteem.b.text == dates[2]:
                        trigger = True
                        continue
                    if trigger:
                        try:
                            if iteem['style'] == "background: #b3b3b3; !important; ":
                                break
                        except KeyError:
                            pass
                        # print(iteem)
                        resp[dates[2]].append(self.parseitem(iteem, date))
            # Четверг
            if tag.b.text == dates[3]:
                date = self.confertdatetoico(tag.small.text)
                trigger = False
                for iteem in tbody.find_all('tr'):
                    if iteem.b.text == dates[3]:
                        trigger = True
                        continue
                    if trigger:
                        try:
                            if iteem['style'] == "background: #b3b3b3; !important; ":
                                break
                        except KeyError:
                            pass
                        # print(iteem)
                        resp[dates[3]].append(self.parseitem(iteem, date))
            # Пятница
            if tag.b.text == dates[4]:
                date = self.confertdatetoico(tag.small.text)
                trigger = False
                for iteem in tbody.find_all('tr'):
                    if iteem.b.text == dates[4]:
                        trigger = True
                        continue
                    if trigger:
                        try:
                            if iteem['style'] == "background: #b3b3b3; !important; ":
                                break
                        except KeyError:
                            pass
                        # print(iteem)
                        resp[dates[4]].append(self.parseitem(iteem, date))
            # Суббота
            if tag.b.text == dates[5]:
                date = self.confertdatetoico(tag.small.text)
                trigger = False
                for iteem in tbody.find_all('tr'):
                    if iteem.b.text == dates[5]:
                        trigger = True
                        continue
                    if trigger:
                        try:
                            if iteem['style'] == "background: #b3b3b3; !important; ":
                                break
                        except KeyError:
                            pass
                        # print(iteem)
                        resp[dates[5]].append(self.parseitem(iteem, date))

        return resp

    def parseday(self, soup, date):
        """

        :param soup:
        :param date:
        :return:
        """
        trigger = False
        for item in soup.find("tbody", attrs={'style': 'text-shadow:none;'}).find_all('tr'):
            if item.small.text == date:
                trigger = True
            elif item.small.text != date:
                trigger = False

            if trigger:
                pass

    def confertdatetoico(self, date):
        return date.split(".")[2] + '-' + date.split(".")[1] + '-' + date.split(".")[0]

    def otmetka(self):
        """
        Автоотметка на паре

        :return:
        """
        r = BonchGetPage(self.miden).timetable_response()
        soup = bs(r.text, "html.parser")
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
                self.sendotmetka(rasp, week)
                return {"status": 200}
            else:
                continue
        return 0

    def sendotmetka(self, rasp: str, week: str):
        self.s.post(BonchGetPage.timetabl,
                    data='open=1&rasp=' + rasp + '&week=' + week,
                    headers=self.headers)

tt = BonchTimeTable("4e3004656bff82fc3be0ab2352db0e29")
print(tt.day("4e3004656bff82fc3be0ab2352db0e29"))
