import requests as req
from requests import Response

from app.bonch import Settings


class BonchAuth:

    def __init__(self):
        settings = Settings
        self.link = "https://"+settings.domain.value+"/cabinet/lib/autentificationok.php?"
        self.login_link = "https://" + settings.domain.value + "/cabinet/"
        self.update_link = "https://" + settings.domain.value + "/cabinet/lib/updatesession.php"
        self.headers = settings.headers.value
        self.session = req.Session()
        self.user = {
            'login': '',
            'password': ''
        }

    @property
    def AUTH_MIN_CONTENT_LENGTH(self) -> int:
        return 300

    def sign_in(self, email: str, password: str) -> (int, str):
        """
        Авторизация пользователя. Точнее авторизация токена (miden) пользователем\n\r
        Пока нельзя выбрать свой токен((((

        :param email: str
        :param password: str
        :return: dict
        """

        self.user['login'] = email
        self.user['password'] = password
        data = tuple(self.user.values())

        url = self.link
        miden = self.__miden
        self.session.cookies.set('miden', miden, domain="lk.sut.ru", path="/")
        try:
            request = self.session.post(url, auth=data, headers=self.headers, timeout=Settings.timeout.value)
            if request.status_code == 200:
                # НЕ УДАЛЯТЬ!!!
                self.session.get(self.login_link, headers=self.headers, timeout=Settings.timeout.value)
                return (200, miden) if request.text == "1" else (401, "Не верные данные или вход запрещен")
            return 500
        except req.exceptions.ReadTimeout or req.exceptions.Timeout:
            return 523
        except Exception as e:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            return 500, message

    @property
    def __miden(self) -> str or None:
        """
        Получение токена для его авторизации
        """
        url = self.login_link
        r = req.get(url, headers=self.headers)
        if r.status_code == 200:
            return str(r.cookies['miden'])

    def auth_wrapper(self, r: Response or None) -> (int, Response.text or None):
        """
        Обертка для проверки на авторизацию\r\n
        Использовать только для страниц!!!
        """
        if r:
            if r.status_code == 200:
                if len(r.text) > self.AUTH_MIN_CONTENT_LENGTH:
                    return r.status_code, r.text
                else:
                    return 401, r.text
            else:
                return r.status_code, r.text
        else:
            return 500
