import requests
from requests import Response

from bonch import Settings


class BonchGetPage:
    def __init__(self, miden: str):
        """
        Инициализация класса

        :param miden: str - токен
        """
        self.headers = Settings.headers.value
        self.domain = Settings.domain.value
        self.jar = requests.cookies.RequestsCookieJar()
        self.jar.set('miden', miden, domain=self.domain, path="/")
        self.timeout = Settings.timeout.value
        self.home_link = "https://lk.sut.ru/cabinet/"
        self.auth_link = "https://" + self.domain + "/cabinet/lib/autentificationok.php?"
        self.login_link = "https://" + self.domain + "/cabinet/?login=yes"
        self.update_miden_link = "https://" + self.domain + "/cabinet/lib/updatesession.php"
        self.timetable_link = "https://" + self.domain + "/cabinet/project/cabinet/forms/raspisanie_bak.php"
        self.vedomosty_link = "https://" + self.domain + "/cabinet/project/cabinet/forms/vedomost.php"
        self.zachetka_link = "https://" + self.domain + "/cabinet/project/cabinet/forms/zachetka.php"
        self.uch_grafik_link = "https://" + self.domain + "/cabinet/project/cabinet/forms/uch_grafik.php"
        self.facultativ_link = "https://" + self.domain + "/cabinet/project/cabinet/forms/fakultativ.php"
        self.dolg_link = "https://" + self.domain + "/cabinet/project/cabinet/forms/dolg.php"
        self.prikazi_link = "https://" + self.domain + "/cabinet/project/cabinet/forms/prikazs.php"
        self.portfolio_link = "https://" + self.domain + "/cabinet/project/cabinet/forms/portfolio.php"
        self.group_files_link = "https://" + self.domain + "/cabinet/project/cabinet/forms/files_group_pr.php"
        self.jurnal_link = "https://" + self.domain + "/cabinet/project/cabinet/forms/jurnal_dnevnik.php"
        self.profile_link = "https://" + self.domain + "/cabinet/project/cabinet/forms/profil.php"
        self.settings_link = "https://" + self.domain + "/cabinet/project/cabinet/forms/nastroyki.php"
        self.change_password_link = "https://" + self.domain + "/cabinet/project/cabinet/forms/change.php"
        self.services_link = "https://" + self.domain + "/cabinet/project/cabinet/forms/wifi.php"
        self.ump_link = "https://" + self.domain + "/cabinet/project/cabinet/forms/ump.php"
        self.library_link = "https://" + self.domain + "/cabinet/project/cabinet/forms/library.php"
        self.messages_in_link = "https://" + self.domain + "/cabinet/project/cabinet/forms/message.php?type=in"
        self.messages_out_link = "https://" + self.domain + "/cabinet/project/cabinet/forms/message.php?type=out"
        self.messages_delete_link = "https://" + self.domain + "/cabinet/project/cabinet/forms/message.php?type=del"
        self.zanatie_jurnal_link = "https://" + self.domain + "/cabinet/project/cabinet/modul/raspisanie/zanatie_jurnal.php"

    def timetable_response(self, week: int = 0) -> Response or None:
        """
        Получение страницы с расписанием

        :param week:int. Номер недели
        :return: requests object
        """
        if week:
            params = {"week": week}
        else:
            params = {}
        try:
            return requests.Session().get(
                url=self.timetable_link,
                params=params,
                headers=self.headers,
                cookies=self.jar,
                timeout=self.timeout
            )
        except:
            return None

    def profile_response(self) -> Response or None:
        try:
            return requests.Session().get(
                url=self.profile_link,
                cookies=self.jar,
                headers=self.headers,
                timeout=self.timeout
            )
        except:
            return None

    def messages_in_response(self, page: int = 1) -> Response or None:
        try:
            return requests.Session().get(
                url=self.messages_in_link + "&page=" + str(page),
                cookies=self.jar,
                timeout=self.timeout,
                headers=self.headers
            )
        except:
            return None

    def messages_out_response(self, page: int = 1) -> Response or None:
        try:
            return requests.Session().get(
                url=self.messages_out_link + "&page=" + str(page),
                cookies=self.jar,
                timeout=self.timeout,
                headers=self.headers
            )
        except:
            return None

    def messages_delete_response(self, page: int = 1) -> Response or None:
        try:
            return requests.Session().get(
                url=self.messages_delete_link + "&page=" + str(page),
                cookies=self.jar,
                timeout=self.timeout,
                headers=self.headers
            )
        except:
            return None
