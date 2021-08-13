import requests
from bs4 import BeautifulSoup as bs
from app.bonch import Settings


class BonchSearch:

    def __init__(self, miden: str):
        self.domain = Settings.domain
        self.timeout = Settings.timeout
        self.cookies = requests.cookies.RequestsCookieJar()
        self.cookies.set('miden', miden, domain=self.domain, path="/")
        self.searchlinkbyname = "https://" + self.domain + "/cabinet/subconto/search.php"
        self.searchlinkbyid = "https://" + self.domain + "/cabinet/subconto/subcontokeytable.php"

    def userbyname(self, fio: str = None):
        """
        Поиск людей из бонча по ФИО. Пример Аааааа А.А.

        :param fio: ФИО пользователя
        :return: dict
        """
        # todo Сделать все остальные обработки на все случаи жизни
        # todo сделать обработку на 404 когда ничего не нашел
        s = requests.Session()
        params = {}
        if fio != None:
            params.update({"value": fio})
        url = self.searchlinkbyname
        try:
            r = s.get(url, params=params, cookies=self.cookies, timeout=self.timeout)
            soup = bs(r.text, "html.parser")
            res = self.parseuserbyname(soup)
            if len(r.text) < 400:
                return {'status': 401}
            else:
                return {"status": 200, "responce": res}
        except requests.exceptions.Timeout or requests.exceptions.ReadTimeout:
            return {"status": 523}

    def parseuserbyname(self, soup):
        """
        Парсер для userbyname
        :param soup:
        :return: list
        """
        username = ""
        id = 0
        res = []
        for user in soup.find("tbody").find_all("tr"):
            username = user.text.split(' (')[0]
            id = user.text.split(' (')[1].replace("id=", '').replace(')', '')
            res.append({"fio": username, "id": id})
        return res

    def fullfio(self, fio: str):
        """

        :param fio:
        :return:
        """
        # todo Сделать все остальные обработки на все случаи жизни
        s = requests.Session()
        params = {}
        if fio != None:
            params.update({"value": fio, "pole": "student"})
        url = self.searchlinkbyname
        try:
            r = s.get(url, params=params, cookies=self.cookies, timeout=self.timeout)
            soup = bs(r.text, "html.parser")
            res = self.parsefullfio(soup)
            if len(r.text) < 400:
                return {'status': 401}
            else:
                return {"status": 200, "responce": res}
        except requests.exceptions.Timeout or requests.exceptions.ReadTimeout:
            return {"status": 523}

    def parsefullfio(self, soup):
        """

        :param soup:
        :return:
        """
        username = ""
        temp = ""
        res = []
        for user in soup.find("tbody").find_all("tr"):
            username = user.text.split(' (')[0]
            if temp == username:
                continue
            temp = username
            res.append({"username": username})
        return res

    def userbyid(self, id: int):
        """

        :param id:
        :return: dict
        """
        # todo Сделать все остальные обработки на все случаи жизни
        s = requests.Session()
        params = {"key": id, "s": "fizlico"}
        url = self.searchlinkbyid
        try:
            r = s.get(url, params=params, cookies=self.cookies, timeout=self.timeout)
            print(r.url)
            soup = bs(r.text, "html.parser")
            try:
                res = self.parseruserbyid(soup)
            except:
                return {"status": 404}
            if len(r.text) < 400:
                return {'status': 401}
            else:
                return {"status": 200, "responce": res}
        except requests.exceptions.Timeout or requests.exceptions.ReadTimeout:
            return {"status": 523}

    def parseruserbyid(self, soup):
        """

        :param soup:
        :return: list
        """
        res = []
        tbody = soup.find_all("table", attrs={'style': 'width:100%'})[1]
        for user in tbody.find_all('tr'):
            fio = user.find_all('td')[0].text
            id = user.find_all('td')[1].text
            res.append({"fio": fio, "id": id})
        return res

# search = BonchSearch("ce796888c2e5c06b7c8c6a6baa59fc9e")
# print(search.userbyname("Никоноров Н.В."))
