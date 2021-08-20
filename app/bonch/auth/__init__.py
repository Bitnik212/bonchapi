import requests as req
import json

from bonch import Settings


class BonchAuth:

    def __init__(self):
        settings = Settings
        self.link = "https://"+settings.domain.value+"/cabinet/lib/autentificationok.php?"
        self.loginlink = "https://"+settings.domain.value+"/cabinet/"
        self.updatelink = "https://"+settings.domain.value+"/cabinet/lib/updatesession.php"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/92.0.4515.131 Safari/537.36 "
        }

    def sign_in(self, email: str, password: str, miden: str or None = None) -> (int, str):
        """
        Авторизация пользователя. Точнее авторизация токена (miden) пользователем\n\r
        Пока нельзя выбрать свой токен((((

        :param email: str
        :param password: str
        :param miden: str = ""
        :return: dict
        """
        # todo не срабатывает обработка на 504 от бонча
        s = req.Session()
        url = self.link+"users="+email+"&parole="+password
        jar = req.cookies.RequestsCookieJar()
        if miden is None:
            miden = self.__miden
        jar.set('miden', miden, domain="lk.sut.ru", path="/")
        try:
            r = s.post(url, cookies=jar, headers=self.headers, timeout=Settings.timeout.value)
            if r.status_code == 200:
                if r.text == "1":
                    s.get(self.loginlink+"?login=yes", headers=self.headers,  cookies=jar, timeout=Settings.timeout.value)
                    return 200, miden
                elif r.text == "0":
                    return 401, "Не все данные введены"
                elif r.text.split("|") or len(r.text) < 300:
                    try:
                        for attention in  r.text.split("|"):
                            if attention.split("=")[0] == "error":
                                return  401, "Не верные данные или вход запрещен"
                    except IndexError:
                        pass
                    return 401, "Не верные данные или вход запрещен"
                else:
                    return 401, "Не верные данные или вход запрещен"
            elif r.status_code == 504:
                return 523
        except req.exceptions.ReadTimeout or req.exceptions.Timeout:
            return 523

    @property
    def __miden(self) -> str or None:
        """
        Получение токена для его авторизации
        """
        # todo сделать обработки на все случаи жизни
        url = self.loginlink
        r = req.get(url, headers=self.headers)
        if r.status_code == 200:
            miden = str(r.cookies['miden'])
            return miden

    # def logout(self, miden: str):
    #     """
    #     разлогин токена от пользователя
    #
    #     :param miden: токен
    #     :return: dict
    #     """
    #     # todo сделать обработки на все случаи жизни
    #     res = self.sign_in('0', '0', miden)
    #     if res['status'] == 401:
    #         return {"status": 200}



# auth = BonchAuth()
# res = auth.sign_in("minikraft1212@gmail.com", "cocos1234")
# print(res)
# res = BonchAuth.updatetoken("minikraft1212@gmail.com", "cocos1234", "7a7a43726437d194b8bc21610e56a6bb")
# res = BonchAuth.logout("6e7c1deeb07a737c4c0cf903c3991536")
# print(res) AnanasCocos123
# 34b8a38641d9a39e3cab8e350dbfcd7c 02:00
# BonchAuth.getmiden()
