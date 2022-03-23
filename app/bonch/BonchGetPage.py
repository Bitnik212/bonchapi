import requests
from app.bonch import Settings


class BonchGetPage:
    def __init__(self, miden: str):
        """
        Инициализация класса

        :param miden: str - токен
        """
        self.jar = requests.cookies.RequestsCookieJar()
        self.jar.set('miden', miden, domain=self.domain, path="/")

    headers = Settings.headers.value
    timeout = Settings.timeout.value
    domain = Settings.domain.value
    home_link = "https://lk.sut.ru/cabinet/"
    auth_link = "https://" + domain + "/cabinet/lib/autentificationok.php?"
    login_link = "https://" + domain + "/cabinet/?login=yes"
    update_miden_link = "https://" + domain + "/cabinet/lib/updatesession.php"
    timetable_link = "https://" + domain + "/cabinet/project/cabinet/forms/raspisanie_bak.php"
    vedomosty_link = "https://" + domain + "/cabinet/project/cabinet/forms/vedomost.php"
    zachetka_link = "https://" + domain + "/cabinet/project/cabinet/forms/zachetka.php"
    uch_grafik_link = "https://" + domain + "/cabinet/project/cabinet/forms/uch_grafik.php"
    facultativ_link = "https://" + domain + "/cabinet/project/cabinet/forms/fakultativ.php"
    dolg_link = "https://" + domain + "/cabinet/project/cabinet/forms/dolg.php"
    prikazi_link = "https://" + domain + "/cabinet/project/cabinet/forms/prikazs.php"
    portfolio_link = "https://" + domain + "/cabinet/project/cabinet/forms/portfolio.php"
    group_files_link = "https://" + domain + "/cabinet/project/cabinet/forms/files_group_pr.php"
    jurnal_link = "https://" + domain + "/cabinet/project/cabinet/forms/jurnal_dnevnik.php"
    profile_link = "https://" + domain + "/cabinet/project/cabinet/forms/profil.php"
    settings_link = "https://" + domain + "/cabinet/project/cabinet/forms/nastroyki.php"
    change_password_link = "https://" + domain + "/cabinet/project/cabinet/forms/change.php"
    services_link = "https://" + domain + "/cabinet/project/cabinet/forms/wifi.php"
    ump_link = "https://" + domain + "/cabinet/project/cabinet/forms/ump.php"
    library_link = "https://" + domain + "/cabinet/project/cabinet/forms/library.php"
    messages_in_link = "https://" + domain + "/cabinet/project/cabinet/forms/message.php?type=in"
    messages_out_link = "https://" + domain + "/cabinet/project/cabinet/forms/message.php?type=out"
    messages_delete_link = "https://" + domain + "/cabinet/project/cabinet/forms/message.php?type=del"
    zanatie_jurnal_link = "https://" + domain + "/cabinet/project/cabinet/modul/raspisanie/zanatie_jurnal.php"

    def timetable_response(self, week: int = 0) -> Response or None:
        """
        Получение страницы с расписанием

        :param week:int. Номер недели
        :return: requests object
        """
        if bool(week):
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
