import requests as req
import json

from app.bonch import Settings


class BonchAuth:

    def __init__(self):
        self.link = "https://lk.sut.ru/cabinet/lib/autentificationok.php?"
        self.loginlink = "https://lk.sut.ru/cabinet/"
        self.updatelink = "https://lk.sut.ru/cabinet/lib/updatesession.php"

    def login(self, email: str, password: str, miden: str = ""):
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
        # вообще хз зачем здесь miden тк если кидать свой miden при авторизации то ничего не получится
        if miden == "":
            miden = self.getmiden()
        jar.set('miden', miden, domain="lk.sut.ru", path="/")
        try:
            r = s.get(url, cookies=jar, timeout=Settings.timeout)
            if r.status_code == 200:
                if r.text == "1":
                    s.get(self.loginlink+"?login=yes",  cookies=jar, timeout=Settings.timeout)
                    return {"status": 200, "miden": miden}
                elif r.text == "0":
                    return {"status": 401, "description": "Не все данные введены"}
                elif r.text.split("|") or len(r.text) < 300:
                    try:
                        for attention in  r.text.split("|"):
                            if attention.split("=")[0] == "error":
                                return {"status": 401, "description": "Не верные данные или вход запрещен"}
                    except IndexError:
                        pass
                    return {"status": 401, "description": "Не верные данные или вход запрещен"}
                else:
                    return {"status": 401, "description": "Не верные данные или вход запрещен"}
            elif r.status_code == 504:
                return {"status": 523}
        except req.exceptions.ReadTimeout or req.exceptions.Timeout:
            return {"status": 523}

    def getmiden(self):
        """
        Получение кук для авторизации

        :return: miden: str
        """
        # todo сделать обработки на все случаи жизни
        url = self.loginlink
        r = req.get(url, timeout=Settings.timeout)
        if r.status_code == 200:
            return str(r.cookies['miden'])

    def logout(self, miden: str):
        """
        разлогин токена от пользователя

        :param miden: токен
        :return: dict
        """
        # todo сделать обработки на все случаи жизни
        res = self.login('0', '0', miden)
        if res['status'] == 401:
            return {"status": 200}
        else:
            res



Auth = BonchAuth()
# res = BonchAuth.updatetoken("minikraft1212@gmail.com", "cocos1234", "7a7a43726437d194b8bc21610e56a6bb")
# res = BonchAuth.logout("6e7c1deeb07a737c4c0cf903c3991536")
# print(res)
# 34b8a38641d9a39e3cab8e350dbfcd7c 02:00
# BonchAuth.getmiden()
