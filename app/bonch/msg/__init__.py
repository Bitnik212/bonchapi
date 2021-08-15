from bs4 import BeautifulSoup as bs
import requests
import json
import io

from bonch.BonchGetPage import BonchGetPage
from bonch import Settings


class BonchMessage:

    def __init__(self, miden: str):
        """

        :param miden:
        """
        self.miden = miden
        self.domain = Settings.domain.value
        self.timeout = Settings.timeout.value
        self.bonch = BonchGetPage(self.miden)
        self.headers=Settings.headers.value
        self.cookies = requests.cookies.RequestsCookieJar()
        self.cookies.set('miden', miden, domain=self.domain, path="/")
        self.link_sendto = "https://" + self.domain + "/cabinet/project/cabinet/forms/sendto2.php"
        self.link_message = "https://" + self.domain + "/cabinet/project/cabinet/forms/message.php"
        self.link_send_new_message = "https://" + self.domain + "/cabinet/project/cabinet/forms/message_create_stud.php"

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
            r = requests.Session().post(
                url=self.link_sendto,
                data=data,
                headers=self.headers,
                cookies=self.cookies,
                timeout=self.timeout
            )
            if len(r.text) < 400:
                return 401, "Ошибка доступа"
            else:
                return 200, json.loads(r.text)
        except requests.exceptions.Timeout or requests.exceptions.ReadTimeout:
            return 523, "Не получилось получить страницу сообщений"

    def get_history(self, id: int) -> (int, str):
        """
        Получение истории переписки

        :param id:
        :return: dict
        """
        data = {
            "id": id,
            "history_show": ""
        }
        try:
            r = requests.Session().post(
                url=self.link_sendto,
                data=data,
                headers=self.headers,
                cookies=self.cookies,
                timeout=self.timeout
            )
            if r.text == "":
                return 401, "Ошибка доступа"
            else:
                return 200, json.loads(r.text)
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
            "title": title,
            "mes_otvet": message,
            "adresat": destination_user,
            "saveotv": ""
        }
        s = requests.Session()
        url = self.link_message
        try:
            s.post(url, data=data, cookies=self.cookies, headers=self.headers, timeout=self.timeout)
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
            r = requests.Session().post(
                url=self.link_message,
                data=data,
                cookies=self.cookies,
                headers=self.headers,
                timeout=self.timeout
            )
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
            r = requests.Session().post(
                url=self.link_send_new_message,
                files={"userfile": file},
                data=data,
                headers=self.headers,
                cookies=self.cookies,
                timeout=self.timeout + 10
            )
            if r.status_code == 200:
                text = str(bs(r.text, "html.parser"))
                is_error = text.find("Ошибка доступа") != -1
                is_big_size = text.find('data.idinfo') == -1

                if is_error is False and is_big_size is False:
                    temp1 = text[text.find('data.idinfo') + 5 + 6 + 4:]
                    idinfo = bs(temp1[:temp1.find('"')], "html.parser").text
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

    def get_messages_in(self, page_start: int = 1, page_end: int = 2, page: int = 0) -> (int, list[dict]):
        """
        Получение входящих сообщений на определенной странице.
        Можно указать кокретную страницу либо указать с какой по какую.
        """
        resp = []
        if bool(page) is False:
            for page_number in range(page_start, page_end):
                r = self.bonch.messages_in_response(page_number)
                if r:
                    soup = bs(r.text, "html.parser")
                    for msg in self.__messages_parser(soup):
                        resp.append(msg)
        else:
            r = self.bonch.messages_in_response(page)
            soup = bs(r.text, "html.parser")
            resp = self.__messages_parser(soup)
        if resp:
            return 200, resp
        else:
            return 500, "Не получилось получить страницу сообщений"

    def __messages_parser(self, soup) -> list[dict]:
        """
        парсер
        """
        table = soup.find("table", attrs={"class": "simple-little-table"})
        msgs = []
        for msg in table.tbody.find_all("tr"):
            try:
                int(msg["id"].replace("tr_", ""))
                msgs.append(self.__parse_message(msg))
            except:
                continue
        return msgs

    def get_messages_out(self, page_start: int = 1, page_end: int = 2, page: int = 0):
        resp = []
        if bool(page) is False:
            for page_number in range(page_start, page_end):
                r = self.bonch.messages_out_response(page_number)
                if r:
                    soup = bs(r.text, "html.parser")
                    for msg in self.__messages_parser(soup):
                        resp.append(msg)
        else:
            r = self.bonch.messages_out_response(page)
            soup = bs(r.text, "html.parser")
            resp = self.__messages_parser(soup)
        if resp:
            return 200, resp
        else:
            return 500, "Не получилось получить страницу сообщений"

    def get_messages_deleted(self, page_start: int = 1, page_end: int = 2, page: int = 0):
        resp = []
        if bool(page) is False:
            for page_number in range(page_start, page_end):
                r = self.bonch.messages_delete_response(page_number)
                if r:
                    soup = bs(r.text, "html.parser")
                    for msg in self.__messages_parser(soup):
                        resp.append(msg)
        else:
            r = self.bonch.messages_delete_response(page)
            soup = bs(r.text, "html.parser")
            resp = self.__messages_parser(soup)
        if resp:
            return 200, resp
        else:
            return 500, "Не получилось получить страницу сообщений"

    @staticmethod
    def __parse_message(soup):
        """

        :param soup:
        :return:
        """
        tempid = soup["id"].replace("tr_", "")
        temppid = soup.find_all("td")[0]["onclick"].split("(")[1].replace(");", "")
        global id, readed
        id = 0
        if tempid == temppid:
            id = tempid
        trs = soup.find_all("td")
        readed = True
        try:
            if (soup["style"] == "font-weight: bold !important;"):
                readed = False
        except:
            pass
        date = trs[0].text.split(" ")
        time = trs[0].small.text
        date = date[0]
        title = trs[1].text.replace("\n", "").replace("\r", "").replace("  ", "")
        if title[0:1] == " ":
            title = title[1:]
        files = []
        for file in trs[2].find_all("a"):
            files.append({"name": file.text, "href": file["href"]})
        sender = trs[3].text
        return (
            {
                "id": int(id),
                "readed": readed,
                "sender": sender,
                "date": date,
                "time": time,
                "title": title,
                "files": files
            }
        )



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
