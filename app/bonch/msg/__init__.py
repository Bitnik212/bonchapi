from bs4 import BeautifulSoup as bs
import requests
import json
import io

from app.bonch.BonchGetPage import BonchGetPage
from app.bonch import Settings


class BonchMessage:

    def __init__(self, miden: str):
        """

        :param miden:
        """
        self.miden = miden
        self.domain = Settings.domain
        self.timeout = Settings.timeout
        self.cookies = requests.cookies.RequestsCookieJar()
        self.cookies.set('miden', miden, domain=self.domain, path="/")
        self.sendto = "https://"+self.domain+"/cabinet/project/cabinet/forms/sendto2.php"
        self.message = "https://lk.sut.ru/cabinet/project/cabinet/forms/message.php"
        self.sendnewmsg = "https://lk.sut.ru/cabinet/project/cabinet/forms/message_create_stud.php"

    def read(self, id: int):
        """
        Прочитать сообщение

        :param id: id сообщения
        :return: dict
        """
        # done Сделать все остальные обработки на все случаи жизни
        data = {
            "id": id,
            "prosmotr": ""
        }
        s = requests.Session()
        url = self.sendto
        try:
            r = s.post(url, data=data, cookies=self.cookies, timeout=self.timeout)
            if len(r.text) < 400:
                return {'status': 401}
            else:
                return {"status": 200, "responce": json.loads(r.text)}
        except requests.exceptions.Timeout or requests.exceptions.ReadTimeout:
            return {"status": 523}

    def gethistory(self, id: int):
        """
        Получение истории переписки

        :param id:
        :return: dict
        """
        # todo Сделать все остальные обработки на все случаи жизни
        data = {
            "id": id,
            "history_show": ""
        }
        s = requests.Session()
        url = self.sendto
        r = s.post(url, data=data, cookies=self.cookies, timeout=self.timeout)
        if r.text == "":
            return {"status": 401}
        else:
            return {"status": 200, "responce": json.loads(r.text)}

    def newmessage(self, title: str, message: str, destinationuser: int, idinfo: int = 0):
        """
        Отправка нового сообщения.\n\r
        Для удаления своего сообщения нужно \n\rtitle: '',  \n\rmessage: '', \n\ridinfo: вашего сообщения, \n\rdestinationuser: id адресата.\n
        Для редактирования своего сообщения нужно \n\rtitle: нужный новый текст,  \n\rmessage: нужный новый текст, \n\ridinfo: вашего сообщения, \n\rdestinationuser: id адресата.\n
        Свое сообщение - это сообщение, которые вы отправили.

        :param title: Загаловок сообщения
        :param message: Само сообщение
        :param idinfo: id сообщения
        :param destinationuser: адресат
        :return: dict
        """
        # todo Сделать все остальные обработки на все случаи жизни
        data = {
            "idinfo": idinfo,
            "title": title,
            "mes": message,
            "adresat": destinationuser
        }
        s = requests.Session()
        url = self.sendnewmsg
        r = s.post(url, data=data, cookies=self.cookies, timeout=self.timeout)
        # print(r.text)
        print(r)

    def answermessage(self, message: str, destinationmsg: int, idinfo: int = 0):
        """
        Ответить на сообщение

        :param message: Сообщение ответа
        :param destinationmsg: на какое сообщение отвечаем
        :param idinfo: файл(ы) если есть иначе 0
        :return: dict
        """
        data = {
            "idinfo": idinfo,
            "mes_otvet": message,
            "item": destinationmsg,
            "saveotv": ""
        }
        s = requests.Session()
        url = self.message
        r = s.post(url, data=data, cookies=self.cookies, timeout=self.timeout)
        print(r.text)
        print(r)

    def delmessage(self, destinationuser: int, idinfo: int = 0):
        """
        Удаление сообщения. если он без файла

        :param destinationuser: адресат
        :param idinfo: id сообщения
        :return:
        """
        # todo Сделать все остальные обработки на все случаи жизни
        res = self.newmessage('', '', destinationuser, idinfo)
        return res

    def uploadfile(self, file: bytes, file_name: str, id: int = 0):
        """
        Загрузка файла

        :param file: bytes:  строка байтов
        :param file_name: str: строка байтов
        :param id: int: куда его загрузить. Дефолт - 0
        :return: dist
        """
        # temp_file = io.open(file, 'rb', buffering = 0)
        file = io.BytesIO(file)
        file.name = file_name
        data = {
            "id": id,
            "upload": ""
        }
        s = requests.Session()
        url = self.sendnewmsg
        r = s.post(url, files={"userfile": file}, data=data,  cookies=self.cookies, timeout=self.timeout+10)
        soup = bs(r.text, "html.parser")
        text = soup.script.text
        print(text)
        temp1 = text[text.find('data.exceptions')+4+7+4:]
        error = bs(temp1[:temp1.find('"')], "html.parser").text
        print("error", error == "")
        # temp1 = text[text.find('data2+=')+5+4:]
        # data = bs(temp1[:temp1.find('"')], "html.parser").text
        # print("data", data)
        temp1 = text[text.find('data.idinfo')+5+6+4:]
        idinfo = bs(temp1[:temp1.find('"')], "html.parser").text
        print("idinfo", idinfo)

        return r.text

    def getmsgsin(self, page_end: int = 1, page_start: int = 1):
        """
        Получение входящих сообщений на определенной странице
        :return: dict
        """
        # todo Сделать определение количества страниц и какая сейчас
        for page_number in range(page_end):
            pass
        r = BonchGetPage(self.miden).msgin(page_start)
        soup = bs(r.text, "html.parser")
        resp = self.getmsgsinparser(soup)
        for msg in resp:
            print(msg)
        return {"status": 200, "responce": resp}


    def getmsgsinparser(self, soup):
        """
        парсер
        :param soup:
        :return: list
        """
        table = soup.find("table", attrs={"class": "simple-little-table"})
        msgs = []
        for msg in table.tbody.find_all("tr"):
            # print("-"*80)
            try:
                int(msg["id"].replace("tr_", ""))
                msgs.append(self.parsemsg(msg))
            except:
                continue
        return msgs

    def getmsgsout(self, amount: int = 20):
        """

        :return:
        """

    def getmsgsdel(self, amount: int = 20):
        """

        :return:
        """

    def parsemsg(self, soup):
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




# msg = BonchMessage("05575093cd69fc6efc27a00f8802d44e")
# msg.getmsgsin(1)
# print(msg.uploadfile(io.open("/home/bit/meme/bit/Загрузки/i33M4UvBjMo.jpg", 'rb').read(), "meme.jpg", 110945))
# print(msg.answermessage('Test2', 1306151))
# for tt in msg.getfullhistory(1303656)['chainraw']:
#     print("tt", tt['itemnumber'])
# msg.newmessage('', '', 97220, 1306186)



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



