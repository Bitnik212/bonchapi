from bs4 import BeautifulSoup as bs
import requests, json, io, time

from requests import Response

from bonch.BonchGetPage import BonchGetPage
from bonch import Settings
from bonch.msg.BonchMessageModel import BonchMessageModel
from bonch.msg.BonchMessageParser import BonchMessageParser


class BonchMessage:

    def __init__(self, miden: str):
        self.miden = miden
        self.bonch = BonchGetPage(self.miden)
        self.session = requests.Session()
        self.session.cookies.set('miden', miden, domain=self.domain, path="/")

    timeout = Settings.timeout.value
    headers = Settings.headers.value
    domain = Settings.domain.value
    link_sendto = "https://" + domain + "/cabinet/project/cabinet/forms/sendto2.php"
    link_message = "https://" + domain + "/cabinet/project/cabinet/forms/message.php"
    link_send_new_message = "https://" + domain + "/cabinet/project/cabinet/forms/message_create_stud.php"
    parse = BonchMessageParser()

    @staticmethod
    def message_auth_wrapper(r: Response) -> (int, str):
        if r.text == "":
            return 403, "Ошибка доступа"
        elif r.text.find("putsessionvalue") != -1:
            return 401, "Ошибка авторизации"
        else:
            return 200, r.text

    def __message_request(self, data: dict) -> (int, dict or str):
        r = self.session.post(
            url=self.link_sendto,
            data=data,
            headers=self.headers,
            timeout=self.timeout
        )
        status_code, response_text = self.message_auth_wrapper(r)
        if status_code == 200:
            return status_code, json.loads(r.text)
        else:
            return status_code, response_text

    def read(self, id: int) -> (int, dict or str):
        """
        Прочитать сообщение

        :param id: id сообщения
        :return: dict
        """
        data = {
            "id": id,
            "prosmotr": ""
        }
        try:
            return self.__message_request(data)
        except requests.exceptions.Timeout or requests.exceptions.ReadTimeout:
            return 523, "Не получилось получить страницу сообщений"

    def history(self, id: int) -> (int, str or dict):
        """
        Получение истории переписки

        :param id: id сообщения
        """
        data = {
            "id": id,
            "history_show": ""
        }
        try:
            return self.__message_request(data)
        except:
            return 500, "Не получилось получить историю сообщений"

    def new(self, title: str, message: str, destination_user: int, idinfo: int = 0) -> (int, str):
        """
        Отправка нового сообщения.\n\r
        Для удаления своего сообщения нужно \n\rtitle: '',  \n\rmessage: '', \n\ridinfo: вашего сообщения, \n\rdestinationuser: id адресата.\n
        Для редактирования своего сообщения нужно \n\rtitle: нужный новый текст,  \n\rmessage: нужный новый текст, \n\ridinfo: вашего сообщения, \n\rdestinationuser: id адресата.\n
        Свое сообщение - это сообщение, которые вы отправили.

        :param title: Загаловок сообщения
        :param message: Само сообщение
        :param idinfo: id сообщения
        :param destination_user: адресат
        :return: dict
        """
        data = {
            "idinfo": idinfo,
            "item": 0,
            "title": title.encode("windows-1251"),
            "mes_otvet": message.encode("windows-1251"),
            "adresat": destination_user,
            "saveotv": ""
        }
        url = self.link_message
        try:
            r = self.session.post(url, data=data, headers=self.headers, timeout=self.timeout)
            if len(r.text) < 290:
                return 401, "Ошибка авторизации"
            else:
                return 200, "Сообщение оправлено"
        except:
            return 500, "Не получилось получить страницу сообщений"

    def answer(self, message: str, destination_message: int, idinfo: int = 0) -> (int, str):
        """
        Ответить на сообщение

        :param message: Сообщение ответа
        :param destination_message: на какое сообщение отвечаем
        :param idinfo: файл(ы) если есть иначе 0
        :return: dict
        """
        data = {
            "idinfo": idinfo,
            "mes_otvet": message,
            "item": destination_message,
            "saveotv": ""
        }
        try:
            r = self.session.post(
                url=self.link_message,
                data=data,
                headers=self.headers,
                timeout=self.timeout
            )
            if len(r.text) > 280:
                return 401, "Ошибка авторизации"
            else:
                return r.status_code, "Сообщение отправлено"
        except:
            return 500, "Не получилось получить страницу сообщений"

    def upload_file(self, file: bytes, file_name: str, id: int = 0) -> (int, dict or str):
        """
        Загрузка файла

        :param file: bytes:  строка байтов
        :param file_name: str: Название файла
        :param id: int: куда его загрузить. Дефолт - 0
        :return: dist
        """
        file = io.BytesIO(file)
        file.name = file_name
        data = {
            "id": id,
            "upload": ""
        }
        try:
            r = self.session.post(
                url=self.link_send_new_message,
                files={"userfile": file},
                data=data,
                headers=self.headers,
                timeout=self.timeout + 10
            )
            if len(r.text) > 280:
                return 401, "Ошибка авторизации"
            if r.status_code == 200:
                text = str(bs(r.text, Settings.bs_parser_type.value))
                is_error = text.find("Ошибка доступа") != -1
                is_big_size = text.find('data.idinfo') == -1

                if is_error is False and is_big_size is False:
                    temp1 = text[text.find('data.idinfo') + 5 + 6 + 4:]
                    idinfo = bs(temp1[:temp1.find('"')], Settings.bs_parser_type.value).text
                    idinfo = int(idinfo)
                    return_data = {
                        "name": file_name,
                        "link": self.__get_file_link_by_idinfo(idinfo=idinfo, file_name=file_name),
                        "idinfo": idinfo
                    }
                    return r.status_code, return_data
                elif is_big_size:
                    return 403, "Файл больше 5мб"
                else:
                    return 403, "Ошибка доступа"
            else:
                return r.status_code, "ошибка"
        except:
            return 500, "Произошла ошибка"

    def __get_file_link_by_idinfo(self, idinfo: int, file_name: str) -> str:
        return "https://" + self.domain + "/cabinet/ini/subconto/sendto/101/" + str(idinfo) + "/" + file_name

    def messages_in(self, page_start: int = 1, page_end: int = 2, page: int = 0) -> (int, list[BonchMessageModel] or str):
        """
        Получение входящих сообщений на определенной странице.
        Можно указать кокретную страницу либо указать с какой по какую.
        """
        resp = []
        if bool(page) is False:
            for page_number in range(page_start, page_end):
                r = self.bonch.messages_in_response(page_number)
                if r:
                    soup = bs(r.text, Settings.bs_parser_type.value)
                    msgs = self.parse.messages(soup)
                    if msgs:
                        for msg in msgs:
                            resp.append(msg)
                time.sleep(.5)
        else:
            r = self.bonch.messages_in_response(page)
            soup = bs(r.text, Settings.bs_parser_type.value)
            resp = self.parse.messages(soup)
        if resp:
            return 200, resp
        else:
            return 404, "Нет сообщений"

    def messages_out(self, page_start: int = 1, page_end: int = 2, page: int = 0):
        resp = []
        if bool(page) is False:
            for page_number in range(page_start, page_end):
                r = self.bonch.messages_out_response(page_number)
                if r:
                    soup = bs(r.text, Settings.bs_parser_type.value)
                    msgs = self.parse.messages(soup)
                    if msgs:
                        for msg in msgs:
                            resp.append(msg)
        else:
            r = self.bonch.messages_out_response(page)
            soup = bs(r.text, Settings.bs_parser_type.value)
            resp = self.parse.messages(soup)
        if resp:
            return 200, resp
        else:
            return 500, "Не получилось получить страницу сообщений"

    def messages_deleted(self, page_start: int = 1, page_end: int = 2, page: int = 0):
        resp = []
        if bool(page) is False:
            for page_number in range(page_start, page_end):
                r = self.bonch.messages_delete_response(page_number)
                if r:
                    soup = bs(r.text, Settings.bs_parser_type.value)
                    msgs = self.parse.messages(soup)
                    if msgs:
                        for msg in msgs:
                            resp.append(msg)
        else:
            r = self.bonch.messages_delete_response(page)
            soup = bs(r.text, Settings.bs_parser_type.value)
            resp = self.parse.messages(soup)
        if resp:
            return 200, resp
        else:
            return 404, "Нет сообщений"


"""
при просмотре сообщения
    "itemnumber": "0",   id предыдущего сообщения. если нет то "0"
    "annotation": "текст",   содержание сообщения
    "name": "Основы экономики",   Загаловок
    "viddok": "mes_prep",    хз что это
    "otvet": 1,  можно ли ответить на это сообщение
    "idinfo": 0,     хз что это. просто по дефолту. это id для файлов
    "files": "",     файлы. обычно их нет
    "sendto": 1305015,   id сообщения
    "history": 0     есть (1) история или нет (0)


iditem id сообщения

ответ на сообщение 
item: 1305359 само сообщение
idinfo: 1305769 сообщение с файлом
mes_otvet:  видимо текст для ответа
saveotv: 

ответ на ответ
<Script Language="JavaScript">var data = new Object;var data2 ='';data.exceptions = "";data.iditem = "1305359";data.idinfo = "1305769";data.name = "reshitzadachy_virychkazagodsostavila_30000t5.docx";window.parent.handleResponse(data);</Script>


"""
