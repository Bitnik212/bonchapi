import requests
from app.bonch import Settings


class BonchGetPage:
    def __init__(self, miden: str):
        """
        Инициализация класса

        :param miden: str - токен
        """
        self.domain = Settings.domain
        self.jar = requests.cookies.RequestsCookieJar()
        self.jar.set('miden', miden, domain=self.domain, path="/")
        self.timeout = Settings.timeout
        self.home = "https://lk.sut.ru/cabinet/"
        self.auth = "https://"+self.domain+"/cabinet/lib/autentificationok.php?"
        self.loginlink = "https://"+self.domain+"/cabinet/?login=yes"
        self.updatemiden = "https://"+self.domain+"/cabinet/lib/updatesession.php"
        self.timetabl = "https://"+self.domain+"/cabinet/project/cabinet/forms/raspisanie_bak.php"
        self.vedomost = "https://"+self.domain+"/cabinet/project/cabinet/forms/vedomost.php"
        self.zachetka = "https://"+self.domain+"/cabinet/project/cabinet/forms/zachetka.php"
        self.uch_grafik = "https://"+self.domain+"/cabinet/project/cabinet/forms/uch_grafik.php"
        self.facultativ = "https://"+self.domain+"/cabinet/project/cabinet/forms/fakultativ.php"
        self.dolg = "https://"+self.domain+"/cabinet/project/cabinet/forms/dolg.php"
        self.prikazi = "https://"+self.domain+"/cabinet/project/cabinet/forms/prikazs.php"
        self.portfolio = "https://"+self.domain+"/cabinet/project/cabinet/forms/portfolio.php"
        self.groupfiles = "https://"+self.domain+"/cabinet/project/cabinet/forms/files_group_pr.php"
        self.dnevnik = "https://"+self.domain+"/cabinet/project/cabinet/forms/jurnal_dnevnik.php"
        self.profil = "https://"+self.domain+"/cabinet/project/cabinet/forms/profil.php"
        self.settings = "https://"+self.domain+"/cabinet/project/cabinet/forms/nastroyki.php"
        self.changepassword = "https://"+self.domain+"/cabinet/project/cabinet/forms/change.php"
        self.services = "https://"+self.domain+"/cabinet/project/cabinet/forms/wifi.php"
        self.ump = "https://"+self.domain+"/cabinet/project/cabinet/forms/ump.php"
        self.library = "https://"+self.domain+"/cabinet/project/cabinet/forms/library.php"
        self.messagesin = "https://"+self.domain+"/cabinet/project/cabinet/forms/message.php?type=in"
        self.messagesout = "https://"+self.domain+"/cabinet/project/cabinet/forms/message.php?type=out"
        self.messagesdel = "https://"+self.domain+"/cabinet/project/cabinet/forms/message.php?type=del"
        self.jurnal = "https://"+self.domain+"/cabinet/project/cabinet/modul/raspisanie/zanatie_jurnal.php"

    def timetable(self, week: int = 0):
        """
        Получение страницы с расписанием

        :param week:int. Номер недели
        :return: requests object
        """

        s = requests.Session()
        url = self.timetabl
        params = {}
        if week != 0:
            params.update({"week": week})
        r = s.get(url, params=params, cookies=self.jar, timeout=self.timeout)
        return r

    def profile(self):
        """

        :return:
        """
        s = requests.Session()
        url = self.profil
        r = s.get(url, cookies=self.jar, timeout=self.timeout)
        return r

    def msgin(self, page: int = 1):
        """

        :return:
        """
        s = requests.Session()
        url = self.messagesin+"&page="+str(page)
        r = s.get(url, cookies=self.jar, timeout=self.timeout)
        return r

    def msgout(self, page: int = 1):
        """

        :return:
        """
        s = requests.Session()
        url = self.messagesout+"&page="+str(page)
        r = s.get(url, cookies=self.jar, timeout=self.timeout)
        return r

    def msgdel(self):
        """

        :return:
        """
        s = requests.Session()
        url = self.messagesdel
        r = s.get(url, cookies=self.jar, timeout=self.timeout)
        return r


# get = BonchGetPage("f6214661f959a77cbae91776221dc59d")
# print(get.timetable(week=11).url)

